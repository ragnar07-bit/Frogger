# 🐸 Frogger

Un'implementazione completa del classico gioco arcade **Frogger** sviluppato in Python con grafica 2D.

---

## 📋 Descrizione

Frogger è un gioco d'azione e logica retrò dove il giocatore controlla una rana che deve attraversare una strada trafficata e un fiume pieno di tronchi per raggiungere l'altra sponda. Il gioco combina elementi di strategia e riflessi, richiedendo al giocatore di pianificare i movimenti per evitare automobili e saltare sui tronchi in movimento.

### Caratteristiche Principali

- 🎮 Gameplay classico e coinvolgente
- 🎨 Grafica sprite-based personalizzata
- 🔊 Effetti audio e musica di sottofondo
- 📊 Sistema di punteggio e vite
- 🎯 Menu principale intuitivo
- ⚡ Difficoltà progressiva

---

## 🗂️ Struttura del Progetto

```
Frogger/
├── main.py                  # Punto di entrata principale
├── main.spec               # Configurazione PyInstaller per compilazione
├── requirements.txt        # Dipendenze Python
├── README.md              # Questo file
│
├── assets/                # Risorse del gioco
│   ├── audio/            # File audio (.mp3, .wav)
│   │   ├── background_music.mp3
│   │   ├── jump_sound.wav
│   │   ├── collision_sound.wav
│   │   └── win_sound.wav
│   │
│   └── images/           # Sprite e texture
│       ├── frog.png
│       ├── car.png
│       ├── log.png
│       ├── background.png
│       └── ui_elements.png
│
├── src/                   # Codice sorgente principale
│   ├── Giocatore.py      # Classe del giocatore (rana)
│   ├── Main_Menu.py      # Schermata del menu principale
│   ├── Game.py           # Logica principale del gioco
│   ├── Enemy.py          # Classe nemici (automobili, tronchi)
│   └── Level.py          # Sistema dei livelli
│
├── lib/                   # Librerie di supporto
│   ├── g2d.py            # Libreria grafica 2D principale
│   └── g2d_pyodide.py    # Supporto compatibilità Pyodide
│
└── build/                 # Directory di build (generato)
    └── main/             # Output compilato PyInstaller
```

---

## 🚀 Installazione

### Prerequisiti

- **Python 3.8+** (testato su Python 3.9+)
- **pip** (gestore pacchetti Python)
- **git** (per clonare il repository)

### Passaggi di Installazione

1. **Clonare il repository**
   ```bash
   git clone https://github.com/USERNAME/Frogger.git
   cd Frogger
   ```

