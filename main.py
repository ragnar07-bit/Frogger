from lib import g2d
import pygame  # Per gestire gli effetti sonori
from pathlib import Path
from src.Giocatore  import Giocatore, CELL
from src.Main_Menu  import MainMenu

# ===========================================================================
# COSTANTI
# ===========================================================================
CANVAS_W, CANVAS_H = 640, 480
FPS        = 30
SPRITE     = "frogger.png"
BACKGROUND = "frogger-bg.png"

# Gestione percorsi per l'audio
BASE_DIR  = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "assets" / "audio"

START_X = CANVAS_W // 2 - CELL // 2
START_Y = CANVAS_H - 50

# Zone del livello (Y)
GOAL_Y         = 20
WATER_TOP_Y    = 60
WATER_BOTTOM_Y = 220
ROAD_TOP_Y     = 260
ROAD_BOTTOM_Y  = 420

# ---------------------------------------------------------------------------
# SPRITE – coordinate di ritaglio (clip_x, clip_y, clip_w, clip_h)
# griglia 32×32 px
# ---------------------------------------------------------------------------
C = CELL

CAR_YELLOW  = (6*C, 0,   C,   C)      # cella 6,0
CAR_PURPLE  = (6*C, 1*C, C,   C)      # cella 6,1
TRUCK_WHITE = (7*C, 2*C, 2*C, C)      # celle 7,2 + 8,2
TRUCK_GREEN = (9*C, 0,   C,   C)      # cella 9,0 (veicolo alternativo)
LOG_LONG    = (6*C, 3*C, 3*C, C)      # celle 6,3 + 7,3 + 8,3
TURTLE      = (6*C, 5*C, C,   C)      # cella 6,5


# ===========================================================================
# CLASSI OSTACOLI / PIATTAFORME
# ===========================================================================

class Veicolo:
    def __init__(self, x, y, velocita, clip, w=C):
        self._x, self._y = x, y
        self._vx         = velocita
        self._clip       = clip
        self._w, self._h = w, C

    def aggiorna(self):
        self._x += self._vx
        if self._vx > 0 and self._x > CANVAS_W:
            self._x = -self._w
        elif self._vx < 0 and self._x + self._w < 0:
            self._x = CANVAS_W

    def rettangolo(self):
        return (self._x, self._y, self._w, self._h)

    def disegna(self):
        cx, cy, cw, ch = self._clip
        g2d.draw_image(SPRITE, (self._x, self._y), (cx, cy), (cw, ch))


class Piattaforma:
    def __init__(self, x, y, velocita, clip, w=C):
        self._x, self._y = x, y
        self._vx         = velocita
        self._clip       = clip
        self._w, self._h = w, C

    @property
    def velocita(self): return self._vx

    def aggiorna(self):
        self._x += self._vx
        if self._vx > 0 and self._x > CANVAS_W:
            self._x = -self._w
        elif self._vx < 0 and self._x + self._w < 0:
            self._x = CANVAS_W

    def rettangolo(self):
        return (self._x, self._y, self._w, self._h)

    def disegna(self):
        cx, cy, cw, ch = self._clip
        g2d.draw_image(SPRITE, (self._x, self._y), (cx, cy), (cw, ch))


# ===========================================================================
# STATO GLOBALE
# ===========================================================================
_stato:       str              = "menu"
_menu:        MainMenu | None  = None
_giocatore:   Giocatore | None = None
_veicoli:     list             = []
_piattaforme: list             = []
_punteggio:   int              = 0

# Variabili globali per memorizzare i suoni
_sfx_jump:       pygame.mixer.Sound | None = None
_sfx_splash:     pygame.mixer.Sound | None = None
_sfx_squish:     pygame.mixer.Sound | None = None


# ===========================================================================
# INIZIALIZZAZIONE
# ===========================================================================

