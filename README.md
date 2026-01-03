# Python-Env-Manager
# Python Environment Auto-Updater &amp; Manager  Uno strumento professionale in Python per automatizzare la manutenzione dei pacchetti installati, garantendo stabilità tramite backup preventivi e sistemi di rollback.
Python-Env-Manager/
├── .gitignore              # Esclude file inutili (es. __pycache__, .venv)
├── LICENSE                 # Licenza (es. MIT)
├── README.md               # Il "cuore" della presentazione
├── requirements.txt        # Dipendenze per far girare lo script (se ne hai)
└── py_updater.py           # La classe che abbiamo scritto

## 🚀 Funzionalità
* **Aggiornamento Intelligente**: Identifica i pacchetti obsoleti e li aggiorna all'ultima versione stabile.
* **Sicurezza (Rollback)**: Crea un backup automatico dell'ambiente prima di ogni operazione.
* **Logging Professionale**: Tracciamento in tempo reale delle operazioni e report finale.
* **Ripristino**: Metodo dedicato per ricreare l'ambiente da un file `requirements.txt`.

## 🛠️ Tecnologie Utilizzate
* **Python 3.x**
* **Subprocess API**: Per l'interazione sicura con il sistema operativo.
* **Logging & JSON**: Per la gestione dei dati e del debugging.

## 📖 Utilizzo Rapido
```python
from py_updater import PyUpdater

updater = PyUpdater()
updater.update_all(auto_rollback=True)
