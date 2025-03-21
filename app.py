from flask import Flask, request, render_template
import datetime
import sqlite3
import google.generativeai as genai
import os

app = Flask(__name__)

flag = 1
key = "AIzaSyCvLtcDVKeqamwpdQSwPfx0tVL7wiaIeNs"
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/main", methods=["post", "get"])
def main():
    global flag
    if flag == 1:
        user_name = request.form.get("q", "")
        t = datetime.datetime.now()
        conn = sqlite3.connect("user.db")
        c = conn.cursor()
        c.execute("insert into user (name, timestamp) values (?,?)", (user_name, t))
        conn.commit()
        c.close()
        conn.close()
        flag = 0
    return render_template("main.html", name=user_name)


@app.route("/ethical_test", methods=["post", "get"])
def ethical_test():
    return render_template("ethical_test.html")


@app.route("/faq", methods=["post", "get"])
def faq():
    return render_template("faq.html")


@app.route("/faq1", methods=["POST", "GET"])
def faq1():
    q = request.form.get("answer")
    response = model.generate_content(q)
    print(response.candidates[0].content.parts[0])
    return render_template("faq1.html", r=response.candidates[0].content.parts[0])


@app.route("/user_log", methods=["POST", "GET"])
def userLog():
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute("select * from user")
    r = ""
    for row in c:
        r += str(row) + "\n"
    print(r)
    c.close()
    conn.close()
    return render_template("userLog.html", r=r)


@app.route("/del_log", methods=["POST", "GET"])
def deleteLog():
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close()
    return render_template("deleteLog.html")


@app.route("/test_result", methods=["post", "get"])
def test_result():
    answer = request.form.get("answer")
    if answer == "false":
        return render_template("pass.html")
    else:
        return render_template("fail.html")


@app.route("/foodexp", methods=["post"])
def foodexp():
    return render_template("foodexp.html")


@app.route("/foodexp_pred", methods=["post", "get"])
def foodexp_pred():
    q = request.form.get("q")
    return render_template("foodexp_pred.html", r=(0.48517842 * q + 147.47538852370565))


if __name__ == "__main__":
    app.run(debug=True)
