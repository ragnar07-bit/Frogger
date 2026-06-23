import lib.g2d as g2d

# ---------------------------------------------------------------------------
# Costanti sprite sheet (griglia 32×32 px)
# ---------------------------------------------------------------------------
C = 32

SPRITE     = "frogger.png"
BACKGROUND = "frogger-bg.png"

# Clip degli elementi grafici usati nel menu
_LOGO_CLIP   = (0,    8*C, 7*C,  C)   # scritta FROGGER  (224×32)
_CIRCLE_BTN  = (4*C,  6*C,  C,   C)   # cerchio giallo/viola (32×32)
_SNAKE_CLIP  = (0,    7*C, 5*C,  C)   # serpente verde   (160×32)
_CROC_CLIP   = (5*C,  7*C, 5*C,  C)   # coccodrillo      (160×32)
_FROG_CLIP   = (2*C,  0,    C,   C)   # rana ferma (cursore / decorazione)
_TURTLE_CLIP = (6*C,  5*C,  C,   C)   # tartaruga verde (coordinata corretta)

# Dimensioni area cliccabile di ogni bottone
_BTN_W, _BTN_H = 260, 48

# Posizioni Y dei centri dei tre bottoni
_BTN0_CY = 254   # GIOCA
_BTN1_CY = 324   # COME SI GIOCA
_BTN2_CY = 394   # ESCI

_BTNS = [_BTN0_CY, _BTN1_CY, _BTN2_CY]


