"""
Risk trend and pattern analysis with REAL market data integration
"""
import re
import requests
import json
from typing import Dict, List, Any
import numpy as np
from datetime import datetime, timedelta

class RiskTrendAnalyzer:
    def __init__(self):
        self.risk_keywords = [
            'risk', 'uncertainty', 'volatility', 'default', 'investigation',
            'compliance', 'breach', 'failure', 'lawsuit', 'fines'
        ]
        
        # API configurations
        self.alpha_vantage_key = "39VQF76MH0BEEJV2"  # Your Alpha Vantage key
        self.financial_modeling_prep_key = "B3Cx3v3A1ZBN2h7bzlxAtxNbQlmJ9FhB"  # Your FMP key
    
    def analyze_risk_trends(self, text: str, risks: List[Dict]) -> Dict[str, Any]:
        """Analyze risk distribution and trends with REAL market data"""
        if not text or not risks:
            return self._get_empty_trend_analysis()
        
        # Extract companies for market data lookup
        companies = self._extract_companies_for_market_data(text)
        
        # Get REAL market data
        market_data = self._get_market_volatility_data(companies)
        
        # Segment document
        segments = self._segment_document(text)
        
        # Analyze risk distribution with market context
        distribution = self._analyze_risk_distribution(segments, risks, market_data)
        
        # Calculate risk density trends
        density_trend = self._calculate_density_trend(segments)
        
        # Identify risk hotspots with market volatility context
        hotspots = self._identify_risk_hotspots(segments, risks, market_data)
        
        # Analyze risk evolution
        evolution = self._analyze_risk_evolution(segments)
        
        return {
            "risk_distribution": distribution,
            "density_trend": density_trend,
            "risk_hotspots": hotspots,
            "risk_evolution": evolution,
            "segment_count": len(segments),
            "market_context": market_data,
            "trend_summary": self._generate_trend_summary(distribution, density_trend, hotspots, market_data)
        }
    
    def _extract_companies_for_market_data(self, text: str) -> List[str]:
        """Extract company names for market data lookup"""
        company_patterns = [
            r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+(?:Inc|Corp|Company|Ltd)',
            r'\b(Apple|Microsoft|Google|Amazon|Tesla|JPMorgan|Goldman Sachs|Bank of America)\b'
        ]
        
        companies = []
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            companies.extend(matches)
        
        return list(set(companies))[:3]  # Deduplicate and limit
    
    def _get_market_volatility_data(self, companies: List[str]) -> Dict[str, Any]:
        """Get real market volatility data for trend analysis"""
        market_data = {
            "companies_analyzed": [],
            "volatility_metrics": {},
            "market_context": "unknown"
        }
        
        for company in companies:
            symbol = self._company_to_symbol(company)
            if symbol:
                try:
                    # Get stock volatility data
                    volatility_data = self._get_stock_volatility(symbol)
                    if volatility_data:
                        market_data["companies_analyzed"].append(company)
                        market_data["volatility_metrics"][company] = volatility_data
                        
                except Exception as e:
                    # Fallback to simulated market data
                    market_data["volatility_metrics"][company] = self._get_simulated_volatility(company)
        
        # Determine overall market context
        if market_data["volatility_metrics"]:
            avg_volatility = np.mean([data.get('volatility', 0) for data in market_data["volatility_metrics"].values()])
            if avg_volatility > 0.4:
                market_data["market_context"] = "high_volatility"
            elif avg_volatility > 0.2:
                market_data["market_context"] = "moderate_volatility"
            else:
                market_data["market_context"] = "low_volatility"
        
        market_data["data_source"] = "Alpha Vantage" if any('beta' in data for data in market_data["volatility_metrics"].values()) else "simulated"
        
        return market_data
    
    def _get_stock_volatility(self, symbol: str) -> Dict[str, float]:
        """Get stock volatility data from Alpha Vantage"""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                beta = float(data.get('Beta', 1.0))
                
                # Calculate volatility score (simplified)
                volatility_score = min(abs(beta - 1) * 0.5, 1.0)  # Higher beta = higher volatility
                
                return {
                    'beta': beta,
                    'volatility': volatility_score,
                    'pe_ratio': float(data.get('PERatio', 0)),
                    'market_cap': data.get('MarketCapitalization', '0')
                }
                
        except Exception as e:
            print(f"Market data API error for {symbol}: {e}")
        
        return {}
    
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
    
    def _analyze_risk_distribution(self, segments: List[Dict], risks: List[Dict], market_data: Dict) -> Dict[str, Any]:
        """Analyze how risks are distributed across document segments with market context"""
        segment_risks = []
        
        for i, segment in enumerate(segments):
            segment_text = segment["text"].lower()
            segment_risk_score = 0
            risk_categories_in_segment = []
            
            # Calculate risk density for this segment
            risk_word_count = sum(1 for word in segment_text.split() 
                                if any(keyword in word for keyword in self.risk_keywords))
            total_words = len(segment_text.split())
            risk_density = (risk_word_count / total_words * 100) if total_words > 0 else 0
            
            # Check for specific risk categories
            for risk in risks:
                risk_type = risk["type"]
                for keyword in risk.get("keywords_found", []):
                    if keyword in segment_text:
                        segment_risk_score += 10
                        if risk_type not in risk_categories_in_segment:
                            risk_categories_in_segment.append(risk_type)
                        break
            
            # Enhance with market volatility context
            market_enhancement = self._calculate_market_enhancement(segment_text, market_data)
            segment_risk_score += market_enhancement
            
            segment_risks.append({
                "segment_number": i + 1,
                "risk_density": round(risk_density, 1),
                "risk_score": segment_risk_score,
                "risk_categories": risk_categories_in_segment,
                "word_count": total_words,
                "market_enhanced": market_enhancement > 0
            })
        
        # Calculate distribution metrics
        densities = [seg["risk_density"] for seg in segment_risks]
        scores = [seg["risk_score"] for seg in segment_risks]
        
        return {
            "segment_analysis": segment_risks,
            "average_density": round(np.mean(densities), 2) if densities else 0,
            "max_density": round(max(densities), 2) if densities else 0,
            "density_std_dev": round(np.std(densities), 2) if len(densities) > 1 else 0,
            "distribution_type": self._classify_distribution(densities),
            "market_context_applied": bool(market_data.get('volatility_metrics'))
        }
    
    def _calculate_market_enhancement(self, segment_text: str, market_data: Dict) -> float:
        """Calculate risk enhancement based on market volatility"""
        enhancement = 0
        
        # Check if segment mentions volatile companies
        for company, metrics in market_data.get('volatility_metrics', {}).items():
            if company in segment_text:
                volatility = metrics.get('volatility', 0)
                # Higher volatility = higher risk enhancement
                if volatility > 0.3:
                    enhancement += 15
                elif volatility > 0.15:
                    enhancement += 8
        
        return min(enhancement, 25)  # Cap enhancement
    
    def _identify_risk_hotspots(self, segments: List[Dict], risks: List[Dict], market_data: Dict) -> List[Dict[str, Any]]:
        """Identify segments with concentrated risk content with market context"""
        hotspots = []
        
        for i, segment in enumerate(segments):
            segment_text = segment["text"].lower()
            
            # Calculate hotspot score
            hotspot_score = 0
            
            # Risk density component
            risk_word_count = sum(1 for word in segment_text.split() 
                                if any(keyword in word for keyword in self.risk_keywords))
            total_words = len(segment_text.split())
            density = (risk_word_count / total_words * 100) if total_words > 0 else 0
            
            # Risk category diversity
            categories_present = []
            for risk in risks:
                for keyword in risk.get("keywords_found", []):
                    if keyword in segment_text and risk["type"] not in categories_present:
                        categories_present.append(risk["type"])
            
            # Financial impact presence
            financial_terms = ['$', 'million', 'billion', 'fines', 'loss', 'cost']
            financial_present = any(term in segment_text for term in financial_terms)
            
            # Market volatility enhancement
            market_enhancement = self._calculate_market_enhancement(segment_text, market_data)
            
            # Calculate composite score
            hotspot_score = density * 0.6 + len(categories_present) * 20 + (50 if financial_present else 0) + market_enhancement
            
            if hotspot_score > 30:  # Threshold for hotspot
                hotspots.append({
                    "segment_number": i + 1,
                    "hotspot_score": round(hotspot_score, 1),
                    "risk_density": round(density, 1),
                    "risk_categories": categories_present,
                    "financial_impact": financial_present,
                    "market_enhanced": market_enhancement > 0,
                    "segment_preview": segment["text"][:100] + "..." if len(segment["text"]) > 100 else segment["text"]
                })
        
        # Sort by hotspot score
        hotspots.sort(key=lambda x: x["hotspot_score"], reverse=True)
        
        return hotspots[:5]  # Return top 5 hotspots
    
    def _generate_trend_summary(self, distribution: Dict, density_trend: Dict, hotspots: List[Dict], market_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive trend summary with market context"""
        summary = {
            "primary_trend": density_trend["trend"],
            "risk_distribution": distribution["distribution_type"],
            "hotspot_count": len(hotspots),
            "max_risk_density": distribution["max_density"],
            "market_volatility_context": market_data.get("market_context", "unknown"),
            "trend_interpretation": self._interpret_trend(density_trend, distribution, hotspots, market_data)
        }
        
        # Add market data insights
        if market_data.get("companies_analyzed"):
            summary["companies_with_market_data"] = len(market_data["companies_analyzed"])
            summary["data_source"] = market_data.get("data_source", "simulated")
        
        return summary
    
    def _interpret_trend(self, density_trend: Dict, distribution: Dict, hotspots: List[Dict], market_data: Dict) -> str:
        """Generate human-readable trend interpretation with market context"""
        interpretations = []
        
        # Trend interpretation
        if density_trend["trend"] == "increasing":
            interpretations.append("Risk discussion intensifies towards the end of the document.")
        elif density_trend["trend"] == "decreasing":
            interpretations.append("Risk discussion is most prominent in the early sections.")
        else:
            interpretations.append("Risk discussion is relatively consistent throughout.")
        
        # Distribution interpretation
        if distribution["distribution_type"] == "concentrated":
            interpretations.append("Risks are concentrated in specific sections rather than spread evenly.")
        elif distribution["distribution_type"] == "uniform":
            interpretations.append("Risks are evenly distributed across the document.")
        
        # Hotspot interpretation
        if hotspots:
            market_enhanced_hotspots = [h for h in hotspots if h.get("market_enhanced", False)]
            interpretations.append(f"Found {len(hotspots)} risk hotspots ({len(market_enhanced_hotspots)} enhanced by market data).")
        
        # Market context interpretation
        market_context = market_data.get("market_context", "unknown")
        if market_context == "high_volatility":
            interpretations.append("Current market volatility suggests elevated external risk factors.")
        elif market_context == "moderate_volatility":
            interpretations.append("Market conditions show moderate volatility levels.")
        
        return " ".join(interpretations)
    
    def _get_simulated_volatility(self, company: str) -> Dict[str, float]:
        """Fallback simulated volatility data"""
        return {
            'beta': 1.2,
            'volatility': 0.25,
            'pe_ratio': 18.5,
            'market_cap': '150000000000',
            'data_source': 'simulated'
        }

    # KEEP ALL YOUR EXISTING METHODS - they work perfectly!
    def _segment_document(self, text: str, target_segments: int = 10) -> List[Dict[str, Any]]:
        """Segment document into meaningful parts"""
        # Split by paragraphs first
        paragraphs = re.split(r'\n\s*\n', text)
        
        # If not enough paragraphs, split by sentences
        if len(paragraphs) < target_segments:
            sentences = re.split(r'[.!?]+', text)
            # Group sentences into segments
            sentences_per_segment = max(1, len(sentences) // target_segments)
            segments = []
            
            for i in range(0, len(sentences), sentences_per_segment):
                segment_text = ' '.join(sentences[i:i + sentences_per_segment])
                if segment_text.strip():
                    segments.append({
                        "text": segment_text.strip(),
                        "start_position": i,
                        "end_position": i + sentences_per_segment,
                        "type": "sentence_group"
                    })
        else:
            # Use paragraphs as segments
            segments = []
            for i, paragraph in enumerate(paragraphs):
                if paragraph.strip():
                    segments.append({
                        "text": paragraph.strip(),
                        "start_position": i,
                        "end_position": i + 1,
                        "type": "paragraph"
                    })
        
        return segments[:target_segments]  # Limit to target number
    
    def _calculate_density_trend(self, segments: List[Dict]) -> Dict[str, Any]:
        """Calculate risk density trend across segments"""
        densities = []
        
        for segment in segments:
            segment_text = segment["text"].lower()
            risk_word_count = sum(1 for word in segment_text.split() 
                                if any(keyword in word for keyword in self.risk_keywords))
            total_words = len(segment_text.split())
            density = (risk_word_count / total_words * 100) if total_words > 0 else 0
            densities.append(round(density, 2))
        
        if not densities:
            return {"trend": "flat", "slope": 0, "densities": []}
        
        # Calculate trend slope
        x = list(range(len(densities)))
        if len(densities) > 1:
            slope = np.polyfit(x, densities, 1)[0]
        else:
            slope = 0
        
        # Classify trend
        if slope > 0.5:
            trend = "increasing"
        elif slope < -0.5:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "slope": round(slope, 3),
            "densities": densities,
            "peak_density": max(densities) if densities else 0,
            "trough_density": min(densities) if densities else 0
        }
    
    def _analyze_risk_evolution(self, segments: List[Dict]) -> Dict[str, Any]:
        """Analyze how risk discussion evolves through the document"""
        if len(segments) < 3:
            return {"evolution_pattern": "insufficient_data", "phases": []}
        
        evolution_phases = []
        
        # Divide document into thirds
        segment_count = len(segments)
        third = segment_count // 3
        
        phases = [
            {"name": "Introduction", "segments": segments[:third]},
            {"name": "Development", "segments": segments[third:2*third]},
            {"name": "Conclusion", "segments": segments[2*third:]}
        ]
        
        for phase in phases:
            phase_text = " ".join(seg["text"] for seg in phase["segments"])
            phase_text_lower = phase_text.lower()
            
            # Calculate phase metrics
            risk_word_count = sum(1 for word in phase_text_lower.split() 
                                if any(keyword in word for keyword in self.risk_keywords))
            total_words = len(phase_text_lower.split())
            risk_density = (risk_word_count / total_words * 100) if total_words > 0 else 0
            
            # Risk intensity indicators
            intensity_indicators = ['crisis', 'urgent', 'severe', 'critical', 'immediate']
            intensity_score = sum(1 for indicator in intensity_indicators if indicator in phase_text_lower)
            
            evolution_phases.append({
                "phase": phase["name"],
                "risk_density": round(risk_density, 1),
                "intensity_score": intensity_score,
                "segment_count": len(phase["segments"]),
                "primary_focus": self._identify_phase_focus(phase_text)
            })
        
        return {
            "evolution_pattern": self._classify_evolution_pattern(evolution_phases),
            "phases": evolution_phases,
            "most_risky_phase": max(evolution_phases, key=lambda x: x["risk_density"])["phase"] if evolution_phases else "unknown"
        }
    
    def _classify_distribution(self, densities: List[float]) -> str:
        """Classify the distribution pattern of risks"""
        if not densities:
            return "uniform"
        
        avg_density = np.mean(densities)
        std_dev = np.std(densities)
        
        if std_dev < 5:
            return "uniform"
        elif std_dev < 15:
            return "clustered"
        else:
            return "concentrated"
    
    def _identify_phase_focus(self, text: str) -> str:
        """Identify primary focus of a document phase"""
        text_lower = text.lower()
        
        focuses = {
            "regulatory": ["sec", "investigation", "compliance", "regulation"],
            "financial": ["revenue", "profit", "loss", "earnings", "debt"],
            "operational": ["system", "process", "cyber", "breach", "outage"],
            "market": ["volatility", "economic", "recession", "inflation"]
        }
        
        focus_scores = {}
        for focus, keywords in focuses.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            focus_scores[focus] = score
        
        return max(focus_scores, key=focus_scores.get) if any(focus_scores.values()) else "general"
    
    def _classify_evolution_pattern(self, phases: List[Dict]) -> str:
        """Classify the evolution pattern of risk discussion"""
        if len(phases) < 3:
            return "unknown"
        
        densities = [phase["risk_density"] for phase in phases]
        
        if densities[0] < densities[1] < densities[2]:
            return "escalating"
        elif densities[0] > densities[1] > densities[2]:
            return "de-escalating"
        elif densities[1] > densities[0] and densities[1] > densities[2]:
            return "peak_middle"
        elif max(densities) == densities[0]:
            return "front_loaded"
        elif max(densities) == densities[2]:
            return "back_loaded"
        else:
            return "variable"
    
    def _get_empty_trend_analysis(self) -> Dict[str, Any]:
        """Return empty trend analysis structure"""
        return {
            "risk_distribution": {
                "segment_analysis": [],
                "average_density": 0,
                "max_density": 0,
                "density_std_dev": 0,
                "distribution_type": "uniform"
            },
            "density_trend": {
                "trend": "flat",
                "slope": 0,
                "densities": [],
                "peak_density": 0,
                "trough_density": 0
            },
            "risk_hotspots": [],
            "risk_evolution": {
                "evolution_pattern": "unknown",
                "phases": [],
                "most_risky_phase": "unknown"
            },
            "segment_count": 0,
            "trend_summary": {
                "primary_trend": "unknown",
                "risk_distribution": "unknown",
                "hotspot_count": 0,
                "max_risk_density": 0,
                "trend_interpretation": "Insufficient data for trend analysis."
            }
        }