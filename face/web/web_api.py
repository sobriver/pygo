from flask import Flask

app = Flask(__name__)

@app.route('/record/list')
def get_record_list():
    """
    记录列表
    """
    pass

@app.route('/person/add')
def add_person():
    """
    添加人员
    """
    pass





if __name__ == '__main__':
    app.run()