import random

def numeron_arvauspeli():
    print("Tervetuloa numeron arvauspeliin!")
    print("Ajattelen numeroa 1 ja 9 välillä...")
    
    oikea_numero = random.randint(1, 9)
    arvaukset = 0
    
    while True:
        try:
            arvaus = int(input("Arvaa numero: "))
            arvaukset += 1
            
            if arvaus < oikea_numero:
                print("Liian pieni! Yritä uudelleen.")
            elif arvaus > oikea_numero:
                print("Liian suuri! Yritä uudelleen.")
            else:
                print(f"Onneksi olkoon! Arvasit oikein numeron {oikea_numero} {arvaukset} yrityksellä.")
                break
        except ValueError:
            print("Ole hyvä ja syötä kokonaisluku.")

# Käynnistetään peli
numeron_arvauspeli()
