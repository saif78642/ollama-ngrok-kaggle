import os
import subprocess
import time
import getpass
from pyngrok import ngrok

# Change directory to the working directory
def change_working_directory(path='/content/'):
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
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            raise RuntimeError(f"Command failed: {command}")
        print(result.stdout)

# Start the Ollama server using subprocess
def start_ollama_server():
    """Start the Ollama server in the background using subprocess."""
    print("Starting Ollama server...")
    try:
        subprocess.Popen(
            ["/usr/local/bin/ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(5)  # Initial short sleep to let it start
        print("Ollama server started in background.")
    except Exception as e:
        print(f"Failed to start Ollama server: {e}")
        raise

# Wait for the Ollama server to be ready
def wait_for_ollama_server():
    """Wait for the Ollama server to become available."""
    print("Waiting for Ollama server to start...")
    timeout_seconds = 120  # Timeout after 120 seconds
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout_seconds:
            raise TimeoutError("Timeout waiting for Ollama server to start.")
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:11434/api/version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0 and "version" in result.stdout:
                print("Ollama server is ready!")
                break
            else:
                print("Ollama server not yet ready.")
        except Exception as e:
            print(f"Error checking Ollama server: {e}")
        time.sleep(2)

# Install Ollama
def install_ollama():
    """Install Ollama using the official installation script."""
    print("Installing Ollama...")
    commands = [
        "curl -fsSL https://ollama.com/install.sh | sh",
    ]
    run_commands(commands)
    print("Ollama installation complete.")

# Pull the specified model using Ollama
def pull_model(model_name="qwen2.5-coder"):
    """Pull the specified model using Ollama."""
    print(f"Pulling model: {model_name}...")
    commands = [
        f"ollama pull {model_name}"
    ]
    run_commands(commands)
    print(f"Model {model_name} pulled successfully.")

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
    listener = ngrok.connect(addr="localhost:11434", metadata="Ollama server")
    print(f"Please click on the text below to access the Ollama server: {listener}")

# Main function to execute the setup
def main():
    """Main function to set up the Ollama server."""
    change_working_directory()
    set_ollama_env_vars()
    install_ollama()      # Install Ollama FIRST
    start_ollama_server()  # Then try to start the server
    wait_for_ollama_server()  # Wait for the server to be ready
    pull_model()  # Pull the desired model
    set_ngrok_authtoken()  # Set Ngrok authtoken
    connect_ngrok()  # Expose the server via Ngrok
    print("Setup complete! Ollama server is running and accessible via Ngrok.")

# Run the main function
if __name__ == "__main__":
    main()
