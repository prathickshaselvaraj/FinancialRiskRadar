"""
FastAPI main application with modular imports
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modular components
from nlp.financial_parser import FinancialDocumentParser
from nlp.risk_analyzer import FinancialRiskAnalyzer
from nlp.entity_extractor import FinancialEntityExtractor
from nlp.text_processor import FinancialTextProcessor
from data.sec_processor import SECProcessor
from data.news_scraper import FinancialNewsScraper
from data.content_fetcher import ContentFetcher
from analysis.risk_scorer import RiskScorer
from analysis.trend_analyzer import RiskTrendAnalyzer
from analysis.relationship_mapper import RelationshipMapper
from visualization.chart_generator import ChartDataGenerator
from visualization.report_builder import ReportBuilder

# Initialize components
document_parser = FinancialDocumentParser()
risk_analyzer = FinancialRiskAnalyzer()
entity_extractor = FinancialEntityExtractor()
text_processor = FinancialTextProcessor()
sec_processor = SECProcessor()
news_scraper = FinancialNewsScraper()
content_fetcher = ContentFetcher()
risk_scorer = RiskScorer()
trend_analyzer = RiskTrendAnalyzer()
relationship_mapper = RelationshipMapper()
chart_generator = ChartDataGenerator()
report_builder = ReportBuilder()

app = FastAPI(
    title="FinancialRiskRadar API",
    description="Advanced NLP-Powered Financial Risk Analysis Platform",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLAnalysisRequest(BaseModel):
    url: str

class TextAnalysisRequest(BaseModel):
    text: str

class AnalysisOptions(BaseModel):
    include_trends: bool = True
    include_relationships: bool = True
    include_visualizations: bool = True
    generate_report: bool = False

@app.get("/")
async def root():
    return {
        "message": "FinancialRiskRadar Advanced NLP API is running!",
        "status": "success",
        "version": "2.0.0",
        "features": [
            "Advanced financial risk detection",
            "Entity relationship mapping", 
            "Trend analysis and visualization",
            "Comprehensive reporting",
            "Modular NLP pipeline"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "FinancialRiskRadar Advanced API",
        "components_loaded": True
    }

@app.post("/api/analyze-text")
async def analyze_text(request: TextAnalysisRequest, options: AnalysisOptions = None):
    """Comprehensive text analysis with modular NLP pipeline"""
    try:
        if options is None:
            options = AnalysisOptions()
        
        # Step 1: Text Processing
        cleaned_text = text_processor.clean_financial_text(request.text)
        document_structure = document_parser.analyze_document_structure(cleaned_text)
        
        # Step 2: Risk Analysis
        detected_risks = risk_analyzer.analyze_risk_context(cleaned_text)
        overall_risk_score = risk_analyzer.calculate_overall_risk(detected_risks)
        
        # Step 3: Entity Extraction
        entities = entity_extractor.extract_all_entities(cleaned_text)
        
        # Step 4: Advanced Risk Scoring
        risk_scores = risk_scorer.calculate_comprehensive_risk_score(detected_risks, cleaned_text)
        
        # Initialize results
        analysis_results = {
            "timestamp": "2024-10-02T12:00:00Z",  # In production, use actual timestamp
            "document_info": {
                "document_type": document_structure["document_type"],
                "estimated_source": document_structure["estimated_source"],
                "word_count": len(cleaned_text.split()),
                "risk_density": document_structure["risk_density"]
            },
            "risk_scores": risk_scores,
            "entities": entities,
            "detected_risks": detected_risks
        }
        
        # Optional: Trend Analysis
        if options.include_trends:
            trend_analysis = trend_analyzer.analyze_risk_trends(cleaned_text, detected_risks)
            analysis_results["trend_analysis"] = trend_analysis
        
        # Optional: Relationship Mapping
        if options.include_relationships:
            relationships = relationship_mapper.map_entity_relationships(cleaned_text, entities, detected_risks)
            analysis_results["relationships"] = relationships
        
        # Optional: Visualizations
        if options.include_visualizations:
            visualization_data = chart_generator.generate_risk_dashboard_data(analysis_results)
            analysis_results["visualization_data"] = visualization_data
        
        # Optional: Comprehensive Report
        if options.generate_report:
            comprehensive_report = report_builder.generate_comprehensive_report(analysis_results)
            analysis_results["comprehensive_report"] = comprehensive_report
        
        return {
            "status": "success",
            "analysis": analysis_results,
            "text_preview": cleaned_text[:300] + "..." if len(cleaned_text) > 300 else cleaned_text,
            "processing_steps": [
                "Text cleaning and normalization",
                "Document structure analysis", 
                "Risk detection and scoring",
                "Entity extraction",
                "Advanced risk analysis"
            ] + (["Trend analysis"] if options.include_trends else []) +
              (["Relationship mapping"] if options.include_relationships else []) +
              (["Visualization generation"] if options.include_visualizations else []) +
              (["Report generation"] if options.generate_report else [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis error: {str(e)}")

@app.post("/api/analyze-url")
async def analyze_url(request: URLAnalysisRequest, options: AnalysisOptions = None):
    """URL analysis with content fetching and processing"""
    try:
        if options is None:
            options = AnalysisOptions()
        
        # Fetch content from URL
        content_data = content_fetcher.fetch_url_content(request.url)
        
        if content_data["status"] != "success":
            raise HTTPException(status_code=400, detail="Failed to fetch URL content")
        
        # Analyze the fetched content
        text_request = TextAnalysisRequest(text=content_data["content"])
        analysis_results = await analyze_text(text_request, options)
        
        # Enhance with URL-specific data
        analysis_results["url_info"] = {
            "url": request.url,
            "title": content_data["title"],
            "content_type": content_data["content_type"],
            "source_note": content_data.get("note", "")
        }
        
        return analysis_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL analysis error: {str(e)}")

@app.get("/api/risk-categories")
async def get_risk_categories():
    """Get available risk categories and their configurations"""
    return {
        "status": "success",
        "risk_categories": {
            "credit_risk": {
                "description": "Risk of financial default or inability to meet debt obligations",
                "keywords": risk_analyzer.risk_categories["credit_risk"]["keywords"],
                "weight": 0.35,
                "color": "#FF6B6B"
            },
            "market_risk": {
                "description": "Risk from market movements and economic conditions",
                "keywords": risk_analyzer.risk_categories["market_risk"]["keywords"],
                "weight": 0.25,
                "color": "#4ECDC4"
            },
            "operational_risk": {
                "description": "Risk from internal processes, systems, or external events", 
                "keywords": risk_analyzer.risk_categories["operational_risk"]["keywords"],
                "weight": 0.20,
                "color": "#45B7D1"
            },
            "regulatory_risk": {
                "description": "Risk from regulatory changes or legal actions",
                "keywords": risk_analyzer.risk_categories["regulatory_risk"]["keywords"],
                "weight": 0.20,
                "color": "#96CEB4"
            }
        }
    }

@app.get("/api/capabilities")
async def get_capabilities():
    """Get API capabilities and features"""
    return {
        "status": "success",
        "capabilities": {
            "core_nlp": [
                "Financial document parsing",
                "Advanced risk detection",
                "Entity extraction",
                "Text processing and cleaning"
            ],
            "advanced_analysis": [
                "Risk scoring and intensity calculation",
                "Trend analysis and pattern detection", 
                "Relationship mapping",
                "Visualization data generation"
            ],
            "reporting": [
                "Comprehensive risk reports",
                "Executive summaries",
                "Actionable recommendations"
            ],
            "integration": [
                "URL content fetching",
                "SEC filing processing",
                "Financial news analysis"
            ]
        },
        "modules_loaded": [
            "FinancialDocumentParser",
            "FinancialRiskAnalyzer", 
            "FinancialEntityExtractor",
            "FinancialTextProcessor",
            "SECProcessor",
            "FinancialNewsScraper",
            "ContentFetcher",
            "RiskScorer",
            "RiskTrendAnalyzer", 
            "RelationshipMapper",
            "ChartDataGenerator",
            "ReportBuilder"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)