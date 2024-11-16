import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Configurazione del server email per Brevo

# CAMBIATE CON LTF EMAIL DATA
SMTP_SERVER = 'smtp-relay.brevo.com'
SMTP_PORT = 587
USERNAME = '8017e9001@smtp-brevo.com'  # Sostituisci con la tua email di login su Brevo
PASSWORD = 'UcNFEtYBrGMsOdy5'          # Sostituisci con la tua API key SMTP di Brevo

# Carica il file CSV
file_path = './Ammessi_Selezione_Territoriale_2024.csv'  # Assicurati che il file sia nella stessa directory
df = pd.read_csv(file_path)

# Prepara i dati email
df['Email'] = df['Codice\nmeccanografico\nscuola'].str.strip() + '@istruzione.it'
df['FullName'] = df['Nome'] + ' ' + df['Cognome']

# Raggruppa per email e crea liste di nomi completi
grouped = df.groupby('Email').agg({
    'FullName': lambda x: list(x),
    'Nome scuola': 'first'
}).reset_index()

# Messaggio di mentorship
mentorship_message = (
    "Siamo Lead the Future (leadthefuture.tech), "
    "un'associazione del terzo settore che offre orientamento universitario, assistenza con le ammissioni a università "
    "di prestigio, opportunità di ricerca accademica alle superiori e in triennale, e crescita professionale. "
    "\n\n"
    "Dato che la vostra scuola si è distinta con questi risultati d'eccellenza in informatica, "
    "vorremmo offrire ai vostri alunni una mentorship gratuita. "
    "\n\nI nostri mentor vantano affiliazioni con istituzioni di alto livello come Cambridge, MIT, Harvard, Normale di Pisa, "
    "Apple, Google e tante altre. I vostri alunni potranno candidarsi alla mentorship attraverso il seguente link: "
    "https://www.leadthefuture.tech/inizia-candidatura/"
    "\n\nCordiali saluti, Lead the Future"
)

# Funzione per formattare la lista dei nomi
def format_name_list(names):
    names = [name.strip() for name in names]
    if len(names) == 1:
        return names[0]
    else:
        return ', '.join(names[:-1]) + ' e ' + names[-1]

# Crea il contenuto delle email
grouped['Email_Content'] = grouped.apply(
    lambda row: (
        f"Congratulazioni alla scuola {row['Nome scuola']} per avere un alunno/a {format_name_list(row['FullName'])} "
        "che ha passato le selezioni di informatica."
        if len(row['FullName']) == 1 else
        f"Congratulazioni alla scuola {row['Nome scuola']} per gli alunni {format_name_list(row['FullName'])} "
        "che hanno passato le selezioni di informatica."
    ) + f"\n\n{mentorship_message}",
    axis=1
)

# Funzione per inviare email
def send_email(email, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = 'Esiti olimpiadi di informatica e informativa mentorship Lead the Future'
    msg['From'] = VOSTRAEMAIL  # Assicurati che sia un indirizzo verificato su Brevo
    msg['To'] = email # email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.sendmail(msg['From'], email, msg.as_string())
        print(f"Email inviata a {email}")
    except Exception as e:
        print(f"Errore nell'invio a {email}: {e}")

# Invia le email
for _, row in grouped.iterrows():
    send_email(row['Email'], row['Email_Content'])
