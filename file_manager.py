from articoli import Articoli
from articolo import Articolo
import tkinter as tk
from tkinter import messagebox, scrolledtext
from vendite import Vendite

class FileManager:
    def __init__(self, articoli_file="filearticoli.txt", vendite_file="filevendite.txt"):
        self.articoli_file = articoli_file
        self.vendite_file = vendite_file

    def salva_articoli(self, magazzino):
        try:
            with open(self.articoli_file, 'w') as file:
                for i in range(magazzino.get_n()):
                    articolo = magazzino.get_elementodaelencoarticoli(i)
                    if articolo is not None:
                        riga = articolo.generarigasalvataggio()
                        file.write(riga + "\n")
                messagebox.showinfo("Successo", "Articolo salvato con successo!")
        except FileNotFoundError:
            messagebox.showerror("Errore", "File non trovato.")
        except IOError:
            messagebox.showerror("Errore", "Errore nel salvataggio articoli.")
        return None

    def carica_articoli(self):
        try:
            with open(self.articoli_file, 'r') as file:
                if file.readable() and file.read().strip() == "":
                    return []
                file.seek(0)
                articoli = []
                for riga in file:
                    articolo = Articolo()
                    try:
                        articolo.caricarigasalvataggio(riga.strip())
                        articoli.append(articolo)
                    except ValueError as e:
                        messagebox.showerror("Errore", f"Errore nel caricamento dell'articolo: {e}")
                        articolo.descrizione = "ERRORE CARICAMENTO ARTICOLO"
                        articolo.prezzo = 0.0
                        articolo.marca = "ERRORE CARICAMENTO ARTICOLO"
                        articolo.categoria = "ERRORE CARICAMENTO ARTICOLO"
                        articolo.taglia = 0
                        articoli.append(articolo)
        except FileNotFoundError:
            messagebox.showerror("Errore", "File non trovato.")
            return []
        except IOError:
            messagebox.showerror("Errore", "Errore nel caricamento articoli.")
            return []
        return articoli

    def salva_vendite(self, magazzino):

        try:
            with open(self.vendite_file, 'w') as file:
                for i in range(magazzino.get_numerovendite()):
                    articolovenduto = magazzino.get_elementodalistacapiacquistati(i)
                    if articolovenduto is not None:
                        riga = articolovenduto.generarigasalvataggio()
                        file.write(riga + "\n")
                messagebox.showinfo("Successo", "Articoli venduti salvati con successo!")
        except FileNotFoundError:
            messagebox.showerror("Errore", "File non trovato.")
        except IOError:
            messagebox.showerror("Errore", "Errore nel salvataggio vendite.")
        return None