def _crea_veicoli() -> list:
    return [
        # Corsia 1 dal basso – Y=380 – auto gialle verso destra
        Veicolo(0,   370,  3, CAR_YELLOW),
        Veicolo(230, 370,  3, CAR_YELLOW),
        Veicolo(460, 370,  3, CAR_YELLOW),

        # Corsia 2 dal basso – Y=340 – camion bianchi verso sinistra
        Veicolo(100, 340, -2, TRUCK_WHITE, w=2*C),
        Veicolo(450, 340, -2, TRUCK_WHITE, w=2*C),

        # Corsia 3 dal basso – Y=300 – auto viola verso destra
        Veicolo(50,  305,  4, CAR_PURPLE),
        Veicolo(230, 305,  4, CAR_PURPLE),
        Veicolo(410, 305,  4, CAR_PURPLE),
        Veicolo(590, 305,  4, CAR_PURPLE),

        # Corsia 4 dal basso – Y=260 – camion verdi verso sinistra
        Veicolo(200, 270, -3, TRUCK_GREEN),
        Veicolo(550, 270, -3, TRUCK_GREEN),
    ]


def _crea_piattaforme() -> list:
    return [
        # Riga 1 acqua – Y=185 – tronchi verso destra
        Piattaforma(0,   185,  2, LOG_LONG, w=3*C),
        Piattaforma(240, 185,  2, LOG_LONG, w=3*C),
        Piattaforma(480, 185,  2, LOG_LONG, w=3*C),

        # Riga 2 acqua – Y=150 – tartarughe verso sinistra
        Piattaforma(0,   150, -2, TURTLE),
        Piattaforma(175, 150, -2, TURTLE),
        Piattaforma(350, 150, -2, TURTLE),
        Piattaforma(525, 150, -2, TURTLE),

        # Riga 3 acqua – Y=115 – tronchi verso destra
        Piattaforma(0,   115,  3, LOG_LONG, w=3*C),
        Piattaforma(280, 115,  3, LOG_LONG, w=3*C),
        Piattaforma(520, 115,  3, LOG_LONG, w=3*C),

        # Riga 4 acqua – Y=80 – tartarughe verso sinistra
        Piattaforma(0,    80, -1, TURTLE),
        Piattaforma(220,  80, -1, TURTLE),
        Piattaforma(440,  80, -1, TURTLE),
    ]


def inizializza() -> None:
    """Crea canvas, carica risorse, istanzia il menu. Chiamata una sola volta."""
    global _menu, _sfx_jump, _sfx_splash, _sfx_squish # Rimosso _sfx__main_theme dalle globali
    g2d.init_canvas((CANVAS_W, CANVAS_H))
    g2d.load_image(SPRITE)
    g2d.load_image(BACKGROUND)
    
    # Inizializziamo il sistema audio
    pygame.mixer.init()
    
    # Effetti sonori brevi
    _sfx_jump   = pygame.mixer.Sound(str(AUDIO_DIR / "sfx_jump.wav"))
    _sfx_splash = pygame.mixer.Sound(str(AUDIO_DIR / "sfx_splash.wav"))
    _sfx_squish = pygame.mixer.Sound(str(AUDIO_DIR / "sfx_squish.wav"))

    # Gestione Musica di sottofondo con il modulo music
    pygame.mixer.music.load(str(AUDIO_DIR / "sfx_main_theme.wav"))
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)         # Riproduce in loop infinito
    
    _menu = MainMenu(CANVAS_W, CANVAS_H)


def _avvia_partita() -> None:
    """Resetta lo stato di gioco e passa allo stato 'gioco'."""
    global _giocatore, _veicoli, _piattaforme, _punteggio, _stato
    _giocatore   = Giocatore(START_X, START_Y)
    _veicoli     = _crea_veicoli()
    _piattaforme = _crea_piattaforme()
    _punteggio   = 0
    _stato       = "gioco"

def _torna_al_menu() -> None:
    """Torna alla schermata del menu."""
    global _stato
    _stato = "menu"


# ===========================================================================
# LOGICA DI GIOCO
# ===========================================================================

def _collide(a: tuple, b: tuple) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx+bw and ax+aw > bx and ay < by+bh and ay+ah > by


def _aggiorna_ostacoli() -> None:
    for v in _veicoli:     v.aggiorna()
    for p in _piattaforme: p.aggiorna()


