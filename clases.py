import io
import numpy as np
import pandas as pd
import scipy.io as sio
import matplotlib.pyplot as plt


class ArchivoCSV:
    def __init__(self, ruta):
        self.ruta = ruta
        self.df = pd.read_csv(ruta)

        if "time_ms" in self.df.columns:
            self.df = self.df.set_index("time_ms")
        elif "Tiempo" in self.df.columns:
            self.df = self.df.set_index("Tiempo")

    def __str__(self):
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        texto = f"=== ARCHIVO CSV: {self.ruta} ===\n\n"
        texto += buffer.getvalue()
        texto += "\n--- ESTADÍSTICAS DESCRIPTIVAS ---\n"
        texto += self.df.describe().to_string()
        return texto

    def canales(self):
        return [
            c for c in self.df.columns
            if c not in ("subject", "condition", "Condición")
        ]

    def graficar(self, condicion, canal, canal_x, canal_y):
        col_cond = "condition" if "condition" in self.df.columns else "Condición"
        datos = self.df[self.df[col_cond] == condicion]

        fig = plt.figure(figsize=(12, 8))
        cuadricula = fig.add_gridspec(2, 2, width_ratios=[2, 1])
        ax1 = fig.add_subplot(cuadricula[0, :])
        ax2 = fig.add_subplot(cuadricula[1, 0])
        ax3 = fig.add_subplot(cuadricula[1, 1])

        ax1.stem(datos.index, datos[canal], markerfmt=",")
        ax1.axvline(0, color="red", linestyle="--", label="t = 0 ms")
        ax1.set_title(f"Stem de {canal} - Condición {condicion}")
        ax1.set_xlabel("Tiempo (ms)")
        ax1.set_ylabel("Amplitud (µV)")
        ax1.legend()
        ax1.grid(True)

        ax2.hist(datos[canal], bins=30, color="skyblue", edgecolor="black")
        ax2.set_title(f"Histograma de {canal}")
        ax2.set_xlabel("Amplitud (µV)")
        ax2.set_ylabel("Frecuencia")
        ax2.grid(True)

        ax3.scatter(datos[canal_x], datos[canal_y], s=10, alpha=0.6)
        ax3.set_title(f"{canal_x} vs {canal_y}")
        ax3.set_xlabel(f"{canal_x} (µV)")
        ax3.set_ylabel(f"{canal_y} (µV)")
        ax3.grid(True)

        fig.tight_layout()
        nombre = f"grafico_condicion_{condicion}.png"
        fig.savefig(nombre, dpi=150)
        plt.show()

    def diferencia_interhemisferica(self, canal_izq, canal_der):
        nombre = f"{canal_izq}-{canal_der}"
        self.df[nombre] = self.df[canal_izq] - self.df[canal_der]
        print(f"\nNueva columna creada: {nombre}")
        print(self.df[[canal_izq, canal_der, nombre]].head())


class ArchivoMAT:
    def __init__(self, ruta):
        self.ruta = ruta
        self.contenido = sio.loadmat(ruta)
        self.fs = 250
        self.clave_matriz = [
            k for k in self.contenido.keys()
            if not k.startswith("__")
        ][0]

    def __str__(self):
        variables = sio.whosmat(self.ruta)
        salida = f"=== ARCHIVO MAT: {self.ruta} ===\n"
        salida += f"{'Nombre':<20} | {'Dimensiones':<20} | {'Tipo':<12}\n"
        salida += "-" * 58 + "\n"

        for nombre, shape, dtype in variables:
            salida += f"{nombre:<20} | {str(shape):<20} | {dtype:<12}\n"

        return salida

    def operar_y_graficar_2d(
        self, nombre_op, funcion_op,
        ch1, ch2, ch3, ch4, t_min, t_max
    ):
        matriz = self.contenido[self.clave_matriz]

        matriz_2d = np.mean(matriz, axis=2)

        canales = [ch1, ch2, ch3, ch4]
        idx_min = int(t_min * self.fs)
        idx_max = int(t_max * self.fs)

        segmento = matriz_2d[canales, idx_min:idx_max]
        tiempo = np.arange(idx_min, idx_max) / self.fs

        resultado = funcion_op(segmento[0], segmento[1])
        resultado = funcion_op(resultado, segmento[2])
        resultado = funcion_op(resultado, segmento[3])

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

        for i, canal in enumerate(canales):
            ax1.plot(tiempo, segmento[i], label=f"Canal {canal + 1}")

        ax1.set_title(f"4 canales - {nombre_op}")
        ax1.set_xlabel("Tiempo (s)")
        ax1.set_ylabel("Amplitud (µV)")
        ax1.legend()
        ax1.grid(True)

        ax2.plot(tiempo, resultado, label=nombre_op)
        ax2.set_title(f"Resultado: {nombre_op}")
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel("Amplitud (µV)")
        ax2.legend()
        ax2.grid(True)

        fig.tight_layout()
        nombre = f"grafico_mat_{nombre_op}.png"
        fig.savefig(nombre, dpi=150)
        plt.show()

    def analizar_estadisticas_3d(self, eje1, eje2):
        matriz = self.contenido[self.clave_matriz]

        promedio = np.mean(matriz, axis=(eje1, eje2))
        desviacion = np.std(matriz, axis=(eje1, eje2))

        print(f"\nForma del promedio: {promedio.shape}")
        print(f"Forma de la desviación estándar: {desviacion.shape}")

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.boxplot(
            [promedio.flatten(), desviacion.flatten()],
            tick_labels=["Promedio", "Desviación Estándar"]
        )
        ax.set_title("Promedio y Desviación Estándar")
        ax.set_ylabel("Amplitud (µV)")
        ax.grid(True)
        plt.show()


class GestorSistema:
    def __init__(self):
        self.registros = {}

    def registrar(self, clave, objeto):
        self.registros[clave] = objeto

    def buscar(self, clave):
        return self.registros.get(clave)

    def listar_claves(self):
        return list(self.registros.keys())


def pedir_entero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print("Debes escribir un número entero.")


def pedir_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Debes escribir un número.")
