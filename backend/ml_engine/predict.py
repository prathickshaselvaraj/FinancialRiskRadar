import pickle
import numpy as np
from typing import Dict, Any, List  # Added List import
import os

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class RiskPredictor:
    def __init__(self, config: Dict):
        self.config = config
        self.models = {}
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models for each risk type"""
        model_paths = {
            'bank': self.config['models']['bank']['path'],
            'insurance': self.config['models']['insurance']['path'],
            'fintech': self.config['models']['fintech']['path']
        }
        
        for risk_type, path in model_paths.items():
            try:
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        self.models[risk_type] = pickle.load(f)
                    logger.info(f"Loaded {risk_type} model from {path}")
                else:
                    logger.warning(f"Model file not found: {path}. Using dummy model.")
                    self.models[risk_type] = DummyModel(risk_type)
            except Exception as e:
                logger.error(f"Error loading {risk_type} model: {str(e)}")
                self.models[risk_type] = DummyModel(risk_type)
    
    def predict(self, text: str, risk_type: str) -> Dict[str, Any]:
        """Predict risk score for given text and risk type"""
        try:
            if risk_type not in self.models:
                raise ValueError(f"Unsupported risk type: {risk_type}")
            
            # Extract features
            features = self._extract_dummy_features(text, risk_type)
            
            # Get prediction from model
            model = self.models[risk_type]
            risk_probability = model.predict_proba([features])[0][1]
            
            # Convert to score 0-100
            risk_score = risk_probability * 100
            
            # Determine verdict
            threshold = self.config['models'][risk_type]['threshold'] * 100
            if risk_score >= threshold + 20:
                verdict = "HIGH"
            elif risk_score >= threshold:
                verdict = "MEDIUM"
            else:
                verdict = "LOW"
            
            return {
                'risk_score': round(risk_score, 1),
                'risk_probability': round(risk_probability, 3),
                'verdict': verdict,
                'risk_type': risk_type,
                'features_used': len(features)
            }
            
        except Exception as e:
            logger.error(f"Prediction error for {risk_type}: {str(e)}")
            return {
                'risk_score': 50.0,  # Neutral fallback
                'risk_probability': 0.5,
                'verdict': "UNKNOWN",
                'risk_type': risk_type,
                'error': str(e)
            }
    
    def _extract_dummy_features(self, text: str, risk_type: str) -> List[float]:  # Fixed type hint
        """Dummy feature extraction - replace with actual NLP features"""
        # Simple features based on text length and risk type
        features = [
            len(text) / 10000,  # Normalized length
            text.lower().count('risk') / max(len(text.split()), 1),
            text.lower().count(risk_type) / max(len(text.split()), 1),
            len([w for w in text.split() if w.isupper()]) / max(len(text.split()), 1),
        ]
        
        # Add some random variation for demo purposes
        features.extend([np.random.random() * 0.1 for _ in range(6)])
        
        return features

class DummyModel:
    """Dummy model for demonstration when real models aren't available"""
    def __init__(self, risk_type: str):
        self.risk_type = risk_type
    
    def predict_proba(self, X):
        # Base risk based on risk type + some randomness
        base_risk = {
            'bank': 0.3,
            'insurance': 0.4, 
            'fintech': 0.5
        }.get(self.risk_type, 0.5)
        
        # Add some variation based on input features
        variation = np.mean(X) * 0.1 if len(X) > 0 else 0
        risk = min(max(base_risk + variation + np.random.normal(0, 0.1), 0), 1)
        
        return np.array([[1 - risk, risk]])