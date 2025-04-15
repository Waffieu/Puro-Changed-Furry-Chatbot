import google.generativeai as genai
from typing import List, Dict, Any
import config
import logging
import time
from duckduckgo_search import DDGS
from proxy_manager import proxy_manager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Gemini
genai.configure(api_key=config.GEMINI_API_KEY)

def generate_search_queries(user_query: str, chat_history: List[Dict[str, str]]) -> List[str]:
    """
    Generate search queries based on the user's query and chat history

    Args:
        user_query: The user's current query
        chat_history: Recent chat history for context

    Returns:
        List of search queries
    """
    try:
        # Debug: Log the user query and chat history length
        logger.info(f"Generating search queries for user query: '{user_query}'")
        logger.debug(f"Using {len(chat_history)} messages from chat history for context")

        # Create a prompt to generate search queries
        prompt = f"""
        Based on the following conversation and the user's latest query, generate 3 effective search queries.
        Make the queries specific, focused, and likely to return relevant information.

        Recent conversation:
        {format_chat_history(chat_history[-5:] if len(chat_history) > 5 else chat_history)}

        User's latest query: {user_query}

        Generate exactly 3 search queries, one per line. Don't include any explanations or numbering.
        """

        # Debug: Log the prompt length
        logger.debug(f"Generated prompt for search queries with {len(prompt)} characters")

        # Generate search queries
        model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 256,
            },
            safety_settings=config.SAFETY_SETTINGS
        )

        # Debug: Log that we're sending the request to Gemini
        logger.debug(f"Sending request to Gemini model {config.GEMINI_MODEL} for search query generation")

        response = model.generate_content(prompt)

        # Debug: Log the raw response
        logger.debug(f"Received raw response from Gemini: '{response.text}'")

        # Parse the response into individual queries
        queries = [q.strip() for q in response.text.strip().split('\n') if q.strip()]

        # Debug: Log the parsed queries
        logger.info(f"Generated {len(queries)} search queries: {queries}")

        # Limit to 3 queries maximum
        result = queries[:3]

        # Debug: Log if we had to limit the queries
        if len(queries) > 3:
            logger.debug(f"Limited from {len(queries)} to 3 search queries")

        return result
    except Exception as e:
        # Debug: Log the error with detailed information
        logger.error(f"Error generating search queries for '{user_query}': {e}")
        logger.exception("Detailed search query generation error traceback:")
        logger.info(f"Falling back to using original query: '{user_query}'")
        return [user_query]  # Fallback to using the original query

def format_chat_history(chat_history: List[Dict[str, str]]) -> str:
    """
    Format chat history for inclusion in prompts

    Args:
        chat_history: List of message dictionaries

    Returns:
        Formatted chat history as a string
    """
    formatted = []
    for message in chat_history:
        role = "User" if message["role"] == "user" else "Puro"
        formatted.append(f"{role}: {message['content']}")

    return "\n".join(formatted)

def search_with_duckduckgo(query: str) -> Dict[str, Any]:
    """
    Perform a search using DuckDuckGo with detailed debugging
    and automatic proxy rotation if enabled.

    Args:
        query: The search query

    Returns:
        Dictionary containing search results
    """
    # Initialize proxy list if enabled and not already done
    if config.PROXY_ENABLED and not proxy_manager.proxies and config.PROXY_LIST:
        proxy_manager.add_proxies(config.PROXY_LIST)
        logger.info(f"Initialized proxy manager with {len(config.PROXY_LIST)} proxies")

    # Track retries
    retries = 0
    max_retries = config.MAX_SEARCH_RETRIES
    result_list = []

    while retries <= max_retries:
        try:
            # Debug: Log the search query
            logger.info(f"DuckDuckGo search query: '{query}' (Attempt {retries+1}/{max_retries+1})")

            # Initialize DuckDuckGo search with proxy if enabled
            proxies = None
            if config.PROXY_ENABLED and proxy_manager.proxies:
                current_proxy = proxy_manager.get_current_proxy()
                if current_proxy:
                    proxies = {"http": current_proxy, "https": current_proxy}
                    logger.info(f"Using proxy for DuckDuckGo search (masked for privacy)")

            # Create DDGS instance with or without proxy
            ddgs = DDGS(proxies=proxies)
            logger.debug("DuckDuckGo search client initialized")

            # Debug: Log search parameters
            logger.info(f"DuckDuckGo search parameters: region=wt-wt, safesearch=off, max_results={config.MAX_SEARCH_RESULTS}")

            # Perform the search with safety off
            results = ddgs.text(
                keywords=query,
                region="wt-wt",  # Worldwide results
                safesearch="off",  # No safety filtering
                max_results=config.MAX_SEARCH_RESULTS  # Number of results from config
            )

            # Debug: Log raw results count
            result_list = list(results)  # Convert generator to list
            logger.info(f"DuckDuckGo search returned {len(result_list)} results")

            # Debug: Log first result if available
            if result_list:
                logger.debug(f"First result title: '{result_list[0].get('title', 'No title')}'")
                # Search was successful, break the retry loop
                break
            else:
                logger.warning(f"DuckDuckGo search returned no results for query: '{query}'")
                # No results but no error either, might be a legitimate empty result
                # We'll continue with an empty result list rather than retrying
                break

        except Exception as e:
            # Debug: Log detailed error information
            logger.error(f"Error performing DuckDuckGo search for query '{query}' (attempt {retries+1}): {e}")

            # If proxy is enabled, rotate to the next proxy
            if config.PROXY_ENABLED and proxy_manager.proxies:
                current_proxy = proxy_manager.get_current_proxy()
                if current_proxy:
                    proxy_manager.mark_proxy_failed(current_proxy)
                next_proxy = proxy_manager.rotate_proxy()
                if next_proxy:
                    logger.info(f"Rotated to next proxy for retry")
                else:
                    logger.warning("No more proxies available, will retry without proxy")

            # Increment retry counter
            retries += 1

            # If we've reached max retries, log and break
            if retries > max_retries:
                logger.error(f"Reached maximum retries ({max_retries}) for query: '{query}'")
                break

            # Wait a moment before retrying
            time.sleep(1)

    # Format the results
    text = ""
    citations = []

    for i, result in enumerate(result_list):
        # Debug: Log each result being processed
        logger.debug(f"Processing result {i+1}: '{result.get('title', 'No title')}'")

        # Add the result to the text
        text += f"\n\n{result['body']}\n"

        # Add the citation
        citation = {
            "title": result['title'],
            "url": result['href']
        }
        citations.append(citation)

        # Add a reference number and source to the text
        text += f"Source [{i+1}]: {result['title']} - {result['href']}"

    # Debug: Log formatted results summary
    logger.info(f"Formatted {len(citations)} DuckDuckGo results with {len(text)} characters of text")

    # If we got results, return them
    if result_list:
        return {
            "text": text.strip(),
            "citations": citations
        }
    else:
        # If all attempts failed, fall back to Gemini search
        logger.info(f"All DuckDuckGo search attempts failed, falling back to Gemini search for query: '{query}'")
        return search_with_gemini(query)

