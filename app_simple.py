from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import json
import io
import base64
import plotly.graph_objects as go
import plotly.utils
from typing import Dict, List, Any
import math

app = Flask(__name__)
CORS(app)

class ChemicalAnalysisAI:
    """Simplified AI model for chemical analysis (without RDKit dependency)"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.models = {}
        self.is_trained = False
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize machine learning models for different properties"""
        # Models for different chemical properties
        self.models = {
            'molecular_weight': RandomForestRegressor(n_estimators=100, random_state=42),
            'logp': RandomForestRegressor(n_estimators=100, random_state=42),
            'tpsa': RandomForestRegressor(n_estimators=100, random_state=42),
            'solubility': RandomForestRegressor(n_estimators=100, random_state=42),
            'bioavailability': RandomForestRegressor(n_estimators=100, random_state=42)
        }
    
    def predict_properties(self, smiles: str) -> Dict[str, Any]:
        """Predict chemical properties for a given SMILES string (simplified version)"""
        # This is a simplified version that estimates properties based on SMILES patterns
        # In the full version, this would use RDKit for accurate calculations
        
        properties = {}
        
        # Basic pattern-based estimations
        carbon_count = smiles.count('C')
        nitrogen_count = smiles.count('N')
        oxygen_count = smiles.count('O')
        sulfur_count = smiles.count('S')
        ring_count = smiles.count('1') // 2  # Simple ring estimation
        
        # Estimate molecular formula (simplified)
        properties['molecular_formula'] = f"C{carbon_count}H{carbon_count*2}N{nitrogen_count}O{oxygen_count}"
        
        # Estimate molecular weight (very rough)
        estimated_mw = carbon_count * 12 + nitrogen_count * 14 + oxygen_count * 16 + sulfur_count * 32
        estimated_mw += (carbon_count * 2) * 1  # Rough hydrogen estimate
        properties['molecular_weight'] = estimated_mw
        
        # Estimate LogP (simplified)
        properties['logp'] = (carbon_count * 0.5) - (nitrogen_count * 0.7) - (oxygen_count * 1.0)
        
        # Estimate TPSA (simplified)
        properties['tpsa'] = nitrogen_count * 23.79 + oxygen_count * 20.23
        
        # Other properties
        properties['hbd_count'] = smiles.count('O') + smiles.count('N')  # Simplified
        properties['hba_count'] = smiles.count('O') + smiles.count('N')
        properties['rotatable_bonds'] = max(0, carbon_count - ring_count * 3)
        properties['aromatic_rings'] = ring_count
        
        # Calculate Lipinski violations
        properties['lipinski_violations'] = self._calculate_lipinski_violations_simple(properties)
        
        # Calculate drug-likeness score
        properties['drug_likeness_score'] = self._calculate_drug_likeness_simple(properties)
        
        # Predict toxicity
        properties['toxicity_prediction'] = self._predict_toxicity_simple(smiles)
        
        return properties
    
    def _calculate_lipinski_violations_simple(self, properties) -> int:
        """Calculate Lipinski's Rule of Five violations (simplified)"""
        violations = 0
        mw = properties.get('molecular_weight', 0)
        logp = properties.get('logp', 0)
        hbd = properties.get('hbd_count', 0)
        hba = properties.get('hba_count', 0)
        
        if mw > 500:
            violations += 1
        if logp > 5:
            violations += 1
        if hbd > 5:
            violations += 1
        if hba > 10:
            violations += 1
            
        return violations
    
    def _calculate_drug_likeness_simple(self, properties) -> float:
        """Calculate a drug-likeness score (0-1) (simplified)"""
        violations = properties.get('lipinski_violations', 0)
        tpsa = properties.get('tpsa', 0)
        rotatable = properties.get('rotatable_bonds', 0)
        
        score = 1.0
        score -= violations * 0.2  # Penalty for Lipinski violations
        
        if tpsa > 140:
            score -= 0.1
        if rotatable > 10:
            score -= 0.1
            
        return max(0.0, min(1.0, score))
    
    def _predict_toxicity_simple(self, smiles: str) -> str:
        """Simple toxicity prediction based on basic patterns"""
        # This is a very simplified version
        if 'Cl' in smiles and 'C=O' in smiles:
            return "High Risk"
        elif len(smiles) > 50:
            return "Medium Risk"
        elif 'N' in smiles and 'O' in smiles:
            return "Medium Risk"
        else:
            return "Low Risk"
    
    def generate_3d_coordinates(self, smiles: str) -> Dict[str, Any]:
        """Generate simplified 3D coordinates for molecular visualization"""
        # This is a simplified version that creates a basic molecular structure
        # In the full version, this would use RDKit for accurate 3D coordinates
        
        atoms = []
        bonds = []
        
        # Parse basic atoms from SMILES (very simplified)
        atom_count = 0
        for i, char in enumerate(smiles):
            if char in ['C', 'N', 'O', 'S']:
                # Generate pseudo-random 3D coordinates
                angle = (atom_count * 60) * math.pi / 180
                radius = atom_count * 1.5
                
                atoms.append({
                    'element': char,
                    'x': radius * math.cos(angle),
                    'y': radius * math.sin(angle),
                    'z': (atom_count % 3) * 1.0,
                    'atomicNum': {'C': 6, 'N': 7, 'O': 8, 'S': 16}.get(char, 6),
                    'formalCharge': 0,
                    'hybridization': 'SP3'
                })
                
                # Create bonds to previous atoms
                if atom_count > 0:
                    bonds.append({
                        'atom1': atom_count - 1,
                        'atom2': atom_count,
                        'bondType': 'SINGLE',
                        'isAromatic': False
                    })
                
                atom_count += 1
        
        return {
            'atoms': atoms,
            'bonds': bonds,
            'molecular_formula': f'Simplified structure from {smiles}'
        }
    
    def generate_2d_structure(self, smiles: str) -> str:
        """Generate a placeholder 2D structure image"""
        # This returns a placeholder since we don't have RDKit
        # In the full version, this would generate actual molecular structure images
        return "data:image/svg+xml;base64," + base64.b64encode(
            f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
                <rect width="400" height="400" fill="#f8f9fa"/>
                <text x="200" y="180" text-anchor="middle" font-family="Arial" font-size="16" fill="#666">
                    2D Structure
                </text>
                <text x="200" y="200" text-anchor="middle" font-family="Arial" font-size="14" fill="#666">
                    SMILES: {smiles}
                </text>
                <text x="200" y="230" text-anchor="middle" font-family="Arial" font-size="12" fill="#999">
                    (Simplified version - install RDKit for full functionality)
                </text>
            </svg>'''.encode()
        ).decode()

# Initialize the AI model
ai_model = ChemicalAnalysisAI()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_molecule():
    """Analyze a molecule from SMILES input"""
    data = request.get_json()
    smiles = data.get('smiles', '').strip()
    
    if not smiles:
        return jsonify({'error': 'SMILES string is required'}), 400
    
    try:
        # Analyze molecular properties
        properties = ai_model.predict_properties(smiles)
        
        # Generate 3D structure
        structure_3d = ai_model.generate_3d_coordinates(smiles)
        
        # Generate 2D structure image
        structure_2d = ai_model.generate_2d_structure(smiles)
        
        response = {
            'smiles': smiles,
            'properties': properties,
            'structure_3d': structure_3d,
            'structure_2d': structure_2d,
            'success': True,
            'note': 'This is a simplified version. Install RDKit for accurate molecular analysis.'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/examples')
def get_examples():
    """Get example molecules for demonstration"""
    examples = [
        {
            'name': 'Methane',
            'smiles': 'C',
            'description': 'Simplest hydrocarbon molecule'
        },
        {
            'name': 'Ethanol',
            'smiles': 'CCO',
            'description': 'Common alcohol found in beverages'
        },
        {
            'name': 'Caffeine (simplified)',
            'smiles': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
            'description': 'Stimulant found in coffee and tea'
        },
        {
            'name': 'Aspirin (simplified)',
            'smiles': 'CC(=O)OC1=CC=CC=C1C(=O)O',
            'description': 'Common pain reliever and anti-inflammatory drug'
        },
        {
            'name': 'Water',
            'smiles': 'O',
            'description': 'Essential for all life'
        },
        {
            'name': 'Benzene',
            'smiles': 'C1=CC=CC=C1',
            'description': 'Simple aromatic compound'
        }
    ]
    
    return jsonify(examples)

@app.route('/api/search', methods=['POST'])
def search_molecules():
    """Search for molecules by name or properties"""
    data = request.get_json()
    query = data.get('query', '').strip().lower()
    
    # This would typically query a chemical database
    # For demonstration, we'll use our example molecules
    examples = [
        {
            'name': 'Methane',
            'smiles': 'C',
            'description': 'Simplest hydrocarbon molecule'
        },
        {
            'name': 'Ethanol',
            'smiles': 'CCO',
            'description': 'Common alcohol found in beverages'
        },
        {
            'name': 'Caffeine (simplified)',
            'smiles': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
            'description': 'Stimulant found in coffee and tea'
        },
        {
            'name': 'Aspirin (simplified)',
            'smiles': 'CC(=O)OC1=CC=CC=C1C(=O)O',
            'description': 'Common pain reliever and anti-inflammatory drug'
        }
    ]
    
    results = [mol for mol in examples if query in mol['name'].lower() or query in mol['description'].lower()]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)