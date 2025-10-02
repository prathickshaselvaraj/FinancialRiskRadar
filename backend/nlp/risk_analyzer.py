"""
Advanced financial risk detection without ML
"""
import re
from typing import Dict, List, Any

class FinancialRiskAnalyzer:
    def __init__(self):
        self.risk_categories = {
            "credit_risk": {
                "keywords": ["default", "bankruptcy", "liquidity", "debt", "leverage", "collateral", 
                           "loan loss", "borrowing risk", "insolvency", "credit crisis"],
                "intensity_indicators": ["crisis", "severe", "imminent", "unable to pay"],
                "context_phrases": ["unable to meet", "facing default", "credit deterioration"],
                "weight": 0.35,
                "color": "#FF6B6B"
            },
            "market_risk": {
                "keywords": ["volatility", "market crash", "recession", "inflation", "interest rates",
                           "economic downturn", "trading loss", "currency risk", "commodity prices"],
                "intensity_indicators": ["crash", "collapse", "plunge", "sharp decline"],
                "context_phrases": ["impacted by market", "due to economic", "affected by volatility"],
                "weight": 0.25,
                "color": "#4ECDC4"
            },
            "operational_risk": {
                "keywords": ["fraud", "cybersecurity", "data breach", "system outage", "compliance",
                           "internal controls", "operational failure", "process breakdown"],
                "intensity_indicators": ["breach", "outage", "failure", "breakdown"],
                "context_phrases": ["system failure", "security incident", "control weakness"],
                "weight": 0.20,
                "color": "#45B7D1"
            },
            "regulatory_risk": {
                "keywords": ["SEC", "investigation", "fines", "regulation", "lawsuit", "enforcement",
                           "legal action", "compliance failure", "penalties", "subpoena"],
                "intensity_indicators": ["investigation", "lawsuit", "subpoena", "enforcement"],
                "context_phrases": ["under investigation", "facing lawsuit", "regulatory action"],
                "weight": 0.20,
                "color": "#96CEB4"
            }
        }
    
    def analyze_risk_context(self, text: str) -> List[Dict[str, Any]]:
        """Advanced risk analysis with context awareness"""
        text_lower = text.lower()
        sentences = re.split(r'[.!?]+', text)
        
        detected_risks = []
        
        for risk_type, config in self.risk_categories.items():
            risk_instances = []
            total_intensity = 0
            
            for sentence in sentences:
                sentence_lower = sentence.lower().strip()
                if not sentence_lower:
                    continue
                
                # Find risk keywords in sentence
                found_keywords = []
                for keyword in config["keywords"]:
                    if keyword in sentence_lower:
                        found_keywords.append(keyword)
                
                if found_keywords:
                    # Calculate sentence intensity
                    intensity_score = 0
                    
                    # Base score from keyword count
                    intensity_score += len(found_keywords) * 10
                    
                    # Intensity modifiers
                    for indicator in config["intensity_indicators"]:
                        if indicator in sentence_lower:
                            intensity_score += 20
                    
                    # Context awareness
                    for phrase in config["context_phrases"]:
                        if phrase in sentence_lower:
                            intensity_score += 15
                    
                    # Financial magnitude detection
                    amount_matches = re.findall(r'\$\d+(?:\.\d+)?(?:\s+[mb]illion)?', sentence)
                    if amount_matches:
                        intensity_score += len(amount_matches) * 10
                    
                    risk_instances.append({
                        "sentence": sentence.strip(),
                        "keywords": found_keywords,
                        "intensity": min(intensity_score, 100),
                        "financial_impact": amount_matches
                    })
                    total_intensity += intensity_score
            
            if risk_instances:
                avg_intensity = total_intensity / len(risk_instances)
                risk_score = min(avg_intensity, 95)  # Cap at 95%
                
                detected_risks.append({
                    "type": risk_type,
                    "score": risk_score,
                    "instances": risk_instances,
                    "keywords_found": list(set([kw for instance in risk_instances for kw in instance["keywords"]])),
                    "color": config["color"],
                    "description": f"Detected {len(risk_instances)} risk instances",
                    "sentence_count": len(risk_instances)
                })
        
        return detected_risks
    
    def calculate_overall_risk(self, risks: List[Dict]) -> float:
        """Calculate weighted overall risk score"""
        if not risks:
            return 0
        
        total_weighted_score = 0
        total_weight = 0
        
        for risk in risks:
            weight = self.risk_categories[risk["type"]]["weight"]
            total_weighted_score += risk["score"] * weight
            total_weight += weight
        
        return round(total_weighted_score / total_weight, 1) if total_weight > 0 else 0