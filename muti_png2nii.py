import numpy as np
import nibabel as nib
from glob import glob
from PIL import Image
import os

'''
funtion name:muti_png2nii
input:label_path, output_path（有标签的数据集png文件位置，想存放的位置）
output:none
拿取label_path中全部png(不能有其他类型文件），生成对应的png转换nii文件，放到output_path下
'''
def muti_png2nii(label_path, output_path):
    label_path = glob(label_path)  # 获得所有dcm.png的路径
    image = Image.open(label_path[1])  # 打开第一张照片确定初始大小
    x = image.width
    y = image.height
    allImage = np.zeros([x, y, len(label_path)], dtype='uint8')
    for i in range(len(label_path)):
        image = Image.open(label_path[i])
        bw_image = image.convert("L")
        # 把每一个4通道png转换成灰度图
        allImage[:, :, i] = bw_image  # 把图像堆叠
    new_image = nib.Nifti1Image(allImage, np.eye(4))
    nib.save(new_image, output_path)

'''
funtion name:muti_png2nii_all
input:label_path, output_path（有标签的数据集png文件位置，全部患者的文件夹）
output:none
拿取labeled_results中png，通过文件名匹配原文件中的患者，生成对应的png转换nii文件，放到mask的nii一起
'''
def muti_png2nii_all(label_path, output_path):
    label_path1 = glob(label_path+"\*")
    for root, dir, file in os.walk(label_path):
        patint_name = ''
        count_picture = 0 #计算每个患者的图像个数
        num_picture = 0 #标记当前是第几张图片
        for f in file:
            split_file = f.split('_')  # 通过\\来进行截断
            # print(split_file[0])
            # print(len(file))
            if split_file[0] != patint_name:
                print("患者" + patint_name + "目标图像数目为")
                print(count_picture)
                #照片初始化，当患者照片改变，就把前一位患者的nii保存
                image = Image.open(label_path1[num_picture-1])  # 打开第一张照片确定初始大小
                # print(num_picture)
                x = image.width
                y = image.height
                allImage = np.zeros([x, y, count_picture], dtype='uint8')
                for i in range(num_picture-count_picture,num_picture):
                    image = Image.open(label_path1[i])
                    bw_image = image.convert("L")
                    # 把每一个4通道png转换成灰度图
                    allImage[:, :, i-(num_picture-count_picture)] = bw_image  # 把图像堆叠
                new_image = nib.Nifti1Image(allImage, np.eye(4))
                #寻找保存路径
                patint_path = output_path+r'\\'+patint_name+r'\\mr_data.nii.gz'
                nib.save(new_image, patint_path)
                count_picture = 1
                patint_name = split_file[0]
            else:
                count_picture = count_picture + 1
            num_picture = num_picture + 1
            # print(num_picture)
            if num_picture == len(file):            #对最后一个病例单独讨论
                print("患者" + split_file[0] + "目标图像数目为")
                print(count_picture)
                # 照片初始化，当患者照片改变，就把前一位患者的nii保存
                image = Image.open(label_path1[num_picture - 1])  # 打开第一张照片确定初始大小
                # print(num_picture)
                x = image.width
                y = image.height
                allImage = np.zeros([x, y, count_picture], dtype='uint8')
                for i in range(num_picture - count_picture, num_picture):
                    image = Image.open(label_path1[i])
                    bw_image = image.convert("L")
                    # 把每一个4通道png转换成灰度图
                    allImage[:, :, i - (num_picture - count_picture)] = bw_image  # 把图像堆叠
                new_image = nib.Nifti1Image(allImage, np.eye(4))
                # 寻找保存路径
                patint_path = output_path + r'\\' + patint_name + r'\\mr_data.nii.gz'
                nib.save(new_image, patint_path)
                count_picture = 1
                patint_name = split_file[0]



if __name__ == '__main__':
    # #单患者png输出测试
    # label_path1 = r'.\test\*'
    # output_path1 = r'.\test\mr_data.nii.gz'
    #全部患者文件夹测试
    label_path = r'.\labeled_results\png'
    output_path = r'.\patient_group'
    # output_path = r'.\test\mr_data.nii.gz'
    # muti_png2nii(label_path1,output_path1)
    muti_png2nii_all(label_path, output_path)