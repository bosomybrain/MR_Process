import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
from matplotlib import patches

def mask2box(self, mask):  # [x1,y1,x2,y2]
    '''从mask反算出其边框
    mask：[h,w]  0、1组成的图片
    1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
    '''
    index = np.argwhere(mask == 1)
    rows = index[:, 0]
    clos = index[:, 1]
    # 解析左上角行列号
    left_top_r = np.min(rows)  # y
    left_top_c = np.min(clos)  # x
    # 解析右下角行列号
    right_bottom_r = np.max(rows)  # y
    right_bottom_c = np.max(clos)  # x
    return left_top_c, left_top_r, right_bottom_c, right_bottom_r

def mask_find_bboxs(mask):

    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8) # connectivity参数的默认值为8
    # print(retval,labels,centroids)
    stats = stats[stats[:,4].argsort()]
    return stats[:-1] # 排除最外层的连通图

def process_yolov5_data(address):
    # 获取mask（灰度图）
    mask_ori = cv2.imread(r'.\label_process_results\results_compare\Dong Ren Ming103224231_T2W_TSE_10_label.png',
                          cv2.COLOR_BGR2GRAY)
    mask_rgb = cv2.imread(r'.\label_process_results\results_compare\Dong Ren Ming103224231_T2W_TSE_10.png')
    Unet_pic_ori = cv2.imread(r'.\label_process_results\results_compare\Dong Ren Ming103224231_T2W_TSE_10.png')
    ret, mask = cv2.threshold(mask_ori, 20, 255, cv2.THRESH_BINARY)  # 30是最小分类,处理成灰度图才能进mask_find_bboxs函数
    bboxs = mask_find_bboxs(mask)  # 框选目标的参数
    width = len(mask[1, :])  # 宽
    height = len(mask[:, 1])  # 高
    file = open(r".\test\yolo.txt", "w", encoding='utf-8')
    '''
    参数介绍b[0],b[1]:左上角坐标x,y x变大向右平移y变大向下平移
           b[2]     :矩形宽度
           b[3]     :矩形高度

        转换成yolo。txt格式
        类别（0开始） 方框中心点比例（x，y） width宽占比例 height 高占比例

    '''
    classification = 10  # 10表示出错

    for b in bboxs:
        pixel_catch = 0
        for i in range(3, 8):
            for j in range(3, 8):
                pixel_catch = max(mask_ori[int((b[1] + (b[3] * (j / 10)))), int((b[0] + (b[2] * (i / 10))))],
                                  pixel_catch)

        yolo_para_width = b[2] / width
        yolo_para_height = b[3] / height
        yolo_para_x_center = (b[0] / width) + (yolo_para_width / 2)
        yolo_para_y_center = (b[1] / height) + (yolo_para_height / 2)
        print(pixel_catch)
        Unet_pic = Unet_pic_ori[b[1]:b[1] + b[3], b[0]:b[0] + b[2]]
        # Unet_pic = mask_rgb[b[0]:b[0] + b[2], b[1]:b[1] + b[3]]
        Unet_pic_name = r'.\\' + str(b)
        cv2.imwrite('./1_new.jpg', Unet_pic)
        if pixel_catch == 40:
            cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
            classification = 2
        if pixel_catch == 80:
            cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
            classification = 3
        if pixel_catch == 120:
            cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0]+b[2], b[1]+b[3]), (0, 0, 255), 2)
            classification = 0
        if pixel_catch == 160:
            cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
            classification = 1
        if pixel_catch == 200:
            cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
            classification = 4
        if pixel_catch == 240:
            cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
            classification = 5

        file.write(str(classification) + ' ' + str(yolo_para_x_center) + ' ' + str(yolo_para_y_center) + ' ' + str(
            yolo_para_width) + ' ' + str(yolo_para_height) + '\n')
    cv2.imwrite('./000_new.jpg', mask_rgb)
    file.close()

def process_Unet_data(address):
    a = 0

