from flask import Flask, render_template, request
from flask_cors import CORS
from server import *

app = Flask("app",
  template_folder="../templates", # name of folder containing html templates
  static_folder="../static" # name of folder for static files
)
CORS(app)

@app.route('/')  # '/' for the default page
def home():
  init_db()
  return render_template('index.html')

@app.route('/list-inv', methods=['GET'])
def get_inv():
  if request.method == "GET":
    text = list_inventory()
    return render_template('index.html', inv=text)

@app.route('/list-ship', methods=['GET'])
def get_ship():
  if request.method == "GET":
    text = list_shipments()
    return render_template('index.html', ship=text)

@app.route('/create-inv', methods=['POST'])
def create_inv():
  if request.method == "POST":
    data = request.form.to_dict()
    if (data["action"] == "create inventory"):
        text = create_inventory(data["name"], data["amount"])
    else:
        text = edit_inventory(data["name"], data["amount"])
    return render_template('index.html', create_inv_resp=text)

@app.route('/del-inv', methods=['POST'])
def del_inv():
  if request.method == "POST":
    data = request.form.to_dict()
    text = del_inventory(data["name"])
    return render_template('index.html', del_inv_resp=text)

@app.route('/create-ship', methods=['POST'])
def create_ship():
  if request.method == "POST":
    data = request.form.to_dict()
    if (data["action"] == "create shipment"):
      text = create_edit_shipment(data["ship"], data["inv"], data["amount"], create=True)
    else:
      text = create_edit_shipment(data["ship"], data["inv"], data["amount"], create=False)
    return render_template('index.html', ship_resp=text)
    
if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=5000,
    debug=True
	)