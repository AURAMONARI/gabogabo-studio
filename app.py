import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# 1. INIZIALIZZAZIONE APPLICAZIONE FLASK
app = Flask(__name__)

# 2. CONFIGURAZIONE CARTELLA PER IL CARICAMENTO DELLE FOTO
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crea automaticamente la cartella "uploads" dentro "static" se non esiste sul PC
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 3. CONFIGURAZIONE SICUREZZA
ADMIN_PASSWORD = "hihihiha"  # La tua password per eliminare le recensioni
DATABASE = "database.db"     # Il file del database SQL che verrà creato automaticamente

# ==========================================
# FUNZIONI DI GESTIONE DATABASE SQLITE
# ==========================================

def init_db():
    """Crea il database e la tabella recensioni se non esistono ancora, inserendo la prima recensione di prova."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Creazione della tabella SQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recensioni (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                servizio TEXT NOT NULL,
                voto TEXT NOT NULL,
                commento TEXT NOT NULL,
                foto TEXT
            )
        ''')
        
        # Controlla se la tabella è vuota. Se sì, inserisce la recensione di default di Marco Rossi
        cursor.execute("SELECT COUNT(*) FROM recensioni")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO recensioni (nome, servizio, voto, commento, foto)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                "Marco Rossi", 
                "Personal Trainer Team", 
                "5", 
                "Struttura pazzesca e staff super preparato. Gabo mi sta seguendo passo dopo passo e i risultati si vedono già dopo poche settimane!", 
                None
            ))
        conn.commit()

# Esegue l'inizializzazione del database all'avvio dell'app
init_db()


# ==========================================
# ROTTE DEL SITO
# ==========================================

# PAGINA HOME
@app.route('/')
def index():
    return render_template('index.html')


# PAGINA COLLABORATORI (DIVISA IN 3 REPARTI CON HOVER)
@app.route('/collaboratori')
def collaboratori():
    return render_template('collaboratori.html')


# PAGINA RECENSIONI (INVIO, FOTO DA GALLERIA/FOTOCAMERA E POPUP)
@app.route('/recensioni', methods=['GET', 'POST'])
def recensioni():
    if request.method == 'POST':
        nome = request.form.get('nome')
        servizio = request.form.get('servizio')
        voto = request.form.get('voto')
        commento = request.form.get('commento')
        
        # Gestione del file immagine caricato o scattato
        foto_nome = None
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                # Salva fisicamente il file dentro static/uploads/
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                foto_nome = filename

        # SALVATAGGIO IN DATABASE TRAMITE QUERY SQL INSERT INTO
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recensioni (nome, servizio, voto, commento, foto)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, servizio, voto, commento, foto_nome))
            conn.commit()
        
        return redirect(url_for('recensioni'))
    
    # SE LA RICHIESTA È GET: Recupera tutte le recensioni dal database con una SELECT
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row  # Permette di accedere ai dati usando i nomi delle colonne
        cursor = conn.cursor()
        # Ordina per ID decrescente per mostrare le nuove recensioni in alto
        cursor.execute("SELECT * FROM recensioni ORDER BY id DESC")
        righe = cursor.fetchall()
        
        # Converte i risultati in una lista di dizionari per la massima compatibilità con il tuo HTML
        recensioni_salvate = [dict(riga) for riga in righe]
    
    return render_template('recensioni.html', recensioni=recensioni_salvate)


# ROTTA DI CANCELLAZIONE PROTETTA DA PASSWORD
@app.route('/delete_recensione/<int:id>', methods=['POST'])
def delete_recensione(id):
    password_inserita = request.form.get('admin_password')
    
    # Controlla se la password inserita nel popup JavaScript coincide con quella admin
    if password_inserita == ADMIN_PASSWORD:
        # CANCELLAZIONE DAL DATABASE TRAMITE QUERY SQL DELETE FROM
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recensioni WHERE id = ?", (id,))
            conn.commit()
        print(f"[ADMIN] Recensione ID {id} eliminata dal database SQL.")
    else:
        print("[AVVISO] Tentativo di eliminazione fallito: Password Errata!")
        
    return redirect(url_for('recensioni'))


# AVVIO DEL SERVER LOCALE
if __name__ == '__main__':
    app.run(debug=True)