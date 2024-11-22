from tkinter import messagebox
import re
class Articolo:
    def __init__(self, prezzo=0.0, categoria='', descrizione='', marca='', taglia=0):
        self.prezzo = prezzo
        self.categoria = categoria
        self.descrizione = descrizione
        self.marca = marca
        self.taglia = taglia

    def get_descrizione(self):
        return self.descrizione

    def set_descrizione(self, descrizione):
        if not descrizione:
            raise ValueError("La descrizione non può essere vuota.")
        self.descrizione = descrizione

    def get_taglia(self):
        return self.taglia

    def set_taglia(self, taglia_str):
        if not taglia_str:
            raise ValueError("La taglia non può essere vuota.")
        valid_taglie = {36, 38, 40, 42, 44, 46, 48, 50, 52}
        try:
            taglia = int(taglia_str)
        except ValueError:
            raise ValueError("La taglia deve essere un numero intero valido.")
        if taglia not in valid_taglie:
            raise ValueError("La taglia deve essere un numero intero compreso tra: ", valid_taglie)
        else:
            self.taglia = taglia

    def get_categoria_merceologica(self):
        return self.categoria

    def set_categoria_merceologica(self, categoria):
        if not categoria:
            raise ValueError("La categoria non può essere vuota.")
        self.categoria = categoria

    def get_marca(self):
        return self.marca

    def set_marca(self, marca):
        if not marca:
            raise ValueError("La marca non può essere vuota.")
        self.marca = marca

    def get_prezzo(self):
        return self.prezzo

    def set_prezzo(self, prezzo_str):

        if not prezzo_str:
            raise ValueError("Il prezzo non può essere vuoto.")
        if not re.match(r'^\d+(\.\d{1,2})?$', prezzo_str):
            raise ValueError("Il prezzo deve essere un numero decimale con al massimo 2 cifre dopo il punto.")
        prezzo = float(prezzo_str)
        if prezzo < 0:
            raise ValueError("Il prezzo non può essere negativo.")
        self.prezzo = prezzo

    def generarigasalvataggio(self):
        return f"{self.descrizione}|{self.marca}|{self.categoria}|{self.taglia}|{self.prezzo}"

    def caricarigasalvataggio(self, riga):
        campi = riga.split('|')
        if len(campi) != 5:
            raise ValueError("Formato riga non valido: deve contenere 5 campi separati da '|'.")
        else:
            self.descrizione = campi[0]
            self.marca = campi[1]
            self.categoria = campi[2]
            self.taglia = int(campi[3])
            self.prezzo = float(campi[4])
        return None