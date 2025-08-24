from typing import Optional, Dict, Any
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors


def mol_from_smiles(smiles: str) -> Optional[Chem.Mol]:
	mol = Chem.MolFromSmiles(smiles)
	if mol is None:
		return None
	mol = Chem.AddHs(mol)
	return mol


def generate_3d_conformer(mol: Chem.Mol, seed: int = 0) -> Chem.Mol:
	params = AllChem.ETKDGv3()
	params.randomSeed = seed
	AllChem.EmbedMolecule(mol, params)
	try:
		AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
	except Exception:
		try:
			AllChem.UFFOptimizeMolecule(mol, maxIters=200)
		except Exception:
			pass
	return mol


def mol_to_sdf_block(mol: Chem.Mol) -> str:
	return Chem.MolToMolBlock(mol)


def compute_basic_properties(mol: Chem.Mol) -> Dict[str, Any]:
	properties: Dict[str, Any] = {
		"MolecularWeight": Descriptors.MolWt(mol),
		"TPSA": rdMolDescriptors.CalcTPSA(mol),
		"NumHDonors": rdMolDescriptors.CalcNumHBD(mol),
		"NumHAcceptors": rdMolDescriptors.CalcNumHBA(mol),
		"NumRotatableBonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
		"RingCount": rdMolDescriptors.CalcNumRings(mol),
		"CrippenLogP": Descriptors.MolLogP(mol),
		"FractionCSP3": rdMolDescriptors.CalcFractionCSP3(mol),
	}
	return properties


def morgan_fingerprint(mol: Chem.Mol, radius: int = 2, n_bits: int = 2048) -> np.ndarray:
	bitvect = AllChem.GetMorganFingerprintAsBitVect(Chem.RemoveHs(mol), radius, nBits=n_bits)
	arr = np.zeros((n_bits,), dtype=np.int8)
	from rdkit import DataStructs
	DataStructs.ConvertToNumpyArray(bitvect, arr)
	return arr.astype(np.float32)