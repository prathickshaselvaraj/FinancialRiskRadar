import React, { useState } from 'react';
import RiskOverview from './components/RiskDashboard/RiskOverview';
import EntityNetwork from './components/EntityVisualization/EntityNetwork';

const API_BASE = 'http://localhost:8000';

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [inputText, setInputText] = useState('');

  const analyzeText = async (text) => {
    try {
      const response = await fetch(`${API_BASE}/api/analyze-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          request: { 
            text: text 
          } 
        })
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API call failed:', error);
      throw error;
    }
  };

  const handleAnalyze = async (text) => {
    if (!text.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await analyzeText(text);
      setAnalysis(result.analysis);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Financial Risk Radar
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Analysis Input with Button */}
        <div className="mb-8 bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Enter Financial Text for Analysis</h3>
          <textarea 
            className="w-full p-4 border rounded-lg mb-4"
            placeholder="Paste financial text here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows="6"
          />
          <button 
            onClick={() => handleAnalyze(inputText)}
            disabled={loading || !inputText.trim()}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Analyzing...' : 'Analyze Text'}
          </button>
        </div>

        {loading && (
          <div className="text-center p-8 bg-white rounded-lg shadow">
            <div className="text-lg">🔍 Analyzing financial risks...</div>
          </div>
        )}

        {error && (
          <div className="text-red-500 text-center p-4 bg-red-50 rounded-lg">
            Error: {error}
          </div>
        )}

        {analysis && (
          <div className="space-y-8">
            <RiskOverview analysisData={analysis} />
            <EntityNetwork networkData={analysis.visualization_data?.network_data} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;