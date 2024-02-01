import os

'''
funtion name:total_nii
input:patient_folder, target_name（所有患者文件夹地址，目标文件名称，此处是nii文件）
output:count(文件总共的nii个数）
计算这批患者总工有的nii切割数目，
'''
def total_nii(patient_folder, target_name):
    count = 0
    for root, dir, file in os.walk(patient_folder):
        if target_name in file:
            count = count + 1
        else:
            count = count
    return count
'''
funtion name:whether_have_nii
input:patient_addr, target_name（患者文件夹地址，目标文件名称，此处是nii文件）
output:1说明有nii，0说明没nii
计算当下这名患者是否有nii数据
'''
def whether_have_nii(patient_addr, target_name):
    count = 0
    for root, dir, file in os.walk(patient_addr):
        if target_name in file:
            count = count + 1
        else:
            count = count
    if count > 0:
        return True
    else:
        return False


if __name__ == '__main__':
    # dicom文件目录
    folder = r'.\patient_group'
    addr = r'.\patient_group\Ceng Min Ye102963955'  # example with no nii
    # addr = r'.\patient_group\Chen Xiao Ya103433057' #example with  nii
    target_name = "Untitled.nii.gz"
    answer = whether_have_nii(addr, target_name)
    number = total_nii(folder, target_name)
    print(answer)
    print(number)
