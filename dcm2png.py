import os
import pydicom
from matplotlib import pyplot as plt
import numpy as np

'''
funtion name:dcm2png
input:dcm_dir, output_dir（dcm文件夹地址，处理好的数据保存的位置）
output:none
将有dcm图像全部整理到output_dir下,转换成png形式
'''

def dcm2png(dcm_dir, output_dir):
    for root, dirs, files in os.walk(dcm_dir):
        for file in files:
            if file.endswith(".dcm"):
                dicom_file_path = os.path.join(root, file)
                ds = pydicom.dcmread(dicom_file_path)
                pixel_array_numpy = ds.pixel_array  # 找到dcm文件进行保存
                #pixel_array_numpy = np.fliplr(pixel_array_numpy)

                output_path = os.path.join(output_dir, file.replace(".dcm", ".png"))
                plt.imsave(output_path, pixel_array_numpy, cmap='gray')

if __name__ == '__main__':
    dcm_dir = r".\unlabeled_results\dcm"  # 原dcm文件路径
    output_dir = r".\test"  # png图片保存路径
    dcm2png(dcm_dir,output_dir)

