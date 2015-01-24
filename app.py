from flask import Flask, render_template, request, redirect, session, url_for, session, escape
from functools import wraps
import MongoWork
import re

app = Flask(__name__)
app.secret_key = "Really secret but not really secret." #session usage

def authenticate(f):
    @wraps(f)
    def wrap(*args):
        if 'username' in session:
            return f(*args)
        else:
            flash("You must log in to see that page.")
            return redirect(url_for('index',redirect_user = True))
    return wrap

@app.route("/about", methods=["POST","GET"])
def about():
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
        return render_template("about.html", loggedin=loggedin,username=username)
    else:
        loggedin = False
    return render_template("about.html", loggedin=loggedin)

@app.route("/help", methods=["POST","GET"])
def help():
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
        return render_template("help.html", loggedin=loggedin,username=username)
    else:
        loggedin = False
    return render_template("help.html", loggedin=loggedin)

@app.route("/", methods=["POST","GET"])
def index():
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
        return render_template("index.html", loggedin=loggedin,username=username)
    else:
        loggedin = False
    return render_template("index.html", loggedin=loggedin)

@app.route("/profile", methods=["POST","GET"])
def profile():
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
        return render_template("profile.html", loggedin=loggedin,username=username)
    else:
        loggedin = False
    return render_template("profile.html", loggedin=loggedin)

@app.route("/login", methods=["POST","GET"])
def login():
    error = None
    if request.method == 'POST':
        userinput = request.form['user']
        pwdinput = request.form['passwd']
        #print MongoWork.check_user_in_db(userinput)
        if MongoWork.check_user_in_db(userinput) != None:
            if MongoWork.find_pword(userinput) == pwdinput: ##SUCCESSFULLY LOGGED IN
                session['username'] = userinput
                redirect_necessary = request.args.get('redirect_user')
                #redirecting after login
                if redirect_necessary:
                    return redirect(url_for("user"))
                else:
                    return redirect(url_for('index',username=userinput))
            else:#incorrect password error
                error = True
                return render_template("login.html" ,error=error)
        else:
            #print "not in users"
            notreg = True
            return render_template("login.html", notreg = notreg)
    else:#request.method == "GET"
        error = None
        return render_template("login.html")
'''
@app.route("/dashboard")
@authenticate
def dashboard():
    username = escape(session['username'])
    return render_template("dashboard.html",username=username)
'''

@app.route("/favorite", methods=["POST","GET"])
def favorite():
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
        return render_template("favorite.html", loggedin=loggedin,username=username)
    else:
        loggedin = False
    return render_template("favorite.html", loggedin=loggedin)

@app.route("/random", methods=["POST","GET"])
def random():
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
        return render_template("random.html", loggedin=loggedin,username=username)
    else:
        loggedin = False
    return render_template("random.html", loggedin=loggedin)

#must pop off session
@app.route("/logout")
def logout():
    #remove username from session
    session.pop('username', None)
    return redirect(url_for("index"))

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        usr = request.form['username']
        passw = request.form['passwd']
        repassw = request.form['repasswd']
        firstname = request.form['fname']
        lastname = request.form['lname']
        if passw == repassw and usr!='' and passw!='' and firstname!='' and lastname!='':#checks if everything is filled out
        #retVals = ' %s , %s, %s, %s , %s ' % (usr, passw, repassw, firstname, lastname)
            mongo_input = { 'uname':usr,
                            'password':passw, 
                            'firstname':firstname,
                            'lastname':lastname } 
            #print mongo_input
            #print MongoWork.check_user_in_db(usr)
            if MongoWork.check_user_in_db(usr):
                user_taken = True
                return render_template("register.html",user_taken=user_taken, usr=usr)
            elif re.match('''^[~!@#$%^&*()_+{}":;']+$''', usr): #has special characters!
                special_char = True
                return render_template("register.html", special_char=special_char)
            else:####SUCCESS!
                MongoWork.new_user(mongo_input) #put user into our mongodb
                registered = True
                return redirect(url_for("index",registered=registered)) 
        else: #aka passwd !=repassw OR not all filled out
            if passw != repassw:#pwd and re-type pwd fields do not match
                reg_error = True
                return render_template("register.html", reg_error=reg_error)
            else:#missing field error
                empty=True
                return render_template("register.html", empty=empty)
    else:#GET method
        return render_template("register.html")


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
