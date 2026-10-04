import operator
from clases import ArchivoCSV, ArchivoMAT, GestorSistema, pedir_entero, pedir_float


def elegir_canal_csv(archivo, mensaje):
    canales = archivo.canales()

    for i, canal in enumerate(canales, 1):
        print(f"{i}. {canal}")

    n = pedir_entero(mensaje, 1, len(canales))
    return canales[n - 1]


def menu_csv(gestor):
    archivo = None

    while True:
        print("\n=== MENÚ CSV ===")
        print("1. Cargar archivo CSV")
        print("2. Ver información")
        print("3. Graficar por condición")
        print("4. Diferencia interhemisférica")
        print("0. Volver")

        opcion = pedir_entero("Elige una opción: ", 0, 4)

        if opcion == 0:
            break

        if opcion == 1:
            ruta = input("Ruta del archivo: ")

            try:
                archivo = ArchivoCSV(ruta)
                clave = input("Nombre para guardar el objeto: ")
                gestor.registrar(clave, archivo)
                print("Archivo cargado correctamente.")
            except Exception as error:
                print(f"Error: {error}")

        elif archivo is None:
            print("Primero carga un archivo CSV.")

        elif opcion == 2:
            print(archivo)

        elif opcion == 3:
            condicion = pedir_entero("Condición (1, 2 o 3): ", 1, 3)

            print("\nCanal para stem e histograma:")
            canal = elegir_canal_csv(archivo, "Número: ")

            print("\nCanal X del scatter:")
            canal_x = elegir_canal_csv(archivo, "Número: ")

            print("\nCanal Y del scatter:")
            canal_y = elegir_canal_csv(archivo, "Número: ")

            archivo.graficar(
                condicion, canal, canal_x, canal_y
            )

        elif opcion == 4:
            print("\nCanal izquierdo:")
            canal_izq = elegir_canal_csv(archivo, "Número: ")

            print("\nCanal derecho:")
            canal_der = elegir_canal_csv(archivo, "Número: ")

            if canal_izq == canal_der:
                print("Debes escoger dos canales diferentes.")
            else:
                archivo.diferencia_interhemisferica(
                    canal_izq, canal_der
                )


def menu_mat(gestor):
    archivo = None

    while True:
        print("\n=== MENÚ MAT ===")
        print("1. Cargar archivo MAT")
        print("2. Ver información (whosmat)")
        print("3. Operación y gráfica 2D")
        print("4. Análisis estadístico 3D")
        print("0. Volver")

        opcion = pedir_entero("Elige una opción: ", 0, 4)

        if opcion == 0:
            break

        if opcion == 1:
            ruta = input("Ruta del archivo: ")

            try:
                archivo = ArchivoMAT(ruta)
                clave = input("Nombre para guardar el objeto: ")
                gestor.registrar(clave, archivo)
                print("Archivo cargado correctamente.")
            except Exception as error:
                print(f"Error: {error}")

        elif archivo is None:
            print("Primero carga un archivo MAT.")

        elif opcion == 2:
            print(archivo)

        elif opcion == 3:
            print("\n1. Suma (+)")
            print("2. Resta (-)")
            print("3. Multiplicación (*)")

            op = pedir_entero("Operación: ", 1, 3)

            operaciones = {
                1: ("Suma", operator.add),
                2: ("Resta", operator.sub),
                3: ("Multiplicacion", operator.mul)
            }

            nombre_op, funcion_op = operaciones[op]

            print("\nCanales disponibles: 1 a 64")

            ch1 = pedir_entero("Canal 1: ", 1, 64) - 1
            ch2 = pedir_entero("Canal 2: ", 1, 64) - 1
            ch3 = pedir_entero("Canal 3: ", 1, 64) - 1
            ch4 = pedir_entero("Canal 4: ", 1, 64) - 1

            t_min = pedir_float("Tiempo mínimo (s): ")
            t_max = pedir_float("Tiempo máximo (s): ")

            if t_min < 0 or t_max > 2.5 or t_min >= t_max:
                print("El rango debe estar entre 0 y 2.5 s.")
            else:
                archivo.operar_y_graficar_2d(
                    nombre_op, funcion_op,
                    ch1, ch2, ch3, ch4,
                    t_min, t_max
                )

        elif opcion == 4:
            eje1 = pedir_entero("Primer eje (0, 1 o 2): ", 0, 2)

            while True:
                eje2 = pedir_entero("Segundo eje (0, 1 o 2): ", 0, 2)
                if eje2 != eje1:
                    break
                print("Los ejes deben ser diferentes.")

            archivo.analizar_estadisticas_3d(eje1, eje2)


def main():
    gestor = GestorSistema()

    while True:
        print("\n")
        print(" SISTEMA DE MONITOREO NEUROLÓGICO ")
        print("1. Módulo Archivos CSV")
        print("2. Módulo Archivos MAT")
        print("3. Consultar objetos guardados")
        print("0. Salir")

        opcion = pedir_entero("Selecciona una opción: ", 0, 3)

        if opcion == 0:
            break
        elif opcion == 1:
            menu_csv(gestor)
        elif opcion == 2:
            menu_mat(gestor)
        elif opcion == 3:
            registros = gestor.listar_claves()

            if not registros:
                print("No hay objetos guardados.")
                continue

            print("\nObjetos guardados:")
            for clave in registros:
                print("-", clave)

            clave = input("Clave del objeto a buscar: ")
            objeto = gestor.buscar(clave)

            if objeto:
                print(objeto)
            else:
                print("No existe ese objeto.")


if __name__ == "__main__":
    main()
