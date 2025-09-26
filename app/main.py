import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.ingestion.fetcher import ContentFetcher
from backend.nlp_engine.nlp_pipeline import NLPPipeline
from backend.ml_engine.predict import RiskPredictor
from backend.xai.explain import Explainer
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'risk_tags' not in st.session_state:
        st.session_state.risk_tags = None
    if 'content_data' not in st.session_state:
        st.session_state.content_data = None
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "home"  # home, bank, insurance, fintech

def hide_sidebar():
    """Completely hide the Streamlit sidebar"""
    st.markdown("""
    <style>
        /* Hide the entire sidebar */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Adjust main content to full width */
        .stApp {
            margin-left: 0px !important;
            margin-right: 0px !important;
            padding: 0px !important;
        }
        
        /* Hide the sidebar toggle button */
        .stApp > header {
            display: none !important;
        }
        
        /* Remove any sidebar-related padding */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Add this CSS for better button styling
def add_custom_css():
    st.markdown("""
    <style>
    .big-button {
        height: 120px !important;
        font-size: 18px !important;
        padding: 20px !important;
    }
    .risk-selection {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def show_home_view():
    """Show the home page with URL input"""
    add_custom_css()
    
    st.title("🌐 FinancialRiskRadar")
    st.markdown("### AI-Powered Financial Risk Assessment Platform")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 Analyze Financial Content")
        
        # URL input and analyze button (same as before)
        url = st.text_input(
            "Enter URL (Annual Report, News Article, etc.):",
            placeholder="https://www.example.com/annual-report-2023",
            key="url_input"
        )
        
        if st.button("🔍 Analyze Content", type="primary", use_container_width=True):
            if url:
                with st.spinner("Fetching and analyzing content..."):
                    fetcher = ContentFetcher(config)
                    content_data = fetcher.fetch_url(url)
                    
                    if content_data and content_data.get('status') == 'success':
                        nlp_pipeline = NLPPipeline(config)
                        risk_tags = nlp_pipeline.analyze_risk_tags(content_data['content'])
                        
                        st.session_state.content_data = content_data
                        st.session_state.risk_tags = risk_tags
                        st.session_state.analysis_complete = True
                        st.success("✅ Content analysis complete! Select a risk perspective below.")
                    else:
                        st.error("❌ Failed to fetch content from the provided URL.")
            else:
                st.warning("⚠️ Please enter a valid URL.")
    
    with col2:
        st.header("ℹ️ How It Works")
        st.info("""
        1. **Enter URL** - Provide financial content
        2. **Analyze** - Get risk categorization  
        3. **Select Perspective** - Choose institution type
        """)
    
    if st.session_state.analysis_complete and st.session_state.risk_tags:
        # 🎯 PROMINENT RISK SELECTION SECTION
        st.markdown("---")
        
        # Styled container for risk selection
        st.markdown("""
        <div class='risk-selection'>
            <h2 style='color: white; text-align: center;'>🎯 Select Risk Perspective</h2>
            <p style='color: white; text-align: center;'>Choose your institution type for specialized analysis:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Large prominent buttons
        col1, col2, col3 = st.columns(3)
        
        button_style = """
        <style>
        .stButton > button {
            height: 100px;
            font-size: 16px;
            font-weight: bold;
        }
        </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)
        
        with col1:
            if st.button("🏦 **BANK/LENDER**\nCredit & Default Risk", use_container_width=True, key="bank_btn"):
                st.session_state.current_view = "bank"
                st.rerun()
        
        with col2:
            if st.button("🛡️ **INSURANCE**\nClaim Fraud & Integrity", use_container_width=True, key="insurance_btn"):
                st.session_state.current_view = "insurance"
                st.rerun()
        
        with col3:
            if st.button("🚀 **FINTECH**\nCyber Threat Analysis", use_container_width=True, key="fintech_btn"):
                st.session_state.current_view = "fintech"
                st.rerun()
        
        # Preliminary analysis below
        st.markdown("---")
        st.header("📋 Preliminary Risk Analysis")
        
        tags = st.session_state.risk_tags
        cols = st.columns(6)
        metrics = [
            ('Regulatory', tags.get('regulatory', 0)),
            ('Financial', tags.get('financial', 0)),
            ('Operational', tags.get('operational', 0)),
            ('Reputational', tags.get('reputational', 0)),
            ('Sentiment', tags.get('sentiment', 0)),
            ('Overall', tags.get('overall', 0))
        ]
        
        for idx, (label, value) in enumerate(metrics):
            with cols[idx]:
                st.metric(label, f"{value:.1%}")

def show_risk_view(risk_type):
    """Show risk assessment results for a specific risk type"""
    risk_titles = {
        "bank": "🏦 Bank/Lender Risk Assessment",
        "insurance": "🛡️ Insurance Risk Assessment",
        "fintech": "🚀 FinTech Risk Assessment"
    }
    
    risk_descriptions = {
        "bank": "Specialized analysis for banking institutions focusing on credit and default risk",
        "insurance": "Specialized analysis for insurance companies focusing on claim fraud and integrity risk", 
        "fintech": "Specialized analysis for fintech startups focusing on emerging cyber threat severity"
    }
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_view = "home"
        st.rerun()
    
    st.title(risk_titles[risk_type])
    st.markdown(f"### {risk_descriptions[risk_type]}")
    
    # Check if analysis data exists
    if not st.session_state.analysis_complete:
        st.error("❌ No analysis data found. Please go back to the home page and analyze a URL first.")
        return
    
    # Perform risk assessment
    with st.spinner(f"Performing specialized {risk_type} risk analysis..."):
        predictor = RiskPredictor(config)
        explainer = Explainer(config)
        
        prediction = predictor.predict(
            st.session_state.content_data['content'], 
            risk_type
        )
        
        explanation = explainer.explain(
            st.session_state.content_data['content'],
            prediction,
            risk_type
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
    
    # Show content preview
    st.markdown("---")
    with st.expander("📄 View Analyzed Content Preview"):
        content_preview = st.session_state.content_data['content'][:500] + "..." if len(st.session_state.content_data['content']) > 500 else st.session_state.content_data['content']
        st.text_area("Content Preview", content_preview, height=150, disabled=True)

def main():
    st.set_page_config(
        page_title="FinancialRiskRadar",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Completely hide sidebar
    hide_sidebar()
    
    initialize_session_state()
    
    # Show appropriate view based on current state
    if st.session_state.current_view == "home":
        show_home_view()
    elif st.session_state.current_view == "bank":
        show_risk_view("bank")
    elif st.session_state.current_view == "insurance":
        show_risk_view("insurance")
    elif st.session_state.current_view == "fintech":
        show_risk_view("fintech")

if __name__ == "__main__":
    main()