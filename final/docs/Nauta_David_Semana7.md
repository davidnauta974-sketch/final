# DOCUMENTO ACADÉMICO — Semana 7

---

## PORTADA

**Universidad de Especialidades Espíritu Santo (UEES)**

**Actividad:** Semana 7 — Patrones de Diseño, Testing Unitario y Tipos de Datos Abstractos Lineales

**Proyecto:** Sistema de Gestión de Turnos — Soporte Técnico

**Estudiante:** David Patricio Ñauta Picon

**Asignatura:** *(Pendiente de completar)*

**Docente:** *(Pendiente de completar)*

**Fecha de elaboración:** 22 de septiembre de 2026

**Fecha límite de entrega:** 27 de septiembre de 2026

**Repositorio:** https://github.com/<USUARIO>/semana7-cola-repository-python
*(Reemplazar `<USUARIO>` con el usuario real de GitHub tras la publicación)*

---

## 1. Objetivo del proyecto

Desarrollar un sistema de gestión de turnos para soporte técnico que demuestre el uso de:

- **Tipos de datos abstractos lineales**: implementar una cola FIFO manualmente con nodos enlazados.
- **Patrones de diseño**: aplicar el patrón Repository para separar la lógica de negocio del almacenamiento.
- **Testing unitario**: verificar el comportamiento correcto de cada componente mediante pytest.

---

## 2. Descripción del problema

Un centro de soporte técnico recibe solicitudes de clientes que deben atenderse **en el mismo orden en que llegan**. El sistema debe permitir:

1. **Registrar** una solicitud con nombre del cliente y descripción del problema.
2. **Atender** la solicitud más antigua (retirarla de la cola).
3. **Consultar** la siguiente solicitud sin retirarla.
4. **Verificar** si existen solicitudes pendientes.
5. **Conocer** cuántas solicitudes hay en espera.

Cada solicitud tiene un identificador único generado automáticamente.

---

## 3. Justificación de la cola FIFO

**FIFO** significa *First In, First Out* (primero en entrar, primero en salir). Este comportamiento modela exactamente una fila de espera:

- El primer cliente en solicitar ayuda es el primero en ser atendido.
- No hay saltos ni prioridades: el orden de llegada determina el orden de atención.
- Es la estructura de datos más natural y justa para este tipo de sistema.

**¿Por qué no usar una lista de Python?** Porque retirar el primer elemento de una lista (`list.pop(0)`) tiene complejidad O(n), ya que Python debe desplazar todos los elementos restantes. Con nodos enlazados, tanto agregar como retirar se ejecutan en O(1).

---

## 4. Nodos enlazados y operaciones de la cola

### 4.1 Estructura de un nodo

Cada nodo es un objeto simple con dos atributos:

```python
class Nodo:
    def __init__(self, dato):
        self.dato = dato          # El elemento almacenado
        self.siguiente = None     # Referencia al próximo nodo
```

Los nodos se enlazan formando una cadena: cada nodo "apunta" al siguiente, creando una secuencia ordenada sin necesidad de un arreglo contiguo en memoria.

### 4.2 Estructura de la cola

La cola mantiene tres atributos:

- **`_frente`**: referencia al primer nodo (de donde se retiran elementos).
- **`_final`**: referencia al último nodo (donde se agregan elementos).
- **`_tamano`**: contador de elementos.

### 4.3 Las cinco operaciones (todas O(1))

**`enqueue(elemento)`** — Agregar al final:
1. Se crea un nuevo nodo con el elemento.
2. Si la cola está vacía, el nuevo nodo se convierte en frente y final.
3. Si no, el último nodo actual apunta al nuevo nodo, y se actualiza `_final`.
4. Se incrementa el contador.

**`dequeue()`** — Retirar del frente:
1. Se guarda el dato del nodo del frente.
2. `_frente` avanza al siguiente nodo.
3. Se decrementa el contador.
4. **Si la cola queda vacía**, `_final` también se actualiza a `None`.
5. Se devuelve el dato guardado.

**`peek()`** — Consultar sin retirar:
- Devuelve el dato del nodo del frente sin modificar nada.

**`is_empty()`** — Verificar si está vacía:
- Devuelve `True` si el contador es cero.

**`size()`** — Cantidad de elementos:
- Devuelve el valor del contador.

### 4.4 ¿Qué sucede al retirar el último elemento?

Cuando `dequeue()` retira el único elemento restante:
- `_frente` se mueve al siguiente nodo, que es `None`.
- Al detectar que `_frente` es `None`, la cola también establece `_final = None`.
- Esto deja la cola en un estado limpio, lista para recibir nuevos elementos.

---

## 5. Patrón Repository

