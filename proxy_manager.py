import logging
import random
from typing import List, Optional, Dict, Any
import time

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ProxyManager:
    """
    Manages a list of proxies and provides rotation functionality
    when a proxy fails to work properly.
    """
    
    def __init__(self, proxies: List[str] = None):
        """
        Initialize the proxy manager with a list of proxies.
        
        Args:
            proxies: List of proxy URLs in the format "http://host:port" or "socks5://host:port"
        """
        self.proxies = proxies or []
        self.current_proxy_index = 0
        self.failed_proxies = {}  # Track failed proxies and their failure time
        self.retry_interval = 300  # 5 minutes before retrying a failed proxy
        
        if self.proxies:
            logger.info(f"Initialized ProxyManager with {len(self.proxies)} proxies")
        else:
            logger.warning("ProxyManager initialized with no proxies")
    
    def add_proxy(self, proxy: str) -> None:
        """
        Add a new proxy to the list.
        
        Args:
            proxy: Proxy URL in the format "http://host:port" or "socks5://host:port"
        """
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            logger.info(f"Added new proxy: {self._mask_proxy(proxy)}")
    
    def add_proxies(self, proxies: List[str]) -> None:
        """
        Add multiple proxies to the list.
        
        Args:
            proxies: List of proxy URLs
        """
        for proxy in proxies:
            self.add_proxy(proxy)
    
    def get_current_proxy(self) -> Optional[str]:
        """
        Get the current proxy from the list.
        
        Returns:
            Current proxy URL or None if no proxies are available
        """
        if not self.proxies:
            return None
            
        # Check if we have any non-failed proxies
        current_time = time.time()
        available_proxies = [
            p for p in self.proxies 
            if p not in self.failed_proxies or 
            (current_time - self.failed_proxies[p]) > self.retry_interval
        ]
        
        if not available_proxies:
            # If all proxies have failed recently, reset the oldest failed proxy
            if self.failed_proxies:
                oldest_proxy = min(self.failed_proxies.items(), key=lambda x: x[1])[0]
                logger.info(f"All proxies have failed recently. Retrying oldest failed proxy: {self._mask_proxy(oldest_proxy)}")
                del self.failed_proxies[oldest_proxy]
                return oldest_proxy
            return None
            
        # Use the current index if it's valid, otherwise reset to 0
        if self.current_proxy_index >= len(available_proxies):
            self.current_proxy_index = 0
            
        return available_proxies[self.current_proxy_index]
    
    def rotate_proxy(self) -> Optional[str]:
        """
        Rotate to the next available proxy.
        
        Returns:
            Next proxy URL or None if no proxies are available
        """
        if not self.proxies:
            return None
            
        # Mark the current proxy as failed
        current_proxy = self.get_current_proxy()
        if current_proxy:
            self.mark_proxy_failed(current_proxy)
            
        # Move to the next proxy
        self.current_proxy_index = (self.current_proxy_index + 1) % max(1, len(self.proxies))
        
        # Get the next available proxy
        next_proxy = self.get_current_proxy()
        if next_proxy:
            logger.info(f"Rotated to proxy: {self._mask_proxy(next_proxy)}")
        else:
            logger.warning("No available proxies to rotate to")
            
        return next_proxy
    
    def mark_proxy_failed(self, proxy: str) -> None:
        """
        Mark a proxy as failed.
        
        Args:
            proxy: The proxy URL that failed
        """
        if proxy in self.proxies:
            self.failed_proxies[proxy] = time.time()
            logger.warning(f"Marked proxy as failed: {self._mask_proxy(proxy)}")
    
    def get_proxy_dict(self) -> Dict[str, str]:
        """
        Get the current proxy as a dictionary for requests.
        
        Returns:
            Dictionary with 'http' and 'https' keys for the current proxy
        """
        proxy = self.get_current_proxy()
        if not proxy:
            return {}
            
        return {
            'http': proxy,
            'https': proxy
        }
    
    def _mask_proxy(self, proxy: str) -> str:
        """
        Mask the proxy URL for logging purposes to hide sensitive information.
        
        Args:
            proxy: The proxy URL to mask
            
        Returns:
            Masked proxy URL
        """
        try:
            # Extract protocol and host, mask the port and auth if present
            parts = proxy.split('://')
            if len(parts) == 2:
                protocol = parts[0]
                host_parts = parts[1].split('@')
                
                if len(host_parts) == 2:
                    # Has authentication
                    auth = '***:***'
                    host = host_parts[1].split(':')[0]
                    return f"{protocol}://{auth}@{host}:***"
                else:
                    # No authentication
                    host = host_parts[0].split(':')[0]
                    return f"{protocol}://{host}:***"
            return "***://***:***"  # Fallback mask
        except Exception:
            return "***://***:***"  # Complete mask on error

# Create a global instance of the proxy manager
proxy_manager = ProxyManager()
