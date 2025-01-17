import os
from PIL import Image
from pathlib import Path


def tif2jpg(path):
    files = os.listdir(path)
    # print(files)
    Path(f"{path}/converted").mkdir(parents=True, exist_ok=True)
    for file in files:
        if file[-3:] == 'tif':
            outfile = f'{path}/converted/{file[:-3]}jpg'
            im = Image.open(f"{path}/{file}")
            im.mode = 'I'
            im.point(lambda i: i * (1. / 256)).convert('L').save(outfile, "JPEG", quality=100)
            # im.save(outfile, "JPEG", quality=100)

    # yourpath = os.getcwd()
    # for root, dirs, files in os.walk(yourpath, topdown=False):
    #     for name in files:
    #         print(os.path.join(root, name))
    #         if os.path.splitext(os.path.join(root, name))[1].lower() == ".tiff":
    #             if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
    #             else:
    #                 outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
    #                 try:
    #                     im = Image.open(os.path.join(root, name))
    #                     im.thumbnail(im.size)
    #                     im.save(outfile, "JPEG", quality=100)
    #                 except Exception as e:
    #                     print(e)


if __name__ == '__main__':
    # tif2jpg("data/celltracking_results/BF-C2DL-HSC/input/images/01")
    algos = ["Fluo-N2DH-SIM+"]
    # algos = ["DIC-C2DH-HeLa", "Fluo-N2DH-SIM+", "PhC-C2DL-PSC"]
    path = "data/inputs/"
    for algo in algos:
        for i in range(1, 3):
            tif2jpg(f'{path}{algo}/0{i}')
