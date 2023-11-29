import os
from tkinter import filedialog
import cv2
import numpy as np
from utils.to_pil import to_pil


class ImageProcessor:
    image = None
    f_types = [("Jpg Files", "*.jpg"), ("PNG Files", "*.png")]
    demo_path = os.path.join(os.path.dirname(__file__), "../images/demo.jpg")

    def __init__(self) -> None:
        self.image = cv2.imread(self.demo_path)
        self.image = cv2.resize(self.image, (500, 500))
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    @to_pil
    def get_image(self):
        return self.image

    def open(self):
        path = filedialog.askopenfilename(filetypes=self.f_types)
        self.image = cv2.imread(path)
        self.image = cv2.resize(self.image, (500, 500))
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def save(self):
        with open("image.png", "wb") as file:
            file.write(self.image)

    @to_pil
    def resize(self, width=None, height=None):
        if width is None:
            ratio = height / self.image.shape[0]
            dim = (int(self.image.shape[1] * ratio), height)
        elif height is None:
            ratio = width / self.image.shape[1]
            dim = (width, int(self.image.shape[0] * ratio))
        else:
            dim = (width, height)

        return cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)

    @to_pil
    def grayscale(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    @to_pil
    def negative(self):
        return 255 - self.image

    @to_pil
    def pencil(self):
        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0, 0)
        img_blend = cv2.divide(img_gray, img_blur, scale=256)
        return img_blend

    @to_pil
    def red(self):
        row, col, plane = self.image.shape
        red = np.zeros((row, col, plane), np.uint8)
        red[:, :, 0] = self.image[:, :, 0]

        return red

    @to_pil
    def green(self):
        row, col, plane = self.image.shape
        green = np.zeros((row, col, plane), np.uint8)
        green[:, :, 1] = self.image[:, :, 1]

        return green

    @to_pil
    def blue(self):
        row, col, plane = self.image.shape
        blue = np.zeros((row, col, plane), np.uint8)
        blue[:, :, 2] = self.image[:, :, 2]

        return blue

    @to_pil
    def gaussian(self, kernel_size=(5, 5)):
        if kernel_size[0] % 2 == 0:
            kernel_size = (kernel_size[0] + 1, kernel_size[1])
        if kernel_size[1] % 2 == 0:
            kernel_size = (kernel_size[0], kernel_size[1] + 1)

        return cv2.GaussianBlur(self.image, kernel_size, 0)

    @to_pil
    def edge(self):
        return cv2.Canny(self.image, 100, 200)

    @to_pil
    def sharpen(self):
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        return cv2.filter2D(self.image, -1, kernel)

    @to_pil
    def powlawtrans(self, gamma=1.4):
        gamma = float(gamma)
        gamma_corrected = np.array(255 * (self.image / 255) ** gamma, dtype="uint8")
        return gamma_corrected

    @to_pil
    def sepia(self):
        sepia_matrix = np.array(
            [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
        )
        sepia_image = cv2.transform(self.image, sepia_matrix)
        sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
        return sepia_image

    @to_pil
    def flip_horizontal(self):
        return cv2.flip(self.image, 1)

    @to_pil
    def flip_vertical(self):
        return cv2.flip(self.image, 0)

    @to_pil
    def rotate(self, angle):
        rows, cols, _ = self.image.shape
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        rotated_image = cv2.warpAffine(self.image, rotation_matrix, (cols, rows))
        return rotated_image

    @to_pil
    def blur(self, kernel_size=(5, 5)):
        return cv2.blur(self.image, kernel_size)

    @to_pil
    def invert_colors(self):
        return cv2.bitwise_not(self.image)

    @to_pil
    def emboss(self):
        emboss_kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
        embossed_image = cv2.filter2D(self.image, -1, emboss_kernel)
        return embossed_image

    @to_pil
    def median_filter(self, kernel_size=5):
        return cv2.medianBlur(self.image, kernel_size)

    @to_pil
    def threshold(
        self, threshold_value=128, max_value=255, threshold_type=cv2.THRESH_BINARY
    ):
        _, thresholded_image = cv2.threshold(
            self.image, threshold_value, max_value, threshold_type
        )
        return thresholded_image

    @to_pil
    def cartoonize(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cartoon = cv2.bilateralFilter(self.image, d=9, sigmaColor=300, sigmaSpace=300)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 21
        )
        cartoon = cv2.bitwise_and(cartoon, cartoon, mask=edges)

        return cartoon

    @to_pil
    def shear_x(self, factor=0.5):
        rows, cols, ch = self.image.shape
        M = np.float32([[1, factor, 0], [0, 1, 0], [0, 0, 1]])
        return cv2.warpPerspective(self.image, M, (cols, rows))
    
    @to_pil
    def shear_y(self, factor=0.5):
        rows, cols, ch = self.image.shape
        M = np.float32([[1, 0, 0], [factor, 1, 0], [0, 0, 1]])
        return cv2.warpPerspective(self.image, M, (cols, rows))
    

    @to_pil
    def fish_eye(self):
        rows, cols, ch = self.image.shape
        distCoeff = np.zeros((4, 1), np.float64)
        k1 = -6e-5
        k2 = 0.0
        p1 = 0.0
        p2 = 0.0
        distCoeff[0, 0] = k1
        distCoeff[1, 0] = k2
        distCoeff[2, 0] = p1
        distCoeff[3, 0] = p2

        cam = np.eye(3, dtype=np.float32)

        cam[0, 2] = cols / 2.0

        cam[1, 2] = rows / 2.0

        cam[0, 0] = 10.0
        cam[1, 1] = 10.0

        return cv2.fisheye.undistortImage(self.image, cam, distCoeff, None, cam)
