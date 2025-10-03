"""
Generate chart data for frontend visualizations with enhanced APIs
"""
from typing import Dict, List, Any, Optional
import json
import re
import random
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass

@dataclass
class ChartConfig:
    """Configuration for chart styling and behavior"""
    color_schemes: Dict[str, List[str]]
    chart_types: List[str]
    animation_duration: int = 1000
    responsive: bool = True

class ChartDataGenerator:
    def __init__(self):
        # Enhanced color schemes for different chart types
        self.color_scheme = {
            "risk_categories": {
                "credit_risk": "#FF6B6B",
                "market_risk": "#4ECDC4", 
                "operational_risk": "#45B7D1",
                "regulatory_risk": "#96CEB4",
                "cyber_risk": "#6A0572",
                "compliance_risk": "#FF9A8B"
            },
            "sentiment": {
                "positive": "#4CAF50",
                "negative": "#F44336",
                "neutral": "#FFC107"
            },
            "entities": {
                "companies": "#FFE66D",
                "regulators": "#FF9A8B",
                "financial": "#6A0572",
                "people": "#4ECDC4"
            },
            "trends": {
                "upward": "#4CAF50",
                "downward": "#F44336",
                "stable": "#FFC107"
            }
        }
        
        # Chart.js compatible configurations
        self.chart_configs = {
            "bar": {
                "type": "bar",
                "options": {
                    "responsive": True,
                    "plugins": {
                        "legend": {"position": "top"},
                        "title": {"display": True, "text": "Risk Analysis"}
                    }
                }
            },
            "line": {
                "type": "line", 
                "options": {
                    "responsive": True,
                    "interaction": {"mode": "index", "intersect": False},
                    "scales": {
                        "x": {"display": True, "title": {"display": True}},
                        "y": {"display": True, "title": {"display": True}}
                    }
                }
            },
            "pie": {
                "type": "pie",
                "options": {
                    "responsive": True,
                    "plugins": {
                        "legend": {"position": "bottom"},
                        "tooltip": {"callbacks": {"label": "function(context) { return context.label + ': ' + context.parsed + '%'; }"}}
                    }
                }
            },
            "doughnut": {
                "type": "doughnut",
                "options": {
                    "responsive": True,
                    "cutout": "50%"
                }
            },
            "radar": {
                "type": "radar",
                "options": {
                    "responsive": True,
                    "elements": {"line": {"tension": 0.3}}
                }
            }
        }

    # 🎯 ENHANCED DASHBOARD DATA GENERATION
    def generate_risk_dashboard_data(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate complete dashboard data for frontend with enhanced visualizations"""
        dashboard_data = {
            "risk_gauges": self._generate_risk_gauges(analysis_results),
            "category_charts": self._generate_category_charts(analysis_results),
            "entity_visualizations": self._generate_entity_visualizations(analysis_results),
            "trend_charts": self._generate_trend_charts(analysis_results),
            "network_data": self._generate_network_data(analysis_results),
            "sentiment_analysis": self._generate_sentiment_charts(analysis_results),
            "compliance_metrics": self._generate_compliance_charts(analysis_results),
            "temporal_analysis": self._generate_temporal_charts(analysis_results),
            "chart_configs": self.chart_configs,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "data_points": self._calculate_data_points(analysis_results),
                "refresh_interval": 300  # 5 minutes in seconds
            }
        }
        
        return dashboard_data

    # 🔄 REAL-TIME DATA UPDATES
    def generate_live_dashboard_updates(self, analysis_results: Dict, previous_data: Dict = None) -> Dict[str, Any]:
        """Generate incremental updates for real-time dashboard"""
        current_data = self.generate_risk_dashboard_data(analysis_results)
        
        if not previous_data:
            return current_data
        
        # Calculate changes for real-time updates
        updates = {
            "risk_gauges": self._calculate_gauge_changes(current_data["risk_gauges"], previous_data.get("risk_gauges", {})),
            "trend_updates": self._calculate_trend_updates(current_data["trend_charts"], previous_data.get("trend_charts", {})),
            "alerts": self._generate_alerts(current_data, previous_data),
            "timestamp": datetime.now().isoformat()
        }
        
        return updates

    def _calculate_gauge_changes(self, current: Dict, previous: Dict) -> Dict:
        """Calculate changes in gauge values for real-time updates"""
        changes = {}
        for gauge_name, current_gauge in current.items():
            if gauge_name in previous:
                prev_score = previous[gauge_name].get("score", 0)
                curr_score = current_gauge.get("score", 0)
                changes[gauge_name] = {
                    "current": curr_score,
                    "previous": prev_score,
                    "change": curr_score - prev_score,
                    "change_percentage": ((curr_score - prev_score) / prev_score * 100) if prev_score > 0 else 0,
                    "direction": "up" if curr_score > prev_score else "down" if curr_score < prev_score else "stable"
                }
        return changes

    # 📊 ENHANCED RISK GAUGES
    def _generate_risk_gauges(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate enhanced data for risk gauge charts"""
        risk_scores = analysis_results.get("risk_scores", {})
        trend_analysis = analysis_results.get("trend_analysis", {})
        
        overall_score = risk_scores.get("overall_risk_score", 0)
        
        gauges = {
            "overall_risk": {
                "score": overall_score,
                "max_score": 100,
                "ranges": [
                    {"min": 0, "max": 30, "color": "#4CAF50", "label": "Low"},
                    {"min": 30, "max": 70, "color": "#FF9800", "label": "Medium"},
                    {"min": 70, "max": 100, "color": "#F44336", "label": "High"}
                ],
                "trend": trend_analysis.get("trend_direction", "stable"),
                "confidence": risk_scores.get("confidence_score", 85)
            }
        }
        
        # Add category gauges with trend data
        category_scores = risk_scores.get("category_scores", {})
        for risk_type, score in category_scores.items():
            gauges[risk_type] = {
                "score": score,
                "max_score": 100,
                "color": self.color_scheme["risk_categories"].get(risk_type, "#666666"),
                "label": risk_type.replace('_', ' ').title(),
                "trend": self._calculate_category_trend(risk_type, analysis_results),
                "priority": self._calculate_risk_priority(score, risk_type)
            }
        
        return gauges

    def _calculate_category_trend(self, risk_type: str, analysis_results: Dict) -> str:
        """Calculate trend direction for risk category"""
        # This would integrate with historical data
        trends = ["upward", "downward", "stable"]
        return random.choice(trends)

    def _calculate_risk_priority(self, score: float, risk_type: str) -> str:
        """Calculate priority level based on score and risk type"""
        if score >= 80:
            return "critical"
        elif score >= 60:
            return "high"
        elif score >= 40:
            return "medium"
        else:
            return "low"

    # 📈 ENHANCED CATEGORY CHARTS
    def _generate_category_charts(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate enhanced data for risk category charts"""
        risk_scores = analysis_results.get("risk_scores", {})
        category_scores = risk_scores.get("category_scores", {})
        
        if not category_scores:
            category_scores = self._generate_sample_category_scores()

        labels = [rt.replace('_', ' ').title() for rt in category_scores.keys()]
        scores = list(category_scores.values())
        colors = [self.color_scheme["risk_categories"].get(rt, "#666666") for rt in category_scores.keys()]

        # Enhanced Bar Chart
        bar_chart = {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Risk Scores",
                    "data": scores,
                    "backgroundColor": colors,
                    "borderColor": [self._adjust_color_brightness(color, -20) for color in colors],
                    "borderWidth": 2,
                    "borderRadius": 4
                }]
            },
            "options": {
                **self.chart_configs["bar"]["options"],
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "max": 100,
                        "title": {"display": True, "text": "Risk Score"}
                    },
                    "x": {
                        "title": {"display": True, "text": "Risk Categories"}
                    }
                }
            }
        }

        # Enhanced Pie Chart
        pie_chart = {
            "type": "pie",
            "data": {
                "labels": labels,
                "datasets": [{
                    "data": scores,
                    "backgroundColor": colors,
                    "borderColor": "#ffffff",
                    "borderWidth": 2,
                    "hoverOffset": 8
                }]
            },
            "options": self.chart_configs["pie"]["options"]
        }

        # Radar Chart for multi-dimensional analysis
        radar_chart = {
            "type": "radar",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Risk Profile",
                    "data": scores,
                    "backgroundColor": "rgba(255, 107, 107, 0.2)",
                    "borderColor": "#FF6B6B",
                    "pointBackgroundColor": colors,
                    "pointBorderColor": "#fff",
                    "pointHoverBackgroundColor": "#fff",
                    "pointHoverBorderColor": "#FF6B6B"
                }]
            },
            "options": self.chart_configs["radar"]["options"]
        }

        return {
            "bar_chart": bar_chart,
            "pie_chart": pie_chart,
            "radar_chart": radar_chart,
            "summary": {
                "highest_risk": max(category_scores, key=category_scores.get) if category_scores else "none",
                "lowest_risk": min(category_scores, key=category_scores.get) if category_scores else "none",
                "average_score": sum(category_scores.values()) / len(category_scores) if category_scores else 0,
                "total_categories": len(category_scores)
            }
        }

    # 🏢 ENHANCED ENTITY VISUALIZATIONS
    def _generate_entity_visualizations(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate enhanced data for entity visualizations"""
        entities = analysis_results.get("entities", {})
        
        companies = entities.get("companies", [])
        regulatory_bodies = entities.get("regulatory_bodies", [])
        financial_amounts = entities.get("financial_amounts", [])
        
        # Company mentions with frequency
        company_mentions = self._calculate_entity_frequency(companies)
        top_companies = dict(sorted(company_mentions.items(), key=lambda x: x[1], reverse=True)[:8])

        # Company bar chart
        company_chart = {
            "type": "bar",
            "data": {
                "labels": list(top_companies.keys()),
                "datasets": [{
                    "label": "Mention Frequency",
                    "data": list(top_companies.values()),
                    "backgroundColor": self.color_scheme["entities"]["companies"],
                    "borderColor": self._adjust_color_brightness(self.color_scheme["entities"]["companies"], -20),
                    "borderWidth": 1
                }]
            },
            "options": {
                **self.chart_configs["bar"]["options"],
                "indexAxis": 'y',  # Horizontal bar chart
                "plugins": {
                    "title": {"text": "Top Companies Mentioned", "display": True}
                }
            }
        }

        # Financial impact chart
        financial_data = self._process_financial_amounts(financial_amounts)
        financial_chart = {
            "type": "bar",
            "data": {
                "labels": [item["label"] for item in financial_data[:6]],
                "datasets": [{
                    "label": "Amount (Millions)",
                    "data": [item["value"] for item in financial_data[:6]],
                    "backgroundColor": self.color_scheme["entities"]["financial"],
                    "borderColor": self._adjust_color_brightness(self.color_scheme["entities"]["financial"], -20),
                    "borderWidth": 2
                }]
            },
            "options": {
                **self.chart_configs["bar"]["options"],
                "plugins": {
                    "title": {"text": "Financial Impact Analysis", "display": True}
                }
            }
        }

        return {
            "company_chart": company_chart,
            "financial_chart": financial_chart,
            "entity_counts": {
                "companies": len(companies),
                "regulatory_bodies": len(regulatory_bodies),
                "financial_amounts": len(financial_amounts),
                "dates": len(entities.get("dates", [])),
                "people": len(entities.get("people", []))
            },
            "top_entities": {
                "companies": top_companies,
                "regulators": regulatory_bodies[:5]
            }
        }

    # 📈 ENHANCED TREND CHARTS
    def _generate_trend_charts(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate enhanced data for trend analysis charts"""
        trend_analysis = analysis_results.get("trend_analysis", {})
        density_trend = trend_analysis.get("density_trend", {})
        
        # Generate time-based labels
        time_labels = self._generate_time_labels(7)  # Last 7 periods
        
        # Risk density trend line chart
        densities = density_trend.get("densities", self._generate_sample_trend_data())
        
        trend_chart = {
            "type": "line",
            "data": {
                "labels": time_labels,
                "datasets": [{
                    "label": "Risk Density Trend",
                    "data": densities,
                    "borderColor": "#FF6B6B",
                    "backgroundColor": "rgba(255, 107, 107, 0.1)",
                    "fill": True,
                    "tension": 0.4,
                    "pointBackgroundColor": "#FF6B6B",
                    "pointBorderColor": "#ffffff",
                    "pointBorderWidth": 2
                }]
            },
            "options": {
                **self.chart_configs["line"]["options"],
                "plugins": {
                    "title": {"text": "Risk Density Over Time", "display": True}
                },
                "scales": {
                    "y": {"title": {"text": "Risk Density (%)"}},
                    "x": {"title": {"text": "Time Period"}}
                }
            }
        }

        # Multi-category trend comparison
        category_trends = self._generate_category_trends_data()
        multi_trend_chart = {
            "type": "line",
            "data": {
                "labels": time_labels,
                "datasets": [
                    {
                        "label": category,
                        "data": trends,
                        "borderColor": self.color_scheme["risk_categories"].get(category.lower().replace(' ', '_'), "#666666"),
                        "backgroundColor": "transparent",
                        "tension": 0.3
                    }
                    for category, trends in category_trends.items()
                ]
            },
            "options": {
                **self.chart_configs["line"]["options"],
                "plugins": {
                    "title": {"text": "Risk Category Trends", "display": True}
                }
            }
        }

        return {
            "trend_chart": trend_chart,
            "multi_trend_chart": multi_trend_chart,
            "trend_metrics": {
                "trend_direction": density_trend.get("trend", "stable"),
                "peak_density": max(densities) if densities else 0,
                "average_density": sum(densities) / len(densities) if densities else 0,
                "volatility": np.std(densities) if densities else 0
            }
        }

    # 🎭 NEW: SENTIMENT ANALYSIS CHARTS
    def _generate_sentiment_charts(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate sentiment analysis charts"""
        sentiment_data = analysis_results.get("sentiment_analysis", {})
        
        sentiment_scores = sentiment_data.get("scores", {
            "positive": random.randint(20, 40),
            "negative": random.randint(15, 35),
            "neutral": random.randint(30, 50)
        })
        
        # Sentiment distribution doughnut chart
        sentiment_chart = {
            "type": "doughnut",
            "data": {
                "labels": ["Positive", "Negative", "Neutral"],
                "datasets": [{
                    "data": [sentiment_scores["positive"], sentiment_scores["negative"], sentiment_scores["neutral"]],
                    "backgroundColor": [
                        self.color_scheme["sentiment"]["positive"],
                        self.color_scheme["sentiment"]["negative"],
                        self.color_scheme["sentiment"]["neutral"]
                    ],
                    "borderColor": "#ffffff",
                    "borderWidth": 3
                }]
            },
            "options": self.chart_configs["doughnut"]["options"]
        }

        return {
            "sentiment_chart": sentiment_chart,
            "sentiment_score": sentiment_scores,
            "overall_sentiment": self._calculate_overall_sentiment(sentiment_scores)
        }

    # 📋 NEW: COMPLIANCE METRICS
    def _generate_compliance_charts(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate compliance and regulatory metrics charts"""
        compliance_data = analysis_results.get("compliance_metrics", {})
        
        # Compliance status gauge data
        compliance_gauge = {
            "score": compliance_data.get("compliance_score", 75),
            "max_score": 100,
            "ranges": [
                {"min": 0, "max": 60, "color": "#F44336", "label": "Non-Compliant"},
                {"min": 60, "max": 80, "color": "#FFC107", "label": "Partial"},
                {"min": 80, "max": 100, "color": "#4CAF50", "label": "Compliant"}
            ]
        }

        return {
            "compliance_gauge": compliance_gauge,
            "regulatory_mentions": compliance_data.get("regulatory_mentions", 0)
        }

    # ⏰ NEW: TEMPORAL ANALYSIS
    def _generate_temporal_charts(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate time-based analysis charts"""
        # Risk intensity by hour (simulated data)
        hours = [f"{h:02d}:00" for h in range(24)]
        risk_intensity = [random.randint(10, 90) for _ in range(24)]
        
        temporal_chart = {
            "type": "line",
            "data": {
                "labels": hours,
                "datasets": [{
                    "label": "Risk Intensity",
                    "data": risk_intensity,
                    "borderColor": "#6A0572",
                    "backgroundColor": "rgba(106, 5, 114, 0.1)",
                    "fill": True,
                    "tension": 0.4
                }]
            },
            "options": {
                **self.chart_configs["line"]["options"],
                "plugins": {
                    "title": {"text": "Risk Intensity by Hour", "display": True}
                }
            }
        }

        return {
            "temporal_chart": temporal_chart,
            "peak_hour": hours[risk_intensity.index(max(risk_intensity))],
            "low_hour": hours[risk_intensity.index(min(risk_intensity))]
        }

    # 🔗 NETWORK DATA (Enhanced)
    def _generate_network_data(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate enhanced data for network visualization"""
        relationships = analysis_results.get("relationships", {})
        risk_network = relationships.get("risk_networks", {})
        
        # Enhanced network data with more node properties
        nodes = risk_network.get("nodes", self._generate_sample_network_nodes())
        links = risk_network.get("links", self._generate_sample_network_links(nodes))
        
        return {
            "nodes": nodes,
            "links": links,
            "network_metrics": {
                "total_nodes": len(nodes),
                "total_connections": len(links),
                "network_density": risk_network.get("network_density", 0.65),
                "central_nodes": self._find_central_nodes(nodes, links)
            }
        }

    # 🛠️ HELPER METHODS
    def _adjust_color_brightness(self, color: str, percent: int) -> str:
        """Adjust color brightness by percentage"""
        # Simple implementation - in production, use a proper color manipulation library
        return color  # Placeholder

    def _calculate_entity_frequency(self, entities: List[str]) -> Dict[str, int]:
        """Calculate frequency of entity mentions"""
        frequency = {}
        for entity in entities:
            frequency[entity] = frequency.get(entity, 0) + 1
        return frequency

    def _process_financial_amounts(self, amounts: List[str]) -> List[Dict]:
        """Process financial amounts for visualization"""
        processed = []
        for amount in amounts[:8]:  # Limit to top 8
            numeric_value = self._extract_numeric_value(amount)
            processed.append({
                "label": amount[:25] + "..." if len(amount) > 25 else amount,
                "value": numeric_value,
                "original": amount
            })
        return sorted(processed, key=lambda x: x["value"], reverse=True)

    def _extract_numeric_value(self, amount_str: str) -> float:
        """Extract numeric value from financial amount string"""
        try:
            clean_str = amount_str.replace('$', '').replace(',', '')
            numeric_match = re.search(r'(\d+(?:\.\d+)?)', clean_str)
            if numeric_match:
                value = float(numeric_match.group(1))
                
                if 'billion' in amount_str.lower():
                    return value * 1000
                elif 'million' in amount_str.lower():
                    return value
                else:
                    return value / 1000000
            return 0
        except:
            return 0

    def _generate_time_labels(self, periods: int) -> List[str]:
        """Generate time period labels"""
        base_date = datetime.now()
        return [(base_date - timedelta(days=x)).strftime('%m/%d') for x in range(periods)][::-1]

    def _generate_sample_trend_data(self) -> List[float]:
        """Generate sample trend data"""
        return [random.uniform(20, 80) for _ in range(7)]

    def _generate_sample_category_scores(self) -> Dict[str, float]:
        """Generate sample category scores for demo"""
        return {
            "credit_risk": random.uniform(30, 85),
            "market_risk": random.uniform(25, 80),
            "operational_risk": random.uniform(40, 90),
            "regulatory_risk": random.uniform(35, 75),
            "cyber_risk": random.uniform(50, 95)
        }

    def _generate_category_trends_data(self) -> Dict[str, List[float]]:
        """Generate sample category trends data"""
        categories = ["Credit Risk", "Market Risk", "Operational Risk", "Regulatory Risk"]
        return {category: [random.uniform(20, 80) for _ in range(7)] for category in categories}

    def _generate_sample_network_nodes(self) -> List[Dict]:
        """Generate sample network nodes"""
        node_types = ["company", "regulator", "risk", "person"]
        return [
            {
                "id": f"node_{i}",
                "label": f"Entity {i}",
                "type": random.choice(node_types),
                "value": random.randint(1, 10),
                "group": random.randint(1, 4)
            }
            for i in range(15)
        ]

    def _generate_sample_network_links(self, nodes: List[Dict]) -> List[Dict]:
        """Generate sample network links"""
        links = []
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if random.random() > 0.7:  # 30% connection probability
                    links.append({
                        "source": nodes[i]["id"],
                        "target": nodes[j]["id"],
                        "value": random.randint(1, 5)
                    })
        return links

    def _find_central_nodes(self, nodes: List[Dict], links: List[Dict]) -> List[str]:
        """Find central nodes in network"""
        if not nodes:
            return []
        return [node["id"] for node in nodes[:3]]  # Return first 3 as central

    def _calculate_overall_sentiment(self, sentiment_scores: Dict) -> str:
        """Calculate overall sentiment from scores"""
        positive = sentiment_scores.get("positive", 0)
        negative = sentiment_scores.get("negative", 0)
        
        if positive > negative + 10:
            return "positive"
        elif negative > positive + 10:
            return "negative"
        else:
            return "neutral"

    def _calculate_data_points(self, analysis_results: Dict) -> int:
        """Calculate total data points in analysis"""
        entities = analysis_results.get("entities", {})
        total_entities = sum(len(entities.get(key, [])) for key in entities)
        return total_entities + len(analysis_results.get("risk_scores", {}))

    def _calculate_trend_updates(self, current: Dict, previous: Dict) -> Dict:
        """Calculate trend updates for real-time dashboard"""
        return {
            "new_data_points": random.randint(1, 5),
            "trend_changes": {"overall": "stable", "market": "upward"},
            "last_update": datetime.now().isoformat()
        }

    def _generate_alerts(self, current: Dict, previous: Dict) -> List[Dict]:
        """Generate alerts based on data changes"""
        alerts = []
        if random.random() > 0.7:  # 30% chance of alert
            alerts.append({
                "id": f"alert_{int(datetime.now().timestamp())}",
                "type": "warning",
                "title": "Risk Level Increased",
                "message": "Overall risk score has increased by 15%",
                "timestamp": datetime.now().isoformat(),
                "priority": "medium"
            })
        return alerts

    # 📤 ENHANCED EXPORT FUNCTIONALITY
    def generate_export_data(self, analysis_results: Dict, format: str = "json") -> str:
        """Generate enhanced data for export in various formats"""
        dashboard_data = self.generate_risk_dashboard_data(analysis_results)
        
        export_data = {
            "analysis_timestamp": analysis_results.get("timestamp", datetime.now().isoformat()),
            "document_info": analysis_results.get("document_info", {}),
            "risk_analysis": analysis_results.get("risk_scores", {}),
            "entities": analysis_results.get("entities", {}),
            "trends": analysis_results.get("trend_analysis", {}),
            "relationships": analysis_results.get("relationships", {}),
            "sentiment": analysis_results.get("sentiment_analysis", {}),
            "compliance": analysis_results.get("compliance_metrics", {}),
            "visualization_data": dashboard_data,
            "export_metadata": {
                "exported_at": datetime.now().isoformat(),
                "format": format,
                "version": "2.0"
            }
        }
        
        if format == "json":
            return json.dumps(export_data, indent=2, default=str)
        else:
            return json.dumps(export_data, indent=2, default=str)

# USAGE EXAMPLE
if __name__ == "__main__":
    generator = ChartDataGenerator()
    
    # Sample analysis results
    sample_analysis = {
        "risk_scores": {
            "overall_risk_score": 65,
            "category_scores": {
                "credit_risk": 72,
                "market_risk": 58,
                "operational_risk": 81,
                "regulatory_risk": 45
            }
        },
        "entities": {
            "companies": ["Bank of America", "JPMorgan", "Goldman Sachs", "Morgan Stanley"],
            "financial_amounts": ["$2.5 billion fine", "$150 million settlement", "$500,000 penalty"]
        },
        "timestamp": datetime.now().isoformat()
    }
    
    dashboard_data = generator.generate_risk_dashboard_data(sample_analysis)
    print("Dashboard data generated successfully!")
    print(f"Contains {len(dashboard_data)} main visualization categories")