import tifffile as tiff
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import gdal
import copy
from collections import defaultdict
import json
from shapely.geometry import Polygon
import geopandas as gpd
import gdal, ogr

import subprocess
import glob
import os


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
                # poly_objs = dict()
                for key in d.keys():
                    tmp = copy.deepcopy(binary)
                    for j, i in d[key]:
                        tmp[j][i] = 1
                    contours, h = cv.findContours(tmp, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                    # image = cv.drawContours(img, contours, -1, (0, 255, 0), 1)
                    # poly_objs = []

                    # poly_objs.append(Polygon(np.squeeze(contours[0])))  # 여기

                    polygons = contours[0]
                    polygons = gpd.GeoDataFrame(polygons, columns=['geometry'])
                    polygons.to_file('star_polygons.shp')

                    #
                    # print('c0', contours[0])
                    # print('c1')
                    # for c in contours:
                    #     print(c[0])
                    # poly_objs[int(key)] = [[int(c[0][0]), int(c[0][1])] for c in contours[0]]
                # res.append(poly_objs)
            output_file.write(json.dumps(res))
            output_file.flush()


def gdal_test(path):
    in_file = path + '01_RES/mask0000.tif'
    raster = gdal.Open(in_file)
    # print(raster.RasterCount)
    band = raster.GetRasterBand(1)
    # print(band.GetMaximum())
    drv = ogr.GetDriverByName('GeoJSON')
    outfile = drv.CreateDataSource('output.json')
    outlayer = outfile.CreateLayer('polygonized raster', srs=None)
    newField = ogr.FieldDefn('DN', ogr.OFTReal)
    outlayer.CreateField(newField)
    gdal.Polygonize(band, None, outlayer, 0, [])
    outfile = None
    # dst_layername = 'polygonized_test_all_all_2.shp'
    # drv = ogr.GetDriverByName("ESRI Shapefile")
    # dst_ds = drv.CreateDataSource(dst_layername)
    # dst_layer = dst_ds.CreateLayer(dst_layername, srs=in_file)
    # fd = ogr.FieldDefn("DN", ogr.OFTInteger)
    # dst_layer.CreateField(fd)
    # dst_field = dst_layer.GetLayerDefn().GetFieldIndex("DN")
    # gdal.Polygonize(in_file, None, dst_layer, dst_field, [], callback=None)
    # out_file = "out.json"
    # in_file = path + '01_RES/mask0000.tif'
    # cmdline = ['gdal_polygonize.py', in_file, "-f", "GeoJSON", out_file]
    # subprocess.call(cmdline)


if __name__ == '__main__':
    path = '../celltrack_vis/static/celltrack_vis/data/celltracking_results/BF-C2DL-HSC/'
    # read_tiff(path)
    # test_gdal(path)
    gdal_test(path)
