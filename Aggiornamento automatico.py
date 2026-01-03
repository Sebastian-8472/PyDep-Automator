import subprocess
import sys
import json
import datetime
import os

import subprocess
import sys
import json
import datetime
import os
import logging

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("updater_debug.log"),  # Salva su file
        logging.StreamHandler(sys.stdout)  # Mostra a video
    ]
)
logger = logging.getLogger(__name__)


class PyUpdater:
    """
    Gestore avanzato per la manutenzione dei pacchetti Python con sistema di logging.
    """

    def __init__(self):
        self.python_exe = sys.executable
        self.last_backup = None
        logger.info(f"Inizializzato PyUpdater utilizzando: {self.python_exe}")

    def get_outdated_packages(self):
        """Recupera i pacchetti obsoleti."""
        logger.info("Ricerca pacchetti obsoleti in corso...")
        try:
            result = subprocess.run(
                [self.python_exe, "-m", "pip", "list", "--outdated", "--format=json"],
                capture_output=True, text=True, check=True
            )
            packages = json.loads(result.stdout)
            logger.info(f"Trovati {len(packages)} pacchetti obsoleti.")
            return packages
        except subprocess.CalledProcessError as e:
            logger.error(f"Errore critico durante il controllo pacchetti: {e.stderr}")
            raise

    def update_package(self, package_name, current_ver, latest_ver):
        """Aggiorna un singolo pacchetto e logga l'inizio e la fine."""
        logger.info(f"INIZIO AGGIORNAMENTO: {package_name} ({current_ver} -> {latest_ver})")

        try:
            # Eseguiamo l'aggiornamento
            process = subprocess.run(
                [self.python_exe, "-m", "pip", "install", "--upgrade", package_name],
                capture_output=True, text=True, check=True
            )
            # Logghiamo il successo
            logger.info(f"COMPLETATO: {package_name} è ora alla versione {latest_ver}.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"FALLITO: Impossibile aggiornare {package_name}. Errore: {e.stderr.strip()}")
            return False

    def create_backup(self, filename=None):
        """Crea uno snapshot dell'ambiente attuale."""
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backup_env_{timestamp}.txt"

        logger.info(f"Creazione backup di sicurezza in corso: {filename}")
        try:
            result = subprocess.run(
                [self.python_exe, "-m", "pip", "freeze"],
                capture_output=True, text=True, check=True
            )
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result.stdout)
            self.last_backup = filename
            logger.info("Backup creato con successo.")
            return filename
        except Exception as e:
            logger.error(f"Errore durante la creazione del backup: {e}")
            return None

    def update_all(self, auto_rollback=False):
        """Esegue il ciclo completo di aggiornamento con log dettagliato."""
        logger.info("=== Avvio procedura di manutenzione globale ===")

        # 1. Backup
        backup_file = self.create_backup()
        if not backup_file:
            logger.critical("Procedura interrotta: Backup fallito.")
            return

        # 2. Identificazione
        outdated = self.get_outdated_packages()
        if not outdated:
            logger.info("Tutti i moduli sono aggiornati. Nulla da fare.")
            return

        # 3. Ciclo di aggiornamento
        successi = 0
        fallimenti = 0

        for pkg in outdated:
            name = pkg['name']
            c_ver = pkg['version']
            l_ver = pkg['latest_version']

            if self.update_package(name, c_ver, l_ver):
                successi += 1
            else:
                fallimenti += 1

        # 4. Report finale
        logger.info("=== RIEPILOGO OPERAZIONI ===")
        logger.info(f"Totale pacchetti processati: {len(outdated)}")
        logger.info(f"Aggiornamenti riusciti: {successi}")
        logger.info(f"Aggiornamenti falliti: {fallimenti}")

        if fallimenti > 0:
            if auto_rollback:
                logger.warning("Rilevati fallimenti. Avvio rollback automatico...")
                self.rollback(backup_file)
            else:
                logger.warning(f"Attenzione: {fallimenti} pacchetti non sono stati aggiornati. Controlla il log.")

        logger.info("=== Fine procedura ===")

    def install_from_requirements(self, filename="requirements_updated.txt"):
        """
        Installa i pacchetti elencati in un file requirements per ricreare un ambiente.

        Questo metodo è l'opposto di generate_requirements. Legge il file specificato
        ed esegue l'installazione di massa di tutte le dipendenze e versioni elencate.

        Args:
            filename (str): Il percorso del file .txt da cui leggere i pacchetti.
                            Default: 'requirements_updated.txt'.

        Returns:
            bool: True se l'installazione è stata completata con successo, False altrimenti.

        Raises:
            FileNotFoundError: Se il file specificato non esiste.
        """
        if not os.path.exists(filename):
            print(f"Errore: Il file '{filename}' non esiste.")
            return False

        logger.info(f"Inizio installazione dei pacchetti da '{filename}'...")
        try:
            # -r indica a pip di leggere da un file di requisiti
            subprocess.run(
                [self.python_exe, "-m", "pip", "install", "-r", filename],
                check=True
            )
            logger.info(f"Ambiente ripristinato con successo dal file '{filename}'.")
            return True
        except subprocess.CalledProcessError as e:
            logger.info(f"Errore durante l'installazione di massa: {e}")
            return False

    def update_all(self, export_requirements=True):
        """
        Esegue l'aggiornamento automatico di tutti i pacchetti obsoleti.
        """
        outdated = self.get_outdated_packages()
        if not outdated:
            logger.info("Tutti i pacchetti sono già aggiornati.")
            return

        for pkg in outdated:
            self.update_package(pkg['name'])

        if export_requirements:
            self.generate_requirements()


# --- Esempio di utilizzo ---
if __name__ == "__main__":
    updater = PyUpdater()

    # Esempio A: Aggiorna tutto e salva
    # updater.update_all()

    # Esempio B: Ripristina l'ambiente da un file esistente
    # updater.install_from_requirements("requirements_updated.txt")