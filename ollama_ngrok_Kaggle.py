import os
import subprocess
import time
import getpass
from pyngrok import ngrok

# Change directory to the working directory
def change_working_directory(path='/kaggle/working/'):
    """Change the current working directory."""
    try:
        os.chdir(path)
        print(f"Current working directory: {os.getcwd()}")
    except Exception as e:
        print(f"Error changing directory: {e}")

# Set environment variables for Ollama
def set_ollama_env_vars():
    """Set environment variables required for Ollama."""
    os.environ['OLLAMA_HOST'] = "0.0.0.0"
    os.environ['OLLAMA_ORIGINS'] = "*"
    print("Environment variables set for Ollama.")

# Function to run shell commands
def run_commands(commands):
    """Run a list of shell commands and print their output."""
    for command in commands:
        print(f"Running command: {command}")
        with subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        ) as sp:
            for line in sp.stdout:
                if "undefined reference" in line: # Keep this error check if relevant to your commands
                    raise RuntimeError("Failed Processing.")
                print(line, flush=True, end="")

# Start the Ollama server using subprocess
def start_ollama_server():
    """Start the Ollama server in the background using subprocess and check for errors."""
    print("Starting Ollama server...")
    try:
        ollama_process = subprocess.Popen(
            ["/usr/local/bin/ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(5) # Initial short sleep to let it start a bit

        # Check for errors during startup in the first few seconds
        if ollama_process.poll() is not None: # Process has exited
            stderr_output = ollama_process.stderr.read()
            if stderr_output:
                print(f"Error starting Ollama server:\n{stderr_output}")
                raise Exception(f"Ollama server failed to start. Check error output above.")
            else:
                print("Ollama server started but exited unexpectedly without error message.")
                raise Exception("Ollama server failed to start.")

        print("Ollama server started in background (hopefully). Checking readiness...")

    except Exception as e:
        print(f"Failed to start Ollama server: {e}")
        raise

# Wait for the Ollama server to be ready (improved with timeout and better logging)
def wait_for_ollama_server():
    """Wait for the Ollama server to become available."""
    print("Waiting for Ollama server to start...")
    timeout_seconds = 120  # Increased timeout to 120 seconds (2 minutes)
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout_seconds:
            raise TimeoutError("Timeout waiting for Ollama server to start.")
        try:
            response = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/version"], # Check API endpoint
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"curl return code: {response.returncode}") # Print return code
            print(f"curl stdout: {response.stdout.strip()}")   # Print stdout (stripped whitespace)
            print(f"curl stderr: {response.stderr.strip()}")   # Print stderr (stripped whitespace)

            if response.returncode == 0 and "version" in response.stdout: # Check for "version" in API response
                print("Ollama server is ready (API endpoint reachable)!")
                break
            else:
                print("Ollama server not yet ready (API check failed).") # More informative message

        except Exception as e:
            print(f"Error checking Ollama server: {e}")
        time.sleep(2) # Slightly increased sleep in the loop

# Install Ollama
def install_ollama():
    """Install Ollama using the official installation script."""
    print("Installing Ollama...")
    commands = [
        "curl -fsSL https://ollama.com/install.sh | sh",
    ]
    run_commands(commands)
    print("Ollama installation complete.")

# Create a custom Ollama model file
def create_custom_model_file():
    """Create a custom Ollama model file."""
    print("Creating custom Ollama model file...")
    with open('/kaggle/working/ModelFilesabs', 'w') as f:
        f.write("FROM llama3\nPARAMETER num_ctx=32768\n")
    print("Custom Ollama model file created.")

# Pull the Deepseek model
def pull_model(model_name="qwen2.5-coder"):
    """Pull the specified model using Ollama."""
    print(f"Pulling model: {model_name}...")
    commands = [
        f"ollama pull {model_name}"
    ]
    run_commands(commands)
    print(f"Model {model_name} pulled successfully.")

# Install Nginx
def install_nginx():
    """Install Nginx."""
    print("Installing Nginx...")
    commands = [
        "apt update",
        "apt install nginx -y"
    ]
    run_commands(commands)
    print("Nginx installed successfully.")

# Configure Nginx for Ollama
def configure_nginx():
    """Configure Nginx to proxy requests to the Ollama server."""
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
    print("Nginx configuration updated.")

# Install pyngrok and ngrok
def install_ngrok():
    """Install pyngrok and ngrok."""
    print("Installing pyngrok and ngrok...")
    os.system("!pip install pyngrok ngrok --force")
    print("pyngrok and ngrok installed successfully.")

# Set Ngrok authtoken
def set_ngrok_authtoken():
    """Set the Ngrok authtoken."""
    ngrok_token = getpass.getpass('Enter your Ngrok access token and press enter: ')
    print("Setting Ngrok authtoken...")
    commands = [
        f"ngrok authtoken {ngrok_token}"
    ]
    run_commands(commands)
    print("Ngrok authtoken set successfully.")

# Connect Ngrok to expose the Ollama server
def connect_ngrok():
    """Connect Ngrok to expose the Ollama server."""
    print("Starting Ngrok tunnel...")
    listener = ngrok.connect(addr="localhost:80", metadata="Ollama server")
    print(f"Please click on the text below to access the Ollama server: {listener}")

# Restart Nginx to apply the configuration
def restart_nginx():
    """Restart Nginx to apply the new configuration."""
    print("Restarting Nginx...")
    os.system("sudo /etc/init.d/nginx stop")
    os.system("sudo /etc/init.d/nginx start")
    print("Nginx restarted successfully.")

# Main function to execute the setup
def main():
    """Main function to set up the Ollama server."""
    change_working_directory()
    set_ollama_env_vars()
    install_ollama()      # Install Ollama FIRST - Corrected order
    start_ollama_server()  # Then try to start the server
    wait_for_ollama_server() # Improved wait function
    create_custom_model_file()
    pull_model()
    install_nginx()
    configure_nginx()
    install_ngrok()
    set_ngrok_authtoken()
    connect_ngrok()
    restart_nginx()
    print("Setup complete! Ollama server is running and accessible via Ngrok.")

# Run the main function
if __name__ == "__main__":
    main()
