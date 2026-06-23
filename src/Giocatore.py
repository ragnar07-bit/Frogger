import lib.g2d as g2d

# ---------------------------------------------------------------------------
# Coordinate sprite sheet  (frogger.png – griglia 32×32 px, 10 col × 9 righe)
# ---------------------------------------------------------------------------
CELL = 32          # dimensione di una cella nel foglio sprite

# Ogni direzione ha 2 frame: (col_frame0, col_frame1, riga)
_FROG_FRAMES = {
    "up":    (0, 1, 0),
    "down":  (0, 1, 1),
    "left":  (0, 1, 2),
    "right": (0, 1, 3),
}

# ---------------------------------------------------------------------------
# Costanti di gioco
# ---------------------------------------------------------------------------
STEP        = 40     # pixel per ogni salto
ANIM_TICKS  = 6     # frame in cui si mostra il frame di salto


class Giocatore:
    """Rappresenta la rana controllata dal giocatore."""

    # ------------------------------------------------------------------
    # Costruzione
    # ------------------------------------------------------------------
    def __init__(self, start_x: int, start_y: int):
        self._x = start_x
        self._y = start_y
        self._dir   = "up"      # direzione corrente
        self._frame = 0         # 0 = fermo, 1 = in salto
        self._anim  = 0         # contatore tick animazione
        self._vite  = 3
        self._vivo  = True
        self._start_x = start_x
        self._start_y = start_y

    # ------------------------------------------------------------------
    # Proprietà di accesso
    # ------------------------------------------------------------------
    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def w(self) -> int:
        return CELL

    @property
    def h(self) -> int:
        return CELL

    @property
    def vite(self) -> int:
        return self._vite

    @property
    def vivo(self) -> bool:
        return self._vivo

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def gestisci_input(self, canvas_w: int, canvas_h: int) -> None:
        """Legge i tasti premuti e sposta la rana di un passo."""
        if self._anim > 0:
            return  # durante il salto non si accetta input

        moved = False
        if g2d.key_pressed("ArrowUp"):
            self._dir = "up"
            self._y   = max(0, self._y - STEP)
            moved = True
        elif g2d.key_pressed("ArrowDown"):
            self._dir = "down"
            self._y   = min(canvas_h - CELL, self._y + STEP)
            moved = True
        elif g2d.key_pressed("ArrowLeft"):
            self._dir = "left"
            self._x   = max(0, self._x - STEP)
            moved = True
        elif g2d.key_pressed("ArrowRight"):
            self._dir = "right"
            self._x   = min(canvas_w - CELL, self._x + STEP)
            moved = True

        if moved:
            self._frame = 1
            self._anim  = ANIM_TICKS

    # ------------------------------------------------------------------
    # Aggiornamento
    # ------------------------------------------------------------------
    def aggiorna(self) -> None:
        """Avanza l'animazione di salto."""
        if self._anim > 0:
            self._anim -= 1
            if self._anim == 0:
                self._frame = 0

    def trascinato(self, dx: int) -> None:
        """Sposta orizzontalmente la rana (usato dai tronchi/tartarughe)."""
        self._x += dx

    def muori(self) -> None:
        """Scala una vita e riposiziona la rana."""
        self._vite -= 1
        if self._vite <= 0:
            self._vivo = False
        else:
            self.respawn()

    def respawn(self) -> None:
        """Riporta la rana alla posizione di partenza."""
        self._x    = self._start_x
        self._y    = self._start_y
        self._dir  = "up"
        self._frame = 0
        self._anim  = 0

    # ------------------------------------------------------------------
    # Rettangolo di collisione (leggermente più piccolo dello sprite)
    # ------------------------------------------------------------------
    def rettangolo(self) -> tuple[int, int, int, int]:
        """Restituisce (x, y, w, h) del rettangolo di collisione."""
        margin = 4
        return (self._x + margin, self._y + margin,
                CELL - margin * 2, CELL - margin * 2)

    # ------------------------------------------------------------------
    # Disegno
    # ------------------------------------------------------------------
    def disegna(self) -> None:
        """Disegna la rana sullo schermo."""
        col0, col1, row = _FROG_FRAMES[self._dir]
        col = col1 if self._frame == 1 else col0
        clip_x = col  * CELL
        clip_y = row  * CELL
        g2d.draw_image("frogger.png",
                       (self._x, self._y),
                       (clip_x, clip_y),
                       (CELL, CELL))