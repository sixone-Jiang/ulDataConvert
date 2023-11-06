import os
import sys
import argparse
import shutil
import math
from collections import OrderedDict

import json
import cv2

import numpy as np
import matplotlib.pyplot as plt
import yaml
import base64

def convertyolo2labelme(yolo_image_file_path, yolo_txt_file_path, idx_name_list):
    """
        convert yolo txt file to labelme json file
        the yolo txt info like:(ratio location)
            cls_name_idx x_center y_center width height
        
        the idx_name_list like:
            ['name1', 'name2', ...]

        the labelme json file like:
            {
                "version": "5.3.1",
                "flags": {},
                "shapes": [
                    {
                        "label": "name1",
                        "points": [
                            [
                                0,
                                0
                            ],
                            [
                                0,
                                0
                            ]
                        ],
                        "group_id": null,
                        "description": "",
                        "shape_type": "rectangle",
                        "flags": {}
                    }
                ],
                "imagePath": "000000.jpg",
                "imageData": null,
                "imageHeight": 0,
                "imageWidth": 0
        
    """
    cv2_image = cv2.imread(yolo_image_file_path)
    image_height, image_width, _ = cv2_image.shape
    image_name = yolo_image_file_path.split('/')[-1].split('\\')[-1]
    imagePath = image_name
    imageData = base64.b64encode(open(yolo_image_file_path, "rb").read()).decode('utf-8')
    imageHeight = image_height
    imageWidth = image_width
    version = '5.3.1'
    labelme_json = {
        "version": version,
        "flags": {},
        "shapes": [],
        "imagePath": imagePath,
        "imageData": imageData,
        "imageHeight": imageHeight,
        "imageWidth": imageWidth
    }
    shapes = []

    # read the yolo txt file
    with open(yolo_txt_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            line_split = line.split(' ')
            cls_name_idx = int(line_split[0])
            x_center = float(line_split[1])
            y_center = float(line_split[2])
            width = float(line_split[3])
            height = float(line_split[4])
            # convert to labelme json format
            cls_name = idx_name_list[cls_name_idx]
            x1 = int((x_center - width / 2) * image_width)
            y1 = int((y_center - height / 2) * image_height)
            x2 = int((x_center + width / 2) * image_width)
            y2 = int((y_center + height / 2) * image_height)
            points = [[x1, y1], [x2, y2]]
            shape = {
                "label": cls_name,
                "points": points,
                "group_id": None,
                "description": "",
                "shape_type": "rectangle",
                "flags": {}
            }
            shapes.append(shape)
    labelme_json['shapes'] = shapes
    return labelme_json

def convert_all(start_yolo_dir, save_labelme_dir):
    train_yolo_dir = os.path.join(start_yolo_dir, 'images/train')
    train_yolo_txt_dir = os.path.join(start_yolo_dir, 'labels/train')
    val_yolo_dir = os.path.join(start_yolo_dir, 'images/val')
    val_yolo_txt_dir = os.path.join(start_yolo_dir, 'labels/val')
    test_yolo_dir = os.path.join(start_yolo_dir, 'images/test')
    test_yolo_txt_dir = os.path.join(start_yolo_dir, 'labels/test')
    if not os.path.exists(train_yolo_dir):
        os.makedirs(train_yolo_dir)
    if not os.path.exists(train_yolo_txt_dir):
        os.makedirs(train_yolo_txt_dir)
    if not os.path.exists(val_yolo_dir):
        os.makedirs(val_yolo_dir)
    if not os.path.exists(val_yolo_txt_dir):
        os.makedirs(val_yolo_txt_dir)
    if not os.path.exists(test_yolo_dir):
        os.makedirs(test_yolo_dir)
    if not os.path.exists(test_yolo_txt_dir):
        os.makedirs(test_yolo_txt_dir)

    datasets_set = yaml.load(open(os.path.join(start_yolo_dir, 'dataset.yaml'), 'r'), Loader=yaml.FullLoader)
    idx_name_list = datasets_set['names_list']

    save_labelme_dir = os.path.join(save_labelme_dir, 'auto_label')
    if not os.path.exists(save_labelme_dir):
        os.makedirs(save_labelme_dir)
    
    # get all yolo image file path and yolo txt file path
    train_yolo_image_file_path_list = []
    train_yolo_txt_file_path_list = []
    val_yolo_image_file_path_list = []
    val_yolo_txt_file_path_list = []
    test_yolo_image_file_path_list = []
    test_yolo_txt_file_path_list = []
    for file_name in os.listdir(train_yolo_dir):
        if file_name.split('.')[-1] in ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG']:
            train_yolo_image_file_path_list.append(os.path.join(train_yolo_dir, file_name))
    for file_name in os.listdir(train_yolo_txt_dir):
        if file_name.split('.')[-1] in ['txt']:
            train_yolo_txt_file_path_list.append(os.path.join(train_yolo_txt_dir, file_name))
    for file_name in os.listdir(val_yolo_dir):
        if file_name.split('.')[-1] in ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG']:
            val_yolo_image_file_path_list.append(os.path.join(val_yolo_dir, file_name))
    for file_name in os.listdir(val_yolo_txt_dir):
        if file_name.split('.')[-1] in ['txt']:
            val_yolo_txt_file_path_list.append(os.path.join(val_yolo_txt_dir, file_name))
    for file_name in os.listdir(test_yolo_dir):
        if file_name.split('.')[-1] in ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG']:
            test_yolo_image_file_path_list.append(os.path.join(test_yolo_dir, file_name))
    for file_name in os.listdir(test_yolo_txt_dir):
        if file_name.split('.')[-1] in ['txt']:
            test_yolo_txt_file_path_list.append(os.path.join(test_yolo_txt_dir, file_name))
    
    # convert train yolo to labelme
    # for yolo_image_file_path, yolo_txt_file_path in zip(train_yolo_image_file_path_list, train_yolo_txt_file_path_list):
    #     labelme_json = convertyolo2labelme(yolo_image_file_path, yolo_txt_file_path, idx_name_list)
    #     file_name = yolo_image_file_path.split('/')[-1].split('\\')[-1].split('.')[0]
    #     labelme_json_file_path = os.path.join(save_labelme_dir, file_name + '.json')
    #     with open(labelme_json_file_path, 'w') as f:
    #         json.dump(labelme_json, f, indent=4)
    #     print('convert', yolo_image_file_path, 'to', labelme_json_file_path)
    #     # copy image
    #     shutil.copy(yolo_image_file_path, os.path.join(save_labelme_dir, file_name + '.jpg'))
    
    # convert val yolo to labelme
    for yolo_image_file_path, yolo_txt_file_path in zip(val_yolo_image_file_path_list, val_yolo_txt_file_path_list):
        labelme_json = convertyolo2labelme(yolo_image_file_path, yolo_txt_file_path, idx_name_list)
        file_name = yolo_image_file_path.split('/')[-1].split('\\')[-1].split('.')[0]
        labelme_json_file_path = os.path.join(save_labelme_dir, file_name + '.json')
        with open(labelme_json_file_path, 'w') as f:
            json.dump(labelme_json, f, indent=4)
        print('convert', yolo_image_file_path, 'to', labelme_json_file_path)
        shutil.copy(yolo_image_file_path, os.path.join(save_labelme_dir, file_name + '.jpg'))
    
    # convert test yolo to labelme
    for yolo_image_file_path, yolo_txt_file_path in zip(test_yolo_image_file_path_list, test_yolo_txt_file_path_list):
        labelme_json = convertyolo2labelme(yolo_image_file_path, yolo_txt_file_path, idx_name_list)
        file_name = yolo_image_file_path.split('/')[-1].split('\\')[-1].split('.')[0]
        labelme_json_file_path = os.path.join(save_labelme_dir, file_name + '.json')
        with open(labelme_json_file_path, 'w') as f:
            json.dump(labelme_json, f, indent=4)
        print('convert', yolo_image_file_path, 'to', labelme_json_file_path)
        shutil.copy(yolo_image_file_path, os.path.join(save_labelme_dir, file_name + '.jpg'))

if __name__=='__main__':
    start_dir = '../datasets/merge_all/tzc_all'
    save_labelme_dir = '../datasets/merge_all/labelme_auto'
    convert_all(start_dir, save_labelme_dir)