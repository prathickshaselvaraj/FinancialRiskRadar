import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import spacy
import re

from .feature_extraction import FeatureExtractor
from .risk_tagging import RiskTagger  # This should work now
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class NLPPipeline:
    def __init__(self, config: Dict):
        self.config = config
        self.feature_extractor = FeatureExtractor(config)
        self.risk_tagger = RiskTagger(config)  # Now this will work
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning("spaCy model not found. Using basic text processing.")
            self.nlp = None
        
    def analyze_risk_tags(self, text: str) -> Dict[str, float]:
        """Analyze text and return risk category scores"""
        try:
            # Use the RiskTagger to get risk scores
            risk_scores = self.risk_tagger.tag_risks(text)
            
            # Add sentiment analysis if spaCy is available
            if self.nlp and len(text) > 100:
                doc = self.nlp(text[:100000])  # Limit text length
                sentiment_score = self._analyze_sentiment_spacy(doc)
            else:
                sentiment_score = self._analyze_sentiment_basic(text)
            
            # Add sentiment to risk scores
            risk_scores['sentiment'] = sentiment_score
            
            # Calculate overall score
            risk_scores['overall'] = np.mean(list(risk_scores.values()))
            
            logger.info(f"Risk analysis completed. Overall score: {risk_scores['overall']:.3f}")
            return risk_scores
            
        except Exception as e:
            logger.error(f"Error in risk analysis: {str(e)}")
            return self._get_fallback_scores()
    
    def _analyze_sentiment_spacy(self, doc) -> float:
        """Basic sentiment analysis using spaCy"""
        positive_words = ['profit', 'growth', 'increase', 'success', 'positive', 'strong', 'improve']
        negative_words = ['loss', 'decline', 'risk', 'failure', 'negative', 'weak', 'downgrade']
        
        positive_count = sum(1 for token in doc if token.lemma_.lower() in positive_words)
        negative_count = sum(1 for token in doc if token.lemma_.lower() in negative_words)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.5
        
        return negative_count / total  # Higher negative = higher risk
    
    def _analyze_sentiment_basic(self, text: str) -> float:
        """Fallback sentiment analysis without spaCy"""
        positive_words = ['profit', 'growth', 'increase', 'success', 'positive']
        negative_words = ['loss', 'decline', 'risk', 'failure', 'negative']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.5
        
        return negative_count / total
    
    def _get_fallback_scores(self) -> Dict[str, float]:
        """Return fallback scores when analysis fails"""
        return {
            'regulatory': 0.0,
            'financial': 0.0,
            'operational': 0.0,
            'reputational': 0.0,
            'sentiment': 0.5,
            'overall': 0.1
        }
    
    def extract_features(self, text: str) -> np.ndarray:
        """Extract features for ML model"""
        return self.feature_extractor.extract_all_features(text)