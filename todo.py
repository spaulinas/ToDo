from flask import Flask, g
from flask import render_template
import os
import sqlite3

app.config.update(dict(
    SECRET_KEY='bardzosekretnawartosc',
    DATABASE=os.path.join(app.root_path, 'db.sqlite'),
    SITE_NAME='Moje zadania'
))

def get_db():
    """Funkcja tworząca połączenie z bazą danych"""
    if not g.get('db'):  # jeżeli brak połączenia, to je tworzymy
        con = sqlite3.connect(app.config['DATABASE'])
        con.row_factory = sqlite3.Row
        g.db = con  # zapisujemy połączenie w kontekście aplikacji
    return g.db  # zwracamy połączenie z bazą


@app.teardown_appcontext
def close_db(error):
    """Zamykanie połączenia z bazą"""
    if g.get('db'):
        g.db.close()
        
 @app.route('/zadania')
def zadania():
    db = get_db()
    kursor = db.execute('SELECT * FROM zadania ORDER BY data_pub DESC;')
    zadania = kursor.fetchall()
    return render_template('zadania_lista.html', zadania=zadania)
    
 @app.route('/zadania', methods=['GET', 'POST'])
def zadania():
    error = None
    if request.method == 'POST':
        zadanie = request.form['zadanie'].strip()
        if len(zadanie) > 0:
            zrobione = '0'
            data_pub = datetime.now()
            db = get_db()
            db.execute('INSERT INTO zadania VALUES (?, ?, ?, ?);',
                       [None, zadanie, zrobione, data_pub])
            db.commit()
            flash('Dodano nowe zadanie.')
            return redirect(url_for('zadania'))

        error = 'Nie możesz dodać pustego zadania!'  # komunikat o błędzie

    db = get_db()
    kursor = db.execute('SELECT * FROM zadania ORDER BY data_pub DESC;')
    zadania = kursor.fetchall()
    return render_template('zadania_lista.html', zadania=zadania, error=error)
