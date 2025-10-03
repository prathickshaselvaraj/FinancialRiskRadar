const API_BASE = 'http://localhost:8000';

export const analyzeText = async (text) => {
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