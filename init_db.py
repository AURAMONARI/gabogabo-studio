import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS recensioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        servizio TEXT NOT NULL,
        voto INTEGER NOT NULL,
        commento TEXT NOT NULL,
        data TEXT NOT NULL
    )
''')

# Inserimento di 10 record iniziali come richiesto
recensioni_iniziali = [
    ('Marco', 'Personal Training', 5, 'Allenamenti distruttivi ma efficaci!', '2026-05-01'),
    ('Giulia', 'Nutrizione', 4, 'Dieta facile da seguire, ottimi risultati.', '2026-05-02'),
    ('Luca', 'Fisioterapia', 5, 'Spalla guarita in 3 sedute, magici.', '2026-05-05'),
    ('Anna', 'Personal Training', 5, 'Il miglior studio in città.', '2026-05-10'),
    ('Matteo', 'Fisioterapia', 4, 'Molto professionali e attenti.', '2026-05-12'),
    ('Sara', 'Nutrizione', 5, 'Mai sentita così in forma.', '2026-05-15'),
    ('Paolo', 'Personal Training', 3, 'Bravi ma parcheggio scomodo.', '2026-05-18'),
    ('Elena', 'Nutrizione', 5, 'Il piano alimentare ha cambiato la mia vita.', '2026-05-20'),
    ('Giacomo', 'Fisioterapia', 5, 'Addio mal di schiena!', '2026-05-22'),
    ('Chiara', 'Personal Training', 4, 'GaboGabo è una garanzia.', '2026-05-25')
]

cursor.executemany('''
    INSERT INTO recensioni (nome, servizio, voto, commento, data)
    VALUES (?, ?, ?, ?, ?)
''', recensioni_iniziali)

connection.commit()
connection.close()
print("Database creato e popolato con successo!")