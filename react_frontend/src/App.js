import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [activeModule, setActiveModule] = useState('home');
  const [url, setUrl] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeUrl = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/api/analyze-url`, { url });
      setAnalysisResult(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Analysis failed. Check console for details.');
    }
    setLoading(false);
  };

  const ModuleButton = ({ icon, title, description, onClick }) => (
    <div className="module-card">
      <div className="module-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{description}</p>
      <button onClick={onClick} className="module-button">
        Open {title}
      </button>
    </div>
  );

  if (activeModule === 'home') {
    return (
      <div className="App">
        <header className="app-header">
          <h1>🌐 Financial Risk Radar</h1>
          <p>AI-Powered Financial Risk Analysis Platform</p>
        </header>

        <div className="modules-grid">
          <ModuleButton
            icon="📊"
            title="Universal Risk Tagging"
            description="Analyze any financial document or website for general risk assessment"
            onClick={() => setActiveModule('universal')}
          />

          <ModuleButton
            icon="🏦"
            title="Bank Risk Monitor"
            description="Live banking sector risk insights and regulatory alerts"
            onClick={() => setActiveModule('banking')}
          />

          <ModuleButton
            icon="🛡️"
            title="Insurance Assessment"
            description="Individual insurance risk profiling and fraud detection"
            onClick={() => setActiveModule('insurance')}
          />

          <ModuleButton
            icon="🚀"
            title="FinTech Dashboard"
            description="Live fintech sector monitoring and cybersecurity threats"
            onClick={() => setActiveModule('fintech')}
          />
        </div>
      </div>
    );
  }

  if (activeModule === 'universal') {
    return (
      <div className="App">
        <header className="app-header">
          <button onClick={() => setActiveModule('home')} className="back-button">
            ← Back to Home
          </button>
          <h2>📊 Universal Risk Tagging</h2>
        </header>

        <div className="module-content">
          <div className="input-section">
            <input
              type="text"
              placeholder="Enter URL (news, reports, financial documents)..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="url-input"
            />
            <button onClick={analyzeUrl} disabled={loading} className="analyze-button">
              {loading ? 'Analyzing...' : '🔍 Analyze URL'}
            </button>
          </div>

          {analysisResult && (
            <div className="results-section">
              <h3>Analysis Results</h3>
              <div className="risk-tags">
                <div className="risk-tag">
                  <span>Regulatory Risk</span>
                  <span className="risk-value">{Math.round(analysisResult.risk_tags.regulatory * 100)}%</span>
                </div>
                <div className="risk-tag">
                  <span>Financial Risk</span>
                  <span className="risk-value">{Math.round(analysisResult.risk_tags.financial * 100)}%</span>
                </div>
                <div className="risk-tag">
                  <span>Operational Risk</span>
                  <span className="risk-value">{Math.round(analysisResult.risk_tags.operational * 100)}%</span>
                </div>
                <div className="risk-tag">
                  <span>Reputational Risk</span>
                  <span className="risk-value">{Math.round(analysisResult.risk_tags.reputational * 100)}%</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Placeholder for other modules
  return (
    <div className="App">
      <header className="app-header">
        <button onClick={() => setActiveModule('home')} className="back-button">
          ← Back to Home
        </button>
        <h2>🚧 {activeModule.charAt(0).toUpperCase() + activeModule.slice(1)} Module</h2>
      </header>
      <div className="module-content">
        <p>This module is under development. Coming soon!</p>
      </div>
    </div>
  );
}

export default App;