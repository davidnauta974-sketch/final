"""
Nodo para la cola enlazada.

Cada nodo almacena un dato y una referencia al siguiente nodo,
formando una cadena que permite recorrer la cola de principio a fin.
"""


class Nodo:
    """Nodo individual de una estructura enlazada."""

    def __init__(self, dato):
        """
        Crea un nodo con el dato proporcionado.

        Args:
            dato: Elemento almacenado en el nodo.
        """
        self.dato = dato
        self.siguiente = None  # Referencia al próximo nodo (None si es el último)
