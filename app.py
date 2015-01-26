from flask import Flask, render_template, request, redirect, session, url_for, session, escape
from functools import wraps
import MongoWork, recofday
import re
import recipes
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
    if request.method == "POST":
        if request.form['searched']!= "":
            return redirect(url_for("recipeList", tag = request.form['searched']))
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

@app.route("/recipes/<tag>")
def recipeList(tag):
    num = 0
    reclist = []
    while num <=5:
        db = recipes.getSearchVal(tag,num)
        if db['count'] !=  0:
            reclist = reclist + recipes.getrecipes(db, num)
            num =  num + 1

        else:
            break
    return render_template("recipes.html", tag = tag, reclist = reclist)    
@app.route("/recipes/<tag>/<num>/<title>")
def recipe(tag, num, title):
    db = recipes.getSearchVal(tag, num)
    nurl = recipes.getsurl(db, title)
    rec = recipes.retrecipe(nurl) 
    return render_template("recipe.html", title=title, rec = rec)
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
        return render_template("random.html", loggedin=loggedin,username=username, rand=recofday.rand())
    else:
        loggedin = False
    return render_template("random.html", loggedin=loggedin, rand=recofday.rand())

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
            elif not check_pword(passw):
                bad_pword = True
                return render_template("register.html", bad_pword = bad_pword)
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

#helper fxn to search for uppercase letter
def findUpper(word):
    for a in word:
        if ord(a) >= ord('A') and ord(a) <= ord('Z'):
            return True
    return False

#helper fxn to search for lowercase letter
def findLower(word):
    for a in word:
        if ord(a) >= ord('a') and ord(a) <= ord('z'):
            return True
    return False

#helper fxn to search for number
def findNumber(s):
    for a in s:
        if ord(a) >= ord('0') and ord(a) <= ord('9'):
            return True
    return False

def check_pword(pword):
    return findUpper(pword) and findLower(pword) and findNumber(pword) and len(pword) >= 6

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
