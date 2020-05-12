from flask import Flask,render_template,redirect,url_for,request
import os
from PIL import Image
import pymongo
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['MONGO_URI'] = 'conn url '
app.config['IMAGE_UPLOADS'] = '/home/anonymous/Desktop/core/static/img/uploads'
app.config['ALLOWED_IMAGE_EXTENSIONS'] =['PNG','JPG','JPEG','GIF','SVG']

mongo = PyMongo(app)
def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/upload-image',methods=['GET','POST'])
def upload_image():

    if request.method == 'POST':
        if  request.files:
            image = request.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                mongo.save_file(image.filename,image)
                mongo.db.users.insert({'id':1,'profile_img_name':filename})
                print("Image saved")
                return redirect(request.url)
            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template('upload_img.html')



@app.route('/profile/<username>')
def profile(username):
    user = mongo.db.users.find_one_or_404({'username':username})
    return f'''
    <h1>{username}</h1>
    <img src="{url_for('file',filename=user['profile_img_name'])}
    '''

if __name__ == '__main__':
    app.run(debug=True)
