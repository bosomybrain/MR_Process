import numpy as np
import nibabel as nib
from PIL import Image
import os
import shutil
import imageio
import cv2

'''
funtion name:nii2mask2d
input:img_addr,label_addr,target_folder（患者图像nii地址，3dmask的nii地址，处理好的对比图像存放地址）
output:none
将患者图像nii，3dmask的nii匹配，输出图像到target_folder
'''
def nii2mask2d(img_addr,label_addr,target_folder):
    img_addr_n = nib.load(img_addr)
    label_addr_n = nib.load(label_addr)
    # Convert them to numpy format,
    data = img_addr_n.get_fdata()
    label_data = label_addr_n.get_fdata()

    # clip the images within [-125, 275],
    data_clipped = np.clip(data, -125, 275)

    # normalize each 3D image to [0, 1], and
    data_normalised = (data_clipped - (-125)) / (275 - (-125))

    split_root = img_addr.split('\\')  # 通过\\来进行截断
    print(split_root)
    # extract 2D slices from 3D volume for training cases while
    # e.g. slice 000
    for i in range(data_clipped.shape[2]):
        formattedi = "{:03d}".format(i)
        slice000 = data_normalised[:, :, i] * 255
        # np.savetxt(r"label.txt", label_data[:, :, 6], delimiter=',', fmt='%5s')
        label_slice000 = label_data[:, :, i]* 40 #标注像素是3，4，放到0-255的变化范围内



        print(slice000.shape, type(slice000))

        image = Image.fromarray(slice000)
        image = image.convert("L")
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        label = Image.fromarray(label_slice000)
        # print(type(label))
        # label = cv2.normalize(label, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        np.savetxt(r".\test\masknoL" + str(i + 1) + ".txt", label)
        # imageio.imsave(r".\test\mask_new" + str(i + 1) + ".png", label)
        label = label.convert("L")
        label = label.rotate(270)
        np.savetxt(r".\test\mask" + str(i + 1) + ".txt", label)
        #已验证分类结果没消失

        image.save(target_folder + split_root[-2]+"T2W_TSE_" + str(i+1) + ".png")
        label.save(target_folder + "T2W_TSE_" + str(i+1) + "_label.png")

'''
funtion name:nii2mask2d_all
input:img_addr,label_addr,target_folder（患者图像nii地址，3dmask的nii地址，处理好的对比图像存放地址）
output:none
将患者图像nii，3dmask的nii匹配，输出图像到target_folder
'''
def nii2mask2d_all(root_path,masknii,picturenii,target_folder):
    for root, dir, file in os.walk(root_path):
        file_judge = 0 #检测文件夹是否有两个nii文件
        img_addr = ''
        label_addr = ''
        for f in file :
            if f == masknii:
                file_judge = file_judge +1
                label_addr = root + r"\\" + r'\\' + masknii

            if f == picturenii:
                file_judge = file_judge + 1
                img_addr = root + r'\\' + r'\\' + picturenii

        if file_judge == 2:
            print("nii_ready------procss"+label_addr)
            # print(label_addr)
            # print(img_addr)
            img_addr_n = nib.load(img_addr)
            label_addr_n = nib.load(label_addr)
            # Convert them to numpy format,
            data = img_addr_n.get_fdata()
            label_data = label_addr_n.get_fdata()

            # clip the images within [-125, 275],
            data_clipped = np.clip(data, -125, 275)

            # normalize each 3D image to [0, 1], and
            data_normalised = (data_clipped - (-125)) / (275 - (-125))

            split_root = img_addr.split('\\')  # 通过\\来进行截断
            # print(split_root)
            # extract 2D slices from 3D volume for training cases while
            # e.g. slice 000
            for i in range(data_clipped.shape[2]):
                formattedi = "{:03d}".format(i)
                slice000 = data_normalised[:, :, i] * 255
                # np.savetxt(r"label.txt", label_data[:, :, 6], delimiter=',', fmt='%5s')
                label_slice000 = label_data[:, :, i] * 40

                # print(slice000.shape, type(slice000))

                image = Image.fromarray(slice000)
                image = image.convert("L")
                image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

                label = Image.fromarray(label_slice000)
                label = label.convert("L")
                label = label.rotate(270)

                image.save(target_folder + split_root[2]+ "T2W_TSE_" + str(i+1) + ".png")
                label.save(target_folder + split_root[2]+ "T2W_TSE_" + str(i+1) + "_label.png")

