# Puro Telegram Bot

A Telegram chatbot based on Puro from the game "Changed", powered by Google's Gemini 2.0-flash-lite AI model.

## Features

- **Puro Personality**: The bot embodies Puro, the friendly dark latex wolf from "Changed"
- **Typing Indicator**: Shows typing animation while generating responses
- **Web Search Capabilities**:
  - **Automatic Web Search**: Automatically searches the web for every query to provide accurate information
  - **Deep Search Command**: Use `/deepsearch` to search up to 1000 websites with diverse queries for comprehensive answers

- **Persistent Memory System**:
  - Short-term memory (25 messages) for immediate context
  - Long-term memory (100 messages) for each user
  - Memories persist between bot restarts
  - Each user has their own personalized memory file
- **Time Awareness**:
  - Understands the current time in Turkey
  - Recognizes time of day (morning, afternoon, evening, night)
  - Tracks how long it's been since the user's last message
  - Naturally references time information in conversations
- **Language Adaptation**:
  - Automatically detects and responds in the user's language
  - Translates action indicators (like "*tilts head curiously*") to match the detected language
  - Ensures physical expressions are always in the same language as the conversation
- **Natural Responses**: Provides conversational, A1-level language responses

## Setup

### Prerequisites

- Python 3.9+
- A Telegram Bot Token (from [BotFather](https://t.me/botfather))
- A Google Gemini API Key (from [Google AI Studio](https://aistudio.google.com/))

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/puro-telegram-bot.git
   cd puro-telegram-bot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on the `.env.example` template:
   ```
   cp .env.example .env
   ```

4. Edit the `.env` file with your API keys and configuration:
   ```
   # Telegram Bot Token (get from BotFather)
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

   # Google Gemini API Key
   GEMINI_API_KEY=your_gemini_api_key_here

   # Memory settings
   SHORT_MEMORY_SIZE=25
   LONG_MEMORY_SIZE=100
   MEMORY_DIR=user_memories

   # Web search settings
   MAX_SEARCH_RESULTS=5

   # Maximum number of retries for DuckDuckGo searches
   MAX_SEARCH_RETRIES=5
   ```

### Running the Bot

Run the bot with:
```
python main.py
```

## Usage

Once the bot is running, you can interact with it on Telegram by simply sending messages or using commands.

### Regular Chat

Simply send messages to the bot and it will:

- Automatically respond in your language
- Search the web for relevant information for every query
- Remember your entire conversation history
- Show a typing indicator while generating responses

### Commands

- `/deepsearch [query]` - Performs an extensive search across up to 1000 websites using multiple search queries. This provides much more comprehensive information than regular searches. For example: `/deepsearch quantum computing advancements`
  - The bot will continuously update you on the search progress
  - Searches can take several minutes to complete depending on the complexity of the query
  - Results are much more detailed and comprehensive than regular searches
  - Searches are performed in the user's language - if you search in Turkish, the bot will prioritize Turkish language results
  - The bot generates search queries in your language to ensure relevant, localized results
  - Responses are provided in the same language as your search query

## Customization

- Adjust Puro's personality in `personality.py`
- Modify memory settings in `.env`
- Configure Gemini model parameters in `config.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the character Puro from the game "Changed" by DragonSnow
- Powered by Google's Gemini AI
- Built with python-telegram-bot
