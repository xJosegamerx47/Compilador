# Mini-Compilador e Intérprete con Generación de TAC

> Un sistema modular de compilación desarrollado en Python que implementa el ciclo completo de traducción: desde el código fuente hasta la ejecución mediante Código de Tres Direcciones (TAC).

## 📖 Descripción General

Este proyecto es una implementación educativa de un compilador diseñada para procesar un lenguaje de programación personalizado. El sistema no solo analiza la sintaxis, sino que valida la semántica (tipos y declaraciones), genera un código intermedio optimizado y lo ejecuta en una máquina virtual (intérprete).

El proyecto demuestra el dominio de las fases clásicas de la teoría de compiladores y lenguajes formales.

## ⚙️ Arquitectura del Sistema

El flujo de compilación sigue una arquitectura de "Pipeline" secuencial:

| Fase              | Módulo                    | Descripción Técnica                                                                                                                        |
| ----------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Léxico**     | `Analizador_lexico.py`    | Tokenización mediante **Expresiones Regulares**. Identifica palabras reservadas, operadores e identificadores.                             |
| **2. Sintáctico** | `parser.py`               | Análisis mediante **Descenso Recursivo**. Construye el Árbol de Sintaxis Abstracta (AST).                                                  |
| **3. Semántico**  | `analizador_semantico.py` | Patrón **Visitor**. Realiza comprobación de tipos (`int` vs `string`) y validación de scopes (declaración de variables).                   |
| **4. Generación** | `tac_generator.py`        | Aplanamiento del AST. Transforma estructuras jerárquicas en **Código de Tres Direcciones** (TAC) usando variables temporales (`t1`, `t2`). |
| **5. Ejecución**  | `tac_interpreter.py`      | Máquina virtual que procesa el código TAC y gestiona la memoria de ejecución.                                                              |

## 🛠️ Requisitos e Instalación

Este proyecto funciona con **Python 3.x** nativo y no requiere librerías externas (`pip install` no es necesario).

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/mini-compilador.git](https://github.com/tu-usuario/mini-compilador.git)
   cd mini-compilador
   ```

2.  **Verificar estructura:**
    Asegúrate de tener los siguientes archivos en el directorio:
    - `compile.py` (Script principal)
    - `Analizador_lexico.py`
    - `parser.py`
    - `analizador_semantico.py`
    - `tac_generator.py`
    - `tac_interpreter.py`

## 💻 Guía de Uso

Para compilar y ejecutar un archivo de código fuente, utiliza el script orquestador `compile.py`.

### Sintaxis del Comando

```bash
python3 compile.py <archivo_fuente.src>
```

### Ejemplo de Ejecución

```bash
python3 compile.py prueba.src
```

## 📝 Especificación del Lenguaje

El compilador acepta archivos de texto plano (extensión recomendada `.src`). A continuación se detalla la sintaxis soportada:

### Declaración de Variables

Es obligatorio tipar las variables y asignarles un valor inicial.

```text
var int edad = 20;
var string nombre = "Noel";
```

### Operaciones Aritméticas

Soporta expresiones complejas que el compilador desglosará automáticamente.

```text
var int resultado = 0;
resultado = 10 + 20 + 5;
# El compilador generará temporales internos para resolver esto
```

### Comentarios

Las líneas que inician con `#` son ignoradas por el analizador léxico.

```text
# Esto es un comentario
var int x = 1;
```

## 📊 Ejemplo de Salida en Consola

Al ejecutar el compilador, verás el detalle de cada etapa:

```text
--- Compilando: prueba.src ---
1. Ejecutando Lexer...
2. Ejecutando Parser...
3. Ejecutando Semántico...
   Analizando declaración: int costo
   Analizando asignación para: total
4. Generando TAC...

--- CÓDIGO TAC GENERADO ---
t1 = costo + impuesto
t2 = t1 + 10
total = t2
---------------------------
5. Ejecutando...

✅ EJECUCIÓN EXITOSA.
Memoria final:
  costo = 100
  impuesto = 20
  total = 130
```

## 📂 Estructura de Archivos

- `compile.py`: Punto de entrada (Entry Point). Maneja errores y coordina los módulos.
- `analizador_semantico.py`: Contiene también las definiciones de clases del AST (`Node`, `BinOp`, `Assign`, etc.).
- `parser.py`: Lógica de gramática libre de contexto.
- `prueba.src`: Archivo de demostración.
