import pygame
import sys
import random

# Scherm instellingen
BREEDTE = 800
HOOGTE = 600
FPS = 60

# Kleuren
OCEAAN_BLAUW = (0, 105, 148)
ORANJE = (255, 165, 0)
DONKER_ORANJE = (255, 140, 0)
WIT = (255, 255, 255)
ZWART = (0, 0, 0)
ROOD = (255, 0, 0)
GRIJS = (200, 200, 200)
DONKER_ROOD = (200, 80, 0)

# Vis instellingen
VIS_BREEDTE = 45
VIS_HOOGTE = 28
VIS_X = 150
ZWAARTEKRACHT = 0.5
SPRONG_KRACHT = -8


# Koraalrif instellingen
RIF_BREEDTE = 80
RIF_GAT_HOOGTE = 180
RIF_SNELHEID = 4
RIF_INTERVAL = 1800  # milliseconden tussen riffen

KORAAL_ROOD = (255, 69, 0)
KORAAL_DONKER = (200, 50, 0)

# Haai instellingen
HAAI_GRIJS = (150, 150, 160)
HAAI_DONKER = (100, 100, 110)
HAAI_WIT = (240, 240, 240)
HAAI_INTERVAL = 3000  # milliseconden tussen haaien




class Koraalrif:
    """Een obstakel bestaande uit twee koraalstukken met een gat ertussen."""

    def __init__(self):
        """Maakt een nieuw koraalrif aan aan de rechterkant van het scherm."""
        self.x = BREEDTE
        self.snelheid = RIF_SNELHEID
        gat_midden = random.randint(150, HOOGTE - 150)
        self.gat_boven = gat_midden - RIF_GAT_HOOGTE // 2
        self.gat_onder = gat_midden + RIF_GAT_HOOGTE // 2

    def beweeg(self):
        """Beweegt het rif naar links."""
        self.x -= self.snelheid

    def is_buiten_scherm(self):
        """Geeft True terug als het rif links van het scherm is."""
        return self.x + RIF_BREEDTE < 0

    def raakt_vis(self, vis):
        """Geeft True terug als de vis het rif raakt."""
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


class Vis:
    """De speler, beweegt omhoog en omlaag door de oceaan."""

    def __init__(self):
        """Maakt een nieuwe vis aan in het midden van het scherm."""
        self.x = VIS_X
        self.y = HOOGTE // 2
        self.snelheid = 0

    def reset(self):
        """Zet de vis terug naar de beginpositie."""
        self.y = HOOGTE // 2
        self.snelheid = 0

    def beweeg(self):
        """Past zwaartekracht toe en beweegt de vis."""
        self.snelheid += ZWAARTEKRACHT
        self.y += self.snelheid

    def spring(self):
        """Laat de vis omhoog bewegen."""
        self.snelheid = SPRONG_KRACHT

    def is_buiten_scherm(self):
        """Geef True terug als de vis buiten het scherm is."""
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
        """Tekent het oog van de vis."""
        x, y = self.x, int(self.y)
        pygame.draw.circle(scherm, WIT, (x + 33, y + 10), 6)
        pygame.draw.circle(scherm, ZWART, (x + 34, y + 11), 3)
        pygame.draw.circle(scherm, WIT, (x + 35, y + 9), 1)

    def _teken_mond(self, scherm):
        """Tekent de mond van de vis."""
        x, y = self.x, int(self.y)
        pygame.draw.arc(scherm, DONKER_ROOD,
                        (x + 38, y + 14, 10, 8), 3.14, 2 * 3.14, 2)


