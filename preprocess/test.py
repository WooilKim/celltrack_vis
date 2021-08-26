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
            if algorithm == 'input':
                continue
            fw.writerow([index, algorithm])
            index += 1

        f.close()
    # ids.csv does not exist
    else:
        f = open(ids, 'w')
        fw = csv.writer(f)
        fw.writerow(['id','name'])

        index = 0
        for algorithm in algorithms:
            if algorithm == 'input':
                continue
            fw.writerow([index, algorithm])
            index += 1

        f.close()
    pass


def jaccard(dataset):
    # TODO : wrtie {id_a}_{id_b}.csv (t, sim) between existing algorithms (id_a) and new algorithm (id_b)
    """

    0_1.csv
    0, 30,
    0,
    """
    base_url = 'data/celltracking_results/' + dataset
    csv_name = '/ids.csv'
    
    ids = base_url + csv_name

    algorithms = []

    if Path(ids).is_file():
        f = open(ids, 'r')
        fr = list(csv.reader(f))
        f.close()
        algorithms = fr[1:]
    else:
        algorithms = []
        for (_, dirnames, _) in os.walk(base_url):
            algorithms.extend(dirnames)
            break
        if 'input' in algorithms:
            algorithms.remove('input')
            
    algo_len = len(algorithms)
    for i in range(0, algo_len):
        for j in range(i+1, algo_len):
            outer_algorithm = algorithms[i][1]
            inner_algorithm = algorithms[j][1]

            # for 01_RES and 02_RES
            for k in range(2): 
                write_url = base_url + '/' + str(i) + '_' + str(j) + '_0' + str(k + 1) + '_RES.csv'
                f = open(write_url, 'w', newline='')
                wr = csv.writer(f)

                tif_count = 0
                outer_dirname = base_url + '/' + outer_algorithm + '/0' + str(k + 1) + '_RES'
                inner_dirname = base_url + '/' + inner_algorithm + '/0' + str(k + 1) + '_RES'

                for file in os.listdir(outer_dirname):
                    if file.endswith(".tif"):
                        tif_count += 1
                
                length = len(str(tif_count))

                denominator = 0
                numerator = 0

                for l in range(tif_count):
                    tif_name = '/mask' + str(l).zfill(length) + '.tif'

                    outer_tif_name = outer_dirname + tif_name
                    inner_tif_name = inner_dirname + tif_name

                    if not Path(outer_tif_name).is_file() or not Path(inner_tif_name).is_file():
                        wr.writerow([l, -1])
                        continue

                    a = tiff.imread(outer_tif_name)
                    b = tiff.imread(inner_tif_name)

                    for x_index, x in enumerate(a):
                        for y_index, y in enumerate(x):
                            if (y == 0) and (b[x_index][y_index] == 0):
                                continue
                            else:
                                denominator += 1
                                if y == b[x_index][y_index]:
                                    numerator += 1
                    
                    if denominator == 0:
                        wr.writerow([l, 0])
                    else:
                        wr.writerow([l, numerator/denominator])
                
                f.close()
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
    jaccard('BF-C2DL-HSC')
    test()
