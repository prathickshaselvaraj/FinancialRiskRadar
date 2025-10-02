"""
Advanced financial entity extraction
"""
import re
from typing import Dict, List, Tuple

class FinancialEntityExtractor:
    def __init__(self):
        self.company_patterns = [
            r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+(?:Inc|Inc\.|Corp|Corp\.|Corporation|Company|Ltd|Ltd\.|Limited|Bank|Financial|Group|Holdings)\b',
            r'\b(?:Apple|Google|Microsoft|Amazon|Facebook|Tesla|JPMorgan|Goldman Sachs|Bank of America|Wells Fargo|Morgan Stanley|Citigroup)\b'
        ]
        
        self.regulatory_bodies = [
            'SEC', 'Federal Reserve', 'FDIC', 'CFTC', 'OCC', 'FINRA', 'CFPB'
        ]
    
    def extract_all_entities(self, text: str) -> Dict[str, List]:
        """Extract comprehensive financial entities"""
        entities = {
            "companies": [],
            "regulatory_bodies": [],
            "financial_amounts": [],
            "percentages": [],
            "dates": [],
            "people": []
        }
        
        # Extract companies
        for pattern in self.company_patterns:
            matches = re.findall(pattern, text)
            entities["companies"].extend(matches)
        
        # Extract regulatory bodies
        for body in self.regulatory_bodies:
            if body in text:
                entities["regulatory_bodies"].append(body)
        
        # Extract financial amounts with improved patterns
        amount_patterns = [
            r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?',  # $1,000.00
            r'\$\d+(?:\.\d{2})?',  # $100 or $100.50
            r'\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:million|billion|trillion)',  # 1 million, 2.5 billion
            r'\$\d+(?:\.\d{2})?\s*(?:million|billion|trillion)'  # $1 million, $2.5 billion
        ]
        
        for pattern in amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["financial_amounts"].extend(matches)
        
        # Extract percentages
        percentage_patterns = [
            r'\d+(?:\.\d+)?%',  # 15%, 25.5%
            r'\d+(?:\.\d+)?\s+percent',  # 15 percent
            r'\d+(?:\.\d+)?\s+per\s+cent'  # 15 per cent
        ]
        
        for pattern in percentage_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["percentages"].extend(matches)
        
        # Extract dates and time periods
        date_patterns = [
            r'\bQ[1-4]\s*\d{4}\b',  # Q1 2024, Q4 2023
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # 12/31/2024, 31-12-2024
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{4}\b'  # Standalone years
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["dates"].extend(matches)
        
        # Extract people (simple pattern for executives)
        people_patterns = [
            r'(?:CEO|CFO|COO|President)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+),\s+(?:CEO|CFO|COO|President)'
        ]
        
        for pattern in people_patterns:
            matches = re.findall(pattern, text)
            entities["people"].extend(matches)
        
        # Remove duplicates and limit results
        for key in entities:
            entities[key] = list(set(entities[key]))[:8]  # Limit to 8 items each
            
        return entities
    
    def analyze_entity_relationships(self, text: str, entities: Dict) -> List[Tuple]:
        """Analyze relationships between entities"""
        relationships = []
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence_entities = {}
            
            # Check which entities appear in this sentence
            for entity_type, entity_list in entities.items():
                sentence_entities[entity_type] = [
                    entity for entity in entity_list if entity in sentence
                ]
            
            # Create relationships based on co-occurrence
            if len(sentence_entities["companies"]) > 0 and len(sentence_entities["regulatory_bodies"]) > 0:
                relationships.append((
                    sentence_entities["companies"][0],
                    "under_investigation_by",
                    sentence_entities["regulatory_bodies"][0]
                ))
            
            if len(sentence_entities["companies"]) > 0 and len(sentence_entities["financial_amounts"]) > 0:
                relationships.append((
                    sentence_entities["companies"][0],
                    "facing_fines_of",
                    sentence_entities["financial_amounts"][0]
                ))
        
        return relationships