### 5.1 ¿Qué es el patrón Repository?

El **patrón Repository** es un patrón de diseño que **separa la lógica de negocio del mecanismo de almacenamiento**. El servicio no necesita saber cómo se guardan los datos; solo interactúa con una interfaz abstracta.

### 5.2 Arquitectura del proyecto

```
┌──────────┐     ┌──────────────┐     ┌──────────────────────┐     ┌─────────────┐
│ Consola  │ ──→ │  Servicio    │ ──→ │  Repository          │ ──→ │  Cola FIFO  │
│  (UI)    │     │ (Lógica)     │     │  (Contrato/Memoria)  │     │  (Nodos)    │
└──────────┘     └──────────────┘     └──────────────────────┘     └─────────────┘
```

### 5.3 Componentes

| Archivo | Responsabilidad |
|---------|----------------|
| `solicitud.py` | Define el modelo de datos (id, nombre, descripción). |
| `nodo.py` + `cola.py` | Estructura de datos FIFO manual con nodos enlazados. |
| `solicitud_repository.py` | Contrato abstracto (ABC) con las operaciones requeridas. |
| `memory_solicitud_repository.py` | Implementación que **delega todo** a la cola manual. |
| `soporte_service.py` | Lógica de negocio: validación, IDs únicos, coordinación. |
| `consola.py` | Menú interactivo que solo habla con el servicio. |

### 5.4 Inyección de dependencias

El servicio recibe el repositorio en su constructor:

```python
repositorio = MemorySolicitudRepository()
servicio = SoporteService(repositorio)  # Inyección
```

Si en el futuro se quisiera guardar datos en una base de datos, bastaría con crear una nueva implementación de `SolicitudRepository` y pasarla al servicio, **sin modificar la lógica de negocio**.

### 5.5 Almacenamiento en memoria

El repositorio **no mantiene ninguna colección paralela**. Toda la información se almacena exclusivamente en la cola FIFO. Al cerrar la aplicación, los datos se pierden. No se utiliza base de datos ni persistencia en archivos.

---

## 6. Instrucciones de ejecución

### Requisitos
- Python 3.8 o superior.

