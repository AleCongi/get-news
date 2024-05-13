import datetime
import os
import re
import time
import quopri  # Per decodificare le codifiche 'quoted-printable'

from dotenv import load_dotenv
load_dotenv()

def elabora_dati_email(file_path):

    # Leggere il contenuto del file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Dividere il contenuto in blocchi separati per ogni email
    emails = re.split(r"From - \w+ \w+ \d{1,2} \d{2}:\d{2}:\d{2} \d{4}", content)

    # Lista per raccogliere le email parsate
    parsed_emails = []

    # Espressioni regolari per estrarre le informazioni necessarie
    from_pattern = re.compile(r"From: (.+?)\n")
    to_pattern = re.compile(r"To: (.+?)\n")
    subject_pattern = re.compile(r"Subject: (.+?)\n")
    date_pattern = re.compile(r"Date: (.+?)\n")
    body_pattern = re.compile(r"<body.*?>(.*?)</body>", re.DOTALL)

    for email in emails[1:]:  # il primo elemento è vuoto a causa dello split
        # Trovare le informazioni necessarie
        mittente = from_pattern.search(email)
        destinatario = to_pattern.search(email)
        subject = subject_pattern.search(email)
        date = date_pattern.search(email)
        body_match = body_pattern.search(email)
        body = body_match.group(1).strip() if body_match else ""

        # Creare un dizionario per ogni email e aggiungerlo alla lista
        if mittente and subject and date:
            email_data = {
                'Mittente': mittente.group(1),
                'Destinatario': destinatario.group(1) if destinatario else "",
                'Subject': subject.group(1),
                'Data di ricezione': date.group(1),
                'Body': body
            }
            parsed_emails.append(email_data)

    return parsed_emails

# Uso della funzione:
# emails = parse_emails('path_to_your_file.txt')
# print(emails)

def get_most_recent_email(emails):
    # Funzione per trovare l'email con la data più recente
    most_recent = None
    latest_date = None
    
    for email in emails:
        # Convertire la stringa di data in un oggetto datetime
        try:
            email_date = datetime.datetime.strptime(email['Data di ricezione'], "%a, %d %b %Y %H:%M:%S %z")
            if most_recent is None or email_date > latest_date:
                most_recent = email
                latest_date = email_date
        except ValueError:
            continue  # Saltare email se la data non può essere parsata
    
    return most_recent

from bs4 import BeautifulSoup
import html


def clean_email_body(raw_html):
    # Decodifica da quoted-printable se necessario
    try:
        # Tentativo di decodificazione utf-8 standard
        decoded_html = quopri.decodestring(raw_html.encode()).decode('utf-8')
    except UnicodeDecodeError:
        # In caso di errore, ignorare i caratteri che causano problemi
        decoded_html = quopri.decodestring(raw_html.encode()).decode('utf-8', errors='ignore')
    
    # Sostituire le rotture di riga codificate e altri caratteri non necessari
    decoded_html = decoded_html.replace("=\n", "")
    
    # Decodifica ulteriori entità HTML
    decoded_html = html.unescape(decoded_html)
    
    # Utilizza BeautifulSoup per rimuovere i tag HTML e ottenere solo il testo
    soup = BeautifulSoup(decoded_html, 'html.parser')
    text = soup.get_text(separator="\n")  # Usa una nuova linea come separatore per i blocchi di testo
    
    return text

#chiama path dal dot env
path = os.getenv("PATH_TO_INBOX")
# Parse delle email
prev_mre = None
while True:

    emails = elabora_dati_email(path)

    # Ottenere l'email più recente
    most_recent_email = get_most_recent_email(emails)

    if prev_mre is None or most_recent_email != prev_mre:
        # Pulire il corpo dell'email
        cleaned_body = clean_email_body(most_recent_email['Body'])
        print("Mittente:", most_recent_email['Mittente'])
        print("Subject:", most_recent_email['Subject'])
        print("Data:", most_recent_email['Data di ricezione'])
        print("Body:")
        print(cleaned_body)

    prev_mre = most_recent_email
    #sleep 10 minuti
    time.sleep(60)
