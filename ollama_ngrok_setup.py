import os
import subprocess
import time
import getpass
from pyngrok import ngrok

# Change directory to the working directory
os.chdir('/kaggle/working/')
print(f"Current working directory: {os.getcwd()}")

# Set environment variables for Ollama
os.environ['OLLAMA_HOST'] = "0.0.0.0"
os.environ['OLLAMA_ORIGINS'] = "*"

# Function to run commands and check for errors
def run(commands):
    for command in commands:
        with subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,  # Use text mode to avoid binary mode issues
            bufsize=1,  # Line buffering is supported in text mode
            universal_newlines=True  # Ensure compatibility with text mode
        ) as sp:
            for line in sp.stdout:
                if "undefined reference" in line:
                    raise RuntimeError("Failed Processing.")
                print(line, flush=True, end="")

# Start the Ollama server in the background and add a short delay
print("Starting Ollama server...")
os.system("/usr/local/bin/ollama serve &")
time.sleep(5)  # Give the server some time to start

# Run the echo command
os.system("echo 'ollama test'")

# Install Ollama
print("Installing Ollama...")
commands = [
    "curl -fsSL https://ollama.com/install.sh | sh",
]
run(commands)

# Create a custom Ollama model file
print("Creating custom Ollama model file...")
with open('/kaggle/working/ModelFilesabs', 'w') as f:
    f.write("FROM llama3\nPARAMETER num_ctx=32768\n")

# Pull the Deepseek model
print("Pulling Deepseek model...")
commands = [
    "ollama pull deepseek-r1:14b"
]
run(commands)

# Install Nginx
print("Installing Nginx...")
commands = [
    "apt install nginx -y"
]
run(commands)

# Configure Nginx for Ollama
print("Configuring Nginx for Ollama...")
nginx_config = """
server {
    listen 80;
    server_name *.ngrok-free.app;

    location / {
        proxy_pass http://localhost:11434;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
"""
with open('/etc/nginx/conf.d/ollamasvc.conf', 'w') as f:
    f.write(nginx_config)

# Install pyngrok and ngrok
print("Installing pyngrok and ngrok...")
os.system("!pip install pyngrok ngrok --force")

# Prompt for the Ngrok token
ngrok_token = getpass.getpass('Enter your Ngrok access token and press enter: ')

# Set the Ngrok authtoken
print("Setting Ngrok authtoken...")
commands = [
    f"ngrok authtoken {ngrok_token}"
]
run(commands)

# Connect Ngrok to expose the Ollama server
print("Starting Ngrok tunnel...")
listener = ngrok.connect(addr="localhost:80", metadata="Ollama server")
print(f"Please click on the text below to access the Ollama server: {listener}")

# Restart Nginx to apply the configuration
print("Restarting Nginx...")
os.system("sudo /etc/init.d/nginx stop")
os.system("sudo /etc/init.d/nginx start")

print("Setup complete! Ollama server is running and accessible via Ngrok.")