'''
funtion name:nii2mask2d_all_4png
input:img_addr,label_addr,target_folder（患者图像nii地址，3dmask的nii地址，处理好的对比图像存放地址）
output:none
将labeled_results中的png直接和mask一起放到target_folder,患者图像用原来的4通道
（没有文件夹索引，容易报错！）
'''
def nii2mask2d_all_4png(root_path,masknii,picturenii,target_folder):
    print("copy data from \labeled_results\png......")
    for root, dir, file in os.walk(r'.\labeled_results\png'):
        # print(file)
        pic_num = 1
        patient_name = ''
        for f in file:
            split_file = f.split('.')
            f_old_path = os.path.join(root, f)
            # print(f_old_path)
            split_file = split_file[0].split('_')
            # print(split_file)
            # 找到放了T2W_TSE的文件夹，复制里面的所有文件，并修改名称
            if split_file[0] == patient_name: #患者没改变则该序号保存
                pic_num = pic_num + 1
                f_new_name = patient_name + '_T2W_TSE_' + str(pic_num) + ".png"
            else:
                pic_num = 1
                patient_name = split_file[0]
                f_new_name = patient_name + '_T2W_TSE_' + str(pic_num) + ".png"
            # print(f_new_name)
            # 保存图片到新路径
            f_new_path = os.path.join(target_folder, f_new_name)
            # print(f_new_path)
            shutil.copy(f_old_path, f_new_path)
    print("copy finish......")

    for root, dir, file in os.walk(root_path):
        file_judge = 0 #检测文件夹是否有两个nii文件
        img_addr = ''
        label_addr = ''
        for f in file :
            if f == masknii:
                file_judge = file_judge +1
                label_addr = root + r"\\" + r'\\' + masknii

            if f == picturenii:
                file_judge = file_judge + 1
                img_addr = root + r'\\' + r'\\' + picturenii

        if file_judge == 2:
            print("nii_ready------procss"+label_addr)
            # print(label_addr)
            # print(img_addr)
            img_addr_n = nib.load(img_addr)
            label_addr_n = nib.load(label_addr)
            # Convert them to numpy format,
            data = img_addr_n.get_fdata()
            label_data = label_addr_n.get_fdata()

            # clip the images within [-125, 275],
            data_clipped = np.clip(data, -125, 275)

            # normalize each 3D image to [0, 1], and
            data_normalised = (data_clipped - (-125)) / (275 - (-125))

            split_root = img_addr.split('\\')  # 通过\\来进行截断
            # print(split_root)
            # extract 2D slices from 3D volume for training cases while
            # e.g. slice 000
            for i in range(data_clipped.shape[2]):
                formattedi = "{:03d}".format(i)
                slice000 = data_normalised[:, :, i] * 255
                # np.savetxt(r"label.txt", label_data[:, :, 6], delimiter=',', fmt='%5s')
                label_slice000 = label_data[:, :, i] * 40

                # print(slice000.shape, type(slice000))

                # image = Image.fromarray(slice000)
                # image = image.convert("L")
                # image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

                label = Image.fromarray(label_slice000)
                label = label.convert("L")
                label = label.rotate(270)

                # image.save(target_folder + split_root[2]+ "T2W_TSE_" + str(i) + ".png")
                label.save(target_folder + split_root[2]+ "_T2W_TSE_" + str(i+1) + "_label.png")
    print("nii2mask process finish......")



if __name__ == '__main__':
    img_addr = r"C:\Users\22495\Desktop\project_folder\patient_group\Chen Xiao Ya103433057\mr_data.nii.gz"
    label_addr = r"C:\Users\22495\Desktop\myomagroup3a\myomagroup3a\Chen Xiao Ya103433057\Untitled.nii.gz"
    target_folder = "./test/"
    target_folder1 = "./label_process_results/results_compare/"
    root_path = r'.\patient_group'  # 全部患者文件夹路径
    masknii = "Untitled.nii.gz"
    picturenii = "mr_data.nii.gz"


    # nii2mask2d(img_addr, label_addr, target_folder)#单患者放在test观察
    # nii2mask2d_all(root_path, masknii, picturenii, target_folder1)#多患者放在label
    nii2mask2d_all_4png(root_path, masknii, picturenii, target_folder1)
    # img_test = r"C:\Users\22495\Desktop\project_folder\patient_group\Dong Ren Ming103224231\mr_data.nii.gz"
    # label_test = r"C:\Users\22495\Desktop\project_folder\patient_group\Dong Ren Ming103224231\Untitled.nii.gz"
    # # target_folder = "./test/"
    # nii2mask2d(img_test, label_test, target_folder)