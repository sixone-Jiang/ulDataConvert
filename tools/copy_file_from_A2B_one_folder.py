import os
import shutil
import tqdm

'''
labelme output folder like:
    ./labelme_output/cls_name/xxxxx.json
    ./labelme_output/cls_name/xxxxx.jpg
    ...

In some case, we only have one folder, but this folder has many sub-folder
    In this case, the cls_name is not important, we just need to copy all the file to one folder
'''

def copy_labelme_output_image_to_one_folder(start_dir, output_dir):
    # get the class name
    cls_name_list = os.listdir(start_dir)
    for cls_name in cls_name_list:
        # get the file name
        file_name_list = os.listdir(os.path.join(start_dir, cls_name))
        for file_name in file_name_list:
            # get the file type
            file_type = file_name.split('.')[-1]
            # fix bug, make dir
            # if not os.path.exists(os.path.join(output_dir, cls_name)):
            #     os.makedirs(os.path.join(output_dir, cls_name))
            # rename the file
            #os.system('cp ' + os.path.join(start_dir, cls_name, file_name) + ' ' + os.path.join(output_dir, cls_name, cls_name + '_' + str(idx) + '.png'))
            # fix bug, use shutil
            shutil.copy(os.path.join(start_dir, cls_name, file_name), os.path.join(output_dir, file_name))
            print(os.path.join(start_dir, cls_name, file_name), '->', os.path.join(output_dir, file_name))

def copy_labelme_output_json_to_one_folder(start_dir, output_dir):
    # get the class name
    cls_name_list = os.listdir(start_dir)
    for cls_name in cls_name_list:
        # get the file name
        file_name_list = os.listdir(os.path.join(start_dir, cls_name))
        for file_name in file_name_list:
            # get the file type
            file_type = file_name.split('.')[-1]
            # fix bug, make dir
            # if not os.path.exists(os.path.join(output_dir, cls_name)):
            #     os.makedirs(os.path.join(output_dir, cls_name))
            # rename the file
            #os.system('cp ' + os.path.join(start_dir, cls_name, file_name) + ' ' + os.path.join(output_dir, cls_name, cls_name + '_' + str(idx) + '.png'))
            # fix bug, use shutil
            shutil.copy(os.path.join(start_dir, cls_name, file_name), os.path.join(output_dir, file_name))
            print(os.path.join(start_dir, cls_name, file_name), '->', os.path.join(output_dir, file_name))


if __name__ == '__main__':
    image_start_dir = '../datasets/all_labeled'
    image_output_dir = '../datasets/merge_all' # this dir is output to use labelme
    
    json_start_dir = '../datasets/all_labeled'
    json_output_dir = '../datasets/merge_all' # this dir is output to use labelme

    if not os.path.exists(image_output_dir):
        os.makedirs(image_output_dir)
    
    if not os.path.exists(json_output_dir):
        os.makedirs(json_output_dir)

    print('---------Starting Copy Image---------')
    copy_labelme_output_image_to_one_folder(image_start_dir, image_output_dir)
    print('---------Starting Copy Json---------')
    copy_labelme_output_json_to_one_folder(json_start_dir, json_output_dir)