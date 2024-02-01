文件夹介绍：
patient_group 患者文件夹（初始数据全部按照格式放这里）
unlabeled_results 没有标签的dcm，png图像
labeled_results 有标签的dcm，png图像
dcm_select_all 所有的dcm,png图像（有无标签都在）
test 随意操作
label_process_results 有标签的图像进行下一步处理，均在这个文件夹
    Unet_data 把有标签的图像处理成Unet需要的数据，分为图像和mask
              image(有6个文件夹，最多能分6类）
              mask(有6个文件夹，最多能分6类）
    yolo_data 把有标签的图像处理成Yolo需要的数据，分为图像，boundingbox图像和关于boundingbox的txt
         bounding_image 框选的效果图展示
         image 原图像
         label yolo可以直接使用的txt
尝试pull下来
