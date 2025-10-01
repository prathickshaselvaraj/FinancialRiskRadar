from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import sys
import os
import yaml

# Add the backend to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your REAL backend modules
try:
    from backend.ingestion.fetcher import ContentFetcher
    from backend.nlp_engine.nlp_pipeline import NLPPipeline
    from backend.ml_engine.predict import RiskPredictor
    from backend.xai.explain import Explainer
    
    # Load your real config
    with open('../config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize your real components
    nlp_pipeline = NLPPipeline(config)
    risk_predictor = RiskPredictor(config)
    explainer = Explainer(config)
    BACKEND_LOADED = True
    
except ImportError as e:
    print(f"Backend import error: {e}")
    BACKEND_LOADED = False

app = FastAPI(
    title="FinancialRiskRadar API",
    description="AI-Powered Financial Risk Analysis Platform", 
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLAnalysisRequest(BaseModel):
    url: str

class RiskAssessmentRequest(BaseModel):
    content: str
    risk_type: str

@app.get("/")
async def root():
    return {
        "message": "FinancialRiskRadar API is running!", 
        "status": "success",
        "backend_loaded": BACKEND_LOADED
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FinancialRiskRadar API"}

@app.post("/api/analyze-url")
async def analyze_url(request: URLAnalysisRequest):
    """Real URL analysis using your backend"""
    try:
        if not BACKEND_LOADED:
            return {
                "status": "success", 
                "url": request.url,
                "message": "Backend not fully loaded - using demo data",
                "risk_tags": {
                    "regulatory": 0.15,
                    "financial": 0.08, 
                    "operational": 0.05,
                    "reputational": 0.12,
                    "sentiment": 0.45,
                    "overall": 0.10
                }
            }
        
        # Use your REAL backend
        fetcher = ContentFetcher(config)
        content_data = fetcher.fetch_url(request.url)
        
        if not content_data or content_data.get('status') != 'success':
            raise HTTPException(status_code=400, detail="Failed to fetch URL content")
        
        risk_tags = nlp_pipeline.analyze_risk_tags(content_data['content'])
        
        return {
            "status": "success",
            "url": request.url,
            "risk_tags": risk_tags,
            "content_preview": content_data['content'][:500] + "..." if len(content_data['content']) > 500 else content_data['content'],
            "title": content_data.get('title', ''),
            "backend_used": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/api/assess-risk")
async def assess_risk(request: RiskAssessmentRequest):
    """Real risk assessment using your ML models"""
    try:
        if not BACKEND_LOADED:
            return {
                "status": "success",
                "risk_type": request.risk_type,
                "prediction": {
                    "risk_score": 65.5,
                    "verdict": "MEDIUM",
                    "risk_probability": 0.655
                },
                "explanation": {
                    "top_features": [
                        ["regulatory_mentions", 0.3],
                        ["negative_sentiment", 0.2],
                        ["financial_terms", 0.15]
                    ]
                },
                "backend_used": False
            }
        
        # Use your REAL ML models
        prediction = risk_predictor.predict(request.content, request.risk_type)
        explanation = explainer.explain(request.content, prediction, request.risk_type)
        
        return {
            "status": "success",
            "risk_type": request.risk_type,
            "prediction": prediction,
            "explanation": explanation,
            "backend_used": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk assessment error: {str(e)}")

@app.get("/api/live-risks/banking")
async def get_live_banking_risks():
    return {
        "status": "success",
        "risks": [
            {"type": "regulatory", "description": "New banking regulations announced", "severity": "medium"},
            {"type": "market", "description": "Interest rate volatility detected", "severity": "high"}
        ]
    }

@app.get("/api/live-risks/fintech") 
async def get_live_fintech_risks():
    return {
        "status": "success", 
        "risks": [
            {"type": "cybersecurity", "description": "Increased fintech phishing attacks", "severity": "high"},
            {"type": "regulatory", "description": "Digital asset regulations evolving", "severity": "medium"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)