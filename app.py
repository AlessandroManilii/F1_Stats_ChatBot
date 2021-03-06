from flask import Flask, send_file
from FlaskNgrok import run_with_ngrok


  
app = Flask(__name__)
run_with_ngrok(app) # Start ngrok when app is run
  
@app.route("/")
def hello():
    return "Hello"

@app.route('/img/<path:path>')
def get_image(path):
    image_path = 'img/{}'.format(path)

    return send_file(image_path, mimetype='image/png')
  
if __name__ == "__main__":
  app.run()


