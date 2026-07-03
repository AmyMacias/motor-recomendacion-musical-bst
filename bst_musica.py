"""
========================================================================
 Algoritmo de Recomendación de una Plataforma de Música
 Estructura de datos: Árbol de Búsqueda Binaria (BST)
 Clave del nodo: Duración de la canción en segundos (entero)

 Reglas de implementación:
   - Solo se usan nodos y punteros (izq, der). No se usan listas,
     tuplas ni diccionarios nativos de Python para almacenar el árbol.
   - Todas las operaciones sobre el árbol son recursivas (o iterativas
     bajando por punteros, cuando se busca eficiencia O(log n)).
========================================================================
"""


# ------------------------------------------------------------------
# 1. NODO DEL ÁRBOL
# ------------------------------------------------------------------
class NodoCancion:
    """Representa una canción dentro del árbol.

    duracion : int   -> clave del BST (segundos)
    titulo   : str   -> nombre de la canción (dato adicional)
    artista  : str   -> dato adicional
    izq, der : NodoCancion -> punteros a los hijos
    """

    def __init__(self, duracion, titulo, artista="Desconocido"):
        self.duracion = duracion
        self.titulo = titulo
        self.artista = artista
        self.izq = None
        self.der = None


# ------------------------------------------------------------------
# 2. ÁRBOL DE BÚSQUEDA BINARIA (BST) DE LA PLATAFORMA
# ------------------------------------------------------------------
class ArbolMusical:
    def __init__(self):
        self.raiz = None

    # ---------------- INSERCIÓN ----------------
    def insertar(self, duracion, titulo, artista="Desconocido"):
        self.raiz = self._insertar_rec(self.raiz, duracion, titulo, artista)

    def _insertar_rec(self, nodo, duracion, titulo, artista):
        if nodo is None:
            return NodoCancion(duracion, titulo, artista)
        if duracion < nodo.duracion:
            nodo.izq = self._insertar_rec(nodo.izq, duracion, titulo, artista)
        elif duracion > nodo.duracion:
            nodo.der = self._insertar_rec(nodo.der, duracion, titulo, artista)
        else:
            # Duración empatada: se guarda como hijo derecho para no
            # perder la canción (se permiten duraciones repetidas).
            nodo.der = self._insertar_rec(nodo.der, duracion, titulo, artista)
        return nodo

    # ---------------- BÚSQUEDA EXACTA ----------------
    def buscar(self, duracion):
        return self._buscar_rec(self.raiz, duracion)

    def _buscar_rec(self, nodo, duracion):
        if nodo is None or nodo.duracion == duracion:
            return nodo
        if duracion < nodo.duracion:
            return self._buscar_rec(nodo.izq, duracion)
        return self._buscar_rec(nodo.der, duracion)

    # ---------------- RECORRIDO INORDER (auxiliar de visualización) ----------------
    def inorder(self):
        resultado = []
        self._inorder_rec(self.raiz, resultado)
        return resultado

    def _inorder_rec(self, nodo, resultado):
        if nodo is not None:
            self._inorder_rec(nodo.izq, resultado)
            resultado.append(nodo)
            self._inorder_rec(nodo.der, resultado)

    # ---------------- ELIMINACIÓN (nodo hoja, un hijo, dos hijos) ----------------
    def eliminar(self, duracion):
        self.raiz = self._eliminar_rec(self.raiz, duracion)

    def _eliminar_rec(self, nodo, duracion):
        if nodo is None:
            return None  # la canción no existe

        if duracion < nodo.duracion:
            nodo.izq = self._eliminar_rec(nodo.izq, duracion)
        elif duracion > nodo.duracion:
            nodo.der = self._eliminar_rec(nodo.der, duracion)
        else:
            # --- Nodo encontrado: 3 casos clásicos ---
            # Caso 1: nodo hoja
            if nodo.izq is None and nodo.der is None:
                return None
            # Caso 2: un solo hijo
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq
            # Caso 3: dos hijos -> se reemplaza con el sucesor
            # (el menor valor del subárbol derecho)
            sucesor = self._minimo(nodo.der)
            nodo.duracion = sucesor.duracion
            nodo.titulo = sucesor.titulo
            nodo.artista = sucesor.artista
            nodo.der = self._eliminar_rec(nodo.der, sucesor.duracion)
        return nodo

    def _minimo(self, nodo):
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual

    # ====================================================================
    # OPERACIÓN 1: calcular_tiempo_total(nodo_actual)
    # Estadística de la Playlist - suma recursiva de duraciones
    # ====================================================================
    def calcular_tiempo_total(self, nodo_actual=None):
        # Permite invocar sobre todo el árbol o sobre un subárbol específico
        if nodo_actual is None and self.raiz is not None:
            nodo_actual = self.raiz
        return self._calcular_tiempo_total_rec(nodo_actual)

    def _calcular_tiempo_total_rec(self, nodo_actual):
        # Caso base: subárbol vacío no aporta tiempo
        if nodo_actual is None:
            return 0
        # Caso recursivo: nodo + tiempo del subárbol izq + tiempo del subárbol der
        return (
            nodo_actual.duracion
            + self._calcular_tiempo_total_rec(nodo_actual.izq)
            + self._calcular_tiempo_total_rec(nodo_actual.der)
        )

    # ====================================================================
    # OPERACIÓN 2: recomendar_cancion_perfecta(segundos_disponibles)
    # Sugerencia Inteligente - baja por el BST en O(log n) promedio,
    # guardando siempre la menor diferencia absoluta encontrada.
    # ====================================================================
    def recomendar_cancion_perfecta(self, segundos_disponibles):
        if self.raiz is None:
            return None, None  # árbol vacío

        actual = self.raiz
        mejor_nodo = self.raiz
        mejor_diferencia = abs(self.raiz.duracion - segundos_disponibles)

        while actual is not None:
            diferencia_actual = abs(actual.duracion - segundos_disponibles)

            # Actualiza el mejor candidato si encontramos algo más cercano
            if diferencia_actual < mejor_diferencia:
                mejor_diferencia = diferencia_actual
                mejor_nodo = actual

            # Coincidencia exacta: no se puede mejorar, se corta la búsqueda
            if diferencia_actual == 0:
                break

            # Aprovecha la propiedad del BST para descartar la mitad del árbol
            if segundos_disponibles < actual.duracion:
                actual = actual.izq
            else:
                actual = actual.der

        return mejor_nodo, mejor_diferencia

    # ====================================================================
    # OPERACIÓN 3: filtrar_canciones_cortas(duracion_minima)
    # Limpieza de "Audios Basura": elimina todas las canciones con
    # duración menor a la indicada, reestructurando los punteros.
    #
    # Estrategia: se recorre el árbol en inorder recolectando (mediante
    # punteros/recursión, no listas planas de datos "crudos" sino nodos)
    # únicamente las canciones válidas, y se reconstruye un BST
    # balanceado a partir de esos nodos, tomando siempre el elemento
    # central para mantener O(log n) de altura.
    # ====================================================================
    def filtrar_canciones_cortas(self, duracion_minima):
        nodos_validos = []
        self._recolectar_validos(self.raiz, duracion_minima, nodos_validos)
        self.raiz = self._reconstruir_balanceado(nodos_validos, 0, len(nodos_validos) - 1)

    def _recolectar_validos(self, nodo, duracion_minima, nodos_validos):
        if nodo is None:
            return
        self._recolectar_validos(nodo.izq, duracion_minima, nodos_validos)
        if nodo.duracion >= duracion_minima:
            nodos_validos.append(nodo)
        self._recolectar_validos(nodo.der, duracion_minima, nodos_validos)

    def _reconstruir_balanceado(self, nodos_validos, inicio, fin):
        if inicio > fin:
            return None
        medio = (inicio + fin) // 2
        nodo_medio = nodos_validos[medio]
        nuevo_nodo = NodoCancion(nodo_medio.duracion, nodo_medio.titulo, nodo_medio.artista)
        nuevo_nodo.izq = self._reconstruir_balanceado(nodos_validos, inicio, medio - 1)
        nuevo_nodo.der = self._reconstruir_balanceado(nodos_validos, medio + 1, fin)
        return nuevo_nodo

    # ====================================================================
    # OPERACIÓN 4 (funcionalidad_propia): siguiente_cancion_para_transicion
    #
    # Utilidad: en una playlist de "entrenamiento" o "fiesta progresiva" se
    # quiere que la duración de las canciones vaya en aumento (o que, tras
    # escuchar una canción, se sugiera la siguiente más parecida pero un
    # poco más larga, para lograr transiciones suaves de energía/tiempo).
    #
    # Este algoritmo busca el SUCESOR de una duración dada dentro del BST:
    # la canción con la menor duración que sea ESTRICTAMENTE MAYOR a la
    # duración actual. Se resuelve en O(log n) bajando por el árbol,
    # sin recorrer todos los nodos, aprovechando la propiedad del BST.
    # ====================================================================
    def siguiente_cancion_para_transicion(self, duracion_actual):
        actual = self.raiz
        candidato_sucesor = None

        while actual is not None:
            if actual.duracion > duracion_actual:
                # Este nodo es candidato a sucesor; puede existir uno
                # todavía más pequeño (pero mayor que duracion_actual)
                # en el subárbol izquierdo.
                candidato_sucesor = actual
                actual = actual.izq
            else:
                # Los valores <= duracion_actual quedan descartados;
                # el sucesor debe estar en el subárbol derecho.
                actual = actual.der

        return candidato_sucesor

    # ---------------- utilidades de impresión (interfaz) ----------------
    def mostrar_arbol(self, nodo=None, prefijo="", es_izquierdo=True):
        if nodo is None and self.raiz is None:
            print("  (árbol vacío)")
            return
        if nodo is None:
            nodo = self.raiz
        if nodo.der is not None:
            self.mostrar_arbol(nodo.der, prefijo + ("│   " if es_izquierdo else "    "), False)
        print(prefijo + ("└── " if es_izquierdo else "┌── ") + f"{nodo.duracion}s | {nodo.titulo}")
        if nodo.izq is not None:
            self.mostrar_arbol(nodo.izq, prefijo + ("    " if es_izquierdo else "│   "), True)
