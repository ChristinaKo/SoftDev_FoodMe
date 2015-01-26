from flask import Flask, render_template, request, redirect, session, url_for, session, escape, flash
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
            return redirect(url_for('login',redirect_user = True))
    return wrap

@app.route("/about", methods=["POST","GET"])
def about():
    if request.method == "POST":
        if request.form['searched']!= "":
            return redirect(url_for("recipeList", tag = request.form['searched']))
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
        return render_template("about.html", loggedin=loggedin,username=username)
    else:
        loggedin = False
    return render_template("about.html", loggedin=loggedin)

@app.route("/help", methods=["POST","GET"])
def help():
    if request.method == 'POST':
        if request.form['searched']!= "":
            return redirect(url_for("recipeList", tag = request.form['searched']))
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
@authenticate
def profile():
    username = escape(session['username'])
    #POST METHOD MEANS UPDATING PASSWORD
    if request.method == 'POST':
        if 'searched' in request.form:
            if request.form['searched']!= "":
                return redirect(url_for("recipeList", tag = request.form['searched']))
        else:
            real_pwd = MongoWork.find_pword(username)
            currpwd = request.form.get("curpas")
            if currpwd != real_pwd:
                flash("Sorry! Please enter the correct current password!")
                return redirect(url_for("profile"))
            newpwdinput = request.form.get("newpas")
            newrepwdinput = request.form.get("newrepas")
            if newpwdinput == newrepwdinput and check_pword(newpwdinput): #matched successfully, update passwords
                username = escape(session['username'])
                MongoWork.update_password(username,newpwdinput)
                flash("Password was successfully updated.")
                return redirect(url_for("profile"))
            elif not check_pword(newpwdinput):
                flash("Your password must be at least SIX characters long and have an uppercase letter, lowercase letter, and a number!")
                return redirect(url_for("profile"))
            else:
                flash("Passwords did not match. Password was not updated.")
                return redirect(url_for("profile"))
    else: #GET METHOD
        user_info = MongoWork.find_usrinfo(username)
        fname = user_info['firstname']
        lname = user_info['lastname']
        u = user_info['uname']
        return render_template("profile.html",fname=fname, lname=lname,u=u); 

@app.route("/recipes/<tag>")
def recipeList(tag):
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
    else:
        loggedin = False
    num = 1
    reclist = []
    while num <=4:
        db = recipes.getSearchVal(tag,num)
        if db['count'] !=  0:
            reclist = reclist + recipes.getrecipes(db, num)
            num =  num + 1
        else:
            break
    return render_template("recipes.html", loggedin = loggedin, tag = tag, reclist = reclist)    

@app.route("/recipes/<tag>/<num>/<title>", methods=["POST","GET"])
def recipe(tag, num, title):
    db = recipes.getSearchVal(tag, num)
    nurl = recipes.geturls(db, title)
    rec = recipes.retrecipe(nurl[0]) 
    ing = recipes.reting(nurl[1])
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
    else:
        loggedin = False
    if request.method == 'POST':
        if 'searched' in request.form:
            print "remove me"
            #############ADDDDDDDDDDDDDDDDDDD STUFFFFF HERRRRREEEEEEEE
        else:
            if loggedin: #logged in: add to favorites, redirect to same page, and flash message
                mongo_input =  {'title': title,
                                'ing': ing,
                                'rec': rec }
                MongoWork.update_favorites(username, mongo_input)
                print MongoWork.find_favorites(username)
                flash("Added recipe to Favorites!");
                return redirect(url_for("recipe", tag = tag, num=num, title=title))
            else:
                flash("Please log in to use the Add to Favorites feature!")
                return redirect(url_for("recipe", tag = tag, num=num, title=title))
    else: ##GET METHOD
        return render_template("recipe.html", loggedin=loggedin, title=title, rec = rec, ing = ing)
    
@app.route("/login", methods=["POST","GET"])
def login():
    error = None
    if request.method == 'POST':
        if 'searched' in request.form:
            if request.form['searched']!= "": #using search bar
                return redirect(url_for("recipeList", tag = request.form['searched']))
        else:
            userinput = request.form['user']
            pwdinput = request.form['passwd']
            #print MongoWork.check_user_in_db(userinput)
            if MongoWork.check_user_in_db(userinput) != None:
                if MongoWork.find_pword(userinput) == pwdinput: ##SUCCESSFULLY LOGGED IN
                    session['username'] = userinput
                    redirect_necessary = request.args.get('redirect_user')
                    #redirecting after login
                    if redirect_necessary:
                        return redirect(url_for("profile"))
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

@app.route("/favorite", methods=["POST","GET"])
@authenticate
def favorite():
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
    else:
        loggedin = False
    if request.method == 'POST':
        if request.form['searched']!= "":
            return redirect(url_for("recipeList", tag = request.form['searched']))
    else:
        favorites = MongoWork.find_favorites(username)
        if favorites == None:
            empty = True
            return render_template("favorite.html", empty=empty)
        else:
            print favorites
            return render_template("favorite.html", favorites=favorites)
        #return render_template("favorite.html",rand=recofday.rand())
    
@app.route("/random", methods=["POST","GET"])
def random():
    if request.method == "POST":
        if request.form['searched']!= "":
            return redirect(url_for("recipeList", tag = request.form['searched']))
    rand = recofday.rand()
    randrec = recipes.retrecipe(rand['source_url'])
    randing = recipes.reting(rand['f2f_url'])
    if 'username' in session:
        loggedin = True
        username = escape(session['username'])
        return render_template("random.html", loggedin=loggedin,username=username, randrec=randrec, randing=randing, randtitle= rand['title'])
    else:
        loggedin = False
    return render_template("random.html", loggedin=loggedin, randrec=randrec, randing= randing, randtitle=rand['title'])

#must pop off session
@app.route("/logout")
def logout():
    #remove username from session
    session.pop('username', None)
    return redirect(url_for("index"))

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        if 'searched' in request.form:
            if request.form['searched']!= "":
                return redirect(url_for("recipeList", tag = request.form['searched']))
        else:
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
                                'lastname':lastname,
                                'favorites': {} } 
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
