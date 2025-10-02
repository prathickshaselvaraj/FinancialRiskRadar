"""
Entity-risk relationship mapping and analysis
"""
import re
from typing import Dict, List, Tuple, Any
from collections import defaultdict

class RelationshipMapper:
    def __init__(self):
        self.relationship_patterns = {
            "company_risk": [
                (r'(\b[A-Z][a-zA-Z]+\s+(?:Inc|Corp|Company))\s+faces?\s+(\w+\s+risk)', "faces_risk"),
                (r'(\b[A-Z][a-zA-Z]+\s+(?:Inc|Corp|Company))\s+under\s+(\w+\s+investigation)', "under_investigation"),
                (r'(\b[A-Z][a-zA-Z]+\s+(?:Inc|Corp|Company))\s+reports?\s+(\$\d+\s+[^.!?]+)', "reports_impact")
            ],
            "regulatory_action": [
                (r'(SEC|Federal Reserve)\s+(investigation|enforcement)\s+against\s+([^.!?]+)', "regulatory_action"),
                (r'(\$\d+(?:\.\d+)?\s*(?:million|billion)?)\s+(?:fine|penalty)\s+against\s+([^.!?]+)', "financial_penalty")
            ],
            "impact_relationship": [
                (r'(\w+\s+breach)\s+affects?\s+(\d+\s+(?:million|billion)?\s+customers)', "affects_scale"),
                (r'(\w+\s+failure)\s+causes?\s+(\$\d+\s+[^.!?]+)', "causes_loss")
            ]
        }
    
    def map_entity_relationships(self, text: str, entities: Dict, risks: List[Dict]) -> Dict[str, Any]:
        """Map comprehensive relationships between entities and risks"""
        relationships = {
            "company_relationships": [],
            "regulatory_relationships": [],
            "financial_relationships": [],
            "risk_networks": [],
            "relationship_summary": {}
        }
        
        # Extract explicit relationships from text
        explicit_relationships = self._extract_explicit_relationships(text)
        relationships["explicit_relationships"] = explicit_relationships
        
        # Build company-risk relationships
        company_risk_rels = self._build_company_risk_relationships(entities, risks, text)
        relationships["company_relationships"] = company_risk_rels
        
        # Build regulatory relationships
        regulatory_rels = self._build_regulatory_relationships(entities, risks, text)
        relationships["regulatory_relationships"] = regulatory_rels
        
        # Build financial impact relationships
        financial_rels = self._build_financial_relationships(entities, text)
        relationships["financial_relationships"] = financial_rels
        
        # Build risk network
        risk_network = self._build_risk_network(risks, entities, text)
        relationships["risk_networks"] = risk_network
        
        # Generate relationship summary
        relationships["relationship_summary"] = self._generate_relationship_summary(relationships)
        
        return relationships
    
    def _extract_explicit_relationships(self, text: str) -> List[Dict[str, Any]]:
        """Extract explicitly stated relationships from text"""
        relationships = []
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Check each relationship pattern
            for category, patterns in self.relationship_patterns.items():
                for pattern, rel_type in patterns:
                    matches = re.findall(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        if len(match) == 2:
                            source, target = match
                            relationships.append({
                                "source": source.strip(),
                                "target": target.strip(),
                                "relationship": rel_type,
                                "sentence": sentence,
                                "category": category,
                                "confidence": "high"
                            })
                        elif len(match) == 3:
                            regulator, action, company = match
                            relationships.append({
                                "source": regulator.strip(),
                                "target": company.strip(),
                                "relationship": f"{action}_{rel_type}",
                                "sentence": sentence,
                                "category": category,
                                "confidence": "high"
                            })
        
        return relationships
    
    def _build_company_risk_relationships(self, entities: Dict, risks: List[Dict], text: str) -> List[Dict[str, Any]]:
        """Build relationships between companies and risk types"""
        relationships = []
        sentences = re.split(r'[.!?]+', text)
        
        for company in entities.get("companies", [])[:10]:  # Limit to top 10 companies
            company_risks = []
            
            for risk in risks:
                risk_type = risk["type"]
                risk_keywords = risk.get("keywords_found", [])
                
                # Find sentences where company and risk co-occur
                co_occurrence_sentences = []
                for sentence in sentences:
                    if company in sentence and any(keyword in sentence.lower() for keyword in risk_keywords):
                        co_occurrence_sentences.append(sentence)
                
                if co_occurrence_sentences:
                    # Calculate relationship strength
                    strength = min(len(co_occurrence_sentences) * 20, 100)
                    
                    company_risks.append({
                        "risk_type": risk_type,
                        "risk_score": risk["score"],
                        "relationship_strength": strength,
                        "evidence_sentences": co_occurrence_sentences[:3],  # Limit to 3 sentences
                        "co_occurrence_count": len(co_occurrence_sentences)
                    })
            
            if company_risks:
                relationships.append({
                    "company": company,
                    "associated_risks": company_risks,
                    "total_risk_exposure": sum(risk["risk_score"] * risk["relationship_strength"] / 100 
                                             for risk in company_risks) / len(company_risks) if company_risks else 0,
                    "primary_risk": max(company_risks, key=lambda x: x["relationship_strength"])["risk_type"] if company_risks else "none"
                })
        
        return relationships
    
    def _build_regulatory_relationships(self, entities: Dict, risks: List[Dict], text: str) -> List[Dict[str, Any]]:
        """Build relationships involving regulatory bodies"""
        relationships = []
        
        regulatory_bodies = entities.get("regulatory_bodies", [])
        companies = entities.get("companies", [])
        
        if not regulatory_bodies or not companies:
            return relationships
        
        sentences = re.split(r'[.!?]+', text)
        
        for regulator in regulatory_bodies:
            regulator_actions = []
            
            for company in companies:
                # Find sentences with both regulator and company
                joint_sentences = [s for s in sentences if regulator in s and company in s]
                
                if joint_sentences:
                    # Analyze the nature of relationship
                    relationship_type = "monitoring"
                    confidence = "medium"
                    
                    for sentence in joint_sentences:
                        sentence_lower = sentence.lower()
                        if any(word in sentence_lower for word in ["investigation", "probe", "scrutiny"]):
                            relationship_type = "investigation"
                            confidence = "high"
                        elif any(word in sentence_lower for word in ["fine", "penalty", "sanction"]):
                            relationship_type = "enforcement"
                            confidence = "high"
                        elif any(word in sentence_lower for word in ["regulation", "compliance", "oversight"]):
                            relationship_type = "regulation"
                            confidence = "medium"
                    
                    # Find associated financial amounts
                    financial_impacts = []
                    for sentence in joint_sentences:
                        amounts = re.findall(r'\$\d+(?:\.\d+)?(?:\s+[mb]illion)?', sentence)
                        financial_impacts.extend(amounts)
                    
                    regulator_actions.append({
                        "company": company,
                        "relationship_type": relationship_type,
                        "confidence": confidence,
                        "evidence_sentences": joint_sentences[:2],
                        "financial_impact": list(set(financial_impacts))[:3],
                        "interaction_count": len(joint_sentences)
                    })
            
            if regulator_actions:
                relationships.append({
                    "regulatory_body": regulator,
                    "actions": regulator_actions,
                    "total_companies_affected": len(regulator_actions),
                    "primary_action_type": max(
                        set([action["relationship_type"] for action in regulator_actions]),
                        key=[action["relationship_type"] for action in regulator_actions].count
                    ) if regulator_actions else "monitoring"
                })
        
        return relationships
    
    def _build_financial_relationships(self, entities: Dict, text: str) -> List[Dict[str, Any]]:
        """Build relationships involving financial impacts"""
        relationships = []
        
        companies = entities.get("companies", [])
        financial_amounts = entities.get("financial_amounts", [])
        
        if not companies or not financial_amounts:
            return relationships
        
        sentences = re.split(r'[.!?]+', text)
        
        for company in companies:
            company_financials = []
            
            for amount in financial_amounts:
                # Find sentences where company and amount co-occur
                co_occurrence_sentences = [s for s in sentences if company in s and amount in s]
                
                if co_occurrence_sentences:
                    # Determine financial context
                    context = "general"
                    for sentence in co_occurrence_sentences:
                        sentence_lower = sentence.lower()
                        if any(word in sentence_lower for word in ["fine", "penalty", "settlement"]):
                            context = "regulatory_penalty"
                        elif any(word in sentence_lower for word in ["loss", "write-off", "impairment"]):
                            context = "financial_loss"
                        elif any(word in sentence_lower for word in ["debt", "loan", "borrowing"]):
                            context = "debt_obligation"
                        elif any(word in sentence_lower for word in ["revenue", "sales", "income"]):
                            context = "revenue_impact"
                    
                    company_financials.append({
                        "amount": amount,
                        "context": context,
                        "evidence_sentences": co_occurrence_sentences[:2],
                        "occurrence_count": len(co_occurrence_sentences)
                    })
            
            if company_financials:
                # Calculate total financial exposure
                total_exposure = 0
                for financial in company_financials:
                    amount_str = financial["amount"]
                    # Simple extraction of numeric value
                    numeric_match = re.search(r'\$?(\d+(?:\.\d+)?)', amount_str)
                    if numeric_match:
                        base_value = float(numeric_match.group(1))
                        if 'billion' in amount_str.lower():
                            base_value *= 1000  # Convert to millions
                        elif 'million' in amount_str.lower():
                            base_value *= 1
                        else:
                            base_value /= 1000000  # Assume dollars, convert to millions
                        total_exposure += base_value
                
                relationships.append({
                    "company": company,
                    "financial_impacts": company_financials,
                    "total_financial_exposure_millions": round(total_exposure, 2),
                    "impact_categories": list(set([impact["context"] for impact in company_financials])),
                    "primary_impact_type": max(
                        set([impact["context"] for impact in company_financials]),
                        key=[impact["context"] for impact in company_financials].count
                    ) if company_financials else "general"
                })
        
        return relationships
    
    def _build_risk_network(self, risks: List[Dict], entities: Dict, text: str) -> List[Dict[str, Any]]:
        """Build interconnected risk network"""
        network_nodes = []
        network_links = []
        
        # Add risk nodes
        for risk in risks:
            network_nodes.append({
                "id": risk["type"],
                "type": "risk",
                "score": risk["score"],
                "size": risk["score"] / 10,
                "color": risk.get("color", "#666666")
            })
        
        # Add company nodes
        for company in entities.get("companies", [])[:8]:
            network_nodes.append({
                "id": company,
                "type": "company",
                "size": 20,
                "color": "#4ECDC4"
            })
        
        # Add regulatory nodes
        for regulator in entities.get("regulatory_bodies", [])[:5]:
            network_nodes.append({
                "id": regulator,
                "type": "regulator",
                "size": 25,
                "color": "#FF6B6B"
            })
        
        # Build links based on co-occurrence in sentences
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            # Company-Risk links
            for company in entities.get("companies", [])[:8]:
                for risk in risks:
                    if company in sentence and any(keyword in sentence.lower() for keyword in risk.get("keywords_found", [])):
                        link_id = f"{company}-{risk['type']}"
                        existing_link = next((link for link in network_links if link["id"] == link_id), None)
                        
                        if existing_link:
                            existing_link["value"] += 1
                        else:
                            network_links.append({
                                "id": link_id,
                                "source": company,
                                "target": risk["type"],
                                "value": 1,
                                "type": "company_risk"
                            })
            
            # Company-Regulator links
            for company in entities.get("companies", [])[:8]:
                for regulator in entities.get("regulatory_bodies", [])[:5]:
                    if company in sentence and regulator in sentence:
                        link_id = f"{company}-{regulator}"
                        existing_link = next((link for link in network_links if link["id"] == link_id), None)
                        
                        if existing_link:
                            existing_link["value"] += 1
                        else:
                            network_links.append({
                                "id": link_id,
                                "source": company,
                                "target": regulator,
                                "value": 1,
                                "type": "regulatory_oversight"
                            })
        
        return {
            "nodes": network_nodes,
            "links": network_links,
            "total_connections": len(network_links),
            "network_density": len(network_links) / (len(network_nodes) * (len(network_nodes) - 1)) if len(network_nodes) > 1 else 0
        }
    
    def _generate_relationship_summary(self, relationships: Dict) -> Dict[str, Any]:
        """Generate comprehensive relationship summary"""
        company_rels = relationships["company_relationships"]
        regulatory_rels = relationships["regulatory_relationships"]
        financial_rels = relationships["financial_relationships"]
        
        summary = {
            "total_entities_mapped": len(company_rels) + len(regulatory_rels) + len(financial_rels),
            "company_risk_exposure": {},
            "regulatory_landscape": {},
            "financial_impact_analysis": {}
        }
        
        # Company risk exposure summary
        if company_rels:
            high_exposure_companies = [cr for cr in company_rels if cr["total_risk_exposure"] > 60]
            summary["company_risk_exposure"] = {
                "companies_analyzed": len(company_rels),
                "high_exposure_companies": len(high_exposure_companies),
                "most_exposed_company": max(company_rels, key=lambda x: x["total_risk_exposure"])["company"] if company_rels else "none",
                "dominant_risk_type": max(
                    set([cr["primary_risk"] for cr in company_rels]),
                    key=[cr["primary_risk"] for cr in company_rels].count
                ) if company_rels else "none"
            }
        
        # Regulatory landscape summary
        if regulatory_rels:
            summary["regulatory_landscape"] = {
                "regulatory_bodies_active": len(regulatory_rels),
                "total_companies_under_scrutiny": sum(len(rel["actions"]) for rel in regulatory_rels),
                "primary_regulatory_action": max(
                    set([rel["primary_action_type"] for rel in regulatory_rels]),
                    key=[rel["primary_action_type"] for rel in regulatory_rels].count
                ) if regulatory_rels else "monitoring"
            }
        
        # Financial impact summary
        if financial_rels:
            total_exposure = sum(rel["total_financial_exposure_millions"] for rel in financial_rels)
            summary["financial_impact_analysis"] = {
                "companies_with_financial_impact": len(financial_rels),
                "total_exposure_millions": round(total_exposure, 2),
                "highest_exposure_company": max(financial_rels, key=lambda x: x["total_financial_exposure_millions"])["company"] if financial_rels else "none",
                "most_common_impact_type": max(
                    set([rel["primary_impact_type"] for rel in financial_rels]),
                    key=[rel["primary_impact_type"] for rel in financial_rels].count
                ) if financial_rels else "general"
            }
        
        # Overall relationship complexity
        network = relationships["risk_networks"]
        summary["relationship_complexity"] = {
            "total_nodes": len(network.get("nodes", [])),
            "total_connections": network.get("total_connections", 0),
            "network_density": round(network.get("network_density", 0), 3),
            "complexity_level": "high" if network.get("network_density", 0) > 0.1 else "medium" if network.get("network_density", 0) > 0.05 else "low"
        }
        
        return summary