from flask import Flask, send_file
from flask_ngrok import run_with_ngrok
  
app = Flask(__name__)
run_with_ngrok(app)
  
@app.route("/")
def hello():
    return "Hello"

@app.route('/img/<path:path>')
def get_image(path):
    image_path = 'img/{}'.format(path)

    return send_file(image_path, mimetype='image/gif')
  
if __name__ == "__main__":
  app.run()


