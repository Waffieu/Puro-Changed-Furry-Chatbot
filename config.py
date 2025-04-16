import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Memory settings
SHORT_MEMORY_SIZE = int(os.getenv("SHORT_MEMORY_SIZE", "25"))
LONG_MEMORY_SIZE = int(os.getenv("LONG_MEMORY_SIZE", "100"))
MEMORY_DIR = os.getenv("MEMORY_DIR", "user_memories")

# Web search settings
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "100"))

# Proxy settings
PROXY_ENABLED = os.getenv("PROXY_ENABLED", "false").lower() == "true"

# Get proxies from environment variable or file
PROXY_LIST = []
proxy_list_env = os.getenv("PROXY_LIST", "")
proxy_file = os.getenv("PROXY_FILE", "")

if proxy_list_env:
    # Parse comma-separated list of proxies
    PROXY_LIST = [p.strip() for p in proxy_list_env.split(",") if p.strip()]
elif proxy_file and os.path.exists(proxy_file):
    # Load proxies from file
    try:
        with open(proxy_file, "r") as f:
            if proxy_file.endswith(".json"):
                # JSON file with proxies
                proxy_data = json.load(f)
                if isinstance(proxy_data, list):
                    PROXY_LIST = proxy_data
                elif isinstance(proxy_data, dict) and "proxies" in proxy_data:
                    PROXY_LIST = proxy_data["proxies"]
            else:
                # Text file with one proxy per line
                PROXY_LIST = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading proxies from file: {e}")

# Maximum number of retries for DuckDuckGo searches
MAX_SEARCH_RETRIES = int(os.getenv("MAX_SEARCH_RETRIES", "5"))

# Time awareness settings
DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "Europe/Istanbul")
TIME_AWARENESS_ENABLED = os.getenv("TIME_AWARENESS_ENABLED", "true").lower() == "true"

# Gemini model settings
GEMINI_MODEL = "gemini-2.0-flash-lite"
GEMINI_TEMPERATURE = 0.7
GEMINI_TOP_P = 0.95
GEMINI_TOP_K = 40
GEMINI_MAX_OUTPUT_TOKENS = 1024

# Safety settings - all set to BLOCK_NONE as requested
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]
