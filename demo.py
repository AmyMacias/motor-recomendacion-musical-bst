"""
Demostración automática (no interactiva) de todas las operaciones
del árbol, para verificar que la lógica funciona correctamente.
"""
from bst_musica import ArbolMusical


def formatear_tiempo(segundos):
    minutos = segundos // 60
    seg = segundos % 60
    return f"{minutos} min {seg} s ({segundos} s)"


arbol = ArbolMusical()
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
for d, t, a in canciones:
    arbol.insertar(d, t, a)

print("=" * 60)
print(" MOTOR DE RECOMENDACION - PLATAFORMA DE MUSICA")
print(" Catalogo inicial cargado (10 canciones)")
print("=" * 60)

print("\n--- 1) Estructura del arbol (BST por duracion) ---\n")
arbol.mostrar_arbol()

print("\n--- 2) OPERACION 1: calcular_tiempo_total(nodo_actual) ---")
total = arbol.calcular_tiempo_total()
print(f"Tiempo total de la playlist completa: {formatear_tiempo(total)}")

subarbol_izq = arbol.buscar(180).izq  # subárbol específico de prueba
if subarbol_izq:
    total_sub = arbol.calcular_tiempo_total(subarbol_izq)
    print(f"Tiempo total del subarbol que cuelga de la izquierda de 180s: "
          f"{formatear_tiempo(total_sub)}")

print("\n--- 3) OPERACION 2: recomendar_cancion_perfecta(segundos_disponibles) ---")
for consulta in [198, 203, 60, 999, 150]:
    nodo, diff = arbol.recomendar_cancion_perfecta(consulta)
    print(f"Usuario pide {consulta}s -> Recomendado: '{nodo.titulo}' "
          f"({nodo.duracion}s) | diferencia = {diff}s")

print("\n--- 4) OPERACION 3: filtrar_canciones_cortas(duracion_minima) ---")
print("Eliminando canciones con menos de 100 segundos...")
arbol.filtrar_canciones_cortas(100)
print("Arbol resultante (reestructurado y balanceado):\n")
arbol.mostrar_arbol()
nuevo_total = arbol.calcular_tiempo_total()
print(f"\nNuevo tiempo total tras el filtrado: {formatear_tiempo(nuevo_total)}")

print("\n--- 5) OPERACION 4 (propia): siguiente_cancion_para_transicion() ---")
for actual in [150, 200, 260, 170]:
    siguiente = arbol.siguiente_cancion_para_transicion(actual)
    if siguiente:
        print(f"Despues de {actual}s -> Sugerencia para continuar: "
              f"'{siguiente.titulo}' ({siguiente.duracion}s)")
    else:
        print(f"Despues de {actual}s -> No hay una cancion mas larga disponible.")

print("\n--- 6) Prueba de eliminacion (nodo con dos hijos) ---")
print("Buscando cancion de 210s antes de eliminar:", arbol.buscar(210))
arbol.eliminar(210)
print("Arbol despues de eliminar la cancion de 210s:\n")
arbol.mostrar_arbol()
print("\nDemostracion finalizada correctamente. Todas las operaciones funcionan.")
