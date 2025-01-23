import os
import subprocess
import time
import getpass
from pyngrok import ngrok

# Change directory to Colab's working directory
os.chdir('/content')
print(f"Current working directory: {os.getcwd()}")

# Set environment variables for Ollama
os.environ['OLLAMA_HOST'] = "0.0.0.0"
os.environ['OLLAMA_ORIGINS'] = "*"

# Function to run commands with error checking
def run_command(command):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for line in process.stdout:
        print(line.strip())
    return process.wait()

# Install Ollama
print("Installing Ollama...")
run_command("curl -fsSL https://ollama.com/install.sh | sh")

# Start Ollama server in the background
print("Starting Ollama server...")
run_command("nohup ollama serve > /dev/null 2>&1 &")
time.sleep(5)  # Wait for server initialization

# Pull the Deepseek model
print("Pulling Deepseek model...")
run_command("ollama pull deepseek-r1")

# Install pyngrok
print("Installing pyngrok...")
run_command("pip install pyngrok")

# Set up ngrok
print("Setting up ngrok...")
ngrok_token = getpass.getpass('Enter your ngrok authtoken: ')
run_command(f"ngrok authtoken {ngrok_token}")

# Start ngrok tunnel to Ollama
print("Starting ngrok tunnel...")
try:
    public_url = ngrok.connect(addr="127.0.0.1:11434", proto="http").public_url
    print(f"Ollama API is now available at: {public_url}")
except Exception as e:
    print(f"Failed to start ngrok tunnel: {e}")

# Keep the script running
print("Setup complete! The server will remain active for 5 hours.")
print(f"Access your Ollama server at: {public_url}")
time.sleep(5 * 60 * 60)  # Keep alive for 5 hours
