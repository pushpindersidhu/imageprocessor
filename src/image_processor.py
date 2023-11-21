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
    def powlawtrans(self, gamma):
        gamma = float(gamma)
        gamma_corrected = np.array(255 * (self.image / 255) ** gamma, dtype="uint8")
        return gamma_corrected