def _gestisci_zona_acqua() -> None:
    fy = _giocatore.y + _giocatore.h // 2
    if not (WATER_TOP_Y < fy < WATER_BOTTOM_Y):
        return
    for p in _piattaforme:
        if _collide(_giocatore.rettangolo(), p.rettangolo()):
            _giocatore.trascinato(p.velocita)
            return
            
    # Riproduce il suono dell'affogamento appena fallisce il controllo
    _sfx_squish.play()
    _giocatore.muori()


def _gestisci_collisioni_strada() -> None:
    fy = _giocatore.y + _giocatore.h // 2
    if not (ROAD_TOP_Y < fy < ROAD_BOTTOM_Y):
        return
    for v in _veicoli:
        if _collide(_giocatore.rettangolo(), v.rettangolo()):
            # Riproduce il suono dell'auto che schiaccia la rana
            _sfx_splash.play()
            _giocatore.muori()
            return


def _controlla_obiettivo() -> None:
    global _punteggio, _stato
    if _giocatore.y <= GOAL_Y:
        _punteggio += 100
        _giocatore.respawn()
        if _punteggio >= 500:
            _stato = "vinci"


def _controlla_game_over() -> None:
    global _stato
    if not _giocatore.vivo:
        _stato = "game_over"


def aggiorna_logica() -> None:
    """Aggiorna tutto lo stato di gioco per un tick."""
    # Per il salto: salviamo la vecchia posizione prima che gestisci_input agisca
    pos_precedente = (_giocatore.x, _giocatore.y)
    
    _giocatore.gestisci_input(CANVAS_W, CANVAS_H)
    _giocatore.aggiorna()
    
    # Se le coordinate sono cambiate rispetto al frame precedente, riproduce il salto
    if (_giocatore.x, _giocatore.y) != pos_precedente and _giocatore.vivo:
        _sfx_jump.play()
        
    _aggiorna_ostacoli()
    _gestisci_zona_acqua()
    _gestisci_collisioni_strada()
    _controlla_obiettivo()
    _controlla_game_over()


# ===========================================================================
# DISEGNO DI GIOCO
# ===========================================================================

def _disegna_sfondo() -> None:
    g2d.draw_image(BACKGROUND, (0, 0))


def _disegna_ostacoli() -> None:
    for p in _piattaforme: p.disegna()
    for v in _veicoli:     v.disegna()


def _disegna_hud() -> None:
    g2d.set_color((255, 255, 0))
    g2d.draw_text(f"Punteggio: {_punteggio}", (120, 18), 20)
    g2d.draw_text(f"Vite: {_giocatore.vite}",  (520, 18), 20)


def _disegna_schermata_finale(testo: str) -> None:
    g2d.set_color((0, 0, 0, 160))
    g2d.draw_rect((0, 0), (CANVAS_W, CANVAS_H))
    g2d.set_color((255, 220, 0))
    g2d.draw_text(testo, (CANVAS_W // 2, CANVAS_H // 2 - 20), 52)
    g2d.set_color((255, 255, 255))
    g2d.draw_text("R = Rigioca   •   M = Menu",
                  (CANVAS_W // 2, CANVAS_H // 2 + 50), 20)


def disegna_gioco() -> None:
    """Ridisegna l'intero frame di gioco."""
    g2d.clear_canvas()
    _disegna_sfondo()
    _disegna_ostacoli()
    _giocatore.disegna()
    _disegna_hud()
    if _stato in ("game_over", "vinci"):
        label = "GAME  OVER" if _stato == "game_over" else "HAI  VINTO!"
        _disegna_schermata_finale(label)


# ===========================================================================
# TICK PRINCIPALE
# ===========================================================================

def tick() -> None:
    global _stato

    if _stato == "menu":
        _menu.aggiorna()
        _menu.disegna()
        if _menu.avvia:
            _avvia_partita()
        elif _menu.esci:
            g2d.close_canvas()

    elif _stato == "gioco":
        aggiorna_logica()
        disegna_gioco()

    else:  # "game_over" | "vinci"
        disegna_gioco()
        if g2d.key_pressed("r") or g2d.key_pressed("R"):
            _avvia_partita()
        elif g2d.key_pressed("m") or g2d.key_pressed("M"):
            _torna_al_menu()


# ===========================================================================
# ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    inizializza()
    g2d.main_loop(tick, fps=FPS)