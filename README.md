# ollama-ngrok-kaggle


This repository provides a setup to run the [Ollama](https://ollama.ai/) large language model server within a Kaggle environment and make it accessible from anywhere using [ngrok](https://ngrok.com/). It also demonstrates configuring a custom Ollama model and utilizing the Deepseek model.

## Overview

This project achieves the following:

1. **Sets up the Ollama server:** Installs Ollama and configures it to listen on all interfaces and accept requests from any origin, making it ready for remote access.
2. **Creates a custom Ollama model:** Defines a custom model file (using `llama3` as a base and an extended context window).
3. **Pulls the Deepseek model:** Downloads the `deepseek-r1:14b` model for use with Ollama.
4. **Configures Nginx as a reverse proxy:** Sets up Nginx to forward traffic from a public ngrok URL to the local Ollama server (port 11434).
5. **Exposes Ollama with ngrok:** Creates a secure tunnel using ngrok, making the Ollama server accessible via a public URL.

## Prerequisites

*   **Kaggle Account:** You'll need a Kaggle account to run this code in a Kaggle Notebook.
*   **ngrok Account and Token:**  Sign up for a free ngrok account and obtain your authentication token from your [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken).

## Usage

1. **Create a Kaggle Notebook:**  Go to Kaggle and create a new notebook. Choose the following environment specifications:
    *   **GPU:** T4 x2
    *   **Internet:** Enabled

2. **Copy the Code:** Copy the provided Python script into your Kaggle Notebook.

3. **Enter Ngrok Token:** When prompted, enter your ngrok authentication token.

4. **Run the Code:** Run all cells in the Kaggle Notebook.

5. **Access the Ollama Server:** The script will output a URL like `https://<your-subdomain>.ngrok-free.app`. Use this URL to interact with your Ollama server.

## Important Notes

*   **Security:** Be aware that by default, the Ollama server installed in this manner will be open to the public internet. It's highly recommended to implement authentication for your Ollama server if you plan to use it beyond testing. Refer to the Ollama documentation for security best practices.
*   **Kaggle Resources:** Kaggle Notebooks have resource limits (CPU, RAM, GPU, execution time). If you're working with very large models or handling a lot of requests, you might encounter limitations.
*   **ngrok Limitations:** Free ngrok accounts have certain restrictions (e.g., session duration, bandwidth). Consider a paid ngrok plan for more robust usage.
*   **Error Handling:** The provided script includes basic error handling to catch issues related to undefined references during the Ollama installation.
*   **Custom Model:** The example custom model file (`ModelFilesabs`) uses `llama3` as a base and sets `num_ctx` to 32768. You can modify this file to create different custom models based on your requirements.

## Example Interaction

Once the setup is complete, you can interact with the Ollama server using tools like `curl` or any HTTP client. Here's a simple example to test the `deepseek-r1:14b` model:

```bash
curl https://<your-subdomain>.ngrok-free.app/api/generate -d '{
  "model": "deepseek-r1:14b",
  "prompt": "Why is the sky blue?"
}'
