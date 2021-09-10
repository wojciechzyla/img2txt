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
import threading
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/<user_id>", methods=['POST'])
def convert_image(user_id):
    data = request.get_json()

    def retrieve_text(**kwargs):
        URL_PANEL = os.environ.get("URL_PANEL")
        params = kwargs.get('post_data')

        pdf_b64 = params['file']
        file = base64.b64decode(pdf_b64.encode('utf-8'))
        file_name = secure_filename(params['filename'])
        token = params['token']

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

            message = {"file_name": f'{filename}',
                       "text": result,
                       "token": token,
                       "status_code": 200}
            requests.post(URL_PANEL + "/" + file_name + "/" + str(user_id), json=message)
        else:
            message = {"info": "Wrong file type",
                       "status_code":  406}
            requests.post(URL_PANEL + "/" + file_name + "/" + str(user_id), json=message)

    thread = threading.Thread(target=retrieve_text, kwargs={'post_data': data})
    thread.start()
    return {"info": "accepted"}, 202
