import React, { useState } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('universal');
  const [url, setUrl] = useState('');
  const [text, setText] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  // Sample financial text for demo
  const sampleText = `Apple Inc. faces potential liquidity concerns amid market volatility. 
  The SEC investigation into accounting practices may result in significant fines exceeding $2.3 million. 
  Cybersecurity breaches have exposed customer data, leading to operational disruptions. 
  The company's debt burden has increased by 15% year-over-year, raising default risks. 
  Q4 2024 projections show continued market pressure and potential recession impacts.`;

  const analyzeUrl = async () => {
    if (!url) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/analyze-url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Analysis failed. Please check the URL and try again.');
    }
    setLoading(false);
  };

  const analyzeText = async () => {
    if (!text) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/analyze-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Analysis failed. Please try again.');
    }
    setLoading(false);
  };

  const loadSample = () => {
    setText(sampleText);
  };

  const RiskScoreGauge = ({ score, size = 120 }) => {
    const radius = size / 2 - 10;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (score / 100) * circumference;
    
    const getRiskColor = (score) => {
      if (score < 30) return '#4CAF50';
      if (score < 70) return '#FF9800';
      return '#F44336';
    };

    return (
      <div className="risk-gauge">
        <svg width={size} height={size} className="gauge-svg">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#e0e0e0"
            strokeWidth="8"
            fill="none"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={getRiskColor(score)}
            strokeWidth="8"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            transform={`rotate(-90 ${size / 2} ${size / 2})`}
            strokeLinecap="round"
          />
          <text
            x="50%"
            y="50%"
            textAnchor="middle"
            dy="0.3em"
            fontSize="20"
            fontWeight="bold"
            fill={getRiskColor(score)}
          >
            {score}%
          </text>
        </svg>
        <div className="gauge-label">Overall Risk</div>
      </div>
    );
  };

  const RiskCategoryCard = ({ risk }) => {
    if (!risk) return null;
    
    return (
      <div className="risk-category-card" style={{ borderLeft: `4px solid ${risk.color || '#666'}` }}>
        <div className="risk-header">
          <h4>{(risk.type || '').replace('_', ' ').toUpperCase()}</h4>
          <span className="risk-score" style={{ color: risk.color || '#666' }}>
            {risk.score || 0}%
          </span>
        </div>
        <p className="risk-description">{risk.description || 'Risk category'}</p>
        <div className="keywords-list">
          {(risk.keywords_found || []).map((keyword, idx) => (
            <span key={idx} className="keyword-tag">{keyword}</span>
          ))}
        </div>
        <div className="risk-metrics">
          <span>📝 {risk.sentence_count || 0} sentences</span>
          <span>🔑 {(risk.keywords_found || []).length} keywords</span>
        </div>
      </div>
    );
  };

  const EntitySection = ({ entities }) => {
  if (!entities) return null;
  
  return (
    <div className="entities-section" style={{color: '#000000'}}>
      <h3 style={{color: '#000000'}}>📊 Entities Extracted</h3>
      <div className="entities-grid">
        <div className="entity-category">
          <h4 style={{color: '#000000'}}>🏢 Companies</h4>
          {entities.companies && entities.companies.length > 0 ? (
            entities.companies.map((company, idx) => (
              <div key={idx} className="entity-item" style={{color: '#000000', backgroundColor: '#f8f9fa'}}>
                {company}
              </div>
            ))
          ) : (
            <div className="no-entities" style={{color: '#000000'}}>No companies detected</div>
          )}
        </div>
        
        <div className="entity-category">
          <h4 style={{color: '#000000'}}>💰 Financials</h4>
          {entities.amounts && entities.amounts.length > 0 ? (
            entities.amounts.map((amount, idx) => (
              <div key={idx} className="entity-item" style={{color: '#000000', backgroundColor: '#f8f9fa'}}>
                {amount}
              </div>
            ))
          ) : (
            <div className="no-entities" style={{color: '#000000'}}>No amounts detected</div>
          )}
        </div>
        
        <div className="entity-category">
          <h4 style={{color: '#000000'}}>📈 Percentages</h4>
          {entities.percentages && entities.percentages.length > 0 ? (
            entities.percentages.map((percent, idx) => (
              <div key={idx} className="entity-item" style={{color: '#000000', backgroundColor: '#f8f9fa'}}>
                {percent}
              </div>
            ))
          ) : (
            <div className="no-entities" style={{color: '#000000'}}>No percentages detected</div>
          )}
        </div>
        
        <div className="entity-category">
          <h4 style={{color: '#000000'}}>📅 Dates</h4>
          {entities.dates && entities.dates.length > 0 ? (
            entities.dates.map((date, idx) => (
              <div key={idx} className="entity-item" style={{color: '#000000', backgroundColor: '#f8f9fa'}}>
                {date}
              </div>
            ))
          ) : (
            <div className="no-entities" style={{color: '#000000'}}>No dates detected</div>
          )}
        </div>
      </div>
    </div>
  );
};

  const TextMetrics = ({ metrics }) => {
    if (!metrics) return null;
    
    return (
      <div className="text-metrics">
        <h3>📈 Text Analysis</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <span className="metric-value">{metrics.word_count || 0}</span>
            <span className="metric-label">Words</span>
          </div>
          <div className="metric-card">
            <span className="metric-value">{metrics.sentence_count || 0}</span>
            <span className="metric-label">Sentences</span>
          </div>
          <div className="metric-card">
            <span className="metric-value">{metrics.risk_keywords_total || 0}</span>
            <span className="metric-label">Risk Keywords</span>
          </div>
        </div>
      </div>
    );
  };

  const FINANCIAL_RISK_CATEGORIES = {
    credit_risk: { color: '#FF6B6B' },
    market_risk: { color: '#4ECDC4' },
    operational_risk: { color: '#45B7D1' },
    regulatory_risk: { color: '#96CEB4' }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <h1>🧠 FinancialRiskRadar</h1>
        <p>NLP-Powered Financial Risk Detection</p>
      </header>

      {/* Navigation */}
      <nav className="app-nav">
        <button 
          className={activeTab === 'universal' ? 'active' : ''}
          onClick={() => setActiveTab('universal')}
        >
          🌐 Universal Risk Analysis
        </button>
        <button 
          className={activeTab === 'banking' ? 'active' : ''}
          onClick={() => setActiveTab('banking')}
        >
          🏦 Bank Risk Monitor
        </button>
        <button 
          className={activeTab === 'fintech' ? 'active' : ''}
          onClick={() => setActiveTab('fintech')}
        >
          🚀 FinTech Dashboard
        </button>
      </nav>

      {/* Main Content */}
      <main className="app-main">
        {activeTab === 'universal' && (
          <div className="universal-analysis">
            {/* Input Section */}
            <div className="input-section">
              <div className="input-group">
                <h3>🔗 Analyze URL</h3>
                <div className="url-input">
                  <input
                    type="text"
                    placeholder="Enter financial article URL..."
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                  />
                  <button onClick={analyzeUrl} disabled={loading}>
                    {loading ? 'Analyzing...' : 'Analyze URL'}
                  </button>
                </div>
              </div>

              <div className="input-group">
                <h3>📝 Analyze Text</h3>
                <div className="text-input-header">
                  <button onClick={loadSample} className="sample-btn">
                    Load Sample Text
                  </button>
                </div>
                <textarea
                  placeholder="Paste financial text, SEC filing, or news article..."
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  rows="8"
                />
                <button onClick={analyzeText} disabled={loading} className="analyze-btn">
                  {loading ? 'Analyzing...' : 'Analyze Text'}
                </button>
              </div>
            </div>

            {/* Results Section */}
            {analysis && (
              <div className="results-section">
                <div className="results-header">
                  <h2>📊 Analysis Results</h2>
                  {analysis.title && <p className="analysis-title">Title: {analysis.title}</p>}
                  {analysis.note && <p className="analysis-note">📝 {analysis.note}</p>}
                </div>

                {/* Overall Risk Score */}
                <div className="overall-risk">
                  <RiskScoreGauge score={analysis?.analysis?.overall_risk_score || 0} />
                </div>

                {/* Risk Categories */}
                {analysis?.analysis?.risk_categories && analysis.analysis.risk_categories.length > 0 ? (
                  <div className="risk-categories">
                    <h3>🎯 Risk Categories Detected</h3>
                    <div className="risk-cards-grid">
                      {analysis.analysis.risk_categories.map((risk, idx) => (
                        <RiskCategoryCard key={idx} risk={risk} />
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="no-risks">
                    <p>⚠️ No specific financial risks detected in this content.</p>
                  </div>
                )}

                {/* Text Metrics */}
                <TextMetrics metrics={analysis?.analysis?.text_metrics} />

                {/* Entities */}
                <EntitySection entities={analysis?.analysis?.entities_extracted} />

                {/* Content Preview */}
                <div className="content-preview">
                  <h3>📄 Content Preview</h3>
                  <div className="preview-text">
                    {analysis.content_preview || analysis.text_preview || 'No content preview available'}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'banking' && (
          <div className="banking-monitor">
            <h2>🏦 Bank Risk Monitor</h2>
            <p>Real-time banking sector risk analysis (Coming Soon)</p>
          </div>
        )}

        {activeTab === 'fintech' && (
          <div className="fintech-dashboard">
            <h2>🚀 FinTech Dashboard</h2>
            <p>FinTech sector risk monitoring (Coming Soon)</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;