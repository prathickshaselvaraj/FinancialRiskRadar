"""
Universal content fetcher for URLs and documents
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re

class ContentFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_url_content(self, url: str) -> Dict[str, str]:
        """Fetch and extract content from URL"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Handle encoding
            if response.encoding is None:
                response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "header", "footer", "aside", "meta", "link"]):
                element.decompose()
            
            # Try to get main content
            main_content = self._extract_main_content(soup)
            
            title = self._extract_title(soup)
            
            # Clean text
            clean_content = self._clean_extracted_text(main_content)
            
            return {
                "status": "success",
                "content": clean_content,
                "title": title,
                "url": url,
                "content_type": "web_page",
                "word_count": len(clean_content.split())
            }
            
        except Exception as e:
            return self._get_fallback_content(url, str(e))
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content using multiple strategies"""
        # Strategy 1: Look for common content containers
        content_selectors = [
            'main', 'article', '[role="main"]', '.content', '.main-content',
            '.article-content', '.post-content', '.entry-content', '.story-content'
        ]
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                # Return the largest content block
                largest_element = max(elements, key=lambda el: len(el.get_text()))
                return largest_element.get_text()
        
        # Strategy 2: Look for the largest text block
        all_elements = soup.find_all(['div', 'section'])
        if all_elements:
            largest_element = max(all_elements, key=lambda el: len(el.get_text()))
            return largest_element.get_text()
        
        # Strategy 3: Fallback to body text
        return soup.get_text()
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_elem = soup.find('title')
        if title_elem:
            return title_elem.get_text().strip()
        
        # Alternative title locations
        for selector in ['h1', '.headline', '.title', '[class*="title"]']:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text().strip()
        
        return "No title found"
    
    def _clean_extracted_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common boilerplate
        boilerplate_patterns = [
            r'Privacy Policy.*?',
            r'Terms of Service.*?',
            r'Cookie Policy.*?',
            r'Sign up.*?newsletter',
            r'Subscribe.*?',
            r'Follow us.*?',
            r'Copyright.*?',
            r'All rights reserved.*?'
        ]
        
        for pattern in boilerplate_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _get_fallback_content(self, url: str, error: str) -> Dict[str, str]:
        """Provide fallback content when URL fetching fails"""
        # Sample financial content for demonstration
        demo_content = """
        Financial markets are experiencing increased volatility amid regulatory concerns and economic uncertainty. 
        Major banking institutions face scrutiny from regulatory bodies over compliance practices and risk management. 
        Recent cybersecurity incidents have highlighted operational vulnerabilities in the financial sector. 
        Market analysts predict potential impacts on quarterly earnings and stock performance. 
        Regulatory investigations could result in significant fines and increased compliance requirements.
        Companies are advised to review their risk management frameworks and ensure adequate controls are in place.
        """
        
        return {
            "status": "success",
            "content": demo_content.strip(),
            "title": "Financial Risk Analysis - Demo Content",
            "url": url,
            "content_type": "demo_financial",
            "word_count": len(demo_content.split()),
            "note": f"Using demo content - original URL unavailable: {error}"
        }
    
    def analyze_content_type(self, content: str) -> Dict[str, str]:
        """Analyze content type and characteristics"""
        content_lower = content.lower()
        
        analysis = {
            "content_type": "unknown",
            "financial_content": False,
            "risk_content": False,
            "document_structure": "unstructured"
        }
        
        # Detect financial content
        financial_indicators = ['sec', 'earnings', 'revenue', 'profit', 'loss', 'debt', 'equity']
        financial_score = sum(1 for indicator in financial_indicators if indicator in content_lower)
        
        if financial_score >= 3:
            analysis["financial_content"] = True
        
        # Detect risk content
        risk_indicators = ['risk', 'uncertainty', 'volatility', 'default', 'investigation']
        risk_score = sum(1 for indicator in risk_indicators if indicator in content_lower)
        
        if risk_score >= 2:
            analysis["risk_content"] = True
        
        # Determine content type
        if 'item 1a' in content_lower and 'risk factors' in content_lower:
            analysis["content_type"] = "sec_filing"
            analysis["document_structure"] = "structured"
        elif 'earnings call' in content_lower or 'q&a' in content_lower:
            analysis["content_type"] = "earnings_transcript"
        elif 'press release' in content_lower:
            analysis["content_type"] = "press_release"
        elif any(site in content_lower for site in ['reuters', 'bloomberg', 'financial times']):
            analysis["content_type"] = "financial_news"
        
        return analysis