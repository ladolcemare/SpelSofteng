# Opmerking (Famke Top): ik heb codekwaliteit verbeterd (structuur, leesbaarheid en comments); 
# niet alles tussentijds gecommit — overige bijdragen zijn wel via commits zichtbaar.

# =========================================
# Flappy Vis - Pygame Game
# Vak: 5081SOEN6Y - Software Engineering
#
# Beschrijving:
# Dit bestand bevat de main game logica,
# inclusief instellingen, kleuren en physics.
#
# Teamleden - 'pygame group 15': 
# Baving, Veron | Han, Lin | Sodderland, Mare | Top, Famke


# =========================================
# Imports (gebruikte modules):
# pygame  - game engine en rendering
# sys     - afsluiten van het programma
# random  - genereren van willekeurige objecten
# math    - wiskundige berekeningen (bijv. beweging)
# os      - werken met bestanden en paden
# wave    - laden van geluiden
# struct  - verwerken van audio data

import pygame
import sys
import random
import math
import os
import wave
import struct


# =========================================
# Configuratie (game instellingen en constanten):

# Scherm instellingen (resolutie en framerate van de game):
BREEDTE = 800
HOOGTE = 600
FPS = 60

# Kleuren (RGB-waarden voor visuele elementen in de game):
OCEAAN_BLAUW = (0, 105, 148)
ORANJE = (255, 165, 0)
DONKER_ORANJE = (255, 140, 0)
WIT = (255, 255, 255)
ZWART = (0, 0, 0)
ROOD = (255, 0, 0)
GRIJS = (200, 200, 200)
DONKER_ROOD = (200, 80, 0)

# Vis instellingen (speler eigenschappen en beweging):
# VIS_X = vaste horizontale positie van de speler
# ZWAARTEKRACHT = snelheid waarmee de vis naar beneden valt
# SPRONG_KRACHT = kracht van een sprong (negatief = omhoog)
VIS_BREEDTE = 45
VIS_HOOGTE = 28
VIS_X = 150
ZWAARTEKRACHT = 0.5
SPRONG_KRACHT = -8

# Koraalrif instellingen (obstakels waar de speler doorheen moet):
# RIF_GAT_HOOGTE = opening tussen boven- en onderrif
# RIF_SNELHEID = snelheid waarmee obstakels bewegen
# RIF_INTERVAL = tijd tussen nieuwe obstakels (ms)
RIF_BREEDTE = 80
RIF_GAT_HOOGTE = 180
RIF_SNELHEID = 4
RIF_INTERVAL = 1800

# Koraalrif instellingen - kleur (obstakels waar de speler doorheen moet):
KORAAL_ROOD = (255, 69, 0)
KORAAL_DONKER = (200, 50, 0)

# Haai instellingen (extra vijanden / moeilijkheidsgraad)
# HAAI_INTERVAL = tijd tussen het verschijnen van haaien (ms)
HAAI_GRIJS = (150, 150, 160)
HAAI_DONKER = (100, 100, 110)
HAAI_WIT = (240, 240, 240)
HAAI_INTERVAL = 3000


# =========================================
# Koraalrif Klasse (Obstacle)
#
# Beschrijving:
# Deze klasse stelt een koraalrif voor waar
# de speler (vis) doorheen moet navigeren.
# Het rif bestaat uit een boven- en onderstuk
# met een opening (gat) ertussen.
#
# Functionaliteiten:
# - Genereren van een willekeurige opening
# - Bewegen van rechts naar links
# - Detecteren van botsingen met de vis
# - Tekenen van het rif op het scherm

