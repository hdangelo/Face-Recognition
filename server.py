# http://flask.pocoo.org/docs/patterns/fileuploads/
import os
from flask import Flask, request, redirect, url_for, send_from_directory, json, Response, jsonify
from classReconocimiento import clsReconocimiento
import json

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
rec = clsReconocimiento()
def allowed_file(filename):
  # this has changed from the original example because the original did not work for me
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':        
        file = request.files['file']
        if file and allowed_file(file.filename):
            #print ('**found file', file.filename)
            
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # for browser, add 'redirect' function on top of 'url_for'
            caras = rec.Reconocimiento('upload/' + filename)
            print(caras)
            #js= jsonify(caras)
            resp = jsonify(caras) #Response(js, status=200, mimetype='application/json')
            print(resp)
            #resp = caras #Response(js, status=200, mimetype='application/json')
            resp.status_code = 200
            resp.headers['Link'] = 'http://localhost:5000'
            
            return resp
            #return url_for('uploaded_file', filename=filename, caras)
    return 
    '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)

if __name__ == '__main__':
	app.run(debug=False)