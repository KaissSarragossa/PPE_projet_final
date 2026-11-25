from machine import ADC, Pin
import time
from pins import Pins
 
# Configuration des capteurs
capteur_1 = ADC(Pin(Pins.A0))
capteur_2 = ADC(Pin(Pins.A1))
 
capteur_1.atten(ADC.ATTN_11DB)
capteur_2.atten(ADC.ATTN_11DB)
 
# Calibration des capteurs
print("Calibration des capteurs...")
 
total_1 = 0
total_2 = 0
 
for i in range(20):
    total_1 += capteur_1.read()
    total_2 += capteur_2.read()
    time.sleep(0.05)
 
reference_1 = total_1 // 20
reference_2 = total_2 // 20
 
print("Reference J1 :", reference_1)
print("Reference J2 :", reference_2)
 
# Seuils de detection
seuil_couvert_1 = int(reference_1 * 0.30)
seuil_decouvert_1 = int(reference_1 * 0.50)
 
seuil_couvert_2 = int(reference_2 * 0.30)
seuil_decouvert_2 = int(reference_2 * 0.50)
 
# Etats des capteurs
couvert_1 = False
couvert_2 = False
 
# Boucle de test
try:
    while True:
        valeur_1 = capteur_1.read()
        valeur_2 = capteur_2.read()
 
        # Detection du joueur 1 avec hysteresis
        if valeur_1 < seuil_couvert_1:
            couvert_1 = True
        elif valeur_1 > seuil_decouvert_1:
            couvert_1 = False
 
        # Detection du joueur 2 avec hysteresis
        if valeur_2 < seuil_couvert_2:
            couvert_2 = True
        elif valeur_2 > seuil_decouvert_2:
            couvert_2 = False
 
        print("----------------------")
        print("Joueur 1 :", valeur_1)
        print("Etat J1 :", "COUVERT" if couvert_1 else "DECOUVERT")
 
        print("Joueur 2 :", valeur_2)
        print("Etat J2 :", "COUVERT" if couvert_2 else "DECOUVERT")
 
        time.sleep(0.2)
 
except KeyboardInterrupt:
    print("Test des capteurs termine.")