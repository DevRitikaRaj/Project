# Chem AI Analyzer

A minimal AI app for chemical analysis with 3D molecular visualization and a demo solubility predictor.

## Features
- Input SMILES, generate a 3D conformer, and view in 3D (sticks + surface)
- Compute basic descriptors (MW, TPSA, HBD/HBA, rotatable bonds, rings, LogP, FractionCSP3)
- Train/load a lightweight Ridge model on Morgan fingerprints to predict a demo solubility value (using a small sample dataset)

## Quickstart

1) Install dependencies (Python 3.9+ recommended):
```bash
python -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2) Run the Streamlit app:
```bash
streamlit run chem_app/streamlit_app.py
```

3) Open the provided URL in your browser. Enter a SMILES such as `CCO` and click Analyze.

## Notes
- RDKit is provided via prebuilt wheels (`rdkit-pypi`). If installation fails on your platform, ensure you have a manylinux-compatible environment or consult RDKit install docs.
- The "demo solubility" model is trained on a tiny sample dataset for illustration and is not scientifically validated. Replace `chem_app/data/demo_solubility.csv` with your dataset (columns: `smiles,solubility`) to train on real data.