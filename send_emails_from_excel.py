import pandas as pd
# import smtplib
# from email.mime.text import MIMEText

# Configurazione del server email
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USERNAME = 'your_email@gmail.com'  # Sostituisci con la tua email
PASSWORD = 'your_password'         # Sostituisci con la tua password

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
    "Dato che la vostra scuola si è distinta con questi risultati d'eccellenza in informatica, "
    "Vorremmo offrire ai vostri alunni una mentorship gratuita. "
    "I nostri mentor vantano affiliazioni con istituzioni di alto livello come Cambridge, MIT, Harvard, Normale di Pisa, "
    "Apple, Google e tante altre. I vostri alunni potranno candidarsi alla mentorship attraverso il seguente link: "
    "https://leadthefuture.tech/mentorship"
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

# Stampa il contenuto delle email
print(grouped['Email_Content'])

# Scrivi il contenuto delle email in un file di testo
output_file_path = './emails_final.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    for _, row in grouped.iterrows():
        file.write(f"To: {row['Email']}\n")
        file.write(f"Content:\n{row['Email_Content']}\n")
        file.write("\n" + "-"*50 + "\n\n")

print(f"Email contents written to {output_file_path}")

'''
# Funzione per inviare email
def send_email(email, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = 'Congratulazioni per gli alunni ammessi'
    msg['From'] = USERNAME
    msg['To'] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, email, msg.as_string())
        print(f"Email inviata a {email}")
    except Exception as e:
        print(f"Errore nell'invio a {email}: {e}")

# Invia le email
for _, row in grouped.iterrows():
    send_email(row['Email'], row['Email_Content'])
'''
