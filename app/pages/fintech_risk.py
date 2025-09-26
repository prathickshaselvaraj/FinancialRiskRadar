import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.ml_engine.predict import RiskPredictor
from backend.xai.explain import Explainer
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def main():
    st.set_page_config(
        page_title="FinTech Risk Assessment",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 FinTech Risk Assessment")
    st.markdown("### Specialized analysis for financial technology companies")
    
    # Check if analysis data exists
    if ('content_data' not in st.session_state or 
        'risk_tags' not in st.session_state or
        not st.session_state.content_data):
        
        st.error("❌ No analysis data found. Please go back to the main page and analyze a URL first.")
        if st.button("← Back to Home"):
            st.switch_page("app/main.py")
        return
    
    # Perform risk assessment
    with st.spinner("Performing specialized fintech risk analysis..."):
        predictor = RiskPredictor(config)
        explainer = Explainer(config)
        
        prediction = predictor.predict(
            st.session_state.content_data['content'], 
            'fintech'
        )
        
        explanation = explainer.explain(
            st.session_state.content_data['content'],
            prediction,
            'fintech'
        )
    
    # Display results
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        risk_score = prediction['risk_score']
        st.metric("Overall Risk Score", f"{risk_score:.1f}/100")
    
    with col2:
        verdict = prediction['verdict']
        icon = "🔴" if verdict == "HIGH" else "🟡" if verdict == "MEDIUM" else "🟢"
        st.metric("Risk Verdict", f"{icon} {verdict}")
    
    st.markdown("---")
    st.header("🔍 Key Risk Drivers")
    
    for feature, impact in explanation['top_features'][:5]:
        impact_percent = abs(impact) * 100
        if impact > 0:
            st.write(f"**{feature}**: +{impact_percent:.1f}% risk")
            st.progress(min(impact_percent / 100, 1.0))
        else:
            st.write(f"**{feature}**: {impact_percent:.1f}% risk reduction")
            st.progress(0.1)
    
    # Navigation
    st.markdown("---")
    if st.button("← Back to Home"):
        st.switch_page("main.py")

if __name__ == "__main__":
    main()