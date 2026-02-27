# TB_AuSiC Project

## Goal
Build an effective tight-binding model for Au on SiC from DFT Wannier functions. The main objective is to construct a k.p effective model near the K point that reproduces the DFT band structure — especially the **spin polarization** pattern visible in `dft_spin.png`, where a sudden change of spin polarization is expected near K.

## Key References
- **Theory**: `Au_on_SiC (3).pdf` — the main theoretical reference for model construction, SOC, and symmetry analysis
- **DFT data format**: `README.md` — documents orbital ordering, npz data structure, and wannier90_hr.dat format
- **DFT spin reference**: `dft_spin.png` — target band structure with spin-polarized colors (jet colormap, range [-0.8, 0.8])

## Main Notebook
All code lives in **`TB_AuSiC.ipynb`** with this structure:
- **Section 1**: Wannier TB model H(k) via Fourier transform (8-band, no SOC)
- **Section 2**: Comparison with DFT bands (no SOC)
- **Section 3**: k.p effective model expanded at K point (2nd order)
- **Section 4**: Atomic SOC — 16x16 Hamiltonian with parameters lambda1, lambda2

## Orbital Basis (8 Wannier orbitals)
1. Au sp2 hybrid (1/sqrt(3) s + 1/sqrt(2) px + 1/sqrt(6) py)
2. Au sp2 hybrid (1/sqrt(3) s - 2/sqrt(6) py)
3. Au pz
4. Au sp2 hybrid (1/sqrt(3) s - 1/sqrt(2) px + 1/sqrt(6) py)
5. Au dz2
6. Au dx2-y2
7. Au dxy
8. Si pz

## Conventions
- **k-points**: fractional coordinates (no 2*pi factor)
- **Phase convention**: H(k) = sum_R H(R)/deg(R) * exp(2*pi*i k.R)
- **High-symmetry points**: KG=[0,0,0], KK=[1/3,1/3,0], KM=[1/2,0,0], KKp=[1/3,-1/3,0]
- **Fermi energy**: EFermi = 2.71 eV (Mathematica); dft_efermi = 2.6588 eV (DFT no-SOC)
- **Lattice vectors**: a1=(3.096,0,0), a2=(-1.548,2.681215,0), a3=(0,0,20) Angstrom
- **DFT kpoints**: Cartesian with 2*pi divided out; convert via k_frac = k_DFT @ inv(B/(2*pi))
- **DFT kpath**: Gamma -> M -> K -> Gamma, 20 points per segment, 60 total

## SOC Structure
- 16x16 = 8 orbitals x 2 spins; basis: {orb1-8 up, orb1-8 down}
- **lambda1**: SOC for sp2/pz sector (orbitals 1-4), includes both LzSz and L+S-/L-S+ terms
- **lambda2**: SOC for d-orbital sector (orbitals 5-7), only LzSz survives (dxz/dyz not in basis)
- Si pz (orbital 8) has no on-site Au SOC
- Current fitted values: lambda1=0.5, lambda2=0.2 (need further tuning)

## Data Files
- `wannier_processed.npz`: preprocessed Wannier data (R-vectors, hopping, degeneracy)
- `bands_data-noSOC.npz`: DFT bands without SOC (60 kpoints, 120 bands)
- `bands_data-SOC.npz`: DFT bands with SOC (60 kpoints, 60 bands)
- `nbands120-wannier90_hr.dat`: raw Wannier90 hopping data
- `wannier90_0000X.xsf`: Wannier function visualizations

