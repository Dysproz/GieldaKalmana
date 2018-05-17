'''
Kod realizujacy przewidywania cen na gieldzie
wykorzystujac Filtr Kalmana

autor: Szymon Piotr Krasuski
Maj 2017
'''

# Dodanie bibliotek
import pandas
import os
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import inv
from tkinter import Tk
from tkinter import filedialog
import tkinter as tk


#Funkcja Filtru Kalmana
def filtrKalmana(x, cena, P):
    #Deklaracja wartosci T, Q, R
    T=1
    Q=1
    R=1
    #Deklaracja macierzy A,B, C
    A = np.matrix([[1, T],[0, 1]])
    B = np.matrix([[0.5*T*T],[T]])
    C = np.matrix([ 1, 0])
    #Obliczenia wartosci na podstawie dostarczonych danych
    Pprog = np.dot(np.dot(A, P), A.transpose()) + np.dot(np.dot(B, Q), B.transpose())
    K = np.dot((np.dot(Pprog, C.transpose())), inv(np.dot(np.dot(C, Pprog), C.transpose()) + R))
    Pnast = np.dot((np.eye(x.shape[1]) - np.dot(K, C)), Pprog)
    xprog = np.dot(A, x)
    eps = np.array([cena]) - np.dot(C, xprog)
    xest = xprog + np.dot(K, eps)
    #print(Pprog)
    return xprog, xest, Pnast
'''
def ApplicationFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.graph
'''
# Zaladuj cene zakonczenia z kazdego dnia z pliku .csv; cena znajduje sie w kolumnie 4 oraz pierwszy wiersz jest pomijany, poniewaz zawiera nazwe kolumny
Tk().withdraw() #prevent from opening window
url = filedialog.askopenfilename() #choose .csv file from explorer and save path to url
#url = "~/Documents/PythonScripts/FiltrKalmana/AAPL.csv" #path to .csv file with prices. Path defined in code
names = ['price']
dataset = pandas.read_csv(url, usecols=[4], skiprows=1, names=names) # import only 4th column with Close prices and skip first row with 'Close'


#odczyt ilosci dni analizowanych
length = dataset.shape[0]

#wstepna deklaracja wartosci stanu
state = np.matrix([dataset.iloc[0], 0]).transpose() #druga wartosc moze byc zmieniana np. -10 np. 0 itd.


#Wstepna deklaracja mcierzy P jako macierzy jednostkowej 2x2
P = np.eye(2)
#deklaracja listy prognoza do przechowywania prognozowanych wartosci
prognoza = []
#deklaracja pierwszej wartosci
prognoza.append(dataset.iloc[0])
#petla lecaca  po kolejnych dniach na gieldzie i przewidujaca ceny z funkcji FiltrKalmana
for x in range(1, length):
    prog, state, P = filtrKalmana(state, dataset.iloc[x], P)
    #wynik dolacza do listy prognoza
    prognoza.append(prog[0])

#dostosowanie listy prognoza do 2wymiarowej tablicy numpy
prognoza = np.array(prognoza)
#Jesli rozmiar przekonwertowanej macierzy jest 3d, to to polecenie niszczy 3 wymiar
#prognoza = prognoza[:,:,0]

#Wyswietlenie wykresu ceny rzeczywistej i prognozowanej
#cena rzeczywista
plt.plot(dataset, 'b-', label='Cena rzeczywista')
#cena prognozowana
plt.plot( prognoza, 'r--', label='Cena prognozowana')
#wlaczenie siatki
plt.grid(True)
#wlaczenie tytulu wykresu, podpisy osi X oraz Y
plt.title('Filtr Kalmana')
plt.xlabel('Dzień')
plt.ylabel('Cena')
#umieszczenie legendy w dolym prawym roku
plt.legend(loc='lower right')
#wyswietlenie wykresu
plt.show()

'''
roznica = prognoza - dataset
roznica=np.array(roznica)
dataset = np.array(dataset)
akuratne=0
dozwolonyOdchyl=0
sredniOdchyl = 0
for x in range(0, length):
    if roznica[x]==0:
        akuratne=akuratne+1

for j in range(0,length-1):
    if roznica



procentSukcesu = (akuratne/length)*100
procentOdchyluDozwolonego = (dozwolonyOdchyl/length)*100
print(akuratne)
print(procentSukcesu)
print(dozwolonyOdchyl)
print(procentOdchyluDozwolonego)
'''
