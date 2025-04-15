import logging
import google.generativeai as genai
import config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Gemini
genai.configure(api_key=config.GEMINI_API_KEY)

# Cache for translated actions to avoid repeated API calls
action_translation_cache = {}

def translate_action(action: str, language: str) -> str:
    """
    Translate an action indicator to the specified language

    Args:
        action: The action indicator text (e.g., "*tilts head curiously*")
        language: The target language

    Returns:
        Translated action indicator
    """
    # If language is English or not specified, return the original action
    if language.lower() == "english" or not language:
        return action

    # Check cache first
    cache_key = f"{action}_{language}"
    if cache_key in action_translation_cache:
        return action_translation_cache[cache_key]

    try:
        # Create a prompt to translate the action
        prompt = f"""
        Translate the following action indicator to {language}. Keep the asterisks (*) intact:

        {action}

        Respond with ONLY the translated action indicator, nothing else. Keep it at A1 (beginner) language level.
        Make sure to translate the entire action, not just individual words.
        For example, "*tilts head curiously*" in Spanish should be "*inclina la cabeza con curiosidad*", not "*tilts head curiosamente*".
        """

        # Generate translation
        model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL,
            generation_config={
                "temperature": 0.1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 50,
            }
        )

        response = model.generate_content(prompt)

        # Get the translated action
        translated_action = response.text.strip()

        # Ensure asterisks are preserved
        if not translated_action.startswith("*"):
            translated_action = f"*{translated_action}"
        if not translated_action.endswith("*"):
            translated_action = f"{translated_action}*"

        # Cache the result
        action_translation_cache[cache_key] = translated_action

        return translated_action
    except Exception as e:
        logger.error(f"Error translating action to {language}: {e}")
        return action  # Return original action if translation fails

# Common action indicators used in the bot
COMMON_ACTIONS = {
    "EARS_PERK_UP": "*ears perk up*",
    "TAIL_WAGS": "*tail wags excitedly*",
    "TILTS_HEAD": "*tilts head curiously*",
    "EARS_DROOP": "*ears droop*",
    "BOUNCES": "*bounces slightly with excitement*",
    "SITS_DOWN": "*sits down*"
}

def get_translated_action(action_key: str, language: str) -> str:
    """
    Get a translated common action by key

    Args:
        action_key: The key for the action in COMMON_ACTIONS
        language: The target language

    Returns:
        Translated action indicator
    """
    if action_key not in COMMON_ACTIONS:
        return ""

    action = COMMON_ACTIONS[action_key]
    return translate_action(action, language)
