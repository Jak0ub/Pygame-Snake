import pygame
from pygame.locals import *
import random
import time
import os
import platform
#Nastavení cesty, kam se bude ukládat soubor s nejvyšším skórem
platform_system = platform.system()
if platform_system == "Windows":
	temp_Windows_path = os.environ.get('TEMP')
	soubor_skóre = f"{temp_Windows_path}/high_score-snake.txt"
else:
	soubor_skóre = "/tmp/high_score-snake.txt"
#inicializace
pygame.init()
#Okno
šířka_okna = 600
výška_okna = 600
okno = pygame.display.set_mode((šířka_okna, výška_okna))
pygame.display.set_caption("Had")

kliknuto = False

fps = 10
run = True
prohra = 0
stisk = 0
obtiznosti = ["Snadná", "Střední", "Obtížná"]
obtiznost = obtiznosti[2] #volba obtížnosti

aktualizuj = False

velikost_blocku = 20#pixely na jednen block ve hře
směr = 1#1 je nahoru, 2 vpravo, 3 dolu a 4 vlevo
#score
score = 0
konec_hry = False
#Snake
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
font_mensi = pygame.font.SysFont(None, 33)
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
def vykreslení_obtížnosti():
    text_obtiznosti = f"Obtížnost: {obtiznost}"
    if obtiznost == obtiznosti[0]:
        barva = (0, 255, 0)
    elif obtiznost == obtiznosti[1]:
        barva = (255, 255, 0)
    else:
        barva = (255, 0, 0)
    obtiznost_okno = font.render(text_obtiznosti, True, barva)
    okno.blit(obtiznost_okno, ((šířka_okna * 0.3), výška_okna - 33))
def vykreslení_score():
    text = f"Skóre: {score}"
    if obtiznost == obtiznosti[0]:
        barva = (0, 255, 0)
    elif obtiznost == obtiznosti[1]:
        barva = (255, 255, 0)
    else:
        barva = (255, 0, 0)
    skóre = font.render(text, True, barva)
    okno.blit(skóre, ((šířka_okna * 0.42), 3))
def kontrola_konce_hry(konec_hry, pozice_hada):
    #Kontrola kolize hada s jeho tělem
    cislo_blocku = 0
    for segment in pozice_hada:
        if pozice_hada[0] == segment and cislo_blocku > 0: #Vynechá hlavu
            konec_hry = True #kolize hlavy s ostatními částmi
        cislo_blocku += 1
    #kontrola jestli je had mimo pole
    if pozice_hada[0][0] < 0 or pozice_hada[0][0] > šířka_okna - velikost_blocku or pozice_hada[0][1] < 0 or pozice_hada[0][1] > výška_okna - velikost_blocku:
        konec_hry = True
    return konec_hry
def vykresleni_volby():
    text = f"Zvol si obtížnost:"
    volba = font.render(text, True, (255, 255, 255))
    okno.blit(volba, ((šířka_okna * 0.33), 3))