class MainMenu:
    def __init__(self, canvas_w: int, canvas_h: int):
        self._cw = canvas_w
        self._ch = canvas_h

        self._voce_sel  = 0        # 0=GIOCA, 1=COME SI GIOCA, 2=ESCI
        self._anim_tick = 0
        self._mostra_istruzioni = False

        # Segnali letti dal main dopo ogni aggiorna()
        self._avvia = False
        self._esci  = False

    # ------------------------------------------------------------------
    # Segnali pubblici
    # ------------------------------------------------------------------
    @property
    def avvia(self) -> bool:
        return self._avvia

    @property
    def esci(self) -> bool:
        return self._esci

    # ------------------------------------------------------------------
    # Aggiornamento
    # ------------------------------------------------------------------
    def aggiorna(self) -> None:
        self._avvia = False
        self._esci  = False
        self._anim_tick += 1

        if self._mostra_istruzioni:
            # Qualsiasi tasto/click chiude le istruzioni
            if g2d.key_pressed("Enter") or g2d.key_pressed("Escape") \
                    or g2d.key_pressed("Spacebar") or g2d.mouse_clicked():
                self._mostra_istruzioni = False
        else:
            self._gestisci_tastiera()
            self._gestisci_mouse()

    def _gestisci_tastiera(self) -> None:
        if g2d.key_pressed("ArrowUp"):
            self._voce_sel = (self._voce_sel - 1) % 3
        elif g2d.key_pressed("ArrowDown"):
            self._voce_sel = (self._voce_sel + 1) % 3

        if g2d.key_pressed("Enter") or g2d.key_pressed("Spacebar"):
            self._conferma()

    def _gestisci_mouse(self) -> None:
        if not g2d.mouse_clicked():
            return
        mx, my = g2d.mouse_pos()
        bx = self._cw // 2 - _BTN_W // 2
        for i, cy in enumerate(_BTNS):
            if bx <= mx <= bx + _BTN_W:
                if cy - _BTN_H // 2 <= my <= cy + _BTN_H // 2:
                    self._voce_sel = i
                    self._conferma()
                    return

    def _conferma(self) -> None:
        if self._voce_sel == 0:
            self._avvia = True
        elif self._voce_sel == 1:
            self._mostra_istruzioni = True
        else:
            self._esci = True

    # ------------------------------------------------------------------
    # Disegno
    # ------------------------------------------------------------------
    def disegna(self) -> None:
        g2d.clear_canvas()
        self._disegna_sfondo()
        self._disegna_logo()
        self._disegna_sottotitolo()
        self._disegna_tartarughe()
        self._disegna_bottone("  GIOCA  ",        _BTN0_CY, self._voce_sel == 0)
        self._disegna_bottone(" COME SI GIOCA ",  _BTN1_CY, self._voce_sel == 1)
        self._disegna_bottone("   ESCI   ",       _BTN2_CY, self._voce_sel == 2)
        self._disegna_cursore_rana()
        self._disegna_decorazioni_basse()

        if self._mostra_istruzioni:
            self._disegna_schermata_istruzioni()

    def _disegna_sfondo(self) -> None:
        g2d.draw_image(BACKGROUND, (0, 0))
        g2d.set_color((0, 0, 0, 140))
        g2d.draw_rect((0, 0), (self._cw, self._ch))

    def _disegna_logo(self) -> None:
        logo_w = _LOGO_CLIP[2]
        logo_x = self._cw // 2 - logo_w // 2
        logo_y = 40
        g2d.draw_image(SPRITE, (logo_x, logo_y),
                       (_LOGO_CLIP[0], _LOGO_CLIP[1]),
                       (_LOGO_CLIP[2], _LOGO_CLIP[3]))
        g2d.draw_image(SPRITE, (logo_x - C - 8, logo_y),
                       (_FROG_CLIP[0], _FROG_CLIP[1]), (C, C))
        g2d.draw_image(SPRITE, (logo_x + logo_w + 8, logo_y),
                       (_FROG_CLIP[0], _FROG_CLIP[1]), (C, C))

    def _disegna_sottotitolo(self) -> None:
        g2d.set_color((0, 255, 200))
        g2d.draw_text("Usa le frecce  •  INVIO per confermare",
                      (self._cw // 2, 110), 18)

    def _disegna_tartarughe(self) -> None:
        y = 170
        for i in range(8):
            g2d.draw_image(SPRITE, (i * (C + 8) + 24, y),
                           (_TURTLE_CLIP[0], _TURTLE_CLIP[1]), (C, C))

    def _disegna_bottone(self, label: str, cy: int, selezionato: bool) -> None:
        cx = self._cw // 2
        bx = cx - _BTN_W // 2
        by = cy - _BTN_H // 2

        alpha = 180 if selezionato else 120
        g2d.set_color((0, 0, 0, alpha))
        g2d.draw_rect((bx, by), (_BTN_W, _BTN_H))

        border = (255, 220, 0) if selezionato else (80, 80, 80)
        g2d.set_color(border)
        g2d.draw_line((bx,          by         ), (bx + _BTN_W, by          ), 3)
        g2d.draw_line((bx + _BTN_W, by         ), (bx + _BTN_W, by + _BTN_H ), 3)
        g2d.draw_line((bx + _BTN_W, by + _BTN_H), (bx,          by + _BTN_H ), 3)
        g2d.draw_line((bx,          by + _BTN_H), (bx,           by          ), 3)

        icon_y = cy - C // 2
        g2d.draw_image(SPRITE, (bx - C - 4,        icon_y),
                       (_CIRCLE_BTN[0], _CIRCLE_BTN[1]), (C, C))
        g2d.draw_image(SPRITE, (bx + _BTN_W + 4,   icon_y),
                       (_CIRCLE_BTN[0], _CIRCLE_BTN[1]), (C, C))

        testo_color = (255, 220, 0) if selezionato else (180, 180, 180)
        g2d.set_color(testo_color)
        g2d.draw_text(label, (cx, cy), 26)

    def _disegna_cursore_rana(self) -> None:
        cy     = _BTNS[self._voce_sel]
        offset = 4 if (self._anim_tick // 8) % 2 == 0 else 0
        rx     = self._cw // 2 - _BTN_W // 2 - C * 2 - 8
        ry     = cy - C // 2 + offset
        g2d.draw_image(SPRITE, (rx, ry), (_FROG_CLIP[0], _FROG_CLIP[1]), (C, C))

    def _disegna_decorazioni_basse(self) -> None:
        bottom_y = self._ch - C - 8
        g2d.draw_image(SPRITE, (10, bottom_y),
                       (_SNAKE_CLIP[0], _SNAKE_CLIP[1]),
                       (_SNAKE_CLIP[2], _SNAKE_CLIP[3]))
        croc_x = self._cw - _CROC_CLIP[2] - 10
        g2d.draw_image(SPRITE, (croc_x, bottom_y),
                       (_CROC_CLIP[0], _CROC_CLIP[1]),
                       (_CROC_CLIP[2], _CROC_CLIP[3]))

    def _disegna_schermata_istruzioni(self) -> None:
        """Overlay semitrasparente con le istruzioni di gioco."""
        # Sfondo scuro
        g2d.set_color((0, 0, 0, 210))
        g2d.draw_rect((0, 0), (self._cw, self._ch))

        # Riquadro centrale
        box_w, box_h = 480, 320
        box_x = self._cw // 2 - box_w // 2
        box_y = self._ch // 2 - box_h // 2
        g2d.set_color((20, 20, 60, 240))
        g2d.draw_rect((box_x, box_y), (box_w, box_h))

        # Bordo dorato
        g2d.set_color((255, 220, 0))
        g2d.draw_line((box_x,           box_y          ), (box_x + box_w, box_y          ), 3)
        g2d.draw_line((box_x + box_w,   box_y          ), (box_x + box_w, box_y + box_h  ), 3)
        g2d.draw_line((box_x + box_w,   box_y + box_h  ), (box_x,         box_y + box_h  ), 3)
        g2d.draw_line((box_x,           box_y + box_h  ), (box_x,         box_y          ), 3)

        cx = self._cw // 2

        # Titolo
        g2d.set_color((255, 220, 0))
        g2d.draw_text("COME SI GIOCA", (cx, box_y + 30), 28)

        # Istruzioni
        g2d.set_color((255, 255, 255))
        righe = [
            ("↑  Su",            "Muovi la rana verso l'alto"),
            ("↓  Giù",           "Muovi la rana verso il basso"),
            ("←  Sinistra",      "Muovi la rana a sinistra"),
            ("→  Destra",        "Muovi la rana a destra"),
        ]
        y0 = box_y + 80
        for i, (tasto, desc) in enumerate(righe):
            y = y0 + i * 40
            g2d.set_color((0, 255, 200))
            g2d.draw_text(tasto, (box_x + 130, y), 20)
            g2d.set_color((220, 220, 220))
            g2d.draw_text(desc,  (box_x + 330, y), 20)

        # Obiettivo
        g2d.set_color((255, 180, 0))
        g2d.draw_text("Obiettivo: raggiungi la riva 5 volte per vincere!",
                      (cx, box_y + 250), 17)

        # Avviso per chiudere
        g2d.set_color((160, 160, 160))
        g2d.draw_text("Premi INVIO, ESC o clicca per tornare al menu",
                      (cx, box_y + 290), 16)