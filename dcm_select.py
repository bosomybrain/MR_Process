import os
import shutil
import whether_have_nii

'''
funtion name:dcm_select_labeled
input:root_path,output_path（所有患者文件夹地址，处理好的数据保存的位置）
output:none
将有标签的dcm目标图像（序号为701015文件夹和601015文件夹）全部整理到output_path下
'''
def dcm_select_labeled(root_path,output_path,target_name):
    for root, dir, file in os.walk(root_path):
        split_root = root.split('\\')  # 通过\\来进行截断
        if (split_root[-1]) == "701015" or (split_root[-1]) == "601015":
            root_patient = '.'
            for i in range(1,len(split_root)-2):
                root_patient = root_patient + '/' + split_root[i]#判断该患者是否有nii
            # print(root_patient)
            answer = whether_have_nii.whether_have_nii(root_patient, target_name)
            print(root_patient + "地址患者的nii分割存在结果是：" )
            print(answer)
            if answer == 1:
                    for f in file:
                        split_file = f.split('_')
                        f_old_path = os.path.join(root, f)
                        # 找到放了T2W_TSE的文件夹，复制里面的所有文件，并修改名称
                        f_new_name = split_root[-3] + '_T2W_TSE_' + split_file[-1]
                        # 保存图片到新路径
                        f_new_path = os.path.join(output_path, f_new_name)
                        shutil.copy(f_old_path, f_new_path)
'''
funtion name:dcm_select_unlabeled
input:root_path,output_path（所有患者文件夹地址，处理好的数据保存的位置）
output:none
将无标签的dcm目标图像（序号为701015文件夹和601015文件夹）全部整理到output_path下
'''
def dcm_select_unlabeled(root_path,output_path,target_name):
    for root, dir, file in os.walk(root_path):
        split_root = root.split('\\')  # 通过\\来进行截断
        if (split_root[-1]) == "701015" or (split_root[-1]) == "601015":
            root_patient = '.'
            for i in range(1,len(split_root)-2):
                root_patient = root_patient + '/' + split_root[i]#判断该患者是否有nii
            # print(root_patient)
            answer = whether_have_nii.whether_have_nii(root_patient, target_name)
            print(root_patient + "地址患者的nii分割存在结果是：" )
            print(answer)
            if answer == 0:
                    for f in file:
                        split_file = f.split('_')
                        f_old_path = os.path.join(root, f)
                        # 找到放了T2W_TSE的文件夹，复制里面的所有文件，并修改名称
                        f_new_name = split_root[-3] + '_T2W_TSE_' + split_file[-1]
                        # 保存图片到新路径
                        f_new_path = os.path.join(output_path, f_new_name)
                        shutil.copy(f_old_path, f_new_path)

'''
funtion name:dcm_select_all
input:root_path,output_path（所有患者文件夹地址，处理好的数据保存的位置）
output:none
将所有的dcm目标图像（序号为701015文件夹和601015文件夹）全部整理到output_path下
'''
def dcm_select_all(root_path,output_path):
    for root, dir, file in os.walk(root_path):
        split_root = root.split('\\')  # 通过\\来进行截断
        if (split_root[-1]) == "701015" or (split_root[-1]) == "601015":
            print('patient_' + split_root[-3] + ' pictures are storing')
            # 下面是修改名称的部分，按需来写
            for f in file:
                split_file = f.split('_')
                f_old_path = os.path.join(root, f)
                # 找到放了T2W_TSE的文件夹，复制里面的所有文件，并修改名称
                f_new_name = split_root[-3] + '_T2W_TSE_' + split_file[-1]
                # 保存图片到新路径
                f_new_path = os.path.join(output_path, f_new_name)
                shutil.copy(f_old_path, f_new_path)


if __name__ == '__main__':
    # dicom文件目录
    target_name = "Untitled.nii.gz"
    root_path = r'.\patient_group' #dcm原文件夹路径
    output_path = r'.\unlabeled_results' #最后输出的dcm文件夹路径
    output_path1 = r'.\labeled_results'
    # dcm_select_all(root_path,output_path)
    dcm_select_unlabeled(root_path, output_path, target_name)
    dcm_select_labeled(root_path, output_path1, target_name)