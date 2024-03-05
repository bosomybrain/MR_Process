import dcm_select
import dcm2png
import muti_png2nii
import nii2mask2d
import mask2bbox
import clear_folder

if __name__ == '__main__':


    # clear_folder.del_file(r'.\label_process_results\yolo_data\image')
    # clear_folder.del_file(r'.\label_process_results\yolo_data\label')
    # clear_folder.del_file(r'.\label_process_results\yolo_data\none_empty_label')
    # clear_folder.del_file(r'.\label_process_results\yolo_data\none_empty_image')
    # clear_folder.del_file(r'.\label_process_results\Unet_data')

    target_name = "Untitled.nii.gz"  # nii文件的名称
    root_path = './patient_group'  # 全部患者文件夹路径
    output_path_all = './dcm_select_all/dcm'
    output_path_all_png = './dcm_select_all/png'
    output_path_unlabeled = './unlabeled_results/dcm' # 最后输出的dcm文件夹路径
    output_path_unlabeled_png = './unlabeled_results/png'
    output_path_labeled = './labeled_results/dcm'
    output_path_labeled_png = './labeled_results/png'
    #nii生成参数
    label_path = './labeled_results/png'
    output_path = './patient_group'
    # output_path_unlabeled = r'.\test'
    # nii比较结果
    masknii = "Untitled.nii.gz"
    picturenii = "mr_data.nii.gz"
    target_folder = "./label_process_results/results_compare/"



    clear_folder.del_all()
    #把文件夹里的目标dcm以及转换后的png放到指定文件夹
    dcm_select.dcm_select_all(root_path, output_path_all)# 将全部目标dcm输出到output_path_all
    dcm_select.dcm_select_unlabeled(root_path, output_path_unlabeled, target_name)# 将全部目标dcm输出到output_path_unlabeled
    dcm_select.dcm_select_labeled(root_path, output_path_labeled, target_name)# 将全部目标dcm输出到output_path_labeled
    # 可以通过output_path_all = output_path_unlabeled + output_path_labeled 检查文件数目是否有问题
    dcm2png.dcm2png(output_path_all,output_path_all_png)
    print("dcm2png_all finished")
    dcm2png.dcm2png(output_path_unlabeled, output_path_unlabeled_png)
    print("dcm2png_unlabeled finished")
    dcm2png.dcm2png(output_path_labeled, output_path_labeled_png)
    print("dcm2png_labeled finished")

    #生成多png转nii文件，并放到对应的患者文件夹里面
    muti_png2nii.muti_png2nii_all(label_path, output_path)
    print("png2nii finished")

    #nii转2d比较，放到比较结果中
    # nii2mask2d.nii2mask2d_all(root_path, masknii, picturenii, target_folder)  # 多患者放在label
    nii2mask2d.nii2mask2d_all_4png(root_path, masknii, picturenii, target_folder) #直接从labeled_results拉取4通道png数据
    print("nii2mask2d_all_4png finished")

    #处理好的数据输出Unet和yolo数据
    mask2bbox.process_yolov5_and_Unet_data_together(target_folder)#全部归为一类
    # # mask2bbox.process_yolov5_and_Unet_data_respective(target_folder)#按照颜色分类

