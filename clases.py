import io
import pandas as pd


class ArchivoCSV:
    def __init__(self, ruta):
        self.ruta = ruta
        self.df = pd.read_csv(ruta)
        self.df = self.df.set_index("time_ms")

    def __str__(self):
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        texto = "Archivo: " + self.ruta + "\n\n"
        texto += buffer.getvalue() + "\n"
        texto += self.df.describe().to_string()
        return texto