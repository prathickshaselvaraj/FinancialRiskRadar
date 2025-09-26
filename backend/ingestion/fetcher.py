import requests
from bs4 import BeautifulSoup
import time
from typing import Optional, Dict
import re
from urllib.parse import urlparse
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ContentFetcher:
    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
        
        # Realistic browser headers to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def fetch_url(self, url: str) -> Optional[Dict]:
        """Fetch and extract text content from URL with improved handling"""
        try:
            logger.info(f"Fetching URL: {url}")
            
            # Validate URL first
            if not self._is_valid_url(url):
                logger.error(f"Invalid URL: {url}")
                return None
            
            response = self.session.get(
                url, 
                timeout=self.config['scraping']['timeout'],
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Check if content is HTML
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                logger.warning(f"Non-HTML content type: {content_type}")
                return self._handle_non_html_content(url, content_type)
            
            return self._extract_content_from_html(url, response.content)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {str(e)}")
            return None
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except Exception:
            return False
    
    def _extract_content_from_html(self, url: str, html_content: bytes) -> Optional[Dict]:
        """Extract content from HTML response"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 
                               'aside', 'form', 'button', 'meta', 'link']):
                element.decompose()
            
            # Try to get title
            title = self._extract_title(soup, url)
            
            # Try multiple content extraction strategies
            content = self._extract_article_content(soup)
            if not content or len(content.strip()) < 100:
                content = self._extract_fallback_content(soup)
            
            if not content or len(content.strip()) < 50:
                logger.warning(f"Insufficient content extracted from {url}")
                return None
            
            # Clean the content
            cleaned_content = self._clean_text(content)
            
            return {
                'url': url,
                'title': title,
                'content': cleaned_content,
                'content_length': len(cleaned_content),
                'timestamp': time.time(),
                'status': 'success',
                'domain': urlparse(url).netloc
            }
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return None
    
    def _extract_article_content(self, soup) -> str:
        """Extract main article content using common patterns"""
        # Common selectors for article content
        article_selectors = [
            'article',
            '.article-content',
            '.story-content',
            '.post-content',
            '.entry-content',
            '[role="main"]',
            'main',
            '.content',
            '.main-content',
            '#content',
            '#main-content',
            '.article-body',
            '.story-body',
            '.post-body'
        ]
        
        for selector in article_selectors:
            elements = soup.select(selector)
            if elements:
                content = ' '.join([elem.get_text().strip() for elem in elements])
                if len(content) > 200:
                    logger.info(f"Found content using selector: {selector}")
                    return content
        
        # Try Reuters-specific selectors
        reuters_selectors = [
            '[data-testid="Paragraph"]',
            '.article-body__content__17Yit',
            '.story-content',
            '.ArticleBody-wrapper'
        ]
        
        for selector in reuters_selectors:
            elements = soup.select(selector)
            if elements:
                content = ' '.join([elem.get_text().strip() for elem in elements])
                if len(content) > 200:
                    logger.info(f"Found Reuters content using selector: {selector}")
                    return content
        
        return ""
    
    def _extract_fallback_content(self, soup) -> str:
        """Fallback content extraction"""
        # Get all paragraphs
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50])
        
        if len(content) > 200:
            return content
        
        # Last resort: get all text and filter
        all_text = soup.get_text()
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]
        
        # Filter meaningful content
        content_lines = []
        for line in lines:
            if (len(line) > 100 and 
                not any(x in line.lower() for x in ['cookie', 'privacy', 'terms', '©', 'copyright']) and
                len(line.split()) > 10):
                content_lines.append(line)
        
        return ' '.join(content_lines)
    
    def _extract_title(self, soup, url: str) -> str:
        """Extract page title"""
        # Try multiple title selectors
        title_selectors = [
            'title',
            'h1',
            '.article-title',
            '.story-title',
            '.headline',
            '[data-testid="Heading"]',
            'h1[class*="title"]',
            'h1[class*="headline"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                return element.get_text().strip()
        
        return urlparse(url).netloc  # Fallback to domain name
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        # Trim and return
        return text.strip()[:self.config['scraping']['max_content_length']]
    
    def _handle_non_html_content(self, url: str, content_type: str) -> Optional[Dict]:
        """Handle non-HTML content types"""
        logger.info(f"Non-HTML content: {content_type}")
        
        if 'pdf' in content_type:
            return {
                'url': url,
                'title': 'PDF Document',
                'content': f'PDF content from {url} - PDF processing not implemented',
                'content_type': 'pdf',
                'status': 'success',
                'timestamp': time.time()
            }
        else:
            return {
                'url': url,
                'title': f'Unsupported content: {content_type}',
                'content': f'Content type {content_type} not supported',
                'content_type': content_type,
                'status': 'unsupported',
                'timestamp': time.time()
            }