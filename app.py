from flask import Flask, request, render_template
import datetime
import sqlite3
import google.generativeai as genai
import os
import markdown
import re
import wikipedia

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
    return render_template("main.html", name=user_name if user_name else "")


@app.route("/ethical_test", methods=["post", "get"])
def ethical_test():
    return render_template("ethical_test.html")


@app.route("/faq", methods=["post", "get"])
def faq():
    return render_template("faq.html")


@app.route("/faq1", methods=["POST", "GET"])
def faq1():
    q = request.form.get("q")
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


@app.route("/foodexp2", methods=["POST", "GET"])
def foodexp2():
    return render_template("foodexp2.html")


@app.route("/FAQ2", methods=["POST", "GET"])
def faq2():
    ques = request.form.get("response")
    answer = model.generate_content("Risk Assessment")
    answer = markdown.markdown(answer.text)
    answer = re.sub(r"<.*?>", "", answer)
    return render_template("FAQ2.html", answer=answer)


@app.route("/FAQ3", methods=["POST", "GET"])
def faq3():
    # ques = request.form.get("response")
    answer = model.generate_content("Economic Indicators")
    answer = markdown.markdown(answer.text)
    answer = re.sub(r"<.*?>", "", answer)
    return render_template("FAQ3.html", answer=answer)


@app.route("/FAQ1input", methods=["POST", "GET"])
def faq1_wiki():
    ques = request.form.get("ques")
    r = wikipedia.summary(ques)
    return render_template("FAQ1input.html", r=r)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
