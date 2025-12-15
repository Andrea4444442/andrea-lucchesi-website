import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

# Verifica che le variabili d'ambiente siano caricate (solo per debug)
if os.environ.get("MAIL_USER"):
    print("[DEBUG] File .env caricato correttamente")
    print(f"[DEBUG] MAIL_USER: {os.environ.get('MAIL_USER')}")
    print(f"[DEBUG] MAIL_HOST: {os.environ.get('MAIL_HOST', 'smtp.gmail.com')}")
else:
    print("[WARNING] File .env non trovato o MAIL_USER non configurato!")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "chiave-segreta-cambiami-in-produzione")

@app.after_request
def add_ngrok_header(response):
    # Evita blocchi/preview ngrok (403 / warning)
    response.headers["ngrok-skip-browser-warning"] = "1"
    return response

@app.route("/")
def home():
    return render_template("index.html", title="Home")


@app.route("/chi-sono")
def chi_sono():
    return render_template("chi-sono.html", title="Chi sono")


@app.route("/competenze")
def competenze():
    return render_template("competenze.html", title="Competenze & CV")


@app.route("/contatti", methods=["GET", "POST"])
def contatti():
    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        email = (request.form.get("email") or "").strip()
        messaggio = (request.form.get("messaggio") or "").strip()

        # Validazione minima
        if not nome or not email or not messaggio:
            flash("Compila tutti i campi, per favore.", "error")
            return redirect(url_for("contatti"))

        if "@" not in email or "." not in email:
            flash("Inserisci un'email valida.", "error")
            return redirect(url_for("contatti"))

        # Invio email (notifica a te + conferma al visitatore)
        try:
            print(f"[DEBUG] Tentativo invio email per: {nome} ({email})")
            send_contact_emails(nome, email, messaggio)
            print(f"[SUCCESS] Email inviate con successo!")
            flash(
                f"Grazie {nome}! Messaggio inviato. Riceverai anche una mail di conferma.",
                "success",
            )
        except KeyError as e:
            # Variabile d'ambiente mancante
            error_msg = f"Configurazione mancante: {e}. Controlla il file .env"
            print(f"[ERRORE CONFIG] {error_msg}")
            flash(
                "Errore di configurazione. Controlla il file .env e riavvia il server.",
                "error",
            )
        except Exception as e:
            # Messaggio generico all'utente, dettagli nel terminale per debug
            flash(
                "Errore nell'invio del messaggio. Riprova più tardi o contattami direttamente.",
                "error",
            )
            print(f"[ERRORE EMAIL] {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

        return redirect(url_for("contatti"))

    return render_template("contatti.html", title="Contatti")


def _smtp_send(msg: EmailMessage) -> None:
    host = os.environ.get("MAIL_HOST", "smtp.gmail.com")
    port = int(os.environ.get("MAIL_PORT", "587"))
    user = os.environ["MAIL_USER"]
    password = os.environ["MAIL_PASS"]
    
    print(f"[DEBUG SMTP] Connessione a {host}:{port} con utente {user}")
    
    try:
        with smtplib.SMTP(host, port) as server:
            print("[DEBUG SMTP] Connessione stabilita")
            server.ehlo()
            print("[DEBUG SMTP] STARTTLS...")
            server.starttls()
            server.ehlo()
            print("[DEBUG SMTP] Login...")
            server.login(user, password)
            print("[DEBUG SMTP] Invio messaggio...")
            server.send_message(msg)
            print("[DEBUG SMTP] Messaggio inviato con successo!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"[ERRORE SMTP] Autenticazione fallita. Verifica MAIL_USER e MAIL_PASS nel .env")
        print(f"[ERRORE SMTP] Dettaglio: {e}")
        raise
    except Exception as e:
        print(f"[ERRORE SMTP] Errore durante l'invio: {e}")
        raise


def send_contact_emails(nome: str, email: str, messaggio: str) -> None:
    user = os.environ["MAIL_USER"]
    to_addr = os.environ.get("MAIL_TO", user)
    
    print(f"[DEBUG] Preparazione email: da {user} a {to_addr} e conferma a {email}")

    # 1) Email a te (notifica)
    print("[DEBUG] Creazione email notifica...")
    msg_owner = EmailMessage()
    msg_owner["Subject"] = f"[Sito] Nuovo messaggio da {nome}"
    msg_owner["From"] = f"Website Contact <{user}>"
    msg_owner["To"] = to_addr
    msg_owner["Reply-To"] = email  # così "Rispondi" va al visitatore
    msg_owner.set_content(
        "Hai ricevuto un nuovo messaggio dal form contatti.\n\n"
        f"Nome: {nome}\n"
        f"Email: {email}\n\n"
        "Messaggio:\n"
        f"{messaggio}\n"
    )
    _smtp_send(msg_owner)
    print("[DEBUG] Email notifica inviata!")

    # 2) Email al visitatore (conferma)
    print("[DEBUG] Creazione email conferma...")
    msg_user = EmailMessage()
    msg_user["Subject"] = "Conferma ricezione messaggio – Andrea Lucchesi"
    msg_user["From"] = f"Andrea Lucchesi <{user}>"
    msg_user["To"] = email
    msg_user.set_content(
        f"Ciao {nome},\n\n"
        "grazie per avermi contattato. Ho ricevuto correttamente il tuo messaggio e ti risponderò appena possibile.\n\n"
        "—\n"
        "Andrea Lucchesi\n"
        "Email: a.lucchesi1999@gmail.com\n"
        "LinkedIn: https://www.linkedin.com/in/andrea-lucchesi-\n"
    )
    _smtp_send(msg_user)
    print("[DEBUG] Email conferma inviata!")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
