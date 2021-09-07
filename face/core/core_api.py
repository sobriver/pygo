from flask import Flask

app = Flask(__name__)

@app.route('/feature/gen')
def gen_feature():
    """
    产生feature
    """
    pass



if __name__ == '__main__':
    app.run()