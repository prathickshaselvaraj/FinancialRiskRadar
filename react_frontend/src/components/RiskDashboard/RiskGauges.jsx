import React from 'react';

const RiskGauges = ({ scores }) => {
  if (!scores) return null;

  // Handle different score structures
  const overallRisk = scores.overall_risk_score || scores.overall_risk || 0;
  const categoryScores = scores.category_scores || {};
  
  const getRiskLevel = (score) => {
    if (score < 30) return { level: 'Low', color: 'green' };
    if (score < 70) return { level: 'Medium', color: 'orange' };
    return { level: 'High', color: 'red' };
  };

  const riskInfo = getRiskLevel(overallRisk);

  return (
    <div className="risk-gauges bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-4">Risk Assessment</h3>
      
      <div className="gauge-container text-center">
        <div className="gauge-wrapper relative inline-block">
          <div className="gauge w-48 h-24 bg-gray-200 rounded-t-full overflow-hidden relative">
            <div 
              className="gauge-fill absolute bottom-0 left-0 right-0 transition-all duration-500"
              style={{
                height: `${overallRisk}%`,
                backgroundColor: riskInfo.color
              }}
            ></div>
          </div>
          <div className="gauge-value absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <span className="text-2xl font-bold">{overallRisk}</span>
            <span className="text-sm block">{riskInfo.level} Risk</span>
          </div>
        </div>
      </div>

      {/* Category Scores */}
      {Object.keys(categoryScores).length > 0 && (
        <div className="category-scores mt-6 grid grid-cols-2 gap-4">
          {Object.entries(categoryScores).map(([category, score]) => (
            <div key={category} className="category-score text-center">
              <div className="text-sm capitalize">{category.replace('_', ' ')}</div>
              <div className="font-bold">{score}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RiskGauges;