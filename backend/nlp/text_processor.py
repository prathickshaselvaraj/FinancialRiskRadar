"""
Advanced text processing and normalization with AI-powered financial understanding
"""
import re
import html
import requests
from typing import List, Dict, Any
import json

class FinancialTextProcessor:
    def __init__(self):
        self.financial_abbreviations = {
            'sec': 'Securities and Exchange Commission',
            'fed': 'Federal Reserve',
            'nyse': 'New York Stock Exchange',
            'nasdaq': 'NASDAQ Stock Market',
            'ceo': 'Chief Executive Officer',
            'cfo': 'Chief Financial Officer',
            'gaap': 'Generally Accepted Accounting Principles',
            'ifrs': 'International Financial Reporting Standards',
            'ebitda': 'Earnings Before Interest, Taxes, Depreciation, and Amortization',
            'eps': 'Earnings Per Share',
            'ipo': 'Initial Public Offering',
            'm&a': 'Mergers and Acquisitions',
            'roi': 'Return on Investment',
            'roa': 'Return on Assets',
            'roe': 'Return on Equity'
        }
        
        self.noise_patterns = [
            r'\s+',  # Multiple spaces
            r'\[.*?\]',  # Square brackets content
            r'\(.*?\)',  # Parentheses content (but keep financial amounts)
            r'<.*?>',  # HTML tags
            r'\bPage\s+\d+\b',  # Page numbers
            r'\bFigure\s+\d+\b',  # Figure references
            r'\bTable\s+\d+\b',  # Table references
            r'©.*$',  # Copyright notices
            r'Confidential.*$',  # Confidential markings
        ]
        
        # Enhanced financial patterns
        self.financial_patterns = {
            'stock_symbols': r'\b[A-Z]{1,5}\b',  # Basic stock symbol pattern
            'cik_numbers': r'\b\d{10}\b',  # SEC CIK numbers
            'accession_numbers': r'\b\d{10}-\d{2}-\d{6}\b',  # SEC accession numbers
            'isin_codes': r'\b[A-Z]{2}[A-Z0-9]{9}\d\b',  # ISIN codes
        }
    
    def clean_financial_text(self, text: str) -> str:
        """Comprehensive text cleaning for financial documents with AI enhancement"""
        if not text:
            return ""
        
        # Store original for reference
        original_length = len(text)
        
        # Decode HTML entities
        text = html.unescape(text)
        
        # Remove specific noise patterns
        for pattern in self.noise_patterns:
            text = re.sub(pattern, ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common financial text issues
        text = self._fix_financial_formatting(text)
        
        # Expand common financial abbreviations
        text = self._expand_abbreviations(text)
        
        # Enhance with financial entity recognition
        text = self._enhance_financial_entities(text)
        
        # Calculate cleaning metrics
        cleaned_length = len(text)
        compression_ratio = (original_length - cleaned_length) / original_length if original_length > 0 else 0
        
        return text.strip()
    
    def _fix_financial_formatting(self, text: str) -> str:
        """Fix common financial document formatting issues"""
        # Fix broken dollar amounts
        text = re.sub(r'\$\s+(\d)', r'$\1', text)
        
        # Fix percentage formatting
        text = re.sub(r'(\d)\s+%', r'\1%', text)
        
        # Fix date formatting
        text = re.sub(r'(\d{4})\s+-\s+(\d{4})', r'\1-\2', text)
        text = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{4})', r'\1/\2/\3', text)
        
        # Fix common financial term casing
        financial_terms = ['SEC', 'GAAP', 'IFRS', 'EBITDA', 'EPS', 'IPO', 'NASDAQ', 'NYSE', 'FASB']
        for term in financial_terms:
            text = re.sub(r'\b' + term.lower() + r'\b', term, text, flags=re.IGNORECASE)
        
        # Fix broken numbers with commas
        text = re.sub(r'(\d),(\d{3})', r'\1,\2', text)
        
        # Fix broken financial ratios
        text = re.sub(r'(\d)\s*:\s*(\d)', r'\1:\2', text)
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand common financial abbreviations with context awareness"""
        # First pass: expand standalone abbreviations
        for abbr, expansion in self.financial_abbreviations.items():
            # Only replace standalone abbreviations (not part of other words)
            text = re.sub(r'\b' + abbr + r'\b', expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def _enhance_financial_entities(self, text: str) -> str:
        """Enhance text with financial entity recognition"""
        # This would integrate with a financial NER API in production
        # For now, implement rule-based enhancements
        
        # Add context to stock symbols
        stock_symbols = re.findall(self.financial_patterns['stock_symbols'], text)
        for symbol in set(stock_symbols):
            if len(symbol) >= 2 and len(symbol) <= 5:
                company_name = self._symbol_to_company(symbol)
                if company_name:
                    # Add company name after first occurrence of symbol
                    first_occurrence = text.find(symbol)
                    if first_occurrence != -1:
                        text = text[:first_occurrence + len(symbol)] + f" ({company_name})" + text[first_occurrence + len(symbol):]
        
        return text
    
    def _symbol_to_company(self, symbol: str) -> str:
        """Convert stock symbol to company name"""
        symbol_map = {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'TSLA': 'Tesla Inc.',
            'JPM': 'JPMorgan Chase & Co.',
            'GS': 'Goldman Sachs Group Inc.',
            'BAC': 'Bank of America Corporation',
            'WFC': 'Wells Fargo & Company',
            'MS': 'Morgan Stanley'
        }
        return symbol_map.get(symbol, '')
    
    def segment_into_paragraphs(self, text: str, min_paragraph_length: int = 50) -> List[str]:
        """Segment text into meaningful paragraphs with financial context"""
        # Split by multiple newlines
        raw_paragraphs = re.split(r'\n\s*\n', text)
        
        # Filter and clean paragraphs
        paragraphs = []
        for paragraph in raw_paragraphs:
            paragraph = paragraph.strip()
            if len(paragraph) >= min_paragraph_length:
                # Remove paragraph numbers and bullet points
                paragraph = re.sub(r'^\s*[\d•\-]\s*', '', paragraph)
                
                # Classify paragraph type
                paragraph_type = self._classify_paragraph_type(paragraph)
                if paragraph_type != 'noise':
                    paragraphs.append({
                        'text': paragraph,
                        'type': paragraph_type,
                        'financial_density': self._calculate_financial_density(paragraph)
                    })
        
        return paragraphs
    
    def _classify_paragraph_type(self, paragraph: str) -> str:
        """Classify paragraph type based on content"""
        paragraph_lower = paragraph.lower()
        
        if any(term in paragraph_lower for term in ['risk factor', 'may adversely affect', 'could result in']):
            return 'risk_disclosure'
        elif any(term in paragraph_lower for term in ['financial statement', 'balance sheet', 'income statement']):
            return 'financial_statement'
        elif any(term in paragraph_lower for term in ['management discussion', 'md&a', 'executive summary']):
            return 'management_discussion'
        elif any(term in paragraph_lower for term in ['legal proceeding', 'lawsuit', 'litigation']):
            return 'legal_matters'
        elif any(term in paragraph_lower for term in ['$', 'million', 'billion', 'revenue', 'profit']):
            return 'financial_data'
        elif len(paragraph.split()) < 20:
            return 'noise'
        else:
            return 'general'
    
    def _calculate_financial_density(self, text: str) -> float:
        """Calculate financial term density in text"""
        financial_terms = [
            '$', 'million', 'billion', 'revenue', 'profit', 'loss', 'debt', 'equity',
            'assets', 'liabilities', 'eps', 'ebitda', 'margin', 'growth', 'decline'
        ]
        
        words = text.lower().split()
        if not words:
            return 0.0
        
        financial_count = sum(1 for word in words if any(term in word for term in financial_terms))
        return round(financial_count / len(words), 3)
    
    def extract_sentences_with_risk(self, text: str, risk_keywords: List[str]) -> Dict[str, List[Dict]]:
        """Extract sentences containing risk-related keywords with enhanced context"""
        sentences = re.split(r'[.!?]+', text)
        
        risk_sentences = {}
        for keyword in risk_keywords:
            risk_sentences[keyword] = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            for keyword in risk_keywords:
                if keyword.lower() in sentence.lower():
                    risk_sentences[keyword].append({
                        'sentence': sentence,
                        'intensity': self._calculate_risk_intensity(sentence),
                        'financial_context': self._extract_financial_context(sentence),
                        'contains_amount': bool(re.search(r'\$\d+', sentence))
                    })
        
        return risk_sentences
    
    def _calculate_risk_intensity(self, sentence: str) -> str:
        """Calculate risk intensity level for a sentence"""
        sentence_lower = sentence.lower()
        
        high_intensity_terms = ['severe', 'critical', 'material', 'significant', 'substantial', 'major']
        medium_intensity_terms = ['moderate', 'potential', 'could', 'may', 'possible']
        
        if any(term in sentence_lower for term in high_intensity_terms):
            return 'high'
        elif any(term in sentence_lower for term in medium_intensity_terms):
            return 'medium'
        else:
            return 'low'
    
    def _extract_financial_context(self, sentence: str) -> List[str]:
        """Extract financial context from sentence"""
        context = []
        
        # Extract dollar amounts
        amounts = re.findall(r'\$\d+(?:\.\d+)?(?:\s*(?:million|billion))?', sentence)
        if amounts:
            context.extend(amounts)
        
        # Extract percentages
        percentages = re.findall(r'\d+(?:\.\d+)?%', sentence)
        if percentages:
            context.extend(percentages)
        
        # Extract timeframes
        timeframes = re.findall(r'(?:Q[1-4]\s*\d{4}|\d{4})', sentence)
        if timeframes:
            context.extend(timeframes)
        
        return context
    
    def calculate_text_metrics(self, text: str) -> Dict[str, Any]:
        """Calculate comprehensive text metrics with financial intelligence"""
        words = text.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        # Count financial terms with enhanced categories
        financial_categories = {
            'monetary': ['$', 'million', 'billion', 'revenue', 'profit', 'loss'],
            'ratios': ['ratio', 'margin', 'growth', 'return', 'yield'],
            'risk': ['risk', 'uncertain', 'volatility', 'default', 'exposure'],
            'regulatory': ['sec', 'regulation', 'compliance', 'investigation', 'fine']
        }
        
        category_counts = {}
        for category, terms in financial_categories.items():
            category_counts[category] = sum(1 for word in words 
                                          if any(term in word.lower() for term in terms))
        
        # Calculate readability metrics (simplified)
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Financial complexity score
        financial_complexity = sum(category_counts.values()) / len(words) if words else 0
        
        return {
            'basic_metrics': {
                'word_count': len(words),
                'sentence_count': len(sentences),
                'paragraph_count': len(self.segment_into_paragraphs(text)),
                'avg_sentence_length': round(avg_sentence_length, 1),
                'avg_word_length': round(avg_word_length, 1)
            },
            'financial_metrics': {
                'total_financial_terms': sum(category_counts.values()),
                'financial_term_density': round(financial_complexity, 3),
                'category_breakdown': category_counts,
                'risk_term_ratio': round(category_counts['risk'] / len(words), 3) if words else 0
            },
            'readability_metrics': {
                'complexity_level': 'high' if financial_complexity > 0.1 else 'medium' if financial_complexity > 0.05 else 'low',
                'financial_jargon_density': round(category_counts['monetary'] / len(words), 3) if words else 0
            }
        }
    
    def normalize_financial_terms(self, text: str) -> str:
        """Normalize financial terms to standard format"""
        # Standardize currency formats
        text = re.sub(r'\$(\d+)\.?(\d*)\s*(million|billion|trillion)', 
                     lambda m: f"${m.group(1)}.{m.group(2) or '00'} {m.group(3)}", text)
        
        # Standardize percentage formats
        text = re.sub(r'(\d+(?:\.\d+)?)\s*percent', r'\1%', text, flags=re.IGNORECASE)
        
        # Standardize date formats
        text = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{4})', r'\1/\2/\3', text)
        
        # Standardize company names
        company_replacements = {
            'Apple Inc': 'Apple Inc.',
            'Microsoft Corp': 'Microsoft Corporation',
            'Google LLC': 'Alphabet Inc.',
            'Amazon.com Inc': 'Amazon.com Inc.',
            'Tesla Inc': 'Tesla Inc.'
        }
        
        for old, new in company_replacements.items():
            text = text.replace(old, new)
        
        return text