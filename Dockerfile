FROM python:3.8-slim
WORKDIR /img2txt
COPY . /img2txt
RUN apt-get update
RUN apt-get install poppler-utils -y
RUN apt install tesseract-ocr -y
RUN apt-get install tesseract-ocr-all -y
RUN apt install libtesseract-dev -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install -r requirements.txt
RUN chmod +x gunicorn_starter.sh
EXPOSE 5001
CMD ["python", "app.py"]
