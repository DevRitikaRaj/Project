#!/usr/bin/env python3
"""
Demo script for ChemAI - Chemical Analysis with 3D Visualization
This script demonstrates the key features of the application.
"""

import requests
import json
import time

def test_api_endpoint(url, data, description):
    """Test an API endpoint and display results"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis successful!")
            
            if 'properties' in result:
                props = result['properties']
                print(f"\n📊 Molecular Properties:")
                print(f"   Formula: {props.get('molecular_formula', 'N/A')}")
                print(f"   Molecular Weight: {props.get('molecular_weight', 'N/A'):.2f} g/mol")
                print(f"   LogP: {props.get('logp', 'N/A'):.2f}")
                print(f"   TPSA: {props.get('tpsa', 'N/A'):.2f} Ų")
                print(f"   H-Bond Donors: {props.get('hbd_count', 'N/A')}")
                print(f"   H-Bond Acceptors: {props.get('hba_count', 'N/A')}")
                print(f"   Lipinski Violations: {props.get('lipinski_violations', 'N/A')}")
                print(f"   Drug-likeness: {props.get('drug_likeness_score', 0)*100:.1f}%")
                print(f"   Toxicity Risk: {props.get('toxicity_prediction', 'N/A')}")
            
            if result.get('note'):
                print(f"\n💡 Note: {result['note']}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the application is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_examples():
    """Demonstrate analysis of example molecules"""
    examples = [
        {
            'name': 'Ethanol (alcohol)',
            'smiles': 'CCO',
            'description': 'Simple alcohol molecule'
        },
        {
            'name': 'Caffeine',
            'smiles': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
            'description': 'Stimulant found in coffee'
        },
        {
            'name': 'Aspirin',
            'smiles': 'CC(=O)OC1=CC=CC=C1C(=O)O',
            'description': 'Common painkiller'
        },
        {
            'name': 'Benzene',
            'smiles': 'C1=CC=CC=C1',
            'description': 'Simple aromatic compound'
        }
    ]
    
    print("🚀 ChemAI Demo - Chemical Analysis with AI")
    print("📊 Testing molecular analysis capabilities...")
    
    for example in examples:
        test_api_endpoint(
            'http://localhost:5000/api/analyze',
            {'smiles': example['smiles']},
            f"Analyzing {example['name']} ({example['description']})"
        )
        time.sleep(1)  # Brief pause between requests

def check_server():
    """Check if the server is running"""
    try:
        response = requests.get('http://localhost:5000/api/examples', timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def main():
    """Main demo function"""
    print("🧪 ChemAI Demo Script")
    print("=" * 50)
    
    # Check if server is running
    print("🔍 Checking if ChemAI server is running...")
    if not check_server():
        print("❌ ChemAI server is not running!")
        print("   Please start the application first:")
        print("   - Run: python3 app.py (full version)")
        print("   - Or: python3 app_simple.py (simplified version)")
        print("   - Or: ./run.sh (auto-detect)")
        return
    
    print("✅ ChemAI server is running!")
    
    # Run demo
    demo_examples()
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed!")
    print("🌐 Open http://localhost:5000 in your browser to use the web interface")
    print("📚 See README.md for detailed usage instructions")

if __name__ == "__main__":
    main()