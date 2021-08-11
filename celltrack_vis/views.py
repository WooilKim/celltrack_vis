from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
import tifffile as tiff
import matplotlib.pyplot as plt


# tiff file read
# return list of [y, x, v] if v != 0
def read_tiff(path):
    return [[j, i, x] for j, y in enumerate(tiff.imread(path)) for i, x in enumerate(y) if x != 0]


def index(request):
    context = {

    }
    return render(request, 'celltrack_vis/index.html', context)


def hyungmin(request):
    context = {

    }
    return render(request, 'celltrack_vis/hyungmin.html', context)


def segmentation(request):
    # template = loader.get_template('skyflow/index.html')
    # years = [1978 + i for i in range(39)]
    num_files = 1764
    path1 = '/Users/wooil/wooilkim-github/celltrack_vis/celltrack_vis/static/celltrack_vis/data/celltracking_results/BF-C2DL-HSC/01_RES_20.json'
    path2 = '/Users/wooil/wooilkim-github/celltrack_vis/celltrack_vis/static/celltrack_vis/data/celltracking_results/BF-C2DL-HSC/02_RES_20.json'
    res = list()
    #
    # for n in range(num_files):
    #     file = 'mask' + f'{n:04d}' + '.tif'
    #     res.append([read_tiff(path1 + file), read_tiff(path2 + file)])
    #
    # # print(path)
    context = {
        # 'res': res
    }
    print(context)
    return render(request, 'celltrack_vis/segmentation.html', context)