class Koraalrif:
    """Een obstakel bestaande uit twee koraalstukken met een gat ertussen."""

    def __init__(self, snelheid=RIF_SNELHEID):  
        """ 
        Maakt een nieuw koraalrif aan aan de rechterkant van het scherm.

        >>> isinstance(Koraalrif().gat_boven, int)
        True

        >>> isinstance(Koraalrif().gat_onder, int)
        True

        >>> Koraalrif().x == BREEDTE
        True
        """

        self.x = BREEDTE
        self.snelheid = snelheid
        gat_midden = random.randint(150, HOOGTE - 150)

        self.gat_boven = gat_midden - RIF_GAT_HOOGTE // 2
        self.gat_onder = gat_midden + RIF_GAT_HOOGTE // 2

        self.gepasseerd = False  

    def beweeg(self):
        """
        Verplaatst het rif horizontaal naar links met constante snelheid.
        
        >>> rif = Koraalrif(snelheid=5)
        >>> oude_x = rif.x
        >>> rif.beweeg()
        >>> rif.x == oude_x - 5
        True
        """

        self.x -= self.snelheid

    def is_buiten_scherm(self):
        """
        Geeft True terug als het rif links van het scherm is.

        >>> rif = Koraalrif()
        >>> rif.x = -RIF_BREEDTE - 1
        >>> rif.is_buiten_scherm()
        True

        >>> rif = Koraalrif()
        >>> rif.x = 0
        >>> rif.is_buiten_scherm()
        False

        >>> rif = Koraalrif()
        >>> rif.x = -RIF_BREEDTE
        >>> rif.is_buiten_scherm()
        False
        """
        
        return self.x + RIF_BREEDTE < 0

    # -----------------------------------------
    # Botsingsdetectie
    #
    # Controleert:
    # - Controleer horizontale overlap tussen vis en rif (overlap x-as)
    # - Controleer of de vis zich buiten de opening (gat) bevindt
    # -----------------------------------------

    def raakt_vis(self, vis):
        """
        Geeft True terug als de vis het rif raakt.
        
        >>> vis = Vis()
        >>> rif = Koraalrif()
        >>> rif.x = vis.x
        >>> rif.gat_boven = 0
        >>> rif.gat_onder = 10
        >>> vis.y = 100
        >>> rif.raakt_vis(vis)
        True

        >>> vis = Vis()
        >>> rif = Koraalrif()
        >>> rif.x = vis.x
        >>> rif.gat_boven = 50
        >>> rif.gat_onder = 200
        >>> vis.y = 100
        >>> rif.raakt_vis(vis)
        False

        >>> vis = Vis()
        >>> rif = Koraalrif()
        >>> rif.x = vis.x + 200
        >>> rif.gat_boven = 0
        >>> rif.gat_onder = 10
        >>> vis.y = 100
        >>> rif.raakt_vis(vis)
        False

        """

        vis_rechts = vis.x + VIS_BREEDTE
        vis_onder = vis.y + VIS_HOOGTE

        raakt_x = vis.x < self.x + RIF_BREEDTE and vis_rechts > self.x
        raakt_boven = vis.y < self.gat_boven
        raakt_onder = vis_onder > self.gat_onder

        return raakt_x and (raakt_boven or raakt_onder)

    def teken(self, scherm):
        """Tekent het boven- en onderstuk van het koraalrif."""
        self._teken_stuk(scherm, 0, self.gat_boven)
        self._teken_stuk(scherm, self.gat_onder, HOOGTE)

    def _teken_stuk(self, scherm, van, tot):
        """Tekent één stuk koraal van een gegeven hoogte."""

        pygame.draw.rect(scherm, KORAAL_ROOD,
                         (self.x, van, RIF_BREEDTE, tot - van))
        
        # Rand voor diepte effect
        pygame.draw.rect(scherm, KORAAL_DONKER,
                         (self.x, van, 8, tot - van))
        
        pygame.draw.rect(scherm, KORAAL_DONKER,
                         (self.x + RIF_BREEDTE - 8, van, 8, tot - van))


# =========================================
# Vis Klasse (Speler)
#
# Beschrijving:
# Deze klasse stelt de speler voor in de vorm
# van een vis die door de oceaan beweegt.
# De vis kan omhoog springen en wordt continu
# naar beneden getrokken door zwaartekracht.
#
# Functionaliteiten:
# - Bewegen met zwaartekracht
# - Springen (omhoog bewegen)
# - Resetten naar beginpositie
# - Detecteren of de vis buiten beeld is
# - Tekenen van de vis (lichaam + details)

