import random

def kivi_sakset_paperi():
    print("Tervetuloa Kivi–Sakset–Paperi -peliin! Pelataan 3 kierrosta.")
    vaihtoehdot = ["kivi", "sakset", "paperi"]
    pelaajan_pisteet = 0
    tietokoneen_pisteet = 0

    for kierros in range(1, 4):
        print(f"\nKierros {kierros}:")
        while True:
            pelaaja = input("Valitse kivi, sakset tai paperi: ").lower()
            if pelaaja not in vaihtoehdot:
                print("Virheellinen valinta. Yritä uudelleen.")
                continue
            break
        
        tietokone = random.choice(vaihtoehdot)
        print(f"Tietokone valitsi: {tietokone}")
        
        if pelaaja == tietokone:
            print("Tasapeli!")
        elif (pelaaja == "kivi" and tietokone == "sakset") or \
             (pelaaja == "sakset" and tietokone == "paperi") or \
             (pelaaja == "paperi" and tietokone == "kivi"):
            print("Voitit kierroksen!")
            pelaajan_pisteet += 1
        else:
            print("Hävisit kierroksen!")
            tietokoneen_pisteet += 1

    print("\nPeli päättyi!")
    print(f"Pisteet - Pelaaja: {pelaajan_pisteet}, Tietokone: {tietokoneen_pisteet}")
    
    if pelaajan_pisteet > tietokoneen_pisteet:
        print("Onneksi olkoon! Voitit pelin!")
    elif pelaajan_pisteet < tietokoneen_pisteet:
        print("Hävisit pelin!")
    else:
        print("Peli päättyi tasapeliin!")

kivi_sakset_paperi()