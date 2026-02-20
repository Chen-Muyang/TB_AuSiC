# Reading .npz file I got from DFT
```python
file_npz = np.load("data.npz")
kpoints = file_npz["kpoints"]
    # kpoints cartesian coordinates, shape=(n_kpoints, 3)
eigenval = file_npz["eigenval"]
    # eigenvalues, shape=(n_kpoints, n_bands, n_props, n_spin)
    # n_props=2 for eigenvalues (0), occupation (1)
procar = file_npz["procar"]
    # procar, shape=(n_kpoints, n_bands, n_atoms, n_orbitals, n_spins)
    # n_orbitals=10 (or 17)
        # 0  1  2  3   4   5   6   7     8 (    9   10   11  12  13   14  15)  16
        # s py pz px dxy dyz dz2 dxz x2-y2 (fy3x2 fxyz fyz2 fz3 fz2 fzx2 fx3) tot
```

# My choice of initial projections for Wannierization
Au: s, p, dz2, dx2-y2, dxy  
top Si: pz  
After wannierization, Wannier functions look like (see .xsf files):
1. Au sp2 hybrid（1/sqrt(3) s + 1/sqrt(2) px + 1/sqrt(6) py）
2. Au sp2 hybrid（1/sqrt(3) s - 2/sqrt(6) py）
3. Au pz
4. Au sp2 hybrid（1/sqrt(3) s - 1/sqrt(2) px + 1/sqrt(6) py）
5. Au dz2
6. Au dx2-y2
7. Au dxy
8. Si pz

# Reading wannier90_hr.dat
Ignore the first block.
In the main data block, one example line is:  
```-16   -9    0    2    1   -0.000235   -0.000004```  
meaning $\vec{R} = (-16,-9,0)$ and $\left<2\vec{0}|H|1\vec{R}\right> = -0.000235-0.000004j$