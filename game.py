import pygame
import sys
import random
import math
import os
import wave
import struct

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

    def __init__(self, snelheid=RIF_SNELHEID):  
        """Maakt een nieuw koraalrif aan aan de rechterkant van het scherm."""
        self.x = BREEDTE
        self.snelheid = snelheid
        gat_midden = random.randint(150, HOOGTE - 150)
        self.gat_boven = gat_midden - RIF_GAT_HOOGTE // 2
        self.gat_onder = gat_midden + RIF_GAT_HOOGTE // 2
        self.gepasseerd = False  

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


class Explosie:
    """Particle-based explosie special effect.

    Genereert meerdere deeltjes met velocity, life en fade-out.
    Tekent een korte flits en de deeltjes met alpha.
    """

    def __init__(self, x, y, count=48):
        self.x = x + VIS_BREEDTE // 2
        self.y = y + VIS_HOOGTE // 2
        self.frame = 0
        self.finished = False
        self.particles = []
        self.flash_life = 14

        kleuren = [ORANJE, ROOD, DONKER_ORANJE, (255, 220, 120)]
        for _ in range(count):
            # verstrooi de startpositie over het rechthoek van de vis
            start_x = random.uniform(x, x + VIS_BREEDTE)
            start_y = random.uniform(y, y + VIS_HOOGTE)
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

        # used to track if sound already played for this explosion
        self.sound_played = False

    def update(self):
        self.frame += 1
        for p in self.particles:
            p["vel"].y += 0.18  # lichte zwaartekracht
            p["pos"] += p["vel"]
            p["life"] -= 1
        # verwijder dode deeltjes
        self.particles = [p for p in self.particles if p["life"] > 0]
        if self.frame > self.flash_life and not self.particles:
            self.finished = True

    def teken(self, scherm):
        # overlay voor flits + deeltjes met alpha
        overlay = pygame.Surface((BREEDTE, HOOGTE), pygame.SRCALPHA)

        # flits in het midden (groeit en vervaagt snel)
        if self.frame <= self.flash_life:
            progress = self.frame / max(1, self.flash_life)
            alpha = int(220 * (1 - progress))
            radius = int(60 + 120 * progress)
            pygame.draw.circle(overlay, (255, 250, 230, alpha),
                               (int(self.x), int(self.y)), radius)

        # teken deeltjes
        for p in self.particles:
            life_frac = p["life"] / p["max_life"]
            alpha = int(255 * max(0, life_frac))
            col = (*p["c"][:3], alpha) if len(p["c"]) == 3 else (*p["c"], alpha)
            pygame.draw.circle(overlay, col,
                               (int(p["pos"].x), int(p["pos"].y)), p["r"])

        scherm.blit(overlay, (0, 0))


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

    def toon_game_over(self, score=0):  # score parameter toegevoegd
        """Toont het game over scherm met score en herstart instructie."""
        self._teken_tekst_gecentreerd("Game Over!", self.font_groot, ROOD, -60)
        score_tekst = self.font_klein.render(f"Score: {score}", True, WIT)  
        x = BREEDTE // 2 - score_tekst.get_width() // 2
        self.oppervlak.blit(score_tekst, (x, HOOGTE // 2))
        self._teken_tekst_gecentreerd("Druk op SPATIE om opnieuw te spelen",
                                      self.font_klein, GRIJS, 50)
        pygame.display.flip()

    def toon_spel(self, vis, riffen=None, haaien=None, draw_vis=True, score=0, target=None):
        """Tekent het spelscherm met achtergrond, riffen, vis en haaien.

        Gebruik `None` als default om mutability van lijsten te vermijden.
        Als `target` wordt meegegeven, renderen we naar dat oppervlak en
        retourneren het — anders wordt direct naar het hoofdscherm geflipt.
        """
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

def maak_haai():
    """Factory: retourneer een willekeurige haai instantie.

    Dit voorkomt een NameError in de game loop.
    """
    if random.random() < 0.6:
        return GewoneHaai()
    return ZigzagHaai()

def main():
    """Start en beheert het spel"""
    pygame.init()
    # zorg dat mixer klaar is en maak laad geluid
    try:
        pygame.mixer.init(frequency=22050)
    except Exception:
        pass
    oppervlak = pygame.display.set_mode((BREEDTE, HOOGTE))
    pygame.display.set_caption("Flappy Vis")
    klok = pygame.time.Clock()

    # laad of maak kort 'pop' geluid (voor springen)
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

    # laad of maak explosie geluid (sterker, ruis-achtige burst)
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
                # korte ruis-burst met lage frequentie flutter
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

        if gestart and not game_over:
            vis.beweeg()

            nu = pygame.time.get_ticks()

            # Voeg nieuw rif toe (interval wordt korter naarmate score stijgt)
            rif_interval = max(800, RIF_INTERVAL - score * 20)
            if nu - laatste_rif > rif_interval:
                huidige_snelheid = RIF_SNELHEID + score * 0.1
                riffen.append(Koraalrif(snelheid=huidige_snelheid))
                laatste_rif = nu

            # Voeg nieuwe haai toe
            if nu - laatste_haai > HAAI_INTERVAL:
                haaien.append(maak_haai())
                laatste_haai = nu

            # Beweeg riffen
            for rif in riffen:
                rif.beweeg()

            # verwijder riffen buiten scherm
            riffen = [rif for rif in riffen if not rif.is_buiten_scherm()]

            # Beweeg en verwijder haaien
            for haai in haaien:
                haai.beweeg()
            haaien = [haai for haai in haaien if not haai.is_buiten_scherm()]

            # Puntentelling: +1 voor elk rif dat de vis passeert
            for rif in riffen:
                if not rif.gepasseerd and rif.x + RIF_BREEDTE < vis.x:
                    score += 1
                    rif.gepasseerd = True

            # Controleer botsingen
            geraakt = (vis.is_buiten_scherm() or
                       any(rif.raakt_vis(vis) for rif in riffen) or
                       any(haai.raakt_vis(vis) for haai in haaien))

            # Start explosie wanneer geraakt (als nog niet bezig)
            if geraakt and not dying and not game_over:
                dying = True
                explosie = Explosie(vis.x, vis.y)
                # speel explosie geluid één keer
                if explosion_sound:
                    try:
                        explosion_sound.play()
                    except Exception:
                        pass

            if dying:
                # voorkom verder bewegen van de vis tijdens explosie
                vis.snelheid = 0
                # render eerst naar een tussenoppervlak
                scene = pygame.Surface((BREEDTE, HOOGTE))
                scherm.toon_spel(vis, riffen, haaien, draw_vis=False, score=score, target=scene)
                if explosie:
                    explosie.teken(scene)
                    explosie.update()

                # bereken schermschud amplitude op basis van explosie progress
                if explosie:
                    prog = min(1.0, explosie.frame / max(1, explosie.flash_life))
                    amp = int(18 * (1.0 - prog))
                else:
                    amp = 0
                if amp > 0:
                    ox = random.randint(-amp, amp)
                    oy = random.randint(-amp, amp)
                else:
                    ox = oy = 0

                # blit scene naar hoofdscherm met offset (schud-effect)
                oppervlak.fill((0, 0, 0))
                oppervlak.blit(scene, (ox, oy))
                pygame.display.flip()

                if explosie and explosie.finished:
                    dying = False
                    game_over = True
                    scherm.toon_game_over(score)
            else:
                scherm.toon_spel(vis, riffen, haaien, score=score)

        klok.tick(FPS)


if __name__ == "__main__":
    main()
