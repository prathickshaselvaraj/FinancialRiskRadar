from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FINANCIAL_RISK_CATEGORIES = {
    "credit_risk": {
        "keywords": ["default", "bankruptcy", "liquidity", "debt", "loan"],
        "color": "#FF6B6B",
        "description": "Risk of financial default"
    },
    "market_risk": {
        "keywords": ["volatility", "recession", "inflation", "interest rates"],
        "color": "#4ECDC4",
        "description": "Risk from market movements"
    },
    "operational_risk": {
        "keywords": ["fraud", "cybersecurity", "data breach"],
        "color": "#45B7D1", 
        "description": "Risk from internal processes"
    },
    "regulatory_risk": {
        "keywords": ["SEC", "investigation", "fines", "regulation"],
        "color": "#96CEB4",
        "description": "Risk from regulatory changes"
    }
}

class URLAnalysisRequest(BaseModel):
    url: str

class TextAnalysisRequest(BaseModel):
    text: str

def analyze_financial_risk(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    risks_detected = []
    
    for risk_type, config in FINANCIAL_RISK_CATEGORIES.items():
        found_keywords = []
        for keyword in config["keywords"]:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        if found_keywords:
            score = min(len(found_keywords) * 25, 100)
            risks_detected.append({
                "type": risk_type,
                "score": score,
                "keywords_found": found_keywords,
                "color": config["color"],
                "description": config["description"],
                "sentence_count": len([s for s in text_lower.split('.') if any(kw in s for kw in found_keywords)])
            })
    
    # Calculate overall score
    overall_score = 0
    if risks_detected:
        overall_score = sum(risk["score"] for risk in risks_detected) / len(risks_detected)
    
    # Simple entity extraction
    companies = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|Corp|Company|Bank)\b', text)
    amounts = re.findall(r'\$\d+(?:\.\d+)?(?:\s+[mb]illion)?', text)
    percentages = re.findall(r'\d+(?:\.\d+)?%', text)
    dates = re.findall(r'\b(?:Q[1-4]\s*\d{4}|\d{4})\b', text)
    
    return {
        "overall_risk_score": round(overall_score, 1),
        "risk_categories": risks_detected,
        "entities_extracted": {
            "companies": list(set(companies))[:5],
            "amounts": list(set(amounts))[:5],
            "percentages": list(set(percentages))[:5],
            "dates": list(set(dates))[:5]
        },
        "text_metrics": {
            "word_count": len(text.split()),
            "sentence_count": len([s for s in text.split('.') if s.strip()]),
            "risk_keywords_total": sum(len(risk["keywords_found"]) for risk in risks_detected)
        }
    }

@app.post("/api/analyze-text")
async def analyze_text(request: TextAnalysisRequest):
    try:
        analysis_result = analyze_financial_risk(request.text)
        
        return {
            "status": "success", 
            "analysis": analysis_result,
            "text_preview": request.text[:200] + "..." if len(request.text) > 200 else request.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/api/analyze-url")
async def analyze_url(request: URLAnalysisRequest):
    try:
        # Simple scraping or return demo data
        demo_text = """
        Apple Inc faces liquidity crisis with $2.3 billion debt due in Q4 2024. 
        SEC investigation may result in $500 million fines for accounting fraud.
        Cybersecurity breach exposed 2 million customer records.
        Market volatility and inflation concerns impact revenue.
        """
        
        analysis_result = analyze_financial_risk(demo_text)
        
        return {
            "status": "success",
            "url": request.url,
            "title": "Financial Risk Analysis",
            "analysis": analysis_result,
            "content_preview": demo_text[:300] + "..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL analysis error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)