def vykresleni_konce_hry():
    konec = "! Konec hry !"
    konec = font.render(konec, True, (255, 255, 255))
    pygame.draw.rect(okno, (255, 0, 0), (šířka_okna // 2 - 100, výška_okna // 2 - 70, 200, 50), 2, 3)
    okno.blit(konec, (šířka_okna // 2 - 85, výška_okna // 2 - 58))
    znovu = "Hrát znovu?"
    znovu = font.render(znovu, True, (255, 255, 255))
    pygame.draw.rect(okno, (255, 0, 0), tlačítko, 2, 3)
    okno.blit(znovu, (šířka_okna // 2 - 80, výška_okna // 2 + 10))
    info = "<--- klikni"
    info = font_mensi.render(info, True, (0, 255, 0))
    okno.blit(info, (šířka_okna // 2 + 100, výška_okna // 2 + 10))
    if změna == True:
        info = "|i| Dosáhl jsi nového nejlepšího skóre |i|"
        info = font_mensi.render(info, True, (255, 255, 255))
        okno.blit(info, (0 + šířka_okna // 6, výška_okna - výška_okna // 5))


#Zapisování nejlepšího výsledku skóre uživatelem dosaženého
def zápis_score():
    #  Struktura souboru pro high score:
    #  1;10 
    #  2;8
    #  3;12
    # čísla značí obtížnost, to po ";" jsou hodnoty nejlepšího skóre pro individuální level obtížnosti 
    high_score = []
    working = score #pracovní proměná pro lepší orientaci
    vytvoř = False
    změna = False
    try:
        with open(f"{soubor_skóre}", "r", encoding="utf-8") as file:
            radky = file.readlines()
            try:
                for i in range(3):
                    hlavni = radky[i].strip()
                    try:
                        if int(hlavni.split(";")[0]) == i + 1:
                            try:
                                cislo = hlavni.split(";")[1]
                                try:
                                    cislo = int(cislo)
                                    high_score.append(cislo)
                                except ValueError:
                                    high_score.append("0")
                            except IndexError:
                                high_score.append("0")
                        else:
                            vytvoř = True
                    except ValueError:
                        vytvoř = True
                        high_score = ["0", "0", "0"]
            except IndexError:
                vytvoř = True
                high_score = ["0", "0", "0"]
    except FileNotFoundError:
        vytvoř = True
        high_score = ["0", "0", "0"]
    if vytvoř == True:
        high_score[obtiznosti.index(obtiznost)] = working
        radky = []
        pocet = 0
        for obsah in high_score:
            pocet += 1
            if pocet == 3:
                radky.append(f"{pocet};{obsah}")
            else:
                radky.append(f"{pocet};{obsah}\n")
        with open(f"{soubor_skóre}", "w", encoding="utf-8") as file:
            file.writelines(radky)
        if working != 0:
            změna = True
    if int(high_score[obtiznosti.index(obtiznost)]) < working:
        high_score[obtiznosti.index(obtiznost)] = working
        radky = []
        pocet = 0
        for obsah in high_score:
            pocet += 1
            if pocet == 3:
                radky.append(f"{pocet};{obsah}")
            else:
                radky.append(f"{pocet};{obsah}\n")
        with open(f"{soubor_skóre}", "w", encoding="utf-8") as file:
            file.writelines(radky) 
        změna = True 

    return změna
#Volba obtížnosti
run = True
prohra = 0
stisk = 0
start = time.time()
easy = [šířka_okna // 5, výška_okna // 3]
medium = [šířka_okna // 2, výška_okna // 3]
hard = [šířka_okna // 1.25, výška_okna // 3]
def popisky():#Popisky k blockům obtížnosti, volitelné
    moznosti = [easy, medium, hard]
    for i in range(3):
        info = f"{obtiznosti[i]}"
        block = moznosti[i]
        info = font_mensi.render(info, True, (255, 255, 255))
        okno.blit(info, (block[0] + 30, block[1]))
skore = [4 * velikost_blocku, (výška_okna // 3) * 2 + velikost_blocku * 3]
reset = [šířka_okna // 1.5, (výška_okna // 3) - velikost_blocku * 3]
popis = [šířka_okna - velikost_blocku * 4, (výška_okna // 3) * 2 + velikost_blocku * 3]
def choice():
    timeout = 0
    zobraz_skore = False
    run = True
    start = time.time()
    pozice_hada = [[int(šířka_okna / 2), int(výška_okna / 2)]]#list pozic blocků + přidání prvního blocku
    pozice_hada.append([int(šířka_okna / 2) - velikost_blocku, int(výška_okna / 2) ])#Druhý block
    pozice_hada.append([int(šířka_okna / 2) -velikost_blocku * 2, int(výška_okna / 2)])#Třetí block
    pozice_hada.append([int(šířka_okna / 2) - velikost_blocku * 3, int(výška_okna / 2)])#Čtvrtý block
    konec_hry = False
    aktualizuj = False
    cekej = 0
    směr = 2
    pomoc = False
    prohra = 0
    while run:
        cas = round(time.time() - start, 2)
        vykreslení_okna()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and stisk == 0:
                if event.key == pygame.K_w and směr != 3:#Pokud stiskneme W a proměnná směr není 3, což by znamenalo že had se pohybuje směrem dolu, tak se změní proměnná směr na 1, což znamená, že pojede nahoru
                    směr = 1
                if event.key == pygame.K_d and směr != 4:#Pokud stiskneme D a proměnná směr není 4, což by znamenalo že had se pohybuje směrem doleva, tak se změní proměnná směr na 2, což znamená, že pojede doprava
                    směr = 2
                if event.key == pygame.K_s and směr != 1:#Pokud stiskneme S a proměnná směr není 1, což by znamenalo že had se pohybuje směrem nahoru, tak se změní proměnná směr na 1, což znamená, že pojede dolu
                    směr = 3
                if event.key == pygame.K_a and směr != 2:#Pokud stiskneme A a proměnná směr není 2, což by znamenalo že had se pohybuje směrem doprava, tak se změní proměnná směr na 1, což znamená, že pojede doleva
                    směr = 4
                stisk += 1
        if zobraz_skore == False:
            vykresleni_volby()
            if pomoc == True:
                popisky()
            pygame.draw.rect(okno, (0, 255, 0), (easy[0], easy[1], velikost_blocku, velikost_blocku))
            pygame.draw.rect(okno, (255, 255, 0), (medium[0], medium[1], velikost_blocku, velikost_blocku))
            pygame.draw.rect(okno, (255, 0, 0), (hard[0], hard[1], velikost_blocku, velikost_blocku))
            pygame.draw.rect(okno, (0, 255, 255), (skore[0], skore[1], velikost_blocku, velikost_blocku))#Block pro volbu zobrazení nejvyššího dosaženého skóre
            pygame.draw.rect(okno, (5, 110, 80), (popis[0], popis[1], velikost_blocku, velikost_blocku))
            info = "Nápověda"
            info = font_mensi.render(info, True, (255, 255, 255))
            okno.blit(info, (popis[0] - 40, popis[1] + 30))
            info = "Nejvyšší skóre"
            info = font_mensi.render(info, True, (255, 255, 255))
            okno.blit(info, (skore[0] - 64, skore[1] + 30))
            if pozice_hada[0] == easy:#[0] je block hlavy hada a jeho pozice, neboli (1, 20) třeba. Pokud se rovná s pozicí jídla, tak se podmínka vykoná
                obtiznost = obtiznosti[0]
                break
            elif pozice_hada[0] == medium:#[0] je block hlavy hada a jeho pozice, neboli (1, 20) třeba. Pokud se rovná s pozicí jídla, tak se podmínka vykoná
                obtiznost = obtiznosti[1]
                break
            elif pozice_hada[0] == hard:#[0] je block hlavy hada a jeho pozice, neboli (1, 20) třeba. Pokud se rovná s pozicí jídla, tak se podmínka vykoná
                obtiznost = obtiznosti[2]
                break
            elif pozice_hada[0] == skore:
                if round(time.time() - timeout, 2) > 0.3:
                    zobraz_skore = True
                    timeout = time.time()
            elif pozice_hada[0] == popis:
                if round(time.time() - cekej, 2) > 0.3:
                    cekej = time.time()
                    if pomoc == False:
                        pomoc = True
                    else:
                        pomoc = False
                else:
                    cekej = time.time()
        else:
            info = "Reset hodnot"
            info = font_mensi.render(info, True, (255, 255, 255))
            okno.blit(info, (reset[0] + 30, reset[1]))
            pygame.draw.rect(okno, (255, 0, 0), (reset[0], reset[1], velikost_blocku, velikost_blocku))
            info = "Exit"
            info = font_mensi.render(info, True, (255, 255, 255))
            okno.blit(info, (skore[0] - 15, skore[1] + 30))
            if round(time.time() - timeout, 2) > 0.3:
                pygame.draw.rect(okno, (0, 255, 255), (skore[0], skore[1], velikost_blocku, velikost_blocku))
                if pozice_hada[0] == skore:
                    zobraz_skore = False
                    timeout = time.time()
                if pozice_hada[0] == reset:
                    with open(f"{soubor_skóre}", "w", encoding="utf-8") as file: 
                        file.write("1;0\n2;0\n3;0")
            hodnoty = []
            try:
                with open(f"{soubor_skóre}", "r", encoding="utf-8") as file:
                    radky = file.readlines()
                    for i in range(3):
                        try:
                            hodnoty.append(radky[i].split(";")[1].strip())
                        except IndexError:
                            hodnoty.append("0")
            except FileNotFoundError:
                hodnoty = ["0", "0", "0"]
            for i in range(3):
                hodnota = f"{obtiznosti[i]} : {hodnoty[i]}"
                hodnota = font_mensi.render(hodnota, True, (255, 255, 255))
                okno.blit(hodnota, (50, (výška_okna // 8) * (2 + i)))
                box = Rect(25, (výška_okna // 8) * (2 + i) - 11, 160, 45)
                pygame.draw.rect(okno, (255, 0, 0), box, 2, 3)

        
        if cas > 1 / fps:
            aktualizuj = True
            start = time.time()
            stisk = 0
        if konec_hry == False:
            if aktualizuj == True:
                aktualizuj = False
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
                konec_hry = kontrola_konce_hry(konec_hry, pozice_hada)
        else:
            #Moc krásný efekt!
            if pozice_hada[0][0] > šířka_okna + velikost_blocku * 3:
                pozice_hada = [[0, pozice_hada[0][1]]]
                pozice_hada.append([0 - velikost_blocku, pozice_hada[0][1]])
                pozice_hada.append([0 -velikost_blocku * 2, pozice_hada[0][1]])
                pozice_hada.append([0 - velikost_blocku * 3, pozice_hada[0][1]])
            if pozice_hada[0][0] < 0 - velikost_blocku * 3:
                pozice_hada = [[šířka_okna, pozice_hada[0][1]]]
                pozice_hada.append([šířka_okna + velikost_blocku, pozice_hada[0][1]])
                pozice_hada.append([šířka_okna + velikost_blocku * 2, pozice_hada[0][1]])
                pozice_hada.append([šířka_okna + velikost_blocku * 3, pozice_hada[0][1]])
            if pozice_hada[0][1] > výška_okna + velikost_blocku * 3:
                pozice_hada = [[pozice_hada[0][0], 0]]
                pozice_hada.append([pozice_hada[0][0], 0 - velikost_blocku])
                pozice_hada.append([pozice_hada[0][0], 0 - velikost_blocku * 2])
                pozice_hada.append([pozice_hada[0][0], 0 - velikost_blocku * 3])
            if pozice_hada[0][1] < 0 - velikost_blocku * 3:
                pozice_hada = [[pozice_hada[0][0], výška_okna]]
                pozice_hada.append([pozice_hada[0][0], výška_okna + velikost_blocku])
                pozice_hada.append([pozice_hada[0][0], výška_okna + velikost_blocku * 2])
                pozice_hada.append([pozice_hada[0][0], výška_okna + velikost_blocku * 3])
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
    return obtiznost, pozice_hada, směr
#Main loop
start = time.time()
obtiznost, pozice_hada, směr = choice()
while run:
    cas = round(time.time() - start, 2)
    vykreslení_okna()
    vykreslení_score()
    vykreslení_obtížnosti()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and stisk == 0:
            if event.key == pygame.K_w and směr != 3:#Pokud stiskneme W a proměnná směr není 3, což by znamenalo že had se pohybuje směrem dolu, tak se změní proměnná směr na 1, což znamená, že pojede nahoru
                směr = 1
            if event.key == pygame.K_d and směr != 4:#Pokud stiskneme D a proměnná směr není 4, což by znamenalo že had se pohybuje směrem doleva, tak se změní proměnná směr na 2, což znamená, že pojede doprava
                směr = 2
            if event.key == pygame.K_s and směr != 1:#Pokud stiskneme S a proměnná směr není 1, což by znamenalo že had se pohybuje směrem nahoru, tak se změní proměnná směr na 1, což znamená, že pojede dolu
                směr = 3
            if event.key == pygame.K_a and směr != 2:#Pokud stiskneme A a proměnná směr není 2, což by znamenalo že had se pohybuje směrem doprava, tak se změní proměnná směr na 1, což znamená, že pojede doleva
                směr = 4
            stisk += 1
    #tvorba jídla
    if nove_jidlo == True:
        nove_jidlo = False
        if obtiznost == obtiznosti[0]: #Neboli pokud se rovná zvolená obtížnost první obtížnosti v listu(easy)
            jidlo[0] = velikost_blocku * random.randint(2, round(šířka_okna / velikost_blocku) - 2) #Generování náhodného čísla reprezentující pozici x, pro block jídla, který nebude na okraji obrazovky
            jidlo[1] = velikost_blocku * random.randint(2, round(výška_okna / velikost_blocku) - 2) #Generování náhodného čísla reprezentující pozici y, pro block jídla, který nebude na okraji obrazovky
        elif obtiznost == obtiznosti[1]: #medium obtížnost
            nahodne = random.randint(0, 1)
            if nahodne == 1: #jídlo bude na okraji
                osa = random.choice(["x", "y"])
                strana = random.randint(0,1)
                if osa == "y":
                    jidlo[0] = velikost_blocku * random.randint(0, round(šířka_okna / velikost_blocku) - 1) #Generování náhodného čísla reprezentující pozici x, pro block jídla
                    if strana == 1:
                        jidlo[1] = 0
                    else:
                        jidlo[1] = výška_okna - velikost_blocku
                elif osa == "x":
                    if strana == 1:
                        jidlo[0] = 0
                    else:
                        jidlo[0] = šířka_okna - velikost_blocku
                    jidlo[1] = velikost_blocku * random.randint(0, round(výška_okna / velikost_blocku) - 1) #Generování náhodného čísla reprezentující pozici y, pro block jídla
            else: #jídlo nebude na okraji
                jidlo[0] = velikost_blocku * random.randint(2, round(šířka_okna / velikost_blocku) - 2) #Generování náhodného čísla reprezentující pozici x, pro block jídla
                jidlo[1] = velikost_blocku * random.randint(2, round(výška_okna / velikost_blocku) - 2) #Generování náhodného čísla reprezentující pozici y, pro block jídla
        elif obtiznost == obtiznosti[2]: #hard obtížnost, neboli jídlo je vždy na okraji obrazovky
                osa = random.choice(["x", "y"])
                strana = random.randint(0,1)
                if osa == "y":
                    jidlo[0] = velikost_blocku * random.randint(0, round(šířka_okna / velikost_blocku) - 1) #Generování náhodného čísla reprezentující pozici x, pro block jídla
                    if strana == 1:
                        jidlo[1] = 0
                    else:
                        jidlo[1] = výška_okna - velikost_blocku
                elif osa == "x":
                    if strana == 1:
                        jidlo[0] = 0
                    else:
                        jidlo[0] = šířka_okna - velikost_blocku
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
    if cas > 1 / fps:
        aktualizuj = True
        start = time.time()
        stisk = 0
    if konec_hry == False:
        if aktualizuj == True:
            aktualizuj = False
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
            konec_hry = kontrola_konce_hry(konec_hry, pozice_hada)
    else:
        prohra += 1
        if prohra == 1:
            pygame.time.delay(2000)
            změna = zápis_score()
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
                aktualizuj = False
                jidlo = [0, 0]
                nove_jidlo = True
                prodlouzeny_block = [0, 0]
                score = 0
                stisk = 0
                prohra = 0
                konec_hry = False
                obtiznost, pozice_hada, směr = choice()
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
pygame.quit()
