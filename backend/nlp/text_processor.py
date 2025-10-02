"""
Advanced text processing and normalization for financial documents
"""
import re
import html
from typing import List, Dict

class FinancialTextProcessor:
    def __init__(self):
        self.financial_abbreviations = {
            'sec': 'SEC',
            'fed': 'Federal Reserve',
            'nyse': 'NYSE',
            'nasdaq': 'NASDAQ',
            'ceo': 'CEO',
            'cfo': 'CFO',
            'gaap': 'GAAP',
            'ifrs': 'IFRS',
            'ebitda': 'EBITDA',
            'eps': 'EPS'
        }
        
        self.noise_patterns = [
            r'\s+',  # Multiple spaces
            r'\[.*?\]',  # Square brackets content
            r'\(.*?\)',  # Parentheses content (but keep financial amounts)
            r'<.*?>',  # HTML tags
            r'\bPage\s+\d+\b',  # Page numbers
            r'\bFigure\s+\d+\b',  # Figure references
        ]
    
    def clean_financial_text(self, text: str) -> str:
        """Comprehensive text cleaning for financial documents"""
        if not text:
            return ""
        
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
        
        return text.strip()
    
    def _fix_financial_formatting(self, text: str) -> str:
        """Fix common financial document formatting issues"""
        # Fix broken dollar amounts
        text = re.sub(r'\$\s+(\d)', r'$\1', text)
        
        # Fix percentage formatting
        text = re.sub(r'(\d)\s+%', r'\1%', text)
        
        # Fix date formatting
        text = re.sub(r'(\d{4})\s+-\s+(\d{4})', r'\1-\2', text)
        
        # Fix common financial term casing
        financial_terms = ['SEC', 'GAAP', 'IFRS', 'EBITDA', 'EPS', 'IPO']
        for term in financial_terms:
            text = re.sub(r'\b' + term.lower() + r'\b', term, text, flags=re.IGNORECASE)
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand common financial abbreviations"""
        for abbr, expansion in self.financial_abbreviations.items():
            text = re.sub(r'\b' + abbr + r'\b', expansion, text, flags=re.IGNORECASE)
        return text
    
    def segment_into_paragraphs(self, text: str, min_paragraph_length: int = 50) -> List[str]:
        """Segment text into meaningful paragraphs"""
        # Split by multiple newlines
        raw_paragraphs = re.split(r'\n\s*\n', text)
        
        # Filter and clean paragraphs
        paragraphs = []
        for paragraph in raw_paragraphs:
            paragraph = paragraph.strip()
            if len(paragraph) >= min_paragraph_length:
                # Remove paragraph numbers and bullet points
                paragraph = re.sub(r'^\s*[\d•\-]\s*', '', paragraph)
                paragraphs.append(paragraph)
        
        return paragraphs
    
    def extract_sentences_with_risk(self, text: str, risk_keywords: List[str]) -> Dict[str, List[str]]:
        """Extract sentences containing risk-related keywords"""
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
                    risk_sentences[keyword].append(sentence)
        
        return risk_sentences
    
    def calculate_text_metrics(self, text: str) -> Dict[str, int]:
        """Calculate comprehensive text metrics"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        # Count financial terms
        financial_terms = ['$', '%', 'million', 'billion', 'revenue', 'profit', 'loss', 'debt']
        financial_count = sum(1 for word in words if any(term in word.lower() for term in financial_terms))
        
        # Count risk terms
        risk_terms = ['risk', 'uncertain', 'volatility', 'default', 'investigation', 'compliance']
        risk_count = sum(1 for word in words if any(term in word.lower() for term in risk_terms))
        
        return {
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'paragraph_count': len(self.segment_into_paragraphs(text)),
            'financial_term_count': financial_count,
            'risk_term_count': risk_count,
            'avg_sentence_length': len(words) / len([s for s in sentences if s.strip()]) if sentences else 0
        }