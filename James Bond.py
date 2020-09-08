import re #Library for 'Regular expression operations' Brukes bare for å teste
# etter romertall på en enkel måte

# Ærklær variabler som skal brukes senere
prepos = ["Von","Van","De","Di"] # Alle preposisjoner
suffix = ["Jr","Sr"] # Alle ord som kan settes bakerst i navnet uten å telles
etternavn_array = [] # Lagre en etternavn array, denne printes før hele navnet
# Ærklær en funksjon som sjekker om inputtet er romertall
# Støtter romertall langt over 1000 (selv om det kanskje ikke er noe vits xD )
# !ADVARSEL! Navn som inneholder en kobinasjon av (og bare av) bokstavene I, V,
# X, L, C, D, M kan telles som romertall og ikke telles som et etternavn!
er_romersk = lambda x: re.match("^[IVXLCDM]*$", x) != None

#navn = "Henry Von Huxtable III" # Kommenter ut/inn for å teste forskjellige navn enklere
navn = input("Jeg heter: ")
navn_array = navn.split(" ")

# Looper over alle delnavnene, start bakerst
for i in range(len(navn_array)-1,0-1,-1):
    _delnavn = navn_array[i]
    # Hvist delnavnet ikke er romertall eller i 'siffix' ("Jr","Sr"...)
    # Så er dette en del av det som skal printes før komma
    if ( not er_romersk(_delnavn) ) and ( not _delnavn in suffix):
        # Legg til delnavnet i 'etternavn_array' for å printes før komma senere
        etternavn_array.append(_delnavn)
        # Finn ut om delnavnet før etternavnet er i 'prepos' ("Von","Van"...)
        # og legg det til i 'etternavn_array' hvis det er det
        if (navn_array[i-1] in prepos) and (i-1 != 0):
            etternavn_array.insert(0,navn_array[i-1])
        # Break for å avslutte loopen når navnet er ferdig
        break

l = len(etternavn_array)
# Slå sammen 'etternavn_array' og 'navn' til det endelige resultatet
først = " ".join([etternavn_array[i] for i in range(0,l) ])
print(f"{først}, {navn}")
