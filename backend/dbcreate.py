from flask import Flask
from models import Patient, db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/labus_rsiot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # создаем пациентов
        patient1 = Patient(name='Arthur', sec_name='Novikow', area=1)
        patient2 = Patient(name='Gleb', sec_name='Ulianov', area=2)
        patient3 = Patient(name='Iliya', sec_name='Jefferson', area=1)
        patient4 = Patient(name='Ivan', sec_name='Shpigun', area=3)
        db.session.add_all([patient1, patient2, patient3, patient4])
        db.session.commit()