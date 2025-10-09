# 🚀 Copilot Web Demo

Una applicazione web Flask dimostrativa per esplorare le funzionalità di **GitHub Copilot** e l'integrazione con **Azure DevOps MCP (Model Context Protocol)**.

---

## 📋 Indice

- [Descrizione](#-descrizione)
- [Funzionalità](#-funzionalità)
- [Requisiti](#-requisiti)
- [Installazione](#-installazione)
- [Utilizzo](#-utilizzo)
- [Modalità GitHub Copilot](#-modalità-github-copilot)
- [Azure DevOps MCP](#-azure-devops-mcp)
- [Testing](#-testing)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Contribuire](#-contribuire)

---

## 📖 Descrizione

Questo progetto è un'applicazione web Flask progettata per dimostrare:

1. **Funzionalità di GitHub Copilot**: esempi pratici delle modalità Ask, Edit e Agent
2. **Integrazione Azure DevOps MCP**: comandi e esempi per interagire con Azure DevOps tramite Model Context Protocol
3. **Best practices**: gestione form, validazione input, logging, testing e styling moderno

L'applicazione permette agli utenti di:
- Inviare il proprio nome tramite un form web
- Visualizzare lo storico delle sottomissioni
- Esplorare esempi di comandi Azure DevOps MCP

---

## ✨ Funzionalità

### Applicazione Web
- ✅ **Form di sottomissione** con validazione input lato client e server
- ✅ **Storico sottomissioni** persistente in formato JSON
- ✅ **Logging** delle operazioni in file di log
- ✅ **UI moderna** con CSS personalizzato e animazioni
- ✅ **Gestione errori** con messaggi user-friendly
- ✅ **Cancellazione storico** con un click

### GitHub Copilot Demo
- 📚 **Esempi di prompt** per le tre modalità (Ask, Edit, Agent)
- 🎯 **Istruzioni per task** strutturati e pronti all'uso
- 💡 **Guide pratiche** per dimostrazioni efficaci

### Azure DevOps MCP
- 🔧 **Comandi testati** per Repository, Work Items, Build, Release e Wiki
- 📖 **Esempi pratici** con parametri reali
- 🌐 **Supporto multilingua** (Inglese e Italiano)

---

## 🛠 Requisiti

- **Python** 3.7 o superiore
- **pip** (gestore pacchetti Python)

### Dipendenze
Le dipendenze sono elencate in `requirements.txt`:
- `flask` - Framework web
- `pytest` - Testing framework

---

## 📦 Installazione

### 1. Clona il repository

```bash
git clone https://github.com/pta19059/Copilot_web_Demo.git
cd Copilot_web_Demo
```

### 2. Crea un ambiente virtuale (consigliato)

```bash
python -m venv venv
```

Attiva l'ambiente virtuale:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

---

## 🚀 Utilizzo

### Avvia l'applicazione

```bash
python app.py
```

L'applicazione sarà disponibile su: `http://127.0.0.1:5000`

### Pagine disponibili

- **Homepage (`/`)**: Form per inserire il proprio nome
- **Storico (`/history`)**: Visualizza tutte le sottomissioni salvate
- **Cancella storico (`/clear-history`)**: Rimuove tutte le sottomissioni (POST)

### Esempio d'uso

1. Apri il browser su `http://127.0.0.1:5000`
2. Inserisci il tuo nome nel form
3. Clicca "Submit"
4. Visualizza il messaggio di benvenuto
5. Naviga su `/history` per vedere lo storico delle sottomissioni

---

## 🤖 Modalità GitHub Copilot

Questa repository include esempi pratici per tutte le modalità di GitHub Copilot. Consulta i file:

### 📄 `copilot_prompts.md`
Contiene prompt pronti all'uso per:
- **Ask Mode**: domande sul codice
- **Edit Mode**: modifiche inline
- **Agent Mode**: task complessi e multi-file

### 📄 `agent_instructions.md`
Istruzioni strutturate per l'Agent Mode, inclusi:
- ✅ TASK 1: Gestione errori
- ✅ TASK 2: Logging sottomissioni
- ✅ TASK 3: Pagina storico
- ✅ TASK 4: Unit tests
- ✅ TASK 5: Miglioramento UI
- ✅ TASK 6: Dockerizzazione (opzionale)
- 🧪 Bonus: API REST

### Esempi di prompt

**Ask Mode:**
```
"Come funziona la gestione dei form in Flask?"
"Quali edge case mancano in questa funzione?"
```

**Edit Mode:**
```
"Aggiungi validazione: mostra errore se il nome è vuoto"
"Sanitizza l'input per prevenire XSS"
```

**Agent Mode:**
```
"Crea una nuova pagina che elenca tutti i nomi inviati"
"Aggiungi unit test per input vuoti e caratteri non validi"
"Dockerizza l'applicazione con Dockerfile e docker-compose"
```

---

## 🔧 Azure DevOps MCP

### Comandi disponibili

Questa repository include una raccolta completa di comandi MCP testati per Azure DevOps:

#### 📁 Repository Management
- Lista repository di un progetto
- Dettagli di un repository specifico
- Lista branch
- Dettagli di un branch

#### 🏷️ Work Items
- Recupera work item per ID
- Lista work item assegnati all'utente corrente
- Schema dei tipi di work item (Bug, Task, Epic)

#### 🔧 Build & Release
- Lista build definitions
- Lista release definitions

#### 📚 Wiki
- Lista wiki di un progetto

### File di riferimento

- `azure-devops-mcp-demo-commands.md`: Comandi testati (Inglese/Italiano)
- `wit_get_work_item_example.md`: Esempi dettagliati per Work Items

### Esempio di utilizzo MCP

```json
{
  "command": "mcp_ado_repo_list_repos_by_project",
  "parameters": {
    "project": "Test MCP Server ADO",
    "top": 10
  }
}
```

---

## 🧪 Testing

L'applicazione include una suite di test completa.

### Esegui i test

```bash
pytest test_app.py -v
```

### Test inclusi

- ✅ Rendering homepage
- ✅ Sottomissione form con nome valido
- ✅ Visualizzazione storico vuoto
- ✅ Visualizzazione storico con sottomissioni
- ✅ Cancellazione storico
- ✅ Funzione `save_submission()`
- ✅ Funzione `load_history()`
- ✅ Creazione file di log

### Coverage

Per eseguire i test con coverage:

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

---

## 📂 Struttura del Progetto

```
Copilot_web_Demo/
├── app.py                              # Applicazione Flask principale
├── requirements.txt                    # Dipendenze Python
├── test_app.py                        # Suite di test
│
├── templates/                         # Template HTML
│   ├── index.html                    # Homepage con form
│   └── history.html                  # Pagina storico
│
├── static/                           # File statici (CSS, JS)
│   └── style.css                    # Stili personalizzati
│
├── agent_instructions.md             # Istruzioni per Copilot Agent
├── copilot_prompts.md               # Esempi di prompt Copilot
├── azure-devops-mcp-demo-commands.md # Comandi Azure DevOps MCP
├── wit_get_work_item_example.md     # Esempi Work Items
├── Test.txt                         # Tabella modalità Copilot
│
├── submission_history.json          # Storico sottomissioni (generato)
├── submissions.log                  # File di log (generato)
│
└── .vscode/                        # Configurazioni VS Code
    ├── copilot-instructions.md     # Istruzioni per Copilot
    └── mcp.json                    # Configurazione MCP
```

---

## 🎨 Caratteristiche UI

- **Design moderno** con gradiente e glassmorphism
- **Validazione real-time** con feedback visivo
- **Animazioni fluide** per transizioni e interazioni
- **Responsive design** per dispositivi mobili
- **Messaggi di errore** chiari e user-friendly
- **Icone e emoji** per migliore UX

---

## 🔄 Workflow Tipico

1. **Sviluppo**: Usa i prompt in `copilot_prompts.md` per esplorare Copilot
2. **Testing**: Esegui `pytest` per validare le modifiche
3. **Azure DevOps**: Testa i comandi MCP con i tuoi progetti
4. **Iterazione**: Usa le istruzioni in `agent_instructions.md` per nuove feature

---

## 📝 Note

- I file `submission_history.json` e `submissions.log` sono generati automaticamente
- L'applicazione è in modalità debug per default (modifica in produzione)
- I comandi MCP richiedono un Personal Access Token (PAT) di Azure DevOps
- Alcuni comandi MCP sono specifici per il progetto "Test MCP Server ADO"

---

## 🤝 Contribuire

Le contribuzioni sono benvenute! Per contribuire:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Pusha sul branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

---

## 📄 Licenza

Questo progetto è fornito "as-is" per scopi dimostrativi ed educativi.

---

## 👤 Autore

**pta19059**

- GitHub: [@pta19059](https://github.com/pta19059)

---

## 🙏 Ringraziamenti

- **GitHub Copilot** per l'assistenza allo sviluppo
- **Flask** per il framework web
- **Azure DevOps** per l'integrazione MCP
- La community open source

---

## 📚 Risorse Utili

- [Documentazione Flask](https://flask.palletsprojects.com/)
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Azure DevOps API](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Buon coding con GitHub Copilot! 🚀**
