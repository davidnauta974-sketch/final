"""
Cola FIFO implementada manualmente con nodos enlazados.

La cola mantiene referencias al primer nodo (frente) y al último nodo (final),
junto con un contador de elementos, para garantizar que todas las operaciones
se ejecuten en tiempo O(1).

No utiliza list, collections.deque ni queue.Queue como almacenamiento interno.
"""

from src.structures.nodo import Nodo


class Cola:
    """
    Cola FIFO (First In, First Out) basada en nodos enlazados.

    Los elementos se agregan por el final y se retiran por el frente,
    respetando el orden de llegada.
    """

    def __init__(self):
        """Crea una cola vacía."""
        self._frente = None   # Referencia al primer nodo
        self._final = None    # Referencia al último nodo
        self._tamano = 0      # Contador de elementos

    def enqueue(self, elemento) -> None:
        """
        Agrega un elemento al final de la cola.

        Complejidad: O(1) gracias a la referencia directa al último nodo.

        Args:
            elemento: Dato a agregar a la cola.
        """
        nuevo_nodo = Nodo(elemento)

        if self.is_empty():
            # Si la cola está vacía, el nuevo nodo es tanto el frente como el final
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            # Enlazar el nodo actual del final con el nuevo nodo
            self._final.siguiente = nuevo_nodo
            # Actualizar la referencia al final
            self._final = nuevo_nodo

        self._tamano += 1

    def dequeue(self):
        """
        Retira y devuelve el elemento del frente de la cola.

        Complejidad: O(1).

        Returns:
            El elemento que estaba al frente de la cola.

        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("No se puede retirar: la cola está vacía.")

        dato = self._frente.dato
        self._frente = self._frente.siguiente
        self._tamano -= 1

        # Si la cola quedó vacía, actualizar también la referencia al final
        if self._frente is None:
            self._final = None

        return dato

    def peek(self):
        """
        Consulta el elemento del frente sin retirarlo de la cola.

        Complejidad: O(1).

        Returns:
            El elemento que está al frente de la cola.

        Raises:
            IndexError: Si la cola está vacía.
        """
        if self.is_empty():
            raise IndexError("No se puede consultar: la cola está vacía.")

        return self._frente.dato

    def is_empty(self) -> bool:
        """
        Indica si la cola no contiene elementos.

        Complejidad: O(1).

        Returns:
            True si la cola está vacía, False en caso contrario.
        """
        return self._tamano == 0

    def size(self) -> int:
        """
        Devuelve la cantidad de elementos en la cola.

        Complejidad: O(1) gracias al contador interno.

        Returns:
            Número de elementos actualmente en la cola.
        """
        return self._tamano
