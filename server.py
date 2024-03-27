from flask import Flask

app = Flask(__name__)

@app.route("/test")
def test():
    return "This is a test to see if Flask is working right"

if __name__ == "__main__":
    app.run(debug = True)