class Scherm:
    """De schermweergaven zoals startscherm en game over."""

    def __init__(self, oppervlak):
        """Initialiseer met het pygame oppervlak."""
        self.oppervlak = oppervlak
        self.font_groot = pygame.font.SysFont(None, 72)
        self.font_klein = pygame.font.SysFont(None, 36)

    def _teken_tekst_gecentreerd(self, tekst, font, kleur, y_offset):
        """Tekent gecentreerde tekst op gegeven hoogte."""
        render = font.render(tekst, True, kleur)
        x = BREEDTE // 2 - render.get_width() // 2
        self.oppervlak.blit(render, (x, HOOGTE // 2 + y_offset))

    def toon_startscherm(self):
        """Toont het startscherm met titel en instructie."""
        self.oppervlak.fill(OCEAAN_BLAUW)
        self._teken_tekst_gecentreerd("Flappy Vis!", self.font_groot, WIT, -60)
        self._teken_tekst_gecentreerd("Druk op SPATIE om te beginnen",
                                      self.font_klein, GRIJS, 20)
        pygame.display.flip()

    def toon_game_over(self):
        """Toont het game over scherm met herstart instructie."""
        self._teken_tekst_gecentreerd("Game Over!", self.font_groot, ROOD, -40)
        self._teken_tekst_gecentreerd("Druk op SPATIE om opnieuw te spelen",
                                      self.font_klein, GRIJS, 30)
        pygame.display.flip()

    def toon_spel(self, vis, riffen=[]):
        """Tekent het spelscherm met achtergrond, riffen en vis."""
        self.oppervlak.fill(OCEAAN_BLAUW)
        for rif in riffen:
            rif.teken(self.oppervlak)
        vis.teken(self.oppervlak)
        pygame.display.flip()


class Haai:
    """Basisklasse voor alle haaien."""

    def __init__(self):
        """Maak een nieuwe haai aan aan de rechterkant van het scherm."""
        self.x = BREEDTE + 50
        self.y = random.randint(50, HOOGTE - 50)
        self.breedte = 60
        self.hoogte = 30

    def beweeg(self):
        """Moet worden geïmplementeerd door subklassen."""
        raise NotImplementedError

    def is_buiten_scherm(self):
        """Geef True terug als de haai links van het scherm is."""
        return self.x + self.breedte < 0

    def raakt_vis(self, vis):
        """Geef True terug als de haai de vis raakt."""
        return (vis.x < self.x + self.breedte and
                vis.x + VIS_BREEDTE > self.x and
                vis.y < self.y + self.hoogte and
                vis.y + VIS_HOOGTE > self.y)

    def teken(self, scherm):
        """Teken de haai op het scherm."""
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


class GewoneHaai(Haai):
    """Een haai die rechtdoor zwemt van rechts naar links."""

    def __init__(self):
        """Maak een gewone haai aan met vaste snelheid."""
        super().__init__()
        self.snelheid = random.uniform(2, 4)

    def beweeg(self):
        """Beweeg de haai rechtdoor naar links."""
        self.x -= self.snelheid


class ZigzagHaai(Haai):
    """Een haai die zigzaggend beweegt."""

    def __init__(self):
        """Maak een zigzag haai aan."""
        super().__init__()
        self.snelheid = random.uniform(1.5, 3)
        self.golf_amplitude = 60
        self.golf_snelheid = 0.05
        self.hoek = 0
        self.start_y = self.y

    def beweeg(self):
        """Beweeg de haai naar links en zigzaggend op en neer."""
        self.x -= self.snelheid
        self.hoek += self.golf_snelheid
        self.y = self.start_y + self.golf_amplitude * pygame.math.Vector2(
            0, 1).rotate(self.hoek * 57.3).y
        

def main():
    """Start en beheert het spel"""
    pygame.init()
    oppervlak = pygame.display.set_mode((BREEDTE, HOOGTE))
    pygame.display.set_caption("Flappy Vis")
    klok = pygame.time.Clock()

    vis = Vis()
    scherm = Scherm(oppervlak)
    riffen = []
    haaien = []
    laatste_rif = pygame.time.get_ticks()
    laatste_haai = pygame.time.get_ticks()
    gestart = False
    game_over = False

    scherm.toon_startscherm()

    while True:
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
                        gestart = True
                    elif not gestart:
                        gestart = True
                    else:
                        vis.spring()

        if gestart and not game_over:
            vis.beweeg()

            # Voeg nieuw rif toe
            nu = pygame.time.get_ticks()
            if nu - laatste_rif > RIF_INTERVAL:
                riffen.append(Koraalrif())
                laatste_rif = nu

            # Voeg nieuwe haai toe
            if nu - laatste_haai > HAAI_INTERVAL:
                haaien.append(maak_haai())
                laatste_haai = nu

            # Beweeg en verwijder riffen
            for rif in riffen:
                rif.beweeg()
            riffen = [rif for rif in riffen if not rif.is_buiten_scherm()]

            # Beweeg en verwijder haaien
            for haai in haaien:
                haai.beweeg()
            haaien = [haai for haai in haaien if not haai.is_buiten_scherm()]

            # Controleer botsingen
            geraakt = (vis.is_buiten_scherm() or
                       any(rif.raakt_vis(vis) for rif in riffen) or
                       any(haai.raakt_vis(vis) for haai in haaien))

            if geraakt:
                game_over = True
                scherm.toon_spel(vis, riffen, haaien)
                scherm.toon_game_over()
            else:
                scherm.toon_spel(vis, riffen, haaien)

        klok.tick(FPS)


if __name__ == "__main__":
    main()