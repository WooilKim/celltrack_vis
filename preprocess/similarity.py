import json


def calculate_sim():
    datas = ['BF-C2DL-HSC-01', 'BF-C2DL-HSC-02']
    for data in datas:
        algs = ['KIT-Sch-GE', 'MU-Lux-CZ']
        for alg in algs:

            path = f'../celltrack_vis/static/celltrack_vis/data/celltracking_results/{data}/{alg}/'
            file = 'SEG.json'
            with open(path + file, 'r') as json_file:
                json_data = json.load(json_file)
                print(json_data)


if __name__ == '__main__':
    calculate_sim()
