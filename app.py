from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, AllChem, Draw
from rdkit.Chem.Draw import rdMolDraw2D
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import json
import io
import base64
import plotly.graph_objects as go
import plotly.utils
from typing import Dict, List, Any

app = Flask(__name__)
CORS(app)

class ChemicalAnalysisAI:
    """AI model for chemical analysis and property prediction"""
    
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
    
    def extract_molecular_features(self, smiles: str) -> np.ndarray:
        """Extract molecular features from SMILES string"""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        features = []
        
        # Basic molecular descriptors
        features.extend([
            Descriptors.MolWt(mol),
            Descriptors.MolLogP(mol),
            Descriptors.TPSA(mol),
            Descriptors.NumHDonors(mol),
            Descriptors.NumHAcceptors(mol),
            Descriptors.NumRotatableBonds(mol),
            Descriptors.NumAromaticRings(mol),
            Descriptors.NumSaturatedRings(mol),
            Descriptors.FractionCsp3(mol),
            Descriptors.BertzCT(mol)
        ])
        
        # Morgan fingerprint features (first 50 bits)
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
        features.extend(list(fp)[:50])
        
        return np.array(features)
    
    def predict_properties(self, smiles: str) -> Dict[str, Any]:
        """Predict chemical properties for a given SMILES string"""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return {"error": "Invalid SMILES string"}
        
        # Calculate actual properties
        properties = {
            'molecular_formula': Chem.rdMolDescriptors.CalcMolFormula(mol),
            'molecular_weight': Descriptors.MolWt(mol),
            'logp': Descriptors.MolLogP(mol),
            'tpsa': Descriptors.TPSA(mol),
            'hbd_count': Descriptors.NumHDonors(mol),
            'hba_count': Descriptors.NumHAcceptors(mol),
            'rotatable_bonds': Descriptors.NumRotatableBonds(mol),
            'aromatic_rings': Descriptors.NumAromaticRings(mol),
            'lipinski_violations': self._calculate_lipinski_violations(mol),
            'drug_likeness_score': self._calculate_drug_likeness(mol),
            'toxicity_prediction': self._predict_toxicity(mol)
        }
        
        return properties
    
    def _calculate_lipinski_violations(self, mol) -> int:
        """Calculate Lipinski's Rule of Five violations"""
        violations = 0
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hbd = Descriptors.NumHDonors(mol)
        hba = Descriptors.NumHAcceptors(mol)
        
        if mw > 500:
            violations += 1
        if logp > 5:
            violations += 1
        if hbd > 5:
            violations += 1
        if hba > 10:
            violations += 1
            
        return violations
    
    def _calculate_drug_likeness(self, mol) -> float:
        """Calculate a drug-likeness score (0-1)"""
        # Simplified drug-likeness calculation
        violations = self._calculate_lipinski_violations(mol)
        tpsa = Descriptors.TPSA(mol)
        rotatable = Descriptors.NumRotatableBonds(mol)
        
        score = 1.0
        score -= violations * 0.2  # Penalty for Lipinski violations
        
        if tpsa > 140:
            score -= 0.1
        if rotatable > 10:
            score -= 0.1
            
        return max(0.0, min(1.0, score))
    
    def _predict_toxicity(self, mol) -> str:
        """Simple toxicity prediction based on structural alerts"""
        # This is a simplified version - in practice, you'd use more sophisticated models
        alerts = [
            'c1ccccc1[N+](=O)[O-]',  # Nitrobenzene
            'C(=O)Cl',               # Acyl chloride
            'S(=O)(=O)Cl',          # Sulfonyl chloride
            '[CH2][CH2]Cl',         # Alkyl chloride
        ]
        
        smiles = Chem.MolToSmiles(mol)
        for alert in alerts:
            alert_mol = Chem.MolFromSmarts(alert)
            if alert_mol and mol.HasSubstructMatch(alert_mol):
                return "High Risk"
        
        # Check for other risk factors
        if Descriptors.MolWt(mol) > 800:
            return "Medium Risk"
        if Descriptors.MolLogP(mol) > 6:
            return "Medium Risk"
            
        return "Low Risk"
    
    def generate_3d_coordinates(self, smiles: str) -> Dict[str, Any]:
        """Generate 3D coordinates for molecular visualization"""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return {"error": "Invalid SMILES string"}
        
        # Add hydrogens and generate 3D coordinates
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.OptimizeMoleculeConfs(mol)
        
        # Extract atomic coordinates and properties
        conf = mol.GetConformer()
        atoms = []
        bonds = []
        
        for atom in mol.GetAtoms():
            pos = conf.GetAtomPosition(atom.GetIdx())
            atoms.append({
                'element': atom.GetSymbol(),
                'x': float(pos.x),
                'y': float(pos.y),
                'z': float(pos.z),
                'atomicNum': atom.GetAtomicNum(),
                'formalCharge': atom.GetFormalCharge(),
                'hybridization': str(atom.GetHybridization())
            })
        
        for bond in mol.GetBonds():
            bonds.append({
                'atom1': bond.GetBeginAtomIdx(),
                'atom2': bond.GetEndAtomIdx(),
                'bondType': str(bond.GetBondType()),
                'isAromatic': bond.GetIsAromatic()
            })
        
        return {
            'atoms': atoms,
            'bonds': bonds,
            'molecular_formula': Chem.rdMolDescriptors.CalcMolFormula(mol)
        }
    
    def generate_2d_structure(self, smiles: str) -> str:
        """Generate 2D molecular structure as base64 encoded image"""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        # Generate 2D image
        img = Draw.MolToImage(mol, size=(400, 400))
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"

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
            'success': True
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/examples')
def get_examples():
    """Get example molecules for demonstration"""
    examples = [
        {
            'name': 'Caffeine',
            'smiles': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
            'description': 'Stimulant found in coffee and tea'
        },
        {
            'name': 'Aspirin',
            'smiles': 'CC(=O)OC1=CC=CC=C1C(=O)O',
            'description': 'Common pain reliever and anti-inflammatory drug'
        },
        {
            'name': 'Morphine',
            'smiles': 'CN1CC[C@]23C4=C5C=CC(O)=C4O[C@H]2[C@@H](O)C=C[C@H]3[C@H]1C5',
            'description': 'Powerful opioid pain medication'
        },
        {
            'name': 'Penicillin',
            'smiles': 'CC1([C@@H](N2[C@H](S1)[C@@H](C2=O)NC(=O)CC3=CC=CC=C3)C(=O)O)C',
            'description': 'Antibiotic medication'
        },
        {
            'name': 'Dopamine',
            'smiles': 'NCCc1ccc(O)c(O)c1',
            'description': 'Neurotransmitter associated with reward and motivation'
        },
        {
            'name': 'Glucose',
            'smiles': 'C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O)O',
            'description': 'Simple sugar and primary source of energy'
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
            'name': 'Caffeine',
            'smiles': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
            'description': 'Stimulant found in coffee and tea'
        },
        {
            'name': 'Aspirin',
            'smiles': 'CC(=O)OC1=CC=CC=C1C(=O)O',
            'description': 'Common pain reliever and anti-inflammatory drug'
        },
        {
            'name': 'Morphine',
            'smiles': 'CN1CC[C@]23C4=C5C=CC(O)=C4O[C@H]2[C@@H](O)C=C[C@H]3[C@H]1C5',
            'description': 'Powerful opioid pain medication'
        },
        {
            'name': 'Penicillin',
            'smiles': 'CC1([C@@H](N2[C@H](S1)[C@@H](C2=O)NC(=O)CC3=CC=CC=C3)C(=O)O)C',
            'description': 'Antibiotic medication'
        },
        {
            'name': 'Dopamine',
            'smiles': 'NCCc1ccc(O)c(O)c1',
            'description': 'Neurotransmitter associated with reward and motivation'
        }
    ]
    
    results = [mol for mol in examples if query in mol['name'].lower() or query in mol['description'].lower()]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)