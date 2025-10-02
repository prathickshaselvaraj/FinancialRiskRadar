"""
Advanced risk scoring and intensity calculation
"""
import re
from typing import Dict, List, Any
from datetime import datetime

class RiskScorer:
    def __init__(self):
        self.risk_weights = {
            "credit_risk": 0.35,
            "market_risk": 0.25,
            "operational_risk": 0.20,
            "regulatory_risk": 0.20
        }
        
        self.intensity_factors = {
            "financial_magnitude": {
                "billion": 30,
                "million": 20,
                "thousand": 10,
                "percent": 15
            },
            "temporal_urgency": {
                "imminent": 25,
                "immediate": 25,
                "urgent": 20,
                "pending": 15,
                "potential": 10
            },
            "regulatory_severity": {
                "investigation": 25,
                "lawsuit": 30,
                "subpoena": 25,
                "enforcement": 20,
                "review": 15
            },
            "impact_scale": {
                "crisis": 30,
                "collapse": 30,
                "breach": 25,
                "failure": 20,
                "concern": 10
            }
        }
    
    def calculate_comprehensive_risk_score(self, risks: List[Dict], text: str) -> Dict[str, Any]:
        """Calculate comprehensive risk score with multiple factors"""
        if not risks:
            return self._get_empty_risk_analysis()
        
        # Calculate base scores
        base_scores = self._calculate_base_risk_scores(risks)
        
        # Calculate intensity modifiers
        intensity_modifiers = self._calculate_intensity_modifiers(text)
        
        # Calculate temporal factors
        temporal_factors = self._analyze_temporal_urgency(text)
        
        # Calculate financial impact
        financial_impact = self._analyze_financial_impact(text)
        
        # Combine all factors
        final_scores = self._combine_risk_factors(
            base_scores, 
            intensity_modifiers, 
            temporal_factors, 
            financial_impact
        )
        
        return {
            "overall_risk_score": final_scores["overall"],
            "category_scores": final_scores["categories"],
            "risk_breakdown": {
                "base_scores": base_scores,
                "intensity_modifiers": intensity_modifiers,
                "temporal_factors": temporal_factors,
                "financial_impact": financial_impact
            },
            "risk_summary": self._generate_risk_summary(final_scores, risks)
        }
    
    def _calculate_base_risk_scores(self, risks: List[Dict]) -> Dict[str, float]:
        """Calculate base risk scores from detected risks"""
        base_scores = {}
        
        for risk in risks:
            risk_type = risk["type"]
            base_score = risk["score"]
            
            # Apply category-specific adjustments
            if risk_type == "credit_risk":
                # Credit risks are typically more severe
                base_score = min(base_score * 1.1, 100)
            elif risk_type == "regulatory_risk":
                # Regulatory risks often have immediate consequences
                base_score = min(base_score * 1.05, 100)
            
            base_scores[risk_type] = round(base_score, 1)
        
        return base_scores
    
    def _calculate_intensity_modifiers(self, text: str) -> Dict[str, float]:
        """Calculate intensity modifiers based on language used"""
        text_lower = text.lower()
        modifiers = {}
        
        for factor_type, factors in self.intensity_factors.items():
            factor_score = 0
            max_possible = 0
            
            for term, weight in factors.items():
                max_possible += weight
                if term in text_lower:
                    factor_score += weight
            
            # Convert to percentage
            modifiers[factor_type] = (factor_score / max_possible * 100) if max_possible > 0 else 0
        
        return modifiers
    
    def _analyze_temporal_urgency(self, text: str) -> Dict[str, Any]:
        """Analyze temporal urgency of risks"""
        text_lower = text.lower()
        
        # Extract time references
        time_patterns = {
            "immediate": r'\b(immediately|now|urgent|asap)\b',
            "short_term": r'\b(soon|shortly|coming weeks|next month)\b',
            "medium_term": r'\b(Q[1-4]\s*\d{4}|next quarter|this year)\b',
            "long_term": r'\b(long.?term|future|beyond|subsequent)\b'
        }
        
        urgency_scores = {}
        for timeframe, pattern in time_patterns.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            urgency_scores[timeframe] = len(matches)
        
        # Calculate overall urgency
        total_references = sum(urgency_scores.values())
        immediate_weight = urgency_scores["immediate"] * 100
        short_term_weight = urgency_scores["short_term"] * 75
        medium_term_weight = urgency_scores["medium_term"] * 50
        long_term_weight = urgency_scores["long_term"] * 25
        
        total_weighted = immediate_weight + short_term_weight + medium_term_weight + long_term_weight
        max_possible = total_references * 100 if total_references > 0 else 1
        
        overall_urgency = (total_weighted / max_possible) * 100
        
        return {
            "overall_urgency": round(overall_urgency, 1),
            "time_references": urgency_scores,
            "primary_timeframe": max(urgency_scores, key=urgency_scores.get) if total_references > 0 else "unknown"
        }
    
    def _analyze_financial_impact(self, text: str) -> Dict[str, Any]:
        """Analyze financial impact magnitude"""
        # Extract financial amounts
        amount_patterns = [
            r'\$(\d+(?:\.\d+)?)\s*(billion|million|thousand)',
            r'(\d+(?:\.\d+)?)\s*(billion|million|thousand)\s+dollars',
            r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)'  # Standard dollar amounts
        ]
        
        amounts_found = []
        total_value = 0
        
        for pattern in amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    value, unit = match
                    numeric_value = float(value.replace(',', ''))
                    
                    # Convert to base units (millions)
                    if unit.lower() == 'billion':
                        numeric_value *= 1000
                    elif unit.lower() == 'thousand':
                        numeric_value /= 1000
                    
                    amounts_found.append({
                        "original": f"${value} {unit}",
                        "value_millions": numeric_value
                    })
                    total_value += numeric_value
                else:
                    # Single dollar amount
                    value = match[0]
                    numeric_value = float(value.replace(',', '')) / 1000000  # Convert to millions
                    amounts_found.append({
                        "original": f"${value}",
                        "value_millions": numeric_value
                    })
                    total_value += numeric_value
        
        # Calculate impact score based on total value
        impact_score = 0
        if total_value > 0:
            if total_value > 1000:  # Over 1 billion
                impact_score = 90
            elif total_value > 100:  # Over 100 million
                impact_score = 70
            elif total_value > 10:   # Over 10 million
                impact_score = 50
            elif total_value > 1:    # Over 1 million
                impact_score = 30
            else:
                impact_score = 15
        
        return {
            "total_impact_millions": round(total_value, 2),
            "amounts_found": amounts_found,
            "impact_score": impact_score,
            "impact_level": self._get_impact_level(impact_score)
        }
    
    def _combine_risk_factors(self, base_scores: Dict, intensity: Dict, temporal: Dict, financial: Dict) -> Dict[str, Any]:
        """Combine all risk factors into final scores"""
        category_scores = {}
        
        for risk_type, base_score in base_scores.items():
            # Apply intensity modifiers
            intensity_bonus = sum(intensity.values()) / len(intensity) * 0.2
            
            # Apply temporal urgency
            temporal_bonus = temporal["overall_urgency"] * 0.15
            
            # Apply financial impact
            financial_bonus = financial["impact_score"] * 0.25
            
            # Calculate final category score
            final_score = base_score * (1 + intensity_bonus + temporal_bonus + financial_bonus)
            category_scores[risk_type] = min(round(final_score, 1), 100)
        
        # Calculate overall risk score
        overall_score = 0
        total_weight = 0
        
        for risk_type, score in category_scores.items():
            weight = self.risk_weights.get(risk_type, 0.25)
            overall_score += score * weight
            total_weight += weight
        
        overall_final = overall_score / total_weight if total_weight > 0 else 0
        
        return {
            "overall": round(overall_final, 1),
            "categories": category_scores
        }
    
    def _get_impact_level(self, score: float) -> str:
        """Get human-readable impact level"""
        if score >= 80:
            return "Severe"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Moderate"
        elif score >= 20:
            return "Low"
        else:
            return "Minimal"
    
    def _generate_risk_summary(self, final_scores: Dict, risks: List[Dict]) -> Dict[str, Any]:
        """Generate comprehensive risk summary"""
        overall_score = final_scores["overall"]
        
        # Determine risk level
        if overall_score >= 80:
            risk_level = "Critical"
            recommendation = "Immediate attention required. Significant financial and operational impacts likely."
        elif overall_score >= 60:
            risk_level = "High"
            recommendation = "Urgent review needed. Potential for material impacts."
        elif overall_score >= 40:
            risk_level = "Moderate"
            recommendation = "Monitor closely. Some potential for negative impacts."
        elif overall_score >= 20:
            risk_level = "Low"
            recommendation = "Standard monitoring. Limited immediate concerns."
        else:
            risk_level = "Minimal"
            recommendation = "Routine oversight. No significant risks identified."
        
        # Count risk instances
        total_instances = sum(risk.get("sentence_count", 0) for risk in risks)
        
        return {
            "risk_level": risk_level,
            "recommendation": recommendation,
            "total_risk_instances": total_instances,
            "primary_risk_category": max(final_scores["categories"], key=final_scores["categories"].get) if final_scores["categories"] else "None",
            "confidence_score": min(overall_score * 1.1, 95)  # Confidence based on analysis depth
        }
    
    def _get_empty_risk_analysis(self) -> Dict[str, Any]:
        """Return empty risk analysis structure"""
        return {
            "overall_risk_score": 0,
            "category_scores": {},
            "risk_breakdown": {
                "base_scores": {},
                "intensity_modifiers": {},
                "temporal_factors": {"overall_urgency": 0, "time_references": {}, "primary_timeframe": "unknown"},
                "financial_impact": {"total_impact_millions": 0, "amounts_found": [], "impact_score": 0, "impact_level": "Minimal"}
            },
            "risk_summary": {
                "risk_level": "Minimal",
                "recommendation": "No significant risks identified in the analyzed content.",
                "total_risk_instances": 0,
                "primary_risk_category": "None",
                "confidence_score": 0
            }
        }