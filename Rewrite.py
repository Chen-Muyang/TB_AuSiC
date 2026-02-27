import numpy as np

# read data from wannier_data.npz
data = np.load('wannier_data.npz')
nbands = int(data['nbands'])
NRPTS = int(data['NRPTS'])
wannierdata = data['wannierdata']

# Extract degeneracy values
filename = "nbands120-wannier90_hr.dat"
with open(filename, 'r') as f:
    lines = f.readlines()

import math
ndegen_lines = math.ceil(NRPTS / 15)
startingLine = 3 + ndegen_lines

# Extract degVals
degVals = []
for i in range(3, startingLine): 
    values = lines[i].strip().split()
    degVals.extend([int(v) for v in values])

degVals = np.array(degVals)
print(f"degVals shape: {degVals.shape}")
print(f"degVals前几个值: {degVals[:10]}")

NHam = nbands ** 2
print(f"NHam = {NHam}")

# Dimensions: (NRPTS, NHam)
Hdeg = np.array([np.full(NHam, 1.0/degVals[i]) for i in range(len(degVals))])
print(f"Hdeg shape: {Hdeg.shape}")
print(f"Hdeg[0, 0] = {Hdeg[0, 0]}")

# LatticeVectors: standard form
LatticeVectors = wannierdata[:, 0:3].reshape(NRPTS, NHam, 3).astype(int)
print(f"\nLatticeVectors shape: {LatticeVectors.shape}")
print(f"LatticeVectors[0] shape: {LatticeVectors[0].shape}")
print(f"LatticeVectors[0, 0]: {LatticeVectors[0, 0]}")
print(f"LatticeVectors[0, 1]: {LatticeVectors[0, 1]}")
print(f"LatticeVectors[1, 0]: {LatticeVectors[1, 0]}")

# Hopping: matrix element
# reshape to (NRPTS, NHam)
real_part = wannierdata[:, 5]
imag_part = wannierdata[:, 6]
Hopping = (real_part + 1j * imag_part).reshape(NRPTS, NHam)
print(f"\nHopping shape: {Hopping.shape}")
print(f"Hopping[0] shape: {Hopping[0].shape}")
print(f"Hopping[0, 0] = {Hopping[0, 0]}")

# HamMatrixElement: Hdeg*Hopping
HamMatrixElement = Hdeg * Hopping
print(f"\nHamMatrixElement shape: {HamMatrixElement.shape}")
print(f"HamMatrixElement[0] shape: {HamMatrixElement[0].shape}")
print(f"HamMatrixElement[0, 0] = {HamMatrixElement[0, 0]}")

# Save data to wannier_processed.npz
np.savez('wannier_processed.npz',
         nbands=nbands,
         NRPTS=NRPTS,
         NHam=NHam,
         degVals=degVals,
         Hdeg=Hdeg,
         LatticeVectors=LatticeVectors,
         Hopping=Hopping,
         HamMatrixElement=HamMatrixElement,
         wannierdata=wannierdata)

print("\nData saved to wannier_processed.npz")