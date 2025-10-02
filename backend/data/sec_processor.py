"""
SEC filing specific processing and analysis
"""
import re
from typing import Dict, List, Any
from datetime import datetime

class SECProcessor:
    def __init__(self):
        self.filing_types = {
            '10-K': 'Annual Report',
            '10-Q': 'Quarterly Report', 
            '8-K': 'Current Report',
            'S-1': 'Registration Statement'
        }
        
        self.standard_sections = {
            'item_1a': 'Risk Factors',
            'item_7': 'Management Discussion',
            'item_7a': 'Quantitative Qualitative',
            'item_8': 'Financial Statements'
        }
    
    def identify_filing_type(self, text: str) -> Dict[str, str]:
        """Identify SEC filing type and extract metadata"""
        text_lower = text.lower()
        
        filing_info = {
            'filing_type': 'unknown',
            'company_name': 'unknown',
            'filing_date': 'unknown',
            'fiscal_year': 'unknown'
        }
        
        # Identify filing type
        for filing_code, filing_name in self.filing_types.items():
            if filing_code.lower() in text_lower:
                filing_info['filing_type'] = filing_name
                break
        
        # Extract company name (simplified pattern)
        company_match = re.search(r'COMPANY\s+CONFORMED\s+NAME:\s*([^\n]+)', text, re.IGNORECASE)
        if company_match:
            filing_info['company_name'] = company_match.group(1).strip()
        else:
            # Fallback: look for common company patterns
            company_pattern = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+(?:Inc|Corp|Corporation|Company))\b'
            companies = re.findall(company_pattern, text)
            if companies:
                filing_info['company_name'] = companies[0]
        
        # Extract filing date
        date_match = re.search(r'FILED\s+AS\s+OF\s+DATE:\s*(\d{8})', text, re.IGNORECASE)
        if date_match:
            date_str = date_match.group(1)
            try:
                filing_date = datetime.strptime(date_str, '%Y%m%d')
                filing_info['filing_date'] = filing_date.strftime('%Y-%m-%d')
                filing_info['fiscal_year'] = str(filing_date.year)
            except ValueError:
                filing_info['filing_date'] = date_str
        
        return filing_info
    
    def extract_standard_sections(self, text: str) -> Dict[str, str]:
        """Extract standard sections from SEC filings"""
        sections = {}
        
        # Item 1A - Risk Factors
        risk_match = re.search(r'ITEM\s*1A\.?\s*RISK\s*FACTORS([\s\S]*?)(?=ITEM\s*1B|ITEM\s*2|$)', text, re.IGNORECASE)
        if risk_match:
            sections['risk_factors'] = risk_match.group(1).strip()
        
        # Item 7 - MD&A
        mda_match = re.search(r'ITEM\s*7\.?\s*MANAGEMENT[\'\s]?S\s*DISCUSSION([\s\S]*?)(?=ITEM\s*7A|ITEM\s*8|$)', text, re.IGNORECASE)
        if mda_match:
            sections['management_discussion'] = mda_match.group(1).strip()
        
        # Item 7A - Quantitative Qualitative
        qq_match = re.search(r'ITEM\s*7A\.?\s*QUANTITATIVE([\s\S]*?)(?=ITEM\s*8|$)', text, re.IGNORECASE)
        if qq_match:
            sections['quantitative_qualitative'] = qq_match.group(1).strip()
        
        return sections
    
    def analyze_risk_factors_structure(self, risk_factors_text: str) -> Dict[str, Any]:
        """Analyze the structure and content of risk factors section"""
        if not risk_factors_text:
            return {}
        
        # Split into individual risk factors
        risk_items = re.split(r'\n\s*\d+\.\s*', risk_factors_text)
        risk_items = [item.strip() for item in risk_items if item.strip()]
        
        analysis = {
            'total_risk_factors': len(risk_items),
            'risk_categories': {},
            'avg_risk_length': 0,
            'risk_titles': []
        }
        
        # Analyze each risk factor
        total_length = 0
        for i, risk_item in enumerate(risk_items):
            if not risk_item:
                continue
                
            # Extract risk title (first sentence or line)
            lines = risk_item.split('\n')
            title = lines[0].strip() if lines else risk_item[:100] + '...'
            analysis['risk_titles'].append(title)
            
            # Calculate length
            risk_length = len(risk_item.split())
            total_length += risk_length
            
            # Categorize by common risk types
            risk_lower = risk_item.lower()
            if any(word in risk_lower for word in ['market', 'economic', 'volatility']):
                analysis['risk_categories']['market_risk'] = analysis['risk_categories'].get('market_risk', 0) + 1
            elif any(word in risk_lower for word in ['credit', 'debt', 'liquidity', 'default']):
                analysis['risk_categories']['credit_risk'] = analysis['risk_categories'].get('credit_risk', 0) + 1
            elif any(word in risk_lower for word in ['operational', 'cyber', 'system', 'process']):
                analysis['risk_categories']['operational_risk'] = analysis['risk_categories'].get('operational_risk', 0) + 1
            elif any(word in risk_lower for word in ['regulatory', 'legal', 'compliance', 'investigation']):
                analysis['risk_categories']['regulatory_risk'] = analysis['risk_categories'].get('regulatory_risk', 0) + 1
        
        analysis['avg_risk_length'] = total_length / len(risk_items) if risk_items else 0
        
        return analysis
    
    def calculate_risk_density(self, text: str, section: str = None) -> float:
        """Calculate risk mention density in text or specific section"""
        if section:
            # Extract specific section first
            sections = self.extract_standard_sections(text)
            analysis_text = sections.get(section, '')
        else:
            analysis_text = text
        
        if not analysis_text:
            return 0.0
        
        risk_keywords = [
            'risk', 'uncertain', 'volatility', 'default', 'may adversely', 
            'could result', 'potential loss', 'exposure', 'vulnerability'
        ]
        
        words = analysis_text.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        risk_mentions = sum(1 for word in words if any(keyword in word for keyword in risk_keywords))
        
        return (risk_mentions / total_words) * 100  # Return as percentage