import io
import pandas as pd
import matplotlib.pyplot as plt


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

    def graficar(self, condicion, canal, canal_x, canal_y):
        datos = self.df[self.df["condition"] == condicion]

        fig = plt.figure(figsize=(12, 8))
        cuadricula = fig.add_gridspec(2, 2, width_ratios=[2, 1])
        ax1 = fig.add_subplot(cuadricula[0, :])
        ax2 = fig.add_subplot(cuadricula[1, 0])
        ax3 = fig.add_subplot(cuadricula[1, 1])

        ax1.stem(datos.index, datos[canal], markerfmt=",")
        ax1.axvline(0, color="red", linestyle="--", label="t = 0 ms")
        ax1.set_title("Stem de " + canal + " (condición " + str(condicion) + ")")
        ax1.set_xlabel("Tiempo (ms)")
        ax1.set_ylabel("Amplitud (µV)")
        ax1.legend()

        ax2.hist(datos[canal], bins=30)
        ax2.set_title("Histograma de " + canal)
        ax2.set_xlabel("Amplitud (µV)")
        ax2.set_ylabel("Frecuencia (muestras)")

        ax3.scatter(datos[canal_x], datos[canal_y], s=5)
        ax3.set_title(canal_x + " vs " + canal_y)
        ax3.set_xlabel(canal_x + " (µV)")
        ax3.set_ylabel(canal_y + " (µV)")

        fig.tight_layout()
        nombre = "grafico_condicion" + str(condicion) + ".png"
        fig.savefig(nombre, dpi=150)
        plt.show()

    def diferencia_interhemisferica(self, canal_izq, canal_der):
        canales = [c for c in self.df.columns if c not in ("subject", "condition")]
        for canal in (canal_izq, canal_der):
            if canal not in canales:
                raise ValueError("El canal " + canal + " no existe. Canales: " + str(canales))

        nombre = canal_izq + "-" + canal_der
        self.df[nombre] = self.df[canal_izq] - self.df[canal_der]

        print("Nueva columna creada: " + nombre + " (µV)")
        print(self.df[nombre].head())
        print(self.df[nombre].describe())
        return self.df[nombre]

def pedir_entero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje)
        try:
            valor = int(texto)
        except ValueError:
            print("Debes escribir un numero entero.")
            continue
        if valor < minimo or valor > maximo:
            print("El numero debe estar entre " + str(minimo) + " y " + str(maximo) + ".")
            continue
        return valor
