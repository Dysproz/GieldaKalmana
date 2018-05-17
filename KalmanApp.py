'''
Proste GUI do drukowania wykresow przebiegow przewidzianych, a rzeczywistych, histogramow oraz ustawiania zmiennych.
'''
import pandas
import os
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import inv
from tkinter import Tk
from tkinter import filedialog
import tkinter as tk
import os
import matplotlib.patches as mpatches


#Aplikacja do oblusgi filtru
class Application(tk.Frame):
#funkcja tworzaca
    def __init__(self, master=None):
        master.minsize(width=600, height=600)
        super().__init__(master)
        self.pack()
        #wstepna deklaracja T, Q, R
        self.T=1
        self.Q=1
        self.R=1
        #Przypisanie wsystkich potrzebnych danych z pliku .csv
        self.PrzypiszWszystko()
        #przyciski, labele itp.
        self.create_widgets()




    def create_widgets(self):
        #przycisk do drukowania grafu
        self.graf=tk.Button(master=None, text="Graf\nporównujący ceny",width=50, height=3, background="#B0E0E6", command= lambda: self.Grafik(self.dataset, self.prognoza, self.nazwa))
        self.graf.pack()
        #Przycisk do drukowania histogramu
        self.graf=tk.Button(master=None, text="Histogram\nróznicy cen",width=50, height=3, background="#B0E0E6", command= lambda: self.Histogram())
        self.graf.pack()
        #Przycisk do otwarcia innego .csv
        self.nowy=tk.Button(master=None, text="Otwórz plik",bg="#90EE90",width=50, height=3, command= lambda: self.PrzypiszWszystko())
        self.nowy.pack()
        #Label + entry dla wartosci T
        self.ChooseT = tk.Label(master=None,bg="#B0C4DE", text="T: ")
        self.ChooseT.pack(side="left")
        self.t=tk.Entry(master=None)
        self.t.pack(side="left")
        #Label + entry dla wartosci Q
        self.ChooseQ = tk.Label(master=None,bg="#B0C4DE", text="Q: ")
        self.ChooseQ.pack(side="left")
        self.q=tk.Entry(master=None)
        self.q.pack(side="left")
        #Label + Entry dla wartosci R
        self.ChooseR = tk.Label(master=None,bg="#B0C4DE", text="R: ")
        self.ChooseR.pack(side="left")
        self.r=tk.Entry(master=None)
        self.r.pack(side="left")


        #Przycisk do zmiany wartosci T, Q, R na te z okienek
        self.ChangeLetters=tk.Button(master=None, text="Zmień dane", command= lambda: self.letters())
        self.ChangeLetters.pack(side="left")
        #Przycisk EXIT
        self.quit = tk.Button(master=None, text="EXIT", fg="#FFD700", background="#F08080",
                              command=root.destroy)
        self.quit.pack(side="bottom")





    #Funkcja do zmiany T, Q, R na odczytan ewartosci z okienek
    def letters(self):
        #sprawdzenie poprawnosci danych wejsciowych
        def isfloat(value):
            try:
                float(value)
                return float(value)
            except:
                return 1
        self.T=isfloat(self.t.get())
        self.Q=isfloat(self.q.get())
        self.R=isfloat(self.r.get())
        self.prognoza = self.MoneyShot(self.dataset)

#Funckja do odczytu danych z pliku
    def czytURL(self):
        url = filedialog.askopenfilename()
        names = ['price']
        dataset = pandas.read_csv(url, usecols=[4], skiprows=1, names=names) # import only 4th column with Close prices and skip first row with 'Close'
        nazwa=os.path.basename(url)
        return dataset, nazwa
    #Funkcja obliczajaca prognoze
    def MoneyShot(self,dataset):
        #Funkcja Filtru Kalmana
        def filtrKalmana(x, cena, P):
            #Deklaracja wartosci T, Q, R
            T=self.T
            Q=self.Q
            R=self.R
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
        #odczyt ilosci dni analizowanych
        self.length = dataset.shape[0]
        length = self.length
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
        return prognoza

    def Grafik(self, dataset, prognoza, nazwa):
        #Wyswietlenie wykresu ceny rzeczywistej i prognozowanej
        #cena rzeczywista

        plt.plot(self.dataset, 'b-', label='Cena rzeczywista')
        #cena prognozowana
        plt.plot( self.prognoza, 'r--', label='Cena prognozowana')
        #wlaczenie siatki
        plt.grid(True)
        #wlaczenie tytulu wykresu, podpisy osi X oraz Y
        plt.title(self.nazwa)
        plt.xlabel('Dzień')
        plt.ylabel('Cena')
        #umieszczenie legendy w dolym prawym roku
        plt.legend(loc='lower right')
        #wyswietlenie wykresu
        plt.show()

    #Funcja liczaca roznice wartosci przewidywanych wzgledem rzeczywistych
    def Odchyl(self):
        #obliczenie roznicy
        self.roznica=self.prognoza-self.dataset
        #wyliczneie srednich cen
        self.sredniaPrognoz = np.mean(self.prognoza)
        self.sredniaData = np.mean(self.dataset)
#Funkcja rysujaca histogram roznicy cen
    def Histogram(self):
        self.roznica=self.roznica.astype(float)

        self.roznica.plot.hist(alpha=1, bins=15, color='b', legend=None )
        plt.show()



#Funkcja do wywolania innych funkcji i przypisania najwazniejszych zmiennych
    def PrzypiszWszystko(self):
        self.dataset, self.nazwa = self.czytURL()
        self.prognoza = self.MoneyShot(self.dataset)
        self.Odchyl()

#Kod do wywolania okna
root = tk.Tk()
root.wm_title("Filtr Kalmana by Szymon Piotr Krasuski")
root.configure(background='#B0C4DE')
app = Application(master=root)
app.mainloop()
