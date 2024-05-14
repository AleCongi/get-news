# Guida all'Installazione e Uso

Questa guida fornisce istruzioni dettagliate su come installare Python, preparare un ambiente virtuale, installare le dipendenze e eseguire codice Python.

## Prerequisiti

Assicurati di avere installato Git e Python sul tuo sistema. Le istruzioni seguenti sono state testate con Python 3.8 e superiori.

## Installazione di Python

Per installare Python, visita [python.org](https://python.org) e scarica l'ultima versione di Python per il tuo sistema operativo. Segui le istruzioni di installazione specifiche per il tuo sistema.

### Windows

Esegui l'installer scaricato e assicurati di selezionare l'opzione "Add Python to PATH" all'inizio dell'installazione.

### macOS e Linux

Python è spesso preinstallato su questi sistemi. Puoi verificare la versione installata con il comando:

```bash
python --version
```

Se necessario, installa Python usando brew su macOS:

```bash
brew install python
```
O apt su Ubuntu:
```bash
sudo apt update
sudo apt install python3
```
## Configurazione dell'Ambiente Virtuale
Per creare un ambiente virtuale, utilizza il modulo venv incluso in Python.

```bash
python -m venv nome_del_tuo_ambiente
```

### Attivazione dell'Ambiente Virtuale
Una volta creato l'ambiente virtuale, attivalo con il seguente comando:

#### Windows
```bash
.\nome_del_tuo_ambiente\Scripts\activate
```

#### macOS e Linux
```bash
source nome_del_tuo_ambiente/bin/activate
```
## Installazione delle Dipendenze

Con l'ambiente virtuale attivato, installa tutte le dipendenze necessarie utilizzando il file requirements.txt.

```bash
pip install -r requirements.txt
```

## Esecuzione del Codice Python
Per eseguire il tuo script Python:

```bash
python nome_del_file.py
```

## Disattivazione dell'Ambiente Virtuale
Per uscire dall'ambiente virtuale, usa il comando:

```bash
deactivate
```

# Dotenv
È necessario creare un file .env per impostare le variabili d'ambiente. Prendi spunto da [questo template](https://github.com/AleCongi/get-news/blob/main/.env-template) per creare il tuo dotenv

# Problemi Comuni
In caso di problemi con l'installazione o l'esecuzione, controlla le versioni di Python (o Python3) e pip (o pip3) e assicurati che l'ambiente virtuale sia attivato correttamente.