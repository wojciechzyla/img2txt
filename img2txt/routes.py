#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from flask import request, Response
from werkzeug.utils import secure_filename
from img2txt import app
from img2txt.convert_to_txt import Pdf2txt, Image2text
import os
import cv2
import base64
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['POST'])
def convert_image():
    if 'file' not in request.json:
        message = json.dumps({"info": "No file included"})
        resp = Response(message, status=406, mimetype='application/json')
        return resp
    pdf_b64 = request.json['file']
    file = base64.b64decode(pdf_b64.encode('utf-8'))
    file_name = secure_filename(request.json['filename'])
    if file and allowed_file(file_name):
        filename = secure_filename(file_name)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb") as f:
            f.write(file)
        if file_name.rsplit('.', 1)[1].lower() == 'pdf':
            preprocess = Pdf2txt(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            preprocess = Image2text([image])
        result = preprocess.convert()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        message = json.dumps({"file_name": f'{filename}', "text": result})
        resp = Response(message, status=200, mimetype='application/json')
        return resp
    else:
        message = json.dumps({"info": "Wrong file type"})
        resp = Response(message, status=406, mimetype='application/json')
        return resp

