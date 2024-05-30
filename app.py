import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "POST":
        print("ENTERING PORTFOLIO")
    else:
        user_id = int(session["user_id"])
        cashl = db.execute("SELECT cash FROM users WHERE id=?", user_id)
        cash = cashl[0]['cash']
        # index=db.execute("SELECT symbol, SUM(shares), price, SUM(total) FROM transactions WHERE user_id=? GROUP BY symbol",user_id)
        index = db.execute("SELECT * FROM portfolio WHERE user_id=?", user_id)
        tototal = 0
        for fafa in index:
            tototal = tototal+fafa['total']
        total = tototal+cash
        return render_template("index.html", index=index, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    user = db.execute("SELECT ID,username,cash FROM users")
    user_id = int(session["user_id"])
    name = user[user_id-1]["username"]
    owns = db.execute("SELECT symbol FROM portfolio WHERE user_id=?", user_id)
    cashl = db.execute("SELECT cash FROM users WHERE id=?", user_id)
    cash = cashl[0]['cash']
    symbol = request.form.get("symbol")
    symbol = str(symbol)
    symbol = symbol.upper()
    amount = request.form.get("shares")
    time = datetime.now()
    sign = 0
    if request.method == "POST":
        if not symbol:
            return apology("No symbol", 403)
        if not amount:
            return apology("No amount", 403)
        try:
            amount = float(amount)
        except:
            return apology("ENTER number for shares")

        if amount < 0.0:
            return apology("Do not enter negative")
        if amount % 1 != 0.0:
            return apology("Do not enter fraction")

        if lookup(symbol) is None:
            return apology("Invalid symbol is entered", 400)

        total = int(lookup(symbol)['price'])*float(amount)
        if cash < total:
            return apology("Not enough cash", 403)

        for i in owns:
            if symbol == i['symbol']:
                sign = 1
                break

        if sign == 0:
            db.execute("INSERT INTO portfolio (user_id,symbol,shares,price,total) VALUES(?,?,?,?,?)",
                       user_id, symbol, int(amount), int(lookup(symbol)['price']), total)
            db.execute("INSERT INTO transactions (user_id,symbol,shares,price,total,transacted) VALUES(?,?,?,?,?,?)",
                       user_id, symbol, int(amount), int(lookup(symbol)['price']), total, time)
            db.execute("UPDATE users SET cash=?-? WHERE id=?", cash, total, user_id)
            # return render_template("temp.html",name=name,total=total,user_id=user_id,symbol=symbol,user=user)
            return redirect("/")
        else:
            print(type(total))
            db.execute("INSERT INTO transactions (user_id,symbol,shares,price,total,transacted) VALUES(?,?,?,?,?,?)",
                       user_id, symbol, int(amount), int(lookup(symbol)['price']), total, time)
            db.execute("UPDATE portfolio SET shares=shares+?, total=total+? WHERE user_id=? AND symbol LIKE ?",
                       int(amount), total, user_id, symbol)
            db.execute("UPDATE users SET cash=?-? WHERE id=?", cash, total, user_id)
            # return render_template("temp.html",name=name,total=total,user_id=user_id,symbol=symbol,user=user)
            asdf = db.execute("SELECT * FROM users WHERE id=?", user_id)
            print(asdf[0]['cash'])
            return redirect("/")

    else:
        return render_template("buy.html")
    """Buy shares of stock"""


@app.route("/history")
@login_required
def history():
    user_id = int(session["user_id"])
    indexl = db.execute("SELECT * FROM transactions WHERE user_id=?", user_id)
    if request.method == "POST":
        print("Hi")
        return apology("TODO")
    else:
        return render_template("history.html", indexl=indexl)
    """Show history of transactions"""


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        symbol = str(symbol)
        symbol = symbol.upper()
        if not symbol:
            return apology("NO SYMBOL", 400)
        if lookup(symbol) is None:
            return apology("Invalid Symbol", 400)
        simba = lookup(symbol)
        print(type(simba['price']))
        # simba['price']=str(simba['price'])
        print(type(simba['price']))
        # price=simba['price']
        # return apology("Search successfull",403)
        return render_template("quoted.html", simba=simba)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        if not request.form.get("password"):
            return apology("must provide password", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username,hash) VALUES(?,?)", username, hash)
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = int(session["user_id"])
    cashl = db.execute("SELECT cash FROM users WHERE id=?", user_id)
    cash = cashl[0]['cash']
    owns = db.execute("SELECT symbol FROM portfolio WHERE user_id=?", user_id)
    symbol = request.form.get("symbol")
    symbol = str(symbol)
    symbol = symbol.upper()
    shares = request.form.get("shares")
    sign = 0
    time = datetime.now()

    if request.method == "POST":
        if not symbol:
            return apology("No symbol")
        if not shares:
            return apology("No shares")
        for i in owns:
            if symbol == i['symbol']:
                sign = 1
                break
        if sign == 0:
            if lookup(symbol) is None:
                print(lookup(symbol))
                return apology("Invalid symbol is entered", 400)
            return apology("You do not own this stock")
        else:
            owned = db.execute("SELECT shares FROM portfolio WHERE user_id=? AND symbol LIKE ?", user_id, symbol)
            if int(shares) > int(owned[0]['shares']):
                return apology("Not enough shares")
            else:
                print(f"{shares} were bought and {int(owned[0]['shares'])-int(shares)} is left user_id: {user_id}")
                db.execute("UPDATE portfolio SET shares=?-? WHERE user_id=? AND symbol LIKE ?",
                           int(owned[0]['shares']), int(shares), user_id, symbol)
                db.execute("UPDATE users SET cash=?+? WHERE id=?", cash, int(lookup(symbol)['price'])*int(shares), user_id)
                total = int(lookup(symbol)['price'])*float(shares)
                db.execute("INSERT INTO transactions (user_id,symbol,shares,price,total,transacted) VALUES(?,?,?,?,?,?)",
                           user_id, symbol, int(shares), int(lookup(symbol)['price']), total, time)

                return redirect("/")

    else:
        return render_template("sell.html")
