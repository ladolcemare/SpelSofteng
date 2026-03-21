# 🐟 Flappy Vis
Een Nederlandstalig door Flappy-bird geïnspireerd spel gemaakt met Pygame, gesitueerd in een onderwaterwereld. Stuur je vis door koraalriffen heen terwijl je haaien ontwijkt!

## Gameplay
Druk op **SPATIE** om de vis omhoog te laten zwemmen. Zwaartekracht trekt hem weer naar beneden. Navigeer door de gaten in de koraalriffen zonder de wanden, het koraal of haaien te raken.

## Bediening

| Toets | Actie |
|-------|-------|
| `SPATIE` | Spel starten / omhoog zwemmen |
| `SPATIE` | Opnieuw spelen na game over |

## Obstakels

- **Koraalriffen** — Verticale barrières met een willekeurig gat om doorheen te zwemmen
- **Gewone haaien** — Zwemmen rechtdoor van rechts naar links met wisselende snelheid
- **Zigzaghaaien** — Bewegen in een golfpatroon, waardoor ze moeilijker te ontwijken zijn

## Installatie

**Vereisten:** Python 3 en Pygame

Windows: 
```bash
pip install pygame
python flappy_vis.py
```

Mac: 
```bash
pip3 install pygame
python3 flappy_vis.py
```



## Projectstructuur

| Klasse | Beschrijving |
|--------|--------------|
| `Vis` | De spelervis — beweging, springen en weergave |
| `Koraalrif` | Koraalrif-obstakel met een willekeurige gatpositie |
| `Haai` | Basisklasse voor alle haaien |
| `GewoneHaai` | Rechtdoor zwemmende haai |
| `ZigzagHaai` | Haai met golfpatroon |
| `Scherm` | Beheert alle schermweergaven (start, spel, game over) |

## Configuratie

De constanten bovenaan het bestand kunnen worden aangepast om de moeilijkheidsgraad te wijzigen:

| Constante | Standaard | Effect |
|-----------|-----------|--------|
| `RIF_GAT_HOOGTE` | `180` | Grootte van het gat in de koraalriffen |
| `RIF_SNELHEID` | `4` | Hoe snel de riffen naar links scrollen |
| `RIF_INTERVAL` | `1800ms` | Tijd tussen nieuwe riffen |
| `HAAI_INTERVAL` | `3000ms` | Tijd tussen nieuwe haaien |
| `ZWAARTEKRACHT` | `0.5` | Neerwaartse kracht op de vis |
| `SPRONG_KRACHT` | `-8` | Opwaartse kracht bij een sprong |

## Bekende problemen

- `maak_haai()` wordt aangeroepen in `main()` maar is niet gedefinieerd in de broncode — voeg deze functie toe voordat je het spel start.
