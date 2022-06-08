import pytesseract
import cv2
import os
import re
from utils import remove_noise_and_smooth

pytesseract.pytesseract.tesseract_cmd  = r'/usr/local/bin/tesseract'
DIR_UPLD = os.path.join("Figures/")
DIR_DWNLD = os.path.join("Texts/")


# extract text and save it to txt file in folder 'Texts'
class Extract:
    def __init__(self):
        self.img_lst = []
        for root, dirs, files in os.walk(DIR_UPLD):
            for file in files:
                if file.endswith(".png"):
                    self.img_lst += [f"{DIR_UPLD}{file}"]  # for now one image only

    def ocr(self):
        txt_ALL = [] #return list of txt files for each image
        for i, img_nm in enumerate(self.img_lst):
            img = cv2.imread(img_nm)
            gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            (h, w) = gry.shape[:2]
            if i == 0:
                thr = gry
            else:
                gry = cv2.resize(gry, (w * 2, h * 2))
                erd = cv2.erode(gry, None, iterations=1)
                if i == len(self.img_lst) - 1:
                    thr = cv2.threshold(erd, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                else:
                    thr = cv2.threshold(erd, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            bnt = cv2.bitwise_not(thr)
            txt = pytesseract.image_to_string(bnt) #config="--psm 6 digits" for digits only
            txt_ALL += [txt]
            #print("".join([t for t in txt])) or print(txt)
        return txt_ALL


def get_raw_text(extracted_texts):
    for root, dirs, files in os.walk(DIR_UPLD):
        for file in files:
            if file.endswith(".png"):
                pre_fix = file[:-4]
                with open(DIR_DWNLD + "/" + pre_fix + "raw" + ".txt", 'w') as f:
                    for x in extracted_texts:
                        f.write(str(x))


def get_processed_text():
    for root, dirs, files in os.walk(DIR_DWNLD):
        for file in files:
            if file.endswith(".png"):
                pre_fix = file[:-4]
                with open(f"{DIR_DWNLD}{file}", 'r', encoding="ISO-8859-1") as fread, \
                        open(DIR_DWNLD + "/" + pre_fix + "processed" + ".txt", 'w') as fwrite:
                    for line in fread:
                        line = re.sub('%', '', line)  # remove specified special chars (%)
                        line_new = " ".join("| " + i if i.isalpha() else i for i in line.split())
                        line_new = ' | '.join(re.split('\s(?=\d)', line_new))
                        line_new = line_new.strip().split(" | ")
                        if len(line_new) >= 9 and 'Random' not in line:
                            Study = ''
                            for s in line_new:
                                if any(c.isalpha() for c in s):
                                    Study += s
                            Study = ''.join(e for e in Study if e.isalnum())
                            Rest = [''.join(re.split(' =', x)) for x in line_new if
                                    x.isnumeric() or (x.isnumeric() or '.' in x or ',' in x)]
                            ES, SE, N1, N2, Weight = Rest[:5]
                            Weight = float(Weight) / 100
                            pre_fix = file[:-4]
                            # print(Study + "\t" + " ".join(str(c) for c in (ES, SE, N1, N2, Weight)))
                            fwrite.writelines(Study + "\t" + " ".join(str(c) for c in (ES, SE, N1, N2, Weight)) + "\n")
                fwrite.close()


################################ main ####################################
def main():
    my_extraction = Extract()
    extracted_texts = my_extraction.ocr()
    get_raw_text(extracted_texts)
    get_processed_text()


if __name__ == "__main__":
    main()





