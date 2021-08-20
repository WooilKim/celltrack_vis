import tifffile as tiff
import matplotlib.pyplot as plt
import csv
import os
from pathlib import Path


def organize_id(dataset):
    # TODO : add new algorithms to ids.csv file (id, name)
    """

    id,name
    0,"KIT-Sch-GE"
    1,"MU"
    """
    base_url = 'data/celltracking_results/' + dataset
    csv_name = '/ids.csv'

    algorithms = []
    for (_, dirnames, _) in os.walk(base_url):
        algorithms.extend(dirnames)
        break
    
    ids = base_url + csv_name

    # ids.csv exists
    if Path(ids).is_file():
        f = open(ids, 'r')
        fr = list(csv.reader(f))
        f.close()

        index = len(fr[1:])
        current_list = []

        for row in fr[1:]:
            _, algorithm = row
            current_list.append(algorithm)
        
        difference_list = [i for i in algorithms if i not in current_list]

        f = open(ids, 'a', newline='')
        fw = csv.writer(f)

        for algorithm in difference_list:
            fw.writerow([index, algorithm])
            index += 1

        f.close()
    # ids.csv does not exist
    else:
        f = open(ids, 'w')
        fw = csv.writer(f)
        fw.writerow(['id','name'])

        for i, algorithm in enumerate(algorithms):
            fw.writerow([i, algorithm])

        f.close()
    pass


def jaccard(dataset):
    # TODO : wrtie {id_a}_{id_b}.csv (t, sim) between existing algorithms (id_a) and new algorithm (id_b)
    """

    0_1.csv
    0, 30,
    0,
    """
    pass


def test():
    path1 = 'data/celltracking_results/BF-C2DL-HSC/KIT-Sch-GE/01_RES/mask0000.tif'
    path2 = 'data/celltracking_results/BF-C2DL-HSC/MU-Lux-CZ/01_RES/mask0000.tif'

    a = tiff.imread(path1)
    # for j in a:
    #     for i in j:
    #         a[j][i] == b[j][i]
    #         v+=1

    b = tiff.imread(path1)
    fig = plt.figure()
    fig.add_subplot(1, 2, 1)
    plt.imshow(a)
    fig.add_subplot(1, 2, 2)
    plt.imshow(b)
    plt.show()


if __name__ == '__main__':
    organize_id('BF-C2DL-HSC')
    test()