def process_yolov5_and_Unet_data_together(address):
    for root, dir, file in os.walk(address):
        for f in file:
            split_file = f.split('_')  # 通过\\来进行截断
            if split_file[-1] == "label.png":
                #mask_ori是mask照片，rgb_name是mask对应的rgb照片
                mask_ori = cv2.imread(r'.\\label_process_results\\results_compare\\' + f, cv2.COLOR_BGR2GRAY)
                rgb_name = r'.\\label_process_results\\results_compare\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2]+ r'_'+ split_file[3] + r'.png'
                Unet_pic_ori = cv2.imread(r'.\\label_process_results\\results_compare\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2]+ r'_'+ split_file[3] + r'.png')
                yolo_name = r'.\\label_process_results\\yolo_data\\label\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2] + r'_'+ split_file[3] + r'.txt'
                target_bbox_name = r'.\\label_process_results\\yolo_data\\bounding_image\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2] + r'_'+ split_file[3] + r'.jpg'

                f_new_path_yolo = r'.\\label_process_results\\yolo_data\\image\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2]+ r'_'+ split_file[3] + r'.png'
                # f_new_path_Unet = r'.\\label_process_results\\Unet_data\\image\\' + split_file[0] + r'_' + split_file[
                #     1] + r'_' + split_file[2] + r'_' + split_file[3] + r'.png'
                shutil.copy(rgb_name, f_new_path_yolo)


                mask_rgb = cv2.imread(rgb_name)
                ret, mask = cv2.threshold(mask_ori, 20, 255, cv2.THRESH_BINARY)  # 30是最小分类,处理成灰度图才能进mask_find_bboxs函数
                bboxs = mask_find_bboxs(mask)  # 框选目标的参数
                width = len(mask[1, :])  # 宽
                height = len(mask[:, 1])  # 高
                file = open(yolo_name, "w", encoding='utf-8')
                '''
                参数介绍b[0],b[1]:左上角坐标x,y x变大向右平移y变大向下平移
                       b[2]     :矩形宽度
                       b[3]     :矩形高度

                    转换成yolo。txt格式
                    类别（0开始） 方框中心点比例（x，y） width宽占比例 height 高占比例

                '''
                classification = 10  # 10表示出错

                num_classification0 = 0
                num_classification1 = 0
                num_classification2 = 0
                num_classification3 = 0
                num_classification4 = 0
                num_classification5 = 0

                for b in bboxs:
                    pixel_catch = 0
                    for i in range(3, 8):
                        for j in range(3, 8):
                            pixel_catch = max(
                                mask_ori[int((b[1] + (b[3] * (j / 10)))), int((b[0] + (b[2] * (i / 10))))],
                                pixel_catch)

                    yolo_para_width = b[2] / width
                    yolo_para_height = b[3] / height
                    yolo_para_x_center = (b[0] / width) + (yolo_para_width / 2)
                    yolo_para_y_center = (b[1] / height) + (yolo_para_height / 2)


                    if pixel_catch == 40:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 0
                        num_classification0 = num_classification0 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification2) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification2) + r'.png'
                    if pixel_catch == 80:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 0
                        num_classification0 = num_classification0 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification3) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification3) + r'.png'
                    if pixel_catch == 120:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (0, 0, 255), 2)
                        classification = 0
                        num_classification0 = num_classification0 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification0) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification0) + r'.png'
                    if pixel_catch == 160:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 0
                        num_classification0 = num_classification0 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification1) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification1) + r'.png'
                    if pixel_catch == 200:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 0
                        num_classification0 = num_classification0 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification4) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification4) + r'.png'
                    if pixel_catch == 240:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 0
                        num_classification0 = num_classification0 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification5) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification5) + r'.png'


                    Unet_pic = Unet_pic_ori[b[1]:b[1] + b[3], b[0]:b[0] + b[2]]


                    Unet_mask = mask[b[1]:b[1] + b[3], b[0]:b[0] + b[2]]

                    cv2.imwrite(Unet_pic_name, Unet_pic)
                    cv2.imwrite(Unet_mask_name, Unet_mask)

                    file.write(
                        str(classification) + ' ' + str(yolo_para_x_center) + ' ' + str(yolo_para_y_center) + ' ' + str(
                            yolo_para_width) + ' ' + str(yolo_para_height) + '\n')
                cv2.imwrite(target_bbox_name, mask_rgb)
                file.close()

