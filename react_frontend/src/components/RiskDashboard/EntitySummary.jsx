import React from 'react';

const EntitySummary = ({ entities }) => {
  if (!entities) return null;

  // Remove duplicates and clean data
  const companies = [...new Set(entities.companies || [])].filter(company => company && company.trim());
  const financialAmounts = [...new Set(entities.financial_amounts || [])].filter(amount => amount && amount.trim());
  const regulatoryBodies = [...new Set(entities.regulatory_bodies || [])].filter(regulator => regulator && regulator.trim());

  return (
    <div className="entity-summary bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-xl font-bold mb-4 text-gray-800">Entities Detected</h3>
      
      <div className="space-y-4">
        {/* Companies */}
        {companies.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-600 mb-2">🏢 Companies</h4>
            <div className="flex flex-wrap gap-2">
              {companies.map((company, index) => (
                <span key={index} className="bg-blue-100 text-blue-800 px-3 py-2 rounded-lg text-sm font-medium shadow-sm">
                  {company}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Financial Amounts */}
        {financialAmounts.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-600 mb-2">💰 Financial Amounts</h4>
            <div className="flex flex-wrap gap-2">
              {financialAmounts.map((amount, index) => (
                <span key={index} className="bg-green-100 text-green-800 px-3 py-2 rounded-lg text-sm font-medium shadow-sm">
                  {amount}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Regulatory Bodies */}
        {regulatoryBodies.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-600 mb-2">⚖️ Regulators</h4>
            <div className="flex flex-wrap gap-2">
              {regulatoryBodies.map((regulator, index) => (
                <span key={index} className="bg-red-100 text-red-800 px-3 py-2 rounded-lg text-sm font-medium shadow-sm">
                  {regulator}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Show message if no entities */}
        {companies.length === 0 && financialAmounts.length === 0 && regulatoryBodies.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <div className="text-4xl mb-2">🔍</div>
            <p>No entities detected</p>
          </div>
        )}

        {/* Entity Count Summary */}
        {(companies.length > 0 || financialAmounts.length > 0 || regulatoryBodies.length > 0) && (
          <div className="mt-4 p-3 bg-gray-50 rounded-lg">
            <div className="grid grid-cols-3 gap-4 text-center text-sm">
              <div>
                <div className="font-bold text-blue-600">{companies.length}</div>
                <div className="text-gray-600">Companies</div>
              </div>
              <div>
                <div className="font-bold text-green-600">{financialAmounts.length}</div>
                <div className="text-gray-600">Amounts</div>
              </div>
              <div>
                <div className="font-bold text-red-600">{regulatoryBodies.length}</div>
                <div className="text-gray-600">Regulators</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EntitySummary;