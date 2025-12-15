# 📧 Configurazione Email - Istruzioni

## Passo 1: Crea il file .env

Nella cartella `Sito/` crea un file chiamato `.env` con **una variabile per riga**:

```
MAIL_USER=a.lucchesi1999@gmail.com
MAIL_PASS=INSERISCI_APP_PASSWORD_QUI
MAIL_TO=a.lucchesi1999@gmail.com
FLASK_SECRET_KEY=chiave-segreta-cambiami-in-produzione
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
```

**IMPORTANTE**: Ogni variabile deve essere su una riga separata!

## Passo 2: Ottieni l'App Password di Gmail

1. Vai su: https://myaccount.google.com/apppasswords
   (Se non vedi questa opzione, devi prima attivare la "Verifica in due passaggi")

2. Seleziona:
   - App: "Mail"
   - Dispositivo: "Altro (nome personalizzato)" → scrivi "Sito Web"

3. Clicca "Genera"

4. Ti verrà mostrata una password di 16 caratteri (tipo: `abcd efgh ijkl mnop`)

5. **Copia la password SENZA SPAZI** e incollala nel file `.env` al posto di `INSERISCI_APP_PASSWORD_QUI`

   Esempio: se Google ti dà `abcd efgh ijkl mnop`, nel .env metti `abcd efgh ijkl mnop` (senza spazi)

## Passo 3: Installa python-dotenv

Nel Terminale:

```bash
cd ~/Desktop/Sito
source venv/bin/activate
python -m pip install python-dotenv
```

## Passo 4: Riavvia il server

Se il server è acceso: premi **CTRL + C** per fermarlo.

Poi:

```bash
cd ~/Desktop/Sito
source venv/bin/activate
python app.py
```

## ✅ Test invio

1. Apri: `http://127.0.0.1:5000/contatti`
2. Compila il form con nome, email e messaggio
3. Invia il messaggio
4. Controlla la tua email `a.lucchesi1999@gmail.com` - dovresti ricevere il messaggio!

---

## 🔍 Debug

Se l'invio fallisce:
- All'utente viene mostrato un messaggio generico
- Nel Terminale vedrai i dettagli dell'errore per capire cosa non va

---

**Nota importante**: Il file `.env` contiene password sensibili. NON committarlo mai su Git (è già nel `.gitignore`).