class Vis:
    """De speler (vis), beweegt omhoog en omlaag door de oceaan."""

    def __init__(self):
        """
        Maakt een nieuwe vis aan in het midden van het scherm.

        >>> vis = Vis()
        >>> vis.x == VIS_X
        True

        >>> vis.y == HOOGTE // 2
        True

        >>> vis.snelheid == 0
        True
        """
        
        self.x = VIS_X
        self.y = HOOGTE // 2
        self.snelheid = 0

    def reset(self):
        """
        Zet de vis terug naar de beginpositie.

        >>> vis = Vis()
        >>> vis.y = 100
        >>> vis.snelheid = 5
        >>> vis.reset()

        >>> vis.y == HOOGTE // 2
        True

        >>> vis.snelheid == 0
        True
        """

        self.y = HOOGTE // 2
        self.snelheid = 0

    def beweeg(self):
        """
        Past zwaartekracht toe en beweegt de vis.
        >>> vis = Vis()
        >>> oude_y = vis.y
        >>> vis.beweeg()

        >>> vis.y > oude_y
        True
        """

        self.snelheid += ZWAARTEKRACHT
        self.y += self.snelheid

    def spring(self):
        """
        Laat de vis omhoog bewegen.
        >>> vis = Vis()
        >>> vis.spring()

        >>> vis.snelheid == SPRONG_KRACHT
        True
        """

        self.snelheid = SPRONG_KRACHT

    def is_buiten_scherm(self):
        """
        Geef True terug als de vis buiten het scherm is.
        >>> vis = Vis()
        >>> vis.y = -1
        >>> vis.is_buiten_scherm()
        True

        >>> vis = Vis()
        >>> vis.y = HOOGTE + 1
        >>> vis.is_buiten_scherm()
        True

        >>> vis = Vis()
        >>> vis.y = HOOGTE // 2
        >>> vis.is_buiten_scherm()
        False
        """

        return self.y < 0 or self.y > HOOGTE

    def teken(self, scherm):
        """Teken de vis op het scherm."""
        self._teken_staart(scherm)
        self._teken_lichaam(scherm)
        self._teken_vinnen(scherm)
        self._teken_oog(scherm)
        self._teken_mond(scherm)

    def _teken_staart(self, scherm):
        """Tekent de staart van de vis."""
        x, y = self.x, int(self.y)

        staart_punten = [
            (x + 2, y + 8),
            (x + 2, y + 20),
            (x - 15, y + 14),
        ]

        pygame.draw.polygon(scherm, DONKER_ORANJE, staart_punten)

    def _teken_lichaam(self, scherm):
        """Tekent het lichaam van de vis."""
        x, y = self.x, int(self.y)

        pygame.draw.ellipse(scherm, ORANJE, (x, y, VIS_BREEDTE, VIS_HOOGTE))

    def _teken_vinnen(self, scherm):
        """Tekent de boven- en buikvin van de vis."""

        x, y = self.x, int(self.y)
        bovenvin_punten = [
            (x + 10, y),
            (x + 25, y),
            (x + 18, y - 12),
        ]

        buikvin_punten = [
            (x + 10, y + VIS_HOOGTE),
            (x + 22, y + VIS_HOOGTE),
            (x + 16, y + VIS_HOOGTE + 10),
        ]

        pygame.draw.polygon(scherm, ORANJE, bovenvin_punten)
        pygame.draw.polygon(scherm, ORANJE, buikvin_punten)

    def _teken_oog(self, scherm):
        """Tekent het oog van de vis inclusief pupil en highlight voor detail."""

        x, y = self.x, int(self.y)

        pygame.draw.circle(scherm, WIT, (x + 33, y + 10), 6)
        pygame.draw.circle(scherm, ZWART, (x + 34, y + 11), 3)
        pygame.draw.circle(scherm, WIT, (x + 35, y + 9), 1)

    def _teken_mond(self, scherm):
        """Tekent de mond van de vis."""

        x, y = self.x, int(self.y)

        pygame.draw.arc(scherm, DONKER_ROOD,
                        (x + 38, y + 14, 10, 8), 3.14, 2 * 3.14, 2)


# =========================================
# Explosie Klasse (Effect)
#
# Beschrijving:
# Deze klasse genereert een particle-based
# explosie effect op de positie van de vis.
# De explosie bestaat uit meerdere deeltjes
# die bewegen, vervagen en verdwijnen.
#
# Functionaliteiten:
# - Genereren van deeltjes met willekeurige richting
# - Simuleren van beweging met zwaartekracht
# - Fade-out effect (alpha)
# - Korte flits in het midden
# - Automatisch afronden van de animatie

