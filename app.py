from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Expense database model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(100), nullable=False)
    Category = db.Column(db.String(100), nullable=False)
    Amount = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.String(20), nullable=False)


# Create database tables
with app.app_context():
    db.create_all()


# Homepage: display and add expenses
@app.route("/", methods=["GET", "POST"])
def hello_World():

    if request.method == "POST":
        try:
            description = request.form["Description"].strip()
            amount = int(request.form["Amount"])
            category = request.form["Category"]
            date = request.form["Date"]

            if not description or not category or not date or amount <= 0:
                return "Please enter valid expense details.", 400

            new_expense = Expense(
                Description=description,
                Amount=amount,
                Category=category,
                Date=date
            )

            db.session.add(new_expense)
            db.session.commit()

        except (ValueError, KeyError):
            db.session.rollback()
            return "Invalid expense details. Please try again.", 400

        return redirect(url_for("hello_World"))

    expenses = Expense.query.order_by(Expense.id.desc()).all()

    return render_template(
        "index.html",
        expenses=expenses
    )


# Delete an expense
@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):

    expense = db.session.get(Expense, expense_id)

    if expense:
        db.session.delete(expense)
        db.session.commit()

    return redirect(url_for("hello_World"))


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