### Instalación
```bash
git clone https://github.com/<USUARIO>/semana7-cola-repository-python.git
cd semana7-cola-repository-python
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Ejecutar la aplicación
```bash
python main.py
```

### Ejecutar las pruebas
```bash
python -m pytest -v
```

---

## 7. Descripción de las pruebas

Se implementaron **38 pruebas unitarias** organizadas en dos archivos:

### 7.1 Pruebas de la cola (`test_cola.py`) — 16 pruebas

| Categoría | Pruebas | Qué verifican |
|-----------|---------|----------------|
| Estado inicial | 2 | Cola nueva está vacía y tiene tamaño cero. |
| Enqueue | 3 | Agregar permite consultar; incrementa tamaño; conserva orden FIFO. |
| Dequeue | 5 | Devuelve elemento correcto; actualiza tamaño; respeta FIFO; deja cola vacía; actualiza referencias. |
| Peek | 3 | No elimina el elemento; no modifica tamaño; siempre devuelve el frente. |
| Cola vacía | 2 | `dequeue()` y `peek()` lanzan `IndexError`. |
| Reutilización | 1 | Se pueden agregar elementos después de vaciar la cola. |

### 7.2 Pruebas del repositorio y servicio (`test_repository_service.py`) — 22 pruebas

| Categoría | Pruebas | Qué verifican |
|-----------|---------|----------------|
| Repository vacío | 1 | Repositorio nuevo está vacío. |
| Guardar/consultar | 2 | Guardar y consultar/recuperar solicitudes. |
| Orden FIFO | 1 | Las solicitudes se atienden en orden de llegada. |
| Peek en repository | 1 | Consultar no elimina la solicitud. |
| Cantidad | 1 | El contador se actualiza correctamente. |
| Repository vacío (errores) | 2 | Lanza error al operar sobre repositorio vacío. |
| Registrar solicitud | 1 | Devuelve solicitud válida con datos correctos. |
| IDs únicos | 1 | Los identificadores son secuenciales. |
| Atender en orden | 1 | Se atiende en orden FIFO. |
| Consultar siguiente | 1 | Consultar no retira la solicitud. |
| Estado pendientes | 3 | Estado vacío/no vacío y cantidad se actualizan. |
| Errores sin solicitudes | 2 | Atender/consultar sin solicitudes lanza error. |
| Validación | 5 | Rechaza nombre vacío, solo espacios, descripción vacía, solo espacios; limpia espacios extra. |

---

## 8. Evidencias de ejecución de pytest

A continuación se muestra la **salida real** de la ejecución de `python -m pytest -v`:

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\elmij\Music\programacion 27\semana7-cola-repository-python
plugins: anyio-4.15.1, flet-1.0.0
collected 38 items

tests/test_cola.py::TestColaVaciaInicial::test_cola_nueva_esta_vacia PASSED       [  2%]
tests/test_cola.py::TestColaVaciaInicial::test_cola_nueva_tiene_tamano_cero PASSED [  5%]
tests/test_cola.py::TestEnqueue::test_agregar_un_elemento_permite_consultarlo PASSED [  7%]
tests/test_cola.py::TestEnqueue::test_agregar_un_elemento_incrementa_tamano PASSED [ 10%]
tests/test_cola.py::TestEnqueue::test_agregar_varios_elementos_conserva_orden_fifo PASSED [ 13%]
tests/test_cola.py::TestDequeue::test_retirar_devuelve_el_elemento_correcto PASSED [ 15%]
tests/test_cola.py::TestDequeue::test_retirar_actualiza_el_tamano PASSED         [ 18%]
tests/test_cola.py::TestDequeue::test_retirar_varios_respeta_orden_fifo PASSED   [ 21%]
tests/test_cola.py::TestDequeue::test_retirar_todos_los_elementos_deja_cola_vacia PASSED [ 23%]
tests/test_cola.py::TestDequeue::test_retirar_ultimo_elemento_actualiza_frente_y_final PASSED [ 26%]
tests/test_cola.py::TestPeek::test_peek_no_elimina_el_elemento PASSED            [ 28%]
tests/test_cola.py::TestPeek::test_peek_no_modifica_el_tamano PASSED             [ 31%]
tests/test_cola.py::TestPeek::test_peek_devuelve_siempre_el_frente PASSED        [ 34%]
tests/test_cola.py::TestColaVaciaOperaciones::test_dequeue_en_cola_vacia_lanza_error PASSED [ 36%]
tests/test_cola.py::TestColaVaciaOperaciones::test_peek_en_cola_vacia_lanza_error PASSED [ 39%]
tests/test_cola.py::TestReutilizacionCola::test_agregar_elementos_despues_de_vaciar_la_cola PASSED [ 42%]
tests/test_repository_service.py::TestMemorySolicitudRepository::test_repositorio_nuevo_esta_vacio PASSED [ 44%]
tests/test_repository_service.py::TestMemorySolicitudRepository::test_guardar_y_consultar_solicitud PASSED [ 47%]
tests/test_repository_service.py::TestMemorySolicitudRepository::test_guardar_y_recuperar_solicitud PASSED [ 50%]
tests/test_repository_service.py::TestMemorySolicitudRepository::test_orden_fifo_en_repositorio PASSED [ 52%]
tests/test_repository_service.py::TestMemorySolicitudRepository::test_consultar_siguiente_no_lo_elimina PASSED [ 55%]
tests/test_repository_service.py::TestMemorySolicitudRepository::test_cantidad_se_actualiza_correctamente PASSED [ 57%]
tests/test_repository_service.py::TestMemorySolicitudRepository::test_obtener_de_repositorio_vacio_lanza_error PASSED [ 60%]
tests/test_repository_service.py::TestMemorySolicitudRepository::test_consultar_de_repositorio_vacio_lanza_error PASSED [ 63%]
tests/test_repository_service.py::TestSoporteService::test_registrar_solicitud_devuelve_solicitud_valida PASSED [ 65%]
tests/test_repository_service.py::TestSoporteService::test_identificadores_unicos_secuenciales PASSED [ 68%]
tests/test_repository_service.py::TestSoporteService::test_atender_solicitudes_en_orden_de_llegada PASSED [ 71%]
tests/test_repository_service.py::TestSoporteService::test_consultar_siguiente_sin_eliminarla PASSED [ 73%]
tests/test_repository_service.py::TestSoporteService::test_hay_solicitudes_pendientes_inicialmente_false PASSED [ 76%]
tests/test_repository_service.py::TestSoporteService::test_hay_solicitudes_pendientes_despues_de_registrar PASSED [ 78%]
tests/test_repository_service.py::TestSoporteService::test_cantidad_pendientes PASSED [ 81%]
tests/test_repository_service.py::TestSoporteService::test_atender_sin_solicitudes_lanza_error PASSED [ 84%]
tests/test_repository_service.py::TestSoporteService::test_consultar_sin_solicitudes_lanza_error PASSED [ 86%]
tests/test_repository_service.py::TestSoporteService::test_rechazar_nombre_vacio PASSED [ 89%]
tests/test_repository_service.py::TestSoporteService::test_rechazar_nombre_solo_espacios PASSED [ 92%]
tests/test_repository_service.py::TestSoporteService::test_rechazar_descripcion_vacia PASSED [ 94%]
tests/test_repository_service.py::TestSoporteService::test_rechazar_descripcion_solo_espacios PASSED [ 97%]
tests/test_repository_service.py::TestSoporteService::test_nombre_se_limpia_de_espacios_extra PASSED [100%]

============================= 38 passed in 0.82s ==============================
```

