from PIL import Image
# import layoutparser as lp
import pytesseract
import easyocr
import cv2
import numpy as np
import sys

########################################## page_layout func ########################################
# def page_layout(img):
#     model = lp.Detectron2LayoutModel('lp://NewspaperNavigator/faster_rcnn_R_50_FPN_3x/config',
#                                      extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
#                                      label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})
#
#     # img = cv2.imread(ImagePath)
#     layout_result = model.detect(img)
#     lp.draw_box(img, layout_result, box_width=5, box_alpha=0.2, show_element_type=True)
#     return img


########################################## page_layout func ########################################

########################################## tesseract func ##########################################
def tessract_engine(ImagePath, lang='fas', ConfigurationNumber=2):
    if lang == 'fas':
        langu = 'fas'
    elif lang == 'en':
        langu = 'eng'
    elif lang == 'en+fas':
        langu = 'eng+fas'
    elif lang == 'ar':
        langu = 'ara'

    if ConfigurationNumber == 1:
        tessdata_dir_config = "/usr/bin/tesseract"  # '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
    else:
        tessdata_dir_config = "--oem 3 --psm 6"
        # '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata" --oem 3 --psm 6'

        Total_text = pytesseract.image_to_string(Image.open(ImagePath), lang=langu, config=tessdata_dir_config)

        Total_text = Total_text.strip()

        details = pytesseract.image_to_data(Image.open(ImagePath), lang=langu, config=tessdata_dir_config,
                                            output_type='data.frame')

        details = details[details.conf != -1]
        details = details[details.conf != -1]
        data_text = pytesseract.image_to_data(Image.open(ImagePath), lang=langu, config=tessdata_dir_config,
                                              output_type='dict')

        lines = details.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['text'].apply(
            lambda x: ' '.join(list(x))).tolist()
        confs = details.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['conf'].mean().tolist()
        line_text = []
        line_conf = []
        for i in range(len(lines)):
            if lines[i].strip():
                line_text.append(lines[i])
                line_conf.append(round(confs[i], 3))

        Average_Confidence_Value = line_conf[0]
        Text_list = data_text['text']
        Level_list = data_text['level']
        Conf_list = data_text['conf']

    return Total_text, Average_Confidence_Value


########################################## tesseract func ##########################################

########################################## easyocr func ############################################
def easyocr_engine(ImagePath, lang='fas'):
    if lang == 'fas':
        langu = ['fa']
    elif lang == 'en':
        langu = ['en']
    elif lang == 'en+fas':
        langu = ['en', 'fa']
    elif lang == 'ar':
        langu = ['ar']

    readers = easyocr.Reader(langu)
    word_list = readers.readtext(ImagePath, paragraph=True)
    Total_text = ""
    image = cv2.imread(ImagePath)
    ##          print(np.shape(word_list),word_list[0][0],word_list[0][1])
    for (bbox, text) in word_list:
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        image = cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        Total_text += text + '\n'

    Average_Confidence_Value = 0  #### پیدا کردن کدش
    ##          Total_text = " ".join(word_list)
    ##          Total_text =  Total_text.strip()

    return Total_text, Average_Confidence_Value, image


########################################## easyocr func ############################################


########################################### deskew func############################################


import cv2
import math
import numpy as np
from deskew import determine_skew


# Deskewing Block:
# Parameters: 1) borderValue that can be 0 or 255.

def deskew_cv2(img_gray: np.ndarray, bordervalue: int = 255) -> np.ndarray:
    def rotate_cv2(img_gray, angle):
        angle_radians = math.radians(angle)
        old_width, old_height = img_gray.shape
        width = abs(np.sin(angle_radians) * old_height) + abs(np.cos(angle_radians) * old_width)
        height = abs(np.sin(angle_radians) * old_width) + abs(np.cos(angle_radians) * old_height)

        image_center = old_height / 2, old_width / 2
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1)
        rot_mat[1, 2] += (width - old_width) / 2
        rot_mat[0, 2] += (height - old_height) / 2
        return cv2.warpAffine(img_gray, rot_mat, (int(round(height)), int(round(width))), borderValue=bordervalue,
                              borderMode=cv2.BORDER_CONSTANT)

    angle = determine_skew(img_gray)
    return rotate_cv2(img_gray, angle)


# End of Deskewing Block


########################################## main func ###############################################

def OCR(ImagePath, lang='fas', EngineName='tesseract', ConfigurationNumber=2, preprocessing=False,
        postprocessing=False):
    try:
        loadimg = cv2.imread(ImagePath)
        # outputimg_2=page_layout(loadimg)
        outputimg_2 = loadimg

        if preprocessing[1]:  #### هر کدوم از وارد که تیک خورد این متغیر فعال بشه
            img = cv2.imread(ImagePath, 0)
            deskew_cv2_output = deskew_cv2(img)
            backtorgb = cv2.cvtColor(deskew_cv2_output, cv2.COLOR_GRAY2RGB)
            cv2.imwrite("Temp.png", backtorgb)
            ImagePath = "Temp.png"
            outputimg_2 = backtorgb

        if EngineName == 'tesseract':
            Total_text, Average_Confidence_Value = tessract_engine(ImagePath, lang=lang,
                                                                   ConfigurationNumber=ConfigurationNumber)

        elif EngineName == 'easyocr':
            Total_text, Average_Confidence_Value, outputimg_2 = easyocr_engine(ImagePath, lang=lang)

        if postprocessing:  #### هر کدوم از وارد که تیک خورد این متغیر فعال بشه
            pass
    except Exception as e:
        print(e)
        print(f"""Sorry your input image({ImagePath}) dosen't have a good quality,
			First, make sure the input image is correct.
			If the input image is correct, you probably need pre-processing,
			please set the relevant parameter""")

    return Total_text, Average_Confidence_Value, loadimg, outputimg_2


########################################## main func ###############################################