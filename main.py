from flask import Flask, render_template, request
import requests
import os
import smtplib

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)
MY_EMAIL = os.environ.get("MYEMAIL")
MY_PASSWORD = os.environ.get("PASSWORD")


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    contact_me = True
    if request.method == "POST":
        contact_me = False
        name = request.form['name']
        user_email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        print(f"{name}\n{user_email}\n{phone}\n{message}")
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                                msg=f"Subject: New contact request(Blog) - {name}\n\nName : {name}\nEmail : {user_email}\nPhone : {phone}\nMessage : {message}")

    return render_template('contact.html', contact_me=contact_me)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
