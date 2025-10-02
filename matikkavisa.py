import random

# KYSYMYKSET JA VASTAUKSET
kysymykset = {
    "5 + 3": 8,
    "9 - 4": 5,
    "7 * 2": 14,
    "12 / 3": 4,
    "8 + 6": 14,
    "15 - 7": 8,
    "4 * 5": 20,
    "20 / 4": 5,
    "10 + 9": 19,
    "14 - 6": 8,
    "6 * 3": 18,
    "18 / 2": 9,
    "11 + 8": 19,
    "13 - 9": 4,
    "9 * 4": 36,
    "24 / 6": 4,
    "16 + 7": 23,
    "25 - 12": 13,
    "5 * 8": 40,
    "30 / 5": 6
}

# 5 RANDOM KYSYMYSTÄ
valitut_kysymykset = random.sample(list(kysymykset.items()), 5)

print("Tervetuloa pelaamaan! Vastaa viiteen kysymykseen oikein voittaaksesi.")
print("Jos vastaat väärin, peli loppuu heti.")

# PELI
for kysymys, vastaus in valitut_kysymykset:
    try:
        user_input = float(input(f"{kysymys} = "))
    except ValueError:
        print("Virheellinen syöte.")
        break
    if user_input != vastaus:
        print(f"Väärin! Oikea vastaus on {vastaus}. Hävisit pelin.")
        break
else:
    print("Onneksi olkoon! Vastasit kaikki oikein ja voitit pelin.")
