import os
import shutil

'''
    make a function to rename the file
    like : ./ori/cls_name/xxxxx.jpg (or other type) to ./copy_of_rename/cls_name/{cls_name}_{num_idx}.jpg
'''
def rename_file(start_dir, output_dir):
    # get the class name
    cls_name_list = os.listdir(start_dir)
    for cls_name in cls_name_list:
        # get the file name
        file_name_list = os.listdir(os.path.join(start_dir, cls_name))
        for idx, file_name in enumerate(file_name_list):
            # get the file type
            file_type = file_name.split('.')[-1]
            # fix bug, make dir
            if not os.path.exists(os.path.join(output_dir, cls_name)):
                os.makedirs(os.path.join(output_dir, cls_name))
            # rename the file
            os.rename(os.path.join(start_dir, cls_name, file_name), os.path.join(output_dir, cls_name, cls_name + '_' + str(idx) + '.png'))
            print(os.path.join(start_dir, cls_name, file_name), '->', os.path.join(output_dir, cls_name, cls_name + '_' + str(idx) + '.png'))

def copy_file(start_dir, output_dir):
    # get the class name
    cls_name_list = os.listdir(start_dir)
    for cls_name in cls_name_list:
        # get the file name
        file_name_list = os.listdir(os.path.join(start_dir, cls_name))
        for idx, file_name in enumerate(file_name_list):
            # get the file type
            file_type = file_name.split('.')[-1]
            # fix bug, make dir
            if not os.path.exists(os.path.join(output_dir, cls_name)):
                os.makedirs(os.path.join(output_dir, cls_name))
            # rename the file
            #os.system('cp ' + os.path.join(start_dir, cls_name, file_name) + ' ' + os.path.join(output_dir, cls_name, cls_name + '_' + str(idx) + '.png'))
            # fix bug, use shutil
            shutil.copy(os.path.join(start_dir, cls_name, file_name), os.path.join(output_dir, cls_name, cls_name + '_' + str(idx) + '.png'))
            print(os.path.join(start_dir, cls_name, file_name), '->', os.path.join(output_dir, cls_name, cls_name + '_' + str(idx) + '.png'))

if __name__ == '__main__':
    start_dir = '../datasets/ori1' # before use labelme
    output_dir = '../datasets/copy_of_rename' # this dir is output to use labelme

    print('---------Starting Rename File---------')

    copy_file(start_dir, output_dir)