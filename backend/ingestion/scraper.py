import requests
from bs4 import BeautifulSoup
import time
from typing import Optional, Dict, List
from urllib.parse import urlparse
import re
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class WebScraper:
    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def scrape_url(self, url: str) -> Optional[Dict]:
        """Scrape content from a URL with improved content extraction"""
        try:
            logger.info(f"Scraping URL: {url}")
            
            response = self.session.get(
                url, 
                timeout=self.config.get('scraping', {}).get('timeout', 30),
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'application/pdf' in content_type:
                return self._handle_pdf_url(url, response)
            elif 'text/html' not in content_type:
                logger.warning(f"Unsupported content type: {content_type}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements more aggressively
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 
                               'aside', 'form', 'button', 'input', 'select']):
                element.decompose()
            
            # Try multiple content extraction strategies
            content = self._extract_main_content(soup)
            
            if not content or len(content.strip()) < 100:
                logger.warning("Primary content extraction failed, trying fallback")
                content = self._extract_fallback_content(soup)
            
            if not content or len(content.strip()) < 50:
                logger.error("Content extraction failed")
                return None
            
            # Clean and normalize text
            content = self._clean_text(content)
            
            title = self._extract_title(soup, url)
            
            return {
                'url': url,
                'title': title,
                'content': content,
                'content_length': len(content),
                'status': 'success',
                'timestamp': time.time(),
                'domain': urlparse(url).netloc
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None
    
    def _extract_main_content(self, soup) -> str:
        """Extract main content using common article/content patterns"""
        # Try common article selectors
        selectors = [
            'article',
            '.article-content',
            '.post-content',
            '.story-content',
            '.entry-content',
            '[role="main"]',
            'main',
            '.content',
            '.main-content',
            '#content',
            '#main-content'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                content = ' '.join([elem.get_text() for elem in elements])
                if len(content) > 200:  # Reasonable content length
                    return content
        
        # Fallback: get all paragraphs
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        return content
    
    def _extract_fallback_content(self, soup) -> str:
        """Fallback content extraction"""
        # Get all text and filter by paragraph-like content
        all_text = soup.get_text()
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]
        
        # Filter lines that look like content (not navigation, etc.)
        content_lines = []
        for line in lines:
            if len(line) > 50 and not line.startswith(('©', 'Copyright', 'Privacy', 'Terms')):
                content_lines.append(line)
        
        return ' '.join(content_lines)
    
    def _extract_title(self, soup, url: str) -> str:
        """Extract page title"""
        title_elem = soup.find('title')
        if title_elem:
            return title_elem.get_text().strip()
        
        # Try h1 if no title tag
        h1_elem = soup.find('h1')
        if h1_elem:
            return h1_elem.get_text().strip()
        
        return urlparse(url).netloc  # Fallback to domain name
    
    def _handle_pdf_url(self, url: str, response) -> Optional[Dict]:
        """Handle PDF URLs (placeholder for PDF processing)"""
        logger.info(f"PDF detected: {url}")
        # For now, return minimal content
        return {
            'url': url,
            'title': 'PDF Document',
            'content': f'PDF content from {url} - PDF processing not implemented yet',
            'content_type': 'pdf',
            'status': 'success',
            'timestamp': time.time()
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove excessive line breaks
        text = re.sub(r'\n+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        # Trim and return
        return text.strip()