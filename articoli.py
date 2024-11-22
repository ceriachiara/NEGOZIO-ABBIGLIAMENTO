from articolo import Articolo
from date import Date
class Articoli:
    MAX = 1000

    def __init__(self):
        self.elencoarticoli = [Articolo() for _ in range(Articoli.MAX)]
        self.n = 0

    def get_n(self):
        return self.n

    def add_elemento(self, a):
        if self.n < Articoli.MAX:
            self.elencoarticoli[self.n] = a
            self.n += 1
            return 0
        return -1

    def get_elementodaelencoarticoli(self, p):
        if 0 <= p < self.n:
            return self.elencoarticoli[p]
        return None

    def rimuoviarticolo(self, a, x):
        if self.n <= 0 or x >= self.n or x < 0:
            return -1
        i = x
        while i <= self.n - 1:
            self.elencoarticoli[i] = self.elencoarticoli[i+1]
            i += 1
        self.elencoarticoli[self.n - 1] = None
        self.n -= 1
        return None