**Resultado: 38 pruebas aprobadas, 0 fallidas.**

---

## 9. Ejemplo real de ejecución de la aplicación

A continuación se muestra una sesión completa de la aplicación:

```
=======================================================
   SISTEMA DE GESTIÓN DE TURNOS - SOPORTE TÉCNICO
=======================================================
  1. Registrar una solicitud
  2. Atender la solicitud más antigua
  3. Consultar la siguiente solicitud
  4. Comprobar si hay solicitudes pendientes
  5. Consultar cantidad de solicitudes pendientes
  6. Salir
-------------------------------------------------------
Seleccione una opción: 4

ℹ No hay solicitudes pendientes.

Seleccione una opción: 2

--- Atender solicitud ---
ℹ No hay solicitudes pendientes para atender.

Seleccione una opción: 1

--- Registrar nueva solicitud ---
Nombre del cliente: Carlos López
Descripción del problema: Mi computadora no enciende

✔ Solicitud registrada exitosamente:
  [Solicitud #1] Cliente: Carlos López | Problema: Mi computadora no enciende

Seleccione una opción: 1

--- Registrar nueva solicitud ---
Nombre del cliente: Ana García
Descripción del problema: Error de conexión a internet

✔ Solicitud registrada exitosamente:
  [Solicitud #2] Cliente: Ana García | Problema: Error de conexión a internet

Seleccione una opción: 1

--- Registrar nueva solicitud ---
Nombre del cliente: Pedro Martínez
Descripción del problema: Impresora no imprime

✔ Solicitud registrada exitosamente:
  [Solicitud #3] Cliente: Pedro Martínez | Problema: Impresora no imprime

Seleccione una opción: 5

📋 Hay 3 solicitudes pendientes.

Seleccione una opción: 3

--- Siguiente solicitud en espera ---
  [Solicitud #1] Cliente: Carlos López | Problema: Mi computadora no enciende

Seleccione una opción: 2

--- Atender solicitud ---
✔ Solicitud atendida:
  [Solicitud #1] Cliente: Carlos López | Problema: Mi computadora no enciende

Seleccione una opción: 3

--- Siguiente solicitud en espera ---
  [Solicitud #2] Cliente: Ana García | Problema: Error de conexión a internet

Seleccione una opción: 5

📋 Hay 2 solicitudes pendientes.

Seleccione una opción: 7

⚠ Opción no válida. Ingrese un número del 1 al 6.

Seleccione una opción: 1

--- Registrar nueva solicitud ---
Nombre del cliente:
Descripción del problema: Algo

⚠ Error: El nombre del cliente no puede estar vacío.

Seleccione una opción: 6

¡Hasta luego! El sistema se ha cerrado.
```

---

## 10. Enlace al repositorio público de GitHub

**Repositorio:** `https://github.com/<USUARIO>/semana7-cola-repository-python`

> ⚠ **Pendiente:** Reemplazar `<USUARIO>` con el nombre de usuario real de GitHub
> una vez que el repositorio sea publicado. Consultar la sección de pasos pendientes
> al final de este documento.

---

## 11. Conclusión

Este proyecto permitió comprender y aplicar tres conceptos fundamentales de la ingeniería de software:

1. **Tipos de datos abstractos lineales:** La implementación manual de una cola FIFO con nodos enlazados demuestra cómo funciona internamente esta estructura de datos, más allá de simplemente usar una librería. El manejo de las referencias `frente` y `final`, junto con el contador, garantiza operaciones eficientes en O(1).

2. **Patrones de diseño:** El patrón Repository separa la lógica de negocio del almacenamiento de datos, haciendo el código más mantenible y testeable. Si en el futuro se necesitara persistencia en base de datos, solo habría que crear una nueva implementación del repositorio sin modificar el servicio.

3. **Testing unitario:** Las 38 pruebas con pytest verifican que cada componente funciona correctamente de forma aislada, cubriendo casos normales, casos borde (cola vacía, datos inválidos) y la reutilización de la estructura después de vaciarla. Esto brinda confianza para realizar cambios sin introducir errores.

La combinación de estos tres pilares resulta en un software robusto, bien organizado y verificable.

---

*Documento preparado por David Patricio Ñauta Picon — UEES, septiembre 2026.*