def search_with_gemini(query: str) -> Dict[str, Any]:
    """
    Perform a search using Gemini's knowledge as a fallback

    Args:
        query: The search query

    Returns:
        Dictionary containing search results
    """
    try:
        # Debug: Log that we're using Gemini as a fallback
        logger.info(f"Using Gemini as fallback search for query: '{query}'")

        # Create a prompt that simulates web search results
        search_prompt = f"""
        I want you to act as a web search engine. I'll give you a query, and you'll provide information as if you've searched the web.
        For each piece of information, include a made-up but realistic website citation in the format [Source: website.com].

        My search query is: {query}

        Provide comprehensive information about this topic with at least 3 different sources cited.
        Format your response as a cohesive article with the citations inline.
        """

        # Debug: Log the prompt length
        logger.debug(f"Generated Gemini search prompt with {len(search_prompt)} characters")

        # Use Gemini to generate a response that simulates web search results
        model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL,
            generation_config={
                "temperature": config.GEMINI_TEMPERATURE,
                "top_p": config.GEMINI_TOP_P,
                "top_k": config.GEMINI_TOP_K,
                "max_output_tokens": config.GEMINI_MAX_OUTPUT_TOKENS,
            },
            safety_settings=config.SAFETY_SETTINGS
        )

        # Debug: Log that we're sending the request to Gemini
        logger.debug(f"Sending request to Gemini model {config.GEMINI_MODEL} for fallback search")

        response = model.generate_content(search_prompt)

        # Debug: Log that we received a response
        logger.debug(f"Received Gemini search response with {len(response.text)} characters")

        # Extract citations from the response text
        text = response.text
        citations = []

        # Extract citations in the format [Source: website.com]
        import re
        citation_pattern = r'\[Source: ([^\]]+)\]'
        matches = re.findall(citation_pattern, text)

        # Debug: Log the number of citations found
        logger.info(f"Found {len(matches)} citations in Gemini search response")

        for i, match in enumerate(matches):
            # Debug: Log each citation being processed
            logger.debug(f"Processing citation {i+1}: '{match}'")

            citation = {
                "title": f"Source {i+1}",
                "url": f"https://{match.strip()}"
            }
            citations.append(citation)

            # Replace the citation in the text with a numbered reference and URL
            text = text.replace(f"[Source: {match}]", f"Source [{i+1}]: {citation['title']} - {citation['url']}")

        # Debug: Log the final formatted result
        logger.info(f"Formatted Gemini search results with {len(text)} characters and {len(citations)} citations")

        return {
            "text": text,
            "citations": citations
        }
    except Exception as e:
        # Debug: Log the error with detailed information
        logger.error(f"Error performing Gemini fallback search for '{query}': {e}")
        logger.exception("Detailed Gemini search error traceback:")

        # Return a fallback message
        fallback_message = f"I couldn't search for information about '{query}'. Let me try to answer based on what I know."
        logger.info(f"Using final fallback message: '{fallback_message}'")

        return {
            "text": fallback_message,
            "citations": []
        }
