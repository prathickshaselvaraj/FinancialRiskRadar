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
        page_title="Bank Risk Assessment",
        page_icon="🏦",
        layout="wide"
    )
    
    # Header
    st.title("🏦 Bank/Lender Risk Assessment")
    st.markdown("### Specialized analysis for banking institutions")
    
    # Check if analysis data exists
    if ('content_data' not in st.session_state or 
        'risk_tags' not in st.session_state or
        not st.session_state.content_data):
        
        st.error("❌ No analysis data found. Please go back to the main page and analyze a URL first.")
        if st.button("← Back to Home"):
            st.switch_page("app/main.py")
        return
    
    # Perform risk assessment
    with st.spinner("Performing specialized bank risk analysis..."):
        predictor = RiskPredictor(config)
        explainer = Explainer(config)
        
        prediction = predictor.predict(
            st.session_state.content_data['content'], 
            'bank'
        )
        
        explanation = explainer.explain(
            st.session_state.content_data['content'],
            prediction,
            'bank'
        )
    
    # Display results
    st.markdown("---")
    
    # Risk score and verdict
    col1, col2 = st.columns(2)
    
    with col1:
        risk_score = prediction['risk_score']
        st.metric(
            "Overall Risk Score", 
            f"{risk_score:.1f}/100",
            delta=None
        )
    
    with col2:
        verdict = prediction['verdict']
        if verdict == "HIGH":
            icon = "🔴"
            color = "red"
        elif verdict == "MEDIUM":
            icon = "🟡" 
            color = "orange"
        else:
            icon = "🟢"
            color = "green"
        
        st.metric(
            "Risk Verdict", 
            f"{icon} {verdict}",
            delta=None
        )
    
    st.markdown("---")
    st.header("🔍 Key Risk Drivers")
    
    # Display top risk factors
    for feature, impact in explanation['top_features'][:5]:
        # Create a visual indicator for impact
        impact_percent = abs(impact) * 100
        if impact > 0:
            st.write(f"**{feature}**: +{impact_percent:.1f}% risk")
            st.progress(min(impact_percent / 100, 1.0))
        else:
            st.write(f"**{feature}**: {impact_percent:.1f}% risk reduction")
            st.progress(0.1)  # Minimal progress for negative impact
    
    # Risk drivers explanation
    st.markdown("---")
    st.header("📋 Risk Analysis Details")
    
    if explanation.get('risk_drivers'):
        st.subheader("Primary Risk Factors")
        for driver in explanation['risk_drivers']:
            st.write(f"• {driver}")
    
    if explanation.get('key_phrases'):
        st.subheader("Key Risk Indicators")
        for phrase in explanation['key_phrases'][:3]:
            st.write(f"• \"{phrase}\"")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("← Back to Home", use_container_width=True):
            st.switch_page("main.py")

if __name__ == "__main__":
    main()