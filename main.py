import pygame
from pygame.locals import *
import random
#inicializace
pygame.init()
#Okno
šířka_okna = 600
výška_okna = 600
okno = pygame.display.set_mode((šířka_okna, výška_okna))
pygame.display.set_caption("Snake")

kliknuto = False

velikost_blocku = 25#pixely na jednen block ve hře
směr = 1#1 je nahoru, 2 vpravo, 3 dolu a 4 vlevo
#score
score = 0
konec_hry = False
#Snake
update_snake = 0
pozice_hada = [[int(šířka_okna / 2), int(výška_okna / 2)]]#list pozic blocků + přidání prvního blocku
pozice_hada.append([int(šířka_okna / 2), int(výška_okna / 2) + velikost_blocku])#Druhý block
pozice_hada.append([int(šířka_okna / 2), int(výška_okna / 2) + velikost_blocku * 2])#Třetí block
pozice_hada.append([int(šířka_okna / 2), int(výška_okna / 2) + velikost_blocku * 3])#Čtvrtý block
#jídlo
jidlo = [0, 0]
nove_jidlo = True
prodlouzeny_block = [0, 0]
#font
font = pygame.font.SysFont(None, 40)
#Barvy
bg = (0, 0, 0)
body_inner = (255, 255, 255)
outline = (100, 100, 200)
modra = (0, 0, 255)
barva_jidla = (200, 50, 50)
#Rect pro Další pokus
tlačítko = Rect(šířka_okna // 2 - 90, výška_okna // 2, 180, 45)
#Funkce
def vykreslení_okna():
    okno.fill(bg)
def vykreslení_score():
    text = f"Skóre: {score}"
    skóre = font.render(text, True, (255,255,51))
    okno.blit(skóre, ((šířka_okna * 0.42), 3))
def kontrola_konce_hry(konec_hry):
    #Kontrola kolize hada s jeho tělem
    cislo_blocku = 0
    for segment in pozice_hada:
        if pozice_hada[0] == segment and cislo_blocku > 0: #Vynechá hlavu
            konec_hry = True #kolize hlavy s ostatními částmi
        cislo_blocku += 1
    #kontrola jestli je had mimo pole
    if pozice_hada[0][0] < 0  or pozice_hada[0][0] > šířka_okna - velikost_blocku or pozice_hada[0][1] < 0 or pozice_hada[0][1] > výška_okna - velikost_blocku:
        konec_hry = True
    return konec_hry
def vykresleni_konce_hry():
    konec = "! Konec hry !"
    konec = font.render(konec, True, (255, 255, 255))
    pygame.draw.rect(okno, (255, 0, 0), (šířka_okna // 2 - 100, výška_okna // 2 - 70, 200, 50), 2, 3)
    okno.blit(konec, (šířka_okna // 2 - 85, výška_okna // 2 - 58))
    znovu = "Hrát znovu?"
    znovu = font.render(znovu, True, (255, 255, 255))
    pygame.draw.rect(okno, (255, 0, 0), tlačítko, 2, 3)
    okno.blit(znovu, (šířka_okna // 2 - 80, výška_okna // 2 + 10))
#Main loop
run = True
prohra = 0
while run:
    vykreslení_okna()
    vykreslení_score()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and směr != 3:#Pokud stiskneme W a proměnná směr není 3, což by znamenalo že had se pohybuje směrem dolu, tak se změní proměnná směr na 1, což znamená, že pojede nahoru
                směr = 1
            if event.key == pygame.K_d and směr != 4:#Pokud stiskneme D a proměnná směr není 4, což by znamenalo že had se pohybuje směrem doleva, tak se změní proměnná směr na 2, což znamená, že pojede doprava
                směr = 2
            if event.key == pygame.K_s and směr != 1:#Pokud stiskneme S a proměnná směr není 1, což by znamenalo že had se pohybuje směrem nahoru, tak se změní proměnná směr na 1, což znamená, že pojede dolu
                směr = 3
            if event.key == pygame.K_a and směr != 2:#Pokud stiskneme A a proměnná směr není 2, což by znamenalo že had se pohybuje směrem doprava, tak se změní proměnná směr na 1, což znamená, že pojede doleva
                směr = 4
    #tvorba jídla
    if nove_jidlo == True:
        nove_jidlo = False
        jidlo[0] = velikost_blocku * random.randint(0, round(šířka_okna / velikost_blocku) - 1) #Generování náhodného čísla reprezentující pozici x, pro block jídla
        jidlo[1] = velikost_blocku * random.randint(0, round(výška_okna / velikost_blocku) - 1) #Generování náhodného čísla reprezentující pozici y, pro block jídla
    #Vykreslní jídla
    pygame.draw.rect(okno, barva_jidla, (jidlo[0], jidlo[1], velikost_blocku, velikost_blocku))
    #Kolize s jídlem
    if pozice_hada[0] == jidlo:#[0] je block hlavy hada a jeho pozice, neboli (1, 20) třeba. Pokud se rovná s pozicí jídla, tak se podmínka vykoná
        nove_jidlo = True
        #Prodloužení hada
        prodlouzeny_block = list(pozice_hada[-1])
        if směr == 1:
            prodlouzeny_block[1] += velikost_blocku#Pokud se had pohybuje nahoru, prodlouží se o velikost velikost_blocku na y souřadnici, což reprezentuje jeden block
        elif směr == 3:
            prodlouzeny_block[1] -= velikost_blocku#Pokud se had pohybuje dolu, zmenší se o velikost velikost_blocku na y souřadnici, což reprezentuje jeden block
        elif směr == 2:
            prodlouzeny_block[0] -= velikost_blocku#Pokud se had pohybuje doleva, zmenší se o velikost velikost_blocku na x souřadnici, což reprezentuje jeden block
        if směr == 4:
            prodlouzeny_block[0] += velikost_blocku#Pokud se had pohybuje doprava, zvětší se o velikost velikost_blocku na x souřadnici, což reprezentuje jeden block
        
        #Připojení blocku za sebrání jídla k hadovi
        pozice_hada.append(prodlouzeny_block)
        score += 1 #Přidání score
    if konec_hry == False:
        if update_snake > 333:
            update_snake = 0
            pozice_hada = pozice_hada[-1:] + pozice_hada[:-1]
            if směr == 1:
                pozice_hada[0][0] = pozice_hada[1][0]
                pozice_hada[0][1] = pozice_hada[1][1] - velikost_blocku
            elif směr == 3:
                pozice_hada[0][0] = pozice_hada[1][0]
                pozice_hada[0][1] = pozice_hada[1][1] + velikost_blocku
            elif směr == 2:
                pozice_hada[0][1] = pozice_hada[1][1]
                pozice_hada[0][0] = pozice_hada[1][0] + velikost_blocku
            elif směr == 4:
                pozice_hada[0][1] = pozice_hada[1][1]
                pozice_hada[0][0] = pozice_hada[1][0] - velikost_blocku
            konec_hry = kontrola_konce_hry(konec_hry)
    else:
        prohra += 1
        if prohra == 1:
            pygame.time.delay(2000)
        okno.fill((0, 0, 0))
        vykresleni_konce_hry()
        vykreslení_score()
        if event.type == pygame.MOUSEBUTTONDOWN and kliknuto == False:#Kliknutní
            kliknuto = True
        if event.type == pygame.MOUSEBUTTONUP and kliknuto == True:#Upuštění
            kliknuto = False
        #Jen pro kontrolu, jestli uživatel skutečně kliknul, a nedrží jen tlačítko myši
            pos = pygame.mouse.get_pos()
            if tlačítko.collidepoint(pos):
                #Restart Proměnných
                pozice_hada = [[int(šířka_okna / 2), int(výška_okna / 2)]]
                pozice_hada.append([int(šířka_okna / 2), int(výška_okna / 2) + velikost_blocku])
                pozice_hada.append([int(šířka_okna / 2), int(výška_okna / 2) + velikost_blocku * 2])
                pozice_hada.append([int(šířka_okna / 2), int(výška_okna / 2) + velikost_blocku * 3])
                směr = 1
                update_snake = 0
                jidlo = [0, 0]
                nove_jidlo = True
                prodlouzeny_block = [0, 0]
                score = 0
                prohra = 0
                konec_hry = False
    hlava = 1#Proměnná, která nám zajistí, že podmínka ve for loopu níže bude splněna pouze jednou, pro získání jiné barvy pro block představující hlavu
    if konec_hry == False or prohra == 0:
        for x in pozice_hada:
            if hlava == 0:#Ostatní blocky mimo hlavu, neboli tělo
                pygame.draw.rect(okno, outline, (x[0], x[1], velikost_blocku, velikost_blocku))#Vykreslení větší blocku pod menší block, pro získání efektu stínu/obrysu
                pygame.draw.rect(okno, body_inner, (x[0] + 1, x[1] + 1, velikost_blocku - 2, velikost_blocku - 2))#Vykreslení menšího blocku na větší block, pro uplatnění efektu
            if hlava == 1:#Podmínka za celý for loop proběhne jednou
                pygame.draw.rect(okno, outline, (x[0], x[1], velikost_blocku, velikost_blocku))#Vykreslení větší blocku pod menší block, pro získání efektu stínu/obrysu
                pygame.draw.rect(okno, modra, (x[0] + 1, x[1] + 1, velikost_blocku - 2, velikost_blocku - 2))#Vykreslení menšího blocku na větší block, pro uplatnění efektu
                hlava = 0
    #update displaye
    pygame.display.update()
    update_snake += 1
pygame.quit()