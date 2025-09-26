import re
from urllib.parse import urlparse
from typing import Optional
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class URLCleaner:
    def __init__(self, config: dict):
        self.config = config
        self.allowed_domains = config.get('scraping', {}).get('allowed_domains', [])
        self.blocked_domains = config.get('scraping', {}).get('blocked_domains', [])
    
    def validate_url(self, url: str) -> bool:
        """Validate URL format and domain"""
        try:
            parsed = urlparse(url)
            
            # Basic URL validation
            if not parsed.scheme in ['http', 'https']:
                return False
            
            if not parsed.netloc:
                return False
            
            # Domain validation
            domain = parsed.netloc.lower()
            
            # Check blocked domains
            if any(blocked in domain for blocked in self.blocked_domains):
                return False
            
            # If allowed domains specified, check against them
            if self.allowed_domains and not any(allowed in domain for allowed in self.allowed_domains):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"URL validation error: {str(e)}")
            return False
    
    def clean_url(self, url: str) -> Optional[str]:
        """Clean and normalize URL"""
        try:
            parsed = urlparse(url)
            
            # Remove fragments and query parameters that might cause issues
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            
            return clean_url if self.validate_url(clean_url) else None
            
        except Exception as e:
            logger.error(f"URL cleaning error: {str(e)}")
            return None