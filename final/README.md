# Sistema de Soporte Técnico (Proyecto Final)

## Descripción Breve
Este proyecto implementa un sistema de gestión de turnos de soporte técnico basado en una estructura de datos tipo **Cola (FIFO)**. Fue desarrollado inicialmente en el primer parcial y ha sido ampliado para el examen final incorporando almacenamiento de datos y una interfaz gráfica.

## Objetivo del Proyecto
El objetivo es gestionar eficientemente las solicitudes de soporte técnico de los clientes, asegurando que sean atendidos en orden de llegada (First In, First Out). Además, busca demostrar la aplicación práctica de persistencia de datos y desarrollo de interfaces gráficas.

## Principales Funcionalidades
- **Registro de solicitudes**: Permite ingresar el nombre del cliente y la descripción del problema.
- **Atención de solicitudes**: Atiende (retira de la cola) a los clientes en estricto orden de llegada.
- **Reiniciar IDs**: Vacía las solicitudes pendientes y permite empezar nuevamente desde el ID 1. Si hay pendientes, solicita confirmación antes de borrarlos. El archivo JSON también queda vacío.
- **Estructura Cola manual**: Todo el manejo se realiza mediante una cola desarrollada desde cero con nodos enlazados (sin usar listas integradas de Python).
- **Persistencia de Datos**: Implementa almacenamiento en archivo `JSON` (`datos_solicitudes.json`). Al cerrar y volver a abrir la aplicación, las solicitudes pendientes se recuperan automáticamente.
- **Interfaz Gráfica (GUI)**: Incluye una interfaz gráfica desarrollada con la librería `tkinter` de Python, la cual facilita la interacción del usuario con el sistema.

## Lenguaje Utilizado
- **Python** (versión 3.x)

## Instrucciones Básicas para Ejecutar el Proyecto
1. Asegúrese de tener Python instalado en su sistema.
2. Descargue o clone el repositorio.
3. Navegue hasta la carpeta raíz del proyecto (`semana7-cola-repository-python`).
4. Ejecute el archivo principal usando el siguiente comando en la terminal:
   ```bash
   python main.py
   ```
5. La interfaz gráfica se abrirá. Puede comenzar a registrar clientes y atenderlos. El estado se guardará automáticamente en el archivo `datos_solicitudes.json`.

La aplicación utiliza la biblioteca estándar de Python; `pytest` solo es necesario para las pruebas. Tkinter debe estar disponible en la instalación de Python. Ejecute siempre desde la carpeta raíz: la ruta del JSON es relativa a la carpeta desde la que inicia el programa.

## Organización del código

| Archivo o carpeta | Responsabilidad |
| --- | --- |
| `main.py` | Crea el repositorio JSON, lo entrega al servicio y abre la GUI. |
| `src/models/solicitud.py` | Representa una solicitud con ID, cliente y descripción. |
| `src/structures/nodo.py` y `cola.py` | Implementan los nodos enlazados y las operaciones FIFO. |
| `src/repositories/solicitud_repository.py` | Define el contrato abstracto del almacenamiento. |
| `src/repositories/memory_solicitud_repository.py` | Implementa almacenamiento temporal en memoria. |
| `src/repositories/json_solicitud_repository.py` | Recupera el JSON al iniciar y guarda los pendientes al registrar o atender. |
| `src/services/soporte_service.py` | Valida entradas, asigna identificadores y coordina el repositorio. |
| `src/ui/gui.py` | Construye la ventana, procesa botones y actualiza el estado visible. |
| `src/ui/consola.py` | Conserva la interfaz de consola del desarrollo anterior. |
| `tests/` | Contiene pruebas de la cola, el repositorio en memoria y el servicio. |

El flujo es **GUI → servicio → repositorio → cola**. El repositorio JSON también convierte las solicitudes a diccionarios para guardarlas en disco. La cola usa nodos como almacenamiento interno; la lista utilizada para serializar el JSON no reemplaza esa estructura.

## Comprobar la persistencia

1. Registre dos solicitudes, por ejemplo Ana y Luis, en ese orden.
2. Atienda una: debe salir Ana y quedar Luis como siguiente.
3. Cierre la ventana y ejecute de nuevo `python main.py` desde la misma carpeta.
4. Compruebe que Luis continúa pendiente y revise `datos_solicitudes.json`.

Se guardan **solicitudes pendientes**, no un historial de solicitudes atendidas. Los IDs continúan desde el mayor ID pendiente recuperado; si la cola está vacía al reiniciar, la numeración vuelve a empezar. Actualmente los errores de lectura o escritura del JSON se imprimen en la terminal, por lo que conviene revisarla durante la demostración.

## Pruebas automatizadas

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```
