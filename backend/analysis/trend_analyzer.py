"""
Risk trend and pattern analysis across document sections
"""
import re
from typing import Dict, List, Any
import numpy as np

class RiskTrendAnalyzer:
    def __init__(self):
        self.risk_keywords = [
            'risk', 'uncertainty', 'volatility', 'default', 'investigation',
            'compliance', 'breach', 'failure', 'lawsuit', 'fines'
        ]
    
    def analyze_risk_trends(self, text: str, risks: List[Dict]) -> Dict[str, Any]:
        """Analyze risk distribution and trends throughout the document"""
        if not text or not risks:
            return self._get_empty_trend_analysis()
        
        # Segment document
        segments = self._segment_document(text)
        
        # Analyze risk distribution
        distribution = self._analyze_risk_distribution(segments, risks)
        
        # Calculate risk density trends
        density_trend = self._calculate_density_trend(segments)
        
        # Identify risk hotspots
        hotspots = self._identify_risk_hotspots(segments, risks)
        
        # Analyze risk evolution
        evolution = self._analyze_risk_evolution(segments)
        
        return {
            "risk_distribution": distribution,
            "density_trend": density_trend,
            "risk_hotspots": hotspots,
            "risk_evolution": evolution,
            "segment_count": len(segments),
            "trend_summary": self._generate_trend_summary(distribution, density_trend, hotspots)
        }
    
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
    
    def _analyze_risk_distribution(self, segments: List[Dict], risks: List[Dict]) -> Dict[str, Any]:
        """Analyze how risks are distributed across document segments"""
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
            
            segment_risks.append({
                "segment_number": i + 1,
                "risk_density": round(risk_density, 1),
                "risk_score": segment_risk_score,
                "risk_categories": risk_categories_in_segment,
                "word_count": total_words
            })
        
        # Calculate distribution metrics
        densities = [seg["risk_density"] for seg in segment_risks]
        scores = [seg["risk_score"] for seg in segment_risks]
        
        return {
            "segment_analysis": segment_risks,
            "average_density": round(np.mean(densities), 2) if densities else 0,
            "max_density": round(max(densities), 2) if densities else 0,
            "density_std_dev": round(np.std(densities), 2) if len(densities) > 1 else 0,
            "distribution_type": self._classify_distribution(densities)
        }
    
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
    
    def _identify_risk_hotspots(self, segments: List[Dict], risks: List[Dict]) -> List[Dict[str, Any]]:
        """Identify segments with concentrated risk content"""
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
            
            # Calculate composite score
            hotspot_score = density * 0.6 + len(categories_present) * 20 + (50 if financial_present else 0)
            
            if hotspot_score > 30:  # Threshold for hotspot
                hotspots.append({
                    "segment_number": i + 1,
                    "hotspot_score": round(hotspot_score, 1),
                    "risk_density": round(density, 1),
                    "risk_categories": categories_present,
                    "financial_impact": financial_present,
                    "segment_preview": segment["text"][:100] + "..." if len(segment["text"]) > 100 else segment["text"]
                })
        
        # Sort by hotspot score
        hotspots.sort(key=lambda x: x["hotspot_score"], reverse=True)
        
        return hotspots[:5]  # Return top 5 hotspots
    
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
    
    def _generate_trend_summary(self, distribution: Dict, density_trend: Dict, hotspots: List[Dict]) -> Dict[str, Any]:
        """Generate comprehensive trend summary"""
        return {
            "primary_trend": density_trend["trend"],
            "risk_distribution": distribution["distribution_type"],
            "hotspot_count": len(hotspots),
            "max_risk_density": distribution["max_density"],
            "trend_interpretation": self._interpret_trend(density_trend, distribution, hotspots)
        }
    
    def _interpret_trend(self, density_trend: Dict, distribution: Dict, hotspots: List[Dict]) -> str:
        """Generate human-readable trend interpretation"""
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
            interpretations.append(f"Found {len(hotspots)} sections with particularly high risk concentration.")
        
        return " ".join(interpretations)
    
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