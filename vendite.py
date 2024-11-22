from articoli import Articoli
from articolo import Articolo
from date import Date
import tkinter as tk
from tkinter import messagebox, scrolledtext

class Vendite(Articoli):
    def __init__(self):
        super().__init__()
        self.elenco = Articoli()
        self.numerovendite = 0
        self.capiacquistati = [Articolo() for _ in range(Articoli.MAX)]
        self.datevendita = [Date() for _ in range(Articoli.MAX)]

    def venditaarticolo(self, a, x):
        if self.get_n() <= 0 or x >= self.get_n() or x < 0:
            return -1
        articolo_venduto = self.get_elementodaelencoarticoli(x)
        self.capiacquistati[self.numerovendite] = articolo_venduto
        self.numerovendite += 1
        return 0

    def incassimensili(self, a, m):
        if a < 1900 or a > 2900:
            raise ValueError("Anno non valido.")
        if m < 1 or m > 12:
            raise ValueError("Mese non valido")
        p = 0.0
        for i in range(self.numerovendite):
            if self.datevendita[i].get_year() == a and self.datevendita[i].get_month() == m:
                p += self.capiacquistati[i].get_prezzo()
        return round(p, 2)

    def venditemensili(self, a, m):
        v = 0
        for i in range(self.numerovendite):
            if self.datevendita[i].get_year() == a and self.datevendita[i].get_month() == m:
                v += 1
        return v

    def get_numerovendite(self):
        return self.numerovendite

    def get_elementodalistacapiacquistati(self, index):
        if 0 <= index < self.numerovendite:
            return self.capiacquistati[index]
        return None

    def get_data(self, index):
        if 0 <= index < self.numerovendite:
            return self.datevendita[index]
        return None

    def estrai_data(self, index):
        data = self.get_data(index)
        if data is not None:
            return (data.get_year(), data.get_month(), data.get_day())
        else:
            return (None, None, None)

    def add_data(self, g):
        if self.numerovendite < Articoli.MAX:
            b = (self.numerovendite) - 1
            self.datevendita[b] = g
            return 0
        return -1

