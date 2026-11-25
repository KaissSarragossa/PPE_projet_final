 
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
 
 
from machine import Pin, PWM
import time
from pins import Pins
 
# Configuration des DEL du feu tricolore
led_rouge = Pin(Pins.D5, Pin.OUT)
led_jaune = Pin(Pins.D6, Pin.OUT)
led_verte = Pin(Pins.D7, Pin.OUT)
 
# Configuration des buzzers
buzzer_1 = PWM(Pin(Pins.D10))
buzzer_2 = PWM(Pin(Pins.D11))
 
buzzer_1.freq(1000)
buzzer_2.freq(1000)
 
# Eteindre toutes les DEL
def eteindre_feu():
    led_rouge.value(0)
    led_jaune.value(0)
    led_verte.value(0)
 
# Tester le feu tricolore
def tester_feu():
    print("Test du feu tricolore")
 
    eteindre_feu()
 
    print("ROUGE")
    led_rouge.value(1)
    time.sleep(2)
 
    eteindre_feu()
 
    print("JAUNE")
    led_jaune.value(1)
    time.sleep(2)
 
    eteindre_feu()
 
    print("VERT")
    led_verte.value(1)
    time.sleep(2)
 
    eteindre_feu()
 
# Tester un buzzer
def tester_buzzer(buzzer, nom, frequence):
    print("Test :", nom)
 
    buzzer.freq(frequence)
    buzzer.duty(512)
 
    time.sleep(1)
 
    buzzer.duty(0)
    time.sleep(0.5)
 
# Programme principal
try:
    while True:
 
        # Test du feu tricolore
        tester_feu()
 
        # Test du buzzer du joueur 1
        tester_buzzer(buzzer_1, "Buzzer J1", 1000)
 
        # Test du buzzer du joueur 2
        tester_buzzer(buzzer_2, "Buzzer J2", 1500)
 
        print("Cycle de test termine")
        time.sleep(2)
 
except KeyboardInterrupt:
    print("Test interrompu")
 
finally:
    # Tout eteindre a la fin
    eteindre_feu()
 
    buzzer_1.duty(0)
    buzzer_2.duty(0)
 
    buzzer_1.deinit()
    buzzer_2.deinit()