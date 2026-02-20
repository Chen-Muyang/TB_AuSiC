import numpy as np

# 读取之前保存的数据
data = np.load('wannier_data.npz')
nbands = int(data['nbands'])
NRPTS = int(data['NRPTS'])
wannierdata = data['wannierdata']

# 从原始文件读取degeneracy values
filename = "nbands120-wannier90_hr.dat"
with open(filename, 'r') as f:
    lines = f.readlines()

# 计算startingLine
import math
ndegen_lines = math.ceil(NRPTS / 15)
startingLine = 3 + ndegen_lines

# 提取degVals (第4行到startingLine-1行的所有数值)
degVals = []
for i in range(3, startingLine):  # Python索引：3对应Mathematica的4
    values = lines[i].strip().split()
    degVals.extend([int(v) for v in values])

degVals = np.array(degVals)
print(f"degVals shape: {degVals.shape}")
print(f"degVals前几个值: {degVals[:10]}")

# 计算NHam
NHam = nbands ** 2
print(f"NHam = {NHam}")

# 构建Hdeg: 对每个R点，创建长度为NHam的数组，值为1/degVals[i]
# Dimensions: (NRPTS, NHam)
Hdeg = np.array([np.full(NHam, 1.0/degVals[i]) for i in range(len(degVals))])
print(f"Hdeg shape: {Hdeg.shape}")
print(f"Hdeg[0, 0] = {Hdeg[0, 0]}")

# LatticeVectors: 提取前3列并重塑为 (NRPTS, NHam, 3)
# wannierdata的前3列是R点坐标
LatticeVectors = wannierdata[:, 0:3].reshape(NRPTS, NHam, 3).astype(int)
print(f"\nLatticeVectors shape: {LatticeVectors.shape}")
print(f"LatticeVectors[0] shape: {LatticeVectors[0].shape}")
print(f"LatticeVectors[0, 0]: {LatticeVectors[0, 0]}")
print(f"LatticeVectors[0, 1]: {LatticeVectors[0, 1]}")
print(f"LatticeVectors[1, 0]: {LatticeVectors[1, 0]}")

# Hopping: 提取第6、7列（实部和虚部），构建复数矩阵
# 重塑为 (NRPTS, NHam)
real_part = wannierdata[:, 5]
imag_part = wannierdata[:, 6]
Hopping = (real_part + 1j * imag_part).reshape(NRPTS, NHam)
print(f"\nHopping shape: {Hopping.shape}")
print(f"Hopping[0] shape: {Hopping[0].shape}")
print(f"Hopping[0, 0] = {Hopping[0, 0]}")

# HamMatrixElement: 将Hdeg和Hopping逐元素相乘
# 这应用了简并度权重到跃迁矩阵元
HamMatrixElement = Hdeg * Hopping
print(f"\nHamMatrixElement shape: {HamMatrixElement.shape}")
print(f"HamMatrixElement[0] shape: {HamMatrixElement[0].shape}")
print(f"HamMatrixElement[0, 0] = {HamMatrixElement[0, 0]}")

# 保存所有处理后的数据
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

print("\n所有处理后的数据已保存到 wannier_processed.npz")