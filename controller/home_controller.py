from flask import current_app,render_template,request, redirect


def home_index():
    return render_template("/home/index.html")