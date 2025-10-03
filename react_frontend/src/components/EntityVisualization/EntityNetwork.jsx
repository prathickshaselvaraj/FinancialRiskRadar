import React from 'react';

const EntityNetwork = ({ networkData }) => {
  if (!networkData) return null;

  const nodes = networkData.nodes || [];
  const links = networkData.links || [];

  return (
    <div className="entity-network bg-white p-6 rounded-lg shadow-lg">
      <h3 className="text-2xl font-bold mb-6 text-gray-800">Entity Relationships</h3>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Network Visualization Placeholder */}
        <div className="network-visualization min-h-64 border-2 border-dashed border-gray-300 rounded-lg p-4 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <div className="text-4xl mb-2">🕸️</div>
            <p className="font-semibold">Network Visualization</p>
            <p className="text-sm mt-2">
              {nodes.length} entities, {links.length} relationships
            </p>
            <p className="text-xs mt-1 text-gray-400">
              Interactive graph coming soon
            </p>
          </div>
        </div>
        
        {/* Entity Relationships List */}
        <div className="entity-relationships">
          <h4 className="font-bold text-lg mb-4 text-gray-700">Relationship Summary</h4>
          
          {links.length > 0 ? (
            <div className="space-y-3">
              {links.slice(0, 8).map((link, index) => (
                <div key={index} className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="flex items-center justify-between">
                    <div className="font-medium text-blue-600">{link.source}</div>
                    <div className="text-gray-400 mx-2">→</div>
                    <div className="font-medium text-green-600">{link.target}</div>
                  </div>
                  {link.relationship && (
                    <div className="mt-1 text-xs text-gray-600 text-center">
                      {link.relationship}
                    </div>
                  )}
                </div>
              ))}
              {links.length > 8 && (
                <div className="text-center text-sm text-gray-500">
                  + {links.length - 8} more relationships
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <div className="text-3xl mb-2">🔗</div>
              <p>No relationships detected</p>
            </div>
          )}
        </div>
      </div>

      {/* Network Statistics */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-semibold text-blue-800 mb-2">Network Statistics</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-blue-600">{nodes.length}</div>
            <div className="text-sm text-blue-700">Total Entities</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">{links.length}</div>
            <div className="text-sm text-green-700">Relationships</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-600">
              {nodes.filter(n => n.type === 'company').length}
            </div>
            <div className="text-sm text-purple-700">Companies</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-red-600">
              {nodes.filter(n => n.type === 'regulator').length}
            </div>
            <div className="text-sm text-red-700">Regulators</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EntityNetwork;