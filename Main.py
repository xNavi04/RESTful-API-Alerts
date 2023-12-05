from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DBASE_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_CODE")

db = SQLAlchemy()
db.init_app(app)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100))

with app.app_context():
    db.create_all()

#--------------TWORZENIE  ALERTU------------------#
@app.route("/add", methods=["POST"])
def request_post():
    try:
        db.session.add(Alert(name=request.form.get("name"), description=request.form.get("description")))
        db.session.commit()
        return jsonify(response={"Alert has been added": 200}), 200
    except Exception as e:
        return jsonify(error={f"Error: {e}": 404}), 404
#-------------------------------------------------------#


#---------------EDYCJA OPISU ALERTU---------------------------#
@app.route("/edit_description/<int:num>", methods=["PATCH"])
def request_path(num):
    try:
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


#---------------USUWANIE ALERTU---------------------------#
@app.route("/delete/<int:num>", methods=["DELETE"])
def request_delete(num):
    try:
        alert = db.get_or_404(Alert, num)
        db.session.delete(alert)
        db.session.commit()
        return jsonify(response={"Alert has been deleted": 200}), 200
    except Exception as e:
        return jsonify(error={f"Error: {e}": 404}), 404
#-------------------------------------------------------#


#---------------SEND SMS---------------------------#
@app.route("/send_sms_alert/<int:num>", methods=["POST"])
def send_alert(num):
    try:
        alert = db.get_or_404(Alert, num)
        account_sid = os.environ.get("account_sid")
        auth_token = os.environ.get("auth_token")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
          from_='+12295958359',
          body=f"{alert.name},\n{alert.description}",
          to=os.environ.get("my_number")
        )
        return jsonify(response={"Alert has been sended": 200}), 200
    except Exception as e:
        return jsonify(error={f"Error: {e}": 404}), 404


if __name__ == "__main__":
    app.run(debug=True)


