---
# 📌 RAG-Powered Document Chatbot

Welcome to the **RAG-Powered Document Chatbot** repository! This guide will help you set up the development environment using **Docker** in **VS Code**, configure the **OpenAI API key**, manage Git branches, and run the chatbot to interact with uploaded documents.

*Note: The structure of this README follows the format used in [INFO-5940](https://github.com/AyhamB/INFO-5940).

---
## 🛠️ Prerequisites

Before starting, ensure you have the following installed on your system:
- [Docker](https://www.docker.com/get-started) (Ensure Docker Desktop is running)
- [VS Code](https://code.visualstudio.com/)
- [VS Code Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Git](https://git-scm.com/)
- OpenAI API Key
---
## 🚀 Setup Guide

### 1️⃣ Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/Cynthia-SyC/rag-chatbot.git
cd rag-chatbot
```
---

### 2️⃣ Open in VS Code with Docker

1. Open **VS Code**, navigate to the `rag-chatbot` folder.

2. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on Mac) and search for:

```
Remote-Containers: Reopen in Container
```

3. Select this option. VS Code will build and open the project inside the container.

📌 **Note:** If you don’t see this option, ensure that the **Remote - Containers** extension is installed.

---

### 3️⃣ Configure OpenAI API Key

#### ➤ Set the API Key in `.env` (Recommended)

1. Inside the project folder, create a `.env` file:

```bash

touch .env

```

2. Add your API key and base URL:

```plaintext

OPENAI_API_KEY=your-api-key-here

OPENAI_BASE_URL=https://api.ai.it.cornell.edu/

TZ=America/New_York

```

3. Modify `docker-compose.yml` to include this `.env` file:

```yaml

version: '3.8'

services:

devcontainer:

container_name: info-5940-devcontainer

build:

dockerfile: Dockerfile

target: devcontainer

environment:

- OPENAI_API_KEY=${OPENAI_API_KEY}

- OPENAI_BASE_URL=${OPENAI_BASE_URL}

- TZ=${TZ}

volumes:

- '$HOME/.aws:/root/.aws'

- '.:/workspace'

env_file:

- .env

```

4. Restart the container:

```bash

docker-compose up --build

```

Now, your API key will be automatically loaded inside the container.

---
  
## 🏃 Running the Chatbot

Once inside the **VS Code Dev Container**, launch the Streamlit application:

```bash

streamlit run chat_with_pdf.py

```

---

### Access the Chatbot

When the application starts, it will output a URL like this:

```

You can now view your Streamlit app in your browser.

Local URL: http://localhost:<port-number>

```

Copy and paste this link into your browser to start chatting with your documents!

---

## 🙋 How to Use

1. Upload Documents

- Click on the file uploader and select `.txt` or `.pdf` files.

- You can upload multiple documents at once.

2. Upload Documents

- Type a question in the chat input.

- The chatbot will search the documents and provide an answer.

---

## 🛠️ Troubleshooting

### **Container Fails to Start?**

- Ensure **Docker Desktop is running**.

- Run `docker-compose up --build` again.

- If errors persist, delete existing containers with:

```bash

docker-compose down

```

Then restart:

```bash

docker-compose up --build

```

### **Cannot Access Jupyter Notebook from outside VS Code?**

- Ensure you’re using the correct port.

- Run `docker ps` to check if the container is running.

### **OpenAI API Key Not Recognized?**

- Check if `.env` is correctly created.

- Ensure `docker-compose.yml` includes `env_file: - .env`.

- Restart the container after making changes (`docker-compose up --build`).

---

## 🎯 Next Steps

- Upload .txt and .pdf documents using the UI.

- Ask questions about the uploaded documents in the chat interface.

- Experiment with different documents to test the retrieval-augmented generation (RAG) system.

Enjoy exploring your documents! 🚀
