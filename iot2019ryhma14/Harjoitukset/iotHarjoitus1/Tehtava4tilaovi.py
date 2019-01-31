value = ""
O = 0
L = 0

def valinnat():
    print("Avaa ovi = 1 \n" + "Sulje ovi = 2 \n" + "Avaa lukko = 3 \n" + "Sulje lukko = 4 \n")
    value = int(input("Valitse: "))
    return value

def tarkistalukko(L):
    if L == 0:
        print("Ovi ei ole lukossa!")
    if L == 1:
        print("Ovi on lukossa!")
def tarkistaovi(O):
    if O == 0:
        print("Ovi on auki!")
    if O == 1:
        print("Ovi on kiinni!")

def tarkistavalinta(value, O, L):
    #Halutaan avata ovi
    if value == 1:
        if O == 1 and L == 0:
            print("Avataan ovi....")
            O = 0
            print("Ovi auk!")
        elif O == 0:
            print("Ovi oli jo auki!")
        elif L == 1:
            print("Ovi on lukossa, avaa lukko ensin.")
        return O, L
    #Halutaan sulkea ovi
    if value == 2:
        if O == 0 and L == 0:
            print("Suljetaan ovi....")
            O = 1
            print("Ovi on nyt kiinni!")
        elif O == 1:
            print("Ovi oli jo kiinni!")
        elif L == 1:
            print("Ovi on lukossa, ovi on tässä vaiheessa rikki ")
        return O, L
    #Halutaan avata lukko
    if value == 3:
        if O == 1 and L == 1:
            print("Avataan oven lukkoa....")
            L = 0
            print("Ovi ei ole enää lukossa!")
        elif O == 0:
            print("Ovi on auki, eikä sitä voi avata lukosta. Ovi on rikki!")
        elif L == 0:
            print("Ovi ei ole lukossa!")
        return O, L
    #Halutaan sulkea lukko
    if value == 4:
        if O == 1 and L == 0:
            print("Lukitaan ovea....")
            L = 1
            print("Ovi on nyt lukossa!")
        elif O == 0:
            print("Sulje ovi ennen lukittamista!")
        elif L == 1:
            print("Ovi on jo lukossa!")
        return O, L
    
def main():
    global O
    global L
    tarkistaovi(O)
    tarkistalukko(L)
    value = valinnat()
    O, L = tarkistavalinta(value, O, L)
    
 


try:
    while True:
        main()
except KeyboardInterrupt:
    pass