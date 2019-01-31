

a = 0
b = 1
muuttuja = 0
taulukko = []
taulukko2 = []
taulukko3 = []
taulukko4 = []
for c in range(0,20):
        n = a + b
        a = b
        b = n
        if muuttuja < 5:
            taulukko.append(a)
            muuttuja += 1
        elif muuttuja >= 5 and muuttuja < 10:
            taulukko2.append(a)
            muuttuja += 1
        elif muuttuja >= 10 and muuttuja < 15:
            taulukko3.append(a)
            muuttuja += 1
        elif muuttuja >= 15  muuttuja < 20:
            taulukko4.append(a)
            muuttuja += 1
        
        
print(taulukko)
print(taulukko2)
print(taulukko3)
print(taulukko4)