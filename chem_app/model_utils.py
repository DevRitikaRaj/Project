from typing import Optional, Tuple, Dict
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from rdkit import Chem
from .chem_utils import morgan_fingerprint

MODEL_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
MODEL_PATH = os.path.join(MODEL_DIR, "ridge_morgan.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "demo_solubility.csv")


def _smiles_to_features(smiles_series: pd.Series, n_bits: int = 2048):
	features = []
	valid_idx = []
	for idx, smi in smiles_series.items():
		mol = Chem.MolFromSmiles(smi)
		if mol is None:
			continue
		fp = morgan_fingerprint(mol, n_bits=n_bits)
		features.append(fp)
		valid_idx.append(idx)
	import numpy as np
	X = np.vstack(features)
	return X, valid_idx


def load_or_train_model(force: bool = False):
	os.makedirs(MODEL_DIR, exist_ok=True)
	if os.path.exists(MODEL_PATH) and not force:
		model = joblib.load(MODEL_PATH)
		return model, {"status": "loaded"}
	# load data
	df = pd.read_csv(DATA_PATH)
	X, valid_idx = _smiles_to_features(df["smiles"])
	y = df.loc[valid_idx, "solubility"].values
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
	model = Ridge(alpha=1.0, random_state=42)
	model.fit(X_train, y_train)
	pred = model.predict(X_test)
	rmse = mean_squared_error(y_test, pred, squared=False)
	joblib.dump(model, MODEL_PATH)
	return model, {"status": "trained", "rmse": float(rmse), "n_train": int(len(X_train)), "n_test": int(len(X_test))}


def predict_solubility(smiles: str, model: Optional[Ridge] = None) -> Optional[float]:
	if model is None:
		model, _ = load_or_train_model(force=False)
	mol = Chem.MolFromSmiles(smiles)
	if mol is None:
		return None
	import numpy as np
	X = morgan_fingerprint(mol)[None, :]
	return float(model.predict(X)[0])