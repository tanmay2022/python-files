import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

# Output Dream3D file
file_name = sys.argv[1]

# Layer from bottom at % of total thickness
z_section = float(sys.argv[2])

f = h5py.File(file_name, 'r')

#print(list(f.keys()))

# Reading EulerAngles from Dream3d output
dset = f['DataContainers/SyntheticVolumeDataContainer/CellData/EulerAngles']

cube_dimension = dset.shape
print('Dimension: '+str(cube_dimension[0])+', '+str(cube_dimension[1])+', '+str(cube_dimension[2]))

#print(dset.dtype)

z_section = int(z_section*cube_dimension[0]/100)
print('Layer # from bottom: '+str(z_section))

# Euler angle components in 2D matrix form at the layer from bottom
temp0 = dset[z_section,0:cube_dimension[1],0:cube_dimension[2],0]
temp1 = dset[z_section,0:cube_dimension[1],0:cube_dimension[2],1]
temp2 = dset[z_section,0:cube_dimension[1],0:cube_dimension[2],2]

# Euler angle components in 2D matrix form at the layer from top
Euler_ang_mat0 = temp0[cube_dimension[1]:0:-1,0:cube_dimension[2]]
Euler_ang_mat1 = temp1[cube_dimension[1]:0:-1,0:cube_dimension[2]]
Euler_ang_mat2 = temp2[cube_dimension[1]:0:-1,0:cube_dimension[2]]

# Printing Euler angle component 2D matrices
with open('Euler_ang0','w') as f0:
    np.savetxt(f0, Euler_ang_mat0)
with open('Euler_ang1','w') as f1:
    np.savetxt(f1, Euler_ang_mat1)
with open('Euler_ang2','w') as f2:
    np.savetxt(f2, Euler_ang_mat2)
        

# Ploting Euler angle component 2D matrices
plt.matshow(Euler_ang_mat0, cmap='turbo')
plt.title('Euler_Angle(0)')
plt.colorbar()
plt.show()

plt.matshow(Euler_ang_mat1, cmap='turbo')
plt.title('Euler_Angle(1)')
plt.colorbar()
plt.show()

plt.matshow(Euler_ang_mat2, cmap='turbo')
plt.title('Euler_Angle(2)')
plt.colorbar()
plt.show()

