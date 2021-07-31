from os import write

dataset_list = [
  'BF-C2DL-HSC', 
  'BF-C2DL-MuSC', 
  'DIC-C2DH-HeLa', 
  'Fluo-C2DL-MSC', 
  'Fluo-C3DH-A549', 
  'Fluo-C3DH-H157', 
  'Fluo-C3DL-MDA231',
  'Fluo-N2DH-GOWT1',
  'Fluo-N2DH-SIM+',
  'Fluo-N2DL-HeLa',
  'Fluo-N3DH-CE',
  'Fluo-N3DH-CHO',
  'Fluo-N3DH-SIM+',
  'PhC-C2HD-U373',
  'PhC-C2DL-PSC'
]

dataset_list = ['BF-C2DL-HSC']

########## PARSING FUNCTIONS ##########

# returns the first and last elements from the list words
def parse_line(words):
    return (int(words[0]), int(words[3]))

# checks if entry matches any elements of final_result
def check_duplicate(entry, final_result):
    for result in final_result:
        if entry == result:
            return True
    return False

# gets the last index that has the same parent id
# if entry = [0,3,9]
# and the list goes:
# 0: [0]
# 1: [0,3]
# 2: [0,3,5]
# 3: [0,3,7]
# 4: [0,4]
# then the funciton returns 4
def get_last_index(entry, final_result):
    entry_len = len(entry)
    if entry_len < 2:
        return len(final_result)
    for i, result in enumerate(final_result):
        if i == 0:
            continue
        if len(result) < entry_len - 1:
            continue
        if len(final_result[i-1]) < entry_len - 1:
            continue
        if final_result[i-1][entry_len-2] == entry[-2] and final_result[i][entry_len-2] != entry[-2]:
            return i
    return len(final_result)

def append_to_list(index, parent, final_result):
    for i, result in enumerate(final_result):
        if result[-1] == parent:
            temp = result[:]
            temp.append(index)
            last_index = get_last_index(temp, final_result)
            final_result.insert(last_index, temp)
            break

######################################

######## CSV WRITING FUNCTIONS #######

def print_internal(entry, target):
    result_str = ""
    for item in entry:
        result_str += str(item)
        result_str += "."
    result_str = result_str.rstrip(result_str[-1])
    result_str += ",\n"
    target.write(result_str)

def print_leaf(entry, target):
    result_str = ""
    for item in entry:
        result_str += str(item)
        result_str += "."
    result_str = result_str.rstrip(result_str[-1])
    result_str += ",1000\n"
    target.write(result_str)

######################################

base_url = "./celltrack_vis/static/celltrack_vis/data/celltracking_results/"
res_track = "/res_track.txt"
parsed_track = "/parsed_track.txt"

for dataset in dataset_list:
    for res in ['01_RES','02_RES']:
        # read from url and parse the data appropriately
        read_url = base_url + dataset + "/" + res + res_track

        read_file = open(read_url, 'r')
        lines = read_file.readlines()
        read_file.close()

        final_result = []
        final_result.append([0])

        for line in lines:
            words = line.split()
            (index, parent) = parse_line(words)
            append_to_list(index, parent, final_result)

        # write the parsed data onto url
        write_url = base_url + dataset + "/" + res + parsed_track
        write_file = open(write_url, 'w')
        write_file.write('id,value\n')

        for i, result in enumerate(final_result):
            if i == len(final_result) - 1:
                print_leaf(result, write_file)
            else:
                if len(final_result[i]) < len(final_result[i+1]):
                    print_internal(result, write_file)
                else:
                    print_leaf(result, write_file)

        write_file.close()