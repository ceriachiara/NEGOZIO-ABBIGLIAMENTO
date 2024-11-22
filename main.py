import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from articoli import Articoli
from articolo import Articolo
from date import Date
from file_manager import FileManager
from vendite import Vendite
class Negozio:
    def __init__(self):
        self.mioarticolo = Articolo()
        self.giornovendita = Date()
        self.file_manager = FileManager("filearticoli.txt", "filevendite.txt")
        self.elenco = Articoli()
        self.magazzino = Vendite()
        self.articoli_caricati = self.file_manager.carica_articoli()
        for articolo in self.articoli_caricati:
            if self.magazzino.add_elemento(articolo) != 0:
                messagebox.showerror("Errore", "Magazzino pieno: gli articoli salvati su file superano il numero massimo di articoli inseribili.")
                break

    def stampa_elencoarticoli(self, output):
        output.delete('1.0', tk.END)
        output.insert(tk.END, "ELENCO ARTICOLI:\n")
        n = self.magazzino.get_n()
        for i in range(n):
            x = i + 1
            output.insert(tk.END, f"ARTICOLO {x}\n")
            mioarticolo = self.magazzino.get_elementodaelencoarticoli(i)
            if mioarticolo:
                output.insert(tk.END, f"MARCA: {mioarticolo.get_marca()}\n")
                output.insert(tk.END, f"CATEGORIA: {mioarticolo.get_categoria_merceologica()}\n")
                output.insert(tk.END, f"PREZZO: {mioarticolo.get_prezzo():.2f} €\n")
                output.insert(tk.END, f"TAGLIA: {mioarticolo.get_taglia()}\n")
                output.insert(tk.END, f"DESCRIZIONE: {mioarticolo.get_descrizione()}\n")
                output.insert(tk.END, "...............................................\n")

    def stampa_listacapiacquistati(self, output):
        output.delete('1.0', tk.END)
        output.insert(tk.END, "ARTICOLI ACQUISTATI:\n")
        n = self.magazzino.get_numerovendite()
        for i in range(n):
            x = i + 1
            output.insert(tk.END, f"ARTICOLO {x}\n")
            mioarticolo = self.magazzino.get_elementodalistacapiacquistati(i)
            output.insert(tk.END, f"MARCA: {mioarticolo.get_marca()}\n")
            output.insert(tk.END, f"CATEGORIA: {mioarticolo.get_categoria_merceologica()}\n")
            output.insert(tk.END, f"PREZZO: {mioarticolo.get_prezzo():.2f} €\n")
            output.insert(tk.END, f"TAGLIA: {mioarticolo.get_taglia()}\n")
            output.insert(tk.END, f"DESCRIZIONE: {mioarticolo.get_descrizione()}\n")
            anno, mese, giorno = self.magazzino.estrai_data(i)
            output.insert(tk.END, f"DATA: {giorno}/{mese}/{anno}\n")
            output.insert(tk.END, "...............................................\n")

    def aggiungi_articolo(self):
        self.output.delete(1.0, tk.END)
        try:
            prezzo_str = self.entry_prezzo.get().strip()
            marca = self.entry_marca.get().strip()
            taglia = self.entry_taglia.get()
            categoria = self.entry_categoria.get().strip()
            descrizione = self.entry_descrizione.get().strip()
            qty = self.entry_qty.get()
            if not qty:
                raise ValueError("La quantità non può essere vuota.")
            try:
                qty = int(self.entry_qty.get())
            except ValueError:
                raise ValueError("La quantità deve essere un numero intero valido.")
            if qty <= 0:
                raise ValueError("La quantità deve essere maggiore di zero.")
            if self.magazzino.get_n() + qty > Articoli.MAX:
                raise ValueError(f"Non è possibile aggiungere {qty} articoli. Supererebbe il massimo consentito di {Articoli.MAX} articoli.")
            else:
                for _ in range(qty):
                    mioarticolo = Articolo()
                    mioarticolo.set_prezzo(prezzo_str)
                    mioarticolo.set_categoria_merceologica(categoria)
                    mioarticolo.set_descrizione(descrizione)
                    mioarticolo.set_marca(marca)
                    mioarticolo.set_taglia(taglia)
                    if self.magazzino.add_elemento(mioarticolo) != 0:
                        messagebox.showerror("Errore", "Magazzino pieno.")
                        break
                messagebox.showinfo("Successo", "Articoli aggiunti con successo.")
                self.reset_campi()
        except ValueError as ve:
            messagebox.showerror("Errore", f"Errore nei dati inseriti: {ve}")

    def elimina_articolo(self):
        self.output.delete(1.0, tk.END)
        articolodaeliminare = self.entry_elimina_articolo.get()
        if not articolodaeliminare:
            messagebox.showerror("Errore", "L'ID articolo da eliminare non può essere vuoto.")
        try:
            articolodaeliminare = int(self.entry_elimina_articolo.get()) - 1
            if self.magazzino.rimuoviarticolo(None, articolodaeliminare) != -1:
                messagebox.showinfo("Successo", "Articolo eliminato con successo.")
            else:
                messagebox.showerror("Errore", "ID articolo non valido.")
            self.reset_campi()
        except ValueError:
            messagebox.showerror("Errore", "ID articolo non valido.")

    def modifica_articolo(self):
        self.output.delete(1.0, tk.END)
        articolo_id = self.entry_aggiorna_id.get()
        if not articolo_id:
            messagebox.showerror("Errore", "L'ID articolo non può essere vuoto.")
        try:
            articolo_id = int(self.entry_aggiorna_id.get()) - 1
            if 0 <= articolo_id < self.magazzino.get_n():
                articolo = self.magazzino.get_elementodaelencoarticoli(articolo_id)
                if articolo:
                    if self.entry_aggiorna_prezzo.get():
                        articolo.set_prezzo(self.entry_aggiorna_prezzo.get())
                    if self.entry_aggiorna_marca.get():
                        articolo.set_marca(self.entry_aggiorna_marca.get())
                    if self.entry_aggiorna_taglia.get():
                        articolo.set_taglia(self.entry_aggiorna_taglia.get())
                    if self.entry_aggiorna_categoria.get():
                        articolo.set_categoria_merceologica(self.entry_aggiorna_categoria.get())
                    if self.entry_aggiorna_descrizione.get():
                        articolo.set_descrizione(self.entry_aggiorna_descrizione.get())
                    messagebox.showinfo("Successo", "Articolo aggiornato con successo.")
                    self.reset_campi()
                else:
                    messagebox.showerror("Errore", "Articolo non trovato.")
            else:
                messagebox.showerror("Errore", "ID articolo non valido.")
        except ValueError:
            messagebox.showerror("Errore", "ID articolo non valido.")

    def vendi_articolo(self):
        self.output.delete(1.0, tk.END)
        try:
            articolovenduto_index = int(self.entry_vendi_articolo.get()) - 1
            if 0 <= articolovenduto_index < self.magazzino.get_n():
                gg = int(self.entry_giorno.get())
                mm = int(self.entry_mese.get())
                aaaa = int(self.entry_anno.get())
                giornovendita = Date(gg, mm, aaaa)
                if not giornovendita.is_valid():
                    messagebox.showerror("Errore", "Data non valida.")
                    return
                self.magazzino.venditaarticolo(self.magazzino, articolovenduto_index)
                self.magazzino.add_data(giornovendita)
                self.magazzino.rimuoviarticolo(self.magazzino, articolovenduto_index)
                messagebox.showinfo("Successo", "Articolo venduto con successo.")
            else:
                messagebox.showerror("Errore", "Articolo non valido.")
            self.reset_campi()
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori validi.")

    def calcola_incassi(self):
        self.output.delete(1.0, tk.END)
        try:
            anno = int(self.entry_anno_incassi.get())
            mese = int(self.entry_mese_incassi.get())
            incassi = (self.magazzino.incassimensili(anno, mese))
            self.output.insert(tk.END, f"Incassi totali per {mese}/{anno}: € {incassi:.2F}\n")
            self.reset_campi()
        except ValueError as ve:
            messagebox.showerror("Errore", f"Errore nei dati inseriti: {ve}")

    def ordina_articoli_venduti(self):
        self.output.delete(1.0, tk.END)
        venduti_ordinati = sorted(zip(self.magazzino.capiacquistati, range(len(self.magazzino.datevendita))),key=lambda x: "-".join(map(str, self.magazzino.estrai_data(x[1]))))
        self.output.insert(tk.END, "ARTICOLI VENDUTI ORDINATI PER DATA:\n\n")
        for articolo, indice_data in venduti_ordinati:
            if articolo.get_descrizione():
                self.output.insert(tk.END, f"MARCA: {articolo.get_marca()}\n")
                self.output.insert(tk.END, f"CATEGORIA: {articolo.get_categoria_merceologica()}\n")
                self.output.insert(tk.END, f"PREZZO: {articolo.get_prezzo():.2f}\n")
                self.output.insert(tk.END, f"TAGLIA: {articolo.get_taglia()}\n")
                self.output.insert(tk.END, f"DESCRIZIONE: {articolo.get_descrizione()}\n")
                anno, mese, giorno = self.magazzino.estrai_data(indice_data)
                self.output.insert(tk.END, f"DATA: {giorno}/{mese}/{anno}\n")
                self.output.insert(tk.END, "......................................\n\n")

    def report(self):
        self.output.delete(1.0, tk.END)
        try:
            a = int(self.entry_anno_report.get())
            venditeannuali = 0
            incassiannuali = 0.0
            arrayincassimensili = np.zeros(12)
            self.output.insert(tk.END, f"REPORT INCASSI ANNO {a} :\n\n")
            for i in range(12):
                b = i + 1
                vendite_mensili = self.magazzino.venditemensili(a, b)
                incassi_mensili = self.magazzino.incassimensili(a, b)
                self.output.insert(tk.END, f"Mese {b} :")
                self.output.insert(tk.END, f"\nVendite: {vendite_mensili}")
                self.output.insert(tk.END, f"\nIncassi: € {incassi_mensili:.2f}\n")
                x = int(self.magazzino.venditemensili(a, b))
                venditeannuali = venditeannuali + x
                y = float(self.magazzino.incassimensili(a, b))
                arrayincassimensili[i] = self.magazzino.incassimensili(a, b)
                incassiannuali = incassiannuali + y
                if x != 0:
                    mediacapomensile = y / x
                else:
                    mediacapomensile = 0.0
                self.output.insert(tk.END, f"PREZZO MEDIO ARTICOLO VENDUTO NEL MESE {b}: € {mediacapomensile:.2f}\n")
                self.output.insert(tk.END, f"------------------------------------\n")
            if venditeannuali != 0:
                mediacapoannuale = incassiannuali / venditeannuali
            else:
                mediacapoannuale = 0.0
            mediaannuale = incassiannuali / 12
            self.output.insert(tk.END, f"\nPREZZO MEDIO DEL CAPO ACQUISTATO NELL'ANNO {a}: € {mediacapoannuale:.2f}\n")
            self.output.insert(tk.END, f"GUADAGNO MENSILE MEDIO NELL'ANNO {a}: € {mediaannuale:.2f}\n")
            self.output.insert(tk.END, f"GUADAGNO ANNUALE TOTALE: € {incassiannuali:.2f}\n")
            mesilabel = np.arange(1, 13)
            plt.plot(mesilabel, arrayincassimensili, marker="o", color='purple')
            plt.title("INCASSI ANNO: " + str(a))
            plt.xlabel("MESI")
            plt.ylabel("INCASSI")
            plt.show()
            self.output.update_idletasks()
        except ValueError:
            messagebox.showerror("Errore", "Anno non valido.")

    def salva_su_file(self):
        self.file_manager.salva_articoli(self.magazzino)

    def salva_vendite_su_file(self):
        self.file_manager.salva_vendite(self.magazzino)

    def pulisci_output(self):
        self.output.delete('1.0', tk.END)

    def reset_campi(self):
        self.entry_prezzo.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_taglia.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.entry_descrizione.delete(0, tk.END)
        self.entry_qty.delete(0, tk.END)
        self.entry_elimina_articolo.delete(0, tk.END)
        self.entry_vendi_articolo.delete(0, tk.END)
        self.entry_giorno.delete(0, tk.END)
        self.entry_mese.delete(0, tk.END)
        self.entry_anno.delete(0, tk.END)
        self.entry_anno_incassi.delete(0, tk.END)
        self.entry_mese_incassi.delete(0, tk.END)
        self.entry_aggiorna_id.delete(0, tk.END)
        self.entry_aggiorna_prezzo.delete(0, tk.END)
        self.entry_aggiorna_marca.delete(0, tk.END)
        self.entry_aggiorna_taglia.delete(0, tk.END)
        self.entry_aggiorna_categoria.delete(0, tk.END)
        self.entry_aggiorna_descrizione.delete(0, tk.END)
        self.entry_anno_report.delete(0, tk.END)

    def stampa_elenco_articoli(self):
        self.stampa_elencoarticoli(self.output)

    def stampa_articoli_acquistati(self):
        self.stampa_listacapiacquistati(self.output)

    def main(self):
        root = tk.Tk()
        root.title("Gestione Magazzino Negozio di Abbigliamento")
        root.geometry("950x650")

        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        left_frame = tk.Frame(scrollable_frame, bg="lavender")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        right_frame = tk.Frame(scrollable_frame, bg="lavender")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=1, pady=10)

        frame_gestione = tk.LabelFrame(left_frame, text="Gestione Articoli", bg="lavender", font=('Helvetica', 12, 'bold'), padx=10, pady=10)
        frame_gestione.pack(fill=tk.X, padx=5, pady=5)

        # agg.articolo
        lbl_prezzo = tk.Label(frame_gestione, text="Prezzo:", bg="lavender", font=('Helvetica', 10))
        lbl_prezzo.grid(row=0, column=0, sticky='e')
        self.entry_prezzo = tk.Entry(frame_gestione)
        self.entry_prezzo.grid(row=0, column=1, sticky='w ')

        lbl_marca = tk.Label(frame_gestione, text="Marca:", bg="lavender", font=('Helvetica', 10))
        lbl_marca.grid(row=1, column=0, sticky='e')
        self.entry_marca = tk.Entry(frame_gestione)
        self.entry_marca.grid(row=1, column=1, sticky='w')

        lbl_taglia = tk.Label(frame_gestione, text="Taglia:", bg="lavender", font=('Helvetica', 10))
        lbl_taglia.grid(row=2, column=0, sticky='e')
        self.entry_taglia = tk.Entry(frame_gestione)
        self.entry_taglia.grid(row=2, column=1, sticky='w')

        lbl_categoria = tk.Label(frame_gestione, text="Categoria:", bg="lavender", font=('Helvetica', 10))
        lbl_categoria.grid(row=3, column=0, sticky='e')
        self.entry_categoria = tk.Entry(frame_gestione)
        self.entry_categoria.grid(row=3, column=1, sticky='w')

        lbl_descrizione = tk.Label(frame_gestione, text="Descrizione:", bg="lavender", font=('Helvetica', 10))
        lbl_descrizione.grid(row=4, column=0, sticky='e')
        self.entry_descrizione = tk.Entry(frame_gestione)
        self.entry_descrizione.grid(row=4, column=1, sticky='w')

        lbl_qty = tk.Label(frame_gestione, text="Quantità:", bg="lavender", font=('Helvetica', 10))
        lbl_qty.grid(row=5, column=0, sticky='e')
        self.entry_qty = tk.Entry(frame_gestione)
        self.entry_qty.grid(row=5, column=1, sticky='w')

        btn_aggiungi = tk.Button(frame_gestione, text="Aggiungi Articolo", command=self.aggiungi_articolo, bg="MediumPurple1",
                                 font=('Helvetica', 10))
        btn_aggiungi.grid(row=6, column=0, columnspan=2, pady=5, sticky='nsew')

        # elm.articolo
        lbl_elimina_articolo = tk.Label(frame_gestione, text="ID Articolo da Eliminare:", bg="lavender",
                                    font=('Helvetica', 10))
        lbl_elimina_articolo.grid(row=7, column=0, sticky='e')
        self.entry_elimina_articolo = tk.Entry(frame_gestione)
        self.entry_elimina_articolo.grid(row=7, column=1, sticky='w')

        btn_elimina = tk.Button(frame_gestione, text="Elimina Articolo", command=self.elimina_articolo, bg="MediumPurple1",
                            font=('Helvetica', 10))
        btn_elimina.grid(row=8, column=0, columnspan=2, pady=5, sticky='nsew')

        # mod.articolo
        lbl_aggiorna_id = tk.Label(frame_gestione, text="ID Articolo da Modificare:", bg="lavender", font=('Helvetica', 10))
        lbl_aggiorna_id.grid(row=9, column=0, sticky='e')
        self.entry_aggiorna_id = tk.Entry(frame_gestione)
        self.entry_aggiorna_id.grid(row=9, column=1, sticky='w')

        lbl_aggiorna_prezzo = tk.Label(frame_gestione, text="Nuovo Prezzo:", bg="lavender", font=('Helvetica', 10))
        lbl_aggiorna_prezzo.grid(row=10, column=0, sticky='e')
        self.entry_aggiorna_prezzo = tk.Entry(frame_gestione)
        self.entry_aggiorna_prezzo.grid(row=10, column=1, sticky='w')

        lbl_aggiorna_marca = tk.Label(frame_gestione, text="Nuova Marca:", bg="lavender", font=('Helvetica', 10))
        lbl_aggiorna_marca.grid(row=11, column=0, sticky='e')
        self.entry_aggiorna_marca = tk.Entry(frame_gestione)
        self.entry_aggiorna_marca.grid(row=11, column=1, sticky='w')

        lbl_aggiorna_taglia = tk.Label(frame_gestione, text="Nuova Taglia:", bg="lavender", font=('Helvetica', 10))
        lbl_aggiorna_taglia.grid(row=12, column=0, sticky='e')
        self.entry_aggiorna_taglia = tk.Entry(frame_gestione)
        self.entry_aggiorna_taglia.grid(row=12, column=1, sticky='w')

        lbl_aggiorna_categoria = tk.Label(frame_gestione, text="Nuova Categoria:", bg="lavender", font=('Helvetica', 10))
        lbl_aggiorna_categoria.grid(row=13, column=0, sticky='e')
        self.entry_aggiorna_categoria = tk.Entry(frame_gestione)
        self.entry_aggiorna_categoria.grid(row=13, column=1, sticky='w')

        lbl_aggiorna_descrizione = tk.Label(frame_gestione, text="Nuova Descrizione:", bg="lavender",
                                        font=('Helvetica', 10))
        lbl_aggiorna_descrizione.grid(row=14, column=0, sticky='e')
        self.entry_aggiorna_descrizione = tk.Entry(frame_gestione)
        self.entry_aggiorna_descrizione.grid(row=14, column=1, sticky='w')

        btn_modifica = tk.Button(frame_gestione, text="Modifica Articolo", command=self.modifica_articolo, bg="MediumPurple1",
                                 font=('Helvetica', 10))
        btn_modifica.grid(row=15, column=0, columnspan=2, pady=5, sticky='nsew')


        frame_vendita = tk.LabelFrame(left_frame, text="Vendita e Incassi", bg="lavender", font=('Helvetica', 12, 'bold'),
                                  padx=10, pady=10)
        frame_vendita.pack(fill=tk.X, padx=5, pady=5)

        # ven.
        lbl_vendi_articolo = tk.Label(frame_vendita, text="ID Articolo da Vendere:", bg="lavender", font=('Helvetica', 10))
        lbl_vendi_articolo.grid(row=0, column=0, sticky='e')
        self.entry_vendi_articolo = tk.Entry(frame_vendita)
        self.entry_vendi_articolo.grid(row=0, column=1, sticky='w')

        lbl_giorno = tk.Label(frame_vendita, text="Giorno:", bg="lavender", font=('Helvetica', 10))
        lbl_giorno.grid(row=1, column=0, sticky='e')
        self.entry_giorno = tk.Entry(frame_vendita)
        self.entry_giorno.grid(row=1, column=1, sticky='w')

        lbl_mese = tk.Label(frame_vendita, text="Mese:", bg="lavender", font=('Helvetica', 10))
        lbl_mese.grid(row=2, column=0, sticky='e')
        self.entry_mese = tk.Entry(frame_vendita)
        self.entry_mese.grid(row=2, column=1, sticky='w')

        lbl_anno = tk.Label(frame_vendita, text="Anno:", bg="lavender", font=('Helvetica', 10))
        lbl_anno.grid(row=3, column=0, sticky='e')
        self.entry_anno = tk.Entry(frame_vendita)
        self.entry_anno.grid(row=3, column=1, sticky='w')

        btn_vendi = tk.Button(frame_vendita, text="Vendi Articolo", command=self.vendi_articolo, bg="RoyalBlue1",
                          font=('Helvetica', 10))
        btn_vendi.grid(row=4, column=0, columnspan=2, pady=5, sticky='nsew')

        # inc.
        lbl_anno_incassi = tk.Label(frame_vendita, text="Anno Incassi:", bg="lavender", font=('Helvetica', 10))
        lbl_anno_incassi.grid(row=5, column=0, sticky='e')
        self.entry_anno_incassi = tk.Entry(frame_vendita)
        self.entry_anno_incassi.grid(row=5, column=1, sticky='w')

        lbl_mese_incassi = tk.Label(frame_vendita, text="Mese Incassi:", bg="lavender", font=('Helvetica', 10))
        lbl_mese_incassi.grid(row=6, column=0, sticky='e')
        self.entry_mese_incassi = tk.Entry(frame_vendita)
        self.entry_mese_incassi.grid(row=6, column=1, sticky='w')

        btn_incassi = tk.Button(frame_vendita, text="Calcola Incassi", command=self.calcola_incassi, bg="RoyalBlue1",
                            font=('Helvetica', 10))
        btn_incassi.grid(row=7, column=0, columnspan=2, pady=5, sticky='nsew')

        # ord.
        btn_ordina_venduti = tk.Button(frame_vendita, text="Ordina Articoli Venduti per Data",
                                      command=self.ordina_articoli_venduti, bg="RoyalBlue1", font=('Helvetica', 10))
        btn_ordina_venduti.grid(row=8, column=0, columnspan=2, pady=5, sticky='nsew')

        # rep.
        lbl_anno_report = tk.Label(frame_vendita, text="Anno report:", bg="lavender", font=('Helvetica', 10))
        lbl_anno_report.grid(row=9, column=0, sticky='e')
        self.entry_anno_report = tk.Entry(frame_vendita)
        self.entry_anno_report.grid(row=9, column=1, sticky='w')
        btn_report = tk.Button(frame_vendita, text="Report annuale vendite",
                                   command=self.report, bg="RoyalBlue1", font=('Helvetica', 10))
        btn_report.grid(row=10, column=0, columnspan=2, pady=5, sticky='nsew')

        # sal.
        frame_salva_su_file = tk.LabelFrame(left_frame, text="Salva su file", bg="lavender", font=('Helvetica', 12, 'bold'),
                                 padx=10, pady=10)
        frame_salva_su_file.pack(fill=tk.X, padx=5, pady=5)

        btn_salva_su_file = tk.Button(frame_salva_su_file, text="Salva su file", command=self.salva_su_file,
                                  bg="plum1", font=('Helvetica', 10))
        btn_salva_su_file.pack(fill=tk.X, pady=5)

        #sal. vendite
        frame_salva_su_file = tk.LabelFrame(left_frame, text="Salva vendite", bg="lavender", font=('Helvetica', 12, 'bold'),
                                 padx=10, pady=10)
        frame_salva_su_file.pack(fill=tk.X, padx=5, pady=5)

        btn_salva_vendite = tk.Button(frame_salva_su_file, text="Salva vendite", command=self.salva_vendite_su_file,
                                  bg="plum1", font=('Helvetica', 10))
        btn_salva_vendite.pack(fill=tk.X, pady=5)

        # stamp.
        frame_stampa = tk.LabelFrame(left_frame, text="Stampa Articoli", bg="lavender", font=('Helvetica', 12, 'bold'),
                                 padx=10, pady=10)
        frame_stampa.pack(fill=tk.X, padx=5, pady=5)

        btn_stampa_elenco = tk.Button(frame_stampa, text="Stampa Elenco Articoli", command=self.stampa_elenco_articoli,
                                  bg="MediumOrchid1", font=('Helvetica', 10))
        btn_stampa_elenco.pack(fill=tk.X, pady=5)

        btn_stampa_acquistati = tk.Button(frame_stampa, text="Stampa Articoli Venduti", command=self.stampa_articoli_acquistati,
                                      bg="MediumOrchid1", font=('Helvetica', 10))
        btn_stampa_acquistati.pack(fill=tk.X, pady=5)

        btn_pulisci_output = tk.Button(frame_stampa, text="Pulisci Output", command=self.pulisci_output, bg="MediumOrchid1",
                                   font=('Helvetica', 10))
        btn_pulisci_output.pack(fill=tk.X, pady=5)

        output_label = tk.Label(right_frame, text="NEGOZIO DI ABBIGLIAMENTO", font=('Helvetica', 12, 'bold'), bg="lavender")
        output_label.pack(pady=5)

        self.output = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=('Helvetica', 10))
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        root.mainloop()


if __name__ == "__main__":

    negozio = Negozio()
    negozio.main()
