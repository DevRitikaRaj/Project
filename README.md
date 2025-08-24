# ChemAI - Chemical Analysis with 3D Visualization

A comprehensive AI-powered chemical analysis platform that provides molecular property prediction, 3D visualization, and drug-likeness assessment using machine learning and cheminformatics.

## Features

### 🧪 Chemical Analysis
- **Molecular Property Prediction**: Calculate molecular weight, LogP, TPSA, and other key descriptors
- **Drug-likeness Assessment**: Evaluate Lipinski's Rule of Five violations and drug-likeness scores
- **Toxicity Prediction**: AI-based toxicity risk assessment using structural alerts
- **SMILES Input**: Support for SMILES (Simplified Molecular Input Line Entry System) notation

### 🎮 3D Visualization
- **Interactive 3D Models**: Rotate, zoom, and explore molecular structures in 3D
- **Multiple Visualization Styles**: Stick, sphere, line, and cartoon representations
- **Real-time Rendering**: WebGL-powered molecular visualization using 3Dmol.js
- **2D Structure Display**: Traditional 2D molecular structure diagrams

### 🤖 AI-Powered Features
- **Machine Learning Models**: Random Forest and TensorFlow-based property prediction
- **Molecular Fingerprints**: Morgan fingerprints for molecular similarity and analysis
- **Chemical Descriptors**: Comprehensive calculation of molecular descriptors
- **Automated Analysis**: Instant analysis and property prediction from SMILES input

### 💊 Drug Discovery Tools
- **Bioavailability Prediction**: Assess oral bioavailability potential
- **Lipinski Analysis**: Rule of Five compliance checking
- **Structural Alerts**: Identification of potentially toxic substructures
- **Pharmaceutical Profiling**: Comprehensive drug-like property assessment

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Cheminformatics**: RDKit (molecular analysis and property calculation)
- **Machine Learning**: Scikit-learn, TensorFlow
- **3D Visualization**: 3Dmol.js (WebGL-based molecular viewer)
- **Frontend**: Modern HTML5, CSS3, JavaScript (ES6+)
- **Scientific Computing**: NumPy, Pandas
- **Visualization**: Plotly, Matplotlib

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
python3 setup.py
./run.sh
```

### Option 2: Manual Installation

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd chemai
   ```

2. **Install dependencies**:
   ```bash
   # Basic dependencies (required)
   pip install --user flask flask-cors numpy pandas scikit-learn matplotlib plotly
   
   # RDKit for full functionality (optional but recommended)
   pip install --user rdkit-pypi
   # OR using conda: conda install -c conda-forge rdkit
   ```

3. **Run the application**:
   ```bash
   # Full version (if RDKit is installed)
   python3 app.py
   
   # Simplified version (works without RDKit)
   python3 app_simple.py
   ```

4. **Access the application**:
   Open your web browser and navigate to `http://localhost:5000`

### Testing the Installation
```bash
# Run the demo script to test functionality
python3 demo.py
```

## Usage

### Basic Analysis
1. Navigate to the "Molecular Analyzer" section
2. Enter a SMILES string (e.g., `CCO` for ethanol)
3. Click "Analyze" to generate predictions and visualizations
4. Explore the results:
   - 2D molecular structure
   - Interactive 3D visualization
   - Molecular properties
   - AI analysis results

### Example Molecules
- **Caffeine**: `CN1C=NC2=C1C(=O)N(C(=O)N2C)C`
- **Aspirin**: `CC(=O)OC1=CC=CC=C1C(=O)O`
- **Ethanol**: `CCO`
- **Benzene**: `C1=CC=CC=C1`

### 3D Visualization Controls
- **Mouse controls**: 
  - Left click + drag: Rotate molecule
  - Mouse wheel: Zoom in/out
  - Right click + drag: Pan
- **Style buttons**:
  - Reset View: Return to default zoom and rotation
  - Toggle Style: Switch between stick, sphere, line, and cartoon styles

## API Endpoints

### POST /api/analyze
Analyze a molecule from SMILES input.

**Request**:
```json
{
  "smiles": "CCO"
}
```

**Response**:
```json
{
  "smiles": "CCO",
  "properties": {
    "molecular_formula": "C2H6O",
    "molecular_weight": 46.07,
    "logp": -0.31,
    "tpsa": 20.23,
    "lipinski_violations": 0,
    "drug_likeness_score": 0.85,
    "toxicity_prediction": "Low Risk"
  },
  "structure_3d": {
    "atoms": [...],
    "bonds": [...]
  },
  "structure_2d": "data:image/png;base64,..."
}
```

### GET /api/examples
Get a list of example molecules for demonstration.

### POST /api/search
Search for molecules by name or properties.

## Molecular Properties Explained

### Basic Properties
- **Molecular Weight**: Total mass of the molecule (g/mol)
- **LogP**: Partition coefficient (lipophilicity measure)
- **TPSA**: Topological Polar Surface Area (Ų)
- **H-Bond Donors/Acceptors**: Number of hydrogen bond donors and acceptors

### Drug-likeness Metrics
- **Lipinski's Rule of Five**: Drug-likeness criteria
  - Molecular weight ≤ 500 Da
  - LogP ≤ 5
  - H-bond donors ≤ 5
  - H-bond acceptors ≤ 10
- **Drug-likeness Score**: Composite score (0-1) indicating drug-like properties
- **Toxicity Prediction**: Risk assessment based on structural alerts

## Development

### Project Structure
```
chemai/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # CSS styles
│   └── script.js         # JavaScript functionality
└── README.md             # Project documentation
```

### Adding New Features
1. **New molecular descriptors**: Add calculations in the `ChemicalAnalysisAI` class
2. **Additional ML models**: Extend the `_initialize_models` method
3. **Visualization styles**: Add new cases in the `setMoleculeStyle` function
4. **API endpoints**: Add new routes in `app.py`

### Machine Learning Models
The application uses several ML approaches:
- **Random Forest**: For property prediction (molecular weight, LogP, etc.)
- **Molecular Fingerprints**: Morgan fingerprints for feature extraction
- **Structural Alerts**: Rule-based toxicity prediction
- **Descriptor Calculation**: RDKit-based molecular descriptors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **RDKit**: Open-source cheminformatics toolkit
- **3Dmol.js**: WebGL-based molecular visualization library
- **Scientific Community**: For advancing computational chemistry and drug discovery

## Support

For questions, issues, or feature requests, please open an issue on the project repository.

---

**Disclaimer**: This tool is for research and educational purposes. Results should not be used as the sole basis for drug development or toxicity assessment without proper experimental validation.