def process_yolov5_and_Unet_data_respective(address):
    for root, dir, file in os.walk(address):
        for f in file:
            split_file = f.split('_')  # 通过\\来进行截断
            if split_file[-1] == "label.png":
                #mask_ori是mask照片，rgb_name是mask对应的rgb照片
                mask_ori = cv2.imread(r'.\\label_process_results\\results_compare\\' + f, cv2.COLOR_BGR2GRAY)
                rgb_name = r'.\\label_process_results\\results_compare\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2]+ r'_'+ split_file[3] + r'.png'
                Unet_pic_ori = cv2.imread(r'.\\label_process_results\\results_compare\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2]+ r'_'+ split_file[3] + r'.png')
                yolo_name = r'.\\label_process_results\\yolo_data\\label\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2] + r'_'+ split_file[3] + r'.txt'
                target_bbox_name = r'.\\label_process_results\\yolo_data\\bounding_image\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2] + r'_'+ split_file[3] + r'.jpg'

                f_new_path_yolo = r'.\\label_process_results\\yolo_data\\image\\' + split_file[0] + r'_' + split_file[1] + r'_'+ split_file[2]+ r'_'+ split_file[3] + r'.png'
                # f_new_path_Unet = r'.\\label_process_results\\Unet_data\\image\\' + split_file[0] + r'_' + split_file[
                #     1] + r'_' + split_file[2] + r'_' + split_file[3] + r'.png'
                shutil.copy(rgb_name, f_new_path_yolo)


                mask_rgb = cv2.imread(rgb_name)
                ret, mask = cv2.threshold(mask_ori, 20, 255, cv2.THRESH_BINARY)  # 30是最小分类,处理成灰度图才能进mask_find_bboxs函数
                bboxs = mask_find_bboxs(mask)  # 框选目标的参数
                width = len(mask[1, :])  # 宽
                height = len(mask[:, 1])  # 高
                file = open(yolo_name, "w", encoding='utf-8')
                '''
                参数介绍b[0],b[1]:左上角坐标x,y x变大向右平移y变大向下平移
                       b[2]     :矩形宽度
                       b[3]     :矩形高度

                    转换成yolo。txt格式
                    类别（0开始） 方框中心点比例（x，y） width宽占比例 height 高占比例

                '''
                classification = 10  # 10表示出错

                num_classification0 = 0
                num_classification1 = 0
                num_classification2 = 0
                num_classification3 = 0
                num_classification4 = 0
                num_classification5 = 0

                for b in bboxs:
                    pixel_catch = 0
                    for i in range(3, 8):
                        for j in range(3, 8):
                            pixel_catch = max(
                                mask_ori[int((b[1] + (b[3] * (j / 10)))), int((b[0] + (b[2] * (i / 10))))],
                                pixel_catch)

                    yolo_para_width = b[2] / width
                    yolo_para_height = b[3] / height
                    yolo_para_x_center = (b[0] / width) + (yolo_para_width / 2)
                    yolo_para_y_center = (b[1] / height) + (yolo_para_height / 2)


                    if pixel_catch == 40:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 2
                        num_classification2 = num_classification2 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification2) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification2) + r'.png'
                    if pixel_catch == 80:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 3
                        num_classification3 = num_classification3 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification3) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification3) + r'.png'
                    if pixel_catch == 120:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (0, 0, 255), 2)
                        classification = 0
                        num_classification0 = num_classification0 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification0) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification0) + r'.png'
                    if pixel_catch == 160:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 1
                        num_classification1 = num_classification1 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification1) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification1) + r'.png'
                    if pixel_catch == 200:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 4
                        num_classification4 = num_classification4 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification4) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification4) + r'.png'
                    if pixel_catch == 240:
                        cv2.rectangle(mask_rgb, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 2)
                        classification = 5
                        num_classification5 = num_classification5 + 1
                        Unet_pic_name = r'.\\label_process_results\\Unet_data\\image\\' + str(classification) + r'\\' + \
                                        split_file[0] + r'_' + split_file[
                                            1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification5) + r'.png'
                        Unet_mask_name = r'.\\label_process_results\\Unet_data\\mask\\' + str(classification) + r'\\' + \
                                         split_file[0] + r'_' + split_file[
                                             1] + r'_' + split_file[2] + r'_' + split_file[3] + r'_num' + str(
                            num_classification5) + r'.png'


                    Unet_pic = Unet_pic_ori[b[1]:b[1] + b[3], b[0]:b[0] + b[2]]


                    Unet_mask = mask[b[1]:b[1] + b[3], b[0]:b[0] + b[2]]

                    cv2.imwrite(Unet_pic_name, Unet_pic)
                    cv2.imwrite(Unet_mask_name, Unet_mask)

                    file.write(
                        str(classification) + ' ' + str(yolo_para_x_center) + ' ' + str(yolo_para_y_center) + ' ' + str(
                            yolo_para_width) + ' ' + str(yolo_para_height) + '\n')
                cv2.imwrite(target_bbox_name, mask_rgb)
                file.close()



if __name__ == '__main__':
    address = r".\label_process_results\results_compare"
    process_yolov5_and_Unet_data_respective(address)

    # process_yolov5_data(r'.\label_process_results\results_compare\Dong Ren Ming103224231_T2W_TSE_10.png')

