import React from 'react';

const RiskBreakdown = ({ analysis }) => {
  if (!analysis) return null;

  // Handle the complex risk objects from backend
  const detectedRisks = analysis.detected_risks || [];
  const riskCategories = analysis.risk_categories || [];

  // Function to render risk items properly
  const renderRiskItem = (risk, index) => {
    if (typeof risk === 'string') {
      // Simple string risk
      return (
        <div key={index} className="flex items-center justify-between p-3 bg-red-50 rounded-lg border border-red-200">
          <div>
            <span className="font-medium text-red-800">{risk}</span>
          </div>
          <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-xs font-semibold">
            High Risk
          </span>
        </div>
      );
    } else if (typeof risk === 'object' && risk.type) {
      // Complex risk object from backend
      return (
        <div key={index} className="p-4 bg-white rounded-lg border border-gray-200 shadow-sm">
          <div className="flex justify-between items-start mb-2">
            <div>
              <span className="font-bold text-lg capitalize text-gray-800">
                {risk.type.replace('_', ' ')} Risk
              </span>
              <div className="flex items-center gap-2 mt-1">
                <div className="text-sm text-gray-600">Score: <strong>{risk.score}</strong></div>
                <div 
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: risk.color }}
                ></div>
              </div>
            </div>
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">
              {risk.sentence_count || risk.instances?.length || 0} instances
            </span>
          </div>
          
          {/* Keywords found */}
          {risk.keywords_found && risk.keywords_found.length > 0 && (
            <div className="mb-3">
              <span className="text-sm text-gray-600 mr-2">Keywords:</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {risk.keywords_found.map((keyword, kwIndex) => (
                  <span key={kwIndex} className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Risk description */}
          {risk.description && (
            <p className="text-sm text-gray-700 mt-2">{risk.description}</p>
          )}

          {/* Show first few instances */}
          {risk.instances && risk.instances.slice(0, 2).map((instance, instIndex) => (
            <div key={instIndex} className="mt-2 p-2 bg-gray-50 rounded text-sm">
              <div className="text-gray-600">{instance.sentence}</div>
              {instance.financial_impact && instance.financial_impact.length > 0 && (
                <div className="mt-1 text-red-600 font-semibold">
                  Impact: {instance.financial_impact.join(', ')}
                </div>
              )}
            </div>
          ))}
        </div>
      );
    }
    
    return null;
  };

  return (
    <div className="risk-breakdown bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-2xl font-bold mb-6 text-gray-800">Risk Breakdown</h3>
      
      {/* Display risk categories from backend */}
      {riskCategories.length > 0 ? (
        <div className="space-y-4">
          {riskCategories.map((risk, index) => renderRiskItem(risk, index))}
        </div>
      ) : detectedRisks.length > 0 ? (
        <div className="space-y-3">
          {detectedRisks.map((risk, index) => renderRiskItem(risk, index))}
        </div>
      ) : (
        <p className="text-gray-500 text-center py-8">No specific risks detected in the analysis</p>
      )}

      {/* Risk Summary */}
      {analysis.risk_scores?.risk_summary && (
        <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg border border-blue-200">
          <h4 className="font-bold text-lg mb-2 text-blue-800">Risk Summary</h4>
          <p className="text-blue-700">
            {analysis.risk_scores.risk_summary.recommendation || 
             'Monitor the situation for emerging risks'}
          </p>
          {analysis.risk_scores.risk_summary.risk_level && (
            <div className="mt-2 flex items-center gap-2">
              <span className="text-sm font-semibold">Overall Risk Level:</span>
              <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                analysis.risk_scores.risk_summary.risk_level === 'High' ? 'bg-red-100 text-red-800' :
                analysis.risk_scores.risk_summary.risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {analysis.risk_scores.risk_summary.risk_level}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RiskBreakdown;