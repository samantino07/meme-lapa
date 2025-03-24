import pandas as pd
import matplotlib.pyplot as plt
import os
from models import db, Meme


def export_csv():
    """Eksportē datus no datubāzes uz CSV failu."""
 

    with app.app_context(): 
        memes = Meme.query.all()
        data = [(m.id, m.filename, m.upload_date, m.likes) for m in memes]
        df = pd.DataFrame(data, columns=['ID', 'Filename', 'Upload Date', 'Likes'])
        df.to_csv('meme_data.csv', index=False)

def generate_pie_chart():
    """Ģenerē sektoru diagrammu par meme kategorijām."""
    categories = ["Politiskās", "Video spēles", "Dzīvnieki", "Filmu/TV", "Citi"]
    counts = [25, 40, 15, 30, 20]

    os.makedirs("static/uploads", exist_ok=True)

    plt.figure(figsize=(7, 7))
    plt.pie(counts, labels=categories, autopct='%1.1f%%', colors=['blue', 'green', 'red', 'purple', 'orange'])
    plt.title("Meme kategoriju sadalījums")

    img_path = "static/uploads/meme_pie_chart.png"
    plt.savefig(img_path)
    plt.close()
    return img_path

if __name__ == '__main__':
    export_csv()
    print("Dati saglabāti: meme_data.csv")

    img_path = generate_pie_chart()
    print(f"Diagramma saglabāta: {img_path}")

import csv
from models import db, Meme


def import_csv():
    """Ielādē datus no CSV un saglabā datubāzē."""
    with app.app_context():  # Nodrošina, ka darbojamies Flask kontekstā
        with open('meme_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Pārbauda, vai ieraksts jau eksistē
                existing_meme = Meme.query.filter_by(filename=row['Filename']).first()
                if not existing_meme:
                    meme = Meme(
                        filename=row['Filename'],
                        upload_date=row['Upload Date'],
                        likes=int(row['Likes'])
                    )
                    db.session.add(meme)
            db.session.commit()
        print("CSV dati veiksmīgi ielādēti datubāzē!")

if __name__ == '__main__':
    import_csv()
