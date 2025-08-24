import os
import sys
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import py3Dmol

from chem_utils import mol_from_smiles, generate_3d_conformer, mol_to_sdf_block, compute_basic_properties
from model_utils import load_or_train_model, predict_solubility

st.set_page_config(page_title="Chem AI Analyzer", layout="wide")

st.title("Chemical Analysis and 3D Visualization")
st.caption("Enter a SMILES string, analyze properties, visualize 3D, and predict a demo solubility.")

with st.sidebar:
	smiles = st.text_input("SMILES", value="CCO", help="Enter a valid SMILES string, e.g., CCO for ethanol")
	force_train = st.checkbox("Force retrain demo model", value=False)
	analyze = st.button("Analyze")

if analyze and smiles:
	mol = mol_from_smiles(smiles)
	if mol is None:
		st.error("Invalid SMILES. Please try again.")
		st.stop()
	mol3d = generate_3d_conformer(mol)
	mb = mol_to_sdf_block(mol3d)
	view = py3Dmol.view(width=640, height=480)
	view.addModel(mb, 'sdf')
	view.setStyle({'stick': {}})
	view.addSurface(py3Dmol.VDW, {'opacity': 0.1})
	view.zoomTo()
	st.subheader("3D Structure")
	st.components.v1.html(view._make_html(), height=500, scrolling=False)

	st.subheader("Computed Properties")
	props = compute_basic_properties(mol3d)
	st.json(props)

	st.subheader("Demo Model Prediction")
	with st.spinner("Loading/training model..."):
		model, info = load_or_train_model(force=force_train)
		if info.get("status") == "trained":
			st.info(f"Trained demo model: RMSE={info.get('rmse', float('nan')):.3f} (n={info.get('n_train', 0)} train / {info.get('n_test', 0)} test)")
		else:
			st.success("Loaded pre-trained demo model")
	pred = predict_solubility(smiles, model)
	st.metric("Predicted demo solubility (a.u.)", f"{pred:.3f}")

st.write("")
st.markdown(
	"""
	- The 3D conformer is generated using RDKit ETKDG and MMFF/UFF optimization.
	- The demo model uses Morgan fingerprints and a Ridge regressor trained on a small sample dataset. Replace the dataset with your own for meaningful results.
	"""
)