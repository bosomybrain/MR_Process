import os

def del_file(path):
    list = os.listdir(path)
    for i in list:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


def del_all():
    del_file(r'.\unlabeled_results\png')
    del_file(r'.\unlabeled_results\dcm')
    del_file(r'.\labeled_results\dcm')
    del_file(r'.\labeled_results\png')
    del_file(r'.\dcm_select_all\png')
    del_file(r'.\dcm_select_all\dcm')
    del_file(r'.\label_process_results\results_compare')
    del_file(r'.\label_process_results\Unet_data\image')
    del_file(r'.\label_process_results\Unet_data\mask')
    del_file(r'.\label_process_results\yolo_data\image')
    del_file(r'.\label_process_results\yolo_data\label')
    del_file(r'.\label_process_results\yolo_data\bounding_image')
    print('文件已经清空完成')

def del_patient():
    del_file(r'.\patient_group')


if __name__ == '__main__':
    del_all()