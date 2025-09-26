import numpy as np
from typing import List, Dict
import re
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class FeatureExtractor:
    def __init__(self, config: Dict):
        self.config = config
    
    def extract_all_features(self, text: str) -> np.ndarray:
        """Extract comprehensive feature set from text"""
        features = []
        
        # 1. Basic text statistics
        features.extend(self._extract_text_statistics(text))
        
        # 2. Risk keyword features
        features.extend(self._extract_risk_keyword_features(text))
        
        # 3. Sentiment-related features
        features.extend(self._extract_sentiment_features(text))
        
        return np.array(features)
    
    def _extract_text_statistics(self, text: str) -> List[float]:
        """Extract basic text statistics"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        
        stats = [
            len(text) / 1000,  # Normalized text length
            len(words) / 100,  # Normalized word count
            len(sentences) / 10,  # Normalized sentence count
            len(words) / max(len(sentences), 1),  # Avg sentence length
        ]
        
        return stats
    
    def _extract_risk_keyword_features(self, text: str) -> List[float]:
        """Extract features based on risk-related keywords"""
        risk_categories = {
            'financial_risk': ['loss', 'debt', 'default', 'bankruptcy', 'decline'],
            'regulatory_risk': ['sec', 'regulation', 'compliance', 'violation', 'investigation'],
            'operational_risk': ['breach', 'outage', 'failure', 'disruption', 'cyber'],
        }
        
        text_lower = text.lower()
        words = text_lower.split()
        total_words = max(len(words), 1)
        
        features = []
        for category, keywords in risk_categories.items():
            # Keyword frequency
            frequency = sum(1 for word in words if word in keywords) / total_words
            features.append(frequency)
        
        return features
    
    def _extract_sentiment_features(self, text: str) -> List[float]:
        """Extract sentiment-related features"""
        positive_words = ['profit', 'growth', 'success', 'increase', 'positive', 'strong']
        negative_words = ['loss', 'decline', 'risk', 'challenge', 'negative', 'weak']
        
        text_lower = text.lower()
        words = text_lower.split()
        total_words = max(len(words), 1)
        
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        
        return [
            pos_count / total_words,
            neg_count / total_words,
            (neg_count - pos_count) / total_words,
        ]