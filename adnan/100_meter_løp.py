import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Sette opp Variabler

massen_til_loperen = 80 # Kg Massen til løperen

#Kraften løperen dytter seg fram med
F = 400 #Newton


#Setter opp tiden
antall_steg = 1000
slutt_tid = 10 # omtrent tiden det tar for en olympisk 100 meter løper
tid = np.linspace(0,slutt_tid, antall_steg) # setter opp en array for tid
tids_steg = slutt_tid/antall_steg # bestemmer hvor mye tid skal gå mellom hvert punkt




#Variabler for luftmotstand
luft_tetthet = 1.293 # kg/m^3
areal = 0.45 # Tverrsnitt av løper
luft_faktor = 1.2 # Motstandsfaktor i luft
vind_styrke = 0 #  hastigheten til luften

#Variabler for oppstartsfasen av løpet når løperen er bøyd
F_grense = 25.8 # sN/m Kraften som er avhengig av farten fv
F_bøyd = 488  #N kraften løperen dytter med i starten   fc
tid_bøyd= 0.67 # Tiden løperen er bøyd i oppstartsfasen

#


def enkel_modell(): # Den enkle modellen ser bare på kraften som løperen dytter med.
    return F/massen_til_loperen


def forbedret_modell(v):
    #I denne modellen ser vi også på luftmotstanden
    return (F - (0.5*luft_tetthet*luft_faktor*areal*(v-vind_styrke)**2))/massen_til_loperen


def realistisk_modell(v, t):
    """Siden løperen begynner i en bøyd posisjon og har derfor mindre areal og en større kraft. Dette varer bare i en kort tid så vi bruker noen formler for å legge dette til
    """
    return (F + F_bøyd*np.exp(-(t/tid_bøyd)**2)-F_grense*v- ((0.5*luft_tetthet*luft_faktor*areal*(v - vind_styrke)**2))*(1-0.25*np.exp(-(t/tid_bøyd)**2)))/massen_til_loperen


#setter opp arrayer
akselerasjon = np.zeros(antall_steg)
fart = np.zeros(antall_steg)
posisjon = np.zeros(antall_steg)



#for løkke for Euler-Cromer metode

for element in range(antall_steg - 1):
    akselerasjon[element + 1] = realistisk_modell(fart[element], tid[element])
    fart[element + 1] = fart[element] + akselerasjon[element + 1] * tids_steg
    posisjon[element + 1] = posisjon[element] + fart[element + 1] * tids_steg


#for å finne tiden det tar å løpe 100 meter
for i in range(antall_steg-1):
    if posisjon[i]> 100:
        tid_brukt = tid[i]
        break

print(f"En olympisk løper bruker {tid_brukt:.2f} sekunder på 100 meter")






#Kode for å lage grafer for avstand hastighet og akselerasjon

sns.set()
fig, ax = plt.subplots(3, sharex = True,  figsize=(7,6.5) )
fig.suptitle("Modell for 100 meter lop")
plt.xlabel("Tid i sekunder")

ax[0].plot(tid,posisjon)
ax[0].set_ylabel("Avstand fra start [m]")

ax[1].plot(tid,fart)
ax[1].set_ylabel("Hastighet [m/s]")

ax[2].plot(tid,akselerasjon)
ax[2].set_ylabel("Akselerasjon [$m/s^2$]")


plt.show()
