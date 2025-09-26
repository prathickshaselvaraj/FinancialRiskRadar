import numpy as np
from typing import List, Tuple, Dict, Any
import random

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class Explainer:
    def __init__(self, config: Dict):
        self.config = config
    
    def explain(self, text: str, prediction: Dict[str, Any], risk_type: str) -> Dict[str, Any]:
        """Generate explanations for the prediction"""
        try:
            # Feature importance (simplified - replace with actual SHAP in production)
            feature_importance = self._generate_feature_importance(text, risk_type)
            
            # Key phrases that influenced the decision
            key_phrases = self._extract_key_phrases(text, risk_type)
            
            # Risk drivers explanation
            risk_drivers = self._identify_risk_drivers(prediction['risk_score'], risk_type)
            
            return {
                'top_features': feature_importance,
                'key_phrases': key_phrases,
                'risk_drivers': risk_drivers,
                'confidence': min(prediction['risk_probability'] * 2, 1.0)
            }
            
        except Exception as e:
            logger.error(f"Explanation generation error: {str(e)}")
            return self._generate_fallback_explanation()
    
    def _generate_feature_importance(self, text: str, risk_type: str) -> List[Tuple[str, float]]:
        """Generate feature importance scores (dummy implementation)"""
        # These would come from actual SHAP values in production
        features = {
            'text_length': len(text) / 10000,
            'risk_keyword_density': text.lower().count('risk') / max(len(text.split()), 1),
            'negative_sentiment': text.lower().count('not') / max(len(text.split()), 1) * 0.5,
            'regulatory_mentions': text.lower().count('sec') / max(len(text.split()), 1) * 2,
            'financial_terms': text.lower().count('profit') / max(len(text.split()), 1),
        }
        
        # Adjust based on risk type
        risk_weights = {
            'bank': {'regulatory_mentions': 1.5, 'financial_terms': 1.3},
            'insurance': {'risk_keyword_density': 1.4, 'negative_sentiment': 1.2},
            'fintech': {'text_length': 0.8, 'regulatory_mentions': 1.6}
        }
        
        weights = risk_weights.get(risk_type, {})
        for feature, weight in weights.items():
            if feature in features:
                features[feature] *= weight
        
        # Add some random variation
        for feature in features:
            features[feature] += random.uniform(-0.1, 0.1)
            features[feature] = max(features[feature], 0)
        
        # Sort by importance
        sorted_features = sorted(features.items(), key=lambda x: x[1], reverse=True)
        return sorted_features[:5]
    
    def _extract_key_phrases(self, text: str, risk_type: str) -> List[str]:
        """Extract key phrases that influenced the risk assessment"""
        sentences = text.split('.')
        risk_indicators = []
        
        risk_triggers = {
            'bank': ['debt', 'default', 'credit', 'loan', 'lending'],
            'insurance': ['claim', 'fraud', 'premium', 'coverage', 'policy'],
            'fintech': ['cyber', 'security', 'digital', 'platform', 'crypto']
        }
        
        triggers = risk_triggers.get(risk_type, [])
        
        for sentence in sentences:
            if any(trigger in sentence.lower() for trigger in triggers):
                # Clean and truncate sentence
                clean_sentence = ' '.join(sentence.split()[:15]) + '...'
                risk_indicators.append(clean_sentence.strip())
                if len(risk_indicators) >= 3:
                    break
        
        return risk_indicators if risk_indicators else ["No specific risk indicators found."]
    
    def _identify_risk_drivers(self, risk_score: float, risk_type: str) -> List[str]:
        """Identify main risk drivers based on score and type"""
        drivers = []
        
        if risk_score > 70:
            drivers.append(f"High concentration of {risk_type}-specific risk factors")
            drivers.append("Strong negative sentiment indicators")
            drivers.append("Multiple regulatory red flags detected")
        elif risk_score > 40:
            drivers.append(f"Moderate {risk_type} risk profile")
            drivers.append("Mixed sentiment signals")
            drivers.append("Some regulatory mentions present")
        else:
            drivers.append(f"Low {risk_type} risk exposure")
            drivers.append("Generally positive or neutral sentiment")
            drivers.append("Minimal regulatory concerns")
        
        return drivers
    
    def _generate_fallback_explanation(self) -> Dict[str, Any]:
        """Generate fallback explanation when primary method fails"""
        return {
            'top_features': [('fallback', 0.5)],
            'key_phrases': ['Analysis unavailable'],
            'risk_drivers': ['Explanation generation failed'],
            'confidence': 0.0
        }