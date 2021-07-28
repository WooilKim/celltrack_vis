import tifffile as tiff
import matplotlib.pyplot as plt


def read_tiff(path):
    H = tiff.imread(path)
    plt.imshow(H, interpolation='none')
    plt.show()


if __name__ == '__main__':
    path = '../celltrack_vis/static/celltrack_vis/data/celltracking_results/BF-C2DL-HSC/01_RES/mask0000.tif'
    read_tiff(path)

