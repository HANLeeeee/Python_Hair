import sys, cv2, datetime

from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.qt4_editor.formlayout import QApplication


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(500, 200, 900, 700)

        btn1 = QPushButton("촬영버튼", self)
        btn1.move(100, 70)  #(가로, 세로)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton("영상버튼", self)
        btn2.move(230, 70)  # (가로, 세로)
        btn2.clicked.connect(self.btn2_clicked)

        btn3 = QPushButton("캡쳐사진", self)
        btn3.move(360, 70)
        btn3.clicked.connect(self.btn3_clicked)

        btn4 = QPushButton("binary", self)
        btn4.move(490, 70)
        btn4.clicked.connect(self.btn4_clicked)

        btn5 = QPushButton("damage", self)
        btn5.move(620, 70)
        btn5.clicked.connect(self.btn5_clicked)

        label = QLabel("dfdf", self)
        label.resize(500, 500)


    def btn1_clicked(self):
        cam(self)

    def btn2_clicked(self):
        avi(self)

    def btn3_clicked(self):
        cap(self)

    def btn4_clicked(self):
        binary(self)

    def btn5_clicked(self):
        dam(self)


def cam(self):
    cam = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

    while True:
        ret, img_color = cam.read()

        if ret == False:
            continue

        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Color", img_color)
        cv2.imshow("Gray", img_gray)

        writer.write(img_color)

        if cv2.waitKey(30) & 0xFF == 27:
            break

    cam.release()
    writer.release()
    cv2.destroyAllWindows()


def avi(self):
    try:
        cam = cv2.VideoCapture('output.avi')
        length = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    except:
        QMessageBox.about(self, "삐익", "저장영상없음")
        return

    def onChange(trackbarValue):
        cam.set(cv2.CAP_PROP_POS_FRAMES, trackbarValue)
        err, img = cam.read()
        cv2.imshow("mywindow", img)
        pass


    cv2.namedWindow('mywindow')
    cv2.createTrackbar('start', 'mywindow', 0, length, onChange)


    cv2.waitKey()

    start = cv2.getTrackbarPos('start', 'mywindow')
    cam.set(cv2.CAP_PROP_POS_FRAMES, start)

    while True:
        if (cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get(cv2.CAP_PROP_FRAME_COUNT)):
            cam.open("output.avi")

        ret, img_color = cam.read()

        now = datetime.datetime.now().strftime("%d_%H-%M-%S")
        key = cv2.waitKey(33)

        if ret == False:
            print('오류')
            break

        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

        cv2.imshow("mywindow", img_color)
        cv2.imshow("Gray", img_gray)

        key = cv2.waitKey(0) & 0xFF
        if key == 27:
            break
        elif key == 32:
            print("캡쳐")
            cv2.imwrite("C:/Users/0/Desktop/CAPSTON/" + str(now) + ".png", img_color)
            cv2.imwrite("C:/Users/0/Desktop/CAPSTON/" + str(now) + "_1.png", img_gray)
            QMessageBox.about(self, "Save Success", "사진캡쳐완료.")

    cam.release()
    cv2.destroyAllWindows()


def cap(self):
    fname = QFileDialog.getOpenFileName(self)
    if fname[0]:
        coloredImg = cv2.imread(fname[0])

        capture = cv2.imshow("Capture", coloredImg)
        cv2.imwrite("hair.jpg", coloredImg)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        QMessageBox.about(self, "Warning", "파일을 선택하지 않았습니다.")


def binary(self):
    background = cv2.imread("white.png")
    logo = cv2.imread("hair.jpg")
    # cv2.imshow("이진화 사진", logo)

    gray_logo = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    # _, mask_inv = cv2.threshold(gray_logo, 173, 255, cv2.THRESH_TOZERO)
    _, mask_inv = cv2.threshold(gray_logo, 173, 255, cv2.THRESH_TOZERO)
    _, mask_inv2 = cv2.threshold(gray_logo, 10, 255, cv2.THRESH_TOZERO_INV)

    background_height, background_width, _ = background.shape  # 400, 520, 3
    logo_height, logo_width, _ = logo.shape  # 308, 250, 3

    x = (background_height - logo_height) // 2  # /2의 몫만 가져옴 (정수만 가져오기 위해)
    y = (background_width - logo_width) // 2

    roi = background[x: x + logo_height, y: y + logo_width]

    roi_logo = cv2.add(logo, roi, mask=mask_inv)
    roi_logo1 = cv2.add(logo, roi, mask=mask_inv2)

    result = cv2.add(roi_logo, logo)
    result1 = cv2.add(roi_logo1, logo)
    final = cv2.add(result, result1)
    # cv2.imshow("1", mask_inv)
    # cv2.imshow("q", roi_logo)
    cv2.imshow("result", result)
    cv2.imwrite("C:/Users/0/Desktop/CAPSTON/UI/" + "resultimg" + ".png", result)

    cv2.waitKey()
    cv2.destroyAllWindows()

def dam(self) :
    im = Image.open("resultimg.png")

    im_raw = im.load()

    width, height = im.size

    def mouse_callback(event, x, y, flags, param):
        count1, count2, count3 = 0, 0, 0

        if event == cv2.EVENT_LBUTTONDOWN:
            r, g, b = img_color[y, x]
            print("선택한 RGB값:", r, g, b)
            for i in range(0, width):
                for j in range(0, height):
                    if im.getpixel((i, j)) != (255, 255, 255):
                        r1, g1, b1 = im.getpixel((i, j))
                        z = 100 * (((r - r1) + (g - g1) + (b - b1)) / (r + g + b))
                        if z <= 40:
                            count1 += 1
                        elif 40 < z <= 70:
                            im_raw[i, j] = (255, 255, 0)
                            count2 += 1
                        elif 70 <= z:
                            im_raw[i, j] = (255, 0, 0)
                            count3 += 1
            # im.show()
            im.save("resultimg1.png")

            pixmap = QPixmap("resultimg1.png")
            pixmap = pixmap.scaled(600, 400)
            self.phlabel.setPixmap(pixmap)
            ss = (count2 + count3 * 2) / (count1 + count2 + count3 * 2)
            print("손상도:", round(ss, 2) * 100, "%")

    cv2.namedWindow('img_color')
    cv2.setMouseCallback('img_color', mouse_callback)

    while (True):
        img_color = cv2.imread('resultimg.png')
        cv2.imshow('img_color', img_color)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()