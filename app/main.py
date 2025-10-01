import streamlit as st

def main():
    st.set_page_config(
        page_title="FinancialRiskRadar",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Hide sidebar completely
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        .stApp {
            margin-left: 0px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🌐 Financial Risk Radar")
    st.markdown("### AI-Powered Financial Risk Analysis Platform")
    
    st.markdown("""
    Welcome to FinancialRiskRadar! Our platform provides comprehensive risk analysis 
    across multiple financial domains. Choose your analysis module below:
    """)
    
    st.markdown("---")
    
    # Four module options in 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        # Module 1: Universal Risk Tagging
        st.subheader("📊 Universal Risk Tagging")
        st.markdown("""
        **Analyze any financial document or website**
        - URL or PDF analysis
        - Balance sheets, income statements
        - News articles, reports
        - General financial risk assessment
        """)
        if st.button("🚀 Open Universal Analyzer", use_container_width=True, key="universal"):
            st.switch_page("pages/1_universal_risk.py")
        
        st.markdown("---")
        
        # Module 2: Bank Monitor
        st.subheader("🏦 Bank Risk Monitor")
        st.markdown("""
        **Live banking sector risk insights**
        - Real-time banking news monitoring
        - Regulatory compliance alerts
        - Credit and default risk analysis
        - Market risk assessment
        """)
        if st.button("📈 Open Bank Monitor", use_container_width=True, key="bank"):
            st.switch_page("pages/2_bank_monitor.py")
    
    with col2:
        # Module 3: Insurance Assessment
        st.subheader("🛡️ Insurance Risk Assessment")
        st.markdown("""
        **Individual insurance risk profiling**
        - Personal risk assessment
        - Fraud detection analysis
        - Premium recommendations
        - Claim risk evaluation
        """)
        if st.button("📋 Open Insurance Assessment", use_container_width=True, key="insurance"):
            st.switch_page("pages/3_insurance_assessment.py")
        
        st.markdown("---")
        
        # Module 4: FinTech Dashboard
        st.subheader("🚀 FinTech Risk Dashboard")
        st.markdown("""
        **Live fintech sector monitoring**
        - Cybersecurity threat intelligence
        - Regulatory change tracking
        - Emerging technology risks
        - Market disruption analysis
        """)
        if st.button("🔍 Open FinTech Dashboard", use_container_width=True, key="fintech"):
            st.switch_page("pages/4_fintech_dashboard.py")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>FinancialRiskRadar • AI-Powered Risk Analysis • Secure • Transparent</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()