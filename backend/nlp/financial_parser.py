"""
Advanced financial document structure analysis
"""
import re
from typing import Dict, List, Any

class FinancialDocumentParser:
    def __init__(self):
        self.risk_section_patterns = [
            r'ITEM\s*1A\.?\s*RISK\s*FACTORS([\s\S]*?)(?=ITEM\s*1B|ITEM\s*2|$)',  # SEC 10-K
            r'Risk\s*Factors([\s\S]*?)(?=Business|Properties|Legal|$)',  # Alternative format
            r'PRINCIPAL\s*RISK\s*FACTORS([\s\S]*?)(?=BUSINESS|FINANCIAL|$)'  # Annual reports
        ]
        
        self.section_headers = [
            'credit risk', 'market risk', 'operational risk', 'regulatory risk',
            'liquidity risk', 'interest rate risk', 'currency risk', 'compliance risk'
        ]
    
    def extract_risk_sections(self, text: str) -> Dict[str, str]:
        """Extract structured risk sections from financial documents"""
        risk_sections = {}
        
        # Try to find formal risk factors section
        for pattern in self.risk_section_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                risk_sections['formal_risk_factors'] = match.group(1).strip()
                break
        
        # Extract risk-related paragraphs
        paragraphs = re.split(r'\n\s*\n', text)
        for i, paragraph in enumerate(paragraphs):
            paragraph_lower = paragraph.lower()
            
            # Check if paragraph discusses risks
            risk_indicators = ['risk', 'uncertainty', 'may adversely affect', 'could result in']
            if any(indicator in paragraph_lower for indicator in risk_indicators):
                section_name = f"risk_paragraph_{i+1}"
                risk_sections[section_name] = paragraph.strip()
            
            # Identify specific risk type sections
            for header in self.section_headers:
                if header in paragraph_lower and len(paragraph) > 100:
                    risk_sections[header] = paragraph.strip()
        
        return risk_sections
    
    def analyze_document_structure(self, text: str) -> Dict[str, Any]:
        """Analyze document type and structure"""
        text_lower = text.lower()
        
        structure = {
            'document_type': 'unknown',
            'sections_found': [],
            'risk_density': 0,
            'estimated_source': 'unknown'
        }
        
        # Detect document type
        if 'item 1a' in text_lower and 'sec' in text_lower:
            structure['document_type'] = 'sec_filing'
            structure['estimated_source'] = 'SEC EDGAR'
        elif 'earnings call' in text_lower or 'q&a' in text_lower:
            structure['document_type'] = 'earnings_transcript'
            structure['estimated_source'] = 'Earnings Call'
        elif 'press release' in text_lower or 'announce' in text_lower:
            structure['document_type'] = 'press_release'
            structure['estimated_source'] = 'Company PR'
        elif any(site in text_lower for site in ['reuters', 'bloomberg', 'financial times']):
            structure['document_type'] = 'news_article'
            structure['estimated_source'] = 'Financial News'
        
        # Calculate risk density
        risk_keywords = ['risk', 'uncertain', 'volatility', 'default', 'investigation']
        risk_mentions = sum(1 for keyword in risk_keywords if keyword in text_lower)
        total_words = len(text.split())
        structure['risk_density'] = (risk_mentions / total_words * 100) if total_words > 0 else 0
        
        return structure