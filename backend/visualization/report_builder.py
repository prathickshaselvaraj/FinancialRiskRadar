"""
Generate comprehensive analysis reports and summaries
"""
from typing import Dict, List, Any
from datetime import datetime
import json
import re

class ReportBuilder:
    def __init__(self):
        self.risk_levels = {
            "critical": (80, 100, "🔴", "Immediate attention required"),
            "high": (60, 79, "🟠", "Urgent review needed"), 
            "moderate": (40, 59, "🟡", "Monitor closely"),
            "low": (20, 39, "🟢", "Standard monitoring"),
            "minimal": (0, 19, "⚪", "Routine oversight")
        }
    
    def generate_comprehensive_report(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        report = {
            "metadata": self._generate_report_metadata(),
            "executive_summary": self._generate_executive_summary(analysis_results),
            "risk_analysis": self._generate_risk_analysis_section(analysis_results),
            "entity_analysis": self._generate_entity_analysis_section(analysis_results),
            "trend_analysis": self._generate_trend_analysis_section(analysis_results),
            "relationship_analysis": self._generate_relationship_analysis_section(analysis_results),
            "recommendations": self._generate_recommendations(analysis_results),
            "technical_details": self._generate_technical_details(analysis_results)
        }
        
        return report
    
    def _generate_report_metadata(self) -> Dict[str, Any]:
        """Generate report metadata"""
        return {
            "report_id": f"FRR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "analysis_tool": "FinancialRiskRadar NLP Engine",
            "report_version": "1.0",
            "confidence_level": "High"
        }
    
    def _generate_executive_summary(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate executive summary section"""
        risk_scores = analysis_results.get("risk_scores", {})
        overall_score = risk_scores.get("overall_risk_score", 0)
        
        # Determine risk level
        risk_level = "minimal"
        for level, (min_score, max_score, icon, description) in self.risk_levels.items():
            if min_score <= overall_score <= max_score:
                risk_level = level
                break
        
        return {
            "overall_risk_score": overall_score,
            "risk_level": risk_level,
            "risk_icon": self.risk_levels[risk_level][2],
            "risk_description": self.risk_levels[risk_level][3],
            "key_findings": self._extract_key_findings(analysis_results),
            "primary_concerns": self._identify_primary_concerns(analysis_results),
            "summary_text": self._generate_summary_text(analysis_results, risk_level)
        }
    
    def _generate_risk_analysis_section(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate detailed risk analysis section"""
        risk_scores = analysis_results.get("risk_scores", {})
        category_scores = risk_scores.get("category_scores", {})
        risk_breakdown = risk_scores.get("risk_breakdown", {})
        
        risk_analysis = {
            "overall_assessment": {
                "score": risk_scores.get("overall_risk_score", 0),
                "confidence": risk_scores.get("risk_summary", {}).get("confidence_score", 0),
                "interpretation": self._interpret_risk_score(risk_scores.get("overall_risk_score", 0))
            },
            "category_breakdown": [],
            "intensity_analysis": risk_breakdown.get("intensity_modifiers", {}),
            "temporal_analysis": risk_breakdown.get("temporal_factors", {}),
            "financial_impact": risk_breakdown.get("financial_impact", {})
        }
        
        # Add category details
        for risk_type, score in category_scores.items():
            risk_analysis["category_breakdown"].append({
                "category": risk_type.replace('_', ' ').title(),
                "score": score,
                "level": self._get_risk_level(score),
                "weight": self._get_risk_weight(risk_type),
                "key_indicators": self._get_risk_indicators(risk_type, analysis_results)
            })
        
        return risk_analysis
    
    def _generate_entity_analysis_section(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate entity analysis section"""
        entities = analysis_results.get("entities", {})
        relationships = analysis_results.get("relationships", {})
        
        entity_analysis = {
            "companies_identified": {
                "count": len(entities.get("companies", [])),
                "primary_companies": entities.get("companies", [])[:5],
                "exposure_analysis": self._analyze_company_exposure(relationships)
            },
            "regulatory_landscape": {
                "bodies_identified": entities.get("regulatory_bodies", []),
                "regulatory_actions": self._analyze_regulatory_actions(relationships)
            },
            "financial_impact": {
                "amounts_identified": entities.get("financial_amounts", [])[:10],
                "total_estimated_impact": self._calculate_total_financial_impact(entities),
                "impact_distribution": self._analyze_impact_distribution(entities)
            },
            "temporal_analysis": {
                "time_references": entities.get("dates", []),
                "urgency_indications": self._analyze_temporal_urgency(entities, analysis_results)
            }
        }
        
        return entity_analysis
    
    def _generate_trend_analysis_section(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate trend analysis section"""
        trend_analysis = analysis_results.get("trend_analysis", {})
        
        return {
            "risk_distribution": {
                "pattern": trend_analysis.get("risk_distribution", {}).get("distribution_type", "unknown"),
                "density_metrics": {
                    "average": trend_analysis.get("risk_distribution", {}).get("average_density", 0),
                    "maximum": trend_analysis.get("risk_distribution", {}).get("max_density", 0),
                    "variability": trend_analysis.get("risk_distribution", {}).get("density_std_dev", 0)
                }
            },
            "temporal_trends": {
                "direction": trend_analysis.get("density_trend", {}).get("trend", "stable"),
                "evolution_pattern": trend_analysis.get("risk_evolution", {}).get("evolution_pattern", "unknown"),
                "hotspots_identified": len(trend_analysis.get("risk_hotspots", []))
            },
            "segment_analysis": {
                "total_segments": trend_analysis.get("segment_count", 0),
                "risk_concentration": self._analyze_risk_concentration(trend_analysis)
            }
        }
    
    def _generate_relationship_analysis_section(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate relationship analysis section"""
        relationships = analysis_results.get("relationships", {})
        relationship_summary = relationships.get("relationship_summary", {})
        
        return {
            "network_complexity": {
                "total_entities": relationship_summary.get("total_entities_mapped", 0),
                "connection_density": relationship_summary.get("relationship_complexity", {}).get("network_density", 0),
                "complexity_level": relationship_summary.get("relationship_complexity", {}).get("complexity_level", "low")
            },
            "key_relationships": {
                "company_risk_exposure": relationship_summary.get("company_risk_exposure", {}),
                "regulatory_oversight": relationship_summary.get("regulatory_landscape", {}),
                "financial_networks": relationship_summary.get("financial_impact_analysis", {})
            },
            "risk_propagation": self._analyze_risk_propagation(relationships)
        }
    
    def _generate_recommendations(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []
        risk_scores = analysis_results.get("risk_scores", {})
        overall_score = risk_scores.get("overall_risk_score", 0)
        
        # Risk-level based recommendations
        if overall_score >= 80:
            recommendations.extend([
                {
                    "priority": "critical",
                    "category": "Immediate Action",
                    "recommendation": "Convene emergency risk committee meeting within 24 hours",
                    "rationale": "Critical risk level requires immediate executive attention",
                    "timeline": "24 hours"
                },
                {
                    "priority": "high", 
                    "category": "Financial Controls",
                    "recommendation": "Implement enhanced financial monitoring and controls",
                    "rationale": "Significant financial exposure identified",
                    "timeline": "48 hours"
                }
            ])
        elif overall_score >= 60:
            recommendations.extend([
                {
                    "priority": "high",
                    "category": "Risk Assessment",
                    "recommendation": "Conduct detailed risk assessment of identified exposure areas",
                    "rationale": "High risk concentration in specific categories",
                    "timeline": "1 week"
                }
            ])
        
        # Category-specific recommendations
        category_scores = risk_scores.get("category_scores", {})
        for risk_type, score in category_scores.items():
            if score > 70:
                rec = self._get_category_recommendation(risk_type, score)
                if rec:
                    recommendations.append(rec)
        
        # Relationship-based recommendations
        relationships = analysis_results.get("relationships", {})
        rel_summary = relationships.get("relationship_summary", {})
        if rel_summary.get("company_risk_exposure", {}).get("high_exposure_companies", 0) > 0:
            recommendations.append({
                "priority": "medium",
                "category": "Portfolio Analysis",
                "recommendation": "Review exposure to high-risk companies in investment portfolio",
                "rationale": "Multiple companies show significant risk exposure",
                "timeline": "2 weeks"
            })
        
        return recommendations
    
    def _generate_technical_details(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate technical analysis details"""
        return {
            "analysis_parameters": {
                "nlp_engine": "FinancialRiskRadar Advanced NLP",
                "risk_categories_analyzed": 4,
                "entity_types_extracted": 6,
                "relationship_patterns_matched": len(analysis_results.get("relationships", {}).get("explicit_relationships", [])),
                "confidence_scoring": "Multi-factor weighted analysis"
            },
            "processing_metrics": {
                "document_type": analysis_results.get("document_info", {}).get("document_type", "unknown"),
                "word_count": analysis_results.get("document_info", {}).get("word_count", 0),
                "analysis_duration": "Real-time",  # This would be actual timing in production
                "data_points_analyzed": self._calculate_data_points(analysis_results)
            },
            "methodology": {
                "risk_detection": "Contextual keyword analysis with intensity scoring",
                "entity_extraction": "Pattern-based financial entity recognition", 
                "relationship_mapping": "Co-occurrence and semantic pattern analysis",
                "trend_analysis": "Segmental risk density and distribution analysis"
            }
        }
    
    def _extract_key_findings(self, analysis_results: Dict) -> List[str]:
        """Extract key findings from analysis"""
        findings = []
        risk_scores = analysis_results.get("risk_scores", {})
        
        overall_score = risk_scores.get("overall_risk_score", 0)
        findings.append(f"Overall risk score: {overall_score}/100 ({self._get_risk_level(overall_score).title()} risk level)")
        
        # Highest risk category
        category_scores = risk_scores.get("category_scores", {})
        if category_scores:
            highest_risk = max(category_scores, key=category_scores.get)
            findings.append(f"Primary risk category: {highest_risk.replace('_', ' ').title()} ({category_scores[highest_risk]}/100)")
        
        # Entity findings
        entities = analysis_results.get("entities", {})
        if entities.get("companies"):
            findings.append(f"Identified {len(entities['companies'])} companies in analysis")
        
        # Relationship findings
        relationships = analysis_results.get("relationships", {})
        rel_summary = relationships.get("relationship_summary", {})
        if rel_summary.get("company_risk_exposure", {}).get("high_exposure_companies", 0) > 0:
            findings.append(f"{rel_summary['company_risk_exposure']['high_exposure_companies']} companies with high risk exposure")
        
        return findings
    
    def _identify_primary_concerns(self, analysis_results: Dict) -> List[str]:
        """Identify primary concerns from analysis"""
        concerns = []
        risk_scores = analysis_results.get("risk_scores", {})
        category_scores = risk_scores.get("category_scores", {})
        
        # High scoring risk categories
        for risk_type, score in category_scores.items():
            if score > 70:
                concerns.append(f"Elevated {risk_type.replace('_', ' ')} risk (Score: {score}/100)")
        
        # Financial impact concerns
        financial_impact = risk_scores.get("risk_breakdown", {}).get("financial_impact", {})
        if financial_impact.get("impact_score", 0) > 50:
            concerns.append(f"Significant financial impact potential (${financial_impact.get('total_impact_millions', 0)}M estimated)")
        
        # Regulatory concerns
        entities = analysis_results.get("entities", {})
        if entities.get("regulatory_bodies"):
            concerns.append(f"Multiple regulatory bodies involved ({len(entities['regulatory_bodies'])})")
        
        return concerns
    
    # Helper methods for the report generation...
    def _generate_summary_text(self, analysis_results: Dict, risk_level: str) -> str:
        """Generate human-readable summary text"""
        risk_scores = analysis_results.get("risk_scores", {})
        overall_score = risk_scores.get("overall_risk_score", 0)
        
        summary = f"This analysis identifies {risk_level} level financial risks (Score: {overall_score}/100). "
        
        # Add category information
        category_scores = risk_scores.get("category_scores", {})
        if category_scores:
            high_categories = [cat for cat, score in category_scores.items() if score > 60]
            if high_categories:
                summary += f"Primary risk areas include {', '.join([c.replace('_', ' ').title() for c in high_categories])}. "
        
        # Add entity information
        entities = analysis_results.get("entities", {})
        if entities.get("companies"):
            summary += f"Analysis covers {len(entities['companies'])} companies. "
        
        summary += "Detailed recommendations are provided for risk mitigation."
        
        return summary
    
    def _interpret_risk_score(self, score: float) -> str:
        """Interpret risk score for reporting"""
        if score >= 80:
            return "Critical risk level requiring immediate executive attention and comprehensive mitigation strategies."
        elif score >= 60:
            return "High risk level indicating significant exposure that warrants urgent review and action planning."
        elif score >= 40:
            return "Moderate risk level suggesting careful monitoring and proactive management measures."
        elif score >= 20:
            return "Low risk level appropriate for standard oversight and periodic review."
        else:
            return "Minimal risk level with no immediate concerns identified."
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level from score"""
        for level, (min_score, max_score, _, _) in self.risk_levels.items():
            if min_score <= score <= max_score:
                return level
        return "minimal"
    
    def _get_risk_weight(self, risk_type: str) -> float:
        """Get risk weight for reporting"""
        weights = {
            "credit_risk": 0.35,
            "market_risk": 0.25, 
            "operational_risk": 0.20,
            "regulatory_risk": 0.20
        }
        return weights.get(risk_type, 0.25)
    
    def _get_risk_indicators(self, risk_type: str, analysis_results: Dict) -> List[str]:
        """Get key risk indicators for a category"""
        risk_scores = analysis_results.get("risk_scores", {})
        risks = risk_scores.get("risk_breakdown", {}).get("base_scores", {})
        
        if risk_type in risks:
            return [f"Base score: {risks[risk_type]}", "Contextual intensity factors applied"]
        return ["Standard risk assessment applied"]
    
    def _analyze_company_exposure(self, relationships: Dict) -> Dict[str, Any]:
        """Analyze company risk exposure"""
        company_rels = relationships.get("company_relationships", [])
        if not company_rels:
            return {"analysis": "No company exposure data available"}
        
        high_exposure = [cr for cr in company_rels if cr.get("total_risk_exposure", 0) > 60]
        return {
            "companies_analyzed": len(company_rels),
            "high_exposure_count": len(high_exposure),
            "exposure_distribution": "concentrated" if len(high_exposure) > 0 else "dispersed"
        }
    
    def _analyze_regulatory_actions(self, relationships: Dict) -> Dict[str, Any]:
        """Analyze regulatory actions"""
        regulatory_rels = relationships.get("regulatory_relationships", [])
        if not regulatory_rels:
            return {"analysis": "No regulatory action data available"}
        
        action_types = {}
        for rel in regulatory_rels:
            for action in rel.get("actions", []):
                action_type = action.get("relationship_type", "monitoring")
                action_types[action_type] = action_types.get(action_type, 0) + 1
        
        return {
            "regulatory_bodies": len(regulatory_rels),
            "primary_action_type": max(action_types, key=action_types.get) if action_types else "monitoring",
            "action_distribution": action_types
        }
    
    def _calculate_total_financial_impact(self, entities: Dict) -> float:
        """Calculate total financial impact"""
        amounts = entities.get("financial_amounts", [])
        total = 0
        
        for amount in amounts:
            # Simple extraction - in production this would be more sophisticated
            numeric_match = re.search(r'(\d+(?:\.\d+)?)', amount.replace(',', '').replace('$', ''))
            if numeric_match:
                value = float(numeric_match.group(1))
                if 'billion' in amount.lower():
                    value *= 1000
                elif 'million' not in amount.lower():
                    value /= 1000000
                total += value
        
        return round(total, 2)
    
    def _analyze_impact_distribution(self, entities: Dict) -> Dict[str, int]:
        """Analyze financial impact distribution"""
        amounts = entities.get("financial_amounts", [])
        distribution = {"billion_plus": 0, "million_range": 0, "thousand_range": 0}
        
        for amount in amounts:
            if 'billion' in amount.lower():
                distribution["billion_plus"] += 1
            elif 'million' in amount.lower():
                distribution["million_range"] += 1
            else:
                distribution["thousand_range"] += 1
        
        return distribution
    
    def _analyze_temporal_urgency(self, entities: Dict, analysis_results: Dict) -> Dict[str, Any]:
        """Analyze temporal urgency indicators"""
        dates = entities.get("dates", [])
        risk_scores = analysis_results.get("risk_scores", {})
        temporal_factors = risk_scores.get("risk_breakdown", {}).get("temporal_factors", {})
        
        return {
            "time_references": len(dates),
            "urgency_score": temporal_factors.get("overall_urgency", 0),
            "primary_timeframe": temporal_factors.get("primary_timeframe", "unknown")
        }
    
    def _analyze_risk_concentration(self, trend_analysis: Dict) -> Dict[str, Any]:
        """Analyze risk concentration patterns"""
        hotspots = trend_analysis.get("risk_hotspots", [])
        distribution = trend_analysis.get("risk_distribution", {})
        
        return {
            "hotspot_count": len(hotspots),
            "distribution_type": distribution.get("distribution_type", "unknown"),
            "concentration_level": "high" if len(hotspots) > 2 else "medium" if len(hotspots) > 0 else "low"
        }
    
    def _analyze_risk_propagation(self, relationships: Dict) -> Dict[str, Any]:
        """Analyze risk propagation patterns"""
        network = relationships.get("risk_networks", {})
        return {
            "network_density": network.get("network_density", 0),
            "interconnection_level": "high" if network.get("network_density", 0) > 0.1 else "medium",
            "risk_clusters": self._identify_risk_clusters(network)
        }
    
    def _identify_risk_clusters(self, network: Dict) -> List[str]:
        """Identify risk clusters in network"""
        # Simplified cluster identification
        nodes = network.get("nodes", [])
        risk_nodes = [node for node in nodes if node.get("type") == "risk"]
        
        clusters = []
        if len(risk_nodes) >= 3:
            clusters.append("Multiple risk categories interconnected")
        if any(node.get("score", 0) > 70 for node in risk_nodes):
            clusters.append("High-risk category cluster")
        
        return clusters if clusters else ["Distributed risk profile"]
    
    def _get_category_recommendation(self, risk_type: str, score: float) -> Dict[str, Any]:
        """Get category-specific recommendation"""
        recommendations = {
            "credit_risk": {
                "priority": "high",
                "category": "Credit Risk Management",
                "recommendation": "Enhance credit monitoring and debt sustainability analysis",
                "rationale": f"Elevated credit risk identified (Score: {score}/100)",
                "timeline": "2 weeks"
            },
            "market_risk": {
                "priority": "medium", 
                "category": "Market Risk Assessment",
                "recommendation": "Review hedging strategies and market exposure limits",
                "rationale": f"Significant market risk exposure (Score: {score}/100)",
                "timeline": "3 weeks"
            },
            "operational_risk": {
                "priority": "high",
                "category": "Operational Controls",
                "recommendation": "Conduct operational resilience review and control testing",
                "rationale": f"High operational risk level (Score: {score}/100)", 
                "timeline": "1 week"
            },
            "regulatory_risk": {
                "priority": "high",
                "category": "Compliance Management",
                "recommendation": "Strengthen compliance monitoring and regulatory engagement",
                "rationale": f"Elevated regulatory risk (Score: {score}/100)",
                "timeline": "1 week"
            }
        }
        
        return recommendations.get(risk_type)
    
    def _calculate_data_points(self, analysis_results: Dict) -> int:
        """Calculate total data points analyzed"""
        entities = analysis_results.get("entities", {})
        risk_scores = analysis_results.get("risk_scores", {})
        relationships = analysis_results.get("relationships", {})
        
        entity_count = sum(len(entity_list) for entity_list in entities.values())
        risk_count = len(risk_scores.get("category_scores", {}))
        relationship_count = len(relationships.get("explicit_relationships", []))
        
        return entity_count + risk_count + relationship_count + 100  # Base analysis points