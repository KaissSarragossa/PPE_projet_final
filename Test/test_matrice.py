from machine import Pin, I2C
import time
 
# Configuration du bus I2C
i2c = I2C(
    0,
    scl=Pin(Pin.board.A5),
    sda=Pin(Pin.board.A4)
)
 
# Adresses des deux matrices
matrice_1 = 0x70
matrice_2 = 0x71
 
# Verification des connexions
peripheriques = i2c.scan()
 
print("Peripheriques I2C :", peripheriques)
 
# Initialisation d'une matrice HT16K33
def initialiser_matrice(adresse):
    i2c.writeto(adresse, bytes([0x21]))
    i2c.writeto(adresse, bytes([0x81]))
    i2c.writeto(adresse, bytes([0xEF]))
 
# Effacer une matrice
def effacer_matrice(adresse):
    for ligne in range(0, 16, 2):
        i2c.writeto(adresse, bytes([ligne, 0x00]))
 
# Afficher un nombre de colonnes
def afficher_colonnes(adresse, nombre):
    masque = (1 << nombre) - 1
 
    for ligne in range(0, 16, 2):
        i2c.writeto(adresse, bytes([ligne, masque]))
 
# Initialisation des matrices
if matrice_1 in peripheriques:
    initialiser_matrice(matrice_1)
    effacer_matrice(matrice_1)
else:
    print("Matrice 1 non detectee")
 
if matrice_2 in peripheriques:
    initialiser_matrice(matrice_2)
    effacer_matrice(matrice_2)
else:
    print("Matrice 2 non detectee")
 
# Test de remplissage progressif
try:
    for colonne in range(1, 9):
 
        print("Colonnes allumees :", colonne)
 
        if matrice_1 in peripheriques:
            afficher_colonnes(matrice_1, colonne)
 
        if matrice_2 in peripheriques:
            afficher_colonnes(matrice_2, colonne)
 
        time.sleep(1)
 
    print("Test termine")
 
except KeyboardInterrupt:
    print("Test interrompu")
 
finally:
    if matrice_1 in peripheriques:
        effacer_matrice(matrice_1)
 
    if matrice_2 in peripheriques:
        effacer_matrice(matrice_2)