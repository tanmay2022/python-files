import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def graingrowth(file_name,z_section,is3d):

    f = h5py.File(file_name, 'r')

    #print(list(f.keys()))

    # Reading EulerAngles from Dream3d output
    #dset = f['DataContainers/SyntheticVolumeDataContainer/CellData/IPFColor']
    dset = f['DataContainers/SyntheticVolumeDataContainer/CellData/EulerAngles']

    cube_dimension = dset.shape
    print('Dimension: '+str(cube_dimension[0])+', '+str(cube_dimension[1])+', '+str(cube_dimension[2]))

    #print(dset.dtype)

    z_section = int(z_section*cube_dimension[0]/100)
    print('Layer # from bottom: '+str(z_section))

    # Euler angle components
    if is3d == 0:
        temp2 = dset[z_section,0:cube_dimension[1],0:cube_dimension[2],2]
        states_mat = temp2[cube_dimension[1]:0:-1,0:cube_dimension[2]]
        plot_mat = states_mat
    
    if is3d == 1:
        temp2 = dset[0:cube_dimension[0],0:cube_dimension[1],0:cube_dimension[2],2]
        states_mat = temp2.reshape(cube_dimension[0]*cube_dimension[1],cube_dimension[2])
        plot_mat = temp2[cube_dimension[0]-1,cube_dimension[1]:0:-1,0:cube_dimension[2]]

    #test_list = [[4, 5, 6], [2, 4, 5], [6, 7, 5]]
    
    # printing original list
    #print("The original list is : " + str(states_mat))
    
    # Matrix elements Frequencies Counter
    # using Counter() + sum() + map()
    res = dict(sum(map(Counter, states_mat), Counter()))

    # printing result 
    #print ("The frequencies dictionary is : " + str(res))

    return plot_mat, res

# Output Dream3D file
file_name = sys.argv[1]

# Layer from bottom at % of total thickness
z_section = float(sys.argv[2])

is3d = int(sys.argv[3])

plot_mat, res = graingrowth(file_name,z_section,is3d)

if is3d == 0:
    plt.matshow(plot_mat, cmap='turbo')
    plt.title('Euler_Angle(2)')
    plt.colorbar()
    plt.show()

if is3d == 1:
    plt.matshow(plot_mat, cmap='turbo')
    plt.title('Euler_Angle(2)')
    plt.colorbar()
    plt.show()

#names = list(res.keys())
values = list(res.values())

print('Total cells: '+str(np.sum(values)))

plt.bar(range(len(res)), values)
#, tick_label=names)
plt.show()

