# 🗽 Libertarian AI Telegram Bot

This **Telegram bot** provides answers to questions from a **libertarian perspective**, promoting the principles of individual liberty, free markets, and a minimal role for the state. The bot leverages the power of the **Gemini API** from Google to generate insightful and fact-based responses in Ukrainian.

-----

## ✨ Features

  * **Libertarian Stance:** Answers questions adhering to libertarian principles and the idea of a minimal state.
  * **Gemini AI Integration:** Utilizes the Gemini 2.5 Flash API for generating responses.
  * **Conversation Context:** Trims conversation history to maintain context without exceeding token limits.
  * **Formatted Responses:** Supports HTML formatting (e.g., **bold text**, *italic text*) in replies for better readability.
  * **Flexible Answers:** Provides concise answers by default but can generate more detailed responses with lists if the user asks for a "plan," "list," or "details."
  * **API Error Handling:** Includes mechanisms for handling API errors and delays to prevent rate limit issues.
  * **Secure Configuration:** Loads sensitive data (bot token, API key) from a `.env` file.

-----

## 📋 Prerequisites

  * Python **3.8+**
  * A **Telegram Bot Token** from [@BotFather](https://t.me/BotFather).
  * A **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey).

-----

## ⚙️ Installation

### 1️⃣ Clone the repository (or create files)

```bash
git clone https://github.com/yourusername/libertarian-ai-telegram-bot.git
cd libertarian-ai-telegram-bot
```

*Replace `yourusername` with your actual GitHub username.*

### 2️⃣ Install dependencies

Create a `requirements.txt` file in the root directory of your project with the following content:

```
python-telegram-bot
requests
python-dotenv
```

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

### 3️⃣ Create a `.env` file

In the root directory of your project, create a file named `.env` and add your API keys and tokens:

```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

*Replace `YOUR_TELEGRAM_BOT_TOKEN` and `YOUR_GEMINI_API_KEY` with your actual values.*

-----

### 4️⃣ Run the bot locally

```bash
python bot.py
```

The bot will start polling Telegram for new messages. Any errors will be logged to the console.

-----

## 🚀 Usage

  * **Getting Started:** Send the `/start` command in a private chat with the bot.
  * **General Questions:** Ask the bot any question by tagging it (`@YourBotUsername`) or by replying to its messages.
  * **Detailed Responses:** To get a more elaborate answer with lists, include words like "plan," "list," or "details" in your query.

-----

## 📂 Project Files

  * `bot.py` – The main bot logic, including message handling, interaction with the Gemini API, and text formatting.
  * `requirements.txt` – Lists Python dependencies.
  * `.env` – Stores sensitive environment variables (**should not be committed to a public repository\!**).
  * `.gitignore` – Instructs Git to ignore the `.env` file, preventing it from being tracked.

-----

## 🌐 Hosting

This bot can be easily deployed on cloud platforms that support continuous "Background Workers" or "Always-on" tasks, such as:

  * **Render:** Ideal for hosting a `Background Worker` (polling bot).
  * **PythonAnywhere:** A great option for small Python projects. The free tier might have limitations requiring periodic manual restarts or an upgrade for continuous operation.
  * **Other VPS/Cloud Providers:** You can deploy it on any virtual private server (e.g., DigitalOcean, AWS EC2, Google Cloud VM) using `systemd` or `screen` for background execution.

-----

## License

This project is licensed under the MIT License – see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

-----

🚀 Enjoy using the **Libertarian AI Telegram Bot** to spread the ideas of liberty and free markets\!
