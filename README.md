# Ollama-Ngrok-Setup

This repository contains a script to set up and expose an Ollama server using Ngrok. The script automates the process of installing Ollama, configuring Nginx as a reverse proxy, and setting up Ngrok to provide a public URL.

## Repository Name Suggestion

`ollama-ngrok-deploy`

## Prerequisites

Before running the script, ensure you have the following:

-   **Ngrok Account**: You need an Ngrok account to obtain an access token. Sign up at [https://ngrok.com/](https://ngrok.com/).
-   **Kaggle Notebook**: This script is designed to run within a Kaggle Notebook environment.
-   **Basic understanding of Linux commands**: Some experience with terminal commands is beneficial.
-   **Internet connectivity**: The script needs internet access to install the required packages and connect to Ngrok.

## Setup Instructions

1. **Clone the Repository:**
    If you intend to use this outside of Kaggle download the raw file by navigating to `ollama-ngrok-deploy/ollama_ngrok_setup.py`.

2. **Install Required Libraries (for local/non-Kaggle environment):**
    -   If you are not using a Kaggle Notebook environment, you will need to install the required libraries manually. Add the following to a cell at the beginning of your notebook or script (if running locally):
        ```python
        !pip install pyngrok
        ```
    - This uses `pip`, the Python package installer, to install `pyngrok`, which is used for interacting with Ngrok from Python.

3. **Run the Script in a Kaggle Notebook:**
    -   Create a new Kaggle notebook.
    -   Upload the `ollama_ngrok_setup.py` file to the notebook.
    -   Copy and paste the contents of the Python file into a code cell.
    -   Run the cell.

4. **Ngrok Token Input:**
    -   When prompted, enter your Ngrok access token and press Enter.
    -   The script will then configure Ngrok.

5. **Accessing Ollama:**
    -   Once the script completes, it will print an Ngrok URL (e.g. `https://your-random-id.ngrok-free.app`) to the output.
    -   Click on this link to access the Ollama server.

## Script Details

The `ollama_ngrok_setup.py` script performs the following actions:

-   **Sets Working Directory:**
    -   `os.chdir('/kaggle/working/')`: This line changes the current working directory to `/kaggle/working/`, which is the standard directory for user files in Kaggle Notebooks.

-   **Configures Ollama Environment:**
    -   `os.environ['OLLAMA_HOST'] = "0.0.0.0"`: This sets the `OLLAMA_HOST` environment variable to `0.0.0.0`, which means the Ollama server will listen on all available network interfaces, making it accessible from outside the local machine.
    -   `os.environ['OLLAMA_ORIGINS'] = "*"`: This sets the `OLLAMA_ORIGINS` environment variable to `*`. This allows connections to the Ollama server from any origin.

-   **Runs Commands and Checks for Errors:**
    -   The `run(commands)` function iterates through a list of shell commands and executes each one.
    -   It uses `subprocess.Popen` to run commands in a separate process.
    -   `stdout=subprocess.PIPE`, `stderr=subprocess.STDOUT`, `text=True`, `bufsize=1`, and `universal_newlines=True` are used to capture and process the output of the commands line by line.
    -   It checks each line for `"undefined reference"`. If found, it raises a `RuntimeError` indicating a potential issue with the Ollama installation.
    -   The output of each command is printed to the console using `print(line, flush=True, end="")`.

-   **Starts Ollama Server:**
    -   `os.system("/usr/local/bin/ollama serve &")`: This starts the Ollama server in the background using the `&` symbol.
    -   `time.sleep(5)`: A 5-second delay is added to give the Ollama server some time to initialize before proceeding.

-   **Installs Ollama:**
    -   `curl -fsSL https://ollama.com/install.sh | sh`: This downloads the official Ollama installation script using `curl` and pipes it to `sh` for execution. This script handles the installation process for Ollama.

-   **Creates a Custom Ollama Model File:**
    -   A file named `ModelFilesabs` is created in `/kaggle/working/`.
    -   It writes a basic model configuration to this file:
        ```
        FROM llama3
        PARAMETER num_ctx=32768
        ```
        This defines a model based on `llama3` with a context window size of `32768`.

-   **Pulls the Deepseek Model:**
    -   `ollama pull deepseek-r1:14b`: This uses the `ollama pull` command to download the `deepseek-r1:14b` model from the Ollama registry.

-   **Installs Nginx:**
    -   `apt install nginx -y`: This installs Nginx, a popular web server and reverse proxy, using the `apt` package manager. The `-y` flag automatically answers "yes" to any prompts during installation.

-   **Configures Nginx:**
    -   A configuration file for Nginx (`ollamasvc.conf`) is created at `/etc/nginx/conf.d/`.
    -   The following Nginx configuration is written to the file:
        ```nginx
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
        ```
        - `listen 80;`: This configures Nginx to listen on port 80 (the default HTTP port).
        - `server_name *.ngrok-free.app`: Specifies that this configuration will apply to requests with a server name ending in ngrok-free.app.
        - `proxy_pass http://localhost:11434;`: This is the core of the reverse proxy configuration. It forwards all requests received by Nginx to `http://localhost:11434`, which is the default port where Ollama runs.
        - The other `proxy_set_header` directives are used to ensure proper handling of WebSocket connections, which are often used by applications like Ollama.

-   **Installs pyngrok and ngrok:**
    -   `!pip install pyngrok ngrok --force`: This line was added to ensure that the script installs `pyngrok` in the Kaggle environment.
        -   `pyngrok`: A Python wrapper for Ngrok that allows you to manage Ngrok tunnels from your Python code.
        - `--force`: The `--force` argument ensures these are installed even if they already exist in the system.
        -   `ngrok`: The Ngrok library itself.

-   **Prompts for Ngrok Token:**
    -   `ngrok_token = getpass.getpass('Enter your Ngrok access token and press enter: ')`: This prompts the user to enter their Ngrok access token securely. The `getpass` module is used to hide the input as the user types it.

-   **Sets Ngrok Authtoken:**
    -   `ngrok authtoken {ngrok_token}`: This configures Ngrok with the provided access token. This is essential for Ngrok to authenticate and create tunnels.

-   **Starts Ngrok Tunnel:**
    -   `listener = ngrok.connect(addr="localhost:80", metadata="Ollama server")`: This uses `pyngrok` to create a new Ngrok tunnel.
        -   `addr="localhost:80"`: Specifies that the tunnel should forward traffic to port 80 on the local machine (where Nginx is listening).
        -   `metadata="Ollama server"`: Adds metadata to the tunnel for easier identification.
    -   `print(f"Please click on the text below to access the Ollama server: {listener}")`: This prints the Ngrok URL provided by the `listener` object.

-   **Restarts Nginx:**
    -   `sudo /etc/init.d/nginx stop`: Stops the Nginx service.
    -   `sudo /etc/init.d/nginx start`: Starts the Nginx service.
        - These are to apply the configuration changes.

## Important Notes

-   **Security**: Exposing your server via Ngrok makes it publicly accessible. Take necessary precautions to protect your data and resources.
-   **Ngrok Token**: Keep your Ngrok access token secure and do not share it publicly.
-   **Kaggle Notebook Limitations**: The Kaggle Notebook environment has certain limitations. Be mindful of resource consumption and time limits.
-   **Model Size**: Downloading large models can take time. Please be patient during the model download process.
-   **Troubleshooting**: If you encounter issues, check error messages in the logs and consult the documentation for Ollama, Nginx, and Ngrok.

## Disclaimer

Use this script at your own risk. The author is not responsible for any damage or loss of data. Always take necessary security measures before running the script in sensitive environments.

## Contribution

Feel free to submit issues or pull requests to improve this script. Your contributions are welcome!
