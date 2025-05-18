import time
from typing import Optional, Dict
import requests
import trafilatura
from urllib.parse import urlparse

class ContentExtractor:
    """
    A utility class for extracting main content from web pages.
    
    This class handles the extraction of clean, readable content from URLs,
    removing navigation, headers, footers, and other non-essential elements.
    """
    
    def __init__(self, user_agent: str = None, max_retries: int = 2, request_timeout: int = 15):
        """
        Initialize the ContentExtractor.
        
        Args:
            user_agent: The User-Agent string to use for requests
            max_retries: Maximum number of retry attempts for failed requests
            request_timeout: Timeout in seconds for HTTP requests
        """
        self.user_agent = user_agent or (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        self.max_retries = max_retries
        self.request_timeout = request_timeout
        
    def is_valid_url(self, url: str) -> bool:
        """
        Check if a string is a valid URL.
        
        Args:
            url: The URL to validate
            
        Returns:
            bool: True if the URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except (ValueError, AttributeError):
            return False
            
    def extract_from_url(self, url: str) -> Optional[str]:
        """
        Extract main content from a URL with retries and error handling.
        
        Args:
            url: The URL to extract content from
            
        Returns:
            str: The extracted content, or None if extraction failed
        """
        if not self.is_valid_url(url):
            return None
            
        headers = {'User-Agent': self.user_agent}
        
        for attempt in range(self.max_retries + 1):
            try:
                # Fetch the page
                response = requests.get(
                    url, 
                    headers=headers, 
                    timeout=self.request_timeout,
                    allow_redirects=True
                )
                response.raise_for_status()
                
                # Extract main content using trafilatura
                content = trafilatura.extract(
                    response.text,
                    include_comments=False,
                    include_tables=False,
                    include_links=False,
                    include_images=False,
                    no_fallback=True,
                    include_formatting=False
                )
                
                return content.strip() if content else None
                    
            except Exception as e:
                if attempt == self.max_retries:
                    print(f"Failed to extract content from {url}: {str(e)}")
                    return None
                time.sleep(1)  # Wait before retry
        
        return None
    
    def batch_extract(self, urls: list) -> Dict[str, Optional[str]]:
        """
        Extract content from multiple URLs.
        
        Args:
            urls: List of URLs to extract content from
            
        Returns:
            Dict mapping URLs to their extracted content (or None if extraction failed)
        """
        return {url: self.extract_from_url(url) for url in urls}
