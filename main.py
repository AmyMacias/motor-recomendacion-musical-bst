"""
Interfaz de usuario del Motor de Recomendación Musical.
Menú interactivo por consola que permite probar todas las operaciones
del Árbol de Búsqueda Binaria (BST) implementado en bst_musica.py
"""

from bst_musica import ArbolMusical


def cargar_datos_iniciales(arbol):
    """Carga un catálogo inicial de canciones para poder probar el sistema."""
    canciones = [
        (210, "Bohemian Rhapsody", "Queen"),
        (180, "Blinding Lights", "The Weeknd"),
        (245, "Hotel California", "Eagles"),
        (150, "Levitating", "Dua Lipa"),
        (200, "Shape of You", "Ed Sheeran"),
        (95, "Intro Instrumental", "Varios"),
        (230, "Stairway to Heaven (parte 1)", "Led Zeppelin"),
        (170, "As It Was", "Harry Styles"),
        (260, "Bohemian Reprise", "Queen"),
        (60, "Jingle Corto", "Varios"),
    ]
    for duracion, titulo, artista in canciones:
        arbol.insertar(duracion, titulo, artista)


def formatear_tiempo(segundos):
    minutos = segundos // 60
    seg = segundos % 60
    return f"{minutos} min {seg} s ({segundos} s)"


def menu():
    arbol = ArbolMusical()
    cargar_datos_iniciales(arbol)

    opciones = """
==================================================
   MOTOR DE RECOMENDACION - PLATAFORMA DE MUSICA
   (Arbol de Busqueda Binaria por duracion)
==================================================
1. Mostrar arbol de canciones
2. Insertar nueva cancion
3. Calcular tiempo total de la playlist (Operacion 1)
4. Recomendar cancion perfecta por duracion (Operacion 2)
5. Filtrar canciones cortas / Audios Basura (Operacion 3)
6. Sugerir siguiente cancion para transicion suave (Operacion 4 - propia)
7. Buscar cancion exacta por duracion
8. Eliminar cancion por duracion
0. Salir
--------------------------------------------------
"""
    while True:
        print(opciones)
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            print("\nEstructura actual del arbol (derecha=arriba, izquierda=abajo):\n")
            arbol.mostrar_arbol()

        elif opcion == "2":
            try:
                duracion = int(input("Duracion en segundos: "))
                titulo = input("Titulo de la cancion: ")
                artista = input("Artista: ")
                arbol.insertar(duracion, titulo, artista)
                print(f"-> '{titulo}' ({duracion}s) insertada correctamente.")
            except ValueError:
                print("Duracion invalida.")

        elif opcion == "3":
            total = arbol.calcular_tiempo_total()
            print(f"\nTiempo total de la playlist completa: {formatear_tiempo(total)}")

        elif opcion == "4":
            try:
                segundos = int(input("Segundos disponibles: "))
                nodo, diferencia = arbol.recomendar_cancion_perfecta(segundos)
                if nodo is None:
                    print("El arbol esta vacio, no hay canciones para recomendar.")
                else:
                    print(f"\nRecomendacion: '{nodo.titulo}' - {nodo.artista} "
                          f"({nodo.duracion}s) | diferencia = {diferencia}s")
            except ValueError:
                print("Valor invalido.")

        elif opcion == "5":
            try:
                minima = int(input("Duracion minima aceptada (segundos): "))
                arbol.filtrar_canciones_cortas(minima)
                print(f"-> Canciones con menos de {minima}s eliminadas y arbol reestructurado.")
            except ValueError:
                print("Valor invalido.")

        elif opcion == "6":
            try:
                actual = int(input("Duracion de la cancion que se acaba de reproducir (s): "))
                siguiente = arbol.siguiente_cancion_para_transicion(actual)
                if siguiente is None:
                    print("No hay una cancion mas larga disponible para continuar la transicion.")
                else:
                    print(f"\nSiguiente sugerida (transicion suave): "
                          f"'{siguiente.titulo}' - {siguiente.artista} ({siguiente.duracion}s)")
            except ValueError:
                print("Valor invalido.")

        elif opcion == "7":
            try:
                duracion = int(input("Duracion exacta a buscar (s): "))
                nodo = arbol.buscar(duracion)
                if nodo:
                    print(f"Encontrada: '{nodo.titulo}' - {nodo.artista} ({nodo.duracion}s)")
                else:
                    print("No se encontro ninguna cancion con esa duracion exacta.")
            except ValueError:
                print("Valor invalido.")

        elif opcion == "8":
            try:
                duracion = int(input("Duracion de la cancion a eliminar (s): "))
                arbol.eliminar(duracion)
                print(f"-> Cancion con duracion {duracion}s eliminada (si existia).")
            except ValueError:
                print("Valor invalido.")

        elif opcion == "0":
            print("Gracias por usar el motor de recomendacion. Hasta pronto!")
            break

        else:
            print("Opcion no valida, intente de nuevo.")


if __name__ == "__main__":
    menu()
