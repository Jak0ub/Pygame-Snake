## Úvod
* Jedná se o snake hru naprogramovanou pomocí knihovny Pygame v jazyce Python, za účelem školního projektu.
* Hra obsahuje možnost zvolení obtížnosti(více k obtížnostem níže), obsahuje možnost nápovědy, zobrazení a vynulování hodnot skóre dosažených uživatelem 


## SHA-256
```SHA-256
C7B9C2FB94547BD4D2964A332D1258BFEA06A749AD741F1E75115F47B76C3DDA
```

> ⚠️ **Pozor:**
> Program může obsahovat chyby, pokud nějaké naleznete, prosím kontaktujte mě.

## Changelog

`!` `08.03.25` `Hra obsahuje prvky nutné k samotnému fungovaní hry, zjednodušeně, toto je kostra programu. Veškteré funkce, které budou v budoucnosti přidávány, jsou považovány za dodatkové`

`!` `13.03.25` `Ve hře jsou nyní obtížnosti, které jsou volitelné + byla upravena logika fps`

`!` `14.03.25` `Oprava chyby v určování pozice jídla zavisejíc na obtížnosti uživatelem zvolené`

`!` `19.03.25` `Nyní je možnost zastavit zobrazování se okna programu cmd.exe po každém zapnutí programu užitím donotshowup.vbs souboru fungujicího na Windows systémech. Více níže...`

`!` `20.03.25` `Nyní je ve hře ukládání nejlepšího skóre pro každou obtížnost. Také je nově ve hře možnost nápovědy + drobné úpravy`

`!` `21.03.25` `Drobné úpravy`

<div style="display: flex; gap: 10px;">
    <img src="https://github.com/Jak0ub/PyGame/blob/main/img/1.png" width="30%" height="40%">
    <img src="https://github.com/Jak0ub/PyGame/blob/main/img/2.png" width="30%" height="40%">
</div>
<div style="display: flex; gap: 10px;">
    <img src="https://github.com/Jak0ub/PyGame/blob/main/img/3.png" width="30%" height="40%">
    <img src="https://github.com/Jak0ub/PyGame/blob/main/img/4.png" width="30%" height="40%">
</div>

`Kompatibilní s Unix a Windows based systémy`

## Obtížnosti

| Obtížnost | Easy  | Medium  | Hard |
| ------- | --- | --- | --- |
| Popis | jídlo nebude nikdy na okraji obrazovky | jídlo může, ale nemusí být na okraji obrazovky (50%) | jídlo je vždy na okraji obrazovky |

## VBS soubor(Pouze pro Windows)

Pokud se chcete zbavit vyskakovacího cmd.exe okna, stačí spouštět program přes .vbs soubor
> ⚠️ **Pozor:**
> Pokud přejmenujete .py soubor, je třeba upravit obsah souboru .vbs pro opětovné fungování



## Instalace knihoven

```
pip install -r requirements.txt
```