class Explosie:
    """Particle-based explosie special effect.

    Genereert meerdere deeltjes met velocity, life en fade-out.
    Tekent een korte flits en de deeltjes met alpha.
    """

    def __init__(self, x, y, count=48):
        """
        >>> exp = Explosie(100, 200, count=10)
        >>> exp.frame == 0
        True

        >>> exp.finished
        False

        >>> len(exp.particles) == 10
        True

        >>> isinstance(exp.particles[0]["pos"], pygame.math.Vector2)
        True
        """

        self.x = x + VIS_BREEDTE // 2
        self.y = y + VIS_HOOGTE // 2

        self.frame = 0
        self.finished = False
        self.particles = []

        self.flash_life = 14

        kleuren = [ORANJE, ROOD, DONKER_ORANJE, (255, 220, 120)]

        for _ in range(count):
            #  Startpositie binnen de vis
            start_x = random.uniform(x, x + VIS_BREEDTE)
            start_y = random.uniform(y, y + VIS_HOOGTE)

            # Willekeurige richting (in radialen) zodat deeltjes alle kanten op bewegen
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.5, 9.0)

            vel = pygame.math.Vector2(math.cos(angle) * speed,
                                      math.sin(angle) * speed)
            
            r = random.randint(2, 6)
            kleur = random.choice(kleuren)
            life = random.randint(30, 70)

            self.particles.append({
                "pos": pygame.math.Vector2(start_x, start_y),
                "vel": vel,
                "r": r,
                "c": kleur,
                "life": life,
                "max_life": life,
            })

        # Houdt bij of geluid al is afgespeeld
        self.sound_played = False

    def update(self):
        """
        Update alle deeltjes en de status van de explosie.

        >>> exp = Explosie(100, 200, count=5)
        >>> oude_frame = exp.frame
        >>> exp.update()
        >>> exp.frame == oude_frame + 1
        True

        >>> exp = Explosie(100, 200, count=5)
        >>> for _ in range(100):
        ...     exp.update()
        >>> exp.finished
        True
        """

        self.frame += 1

        for p in self.particles:
            p["vel"].y += 0.18  # Simuleer zwaartekracht zodat deeltjes langzaam naar beneden vallen
            p["pos"] += p["vel"]
            p["life"] -= 1

        # verwijder dode deeltjes
        self.particles = [p for p in self.particles if p["life"] > 0]

        if self.frame > self.flash_life and not self.particles:
            self.finished = True

    # -----------------------------------------
    # Teken logica (flits + particles)
    #
    # - Centrale flits die groeit en vervaagt
    # - Deeltjes met alpha fade-out
    # -----------------------------------------

    def teken(self, scherm):
        """Tekent de explosie op het scherm."""

        overlay = pygame.Surface((BREEDTE, HOOGTE), pygame.SRCALPHA)

        # flits effect
        if self.frame <= self.flash_life:
            progress = self.frame / max(1, self.flash_life)
            alpha = int(220 * (1 - progress))
            radius = int(60 + 120 * progress)
            
            pygame.draw.circle(overlay, (255, 250, 230, alpha),
                               (int(self.x), int(self.y)), radius)

        # deeltjes tekenen
        for p in self.particles:
            life_frac = p["life"] / p["max_life"]

            alpha = int(255 * max(0, life_frac))

            col = (*p["c"][:3], alpha) if len(p["c"]) == 3 else (*p["c"], alpha)
            
            pygame.draw.circle(overlay, col,
                               (int(p["pos"].x), int(p["pos"].y)), p["r"])

        scherm.blit(overlay, (0, 0))


# =========================================
# Scherm Klasse (UI / Weergave)
#
# Beschrijving:
# Deze klasse beheert alle schermweergaven
# van het spel, zoals het startscherm,
# game over scherm en het spelscherm.
#
# Functionaliteiten:
# - Tonen van startscherm en instructies
# - Tonen van game over + score
# - Renderen van het spel (vis, obstakels, UI)
# - Tekenen van gecentreerde tekst

