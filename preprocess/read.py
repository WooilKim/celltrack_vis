import tifffile as tiff
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import gdal
import copy
from collections import defaultdict
import json


# # import arcpy
# # from arcpy import env
# env.workspace = "c:/data"
# arcpy.RasterToPolyline_conversion("flowstr", "c:/output/streams.shp", "ZERO",
#                                   50, "SIMPLIFY")

def read_tiff(path):
    H = tiff.imread(path)
    # plt.imshow(H, interpolation='none')
    # plt.show()
    img = cv.imread(path)
    l = list()
    for j, y in enumerate(H):
        for i, x in enumerate(y):
            if x != 0:
                l.append([j, i, x])

    return l


def test_gdal(path):
    inputs = ['01_RES', '02_RES']
    # num_files = 1764
    num_files = 20
    # /01_RES/mask0000.tif
    img = cv.imread(path + '01_RES/mask0000.tif')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 흑백사진으로 변환
    ret, binary = cv.threshold(gray, 240, 255, 0)
    for input in inputs:
        output = path + input + '.json'
        with open(output, 'w') as output_file:
            res = list()
            for n in range(num_files):
                print(n)
                arr = tiff.imread(path + input + f'/mask{n:04d}.tif')
                d = defaultdict(list)
                for j, y in enumerate(arr):
                    for i, x in enumerate(y):
                        if x != 0:
                            d[x].append([j, i])
                poly_objs = dict()
                for key in d.keys():
                    tmp = copy.deepcopy(binary)
                    for j, i in d[key]:
                        tmp[j][i] = 1
                    contours, h = cv.findContours(tmp, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                    poly_objs[int(key)] = [c.tolist() for c in contours]
                res.append(poly_objs)
            output_file.write(json.dumps(res))
            output_file.flush()


if __name__ == '__main__':
    path = '../celltrack_vis/static/celltrack_vis/data/celltracking_results/BF-C2DL-HSC/'
    # read_tiff(path)
    test_gdal(path)