2. **Creare un ambiente virtuale** (consigliato)
   ```bash
   # Su Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   
   # Su Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Installare le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎮 Come Giocare

### Avviare il Gioco

```bash
python main.py
```

Il gioco si avvierà mostrando il menu principale.

### Controlli

| Azione | Tasto |
|--------|-------|
| **Muovere su** | `↑` oppure `W` |
| **Muovere giù** | `↓` oppure `S` |
| **Muovere sinistra** | `←` oppure `A` |
| **Muovere destra** | `→` oppure `D` |
| **Pausa** | `SPAZIO` |
| **Menu principale** | `ESC` |
| **Uscire** | `ALT + F4` oppure chiudere la finestra |

### Obiettivo del Gioco

1. **Attraversare la strada** - Evita le automobili in movimento
2. **Saltare i tronchi** - Attraversa il fiume saltando da un tronco all'altro
3. **Raggiungere la sponda** - Arriva alla cima dello schermo per completare il livello
4. **Progressione** - Completa più livelli con difficoltà crescente

---

## 📦 Dipendenze

| Libreria | Versione | Utilizzo |
|----------|----------|----------|
| pygame | 2.0+ | Rendering grafico e input |
| numpy | 1.20+ | Calcoli matematici |

Per visualizzare tutte le dipendenze:
```bash
cat requirements.txt
```

---

## 🏗️ Build e Distribuzione

### Compilare in Eseguibile Standalone

Usa PyInstaller per creare un eseguibile indipendente:

```bash
pyinstaller main.spec
```

L'eseguibile compilato si troverà in `build/main/` e potrà essere distribuito senza richiedere Python installato.

### Opzioni PyInstaller

Per personalizzare la build, modifica `main.spec`:
- **Nome applicazione** - Cambia il nome dell'eseguibile
- **Icona** - Aggiungi un'icona personalizzata
- **Dati aggiuntivi** - Includi asset come immagini e audio

---

## 🎯 Architettura del Codice

### Componenti Principali

#### `main.py`
- Punto di entrata dell'applicazione
- Inizializza la finestra di gioco
- Gestisce il loop principale

#### `src/Giocatore.py`
- Classe `Giocatore` che rappresenta la rana
- Gestisce movimento e collisioni
- Stato di vite e punteggio

#### `src/Main_Menu.py`
- Schermata di menu principale
- Selezione difficoltà/livello
- Opzioni di gioco

#### `lib/g2d.py`
- Libreria grafica 2D custom
- Funzioni per disegnare sprite e testi
- Gestione degli eventi input

---

## 🐛 Debugging e Troubleshooting

### Il gioco non si avvia
```bash
# Verificare che Python 3.8+ sia installato
python --version

# Verificare che pygame sia correttamente installato
python -c "import pygame; print(pygame.__version__)"
```

### Errore di import
```bash
# Reinstallare le dipendenze
pip install -r requirements.txt --force-reinstall
```

### Basso framerate o lag
- Chiudere altre applicazioni pesanti
- Verificare il file `main.py` per loop inefficienti
- Controllare le risorse (CPU, RAM) con `top` o Task Manager

---

## 📊 Sistema di Punteggio

- **Movimento avanti**: +10 punti per ogni riga
- **Completamento livello**: +500 punti
- **Bonus tempo**: punti extra se completato velocemente
- **Moltiplicatore difficoltà**: 1x, 2x, 3x in base al livello

---

## 🎓 Sviluppo e Contributi

### Per gli sviluppatori

Se vuoi estendere il gioco:

1. **Aggiungere un nuovo nemico**: Crea una nuova classe in `src/Enemy.py` che eredita da `Enemy`
2. **Aggiungere un nuovo livello**: Modifica `src/Level.py` con parametri personalizzati
3. **Migliorare la grafica**: Sostituisci i file in `assets/images/`
4. **Aggiungere musica**: Aggiungi file audio in `assets/audio/`

### Stile di codice

- Usa **snake_case** per nomi di variabili e funzioni
- Aggiungi **docstring** a tutte le classi e metodi
- Segui lo stile **PEP 8**
- Commenta il codice complesso

---

## 📝 Licenza

Questo progetto è rilasciato sotto la licenza **MIT**.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

Vedi il file `LICENSE` per i dettagli completi.

---

## 👤 Autore

**Studente UNIPR** - Progetto per corso di programmazione

- 📧 Email: [tua-email@example.com]
- 🔗 GitHub: [github.com/USERNAME]
- 🏫 Università: Università di Parma

---

## 🙏 Ringraziamenti

- Ispirato dal classico gioco arcade Frogger (1981)
- Grazie alla comunità Python e pygame
- Ressorse grafiche e audio da fonti open-source

---

## 📞 Supporto

Per segnalare bug o suggerimenti:

1. Apri una **Issue** su GitHub
2. Descrivi il problema in dettaglio
3. Allega screenshot o traceback se disponibili
4. Specifica il sistema operativo e versione Python

---

## 📚 Risorse Utili

- [Documentazione Pygame](https://www.pygame.org/docs/)
- [Tutorial Python](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Git Documentation](https://git-scm.com/doc)

---

**Ultima modifica**: Giugno 2024  
**Versione**: 1.0.0