"""
SEC filing specific processing and analysis
"""
import re
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import pandas as pd

@dataclass
class FilingMetadata:
    """Data class for SEC filing metadata"""
    filing_type: str
    company_name: str
    filing_date: str
    fiscal_year: str
    cik: str
    accession_number: str
    period_end: str

class SECProcessor:
    def __init__(self, edgar_api_key: str = None):
        self.filing_types = {
            '10-K': 'Annual Report',
            '10-Q': 'Quarterly Report', 
            '8-K': 'Current Report',
            'S-1': 'Registration Statement',
            'DEF 14A': 'Proxy Statement',
            '20-F': 'Foreign Annual Report'
        }
        
        self.standard_sections = {
            'item_1a': 'Risk Factors',
            'item_7': 'Management Discussion',
            'item_7a': 'Quantitative Qualitative',
            'item_8': 'Financial Statements'
        }
        
        self.edgar_api_key = edgar_api_key
        self.edgar_base_url = "https://data.sec.gov/api/xbrl"
        
    # EDGAR API METHODS
    def get_company_facts(self, cik: str) -> Optional[Dict]:
        """Get company facts from SEC EDGAR API"""
        try:
            headers = {
                'User-Agent': 'Company Analysis Tool contact@example.com',
                'Accept': 'application/json'
            }
            
            if self.edgar_api_key:
                headers['Authorization'] = f'Bearer {self.edgar_api_key}'
            
            url = f"{self.edgar_base_url}/companyfacts/CIK{cik.zfill(10)}.json"
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching company facts: {e}")
            return None
    
    def get_submissions(self, cik: str) -> Optional[Dict]:
        """Get company submissions from SEC EDGAR API"""
        try:
            headers = {
                'User-Agent': 'Company Analysis Tool contact@example.com',
                'Accept': 'application/json'
            }
            
            url = f"{self.edgar_base_url}/submissions/CIK{cik.zfill(10)}.json"
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching submissions: {e}")
            return None
    
    def search_filings(self, company_name: str, filing_type: str = None) -> List[Dict]:
        """Search for company filings by name and type"""
        try:
            # Using SEC's company ticker API as a search proxy
            headers = {'User-Agent': 'Company Analysis Tool contact@example.com'}
            url = "https://www.sec.gov/files/company_tickers.json"
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            companies = response.json()
            results = []
            
            for key, company in companies.items():
                if company_name.lower() in company['title'].lower():
                    results.append({
                        'cik': str(company['cik_str']).zfill(10),
                        'name': company['title'],
                        'ticker': company['ticker']
                    })
            
            return results
        except Exception as e:
            print(f"Error searching filings: {e}")
            return []
    
    # ENHANCED TEXT PROCESSING METHODS
    def identify_filing_type(self, text: str) -> FilingMetadata:
        """Identify SEC filing type and extract metadata with enhanced parsing"""
        text_lower = text.lower()
        
        filing_info = FilingMetadata(
            filing_type='unknown',
            company_name='unknown',
            filing_date='unknown',
            fiscal_year='unknown',
            cik='unknown',
            accession_number='unknown',
            period_end='unknown'
        )
        
        # Enhanced filing type identification
        for filing_code, filing_name in self.filing_types.items():
            pattern = rf'{re.escape(filing_code)}[\s\-]*(?:\(|\))'
            if re.search(pattern, text, re.IGNORECASE):
                filing_info.filing_type = filing_name
                break
        
        # Extract CIK (Central Index Key)
        cik_match = re.search(r'CENTRAL\s+INDEX\s+KEY:\s*(\d+)', text, re.IGNORECASE)
        if not cik_match:
            cik_match = re.search(r'CIK:\s*(\d+)', text, re.IGNORECASE)
        if cik_match:
            filing_info.cik = cik_match.group(1).zfill(10)
        
        # Extract accession number
        accession_match = re.search(r'ACCESSION\s+NUMBER:\s*([^\s]+)', text, re.IGNORECASE)
        if accession_match:
            filing_info.accession_number = accession_match.group(1)
        
        # Enhanced company name extraction
        company_match = re.search(r'COMPANY\s+CONFORMED\s+NAME:\s*([^\n]+)', text, re.IGNORECASE)
        if company_match:
            filing_info.company_name = company_match.group(1).strip()
        else:
            # Multiple fallback patterns
            patterns = [
                r'^\s*([A-Z][A-Z\s&]+(?:INC|CORP|CORPORATION|COMPANY|LTD)\.?)',
                r'\(Name\s+of\s+Registrant[^)]+\)\s*([A-Z][^.\n]+)'
            ]
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    filing_info.company_name = match.group(1).strip()
                    break
        
        # Enhanced date extraction
        date_patterns = [
            (r'FILED\s+AS\s+OF\s+DATE:\s*(\d{8})', '%Y%m%d'),
            (r'CONFORMED\s+PERIOD\s+OF\s+REPORT:\s*(\d{8})', '%Y%m%d'),
            (r'FILING\s+DATE:\s*(\d{4}-\d{2}-\d{2})', '%Y-%m-%d')
        ]
        
        for pattern, date_format in date_patterns:
            date_match = re.search(pattern, text, re.IGNORECASE)
            if date_match:
                try:
                    filing_date = datetime.strptime(date_match.group(1), date_format)
                    filing_info.filing_date = filing_date.strftime('%Y-%m-%d')
                    filing_info.fiscal_year = str(filing_date.year)
                    break
                except ValueError:
                    continue
        
        return filing_info
    
    def extract_financial_metrics(self, text: str) -> Dict[str, Any]:
        """Extract key financial metrics from filing text"""
        metrics = {}
        
        # Revenue patterns
        revenue_patterns = [
            r'revenue\s*[\$]?\s*([\d,]+(?:\.\d{2})?)\s*million',
            r'total\s+revenue\s*[\$]?\s*([\d,]+(?:\.\d{2})?)',
            r'revenue.*?\$(\d+(?:,\d+)*(?:\.\d{2})?)'
        ]
        
        for pattern in revenue_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Take the first match and convert to numeric
                revenue_str = matches[0].replace(',', '')
                try:
                    if 'million' in pattern.lower():
                        metrics['revenue'] = float(revenue_str) * 1_000_000
                    else:
                        metrics['revenue'] = float(revenue_str)
                    break
                except ValueError:
                    continue
        
        # Net income patterns
        income_patterns = [
            r'net\s+income\s*[\$]?\s*([\d,]+(?:\.\d{2})?)\s*million',
            r'net\s+loss\s*[\$]?\s*([\d,]+(?:\.\d{2})?)'
        ]
        
        for pattern in income_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                income_str = matches[0].replace(',', '')
                try:
                    if 'million' in pattern.lower():
                        metrics['net_income'] = float(income_str) * 1_000_000
                    else:
                        metrics['net_income'] = float(income_str)
                    break
                except ValueError:
                    continue
        
        return metrics
    
    def analyze_management_discussion(self, mda_text: str) -> Dict[str, Any]:
        """Perform detailed analysis of Management Discussion & Analysis section"""
        if not mda_text:
            return {}
        
        analysis = {
            'forward_looking_statements': 0,
            'key_business_drivers': [],
            'challenges_mentioned': [],
            'word_count': len(mda_text.split()),
            'sentence_count': len(re.findall(r'[.!?]+', mda_text)),
            'readability_score': 0
        }
        
        # Count forward-looking statements
        forward_keywords = [
            'expect', 'anticipate', 'believe', 'estimate', 'intend', 'plan',
            'project', 'will', 'should', 'could', 'may', 'might'
        ]
        
        for keyword in forward_keywords:
            analysis['forward_looking_statements'] += len(
                re.findall(rf'\b{keyword}\b', mda_text, re.IGNORECASE)
            )
        
        # Extract business drivers
        driver_patterns = [
            r'increase\s+in\s+([^.,]+)',
            r'growth\s+in\s+([^.,]+)',
            r'improvement\s+in\s+([^.,]+)'
        ]
        
        for pattern in driver_patterns:
            drivers = re.findall(pattern, mda_text, re.IGNORECASE)
            analysis['key_business_drivers'].extend([d.strip() for d in drivers])
        
        # Extract challenges
        challenge_patterns = [
            r'challenge[s]?\s+in\s+([^.,]+)',
            r'difficulties\s+in\s+([^.,]+)',
            r'decline\s+in\s+([^.,]+)'
        ]
        
        for pattern in challenge_patterns:
            challenges = re.findall(pattern, mda_text, re.IGNORECASE)
            analysis['challenges_mentioned'].extend([c.strip() for c in challenges])
        
        # Calculate basic readability (simplified)
        avg_sentence_length = analysis['word_count'] / max(analysis['sentence_count'], 1)
        analysis['readability_score'] = max(0, 100 - avg_sentence_length)
        
        return analysis
    
    def generate_filing_summary(self, text: str) -> Dict[str, Any]:
        """Generate comprehensive filing summary"""
        metadata = self.identify_filing_type(text)
        sections = self.extract_standard_sections(text)
        financial_metrics = self.extract_financial_metrics(text)
        
        summary = {
            'metadata': metadata.__dict__,
            'section_analysis': {},
            'risk_analysis': {},
            'financial_metrics': financial_metrics
        }
        
        # Analyze each section
        for section_name, section_text in sections.items():
            if section_name == 'risk_factors':
                summary['risk_analysis'] = self.analyze_risk_factors_structure(section_text)
            elif section_name == 'management_discussion':
                summary['section_analysis']['mda_analysis'] = self.analyze_management_discussion(section_text)
            
            # Calculate risk density for each section
            summary['section_analysis'][f'{section_name}_risk_density'] = self.calculate_risk_density(
                section_text if section_text else text, None
            )
        
        # Overall risk assessment
        summary['overall_risk_density'] = self.calculate_risk_density(text, None)
        
        return summary

    # The original methods remain the same but enhanced with better error handling
    def extract_standard_sections(self, text: str) -> Dict[str, str]:
        """Extract standard sections from SEC filings with improved patterns"""
        sections = {}
        
        # Enhanced patterns for better section extraction
        section_patterns = {
            'risk_factors': r'ITEM\s*1A\.?\s*RISK\s*FACTORS\s*([\s\S]*?)(?=ITEM\s*1B\b|ITEM\s*2\b|\bUNITED\s+STATES\b|$)',
            'management_discussion': r'ITEM\s*7\.?\s*MANAGEMENT[\'\s]?S\s*DISCUSSION\s*([\s\S]*?)(?=ITEM\s*7A\b|ITEM\s*8\b|$)',
            'quantitative_qualitative': r'ITEM\s*7A\.?\s*QUANTITATIVE\s*([\s\S]*?)(?=ITEM\s*8\b|$)',
            'financial_statements': r'ITEM\s*8\.?\s*FINANCIAL\s*STATEMENTS\s*([\s\S]*?)(?=ITEM\s*9\b|$)'
        }
        
        for section_key, pattern in section_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[section_key] = self.clean_section_text(match.group(1))
        
        return sections
    
    def clean_section_text(self, text: str) -> str:
        """Clean extracted section text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Remove table of contents references
        text = re.sub(r'\(See\s+Table\s+of\s+Contents\)', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def analyze_risk_factors_structure(self, risk_factors_text: str) -> Dict[str, Any]:
        """Enhanced risk factors analysis"""
        if not risk_factors_text:
            return {}
        
        # Improved risk factor splitting
        risk_items = re.split(r'\n\s*\d+\.\s*|\n\s*[•\-]\s*', risk_factors_text)
        risk_items = [item.strip() for item in risk_items if len(item.strip()) > 50]  # Filter very short items
        
        analysis = {
            'total_risk_factors': len(risk_items),
            'risk_categories': {},
            'avg_risk_length': 0,
            'risk_titles': [],
            'word_count': len(risk_factors_text.split()),
            'unique_risk_keywords': set()
        }
        
        # Enhanced risk categorization
        risk_categories = {
            'market_risk': ['market', 'economic', 'volatility', 'competition', 'price'],
            'credit_risk': ['credit', 'debt', 'liquidity', 'default', 'borrowing'],
            'operational_risk': ['operational', 'cyber', 'system', 'process', 'supply chain'],
            'regulatory_risk': ['regulatory', 'legal', 'compliance', 'investigation', 'lawsuit'],
            'technology_risk': ['technology', 'innovation', 'obsolescence', 'research', 'development'],
            'financial_risk': ['financial', 'revenue', 'profit', 'margin', 'cost']
        }
        
        total_length = 0
        risk_keywords = set()
        
        for risk_item in risk_items:
            if not risk_item:
                continue
                
            # Extract risk title (first sentence)
            first_sentence = re.split(r'[.!?]', risk_item)[0]
            analysis['risk_titles'].append(first_sentence[:200])  # Limit title length
            
            # Calculate length
            risk_length = len(risk_item.split())
            total_length += risk_length
            
            # Categorize risk
            risk_lower = risk_item.lower()
            for category, keywords in risk_categories.items():
                if any(keyword in risk_lower for keyword in keywords):
                    analysis['risk_categories'][category] = analysis['risk_categories'].get(category, 0) + 1
                    risk_keywords.update(keywords)
            
            # Extract unique risk keywords
            words = set(risk_lower.split())
            risk_keywords.update(words)
        
        analysis['avg_risk_length'] = total_length / len(risk_items) if risk_items else 0
        analysis['unique_risk_keywords'] = list(risk_keywords)
        
        return analysis
    
    def calculate_risk_density(self, text: str, section: str = None) -> float:
        """Enhanced risk density calculation"""
        if section:
            sections = self.extract_standard_sections(text)
            analysis_text = sections.get(section, '')
        else:
            analysis_text = text
        
        if not analysis_text:
            return 0.0
        
        # Expanded risk keywords
        risk_keywords = [
            'risk', 'uncertain', 'volatility', 'default', 'may adversely', 
            'could result', 'potential loss', 'exposure', 'vulnerability',
            'challenge', 'threat', 'adverse', 'negative impact', 'uncertainty',
            'fluctuation', 'downturn', 'recession', 'crisis', 'failure'
        ]
        
        words = analysis_text.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        risk_mentions = sum(1 for word in words if any(keyword in word for keyword in risk_keywords))
        
        return (risk_mentions / total_words) * 100

# Usage example
if __name__ == "__main__":
    # Initialize processor with optional API key
    processor = SECProcessor(edgar_api_key="your_api_key_here")
    
    # Example usage
    with open('sec_filing.txt', 'r', encoding='utf-8') as file:
        filing_text = file.read()
    
    # Generate comprehensive analysis
    summary = processor.generate_filing_summary(filing_text)
    
    print("Filing Analysis Summary:")
    print(json.dumps(summary, indent=2, default=str))