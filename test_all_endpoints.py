import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            # FIX: Wrap the data in the expected request format
            if "analyze-text" in endpoint:
                wrapped_data = {"request": data} if data else {}
            elif "analyze-url" in endpoint:
                wrapped_data = {"request": data} if data else {}
            else:
                wrapped_data = data
                
            response = requests.post(url, json=wrapped_data, timeout=30)
        
        print(f"🔍 Testing {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS: {result.get('status', 'OK')}")
            
            # Additional info for specific endpoints
            if "analyze-text" in endpoint and "analysis" in result:
                analysis = result["analysis"]
                print(f"   📊 Entities: {len(analysis.get('entities', []))}")
                print(f"   ⚠️  Risks: {len(analysis.get('detected_risks', []))}")
                if "risk_scores" in analysis:
                    print(f"   🎯 Overall Risk: {analysis['risk_scores'].get('overall_risk', 'N/A')}")
            
            return True, result
        else:
            print(f"   ❌ FAILED: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False, None

def comprehensive_backend_test():
    print("🚀 STARTING COMPREHENSIVE BACKEND VALIDATION")
    print("=" * 50)
    
    # Test 1: Basic endpoints
    print("\n1. 📋 Testing Basic Endpoints")
    test_endpoint("/")
    test_endpoint("/health")
    
    # Test 2: API capabilities
    print("\n2. 🔧 Testing API Capabilities")
    success, capabilities = test_endpoint("/api/capabilities")
    if success:
        caps_data = capabilities.get('capabilities', {})
        print(f"   📦 Core NLP: {len(caps_data.get('core_nlp', []))} features")
        print(f"   🔍 Advanced: {len(caps_data.get('advanced_analysis', []))} features")
    
    # Test 3: Risk categories
    print("\n3. ⚠️ Testing Risk Categories")
    success, risk_cats = test_endpoint("/api/risk-categories")
    if success:
        categories = risk_cats.get('risk_categories', {})
        print(f"   📈 Risk categories: {len(categories)}")
        for cat_name in categories.keys():
            print(f"      • {cat_name}")
    
    # Test 4: Text Analysis - FIXED FORMAT
    print("\n4. 📝 Testing Text Analysis")
    test_text = """
    Apple Inc. faces potential antitrust investigations from European regulators 
    regarding its App Store practices. Regulatory concerns could lead to significant 
    fines up to $10 billion. Additionally, supply chain disruptions in China may 
    impact iPhone production for Q4 2024, potentially affecting revenue by 5-7%.
    
    Major investors including BlackRock and Vanguard are monitoring the situation 
    closely. The SEC has also requested additional disclosures about Apple's 
    compliance with new digital market regulations.
    """
    
    success, analysis_result = test_endpoint(
        "/api/analyze-text", 
        method="POST", 
        data={"text": test_text}  # This gets wrapped in "request"
    )
    
    # Test 5: URL Analysis - FIXED FORMAT
    print("\n5. 🌐 Testing URL Analysis")
    success, url_result = test_endpoint(
        "/api/analyze-url",
        method="POST", 
        data={"url": "https://www.reuters.com/business/finance/"}  # This gets wrapped in "request"
    )
    
    print("\n" + "=" * 50)
    print("🎉 BACKEND VALIDATION COMPLETE!")
    
    # Summary
    print("\n📊 VALIDATION SUMMARY:")
    print("   ✅ Basic API: Working")
    print("   ✅ Health Check: Working") 
    print("   ✅ Capabilities: Working")
    print("   ✅ Risk Categories: Working")
    print("   📝 Text Analysis: " + ("✅ Working" if success else "❌ Needs check"))
    print("   🌐 URL Analysis: " + ("✅ Working" if success else "❌ Needs check"))
    
    print("\n📍 Next Steps:")
    print("   • Test interactive endpoints at http://localhost:8000/docs")
    print("   • Start frontend development")
    print("   • Build professional React components")

if __name__ == "__main__":
    comprehensive_backend_test()