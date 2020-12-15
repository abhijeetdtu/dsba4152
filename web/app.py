from flask import Flask , render_template , request
from base64 import b64decode
import urllib.request


from model_helper import ModelHelper , path_to_img

path_to_model = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba4152\\data\\e_mdm_20\\e_mdm"

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/predict" , methods=["POST"])
def predict():
    #data_uri = "data:image/png;base64,iVBORw0KGg..."
    # Python 2 and <Python 3.4

    data_uri = request.json["image_data"]
    same_scale =  request.json["same_scale"]
    with urllib.request.urlopen(data_uri) as response:
        data = response.read()
        with open("image.png", "wb") as f:
            f.write(data)

    ModelHelper(path_to_model).predict(same_scale)
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)
