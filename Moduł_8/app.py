from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

@app.route("/")
def get_parent():
    return render_template('parent.html')

@app.route("/about")
def get_about():
    return render_template('about.html')

@app.route("/contact", methods=["GET", "POST"])
def get_contact():
    if request.method == 'POST':
        # DEBUGOWANIE
        # print('content-type:', request.content_type)
        # print('raw body=', request.get_data().decode('utf-8', errors='replace'))
        # print('form:', request.form)
        # print('form keys=', list(request.form.keys()))
        # KONIEC DEBUGOWANIA
        message = request.form.get('message')
        print('message =', message)
        return redirect(url_for('get_contact'))  # refresh the page with request.method="GET"
    return render_template('contact.html')