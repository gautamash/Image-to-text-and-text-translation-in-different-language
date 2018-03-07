import os
from flask import Flask, render_template, request,send_from_directory
from flask_locale import Locale, _
from Image_to_text import test
import shlex
import locale
import subprocess
__author__ = 'Ashwani'



app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
APP_ROOT = "/home/ubuntu/flaskapp"
locale = Locale(app)
@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT)
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        print(filename)
        destination = "/".join([target, 'Img1.png'])
        print(destination)
        file.save(destination)
    text,TransText=test()
    return render_template("complete.html",text=text,TransText=TransText,user_image="static/Img1.png")
	
if __name__ == "__main__":
    #app.run(host='192.168.43.145',port=4555, debug=True)
	app.run(port=4555, debug=True)