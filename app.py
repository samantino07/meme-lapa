import os
import csv 
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from config import Config
from models import db, Meme
from forms import UploadForm
from generate_graphs import generate_pie_chart
from datetime import datetime  
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.meme.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

         
            meme = Meme(filename=filename, upload_date=datetime.now())  
            db.session.add(meme)
            db.session.commit()
            flash("Meme veiksmīgi augšupielādēts!", "success")
            return redirect(url_for('memes'))
        else:
            flash("Nav atļauts faila formāts!", "danger")
    return render_template('index.html', form=form)

# ✅ Meme galerija
@app.route('/memes')
def memes():
    memes = Meme.query.order_by(Meme.upload_date.desc()).all()  # ✅ Sakārto pēc datuma
    return render_template('memes.html', memes=memes)

@app.route('/like/<int:meme_id>', methods=['POST'])
def like_meme(meme_id):
    meme = Meme.query.get_or_404(meme_id)
    meme.likes += 1
    db.session.commit()
    return {"likes": meme.likes}

# ✅ Statistikas grafiks
@app.route('/stats')
def stats():
    memes = Meme.query.all()
    data = pd.DataFrame([(m.id, m.upload_date, m.likes) for m in memes], columns=['ID', 'Upload Date', 'Likes'])

    if not data.empty:
        plt.figure(figsize=(6, 4))
        plt.hist(pd.to_datetime(data['Upload Date']), bins=5, color='blue', alpha=0.7)
        plt.xlabel('Datums')
        plt.ylabel('Meme augšupielāžu skaits')
        plt.title('Meme augšupielādes')
        plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'meme_histogram.png'))

    return render_template('stats.html', img='static/uploads/meme_histogram.png')

# ✅ Apļveida diagramma
@app.route('/chart')
def chart():
    img_path = generate_pie_chart()
    return render_template('chart.html', img=img_path)

# ✅ CSV augšupielāde
@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nav izvēlēts fails', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Nav izvēlēts fails', 'danger')
            return redirect(request.url)

        if file and file.filename.endswith('.csv'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    with app.app_context():
                        for row in reader:
                            existing_meme = Meme.query.filter_by(filename=row['Filename']).first()
                            if not existing_meme:
                                meme = Meme(
                                    filename=row['Filename'],
                                    upload_date=datetime.strptime(row['Upload Date'], '%Y-%m-%d %H:%M:%S'),
                                    likes=int(row['Likes'])
                                )
                                db.session.add(meme)
                        db.session.commit()

                flash('CSV dati veiksmīgi ielādēti!', 'success')
                return redirect(url_for('memes'))
            except Exception as e:
                flash(f'Kļūda CSV ielādē: {e}', 'danger')

    return render_template('upload_csv.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=True)
    from flask import jsonify  # ✅ Lai atgrieztu JSON atbildi




