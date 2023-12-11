from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DBASE_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_CODE")

db = SQLAlchemy()
db.init_app(app)

PASSWORD = os.environ.get("PASSWORD")

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

#--------------CREATING ALERT------------------#
@app.route("/add", methods=["POST"])
def request_post():
    try:
        if PASSWORD != request.form.get("password"):
            return jsonify(response={"Wrong password": 404}), 404
        db.session.add(Alert(name=request.form.get("name"), description=request.form.get("description")))
        db.session.commit()
        return jsonify(response={"Alert has been added": 200}), 200
    except Exception as e:
        return jsonify(error={f"Error: {e}": 404}), 404
#-------------------------------------------------------#


#---------------EDITING THE ALERT DESCRIPTION---------------------------#
@app.route("/edit_description/<int:num>", methods=["PATCH"])
def request_path(num):
    try:
        if PASSWORD != request.form.get("password"):
            return jsonify(response={"Wrong password": 404}), 404
        alert = db.get_or_404(Alert, num)
        if request.form["description"] is not None:
            alert.description = request.form.get("description")
            db.session.commit()
            return jsonify(response={"Alert has been edited": 200}), 200
        else:
            return jsonify(error={f"Error!": 404}), 404
    except Exception as e:
        return jsonify(error={f"Error: {e}": 404}), 404
#-------------------------------------------------------#


#---------------DELETING ALERT---------------------------#
@app.route("/delete/<int:num>", methods=["DELETE"])
def request_delete(num):
    try:
        if PASSWORD != request.form.get("password"):
            return jsonify(response={"Wrong password": 404}), 404
        alert = db.get_or_404(Alert, num)
        db.session.delete(alert)
        db.session.commit()
        return jsonify(response={"Alert has been deleted": 200}), 200
    except Exception as e:
        return jsonify(error={f"Error: {e}": 404}), 404
#-------------------------------------------------------#


#---------------DISPLAYING ALERT---------------------------#
@app.route("/all")
def display_all():
    try:
        alerts = db.session.execute(db.Select(Alert)).scalars().all()
        return jsonify(response=[alert.to_dict() for alert in alerts])
    except Exception as e:
        return jsonify(error={f"Error: {e}": 404}), 404

#-------------------------------------------------------#

#-------------DISPLAYING ALERT BY NAME--------#
@app.route("/display_one", methods=["GET"])
def display_one():
    try:
        name = request.form.get("name")
        alerts = db.session.execute(db.Select(Alert).where(Alert.name == name)).scalars().all()
        return jsonify(response=[alert.to_dict() for alert in alerts])
    except Exception as e:
        return jsonify(error={f"Error: {e}": 404}), 404



#---------------SENDING SMS (ONE ALERT)---------------------------#
@app.route("/send_sms_alert/<int:num>", methods=["POST"])
def send_alert(num):
    try:
        if PASSWORD != request.form.get("password"):
            return jsonify(response={"Wrong password": 404}), 404

        alert = db.get_or_404(Alert, num)
        account_sid = os.environ.get("account_sid")
        auth_token = os.environ.get("auth_token")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
          from_='+12295958359',
          body=f"{alert.name},\n{alert.description}",
          to=request.form.get("number")
        )
        return jsonify(response={"Alert has been sended": 200}), 200
    except Exception as e:
        return jsonify(error={f"Error: {e}": 404}), 404


if __name__ == "__main__":
    app.run(debug=True)


