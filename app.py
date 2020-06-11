from flask import Flask, render_template, jsonify
from db import FacelogDbManager

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.config['CSRF_ENALBLED'] = True

@app.route("/")
@app.route("/home")
def home_page():
	return render_template("home.html", title='Home Page')

@app.route('/get_img', methods = ['GET'])
def get_img_path():
    db = FacelogDbManager("database/facelog.db")
    data = querry_db(db)
    db.close()
    return jsonify(data=data)


def querry_db(db, key_names=["id_img", "datetime_result", "img_path_result"]):
	results = []
	records = db.get_from_table()

	for row in records:
		record_dict = dict()
		record_dict = {key: value for key, value in zip(key_names, row)} 
		results.append(record_dict)

	return results

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=2810)