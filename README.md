# Clash of LLMs

## Overview

Clash of LLMs is a simulation-based project that allows various language models (LLMs) to interact with one another in a Red/Blue team scenario. The project uses a Python backend for managing simulations and a Vue.js frontend for displaying results.

## Prerequisites

Make sure you have the following installed:

- **Python 3.x**
- **Node.js** (v14.x or later)
- **npm** (Node.js package manager)
- **Git** (Version Control)
- **Bash** shell (for WSL/Linux/macOS environments)

## Installations

### Project Setup

#### Backend - Using Virtual Environments (For Windows/WSL/Linux/macOS users)

1. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:

   - For Linux/WSL/macOS:

     ```bash
     source venv/bin/activate
     ```

   - For Windows:

     ```bash
     .\venv\Scripts\activate
     ```

3. **Install all required packages**:

   ```bash
   pip install -r requirements.txt
   ```

#### APIs

**ChatGPT (Use ChatGPT-4 and above models)**

1. Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

   More help: [OpenAI Quickstart Guide](https://platform.openai.com/docs/quickstartOPEN)

#### Frontend - Vue.js Setup

1. Install the necessary dependencies:

   ```bash
   npm install
   ```

---

## Frontend and Backend Start

To start both the frontend and backend, simply run the following script:

```bash
./init.sh
```
