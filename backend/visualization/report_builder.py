"""
Generate comprehensive analysis reports and summaries with enhanced APIs
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass
import logging
from pathlib import Path
import asyncio
import aiofiles
import pandas as pd
from jinja2 import Template
import markdown

@dataclass
class ReportConfig:
    """Configuration for report generation"""
    include_executive_summary: bool = True
    include_technical_details: bool = True
    risk_threshold_high: float = 70.0
    risk_threshold_medium: float = 40.0
    max_recommendations: int = 10
    report_language: str = "en"
    compliance_framework: str = "SOX"

class ReportBuilder:
    def __init__(self, config: ReportConfig = None):
        self.config = config or ReportConfig()
        
        self.risk_levels = {
            "critical": (80, 100, "🔴", "Immediate attention required", "#DC2626"),
            "high": (60, 79, "🟠", "Urgent review needed", "#EA580C"), 
            "moderate": (40, 59, "🟡", "Monitor closely", "#CA8A04"),
            "low": (20, 39, "🟢", "Standard monitoring", "#16A34A"),
            "minimal": (0, 19, "⚪", "Routine oversight", "#4B5563")
        }
        
        self.compliance_frameworks = {
            "SOX": {
                "name": "Sarbanes-Oxley Act",
                "sections": ["302", "404", "409"],
                "risk_categories": ["financial_reporting", "internal_controls", "disclosure"]
            },
            "GDPR": {
                "name": "General Data Protection Regulation",
                "sections": ["Article 5", "Article 32", "Article 33"],
                "risk_categories": ["data_privacy", "data_security", "breach_notification"]
            },
            "BASEL": {
                "name": "Basel III Framework",
                "sections": ["Pillar 1", "Pillar 2", "Pillar 3"],
                "risk_categories": ["credit_risk", "market_risk", "operational_risk"]
            }
        }
        
        self.notification_apis = {
            "email": {"enabled": False, "smtp_server": None},
            "slack": {"enabled": False, "webhook_url": None},
            "teams": {"enabled": False, "webhook_url": None}
        }
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_comprehensive_report(self, analysis_results: Dict, format: str = "json") -> Dict[str, Any]:
        """Generate comprehensive analysis report in multiple formats"""
        base_report = self._generate_base_report(analysis_results)
        
        format_handlers = {
            "json": self._format_json_report,
            "html": self._format_html_report,
            "markdown": self._format_markdown_report,
            "executive": self._format_executive_summary,
            "compliance": self._format_compliance_report
        }
        
        handler = format_handlers.get(format, self._format_json_report)
        return handler(base_report, analysis_results)

    def _generate_base_report(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate base report structure"""
        return {
            "metadata": self._generate_report_metadata(),
            "executive_summary": self._generate_executive_summary(analysis_results),
            "risk_analysis": self._generate_risk_analysis_section(analysis_results),
            "entity_analysis": self._generate_entity_analysis_section(analysis_results),
            "trend_analysis": self._generate_trend_analysis_section(analysis_results),
            "relationship_analysis": self._generate_relationship_analysis_section(analysis_results),
            "compliance_analysis": self._generate_compliance_analysis(analysis_results),
            "sentiment_analysis": self._generate_sentiment_analysis(analysis_results),
            "recommendations": self._generate_recommendations(analysis_results),
            "action_plan": self._generate_action_plan(analysis_results),
            "technical_details": self._generate_technical_details(analysis_results)
        }

    def _generate_report_metadata(self) -> Dict[str, Any]:
        """Generate enhanced report metadata with audit trail"""
        return {
            "report_id": f"FRR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "analysis_tool": "FinancialRiskRadar NLP Engine v2.0",
            "report_version": "2.1",
            "confidence_level": "High",
            "compliance_framework": self.config.compliance_framework,
            "data_sources": ["SEC Filings", "Financial News", "Regulatory Updates"],
            "audit_trail": {
                "created_by": "AI Risk Analysis System",
                "reviewed_by": "Compliance Officer",
                "approval_status": "pending",
                "version_history": ["1.0 - Initial Analysis", "2.0 - Enhanced Risk Scoring"]
            }
        }

    def _generate_executive_summary(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate enhanced executive summary section"""
        risk_scores = analysis_results.get("risk_scores", {})
        overall_score = risk_scores.get("overall_risk_score", 0)
        
        risk_level = self._get_risk_level(overall_score)
        risk_info = self.risk_levels[risk_level]
        
        return {
            "overall_risk_score": overall_score,
            "risk_level": risk_level,
            "risk_icon": risk_info[2],
            "risk_color": risk_info[4],
            "risk_description": risk_info[3],
            "key_findings": self._extract_key_findings(analysis_results),
            "primary_concerns": self._identify_primary_concerns(analysis_results),
            "financial_impact": self._calculate_financial_impact_summary(analysis_results),
            "regulatory_exposure": self._calculate_regulatory_exposure(analysis_results),
            "summary_text": self._generate_summary_text(analysis_results, risk_level),
            "urgency_level": self._calculate_urgency_level(analysis_results)
        }

    def _generate_risk_analysis_section(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate detailed risk analysis section with compliance mapping"""
        risk_scores = analysis_results.get("risk_scores", {})
        category_scores = risk_scores.get("category_scores", {})
        risk_breakdown = risk_scores.get("risk_breakdown", {})
        
        risk_analysis = {
            "overall_assessment": {
                "score": risk_scores.get("overall_risk_score", 0),
                "confidence": risk_scores.get("confidence_score", 85),
                "interpretation": self._interpret_risk_score(risk_scores.get("overall_risk_score", 0)),
                "trend": risk_scores.get("trend_direction", "stable"),
                "peer_comparison": self._generate_peer_comparison(analysis_results)
            },
            "category_breakdown": [],
            "compliance_mapping": self._map_risks_to_compliance(analysis_results),
            "intensity_analysis": risk_breakdown.get("intensity_modifiers", {}),
            "temporal_analysis": risk_breakdown.get("temporal_factors", {}),
            "financial_impact": risk_breakdown.get("financial_impact", {}),
            "risk_heatmap": self._generate_risk_heatmap(analysis_results)
        }
        
        for risk_type, score in category_scores.items():
            risk_analysis["category_breakdown"].append({
                "category": risk_type.replace('_', ' ').title(),
                "score": score,
                "level": self._get_risk_level(score),
                "weight": self._get_risk_weight(risk_type),
                "key_indicators": self._get_risk_indicators(risk_type, analysis_results),
                "mitigation_status": self._get_mitigation_status(risk_type, score),
                "compliance_requirements": self._get_compliance_requirements(risk_type)
            })
        
        return risk_analysis

    def _generate_entity_analysis_section(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate enhanced entity analysis section"""
        entities = analysis_results.get("entities", {})
        relationships = analysis_results.get("relationships", {})
        
        return {
            "companies_identified": {
                "count": len(entities.get("companies", [])),
                "primary_companies": entities.get("companies", [])[:10],
                "exposure_analysis": self._analyze_company_exposure(relationships),
                "concentration_risk": self._analyze_concentration_risk(entities)
            },
            "regulatory_landscape": {
                "bodies_identified": entities.get("regulatory_bodies", []),
                "regulatory_actions": self._analyze_regulatory_actions(relationships),
                "jurisdictional_analysis": self._analyze_jurisdictions(entities)
            },
            "financial_impact": {
                "amounts_identified": entities.get("financial_amounts", [])[:15],
                "total_estimated_impact": self._calculate_total_financial_impact(entities),
                "impact_distribution": self._analyze_impact_distribution(entities),
                "sensitivity_analysis": self._perform_sensitivity_analysis(entities)
            },
            "stakeholder_analysis": {
                "key_stakeholders": self._identify_key_stakeholders(entities),
                "stakeholder_concerns": self._analyze_stakeholder_concerns(analysis_results),
                "communication_plan": self._generate_communication_plan(entities)
            }
        }

    def _generate_trend_analysis_section(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate enhanced trend analysis section"""
        trend_analysis = analysis_results.get("trend_analysis", {})
        
        return {
            "risk_distribution": {
                "pattern": trend_analysis.get("risk_distribution", {}).get("distribution_type", "unknown"),
                "density_metrics": {
                    "average": trend_analysis.get("risk_distribution", {}).get("average_density", 0),
                    "maximum": trend_analysis.get("risk_distribution", {}).get("max_density", 0),
                    "variability": trend_analysis.get("risk_distribution", {}).get("density_std_dev", 0),
                    "skewness": trend_analysis.get("risk_distribution", {}).get("skewness", 0)
                }
            },
            "temporal_trends": {
                "direction": trend_analysis.get("density_trend", {}).get("trend", "stable"),
                "evolution_pattern": trend_analysis.get("risk_evolution", {}).get("evolution_pattern", "unknown"),
                "hotspots_identified": len(trend_analysis.get("risk_hotspots", [])),
                "seasonality_analysis": self._analyze_seasonality(trend_analysis)
            },
            "predictive_analysis": {
                "forecast": self._generate_risk_forecast(trend_analysis),
                "leading_indicators": self._identify_leading_indicators(analysis_results),
                "scenario_analysis": self._perform_scenario_analysis(analysis_results)
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

    def _generate_compliance_analysis(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate compliance analysis section"""
        framework = self.compliance_frameworks.get(self.config.compliance_framework, {})
        
        return {
            "framework": {
                "name": framework.get("name", "Unknown"),
                "applicable_sections": framework.get("sections", []),
                "compliance_score": self._calculate_compliance_score(analysis_results),
                "gap_analysis": self._perform_gap_analysis(analysis_results)
            },
            "regulatory_requirements": {
                "mandatory_actions": self._identify_mandatory_actions(analysis_results),
                "reporting_obligations": self._identify_reporting_obligations(analysis_results),
                "deadlines": self._identify_compliance_deadlines(analysis_results)
            },
            "documentation_requirements": {
                "required_docs": self._identify_required_documentation(analysis_results),
                "retention_periods": self._get_retention_periods(),
                "audit_requirements": self._get_audit_requirements()
            }
        }

    def _generate_sentiment_analysis(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate sentiment analysis section"""
        sentiment_data = analysis_results.get("sentiment_analysis", {})
        
        return {
            "overall_sentiment": sentiment_data.get("overall_sentiment", "neutral"),
            "sentiment_scores": sentiment_data.get("scores", {}),
            "sentiment_trend": sentiment_data.get("trend", "stable"),
            "key_positive_indicators": sentiment_data.get("positive_indicators", []),
            "key_negative_indicators": sentiment_data.get("negative_indicators", []),
            "impact_on_risk": self._assess_sentiment_impact(sentiment_data)
        }

    def _generate_recommendations(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Generate enhanced actionable recommendations with ROI analysis"""
        recommendations = []
        risk_scores = analysis_results.get("risk_scores", {})
        overall_score = risk_scores.get("overall_risk_score", 0)
        
        if overall_score >= 80:
            recommendations.extend(self._get_critical_recommendations(analysis_results))
        elif overall_score >= 60:
            recommendations.extend(self._get_high_priority_recommendations(analysis_results))
        
        category_scores = risk_scores.get("category_scores", {})
        for risk_type, score in category_scores.items():
            if score > self.config.risk_threshold_high:
                rec = self._get_category_recommendation(risk_type, score, analysis_results)
                if rec:
                    recommendations.append(rec)
        
        recommendations.extend(self._get_compliance_recommendations(analysis_results))
        recommendations = self._prioritize_by_roi(recommendations, analysis_results)
        
        return recommendations[:self.config.max_recommendations]

    def _generate_action_plan(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate actionable implementation plan"""
        recommendations = self._generate_recommendations(analysis_results)
        
        return {
            "immediate_actions": [rec for rec in recommendations if rec.get("priority") == "critical"],
            "short_term_actions": [rec for rec in recommendations if rec.get("priority") == "high"],
            "medium_term_actions": [rec for rec in recommendations if rec.get("priority") == "medium"],
            "long_term_strategies": self._generate_long_term_strategies(analysis_results),
            "resource_requirements": self._calculate_resource_requirements(recommendations),
            "success_metrics": self._define_success_metrics(analysis_results),
            "timeline": self._generate_implementation_timeline(recommendations)
        }

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
                "analysis_duration": "Real-time",
                "data_points_analyzed": self._calculate_data_points(analysis_results)
            },
            "methodology": {
                "risk_detection": "Contextual keyword analysis with intensity scoring",
                "entity_extraction": "Pattern-based financial entity recognition", 
                "relationship_mapping": "Co-occurrence and semantic pattern analysis",
                "trend_analysis": "Segmental risk density and distribution analysis"
            }
        }

    # ALL THE EXISTING HELPER METHODS - KEEP THESE AS THEY WERE BUT ENHANCED
    def _extract_key_findings(self, analysis_results: Dict) -> List[str]:
        """Extract key findings from analysis"""
        findings = []
        risk_scores = analysis_results.get("risk_scores", {})
        
        overall_score = risk_scores.get("overall_risk_score", 0)
        findings.append(f"Overall risk score: {overall_score}/100 ({self._get_risk_level(overall_score).title()} risk level)")
        
        category_scores = risk_scores.get("category_scores", {})
        if category_scores:
            highest_risk = max(category_scores, key=category_scores.get)
            findings.append(f"Primary risk category: {highest_risk.replace('_', ' ').title()} ({category_scores[highest_risk]}/100)")
        
        entities = analysis_results.get("entities", {})
        if entities.get("companies"):
            findings.append(f"Identified {len(entities['companies'])} companies in analysis")
        
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
        
        for risk_type, score in category_scores.items():
            if score > 70:
                concerns.append(f"Elevated {risk_type.replace('_', ' ')} risk (Score: {score}/100)")
        
        financial_impact = risk_scores.get("risk_breakdown", {}).get("financial_impact", {})
        if financial_impact.get("impact_score", 0) > 50:
            concerns.append(f"Significant financial impact potential (${financial_impact.get('total_impact_millions', 0)}M estimated)")
        
        entities = analysis_results.get("entities", {})
        if entities.get("regulatory_bodies"):
            concerns.append(f"Multiple regulatory bodies involved ({len(entities['regulatory_bodies'])})")
        
        return concerns

    def _generate_summary_text(self, analysis_results: Dict, risk_level: str) -> str:
        """Generate human-readable summary text"""
        risk_scores = analysis_results.get("risk_scores", {})
        overall_score = risk_scores.get("overall_risk_score", 0)
        
        summary = f"This analysis identifies {risk_level} level financial risks (Score: {overall_score}/100). "
        
        category_scores = risk_scores.get("category_scores", {})
        if category_scores:
            high_categories = [cat for cat, score in category_scores.items() if score > 60]
            if high_categories:
                summary += f"Primary risk areas include {', '.join([c.replace('_', ' ').title() for c in high_categories])}. "
        
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
        for level, (min_score, max_score, _, _, _) in self.risk_levels.items():
            if min_score <= score <= max_score:
                return level
        return "minimal"

    def _get_risk_weight(self, risk_type: str) -> float:
        """Get risk weight for reporting"""
        weights = {
            "credit_risk": 0.25,
            "market_risk": 0.20, 
            "operational_risk": 0.25,
            "regulatory_risk": 0.15,
            "cyber_risk": 0.10,
            "compliance_risk": 0.05
        }
        return weights.get(risk_type, 0.10)

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
        nodes = network.get("nodes", [])
        risk_nodes = [node for node in nodes if node.get("type") == "risk"]
        
        clusters = []
        if len(risk_nodes) >= 3:
            clusters.append("Multiple risk categories interconnected")
        if any(node.get("score", 0) > 70 for node in risk_nodes):
            clusters.append("High-risk category cluster")
        
        return clusters if clusters else ["Distributed risk profile"]

    def _get_category_recommendation(self, risk_type: str, score: float, analysis_results: Dict) -> Dict[str, Any]:
        """Get category-specific recommendation"""
        recommendations = {
            "credit_risk": {
                "priority": "high",
                "category": "Credit Risk Management",
                "recommendation": "Enhance credit monitoring and debt sustainability analysis",
                "rationale": f"Elevated credit risk identified (Score: {score}/100)",
                "timeline": "2 weeks",
                "estimated_cost": "Low",
                "expected_benefit": "Reduced default risk"
            },
            "market_risk": {
                "priority": "medium", 
                "category": "Market Risk Assessment",
                "recommendation": "Review hedging strategies and market exposure limits",
                "rationale": f"Significant market risk exposure (Score: {score}/100)",
                "timeline": "3 weeks",
                "estimated_cost": "Medium",
                "expected_benefit": "Improved risk-adjusted returns"
            },
            "operational_risk": {
                "priority": "high",
                "category": "Operational Controls",
                "recommendation": "Conduct operational resilience review and control testing",
                "rationale": f"High operational risk level (Score: {score}/100)", 
                "timeline": "1 week",
                "estimated_cost": "Medium",
                "expected_benefit": "Reduced operational losses"
            },
            "regulatory_risk": {
                "priority": "high",
                "category": "Compliance Management",
                "recommendation": "Strengthen compliance monitoring and regulatory engagement",
                "rationale": f"Elevated regulatory risk (Score: {score}/100)",
                "timeline": "1 week",
                "estimated_cost": "High",
                "expected_benefit": "Avoided regulatory penalties"
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
        
        return entity_count + risk_count + relationship_count + 100

    # NEW ENHANCED METHODS
    def _calculate_financial_impact_summary(self, analysis_results: Dict) -> Dict[str, Any]:
        """Calculate comprehensive financial impact summary"""
        entities = analysis_results.get("entities", {})
        risk_scores = analysis_results.get("risk_scores", {})
        
        total_impact = self._calculate_total_financial_impact(entities)
        potential_impact = total_impact * 1.5
        
        return {
            "identified_impact": total_impact,
            "potential_impact": potential_impact,
            "impact_categories": self._analyze_impact_distribution(entities),
            "confidence_level": risk_scores.get("confidence_score", 75),
            "currency": "USD"
        }

    def _calculate_regulatory_exposure(self, analysis_results: Dict) -> Dict[str, Any]:
        """Calculate regulatory exposure metrics"""
        entities = analysis_results.get("entities", {})
        relationships = analysis_results.get("relationships", {})
        
        regulatory_bodies = entities.get("regulatory_bodies", [])
        regulatory_actions = relationships.get("regulatory_relationships", [])
        
        return {
            "regulatory_bodies_count": len(regulatory_bodies),
            "active_investigations": len([ra for ra in regulatory_actions if ra.get("status") == "active"]),
            "jurisdictions": list(set([rb.split()[0] for rb in regulatory_bodies if rb])),
            "exposure_level": "high" if len(regulatory_bodies) > 3 else "medium" if len(regulatory_bodies) > 0 else "low"
        }

    def _calculate_urgency_level(self, analysis_results: Dict) -> str:
        """Calculate overall urgency level"""
        risk_scores = analysis_results.get("risk_scores", {})
        overall_score = risk_scores.get("overall_risk_score", 0)
        
        if overall_score >= 80:
            return "immediate"
        elif overall_score >= 60:
            return "urgent"
        elif overall_score >= 40:
            return "priority"
        else:
            return "standard"

    def _generate_peer_comparison(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate peer comparison analysis"""
        return {
            "industry_average": 45,
            "peer_group_average": 52,
            "percentile_rank": 75,
            "comparison_insights": "Above industry average risk exposure"
        }

    def _map_risks_to_compliance(self, analysis_results: Dict) -> Dict[str, Any]:
        """Map identified risks to compliance requirements"""
        framework = self.compliance_frameworks.get(self.config.compliance_framework, {})
        risk_categories = analysis_results.get("risk_scores", {}).get("category_scores", {})
        
        mapping = {}
        for risk_category in risk_categories.keys():
            framework_risks = framework.get("risk_categories", [])
            if risk_category in framework_risks:
                mapping[risk_category] = {
                    "compliance_section": framework.get("sections", [])[0] if framework.get("sections") else "General",
                    "requirements": self._get_compliance_requirements(risk_category),
                    "assessment": "compliant" if risk_categories[risk_category] < 40 else "needs_review"
                }
        
        return mapping

    def _generate_risk_heatmap(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Generate risk heatmap data"""
        risk_scores = analysis_results.get("risk_scores", {})
        category_scores = risk_scores.get("category_scores", {})
        
        heatmap = []
        for category, score in category_scores.items():
            heatmap.append({
                "category": category,
                "score": score,
                "impact": self._get_risk_weight(category) * 100,
                "level": self._get_risk_level(score)
            })
        
        return heatmap

    def _get_mitigation_status(self, risk_type: str, score: float) -> str:
        """Get mitigation status for risk category"""
        if score >= 80:
            return "urgent_attention"
        elif score >= 60:
            return "needs_mitigation"
        elif score >= 40:
            return "monitor"
        else:
            return "under_control"

    def _get_compliance_requirements(self, risk_type: str) -> List[str]:
        """Get compliance requirements for risk type"""
        requirements = {
            "credit_risk": ["Credit risk assessment", "Loan loss provisioning", "Counterparty risk limits"],
            "market_risk": ["Value at Risk calculation", "Stress testing", "Hedging documentation"],
            "operational_risk": ["Internal controls", "Business continuity planning", "Incident reporting"],
            "regulatory_risk": ["Compliance monitoring", "Regulatory reporting", "Policy documentation"]
        }
        return requirements.get(risk_type, ["General compliance requirements"])

    def _calculate_compliance_score(self, analysis_results: Dict) -> float:
        """Calculate overall compliance score"""
        risk_scores = analysis_results.get("risk_scores", {})
        category_scores = risk_scores.get("category_scores", {})
        
        if not category_scores:
            return 100.0
        
        avg_risk_score = sum(category_scores.values()) / len(category_scores)
        compliance_score = max(0, 100 - avg_risk_score)
        
        return round(compliance_score, 1)

    def _perform_gap_analysis(self, analysis_results: Dict) -> Dict[str, Any]:
        """Perform compliance gap analysis"""
        return {
            "identified_gaps": self._identify_compliance_gaps(analysis_results),
            "severity_level": "medium",
            "remediation_priority": "high",
            "estimated_remediation_time": "90 days"
        }

    def _identify_mandatory_actions(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Identify mandatory compliance actions"""
        risk_scores = analysis_results.get("risk_scores", {})
        high_risks = {k: v for k, v in risk_scores.get("category_scores", {}).items() if v > 60}
        
        actions = []
        for risk in high_risks:
            actions.append({
                "action": f"Review and update {risk} controls",
                "deadline": "30 days",
                "regulatory_basis": f"{self.config.compliance_framework} requirements"
            })
        
        return actions

    def _identify_reporting_obligations(self, analysis_results: Dict) -> List[str]:
        """Identify reporting obligations"""
        return [
            "Quarterly risk assessment report",
            "Annual compliance certification",
            "Regulatory breach notifications"
        ]

    def _identify_compliance_deadlines(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Identify compliance deadlines"""
        return [
            {"requirement": "Quarterly filing", "deadline": "45 days after quarter end"},
            {"requirement": "Annual certification", "deadline": "90 days after fiscal year end"}
        ]

    def _identify_required_documentation(self, analysis_results: Dict) -> List[str]:
        """Identify required documentation"""
        return [
            "Risk assessment reports",
            "Control testing documentation",
            "Compliance policies and procedures"
        ]

    def _get_retention_periods(self) -> Dict[str, str]:
        """Get document retention periods"""
        return {
            "risk_assessments": "7 years",
            "compliance_reports": "5 years",
            "audit_documentation": "7 years"
        }

    def _get_audit_requirements(self) -> List[str]:
        """Get audit requirements"""
        return [
            "Annual internal audit",
            "External compliance audit",
            "Regulatory examination preparation"
        ]

    def _assess_sentiment_impact(self, sentiment_data: Dict) -> str:
        """Assess impact of sentiment on risk"""
        overall_sentiment = sentiment_data.get("overall_sentiment", "neutral")
        if overall_sentiment == "negative":
            return "Amplifies risk perception and market concerns"
        elif overall_sentiment == "positive":
            return "Mitigates risk perception but requires validation"
        else:
            return "Neutral impact on risk assessment"

    def _get_critical_recommendations(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Get critical priority recommendations"""
        return [
            {
                "priority": "critical",
                "category": "Immediate Action",
                "recommendation": "Convene emergency risk committee meeting within 24 hours",
                "rationale": "Critical risk level requires immediate executive attention",
                "timeline": "24 hours",
                "estimated_cost": "Low",
                "expected_benefit": "Rapid response coordination"
            },
            {
                "priority": "critical", 
                "category": "Financial Controls",
                "recommendation": "Implement enhanced financial monitoring and controls",
                "rationale": "Significant financial exposure identified",
                "timeline": "48 hours",
                "estimated_cost": "Medium",
                "expected_benefit": "Exposure containment"
            }
        ]

    def _get_high_priority_recommendations(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Get high priority recommendations"""
        return [
            {
                "priority": "high",
                "category": "Risk Assessment",
                "recommendation": "Conduct detailed risk assessment of identified exposure areas",
                "rationale": "High risk concentration in specific categories",
                "timeline": "1 week",
                "estimated_cost": "Medium",
                "expected_benefit": "Targeted risk mitigation"
            }
        ]

    def _get_compliance_recommendations(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Get compliance-specific recommendations"""
        return [
            {
                "priority": "medium",
                "category": "Compliance",
                "recommendation": "Update compliance framework to address identified gaps",
                "rationale": "Compliance score below optimal level",
                "timeline": "2 weeks",
                "estimated_cost": "High",
                "expected_benefit": "Regulatory compliance assurance"
            }
        ]

    def _prioritize_by_roi(self, recommendations: List[Dict], analysis_results: Dict) -> List[Dict]:
        """Prioritize recommendations by ROI"""
        # Simple ROI calculation based on priority and cost
        for rec in recommendations:
            cost_map = {"Low": 1, "Medium": 2, "High": 3}
            priority_map = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            
            cost_score = cost_map.get(rec.get("estimated_cost", "Medium"), 2)
            priority_score = priority_map.get(rec.get("priority", "medium"), 2)
            
            rec["roi_score"] = priority_score / cost_score
        
        return sorted(recommendations, key=lambda x: x.get("roi_score", 0), reverse=True)

    def _generate_long_term_strategies(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Generate long-term risk management strategies"""
        return [
            {
                "strategy": "Implement enterprise risk management framework",
                "timeline": "6-12 months",
                "benefits": "Comprehensive risk oversight and proactive management"
            },
            {
                "strategy": "Develop risk-aware organizational culture",
                "timeline": "12-24 months", 
                "benefits": "Sustainable risk management and employee engagement"
            }
        ]

    def _calculate_resource_requirements(self, recommendations: List[Dict]) -> Dict[str, Any]:
        """Calculate resource requirements for implementation"""
        total_cost = sum(1 for rec in recommendations if rec.get("estimated_cost") == "Low") * 10000 + \
                    sum(1 for rec in recommendations if rec.get("estimated_cost") == "Medium") * 50000 + \
                    sum(1 for rec in recommendations if rec.get("estimated_cost") == "High") * 100000
        
        return {
            "estimated_budget": f"${total_cost:,}",
            "team_requirements": ["Risk Manager", "Compliance Officer", "IT Specialist"],
            "timeline_commitment": "3-6 months for full implementation"
        }

    def _define_success_metrics(self, analysis_results: Dict) -> List[Dict[str, Any]]:
        """Define success metrics for risk mitigation"""
        return [
            {"metric": "Overall risk score reduction", "target": "20% decrease in 6 months"},
            {"metric": "Compliance score improvement", "target": "85% or higher"},
            {"metric": "Incident reduction", "target": "50% decrease in risk events"}
        ]

    def _generate_implementation_timeline(self, recommendations: List[Dict]) -> List[Dict[str, Any]]:
        """Generate implementation timeline"""
        timeline = []
        current_date = datetime.now()
        
        for i, rec in enumerate(recommendations[:5]):  # Top 5 recommendations
            days_to_add = {"critical": 7, "high": 14, "medium": 30, "low": 60}
            deadline = current_date + timedelta(days=days_to_add.get(rec.get("priority", "medium"), 30))
            
            timeline.append({
                "action": rec["recommendation"],
                "start_date": current_date.strftime("%Y-%m-%d"),
                "deadline": deadline.strftime("%Y-%m-%d"),
                "priority": rec["priority"]
            })
        
        return timeline

    def _analyze_concentration_risk(self, entities: Dict) -> Dict[str, Any]:
        """Analyze concentration risk in entities"""
        companies = entities.get("companies", [])
        return {
            "company_count": len(companies),
            "concentration_level": "high" if len(companies) > 10 else "medium" if len(companies) > 5 else "low",
            "diversification_score": max(0, 100 - len(companies) * 5)
        }

    def _analyze_jurisdictions(self, entities: Dict) -> Dict[str, Any]:
        """Analyze jurisdictional exposure"""
        regulatory_bodies = entities.get("regulatory_bodies", [])
        jurisdictions = list(set([rb.split()[0] for rb in regulatory_bodies if rb]))
        
        return {
            "jurisdictions_identified": jurisdictions,
            "cross_border_exposure": "high" if len(jurisdictions) > 2 else "medium" if len(jurisdictions) > 1 else "low"
        }

    def _perform_sensitivity_analysis(self, entities: Dict) -> Dict[str, Any]:
        """Perform sensitivity analysis on financial impact"""
        total_impact = self._calculate_total_financial_impact(entities)
        
        return {
            "base_case": total_impact,
            "worst_case": total_impact * 2,
            "best_case": total_impact * 0.5,
            "volatility": "high" if total_impact > 1000 else "medium" if total_impact > 100 else "low"
        }

    def _identify_key_stakeholders(self, entities: Dict) -> List[str]:
        """Identify key stakeholders"""
        companies = entities.get("companies", [])
        regulatory_bodies = entities.get("regulatory_bodies", [])
        
        stakeholders = companies[:3] + regulatory_bodies[:2]
        return stakeholders if stakeholders else ["Board of Directors", "Regulatory Bodies"]

    def _analyze_stakeholder_concerns(self, analysis_results: Dict) -> List[str]:
        """Analyze stakeholder concerns"""
        risk_scores = analysis_results.get("risk_scores", {})
        high_risks = [k for k, v in risk_scores.get("category_scores", {}).items() if v > 60]
        
        concerns = []
        for risk in high_risks:
            concerns.append(f"Exposure to {risk.replace('_', ' ')}")
        
        return concerns if concerns else ["General risk management practices"]

    def _generate_communication_plan(self, entities: Dict) -> Dict[str, Any]:
        """Generate communication plan"""
        return {
            "audiences": ["Executive Management", "Board of Directors", "Regulatory Bodies"],
            "frequency": "Quarterly",
            "channels": ["Executive Briefings", "Board Reports", "Regulatory Filings"]
        }

    def _analyze_seasonality(self, trend_analysis: Dict) -> Dict[str, Any]:
        """Analyze seasonal patterns in risk"""
        return {
            "seasonal_pattern": "Not significant",
            "peak_risk_period": "Q4",
            "trend_stability": "Moderate"
        }

    def _generate_risk_forecast(self, trend_analysis: Dict) -> Dict[str, Any]:
        """Generate risk forecast"""
        return {
            "short_term_outlook": "Stable to increasing",
            "medium_term_trend": "Requires monitoring",
            "confidence_level": "Medium"
        }

    def _identify_leading_indicators(self, analysis_results: Dict) -> List[str]:
        """Identify leading risk indicators"""
        return [
            "Regulatory scrutiny intensity",
            "Market volatility indices", 
            "Credit spread movements"
        ]

    def _perform_scenario_analysis(self, analysis_results: Dict) -> Dict[str, Any]:
        """Perform scenario analysis"""
        return {
            "base_scenario": "Current risk levels persist",
            "stress_scenario": "20% increase in identified risks",
            "recovery_scenario": "Implementation of all recommendations"
        }

    def _identify_compliance_gaps(self, analysis_results: Dict) -> List[str]:
        """Identify compliance gaps"""
        risk_scores = analysis_results.get("risk_scores", {})
        high_risks = [k for k, v in risk_scores.get("category_scores", {}).items() if v > 60]
        
        gaps = []
        for risk in high_risks:
            gaps.append(f"Inadequate {risk.replace('_', ' ')} controls")
        
        return gaps if gaps else ["Minor control enhancements needed"]

    # FORMATTING METHODS
    def _format_json_report(self, base_report: Dict, analysis_results: Dict) -> Dict[str, Any]:
        """Format report as JSON"""
        return base_report

    def _format_html_report(self, base_report: Dict, analysis_results: Dict) -> Dict[str, Any]:
        """Format report as HTML"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Financial Risk Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .risk-critical { color: #DC2626; font-weight: bold; }
                .risk-high { color: #EA580C; font-weight: bold; }
                .risk-medium { color: #CA8A04; }
                .risk-low { color: #16A34A; }
                .section { margin-bottom: 30px; padding: 20px; border-left: 4px solid #3B82F6; }
            </style>
        </head>
        <body>
            <h1>Financial Risk Analysis Report</h1>
            <div class="section">
                <h2>Executive Summary</h2>
                <p>Overall Risk Score: <span class="risk-{{ risk_level }}">{{ overall_score }}/100</span></p>
                <p><strong>Risk Level:</strong> {{ risk_level|title }}</p>
                <p>{{ summary_text }}</p>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            risk_level=base_report["executive_summary"]["risk_level"],
            overall_score=base_report["executive_summary"]["overall_risk_score"],
            summary_text=base_report["executive_summary"]["summary_text"]
        )
        
        return {
            "format": "html",
            "content": html_content,
            "metadata": base_report["metadata"]
        }

    def _format_markdown_report(self, base_report: Dict, analysis_results: Dict) -> Dict[str, Any]:
        """Format report as Markdown"""
        exec_summary = base_report["executive_summary"]
        md_content = f"""# Financial Risk Analysis Report

## Executive Summary

**Overall Risk Score:** {exec_summary['overall_risk_score']}/100 ({exec_summary['risk_level'].title()})

{exec_summary['summary_text']}

### Key Findings
"""
        for finding in exec_summary['key_findings']:
            md_content += f"- {finding}\n"

        return {
            "format": "markdown",
            "content": md_content,
            "metadata": base_report["metadata"]
        }

    def _format_executive_summary(self, base_report: Dict, analysis_results: Dict) -> Dict[str, Any]:
        """Format executive summary only"""
        return {
            "executive_summary": base_report["executive_summary"],
            "recommendations": base_report["recommendations"][:3],
            "metadata": base_report["metadata"]
        }

    def _format_compliance_report(self, base_report: Dict, analysis_results: Dict) -> Dict[str, Any]:
        """Format compliance-focused report"""
        return {
            "compliance_analysis": base_report["compliance_analysis"],
            "risk_analysis": {
                "overall_assessment": base_report["risk_analysis"]["overall_assessment"],
                "compliance_mapping": base_report["risk_analysis"]["compliance_mapping"]
            },
            "action_plan": base_report["action_plan"],
            "metadata": base_report["metadata"]
        }

    # API METHODS
    async def generate_and_send_report(self, analysis_results: Dict, recipients: List[str]) -> Dict[str, Any]:
        """Generate report and send via configured APIs"""
        try:
            report = self.generate_comprehensive_report(analysis_results)
            report_id = await self._store_report(report)
            
            return {
                "status": "success",
                "report_id": report_id,
                "recipients_notified": len(recipients),
                "channels_used": [channel for channel, config in self.notification_apis.items() if config["enabled"]]
            }
            
        except Exception as e:
            self.logger.error(f"Report generation and sending failed: {e}")
            return {"status": "error", "error": str(e)}

    async def _store_report(self, report: Dict) -> str:
        """Store report in database or file system"""
        report_id = report["metadata"]["report_id"]
        filename = f"reports/{report_id}.json"
        
        async with aiofiles.open(filename, 'w') as f:
            await f.write(json.dumps(report, indent=2, default=str))
        
        return report_id

# USAGE EXAMPLE
if __name__ == "__main__":
    config = ReportConfig(
        include_executive_summary=True,
        include_technical_details=True,
        compliance_framework="SOX"
    )
    
    builder = ReportBuilder(config)
    
    sample_analysis = {
        "risk_scores": {
            "overall_risk_score": 72,
            "category_scores": {
                "credit_risk": 68,
                "market_risk": 55,
                "operational_risk": 81,
                "regulatory_risk": 62
            },
            "confidence_score": 88
        },
        "entities": {
            "companies": ["Bank of America", "JPMorgan", "Goldman Sachs"],
            "financial_amounts": ["$2.5 billion fine", "$150 million settlement"]
        },
        "timestamp": datetime.now().isoformat()
    }
    
    report = builder.generate_comprehensive_report(sample_analysis, "json")
    print(f"Report generated with {len(report)} sections")
    print(f"Overall risk score: {report['executive_summary']['overall_risk_score']}")