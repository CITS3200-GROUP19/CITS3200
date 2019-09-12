from flask import *
from flask import render_template, request
app = Flask(__name__)

@app.route("/")
def login():
	return render_template("login.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/admin")
def admin():
	return "admin"

@app.route("/cookie")
def cookie():
	res = make_response("<h1>cookie</h1>")
	res.set_cookie('foo','bar')
	return res

@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/login_error")
def login_error():
	return "Invalid username or password. Please try again."

@app.route("/login_success",methods = ["POST"])
def login_success():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["pass"]

	if password=="test":
		resp = make_response(render_template("success.html"))
		resp.set_cookie("email",email)
		return resp
	else:
		return redirect(url_for("login_error"))

@app.route("/user")
def user():
	email = request.cookies.get("email")
	resp = make_response(render_template("user_profile.html",name = email))
	return resp

@app.route("/user_manual")
def user_manual():
	return "user manual"

@app.route("/query")
def query():
	return "query"

#@app.route("/customer")
#def customer():
#	return render_template("customer.html")

#@app.route("/success",methods = ["POST","GET"])
#def display_data():
#	if request.method == "POST":
#		result = request.form
#		return render_template("result.html",result = result)


def page(pageName):
	if pageName == "about":
		return redirect(url_for("about"))
	if pageName == "admin":
		return redirect(url_for("admin"))
	if pageName == "login":
		return redirect(url_for("login"))
	if pageName == "query":
		return redirect(url_for("query"))


#app.add_url_rule("/about","about",about)

if __name__ == "__main__":
    app.run(debug = True)

