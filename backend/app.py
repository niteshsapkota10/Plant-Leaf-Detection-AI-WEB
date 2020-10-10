import os
from predict_leaves import get_prediction
from flask import Flask,render_template,request,redirect,jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
app=Flask(__name__)

app.config["IMAGE_UPLOADS"] = "static/images"
app.config["ALLOWED_IMAGE_EXTENSIONS"]=["JPEG","JPG","PNG"]


def check_extension(filename):
    if not "." in filename:
        return False
    ext=filename.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template("index.html",result=None,img=None,category_percentage=None)

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method=='GET':
        return redirect('/')
    if request.method=='POST':
        file_name=request.files['file']
        if check_extension(file_name.filename):
            file_name.save(os.path.join(app.config["IMAGE_UPLOADS"],file_name.filename))
            name=file_name.filename
            path="static/images/"+name
            result,prob_cat=get_prediction(path)
        else:
            path=None
            prob_cat=None
            result="Unable to Compute"
            name="Extension not allowed"
        return render_template("index.html",result=result,img=path,category_percentage=prob_cat)

@app.route('/rest/upload/',methods=['POST'])
@cross_origin()
def rest_upload():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and check_extension(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        path="static/images/"+filename
        image_path="http://127.0.0.1:5000/static/images/"+filename
        result,prob_cat=get_prediction(path)
        resp = jsonify({"result":result,"Category_Probability":prob_cat,"image_path":image_path})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(
            {'message': 'Allowed file types are png, jpg, jpeg'})
        resp.status_code = 400
        return resp

if __name__=="__main__":
    app.run(debug=True)