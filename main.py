from clases import ArchivoCSV, pedir_entero


def elegir_canal(archivo, mensaje):
    canales = [c for c in archivo.df.columns if c not in ("subject", "condition")]
    for i, c in enumerate(canales, start=1):
        print(str(i) + ". " + c)
    n = pedir_entero(mensaje, 1, len(canales))
    return canales[n - 1]


def menu_csv():
    archivo = None
    while True:
        print("\n=== MENU CSV ===")
        print("1. Cargar archivo CSV")
        print("2. Ver informacion del archivo")
        print("3. Graficar por condicion (stem, histograma y scatter)")
        print("4. Diferencia interhemisferica entre dos canales")
        print("0. Salir")
        opcion = pedir_entero("Elige una opcion: ", 0, 4)

        if opcion == 0:
            break

        if opcion == 1:
            ruta = input("Ruta del archivo (ej: Arch_CSV/ERP_01.csv): ")
            try:
                archivo = ArchivoCSV(ruta)
                print("Archivo cargado.")
            except FileNotFoundError:
                print("No se encontro el archivo.")
            except Exception as error:
                print("No se pudo cargar el archivo: " + str(error))
            continue

        if archivo is None:
            print("Primero carga un archivo (opcion 1).")
            continue

        if opcion == 2:
            print(archivo)

        elif opcion == 3:
            condicion = pedir_entero("Condicion (1, 2 o 3): ", 1, 3)
            print("Canal para el stem y el histograma:")
            canal = elegir_canal(archivo, "Numero del canal: ")
            print("Canal para el eje X del scatter:")
            canal_x = elegir_canal(archivo, "Numero del canal: ")
            print("Canal para el eje Y del scatter:")
            canal_y = elegir_canal(archivo, "Numero del canal: ")
            archivo.graficar(condicion, canal, canal_x, canal_y)

        elif opcion == 4:
            print("Canal izquierdo:")
            canal_izq = elegir_canal(archivo, "Numero del canal: ")
            print("Canal derecho:")
            canal_der = elegir_canal(archivo, "Numero del canal: ")
            archivo.diferencia_interhemisferica(canal_izq, canal_der)


if __name__ == "__main__":
    menu_csv()
