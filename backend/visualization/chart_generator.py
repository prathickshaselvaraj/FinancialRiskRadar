"""
Generate chart data for frontend visualizations
"""
from typing import Dict, List, Any
import json
import re

class ChartDataGenerator:
    def __init__(self):
        self.color_scheme = {
            "credit_risk": "#FF6B6B",
            "market_risk": "#4ECDC4", 
            "operational_risk": "#45B7D1",
            "regulatory_risk": "#96CEB4",
            "companies": "#FFE66D",
            "regulators": "#FF9A8B",
            "financial": "#6A0572"
        }
    
    def generate_risk_dashboard_data(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate complete dashboard data for frontend"""
        dashboard_data = {
            "risk_gauges": self._generate_risk_gauges(analysis_results),
            "category_charts": self._generate_category_charts(analysis_results),
            "entity_visualizations": self._generate_entity_visualizations(analysis_results),
            "trend_charts": self._generate_trend_charts(analysis_results),
            "network_data": self._generate_network_data(analysis_results)
        }
        
        return dashboard_data
    
    def _generate_risk_gauges(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate data for risk gauge charts"""
        risk_scores = analysis_results.get("risk_scores", {})
        
        gauges = {
            "overall_risk": {
                "score": risk_scores.get("overall_risk_score", 0),
                "max_score": 100,
                "ranges": [
                    {"min": 0, "max": 30, "color": "#4CAF50", "label": "Low"},
                    {"min": 30, "max": 70, "color": "#FF9800", "label": "Medium"},
                    {"min": 70, "max": 100, "color": "#F44336", "label": "High"}
                ]
            }
        }
        
        # Add category gauges
        category_scores = risk_scores.get("category_scores", {})
        for risk_type, score in category_scores.items():
            gauges[risk_type] = {
                "score": score,
                "max_score": 100,
                "color": self.color_scheme.get(risk_type, "#666666"),
                "label": risk_type.replace('_', ' ').title()
            }
        
        return gauges
    
    def _generate_category_charts(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate data for risk category charts"""
        risk_scores = analysis_results.get("risk_scores", {})
        category_scores = risk_scores.get("category_scores", {})
        
        # Bar chart data
        bar_chart = {
            "labels": [rt.replace('_', ' ').title() for rt in category_scores.keys()],
            "datasets": [{
                "label": "Risk Scores",
                "data": list(category_scores.values()),
                "backgroundColor": [self.color_scheme.get(rt, "#666666") for rt in category_scores.keys()],
                "borderColor": [self.color_scheme.get(rt, "#666666") for rt in category_scores.keys()],
                "borderWidth": 1
            }]
        }
        
        # Pie chart data
        pie_chart = {
            "labels": [rt.replace('_', ' ').title() for rt in category_scores.keys()],
            "datasets": [{
                "data": list(category_scores.values()),
                "backgroundColor": [self.color_scheme.get(rt, "#666666") for rt in category_scores.keys()],
                "borderColor": "#ffffff",
                "borderWidth": 2
            }]
        }
        
        return {
            "bar_chart": bar_chart,
            "pie_chart": pie_chart,
            "summary": {
                "highest_risk": max(category_scores, key=category_scores.get) if category_scores else "none",
                "lowest_risk": min(category_scores, key=category_scores.get) if category_scores else "none",
                "average_score": sum(category_scores.values()) / len(category_scores) if category_scores else 0
            }
        }
    
    def _generate_entity_visualizations(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate data for entity visualizations"""
        entities = analysis_results.get("entities", {})
        
        # Company bar chart
        companies = entities.get("companies", [])
        company_chart = {
            "labels": companies[:10],  # Top 10 companies
            "datasets": [{
                "label": "Mentions",
                "data": [1] * len(companies[:10]),  # Placeholder - would need actual counts
                "backgroundColor": self.color_scheme["companies"]
            }]
        }
        
        # Financial amounts
        amounts = entities.get("financial_amounts", [])
        amount_chart = {
            "labels": [amt[:20] + "..." if len(amt) > 20 else amt for amt in amounts[:8]],
            "datasets": [{
                "label": "Financial Impact",
                "data": [self._extract_numeric_value(amt) for amt in amounts[:8]],
                "backgroundColor": self.color_scheme["financial"]
            }]
        }
        
        return {
            "company_chart": company_chart,
            "financial_chart": amount_chart,
            "entity_counts": {
                "companies": len(companies),
                "regulatory_bodies": len(entities.get("regulatory_bodies", [])),
                "financial_amounts": len(amounts),
                "dates": len(entities.get("dates", [])),
                "people": len(entities.get("people", []))
            }
        }
    
    def _generate_trend_charts(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate data for trend analysis charts"""
        trend_analysis = analysis_results.get("trend_analysis", {})
        density_trend = trend_analysis.get("density_trend", {})
        
        # Risk density trend line chart
        trend_chart = {
            "labels": [f"Sec {i+1}" for i in range(len(density_trend.get("densities", [])))],
            "datasets": [{
                "label": "Risk Density",
                "data": density_trend.get("densities", []),
                "borderColor": "#FF6B6B",
                "backgroundColor": "rgba(255, 107, 107, 0.1)",
                "fill": True,
                "tension": 0.4
            }]
        }
        
        # Risk distribution by segment
        distribution = trend_analysis.get("risk_distribution", {})
        segment_analysis = distribution.get("segment_analysis", [])
        
        distribution_chart = {
            "labels": [f"Seg {seg['segment_number']}" for seg in segment_analysis],
            "datasets": [{
                "label": "Risk Density",
                "data": [seg.get("risk_density", 0) for seg in segment_analysis],
                "backgroundColor": "#4ECDC4"
            }]
        }
        
        return {
            "trend_chart": trend_chart,
            "distribution_chart": distribution_chart,
            "trend_metrics": {
                "trend_direction": density_trend.get("trend", "stable"),
                "peak_density": density_trend.get("peak_density", 0),
                "average_density": distribution.get("average_density", 0)
            }
        }
    
    def _generate_network_data(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate data for network visualization"""
        relationships = analysis_results.get("relationships", {})
        risk_network = relationships.get("risk_networks", {})
        
        return {
            "nodes": risk_network.get("nodes", []),
            "links": risk_network.get("links", []),
            "network_metrics": {
                "total_nodes": len(risk_network.get("nodes", [])),
                "total_connections": risk_network.get("total_connections", 0),
                "network_density": risk_network.get("network_density", 0)
            }
        }
    
    def _extract_numeric_value(self, amount_str: str) -> float:
        """Extract numeric value from financial amount string"""
        try:
            # Remove $ and commas, extract number
            clean_str = amount_str.replace('$', '').replace(',', '')
            numeric_match = re.search(r'(\d+(?:\.\d+)?)', clean_str)
            if numeric_match:
                value = float(numeric_match.group(1))
                
                # Apply multipliers
                if 'billion' in amount_str.lower():
                    return value * 1000  # Convert to millions
                elif 'million' in amount_str.lower():
                    return value
                else:
                    return value / 1000000  # Assume dollars, convert to millions
            return 0
        except:
            return 0
    
    def generate_export_data(self, analysis_results: Dict, format: str = "json") -> str:
        """Generate data for export in various formats"""
        export_data = {
            "analysis_timestamp": analysis_results.get("timestamp", ""),
            "document_info": analysis_results.get("document_info", {}),
            "risk_analysis": analysis_results.get("risk_scores", {}),
            "entities": analysis_results.get("entities", {}),
            "trends": analysis_results.get("trend_analysis", {}),
            "relationships": analysis_results.get("relationships", {}),
            "visualization_data": self.generate_risk_dashboard_data(analysis_results)
        }
        
        if format == "json":
            return json.dumps(export_data, indent=2)
        else:
            # For other formats, return JSON as fallback
            return json.dumps(export_data, indent=2)