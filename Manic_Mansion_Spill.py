# Importerer nyttige biblioteker
import pygame as pg
import random as rd

# Konstanter
BREDDE = 500  # Bredden til vinduet
HOYDE = 400  # Høyden til vinduet

# Størrelsen til vinduet
STORRELSE = (BREDDE, HOYDE)

# Ulike størrelser i spillet
x = int(round(BREDDE / 5))
y = 0
w = x * 3
h = HOYDE
BREDDE_FIGUR = 20

# Farger
SVART = (0, 0, 0)
GRA = (200, 200, 200)
HVIT = (255, 255, 255)
GRONN = (125, 175, 90)
BLA = (50, 50, 255)
LYSGRA = (50, 50, 50)
ROD = (240, 80, 80)

# Frames Per Second (bilder per sekund)
FPS = 120

# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
overflate = pg.display.set_mode(STORRELSE)

# Lager en klokke
klokke = pg.time.Clock()

# Setter spill_i_gang som True slik at spillet kjøres 
spill_i_gang = True

# Funksjon som skriver tekst til vinduet
def tegnTekst(tekst, x, y, farge, fontStorrelse):
    font = pg.font.SysFont("Arial", fontStorrelse)
    tekstBilde = font.render(tekst, True, farge)
    tekstRektangel = tekstBilde.get_rect()
    
    # Putter i vinduet
    overflate.blit(tekstBilde, (x - tekstRektangel.width//2, y - tekstRektangel.height//2))
    
# Funskjon som sjekker om ulike objekter overalapper hverandre når de lages    
def sjekkOverlapp(x1, y1, objektliste):
    for objekt in objektliste:
        if abs(x1 - objekt.xPosisjon) <= BREDDE_FIGUR and abs(y1 - objekt.yPosisjon) <= BREDDE_FIGUR:
            return True
    return False

# Lager en klasse for selve spillbrettet   
class Spillbrett:
    # Lager en objektliste, definierer høyde og bredde og lager en variabel for poeng i konstruktøren
    def __init__(self, hoyde, bredde):
        self.hoyde = hoyde
        self.bredde = bredde
        self.objekter = []
        self.poeng = 0
    
    # Legger til objekter i objektlisten og sjekker om det siste objektet som ble lagt til overlapper med tidliger lagt til objekter
    def leggTilObjekt(self, SpillObjekt):
        # Sjekk for overlapp før du legger til objektet
        while sjekkOverlapp(SpillObjekt.xPosisjon, SpillObjekt.yPosisjon, self.objekter):
            if isinstance(SpillObjekt, Sau):
                SpillObjekt.xPosisjon = rd.randint(BREDDE - int(BREDDE / 5), BREDDE - BREDDE_FIGUR)
                SpillObjekt.yPosisjon = rd.randint(0, HOYDE - BREDDE_FIGUR)
            if isinstance(SpillObjekt, Hindring):
                SpillObjekt.xPosisjon = rd.randint(x, BREDDE - x - BREDDE_FIGUR)
                SpillObjekt.yPosisjon = rd.randint(0, HOYDE - BREDDE_FIGUR)
                
        self.objekter.append(SpillObjekt)
    
    # Fjerner et objekt fra objektlisten
    def fjernObjekt(self, SpillObjekt):
        self.objekter.remove(SpillObjekt)
    
    # La til en metode som tegner alle objektene i listen på overflaten
    def tegnObjekter(self):
        for objekt in self.objekter:
            pg.draw.rect(overflate, objekt.farge, pg.Rect(objekt.xPosisjon, objekt.yPosisjon, objekt.w, objekt.h),)
    
    # La til en metode som gjør at brettet oppdateres
    def oppdater(self):
        spillbrett.tegnObjekter() 
        menneske.sjekkeTastatur()
        menneske.sjekkKollisjon(spillbrett)
        menneske.sjekkKollisjonHindring(menneske.xPosisjon, menneske.yPosisjon)
        spokelse.plassering()
        spokelse.endreRetning()
            
        
# Lager en spillobjektklasse som er superklasse til andre klasser
class SpillObjekt:
    def __init__(self, xPosisjon, yPosisjon):
        self.xPosisjon = xPosisjon
        self.yPosisjon = yPosisjon
        # Alle objektene har lik størrelse, la derfor til bredde og høyde på firkantene
        self.w = BREDDE_FIGUR
        self.h = BREDDE_FIGUR
        
# Lager en sub-klasse menneske
class Menneske(SpillObjekt):
    # La til fargen på menneskeobjektet i konstruktøren
    def __init__(self, baererSau=False, fart=2):
        super().__init__(BREDDE/10, HOYDE/2)
        self.baererSau = False
        self.fart = fart
        self.farge = BLA
    
    # Sjekker tastaturtrykk og beveger spilleren, hvis den ikke har kollidert med en hindring
    def sjekkeTastatur(self):
        taster = pg.key.get_pressed()
        
        if taster[pg.K_UP]:
            if not self.sjekkKollisjonHindring(self.xPosisjon, self.yPosisjon - self.fart):
                self.yPosisjon -= self.fart
        if taster[pg.K_DOWN]:
            if not self.sjekkKollisjonHindring(self.xPosisjon, self.yPosisjon + self.fart):
                self.yPosisjon += self.fart
        if taster[pg.K_RIGHT]:
            if not self.sjekkKollisjonHindring(self.xPosisjon + self.fart, self.yPosisjon):
                self.xPosisjon += self.fart
        if taster[pg.K_LEFT]:
            if not self.sjekkKollisjonHindring(self.xPosisjon - self.fart, self.yPosisjon):
                self.xPosisjon -= self.fart
    
    # En metode som sjekker kollisjon med vegg eller spøkelse
    def sjekkKollisjon(self, spillbrett):      
        if self.xPosisjon <= 0: 
            self.xPosisjon = 0
        if self.xPosisjon + BREDDE_FIGUR >= BREDDE:
            self.xPosisjon = BREDDE - BREDDE_FIGUR
        if self.yPosisjon <= 0:
            self.yPosisjon = 0
        if self.yPosisjon + BREDDE_FIGUR >= HOYDE:
            self.yPosisjon = HOYDE - BREDDE_FIGUR
        
        # Iterer gjennom alle spillobjekter og hvis de er spøkelser så sjekkes en kollisjon
        for s in spillbrett.objekter:
            if isinstance(s, Spokelse):
                if abs(s.xPosisjon - self.xPosisjon) <= BREDDE_FIGUR and abs(s.yPosisjon - self.yPosisjon) <= BREDDE_FIGUR:
                    #spill_i_gang = False
                    #break
                    pg.quit()
                
            
    # La til en metode som sjekker kollisjon med hindring
    def sjekkKollisjonHindring(self, xPosisjon, yPosisjon):
        for h in spillbrett.objekter:
            if isinstance(h, Hindring):
                if (h.xPosisjon < xPosisjon < h.xPosisjon + BREDDE_FIGUR or h.xPosisjon < xPosisjon + BREDDE_FIGUR < h.xPosisjon + BREDDE_FIGUR) and (h.yPosisjon < yPosisjon < h.yPosisjon + BREDDE_FIGUR or h.yPosisjon < yPosisjon + BREDDE_FIGUR < h.yPosisjon + BREDDE_FIGUR):
                    return True
        return False
    
    # En metode med variabler som skal endres når spiller bærer sau
    def bærSau(self, sau):
        self.baererSau = True
        self.farge = HVIT
        menneske.fart = 1.2
        sau.blirLoftet()     
        
# Lager en sub-klasse spøkelse      
class Spokelse(SpillObjekt):
    # I kontruktøren gis spøkelsene en farge og retning og fart blir tilfeldig
    def __init__(self):
        super().__init__(rd.randint(x, BREDDE - x - BREDDE_FIGUR), rd.randint(0, HOYDE - BREDDE_FIGUR))
        self.farge = LYSGRA
        self.vx = rd.uniform(-1, 1)
        self.vy = rd.uniform(-1, 1)
    
    # En metode som iterer seg gjennom spøkelsene og beveger dem
    def plassering(self):
        for s in spillbrett.objekter:
            if isinstance(s, Spokelse):
                s.xPosisjon = s.xPosisjon + s.vx
                s.yPosisjon = s.yPosisjon + s.vy
    
    # En metode som endrer retningene til spøkelsene ved en kollisjon
    def endreRetning(self):
        for s in spillbrett.objekter:
            if isinstance(s, Spokelse):
                s.xPosisjon += s.vx
                s.yPosisjon += s.vy
                if s.xPosisjon <= x or s.xPosisjon + BREDDE_FIGUR >= BREDDE - x: 
                    s.vx *= -1
                elif s.yPosisjon <= 0 or s.yPosisjon + BREDDE_FIGUR >= HOYDE:
                    s.vy *= -1

# Lager en sub-klasse hindring  
class Hindring(SpillObjekt):
    # I kontruktøren gis spøkelsene en farge i tillegg til tilfeldig plassering på angitt område på brettet
    def __init__(self):
        super().__init__(rd.randint(x, BREDDE - x - BREDDE_FIGUR), rd.randint(0, HOYDE - BREDDE_FIGUR))
        self.farge = ROD

# Lager en sub-klasse sau  
class Sau(SpillObjekt):
    # I kontruktøren gis spøkelsene en farge i tillegg til tilfeldig plassering på angitt område på brettet
    def __init__(self):
        super().__init__(rd.randint(BREDDE - int(BREDDE / 5), BREDDE - BREDDE_FIGUR), rd.randint(0, HOYDE - BREDDE_FIGUR))
        self.farge = HVIT
    
    # En metode som gjør at sauen følger med mennesker når den blir plukket opp
    def blirLoftet(self):
        self.xPosisjon = menneske.xPosisjon
        self.yPosisjon = menneske.yPosisjon

# Lager ulike objekter som brukes i spillet
spillbrett = Spillbrett(HOYDE, BREDDE)

sauer = []
# De førse 3 saueobjektene legges inn i liste
for i in range(3):
    sau = Sau()
    spillbrett.leggTilObjekt(sau)
    sauer.append(sau)

menneske = Menneske()
spillbrett.leggTilObjekt(menneske)

hindringer = []
# De førse 3 hindringsobjektene legges inn i liste
for i in range(3):
    hindring = Hindring()
    spillbrett.leggTilObjekt(hindring)
    hindringer.append(hindring)

spokelse = Spokelse()
spillbrett.leggTilObjekt(spokelse)

# Kjører programmet
while spill_i_gang:
    klokke.tick(FPS)
    
    # Tegner spillbrettts utseende
    overflate.fill(GRA)
    pg.draw.rect(overflate, GRONN, pg.Rect(x, y, w, h))
    
    spillbrett.oppdater()
    
    # Sjekker kollisjon med menneske og sau hvis ikke menneske allerede "bærer" en sau
    for s in spillbrett.objekter:
        if isinstance(s, Sau) and abs(s.xPosisjon - menneske.xPosisjon) <= BREDDE_FIGUR and abs(s.yPosisjon - menneske.yPosisjon) <= BREDDE_FIGUR:
            if not menneske.baererSau:
                menneske.bærSau(s)
                spillbrett.fjernObjekt(s)
                break
            else:
                # Hvis kollisjon med sau imens en bærer sau stopper spillet
                spill_i_gang = False
    
    # Sjekker om en har klart å hente en sau over til mål
    if menneske.xPosisjon < x - BREDDE_FIGUR and menneske.baererSau:
        menneske.baererSau = False
        menneske.fart = 2
        menneske.farge = BLA
        spillbrett.poeng += 1
        
        # Nye objekter lages og legges inn i objektlisten
        ny_sau = Sau()
        spillbrett.leggTilObjekt(ny_sau)
        
        ny_hindring = Hindring()
        spillbrett.leggTilObjekt(ny_hindring)
        
        ny_spokelse = Spokelse()
        spillbrett.leggTilObjekt(ny_spokelse)   
    
    # Skriver ut antall sauer en har fanget til skjermen ved bruk av en funksjon
    tegnTekst(f"Antall sauer: {spillbrett.poeng}", BREDDE//2, HOYDE//5, SVART, 25)   
    
    # Sjekker om spiller ønsker å avslutte spillet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            spill_i_gang = False

    # "Snur" alle endringene til skjermen
    pg.display.flip()

# Lukker vinduet
pg.quit()