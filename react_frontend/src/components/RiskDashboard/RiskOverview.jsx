import React from 'react';
import RiskGauges from './RiskGauges';
import EntitySummary from './EntitySummary';
import RiskBreakdown from './RiskBreakdown';

const RiskOverview = ({ analysisData }) => {
  if (!analysisData) return null;

  // Debug: log the data structure
  console.log('Analysis Data:', analysisData);

  return (
    <div className="risk-overview">
      <h2 className="text-2xl font-bold mb-6">Risk Analysis Dashboard</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Gauges - Main focus */}
        <div className="lg:col-span-2">
          <RiskGauges scores={analysisData.risk_scores} />
        </div>
        
        {/* Entity Summary - Side panel */}
        <div className="lg:col-span-1">
          <EntitySummary entities={analysisData.entities} />
        </div>
        
        {/* Risk Breakdown - Full width */}
        <div className="lg:col-span-3">
          <RiskBreakdown analysis={analysisData} />
        </div>
      </div>
    </div>
  );
};

export default RiskOverview;