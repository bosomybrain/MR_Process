import os
import shutil

target_path_label = '.\label_process_results\yolo_data\label'
target_path_image = '.\label_process_results\yolo_data\image'
none_empty_label = r'.\label_process_results\yolo_data\none_empty_label'
none_empty_image = r'.\label_process_results\yolo_data\none_empty_image'

file_list = os.listdir(target_path_label)


for filename in file_list:
     #print(filename_1)
     #for txt_name in filename_1.readlines():
     #txt_name  = txt_name.strip('\n')
     #print(txt_name)
     label_path = os.path.join(target_path_label,filename)
     image_name = filename.replace('.txt', '.png')
     image_path = os.path.join(target_path_image,image_name)

     #遍历detection-results里txt的路径
     #detection_results_txt_path  = os.path.join('G:/Deep_Code/yolov4-pytorch-master/map_out/detection-results/', filename_1)
     #打开txt
     with open (label_path) as txt:
         #遍历txt的每一行
         #新建一个列表，将每个目标的像素面积放入到该列表当中
         if os.path.getsize(label_path):
             shutil.copy(label_path, os.path.join(none_empty_label,filename))
             shutil.copy(image_path, os.path.join(none_empty_image,image_name))
             print(label_path, " is not empty!")
             continue
