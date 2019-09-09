#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploaded_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 校验用户上传的文件是否是ALLOWED_EXTENSIONS常量指定的后缀
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if file and allowed_file(file.filename):
        if file: # 暂时不做文件后缀名检查
            # secure_filename函数会将文件名中的中文内容过滤掉，解决方法有两种：
            # 1. 修改secure_filename函数源码；
            # 2. 不使用该函数，直接用file.filename作为文件名，不安全
            # filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file',filename=filename))  # 上传完重定向到该文件的下载页面
            return redirect(request.url)
            
    html_template = '''<!DOCTYPE html>
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>文件分享工具 - IT魔君</title>
</head>
<body>
    <h1>上传文件</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="上传">
    </form>
    <hr>

    %s

    <script>
        document.forms[0].onsubmit = function() {
            var file_path = document.getElementsByName("file")[0].value;
            if (! file_path) {
                alert("请选择要上传的文件！");
                return false;
            }
        };
    </script> 
</body>
</html>'''

    file_names = os.listdir("./uploaded_files")
    uploaded_file_list = ""
    for f in file_names:
        uploaded_file_list += '<a href="/download/%s">%s</a><br />' % (f, f)

    return (html_template % uploaded_file_list)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
