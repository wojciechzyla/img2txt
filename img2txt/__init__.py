#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath("img2txt/temp_files")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from img2txt import routes