class Scherm:
    """Beheert alle visuele schermen van het spel."""

    def __init__(self, oppervlak):
        self.oppervlak = oppervlak
        self.font_groot = pygame.font.SysFont(None, 72)
        self.font_klein = pygame.font.SysFont(None, 36)

    def _teken_tekst_gecentreerd(self, tekst, font, kleur, y_offset):
        """Tekent tekst gecentreerde op het scherm."""

        render = font.render(tekst, True, kleur)

        x = BREEDTE // 2 - render.get_width() // 2
        
        self.oppervlak.blit(render, (x, HOOGTE // 2 + y_offset))

    def toon_startscherm(self):
        """Toont het startscherm met titel en instructie."""

        self.oppervlak.fill(OCEAAN_BLAUW)

        self._teken_tekst_gecentreerd(
            "Flappy Vis!", 
            self.font_groot, 
            WIT, 
            -60)
        
        self._teken_tekst_gecentreerd(
            "Druk op SPATIE om te beginnen",
            self.font_klein, 
            GRIJS, 
            20)
        
        pygame.display.flip()

    def toon_game_over(self, score=0):
        """Toont het game over scherm met score."""

        self._teken_tekst_gecentreerd(
            "Game Over!", 
            self.font_groot, 
            ROOD, 
            -60)
        
        score_tekst = self.font_klein.render(f"Score: {score}", True, WIT)

        x = BREEDTE // 2 - score_tekst.get_width() // 2
        
        self.oppervlak.blit(score_tekst, (x, HOOGTE // 2))
        self._teken_tekst_gecentreerd(
            "Druk op SPATIE om opnieuw te spelen",
            self.font_klein, 
            GRIJS, 
            50)
        
        pygame.display.flip()

    # -----------------------------------------
    # Hoofd render functie (spel)
    #
    # - Tekent achtergrond
    # - Tekent riffen, haaien en vis
    # - Toont score linksboven
    # - Ondersteunt optioneel render target
    # -----------------------------------------

    def toon_spel(self, vis, riffen=None, haaien=None, draw_vis=True, score=0, target=None):
        """ Rendert het volledige spelscherm. """

        if riffen is None:
            riffen = []

        if haaien is None:
            haaien = []

        surf = target if target is not None else self.oppervlak

        surf.fill(OCEAAN_BLAUW)
        for rif in riffen:
            rif.teken(surf)

        for haai in haaien:
            haai.teken(surf)

        if draw_vis and vis is not None:
            vis.teken(surf)

        # teken score linksboven
        score_text = self.font_klein.render(str(score), True, WIT)
        surf.blit(score_text, (10, 8))

        if target is None:
            pygame.display.flip()
        else:
            return surf


# =========================================
# Haai Klasse (Vijand - Basis)
#
# Beschrijving:
# Deze klasse vormt de basis voor alle haaien
# in het spel. Haaien bewegen van rechts naar
# links en vormen een extra obstakel voor de vis.
#
# Functionaliteiten:
# - Basispositie en grootte instellen
# - Detecteren of de haai buiten beeld is
# - Botsingsdetectie met de vis
# - Tekenen van de haai (vorm + details)
#
# Let op:
# De beweging wordt bepaald door subklassen.

class Haai:
    """
    Basisklasse voor alle haaien.

    >>> import pygame
    >>> haai = Haai()

    >>> haai.breedte == 60
    True

    >>> haai.x == BREEDTE + 50
    True
    """

    def __init__(self):
        self.x = BREEDTE + 50
        self.y = random.randint(50, HOOGTE - 50)

        self.breedte = 60
        self.hoogte = 30

    def beweeg(self):
        """Moet worden geïmplementeerd door subklassen."""
        raise NotImplementedError

    def is_buiten_scherm(self):
        """
        Controleert of de haai buiten beeld is.
        >>> haai = Haai()
        >>> haai.x = -70
        >>> haai.is_buiten_scherm()
        True

        >>> haai.x = 100
        >>> haai.is_buiten_scherm()
        False

        >>> haai.x = -60
        >>> haai.is_buiten_scherm()
        False
        """

        return self.x + self.breedte < 0
    
    # -----------------------------------------
    # Botsingsdetectie (AABB collision)
    #
    # Controleert overlap tussen vis en haai
    # op zowel x- als y-as
    # -----------------------------------------

    def raakt_vis(self, vis):
        """
        Geeft True terug als de haai de vis raakt.
        >>> vis = Vis()
        >>> haai = Haai()

        >>> vis.x, vis.y = 100, 100
        >>> haai.x, haai.y = 100, 100
        >>> haai.raakt_vis(vis)
        True

        >>> haai.x = 500
        >>> haai.raakt_vis(vis)
        False

        >>> haai.x = vis.x + VIS_BREEDTE + 1
        >>> haai.raakt_vis(vis)
        False
        """

        return (vis.x < self.x + self.breedte and
                vis.x + VIS_BREEDTE > self.x and
                vis.y < self.y + self.hoogte and
                vis.y + VIS_HOOGTE > self.y)

    def teken(self, scherm):
        """
        Teken de haai op het scherm.
        >>> import pygame
        >>> surf = pygame.Surface((100, 100))
        >>> haai = Haai()

        >>> haai.x, haai.y = 10, 10
        >>> haai.teken(surf)
        >>> isinstance(surf, pygame.Surface)
        True
        """

        x, y = int(self.x), int(self.y)

        # Staart
        staart_punten = [
            (x + self.breedte, y + self.hoogte // 2 - 10),
            (x + self.breedte, y + self.hoogte // 2 + 10),
            (x + self.breedte + 20, y + self.hoogte // 2 - 15),
            (x + self.breedte + 20, y + self.hoogte // 2 + 15),
        ]

        pygame.draw.polygon(scherm, HAAI_DONKER, staart_punten)

        # Lichaam
        pygame.draw.ellipse(scherm, HAAI_GRIJS,
                            (x, y, self.breedte, self.hoogte))

        # Buik
        pygame.draw.ellipse(scherm, HAAI_WIT,
                            (x + 5, y + self.hoogte // 2,
                             self.breedte - 15, self.hoogte // 2 - 2))

        # Bovenvin
        vin_punten = [
            (x + 15, y),
            (x + 30, y),
            (x + 22, y - 15),
        ]
        
        pygame.draw.polygon(scherm, HAAI_DONKER, vin_punten)

        # Oog
        pygame.draw.circle(scherm, ZWART, (x + 8, y + 10), 4)
        pygame.draw.circle(scherm, WIT, (x + 9, y + 9), 1)


# =========================================
# Gewone Haai (Subklasse)
#
# Beschrijving:
# Deze haai beweegt in een rechte lijn
# van rechts naar links over het scherm.
# Dit is de simpelste vorm van een vijand.
#
# Functionaliteiten:
# - Constante horizontale beweging
# - Willekeurige snelheid per haai

class GewoneHaai(Haai):
    """
    Een haai die rechtdoor zwemt van rechts naar links.
    >>> import random
    >>> random.seed(42)

    >>> haai = GewoneHaai()
    >>> isinstance(haai, Haai)
    True

    >>> haai.x == BREEDTE + 50
    True
    """

    def __init__(self):
        """
        Maak een gewone haai aan met vaste snelheid.
        >>> random.seed(42)
        >>> haai = GewoneHaai()
        >>> 2 <= haai.snelheid <= 4
        True
        """

        super().__init__()
        self.snelheid = random.uniform(2, 4)

    def beweeg(self):
        """
        Beweeg de haai rechtdoor naar links.

        >>> haai = GewoneHaai()
        >>> haai.snelheid = 3.0
        >>> start_x = haai.x
        >>> haai.beweeg()
        >>> haai.x == start_x - 3.0
        True
        >>> haai.beweeg()
        >>> haai.x == start_x - 6.0
        True
        """

        self.x -= self.snelheid


# =========================================
# Zigzag Haai (Subklasse)
#
# Beschrijving:
# Deze haai beweegt naar links terwijl hij
# een op-en-neer gaande (zigzag) beweging maakt.
#
# Functionaliteiten:
# - Horizontale beweging
# - Verticale golfbeweging (sinus-achtig)

class ZigzagHaai(Haai):
    """
    Een haai die zigzaggend beweegt.

    >>> import pygame
    >>> haai = ZigzagHaai()
    >>> haai.golf_amplitude == 60
    True

    >>> haai.hoek == 0
    True
    """

    def __init__(self):
        """
        Initialiseert de zigzaghaai met een startpositie en golf-instellingen.
        
        >>> haai = ZigzagHaai()
        >>> hasattr(haai, 'start_y')
        True

        >>> 1.5 <= haai.snelheid <= 3
        True
        """
        super().__init__()

        self.snelheid = random.uniform(1.5, 3)

        self.golf_amplitude = 60
        self.golf_snelheid = 0.05

        self.hoek = 0
        self.start_y = self.y

    def beweeg(self):
        """
        Beweeg de haai naar links en zigzaggend op en neer.
        
        >>> import pygame
        >>> haai = ZigzagHaai()
        >>> haai.x = 500

        >>> haai.snelheid = 2.0
        >>> haai.start_y = 200
        >>> haai.y = 200

        >>> haai.hoek = 0
        >>> haai.beweeg()
        >>> haai.x == 498.0
        True

        >>> round(haai.hoek, 2) == 0.05
        True

        >>> haai.y != 200
        True
        """

        self.x -= self.snelheid
        self.hoek += self.golf_snelheid

        self.y = self.start_y + self.golf_amplitude * pygame.math.Vector2(
            0, 1).rotate(self.hoek * 57.3).y
        

# =========================================
# Haai Factory
#
# Beschrijving:
# Maakt willekeurig een type haai aan.
# =========================================

def maak_haai():
    """
    Retourneert een willekeurige haai.
    
    >>> import random
    >>> random.seed(1) # Bij seed(1) is het eerste getal ~0.13
    >>> haai1 = maak_haai()

    >>> isinstance(haai1, GewoneHaai)
    True
    
    >>> random.seed(2)
    >>> haai2 = maak_haai()
    >>> isinstance(haai2, ZigzagHaai)
    True
    
    >>> isinstance(maak_haai(), Haai)
    True
    """

    if random.random() < 0.6:
        return GewoneHaai()
    
    return ZigzagHaai()

# =========================================
# Main Game Loop
#
# Verwerkt:
# - Input (toetsen)
# - Game logica (physics, spawning, collisions)
# - Rendering (tekenen van alles)
# =========================================

def main():
    """Start en beheert het spel
    
    >>> import pygame
    >>> import os
    >>> os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    >>> _ = pygame.init()
    >>> isinstance(pygame.time.Clock(), pygame.time.Clock)
    True
    """

    pygame.init()

    # Initialiseer geluid
    try:
        pygame.mixer.init(frequency=22050)
    except Exception:
        pass

    oppervlak = pygame.display.set_mode((BREEDTE, HOOGTE))
    pygame.display.set_caption("Flappy Vis")

    klok = pygame.time.Clock()

    # -----------------------------------------
    # Geluid laden / genereren
    # -----------------------------------------

    pop_pad = os.path.join(os.path.dirname(__file__), "pop.wav")

    if not os.path.exists(pop_pad):
        framerate = 22050
        duration = 0.12
        freq = 520.0
        amplitude = 13000

        nframes = int(duration * framerate)

        with wave.open(pop_pad, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(framerate)

            for i in range(nframes):
                t = i / framerate
                env = max(0.0, 1.0 - (t / duration))**2

                sample = amplitude * env * math.sin(2 * math.pi * freq * t)
                val = int(max(-32767, min(32767, sample)))

                wf.writeframes(struct.pack('<h', val))
    try:
        pop_sound = pygame.mixer.Sound(pop_pad)
    except Exception:
        pop_sound = None

    expl_pad = os.path.join(os.path.dirname(__file__), "explosion.wav")
    if not os.path.exists(expl_pad):
        framerate = 22050
        duration = 0.36
        amplitude = 19000

        nframes = int(duration * framerate)

        with wave.open(expl_pad, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(framerate)

            for i in range(nframes):
                t = i / framerate

                env = (1.0 - (t / duration))
                noise = random.uniform(-1.0, 1.0)
                tone = math.sin(2 * math.pi * 120.0 * t) * 0.5

                sample = amplitude * env * (0.6 * noise + 0.4 * tone)
                val = int(max(-32767, min(32767, sample)))

                wf.writeframes(struct.pack('<h', val))

    try:
        explosion_sound = pygame.mixer.Sound(expl_pad)
    except Exception:
        explosion_sound = None

    # -----------------------------------------
    # Game setup
    # -----------------------------------------

    vis = Vis()
    scherm = Scherm(oppervlak)

    riffen = []
    haaien = []

    laatste_rif = pygame.time.get_ticks()
    laatste_haai = pygame.time.get_ticks()

    gestart = False
    game_over = False
    dying = False

    explosie = None
    score = 0

    scherm.toon_startscherm()

    while True:
        # -----------------------------------------
        # Input verwerking
        # -----------------------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    if game_over:
                        vis.reset()
                        riffen = []
                        haaien = []
                        
                        laatste_rif = pygame.time.get_ticks()
                        laatste_haai = pygame.time.get_ticks()

                        game_over = False
                        dying = False
                        explosie = None
                        gestart = True
                        score = 0

                    elif not gestart:
                        gestart = True

                    else:
                        vis.spring()

                        if pop_sound:
                            try:
                                pop_sound.play()
                            except Exception:
                                pass

        # ---------------------------------
        # Game update (physics & logic)
        # ---------------------------------

        # Alleen updaten wanneer spel actief is (niet in start- of game-over toestand)
        if gestart and not game_over:
            vis.beweeg()

            nu = pygame.time.get_ticks()

            # ---------------------------------
            # Spawning
            # ---------------------------------

            # Verhoog moeilijkheid: hoe hoger de score, hoe sneller nieuwe riffen verschijnen
            # Minimum van 800 ms voorkomt dat het spel onspeelbaar snel wordt
            rif_interval = max(800, RIF_INTERVAL - score * 20)

            if nu - laatste_rif > rif_interval:
                # Laat riffen sneller bewegen naarmate de score stijgt (moeilijkheid scaling)
                huidige_snelheid = RIF_SNELHEID + score * 0.1
                riffen.append(Koraalrif(snelheid=huidige_snelheid))
                laatste_rif = nu

            if nu - laatste_haai > HAAI_INTERVAL:
                haaien.append(maak_haai())
                laatste_haai = nu

            # ---------------------------------
            # Object updates (beweging & cleanup)
            # ---------------------------------
            for rif in riffen:
                rif.beweeg()

            riffen = [rif for rif in riffen if not rif.is_buiten_scherm()]

            for haai in haaien:
                haai.beweeg()
            haaien = [haai for haai in haaien if not haai.is_buiten_scherm()]

            # Verhoog score wanneer de vis succesvol een rif voorbij zwemt
            for rif in riffen:
                if not rif.gepasseerd and rif.x + RIF_BREEDTE < vis.x:
                    score += 1
                    rif.gepasseerd = True

            # Controleer botsingen
            geraakt = (vis.is_buiten_scherm() or
                       any(rif.raakt_vis(vis) for rif in riffen) or
                       any(haai.raakt_vis(vis) for haai in haaien))
            
            # ---------------------------------
            # Dying / explosie
            # ---------------------------------
            
            if geraakt and not dying and not game_over:
                dying = True
                explosie = Explosie(vis.x, vis.y)

                if explosion_sound:
                    try:
                        explosion_sound.play()
                    except Exception:
                        pass

            if dying:
                vis.snelheid = 0

                scene = pygame.Surface((BREEDTE, HOOGTE))

                scherm.toon_spel(vis, 
                                 riffen, 
                                 haaien, 
                                 draw_vis=False, 
                                 score=score, 
                                 target=scene)
                
                if explosie:
                    explosie.teken(scene)
                    explosie.update()

                if explosie:
                    # Bepaal progressie van de explosie (0 → 1)
                    prog = min(1.0, explosie.frame / max(1, explosie.flash_life))

                    # Screen shake neemt af naarmate explosie vordert
                    amp = int(18 * (1.0 - prog))

                else:
                    amp = 0

                if amp > 0:
                    # Willekeurige offset voor screen shake effect
                    ox = random.randint(-amp, amp)
                    oy = random.randint(-amp, amp)

                else:
                    ox = oy = 0

                oppervlak.fill((0, 0, 0))
                oppervlak.blit(scene, (ox, oy))
                
                pygame.display.flip()

                if explosie and explosie.finished:
                    dying = False
                    game_over = True
                    scherm.toon_game_over(score)

            # -------------------------------
            # RENDERING
            # -------------------------------

            else:
                scherm.toon_spel(vis, riffen, haaien, score=score)

        klok.tick(FPS)


if __name__ == "__main__":
    main()
