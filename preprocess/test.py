import tifffile as tiff
import matplotlib.pyplot as plt

if __name__ == '__main__':
    path1 = 'data/celltracking_results/KIT-Sch-GE/BF-C2DL-HSC/01_RES/mask0000.tif'
    path2 = 'data/celltracking_results/MU-Lux-CZ/BF-C2DL-HSC/01_RES/mask0000.tif'

    a = tiff.imread(path1)
    b = tiff.imread(path1)
    fig = plt.figure()
    fig.add_subplot(1, 2, 1)
    plt.imshow(a)
    fig.add_subplot(1, 2, 2)
    plt.imshow(b)
    plt.show()
