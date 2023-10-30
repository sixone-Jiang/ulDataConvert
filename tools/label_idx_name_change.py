import os
import shutil
import tqdm
import json
'''
    json file like: {
        "version": "5.3.1",
        "flags": {},
        "shapes": [
            {
            "label": "0",
            "points": [
                [
                34.63302752293578,
                53.18348623853214
                ],
                [
                521.7889908256881,
                283.45871559633025
                ]
            ],
            "group_id": null,
            "description": "",
            "shape_type": "rectangle",
            "flags": {}
            }
        ],
        "imagePath": "daodan_0.png",
        "imageData": null,
        "imageHeight": 366,
        "imageWidth": 550
    }
'''

def change_label_idx_name(start_dir, change_name_dict={}):

    json_file_list = []
    # get the json file path
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.json'):
                json_file_list.append(file)

    print('----check the json file laebel num is equal to the change_name_dict----')
    set_of_json_file_label = set()
    for json_file in json_file_list:
        file_path = os.path.join(start_dir, json_file)
        # read json file
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        # change the label name
        for shape in json_data['shapes']:
            set_of_json_file_label.add(shape['label'])
    
    if len(set_of_json_file_label) != len(change_name_dict):
        raise ValueError('The length of json file label num is not equal to the change_name_dict.')
    
    for json_file in json_file_list:
        file_path = os.path.join(start_dir, json_file)
        # read json file
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        # change the label name
        for shape in json_data['shapes']:
            #print(change_name_dict)
            if shape['label'] in change_name_dict:
                shape['label'] = change_name_dict[shape['label']]
        
        with open(file_path, 'w') as f:
            json.dump(json_data, f)


def load_dict_from_txt(key_value_dir):
    key_path = os.path.join(key_value_dir, 'keys')
    value_path = os.path.join(key_value_dir, 'values')
    change_name_dict = {}
    with open(key_path, 'r') as f:
        key_list = f.readlines()
    with open(value_path, 'r') as f:
        value_list = f.readlines()

    if len(key_list) != len(value_list):
        raise ValueError('The length of key list and value list is not equal.')

    for key, value in zip(key_list, value_list):
        change_name_dict[key.strip()] = value.strip()
    
    print('change_name_dict:', change_name_dict)
    return change_name_dict


if __name__=='__main__':
    start_dir = '../datasets/merge_all'
    change_name_dict = load_dict_from_txt('../config/tzc')

    print('---------Starting Change Label Name---------')

    change_label_idx_name(start_dir, change_name_dict)
