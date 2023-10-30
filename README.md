# README - Alice



## tools:

1. the file 'rename_file_batch.py'
   * 将原始收集的图像按idx重命名到目标文件夹
2. the file 'copy_file_from_A2B_one_folder.py'
   * 将通过labelme标注好的图像（有多个文件夹）拷贝到同一个文件夹下
3. the file 'label_idx_name_change.py'
   * 将同一个文件夹下的label做映射变换
   * define the k : v to config/xxx/keys : config/xxx/values


## labelmeCvt

1. the file 'labelme2yolo.py'
   * 转换同一个文件夹下的所有json文件（以及图像本身）为YOLO Train 格式