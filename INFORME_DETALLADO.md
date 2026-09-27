# Informe Detallado del Sistema Experto (Clasificación de Rocas)

Este documento contiene la explicación profunda, técnica y académica del proyecto. Está estructurado de forma que puedas extraer y redactar fácilmente tu informe final para el docente.

---

## 1. Arquitectura del Proyecto

El sistema fue diseñado siguiendo un enfoque modular, limpio y orientado a objetos, separando las responsabilidades de ingeniería de conocimiento del flujo de entrada/salida (CLI).

- **`facts/facts.py`**: Define la *Ontología* del sistema. Aquí viven todas las clases (estructuras) que representan el conocimiento (Evidencias, Origen, etc.).
- **`engine/rules.py`**: Contiene la base de reglas lógicas bajo un esquema de encadenamiento hacia adelante (Forward Chaining). Utiliza un patrón de diseño llamado `Mixin` para inyectar estas reglas en el motor principal sin saturar un solo archivo.
- **`backward/goal_engine.py`**: Aísla las reglas de control. Simula el encadenamiento hacia atrás verificando qué información falta en la Memoria de Trabajo para lograr una meta y pidiéndosela al usuario.
- **`engine/engine.py`**: El corazón del sistema. Une el motor genérico (`KnowledgeEngine`) con nuestras reglas y anula/sobrescribe el bucle de ejecución principal para poder generar las trazas visuales (imprimir la Base de Hechos y el Conjunto Conflicto paso a paso).
- **`main.py`**: Archivo de arranque e interfaz de usuario en consola.
- **`tests/test_classification.py`**: Suite de pruebas unitarias automatizadas.

## 2. Librerías Utilizadas

El desarrollo se fundamenta exclusivamente en Python puro y la librería de Inteligencia Artificial simbólica:

- **`experta`** (y sus dependencias internas `frozendict` y `schema`): Es un motor de reglas para Python fuertemente inspirado en CLIPS. Implementa el **algoritmo Rete**, el cual es el estándar de la industria para sistemas expertos lógicos.
- **Parche de Compatibilidad (`collections.Mapping`)**: Dado que `experta` fue escrito para versiones antiguas de Python, utiliza un módulo deprecado (`collections.Mapping`). Para cumplir el requisito de usar Python 3.10+, aplicamos un "Monkey Patch" dinámico en `main.py` que redirige `collections.Mapping` hacia su nueva ubicación en `collections.abc.Mapping`, logrando compatibilidad total sin modificar el código fuente de la librería.

## 3. Representación del Conocimiento (Los Hechos)

Los elementos atómicos de información (Working Memory Elements) heredan de la clase `Fact`. En lugar de variables sueltas, usamos una estructura `clave=valor` inmutable:

1. **`Evidence`**: Atributos físicos observables de la roca proporcionados por el usuario (ej. `texture="clastic"`, `grain_size="fine"`).
2. **`Origin`**: Hecho intermedio inferido por el sistema (Ígneo, Sedimentario o Metamórfico).
3. **`Classification`**: La deducción del tipo de roca exacto (ej. `type="basalt"`).
4. **`Recommendation`**: Deducción final que liga el tipo de roca con un uso industrial/comercial.
5. **`Goal` y `Request`**: Hechos especiales de control para el motor de encadenamiento hacia atrás. `Goal` define la meta actual, y `Request` le avisa a `main.py` qué variable se le debe preguntar al usuario.

## 4. El Motor de Inferencia y el Algoritmo Rete

El motor Rete está configurado para evitar re-evaluaciones completas, funcionando en dos capas (Redes):

- **Red Alfa**: Cuando se hace un `declare(Evidence(texture="glassy"))`, el hecho pasa por un nodo alfa que evalúa esa condición singular. Solo se evalúa una vez, sin importar cuántas reglas usen la textura vidriosa.
- **Red Beta**: Hace las uniones (JOINs). Si una regla exige `Origin=Igneous` Y `texture=glassy`, el nodo Beta almacena temporalmente las mitades de la condición hasta que ambas se cumplen, momento en el que genera una "Activación".

### El Ciclo Match-Resolve-Act y El Trazador
En `engine/engine.py` reescribimos la función `run()` nativa de Experta para imprimir el estado exacto del motor. Este ciclo hace:
1. **Match**: Busca hechos que cumplan condiciones y pone las reglas resultantes en la *Agenda*.
2. **Resolve (Resolución de Conflictos)**: Si hay más de una regla lista para dispararse (Conjunto Conflicto), usa la prioridad (salience) o el orden léxico para elegir la mejor.
3. **Act**: Dispara el lado derecho (RHS) de la regla elegida. 
*Nuestro trazador expone este proceso interno directamente en la consola para demostración pedagógica.*

## 5. Las Reglas (Base de Conocimiento)

Implementamos un total de **14 Reglas de Encadenamiento Hacia Adelante** estructuradas en 3 niveles de abstracción lógicos:

- **Nivel 1 (Evidencia -> Origen)**: Abstracción primaria (ej. Si textura es foliada O granoblástica, el Origen es Metamórfico). Emplea el operador lógico `OR` de Experta.
- **Nivel 2 (Unión: Origen + Evidencia -> Clasificación)**: Deduzcen el tipo de roca combinando el nivel anterior con nuevos detalles. Permiten clasificar 10 rocas exactas: *Granito, Basalto, Piedra Pómez, Obsidiana, Arenisca, Caliza, Pizarra, Gneis, Mármol, Cuarcita*.
- **Nivel 3 (Clasificación -> Recomendación)**: Utiliza la funcionalidad de ligadura de variables (`MATCH.rock_type`) de Rete para capturar dinámicamente el nombre de la roca y disparar una recomendación de uso industrial, completando así el análisis experto.

Adicionalmente, se programaron **6 Reglas de Encadenamiento Hacia Atrás** (Goal-Driven). Estas reglas se disparan únicamente cuando existe el hecho `Goal(target="classify")` y emplean el operador de negación condicional `NOT(Evidence(...))`. Su RHS inyecta a la memoria un hecho `Request`, pausando la deducción hasta que el sistema externo (`main.py`) capture el dato del usuario.
