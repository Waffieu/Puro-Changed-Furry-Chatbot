# Puro Telegram Bot

A Telegram chatbot based on Puro from the game "Changed", powered by Google's Gemini 2.0-flash-lite AI model.

## Features

- **Puro Personality**: The bot embodies Puro, the friendly dark latex wolf from "Changed"
- **Typing Indicator**: Shows typing animation while generating responses
- **Web Search Capabilities**:
  - **Automatic Web Search**: Automatically searches the web for every query to provide accurate information
  - **Deep Search Command**: Use `/deepsearch` to search up to 1000 websites with diverse queries for comprehensive answers
  - **Proxy Rotation**: Automatically rotates through proxies when DuckDuckGo search fails, ensuring reliable search functionality
- **Persistent Memory System**:
  - Short-term memory (25 messages) for immediate context
  - Long-term memory (100 messages) for each user
  - Memories persist between bot restarts
  - Each user has their own personalized memory file
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

   # Proxy settings for DuckDuckGo searches
   # Set to true to enable proxy rotation
   PROXY_ENABLED=false

   # Comma-separated list of proxies (http://host:port or socks5://host:port)
   # Example: PROXY_LIST=http://proxy1.example.com:8080,http://proxy2.example.com:8080
   PROXY_LIST=

   # Alternatively, specify a file path containing proxies (one per line or JSON format)
   # Example: PROXY_FILE=proxies.txt or PROXY_FILE=proxies.json
   PROXY_FILE=

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

## Proxy Configuration

If you encounter DuckDuckGo search errors, you can enable proxy rotation to automatically switch between multiple proxies:

1. Set `PROXY_ENABLED=true` in your `.env` file
2. Configure proxies using one of these methods:
   - Add a comma-separated list in `.env`: `PROXY_LIST=http://proxy1.com:8080,http://proxy2.com:8080`
   - Create a text file with one proxy per line and set `PROXY_FILE=proxies.txt`
   - Create a JSON file with a "proxies" array and set `PROXY_FILE=proxies.json`

Example proxy formats:
- HTTP proxies: `http://host:port` or `http://username:password@host:port`
- SOCKS5 proxies: `socks5://host:port` or `socks5://username:password@host:port`

The bot will automatically rotate to the next proxy when a search fails, and will retry failed proxies after 5 minutes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the character Puro from the game "Changed" by DragonSnow
- Powered by Google's Gemini AI
- Built with python-telegram-bot
