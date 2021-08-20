from os import write
import json

item_dict = {}


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
        if len(final_result[i - 1]) < entry_len - 1:
            continue
        if final_result[i - 1][entry_len - 2] == entry[-2] and final_result[i][entry_len - 2] != entry[-2]:
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

def recursive_insertion(children_array, item_list):
    for children in children_array:
        if children['name'] == str(item_list[0]):
            popped = item_list.pop(0)
            if 'children' not in children:
                children['children'] = []
            if 'name' not in children:
                children['name'] = str(popped)
            if 'start' not in children:
                children['start'] = item_dict[str(popped)]['start']
            if 'end' not in children:
                children['end'] = item_dict[str(popped)]['end']
            recursive_insertion(children['children'], item_list)
            return

    if len(item_list) == 1:
        new_child = {
            'name': str(item_list[0]),
            'start': item_dict[str(item_list[0])]['start'],
            'end': item_dict[str(item_list[0])]['end'],
        }
        children_array.append(new_child)
        return

    if len(item_list) > 1:
        popped = item_list.pop(0)
        new_child = {
            'name': str(popped),
            'children': [],
            'start': item_dict[str(popped)]['start'],
            'end': item_dict[str(popped)]['end'],
        }
        recursive_insertion(new_child['children'], item_list)
        children_array.append(new_child)
        return


def main():
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
        'PhC-C2DH-U373',
        'PhC-C2DL-PSC'
    ]

    read_url = "./celltrack_vis/static/celltrack_vis/data/celltracking_results/res_track.txt"

    read_file = open(read_url, 'r')
    lines = read_file.readlines()
    read_file.close()

    final_result = []
    final_result.append([0])

    for line in lines:
        words = line.split()

        obj = {}
        obj["start"] = int(words[1])
        obj["end"] = int(words[2])
        item_dict[words[0]] = obj

        (index, parent) = parse_line(words)
        append_to_list(index, parent, final_result)

    final_json = {"name": "0", "children": [], "start": 0, "end": 0}

    for index, item in enumerate(final_result):
        if index == 0:
            continue
        item.pop(0)
        recursive_insertion(final_json['children'], item)

    with open('./result.json', 'w') as json_file:
        json.dump(final_json, json_file)


if __name__ == '__main__':
    main()
