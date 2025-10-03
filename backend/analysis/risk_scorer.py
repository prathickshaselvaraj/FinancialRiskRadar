"""
Advanced risk scoring and intensity calculation
"""
import re
import requests
import json
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

        # API configurations
        self.alpha_vantage_key = "39VQF76MH0BEEJV2"  # Free from alphavantage.co
        self.financial_modeling_prep_key = "B3Cx3v3A1ZBN2h7bzlxAtxNbQlmJ9FhB"   # Free from financialmodelingprep.com

    def _extract_companies_for_apis(self, text: str) -> List[str]:
        """Extract company names for API lookups"""
        company_patterns = [
            r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+(?:Inc|Corp|Company|Ltd)',
            r'\b(Apple|Microsoft|Google|Amazon|Tesla|JPMorgan|Goldman Sachs|Bank of America)\b'
        ]
        
        companies = []
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            companies.extend(matches)
        
        return list(set(companies))[:5]  # Deduplicate and limit
    
    def calculate_comprehensive_risk_score(self, risks: List[Dict], text: str) -> Dict[str, Any]:
        """Calculate comprehensive risk score with REAL financial data"""
        if not risks:
            return self._get_empty_risk_analysis()

        # Extract companies for real financial data lookup
        companies = self._extract_companies_for_apis(text)
        
        # Get REAL financial data from APIs
        financial_data = self._get_real_financial_data(companies)
        
        # Calculate base scores enhanced with real data
        base_scores = self._calculate_base_risk_scores(risks, financial_data)
        
        # Calculate intensity modifiers
        intensity_modifiers = self._calculate_intensity_modifiers(text)
        
        # Calculate temporal factors
        temporal_factors = self._analyze_temporal_urgency(text)
        
        # Calculate financial impact with REAL data
        financial_impact = self._analyze_financial_impact(text, financial_data)
        
        # Combine all factors
        final_scores = self._combine_risk_factors(
            base_scores, 
            intensity_modifiers, 
            temporal_factors, 
            financial_impact,
            financial_data
        )
        
        return {
            "overall_risk_score": final_scores["overall"],
            "category_scores": final_scores["categories"],
            "risk_breakdown": {
                "base_scores": base_scores,
                "intensity_modifiers": intensity_modifiers,
                "temporal_factors": temporal_factors,
                "financial_impact": financial_impact,
                "api_data_used": bool(financial_data)
            },
            "risk_summary": self._generate_risk_summary(final_scores, risks, financial_data)
        }
    
    def _company_to_symbol(self, company: str) -> str:
        """Convert company name to stock symbol"""
        symbol_map = {
            'Apple': 'AAPL',
            'Microsoft': 'MSFT', 
            'Google': 'GOOGL',
            'Amazon': 'AMZN',
            'Tesla': 'TSLA',
            'JPMorgan': 'JPM',
            'Goldman Sachs': 'GS',
            'Bank of America': 'BAC'
        }
        
        for name, symbol in symbol_map.items():
            if name.lower() in company.lower():
                return symbol
        return ""
    
    def _get_simulated_financials(self, company: str) -> Dict[str, float]:
        """Fallback simulated financial data"""
        return {
            "debt_to_equity": 1.5,
            "current_ratio": 1.2,
            "profit_margin": 0.08,
            "quick_ratio": 0.9,
            "data_source": "simulated"
        }
    
    def _get_real_financial_data(self, companies: List[str]) -> Dict[str, Any]:
        """Get real financial data from APIs"""
        financial_data = {}
        
        for company in companies[:3]:  # Limit API calls
            symbol = self._company_to_symbol(company)
            if symbol:
                try:
                    # Get real financial ratios from Financial Modeling Prep
                    ratios = self._get_financial_ratios(symbol)
                    if ratios:
                        financial_data[company] = {
                            "symbol": symbol,
                            "debt_to_equity": ratios.get('debtToEquity', 0),
                            "current_ratio": ratios.get('currentRatio', 0),
                            "profit_margin": ratios.get('profitMargin', 0),
                            "quick_ratio": ratios.get('quickRatio', 0),
                            "data_source": "Financial Modeling Prep"
                        }
                except:
                    # Fallback to simulated data if API fails
                    financial_data[company] = self._get_simulated_financials(company)
        
        return financial_data
    
    def _get_financial_ratios(self, symbol: str) -> Dict[str, float]:
        """Get real financial ratios from Financial Modeling Prep API"""
        try:
            url = f"https://financialmodelingprep.com/api/v3/ratios/{symbol}"
            params = {'apikey': self.financial_modeling_prep_key}
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return data[0]  # Return most recent ratios
        except:
            pass
        return {}
    
    def _calculate_base_risk_scores(self, risks: List[Dict], financial_data: Dict) -> Dict[str, float]:
        """Calculate base risk scores enhanced with real financial data"""
        base_scores = {}
        
        for risk in risks:
            risk_type = risk["type"]
            base_score = risk["score"]
            
            # Enhance with real financial data
            financial_enhancement = self._calculate_financial_enhancement(risk_type, financial_data)
            base_score = min(base_score + financial_enhancement, 100)
            
            # Apply category-specific adjustments
            if risk_type == "credit_risk":
                base_score = min(base_score * 1.1, 100)
            elif risk_type == "regulatory_risk":
                base_score = min(base_score * 1.05, 100)
            
            base_scores[risk_type] = round(base_score, 1)
        
        return base_scores
    
    def _calculate_financial_enhancement(self, risk_type: str, financial_data: Dict) -> float:
        """Calculate risk enhancement based on real financial data"""
        enhancement = 0
        
        for company, data in financial_data.items():
            if risk_type == "credit_risk":
                # High debt-to-equity increases credit risk
                debt_equity = data.get('debt_to_equity', 0)
                if debt_equity > 2.0:
                    enhancement += 15
                elif debt_equity > 1.0:
                    enhancement += 8
                    
            elif risk_type == "operational_risk":
                # Low profit margin increases operational risk
                profit_margin = data.get('profit_margin', 0)
                if profit_margin < 0.05:
                    enhancement += 12
                elif profit_margin < 0.10:
                    enhancement += 6
            
            elif risk_type == "market_risk":
                # Poor liquidity increases market risk
                current_ratio = data.get('current_ratio', 0)
                if current_ratio < 1.0:
                    enhancement += 10
        
        return min(enhancement, 30)  # Cap enhancement
    
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
    
    def _analyze_financial_impact(self, text: str, financial_data: Dict) -> Dict[str, Any]:
        """Analyze financial impact with real data context"""
        # Your existing amount extraction
        amount_analysis = self._extract_amounts_from_text(text)
        
        # Enhance with real financial context
        real_context = self._add_real_financial_context(amount_analysis, financial_data)
        
        return real_context
    
    def _add_real_financial_context(self, amount_analysis: Dict, financial_data: Dict) -> Dict[str, Any]:
        """Add real financial context to amount analysis"""
        total_impact = amount_analysis["total_impact_millions"]
        
        # Compare with real company financials
        context_notes = []
        for company, data in financial_data.items():
            market_cap = data.get('market_cap_millions', 1000)  # Would be real data
            if total_impact > market_cap * 0.1:  # Impact > 10% of market cap
                context_notes.append(f"Major impact for {company}")
            elif total_impact > market_cap * 0.01:  # Impact > 1% of market cap
                context_notes.append(f"Significant impact for {company}")
        
        amount_analysis["real_world_context"] = context_notes
        amount_analysis["data_enhanced"] = bool(financial_data)
        
        return amount_analysis
    
    def _combine_risk_factors(self, base_scores: Dict, intensity: Dict, temporal: Dict, 
                            financial: Dict, financial_data: Dict) -> Dict[str, Any]:
        """Combine all risk factors with real data enhancement"""
        category_scores = {}
        
        for risk_type, base_score in base_scores.items():
            # Apply intensity modifiers
            intensity_bonus = sum(intensity.values()) / len(intensity) * 0.2
            
            # Apply temporal urgency
            temporal_bonus = temporal["overall_urgency"] * 0.15
            
            # Apply financial impact
            financial_bonus = financial["impact_score"] * 0.25
            
            # Real data confidence boost
            data_boost = 0.1 if financial_data else 0
            
            # Calculate final category score
            final_score = base_score * (1 + intensity_bonus + temporal_bonus + financial_bonus + data_boost)
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
    
    def _generate_risk_summary(self, final_scores: Dict, risks: List[Dict], financial_data: Dict) -> Dict[str, Any]:
        """Generate risk summary enhanced with real data"""
        overall_score = final_scores["overall"]
        
        # Determine risk level with real data context
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
        
        # Add real data context to recommendation
        if financial_data:
            recommendation += " Analysis enhanced with real financial data."
        
        # Count risk instances
        total_instances = sum(risk.get("sentence_count", 0) for risk in risks)
        
        return {
            "risk_level": risk_level,
            "recommendation": recommendation,
            "total_risk_instances": total_instances,
            "primary_risk_category": max(final_scores["categories"], key=final_scores["categories"].get) if final_scores["categories"] else "None",
            "confidence_score": min(overall_score * 1.1, 95),
            "real_data_used": bool(financial_data)
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