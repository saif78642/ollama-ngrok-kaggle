
# Ollama Server Setup on Kaggle with Ngrok Integration

This repository contains a Python script that automates the setup of an **Ollama server** on Kaggle, exposing it to the internet using **Ngrok** . The script installs necessary dependencies, configures Nginx as a reverse proxy, and sets up Ngrok for external access.

## Table of Contents

1.  [Prerequisites](https://chat.qwenlm.ai/c/6a2bb436-6ecd-48aa-8e4d-27e336e6b661#prerequisites)
2.  [How It Works](https://chat.qwenlm.ai/c/6a2bb436-6ecd-48aa-8e4d-27e336e6b661#how-it-works)
3.  [Setup Instructions](https://chat.qwenlm.ai/c/6a2bb436-6ecd-48aa-8e4d-27e336e6b661#setup-instructions)
4.  [Running the Script](https://chat.qwenlm.ai/c/6a2bb436-6ecd-48aa-8e4d-27e336e6b661#running-the-script)
5.  [Troubleshooting](https://chat.qwenlm.ai/c/6a2bb436-6ecd-48aa-8e4d-27e336e6b661#troubleshooting)
6.  [Contributing](https://chat.qwenlm.ai/c/6a2bb436-6ecd-48aa-8e4d-27e336e6b661#contributing)

----------

## Prerequisites

Before running this script, ensure you have the following:

1.  **Kaggle Account** : You need a Kaggle account to create and run notebooks.
2.  **Ngrok Account** : Sign up for a free Ngrok account at [https://ngrok.com/](https://ngrok.com/) to get your **authtoken** .
3.  **GPU-enabled Kaggle Notebook** : Ensure you're using a GPU-enabled notebook to handle large models efficiently.
4.  **Basic Knowledge of Kaggle Notebooks** : Familiarity with Kaggle's interface and how to run code cells in a notebook.

----------

## How It Works

The script performs the following steps:

1.  **Install Dependencies** : Installs required packages like `pciutils`, `lshw`, `pyngrok`, and `ngrok`.
2.  **Set Environment Variables** : Configures environment variables for Ollama.
3.  **Install Ollama** : Downloads and installs the Ollama server.
4.  **Start Ollama Server** : Starts the Ollama server in the background.
5.  **Pull Model** : Pulls the specified model (default: `qwen2.5-coder`) from Ollama.
6.  **Install and Configure Nginx** : Sets up Nginx as a reverse proxy to forward requests to the Ollama server.
7.  **Set Up Ngrok** : Exposes the Ollama server to the internet using Ngrok.
8.  **Restart Services** : Restarts Nginx and ensures all services are running correctly.

----------

## Setup Instructions

### Step 1: Create a New Kaggle Notebook

1.  Go to [Kaggle](https://www.kaggle.com/) and log in.
2.  Click on **"Create"** > **"Notebook"** to create a new notebook.

### Step 2: Enable Internet Access

1.  In the notebook settings (gear icon), enable **Internet access** .
2.  Ensure the notebook is running on a **GPU-enabled environment** .

### Step 3: Install Dependencies

Run the following commands in the first cell of your notebook to install the required dependencies:

bash
1. !apt update

2. !apt install -y pciutils lshw

3. !pip install pyngrok ngrok

### Step 4: Upload the Script

1.  Copy the Python script provided in this repository into a new code cell in your Kaggle notebook.
2.  Alternatively, you can upload the script file directly to the notebook by clicking the **"Add Data"** button and selecting the script.

### Step 5: Run the Script

1.  Execute the script by running the cell containing the code.
2.  When prompted, enter your **Ngrok authtoken** (you can find this in your Ngrok dashboard).

----------

## Running the Script

Once the script is running, follow these steps:

1.  **Wait for Installation** : The script will install dependencies, set up Ollama, and configure Nginx. This may take several minutes.
2.  **Ngrok Tunnel** : After Ngrok is set up, the script will display a URL. Click on the link to access your Ollama server externally.
3.  **Access the Server** : Use the Ngrok URL to interact with the Ollama server from any device connected to the internet.

----------

## Troubleshooting

### Common Issues and Solutions

1.  **Timeout Waiting for Ollama Server** :
    
    -   Ensure you're using a GPU-enabled notebook.
    -   Increase the timeout value in the `wait_for_ollama_server` function if necessary.
2.  **Ngrok Authentication Failed** :
    
    -   Double-check your Ngrok authtoken.
    -   Ensure you've entered the token correctly when prompted.
3.  **Nginx Configuration Errors** :
    
    -   Verify that the Nginx configuration file (`/etc/nginx/conf.d/ollamasvc.conf`) is correctly written.
    -   Restart Nginx manually using:
        
        bash
        1. !sudo /etc/init.d/nginx restart
        
4.  **Model Pulling Fails** :
    
    -   Ensure the model name (`qwen2.5-coder`) is correct.
    -   Check your internet connection and retry.

----------

## Contributing

If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Contributions are welcome!
