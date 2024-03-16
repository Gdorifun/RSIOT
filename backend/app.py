from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import Patient, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/labus_rsiot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

@app.route("/")
def home():
    return "Лабораторные Якубца Глеба"


@app.route("/show", methods=['GET', 'POST'])
def show():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_Patient = Patient(name=post_data.get('name'), sec_name=post_data.get('sec_name'), area=int(post_data.get('area')))
        db.session.add(new_Patient)
        db.session.commit()
        response_object['message'] = 'Patient added!'
    else:
        patients_list =[i.serialize for i in Patient.query.order_by(Patient.id).all()]
        response_object['patients'] = patients_list
    return jsonify(response_object)


@app.route('/show/<patient_id>', methods=['PUT', 'DELETE'])
def single_patient(patient_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        Patient.query.filter(Patient.id == patient_id).update({Patient.name: post_data.get('name'), Patient.sec_name: post_data.get('sec_name'), Patient.area: int(post_data.get('area'))}, synchronize_session = 'fetch')
        db.session.commit()
        response_object['message'] = 'Patient updated!'
    if request.method == 'DELETE':
        dead_patient = Patient.query.filter(Patient.id == patient_id).one()
        db.session.delete(dead_patient)
        db.session.commit()
        response_object['message'] = 'Patient died!'
    return jsonify(response_object)


@app.route("/show1", methods=['GET', 'POST'])
def show1():
    patients_list = Patient.query.all()
    return render_template('show.html', patients=patients_list)

@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_Patient = Patient(name=request.form.get('name'), sec_name=request.form.get('sec_name'), area=request.form.get('area'))
        db.session.add(new_Patient)
        db.session.commit()
        return render_template('add.html')
    else:
        return render_template('add.html')


@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        dead_patient = Patient.query.filter(Patient.id == request.form.get('del')).one()
        db.session.delete(dead_patient)
        db.session.commit()
        return render_template('delete.html')
    else:
        return render_template('delete.html')


@app.route("/change", methods=['POST', 'GET'])
def change():
    if request.method == 'POST':
        Patient.query.filter(Patient.id == request.form.get('chg')).update({Patient.id:  "" + request.form.get('id'), Patient.name: "" + request.form.get('name'), Patient.sec_name: "" + request.form.get('sec_name'), Patient.area: "" + request.form.get('area')}, synchronize_session = 'fetch')
        print("1"+request.form.get('name'))
        db.session.commit()
        return render_template('change.html')
    else:
        return render_template('change.html')


if __name__ == '__main__':
    app.run(debug=True)