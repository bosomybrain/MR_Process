import os
import shutil
import whether_have_nii

import nibabel as nib
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

'''
funtion name:dcm_select_labeled
input:root_path,output_path（所有患者文件夹地址，处理好的数据保存的位置）
output:none
将有标签的dcm目标图像（序号为701015文件夹和601015文件夹）全部整理到output_path下
'''
def dcm_select_labeled(root_path,output_path,target_name):
    txt_file = open('dcm_select_exception_log.txt', 'w')
    dcm_dir_id = ["701015", "601015", "401015"]
    for root, dir, file in os.walk(root_path):

        #dcm_nii_match_end = False  #
        #patient_root = ''
        split_root = root.split('\\')  # 通过\\来进行截断

        if target_name in file :
            label_nii_exist = True
            #print('dir',dir)
            #print('root',root)
            nii_label_addr = os.path.join(root, target_name)
            nii_label = nib.load(nii_label_addr).get_fdata()
            (x,y,z) = nii_label.shape
            #print(x,y,z)
        if len(root.split('\\')) == 3: # 找到每个病例的根目录地址
            print(root)
            patient_root = root
            label_nii_exist = whether_have_nii.whether_have_nii(patient_root, target_name)
        if len(root.split('\\')) == 4:  # 找到每个病例的根目录地址
            patient_name = root.split('\\')[2]
            dcm_dir_match_num = 0
            for id in dcm_dir_id:

                #print(id)
                dcm_dir_addr = os.path.join(root,id)
                if os.path.exists(dcm_dir_addr):
                    #print(dcm_dir_addr)
                    print(id)
                    dcm_files = os.listdir(dcm_dir_addr)
                    if len(dcm_files)== z:
                        dcm_dir_match_num += 1
                        print(dcm_dir_match_num)
                        match_id = id

            print('final dcm_dir_match_num',dcm_dir_match_num)
            if label_nii_exist  and dcm_dir_match_num == 1:
                match_dcm_dir = os.path.join(root,match_id)
                match_dcm_files = os.listdir(match_dcm_dir)
                for match_dcm_file in match_dcm_files:
                    split_file = match_dcm_file.split('_')
                    f_old_path = os.path.join(match_dcm_dir, match_dcm_file)
                    # 找到放了T2W_TSE的文件夹，复制里面的所有文件，并修改名称
                    f_new_name = patient_name + '_T2W_TSE_' + split_file[-1]
                    # 保存图片到新路径
                    f_new_path = os.path.join(output_path, f_new_name)

                    shutil.copy(f_old_path, f_new_path)
            else :  # dcm_nii匹配结束且没有找到dcm文件夹匹配nii标注

                txt_file.write('{} dcm_dir_match_num: {}'.format(patient_root, dcm_dir_match_num) + '\n')

                print('{} dcm dir match error while dcm selecting!'.format(patient_root))
                shutil.move(patient_root, patient_root.replace('patient_group', 'exception_patient'))



        # if (split_root[-1]) == "701015" or (split_root[-1]) == "601015" or (split_root[-1]) == "401015":
        #
        #     dcm_nii_match_end = True
        #     #print('root',root)
        #     #print(len(file))
        #     patient_name = root.split('\\')[-3]
        #     if len(file) == z:  #dcm文件夹下数量和nii匹配
        #         dcm_dir_match_num += 1 #dcm文件夹匹配数+1
        #         print(split_root[-1], dcm_dir_match_num)
        #         #assert dcm_dir_num_match == 1 or dcm_dir_num_match == 0, '{} dcm dir match error!'.format(patient_name)
        #         if dcm_dir_match_num == 1 : #出现一个dcm文件夹匹配nii标注
        #             root_patient = '.'
        #             for i in range(1,len(split_root)-2):
        #                 root_patient = root_patient + '/' + split_root[i]#判断该患者是否有nii
        #             # print(root_patient)
        #             answer = whether_have_nii.whether_have_nii(root_patient, target_name)
        #             #print(root_patient + "地址患者的nii分割存在结果是：" )
        #             #print(answer)
        #             if answer == 1:
        #                     for f in file:
        #                         split_file = f.split('_')
        #                         f_old_path = os.path.join(root, f)
        #                         # 找到放了T2W_TSE的文件夹，复制里面的所有文件，并修改名称
        #                         f_new_name = split_root[-3] + '_T2W_TSE_' + split_file[-1]
        #                         # 保存图片到新路径
        #                         f_new_path = os.path.join(output_path, f_new_name)
        #                         #shutil.copy(f_old_path, f_new_path)
        #         elif dcm_dir_match_num >1 :
        #             txt_file.write('{} dcm_dir_match_num: {}'.format(patient_root, dcm_dir_match_num) + '\n')
        #
        #             print('{} dcm dir match error while dcm selecting!'.format(patient_root))
        # #if dcm_nii_match_end == True:
        #     #print(dcm_dir_match_num)
        # if dcm_nii_match_end == True and dcm_dir_match_num == 0: #dcm_nii匹配结束且没有找到dcm文件夹匹配nii标注
        #
        #     txt_file.write('{} dcm_dir_match_num: {}'.format(patient_root, dcm_dir_match_num)+'\n')
        #
        #     print('{} dcm dir match error while dcm selecting!'.format(patient_root))
        #     #print(patient_root)
        #     #shutil.move(patient_root, patient_root.replace('patient_group', 'exception_patient'))
        #     #shutil.move(patient_root, patient_root.replace('exception_patient', 'test1'))
    txt_file.close()


if __name__ == '__main__':
    # dicom文件目录
    target_name = "Untitled.nii.gz"
    root_path = r'.\patient_group' #dcm原文件夹路径
    #root_path = r'.\exception_patient' #dcm原文件夹路径
    output_path = r'.\unlabeled_results' #最后输出的dcm文件夹路径
    output_path1 = r'.\labeled_results'
    # dcm_select_all(root_path,output_path)
    #dcm_select_unlabeled(root_path, output_path, target_name)
    dcm_select_labeled(root_path, output_path1, target_name)