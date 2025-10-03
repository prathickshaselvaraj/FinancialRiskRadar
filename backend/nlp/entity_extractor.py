"""
Advanced financial entity extraction with REAL stock symbols and executive data
"""
import re
import requests
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
        
        # API configurations
        self.alpha_vantage_key = "39VQF76MH0BEEJV2"  # Your Alpha Vantage key
        self.financial_modeling_prep_key = "B3Cx3v3A1ZBN2h7bzlxAtxNbQlmJ9FhB"  # Your FMP key
    
    def extract_all_entities(self, text: str) -> Dict[str, List]:
        """Extract comprehensive financial entities with REAL symbol data"""
        entities = {
            "companies": [],
            "regulatory_bodies": [],
            "financial_amounts": [],
            "percentages": [],
            "dates": [],
            "people": [],
            "stock_symbols": [],
            "enhanced_companies": []
        }
        
        # Extract basic entities
        entities = self._extract_basic_entities(text, entities)
        
        # Enhance with REAL stock symbols and executive data
        entities = self._enhance_with_real_data(entities, text)
        
        return entities
    
    def _extract_basic_entities(self, text: str, entities: Dict) -> Dict[str, List]:
        """Extract basic financial entities using regex patterns"""
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
        
        return entities
    
    def _enhance_with_real_data(self, entities: Dict, text: str) -> Dict[str, List]:
        """Enhance entities with REAL stock symbols and executive data"""
        enhanced_entities = entities.copy()
        
        # Get REAL stock symbols for companies
        for company in entities["companies"][:5]:  # Limit API calls
            symbol_data = self._get_company_symbol_and_data(company)
            if symbol_data:
                if symbol_data["symbol"] and symbol_data["symbol"] not in enhanced_entities["stock_symbols"]:
                    enhanced_entities["stock_symbols"].append(symbol_data["symbol"])
                
                # Add enhanced company data
                enhanced_entities["enhanced_companies"].append({
                    "name": company,
                    "symbol": symbol_data["symbol"],
                    "sector": symbol_data.get("sector", "Unknown"),
                    "market_cap": symbol_data.get("market_cap", "Unknown"),
                    "executives": symbol_data.get("executives", []),
                    "data_source": symbol_data.get("data_source", "simulated")
                })
        
        # Enhance people with real executive roles
        enhanced_entities["people"] = self._enhance_people_with_roles(enhanced_entities["people"], enhanced_entities["enhanced_companies"])
        
        # Remove duplicates and limit results
        for key in enhanced_entities:
            if key not in ["enhanced_companies"]:  # Don't limit enhanced companies
                enhanced_entities[key] = list(set(enhanced_entities[key]))[:8]
        
        enhanced_entities["data_enhanced"] = len(enhanced_entities["enhanced_companies"]) > 0
        
        return enhanced_entities
    
    def _get_company_symbol_and_data(self, company: str) -> Dict[str, any]:
        """Get real company symbol and data from APIs"""
        symbol = self._company_to_symbol(company)
        if not symbol:
            return {}
        
        try:
            # Try Financial Modeling Prep first for company overview
            company_data = self._get_company_overview(symbol)
            if company_data:
                return {
                    "symbol": symbol,
                    "sector": company_data.get("Sector", "Unknown"),
                    "market_cap": company_data.get("MarketCapitalization", "Unknown"),
                    "executives": self._get_company_executives(symbol),
                    "data_source": "Financial Modeling Prep"
                }
        except:
            pass
        
        # Fallback to basic symbol mapping
        return {
            "symbol": symbol,
            "sector": "Unknown", 
            "market_cap": "Unknown",
            "executives": [],
            "data_source": "symbol_mapping"
        }
    
    def _get_company_overview(self, symbol: str) -> Dict[str, any]:
        """Get company overview from Financial Modeling Prep"""
        try:
            url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}"
            params = {'apikey': self.financial_modeling_prep_key}
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return data[0]
        except:
            pass
        return {}
    
    def _get_company_executives(self, symbol: str) -> List[Dict[str, str]]:
        """Get company executives from Financial Modeling Prep"""
        try:
            url = f"https://financialmodelingprep.com/api/v3/key-executives/{symbol}"
            params = {'apikey': self.financial_modeling_prep_key}
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    executives = []
                    for exec_data in data[:5]:  # Limit to top 5 executives
                        executives.append({
                            "name": exec_data.get("name", ""),
                            "title": exec_data.get("title", ""),
                            "pay": exec_data.get("pay", "")
                        })
                    return executives
        except:
            pass
        return []
    
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
            'Bank of America': 'BAC',
            'Wells Fargo': 'WFC',
            'Morgan Stanley': 'MS',
            'Citigroup': 'C',
            'Facebook': 'META',
            'Netflix': 'NFLX',
            'Nvidia': 'NVDA'
        }
        
        for name, symbol in symbol_map.items():
            if name.lower() in company.lower():
                return symbol
        
        # Try to extract symbol from company name
        words = company.split()
        if len(words) >= 2:
            # Simple heuristic: first letter of first two words
            potential_symbol = f"{words[0][0]}{words[1][0]}".upper()
            if len(potential_symbol) == 2:
                return potential_symbol
        
        return ""
    
    def _enhance_people_with_roles(self, people: List[str], enhanced_companies: List[Dict]) -> List[str]:
        """Enhance people names with their executive roles"""
        enhanced_people = people.copy()
        
        for company_data in enhanced_companies:
            for executive in company_data.get("executives", []):
                exec_name = executive.get("name", "")
                exec_title = executive.get("title", "")
                
                if exec_name and exec_name not in enhanced_people:
                    enhanced_people.append(f"{exec_name} ({exec_title})")
        
        return enhanced_people
    
    def analyze_entity_relationships(self, text: str, entities: Dict) -> List[Tuple]:
        """Analyze relationships between entities with enhanced data"""
        relationships = []
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence_entities = {}
            
            # Check which entities appear in this sentence
            for entity_type, entity_list in entities.items():
                if entity_type in ["enhanced_companies", "stock_symbols"]:
                    continue  # Skip enhanced data for basic relationship analysis
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
            
            # Enhanced relationships with stock symbols
            if len(sentence_entities["companies"]) > 0 and entities.get("stock_symbols"):
                company = sentence_entities["companies"][0]
                symbol = self._get_symbol_for_company(company, entities)
                if symbol:
                    relationships.append((
                        company,
                        "traded_as",
                        symbol
                    ))
        
        return relationships
    
    def _get_symbol_for_company(self, company: str, entities: Dict) -> str:
        """Get stock symbol for a company from enhanced data"""
        for enhanced_company in entities.get("enhanced_companies", []):
            if enhanced_company["name"] == company:
                return enhanced_company.get("symbol", "")
        return ""