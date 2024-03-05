import os
import shutil

import pydicom

import whether_have_nii
'''
判断一个列表中的数字是否连续
'''
def is_continuous(lst):
    #如果列表为字符串，则转化为int
    if isinstance(lst[0], str):
        lst = [int(x) for x in lst]
    # 将列表转换为集合
    s = set(lst)
    # 如果集合中的元素数量不等于列表长度，说明有重复元素
    if len(s) != len(lst):
        return False
    # 如果集合中的最小值和最大值之间的元素数量不等于列表长度，说明有缺失元素
    elif max(s) - min(s) + 1 != len(lst):
        return False
    # 如果以上两个条件都不满足，则说明列表是连续的自然数
    else:
        return True

import nibabel as nib
'''
funtion name:dcm_select_unlabeled
input:root_path,output_path（所有患者文件夹地址，处理好的数据保存的位置）
output:none
将无标签的dcm目标图像（序号为701015文件夹和601015文件夹）全部整理到output_path下
'''
def dcm_select_unlabeled(root_path,output_path,target_name):
    for root, dir, file in os.walk(root_path):
        split_root = root.split('/')  # 通过\\来进行截断
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
        split_root = root.split('/')  # 通过\\来进行截断
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

'''
funtion name:dcm_select_labeled
input:root_path,output_path（所有患者文件夹地址，处理好的数据保存的位置）
output:none
将有标签的dcm目标图像（序号为701015文件夹和601015文件夹）全部整理到output_path下
'''
def dcm_select_labeled(root_path,output_path,target_name):
    txt_file = open('dcm_select_exception_log.txt', 'w')
    print(root_path)
    root_name = root_path.split('/')[1]
    print(root_name)
    for root, dir, file in os.walk(root_path):
        print(root)
        if len(root.split('/')) == 3: # 找到每个病例的根目录地址
            num_T2W_TSE = 0
            #print(root)
            patient_root = root
            label_nii_exist = whether_have_nii.whether_have_nii(patient_root, target_name)
            if not label_nii_exist:
                txt_file.write('{} has no label'.format(patient_root) + '\n')
                print('{} has no label!!!!!!!!!!'.format(patient_root))
                shutil.move(patient_root, patient_root.replace(root_name, 'exception_patient/no_label_patient'))
        if len(root.split('/')) == 4:  # 判断T2W_TSE文件夹数目
            for d in dir:
                d_path = os.path.join(root, d)
                #print(d_path)
                sample_f  = os.listdir(d_path)[0]
                #print(sample_f)
                sample_f_old_path = os.path.join(d_path, sample_f)
                sample_f_dcm_data = pydicom.read_file(sample_f_old_path)
                sample_f_SeriesDescription = sample_f_dcm_data.SeriesDescription
                if sample_f_SeriesDescription == 'T2W_TSE':
                        num_T2W_TSE += 1
            #print(num_T2W_TSE)
            if num_T2W_TSE > 1:
                txt_file.write('{} has more than one T2W_TSE dir!!!!!!!!!!'.format(patient_root) + '\n')

                print('{} has more than one T2W_TSE dir!!!!!!!!!!'.format(patient_root))
                shutil.move(patient_root, patient_root.replace(root_name, 'exception_patient/other'))

        #print(num_T2W_TSE)
        if len(root.split('/')) == 5:  # 找到dcm文件夹目录地址
            if num_T2W_TSE == 1:
                #print('yes')
                patient_name = root.split('/')[2]
                sample_f = file[0]
                sample_f_old_path = os.path.join(root, sample_f)
                sample_f_dcm_data = pydicom.read_file(sample_f_old_path)
                f_SeriesDescription = sample_f_dcm_data.SeriesDescription
                if f_SeriesDescription == 'T2W_TSE': #dcm文件tag是否为 ‘T2W_TSE’
                    # 找出dcm文件夹里的dcm文件数字标识
                    file_digits = []
                    for f in file:
                        f_name = f.replace('.dcm', '')
                        f_digit = f_name.split('_')[-1]
                        file_digits.append(f_digit)
                    file_digits.sort()
                    # 找出dcm文件夹里的dcm文件数字标识
                    if is_continuous(file_digits): # dcm数字连续
                        for f in file:
                            f_old_path = os.path.join(root, f)
                            # 找到放了T2W_TSE的文件夹，复制里面的所有文件，并修改名称
                            f_new_name = patient_name + '_T2W_TSE_' + f.split('_')[-1]

                            # 保存图片到新路径
                            f_new_path = os.path.join(output_path, f_new_name)

                            shutil.copy(f_old_path, f_new_path)
                    else :  # dcm数字不连续

                        txt_file.write('{} dcm files are not continuous!!!!!!!!!!!!!'.format(patient_root) + '\n')

                        print('{} dcm files are not continuous!!!!!!!!!!!!!'.format(patient_root))
                        shutil.move(patient_root, patient_root.replace(root_name, 'exception_patient/not_continuous'))

    txt_file.close()


if __name__ == '__main__':
    # dicom文件目录
    target_name = "Untitled.nii.gz"
    root_path = '/patient_group' #dcm原文件夹路径
    #root_path = r'.\exception_patient' #dcm原文件夹路径
    output_path = r'.\unlabeled_results' #最后输出的dcm文件夹路径
    output_path1 = r'.\labeled_results'
    # dcm_select_all(root_path,output_path)
    #dcm_select_unlabeled(root_path, output_path, target_name)
    dcm_select_labeled(root_path, output_path1, target_name)