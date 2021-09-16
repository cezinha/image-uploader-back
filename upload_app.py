import os
from flask import Flask, request, send_from_directory
from flask_restful import reqparse, Resource, Api
from flask_cors import CORS
from werkzeug.utils import secure_filename
import werkzeug

DIRNAME = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(DIRNAME, 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__)
cors = CORS(app, resources={r"/upload/*": {"origins": "*"}})
api = Api(app)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory(UPLOAD_FOLDER, path)

# shows a list of all books, and lets you POST to add new titles
class UploadFiles(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()

  def post(self):
    if 'file' not in request.files:
      return { "success": False, "errors": ["no file part"] }, 422

    file = request.files['file']

    if file.filename == '':
      return { "success": False, "errors": ["no selected file"] }, 422

    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      self.parser.add_argument("file", type=werkzeug.datastructures.FileStorage, location='files')
      args = self.parser.parse_args()
      file.save(os.path.join(UPLOAD_FOLDER, filename))
      return { "success": True, "errors": [], "file": f"/images/{filename}" }, 201

    return { "success": False, "errors": ["invalid file"] }, 422


api.add_resource(UploadFiles, '/upload')

if __name__ == '__main__':
  app.run(debug=True, port=5000)
