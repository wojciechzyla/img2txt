#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from typing import List
import pdf2image
import cv2
import numpy as np
import pytesseract


class Image2text:
    def __init__(self, images: List):
        self.images_ = images
        self.texts = []

    def convert(self):
        for image in self.images_:
            # change image to gray
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # binarize image
            image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            custom_config = r'-l pol'
            # extract text from image
            txt = pytesseract.image_to_string(image, config=custom_config)
            self.texts.append(txt)
        return self.texts


class Pdf2txt(Image2text):
    def __init__(self, pdf_path):
        images = pdf2image.convert_from_path(pdf_path)
        for i in range(len(images)):
            images[i] = np.asarray(images[i])
        super(Pdf2txt, self).__init__(images)
