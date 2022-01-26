from flask import render_template, request, redirect, url_for, flash
from models import app, Resources, db
from werkzeug.utils import secure_filename
import os
from pygdrive3 import service
from sendMail import send_mail
from config import Config
import bleach
from cli import create_db


app.config.from_object(Config)
app.cli.add_command(create_db)
db.init_app(app)


# Drive
drive_service = service.DriveService('client_secret.json')
drive_service.auth()


@app.route('/')
def home():
    category_dict = {
        'Class-10-Hindi': 'Class 10 - Hindi',
        'Class-10-English': 'Class 10 - English',
        'Class-10-Maths': 'Class 10 - Maths',
        'Class-10-Science': 'Class 10 - Science',
        'Class-10-Computer': 'Class 10 - Computer',
        'Class-10-Social-Science': 'Class 10 - Social Science',
        'Class-11-Physics': 'Class 11 - Physics',
        'Class-11-Chemistry': 'Class 11 - Chemistry',
        'Class-11-Maths': 'Class 11 - Maths',
        'Class-11-Biology': 'Class 11 - Biology',
        'Class-11-English': 'Class 11 - English',
        'Class-12-Physics': 'Class 12 - Physics',
        'Class-12-Chemistry': 'Class 12 - Chemistry',
        'Class-12-Maths': 'Class 12 - Maths',
        'Class-12-Biology': 'Class 12 - Biology',
        'Class-12-English': 'Class 12 - English',
    }
    category = request.args.get('c')
    if not category:
        resources = Resources.query.all()
    else:
        resources = Resources.query.filter_by(category=category_dict[category]).all()
    
    return render_template('home.html', resources=resources)


@app.route('/add', methods=["GET", "POST"])
def add_resource():
    allowed_tags =  [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'h1', 'br', 'h2', 'h3', 
        'h4', 'h5', 'h6', 'u', 'font', 'span', 'p']
    resource = Resources()
    if request.method == "POST":
        file = request.files['material']
        resource.name = request.form["name"]
        resource.title = request.form["title"]
        resource.url = request.form["url"]
        resource.description = bleach.clean(request.form["description"], tags=allowed_tags)
        resource.category = request.form["type"]
        if file:
            resource.filename = file.filename
            filename = secure_filename(file.filename)
            static = os.path.join(os.path.curdir, "static")
            files = os.path.join(static, "files")
            location = os.path.join(files, filename)
            file.save(location)
            folder = drive_service.list_folders_by_name('ShareArc')
            file = drive_service.upload_file(file.filename, location, folder[0]['id'])
            resource.link = drive_service.anyone_permission(file)
            os.remove(location)
        db.session.add(resource)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('add_resource.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form['txtName']
        email = request.form['txtEmail']
        phone = request.form['txtPhone']
        msg = request.form['txtMsg']
        send_mail(name, email, phone, msg)
        flash("Thank you for your feedback.")
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about_us.html')


if __name__ == '__main__':
    app.run(debug=True)
