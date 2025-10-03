"""
Financial news scraping and processing with API integrations
"""
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import time
import logging
from urllib.parse import urljoin, urlparse
import hashlib

class FinancialNewsScraper:
    def __init__(self, newsapi_key: str = None, alphavantage_key: str = None):
        self.news_sources = {
            'reuters': {
                'base_url': 'https://www.reuters.com',
                'business_section': '/business/',
                'finance_section': '/business/finance/',
                'selectors': {
                    'title': 'h1, h2, h3, [data-testid="Heading"]',
                    'content': 'article p, .article-body__content__17Yit p, [data-testid="paragraph"]',
                    'date': 'time, [datetime], .date-line__date__23Ge-',
                    'author': '.author-name, .byline__name__1M9qx'
                }
            },
            'bloomberg': {
                'base_url': 'https://www.bloomberg.com',
                'markets_section': '/markets',
                'selectors': {
                    'title': 'h1, h2, h3, .headline',
                    'content': 'article p, .body-content p, .content-well p',
                    'date': 'time, .timestamp, .published-at',
                    'author': '.author, .byline__author'
                }
            },
            'yahoo_finance': {
                'base_url': 'https://finance.yahoo.com',
                'news_section': '/news/',
                'selectors': {
                    'title': 'h1, h2, .caas-title',
                    'content': 'article p, .caas-body p, .content p',
                    'date': 'time, .date, .caas-attr-time-style',
                    'author': '.author, .caas-attr-author'
                }
            },
            'financial_times': {
                'base_url': 'https://www.ft.com',
                'selectors': {
                    'title': 'h1, .article-headline, .headline',
                    'content': 'article p, .article-body p, .content p',
                    'date': 'time, .date, .o-date',
                    'author': '.author, .byline'
                }
            }
        }
        
        # API configurations
        self.newsapi_key = newsapi_key
        self.alphavantage_key = alphavantage_key
        self.finnhub_key = None  # Add your Finnhub key
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    # 🔄 NEWS API INTEGRATION
    def fetch_news_from_api(self, query: str = "financial risk", days: int = 7) -> List[Dict]:
        """Fetch financial news from NewsAPI"""
        if not self.newsapi_key:
            self.logger.warning("NewsAPI key not configured")
            return []
        
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'from': (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
                'to': datetime.now().strftime('%Y-%m-%d'),
                'sortBy': 'relevancy',
                'language': 'en',
                'apiKey': self.newsapi_key,
                'pageSize': 50
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                processed_article = {
                    'title': article.get('title', ''),
                    'content': article.get('description', '') or article.get('content', ''),
                    'source': article.get('source', {}).get('name', 'unknown'),
                    'url': article.get('url', ''),
                    'publish_date': article.get('publishedAt', ''),
                    'author': article.get('author', ''),
                    'word_count': len((article.get('description') or '').split()),
                    'status': 'api_success',
                    'api_source': 'newsapi'
                }
                
                # Analyze sentiment
                sentiment = self.analyze_news_sentiment(processed_article['content'])
                processed_article.update(sentiment)
                
                articles.append(processed_article)
            
            return articles
            
        except Exception as e:
            self.logger.error(f"NewsAPI fetch failed: {e}")
            return []

    # 🔄 ALPHA VANTAGE API INTEGRATION
    def fetch_market_news(self) -> List[Dict]:
        """Fetch market news from Alpha Vantage"""
        if not self.alphavantage_key:
            self.logger.warning("Alpha Vantage key not configured")
            return []
        
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'NEWS_SENTIMENT',
                'apikey': self.alphavantage_key,
                'topics': 'financial_markets,economy',
                'limit': 50
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            articles = []
            for feed in data.get('feed', []):
                processed_article = {
                    'title': feed.get('title', ''),
                    'content': feed.get('summary', ''),
                    'source': feed.get('source', 'unknown'),
                    'url': feed.get('url', ''),
                    'publish_date': feed.get('time_published', ''),
                    'author': feed.get('authors', [''])[0] if feed.get('authors') else '',
                    'word_count': len(feed.get('summary', '').split()),
                    'status': 'api_success',
                    'api_source': 'alphavantage',
                    'sentiment_score': float(feed.get('overall_sentiment_score', 0)),
                    'sentiment_label': feed.get('overall_sentiment_label', 'neutral')
                }
                
                # Add risk analysis
                risk_analysis = self.analyze_news_sentiment(processed_article['content'])
                processed_article.update(risk_analysis)
                
                articles.append(processed_article)
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Alpha Vantage API fetch failed: {e}")
            return []

    # 🔄 ENHANCED SCRAPING WITH FALLBACK APIS
    def scrape_news_article(self, url: str, use_api_fallback: bool = True) -> Dict[str, str]:
        """Scrape financial news article from URL with API fallback"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Identify news source
            source = self._identify_news_source(url)
            
            # Extract content based on source
            article_data = self._extract_article_content(soup, source)
            article_data['source'] = source
            article_data['url'] = url
            article_data['scraped_at'] = datetime.now().isoformat()
            article_data['status'] = 'scraping_success'
            
            # Analyze sentiment and risk
            sentiment = self.analyze_news_sentiment(article_data['content'])
            article_data.update(sentiment)
            
            return article_data
            
        except Exception as e:
            self.logger.warning(f"Scraping failed for {url}: {e}")
            
            if use_api_fallback and self.newsapi_key:
                # Try to get similar news from API
                api_articles = self.fetch_news_from_api("financial markets", 1)
                if api_articles:
                    return api_articles[0]  # Return first relevant article
            
            return self._get_demo_financial_news(url)

    # 🔄 BATCH SCRAPING WITH RATE LIMITING
    def scrape_multiple_articles(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        """Scrape multiple articles with rate limiting"""
        articles = []
        
        for i, url in enumerate(urls):
            try:
                article = self.scrape_news_article(url)
                articles.append(article)
                
                # Rate limiting
                if i < len(urls) - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                self.logger.error(f"Failed to scrape {url}: {e}")
                articles.append(self._get_demo_financial_news(url))
        
        return articles

    # 🔄 ENHANCED CONTENT EXTRACTION
    def _extract_article_content(self, soup: BeautifulSoup, source: str) -> Dict[str, str]:
        """Enhanced article content extraction with multiple fallbacks"""
        selectors = self.news_sources.get(source, {}).get('selectors', {
            'title': 'h1, h2, title',
            'content': 'p, article p, .content p, .article p',
            'date': 'time, .date, .timestamp, .published',
            'author': '.author, .byline, .writer'
        })
        
        # Extract title with multiple fallbacks
        title = self._extract_with_selectors(soup, selectors['title'])
        if not title:
            title = soup.find('title')
            title = title.get_text().strip() if title else 'Financial News Article'
        
        # Extract content with multiple strategies
        content = self._extract_content_advanced(soup, selectors['content'])
        
        # Extract date
        publish_date = self._extract_with_selectors(soup, selectors['date'])
        
        # Extract author
        author = self._extract_with_selectors(soup, selectors['author'])
        
        # Clean content
        content = self._clean_news_content(content)
        
        return {
            'title': title,
            'content': content,
            'publish_date': publish_date or datetime.now().strftime('%Y-%m-%d'),
            'author': author,
            'word_count': len(content.split()),
            'status': 'success'
        }

    def _extract_with_selectors(self, soup: BeautifulSoup, selector_string: str) -> str:
        """Extract text using multiple CSS selectors"""
        for selector in selector_string.split(', '):
            element = soup.select_one(selector.strip())
            if element:
                text = element.get_text().strip()
                if text:
                    return text
        return ''

    def _extract_content_advanced(self, soup: BeautifulSoup, selector_string: str) -> str:
        """Advanced content extraction with paragraph scoring"""
        content_parts = []
        
        # Try structured selectors first
        for selector in selector_string.split(', '):
            paragraphs = soup.select(selector.strip())
            for p in paragraphs:
                text = p.get_text().strip()
                if self._is_valid_paragraph(text):
                    content_parts.append(text)
        
        # Fallback: extract all paragraphs and score them
        if not content_parts:
            all_paragraphs = soup.find_all('p')
            for p in all_paragraphs:
                text = p.get_text().strip()
                if self._is_valid_paragraph(text):
                    content_parts.append(text)
        
        return ' '.join(content_parts[:20])  # Limit to first 20 paragraphs

    def _is_valid_paragraph(self, text: str, min_length: int = 20) -> bool:
        """Check if paragraph is valid content (not navigation, ads, etc.)"""
        if len(text) < min_length:
            return False
        
        invalid_patterns = [
            r'^subscribe',
            r'^sign up',
            r'^read more',
            r'^follow us',
            r'^copyright',
            r'^privacy',
            r'^terms',
            r'^cookie',
            r'^advertisement',
            r'^sponsored'
        ]
        
        text_lower = text.lower()
        return not any(re.match(pattern, text_lower) for pattern in invalid_patterns)

    # 🔄 ENHANCED SENTIMENT ANALYSIS
    def analyze_news_sentiment(self, content: str) -> Dict[str, float]:
        """Enhanced sentiment analysis for financial news"""
        positive_terms = [
            'growth', 'profit', 'gain', 'increase', 'positive', 'strong', 'recovery',
            'outperform', 'bullish', 'optimistic', 'surge', 'rally', 'boom', 'success',
            'expansion', 'record', 'beat', 'exceed', 'upside', 'opportunity'
        ]
        
        negative_terms = [
            'decline', 'loss', 'drop', 'decrease', 'negative', 'weak', 'crisis',
            'underperform', 'bearish', 'pessimistic', 'plunge', 'collapse', 'bankruptcy',
            'recession', 'default', 'failure', 'downturn', 'risk', 'uncertainty'
        ]
        
        risk_terms = [
            'risk', 'uncertainty', 'volatility', 'default', 'investigation', 'lawsuit',
            'breach', 'outage', 'failure', 'fines', 'penalties', 'scrutiny', 'probe',
            'violation', 'non-compliance', 'sanctions', 'litigation', 'fraud'
        ]
        
        regulatory_terms = [
            'sec', 'regulation', 'regulatory', 'compliance', 'enforcement', 'oversight',
            'investigation', 'subpoena', 'subpoena', 'audit', 'examination'
        ]
        
        market_terms = [
            'market', 'trading', 'volatility', 'liquidity', 'capital', 'investment',
            'stocks', 'bonds', 'equities', 'securities', 'derivatives'
        ]
        
        words = content.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return {
                'positive_sentiment': 0,
                'negative_sentiment': 0, 
                'risk_density': 0,
                'regulatory_density': 0,
                'market_density': 0,
                'overall_sentiment': 0
            }
        
        positive_score = sum(1 for word in words if any(term in word for term in positive_terms))
        negative_score = sum(1 for word in words if any(term in word for term in negative_terms))
        risk_score = sum(1 for word in words if any(term in word for term in risk_terms))
        regulatory_score = sum(1 for word in words if any(term in word for term in regulatory_terms))
        market_score = sum(1 for word in words if any(term in word for term in market_terms))
        
        overall_sentiment = ((positive_score - negative_score) / total_words) * 100
        
        return {
            'positive_sentiment': (positive_score / total_words) * 100,
            'negative_sentiment': (negative_score / total_words) * 100,
            'risk_density': (risk_score / total_words) * 100,
            'regulatory_density': (regulatory_score / total_words) * 100,
            'market_density': (market_score / total_words) * 100,
            'overall_sentiment': overall_sentiment
        }

    # 🔄 IDENTIFY NEWS SOURCE (keep existing)
    def _identify_news_source(self, url: str) -> str:
        """Identify the news source from URL"""
        if 'reuters.com' in url:
            return 'reuters'
        elif 'bloomberg.com' in url:
            return 'bloomberg'
        elif 'yahoo.com' in url or 'finance.yahoo.com' in url:
            return 'yahoo_finance'
        elif 'ft.com' in url:
            return 'financial_times'
        elif 'wsj.com' in url:
            return 'wall_street_journal'
        elif 'cnbc.com' in url:
            return 'cnbc'
        elif 'marketwatch.com' in url:
            return 'marketwatch'
        else:
            return 'generic'

    # 🔄 CLEAN CONTENT (keep existing)
    def _clean_news_content(self, content: str) -> str:
        """Clean and normalize news content"""
        ads_patterns = [
            r'Subscribe.*?now',
            r'Sign up.*?newsletter',
            r'Read more.*?',
            r'Reporting by.*?',
            r'Our Standards.*?',
            r'Copyright.*?\d{4}',
            r'All rights reserved.*?',
            r'ADVERTISEMENT',
            r'Sponsored Content.*?'
        ]
        
        for pattern in ads_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        content = re.sub(r'\s+', ' ', content)
        return content.strip()

    # 🔄 DEMO CONTENT (keep existing)
    def _get_demo_financial_news(self, url: str) -> Dict[str, str]:
        """Return demo financial news content when scraping fails"""
        demo_articles = [
            {
                'title': 'Major Banks Face Regulatory Scrutiny Over Compliance Practices',
                'content': 'Several major financial institutions are under investigation by regulatory authorities for potential compliance failures. The SEC has launched probes into accounting practices and internal controls. Analysts estimate potential fines could exceed $2 billion across the industry. Market volatility has increased amid the uncertainty, with banking stocks declining by an average of 5% this week.',
                'source': 'demo',
                'url': url,
                'publish_date': datetime.now().strftime('%Y-%m-%d'),
                'word_count': 78,
                'status': 'demo_content'
            },
            {
                'title': 'Cybersecurity Breaches Impact Financial Sector',
                'content': 'Recent cybersecurity incidents have exposed vulnerabilities in the financial services industry. Multiple banks and fintech companies reported data breaches affecting millions of customers. Regulatory bodies are considering new compliance requirements for data protection. The incidents highlight operational risks facing the sector and potential financial impacts from system outages and data loss.',
                'source': 'demo', 
                'url': url,
                'publish_date': datetime.now().strftime('%Y-%m-%d'),
                'word_count': 65,
                'status': 'demo_content'
            }
        ]
        
        url_hash = int(hashlib.md5(url.encode()).hexdigest(), 16)
        article = demo_articles[url_hash % len(demo_articles)]
        
        # Add sentiment analysis to demo content too
        sentiment = self.analyze_news_sentiment(article['content'])
        article.update(sentiment)
        
        return article

    # 🔄 NEW: RISK SCORING METHOD
    def calculate_risk_score(self, article_data: Dict) -> float:
        """Calculate comprehensive risk score for news article"""
        risk_factors = {
            'negative_sentiment': article_data.get('negative_sentiment', 0) * 0.3,
            'risk_density': article_data.get('risk_density', 0) * 0.4,
            'regulatory_density': article_data.get('regulatory_density', 0) * 0.3
        }
        
        total_score = sum(risk_factors.values())
        return min(total_score, 100)  # Cap at 100

# USAGE EXAMPLE
if __name__ == "__main__":
    # Initialize with API keys
    scraper = FinancialNewsScraper(
        newsapi_key="84f87307b829484fb89a5a6de4e431a5",
        alphavantage_key="39VQF76MH0BEEJV2"
    )
    
    # Example usage
    url = "https://www.reuters.com/business/finance/banks-regulatory-scrutiny-2024-10-02/"
    article = scraper.scrape_news_article(url)
    
    print(f"Title: {article['title']}")
    print(f"Risk Score: {scraper.calculate_risk_score(article):.1f}")
    print(f"Sentiment: {article['overall_sentiment']:.1f}")