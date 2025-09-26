import re
from typing import Dict, List, Tuple, Any
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class RiskTagger:
    """Class for tagging and categorizing risks in text"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.risk_categories = config.get('nlp', {}).get('risk_categories', [])
        
        # Define risk patterns for different categories
        self.risk_patterns = {
            'regulatory': {
                'keywords': ['sec', 'regulation', 'compliance', 'audit', 'violation', 
                           'investigation', 'subpoena', 'enforcement', 'fined', 'penalty'],
                'patterns': [
                    r'\bsec\b.*\binvestigation\b',
                    r'\bregulatory.*\bviolation\b',
                    r'\bcompliance.*\bissue\b'
                ]
            },
            'financial': {
                'keywords': ['loss', 'decline', 'debt', 'bankruptcy', 'default', 
                           'restatement', 'write-down', 'impairment', 'losses', 'declining'],
                'patterns': [
                    r'\bnet.*\bloss\b',
                    r'\bdebt.*\bincrease\b',
                    r'\brevenue.*\bdecline\b'
                ]
            },
            'operational': {
                'keywords': ['cyberattack', 'breach', 'outage', 'disruption', 
                           'supply chain', 'operational risk', 'business interruption', 'downtime'],
                'patterns': [
                    r'\bcyber.*\battack\b',
                    r'\bdata.*\bbreach\b',
                    r'\bsystem.*\boutage\b'
                ]
            },
            'reputational': {
                'keywords': ['scandal', 'lawsuit', 'controversy', 'reputation', 
                           'brand damage', 'public relations', 'crisis', 'lawsuit'],
                'patterns': [
                    r'\breputation.*\bdamage\b',
                    r'\bpublic.*\brelations.*\bcrisis\b',
                    r'\bbrand.*\bimage\b.*\bnegative\b'
                ]
            }
        }
    
    def tag_risks(self, text: str) -> Dict[str, float]:
        """Tag text with risk categories and return scores"""
        try:
            text_lower = text.lower()
            risk_scores = {}
            
            for category, patterns in self.risk_patterns.items():
                score = self._calculate_category_score(text_lower, patterns)
                risk_scores[category] = score
            
            return risk_scores
            
        except Exception as e:
            logger.error(f"Error in risk tagging: {str(e)}")
            return {category: 0.0 for category in self.risk_patterns.keys()}
    
    def _calculate_category_score(self, text: str, patterns: Dict) -> float:
        """Calculate risk score for a specific category"""
        score = 0.0
        
        # Keyword-based scoring
        keyword_matches = 0
        for keyword in patterns['keywords']:
            if keyword in text:
                keyword_matches += 1
                # Each keyword match adds to the score
                score += 0.1
        
        # Pattern-based scoring (regex patterns)
        pattern_matches = 0
        for pattern in patterns['patterns']:
            if re.search(pattern, text, re.IGNORECASE):
                pattern_matches += 1
                # Each pattern match adds more weight
                score += 0.3
        
        # Normalize score (cap at 1.0)
        total_possible = len(patterns['keywords']) * 0.1 + len(patterns['patterns']) * 0.3
        if total_possible > 0:
            score = min(score / total_possible, 1.0)
        
        return score
    
    def extract_risk_phrases(self, text: str, category: str) -> List[str]:
        """Extract specific phrases that indicate risk for a category"""
        if category not in self.risk_patterns:
            return []
        
        risk_phrases = []
        patterns = self.risk_patterns[category]
        
        # Extract sentences containing keywords
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(keyword in sentence_lower for keyword in patterns['keywords']):
                # Clean up the sentence
                clean_sentence = ' '.join(sentence.split())
                if len(clean_sentence) > 10:  # Avoid very short sentences
                    risk_phrases.append(clean_sentence)
            
            # Also check for pattern matches
            for pattern in patterns['patterns']:
                if re.search(pattern, sentence_lower):
                    clean_sentence = ' '.join(sentence.split())
                    if len(clean_sentence) > 10:
                        risk_phrases.append(clean_sentence)
        
        # Return unique phrases, limit to top 5
        return list(set(risk_phrases))[:5]
    
    def get_risk_summary(self, text: str) -> Dict[str, Any]:
        """Get comprehensive risk analysis summary"""
        risk_scores = self.tag_risks(text)
        risk_phrases = {}
        
        for category in risk_scores.keys():
            risk_phrases[category] = self.extract_risk_phrases(text, category)
        
        # Calculate overall risk
        overall_risk = sum(risk_scores.values()) / len(risk_scores) if risk_scores else 0.0
        
        return {
            'risk_scores': risk_scores,
            'risk_phrases': risk_phrases,
            'overall_risk': overall_risk,
            'primary_risk': max(risk_scores.items(), key=lambda x: x[1])[0] if risk_scores else 'unknown'
        }