import re

# 1. Definición de Tipos de Token
# Se usa un diccionario donde la clave es el tipo de token y el valor
# es la expresión regular (regex) que define ese token.
TOKEN_TYPES = {
    # Las reglas con patrones más específicos (como palabras reservadas)
    # DEBEN ir primero para que tengan prioridad.
    'PALABRA_RESERVADA': r'(if|else|while|var|fun|print)',
    
    # 'IDENTIFICADOR' va después de 'PALABRA_RESERVADA'
    'STRING':            r'"[^"]*"',
    'IDENTIFICADOR':     r'[a-zA-Z_][a-zA-Z0-9_]*',
    
    'NUMERO_ENTERO':     r'\d+',
    
    # Operadores de comparación (los de 2 caracteres van primero)
    'OP_LOGICO': r'&&',
    'COMPARADOR':        r'==|!=|<=|>=|<|>',
    
    'OPERADOR_ASIGN':    r'=',
    'OPERADOR_ARIT':     r'[+\-*/]',
    # Delimitadores
    'PARENTESIS_IZQ':    r'\(',
    'PARENTESIS_DER':    r'\)',
    'LLAVE_IZQ':         r'\{',
    'LLAVE_DER':         r'\}',
    'PUNTO_Y_COMA':      r';',
    
    # Reglas para ignorar
    'ESPACIO_BLANCO':    r'\s+', # Coincide con espacios, tabs, saltos de línea
    'COMENTARIO':        r'#.*', # Comentarios de una línea (desde # hasta el final)
    
    # Regla de error: debe ir al final.
    # Coincide con CUALQUIER carácter ('.') que no fue
    # coincidido por ninguna de las reglas anteriores.
    'ERROR':             r'.'      
}

def analizar(codigo_fuente):
    """
    Implementación del analizador léxico.
    Recibe un string de código fuente y devuelve una lista de tuplas (tipo_token, lexema).
    """
    
    # 2. Compilación de la Expresión Regular Maestra
    # Unimos todas las expresiones regulares con el operador OR (|)
    # '(?P<NOMBRE>...)' crea un "grupo nombrado" en la regex.
    # Esto nos permite saber qué TIPO de token encontró la coincidencia.
    token_regex = '|'.join(f'(?P<{tipo}>{patron})' 
                           for tipo, patron in TOKEN_TYPES.items())
    
    tokens_generados = []
    
    # 3. Bucle Principal de Escaneo
    # re.finditer() escanea la cadena de izquierda a derecha y devuelve
    # un iterador de todos los objetos 'match' (coincidencias) que encuentra.
    # Esto implementa la regla de "emparejamiento más largo" (longest match)
    # y maneja el avance del puntero automáticamente.
    for match in re.finditer(token_regex, codigo_fuente):
        
        # 'match.lastgroup' nos da el NOMBRE del grupo que coincidió
        # (ej. 'IDENTIFICADOR', 'NUMERO_ENTERO', etc.)
        tipo_token = match.lastgroup
        
        # 'match.group()' nos da el texto exacto que coincidió (el lexema)
        lexema = match.group()
        
        # 4. Filtrado (Ignorar espacios y comentarios)
        # Si el token es de un tipo que queremos ignorar,
        # simplemente continuamos al siguiente 'match' sin guardarlo.
        if tipo_token == 'ESPACIO_BLANCO' or tipo_token == 'COMENTARIO':
            continue
            
        # 5. Manejo de Errores
        # Si el token es de tipo 'ERROR', significa que un carácter
        # no coincidió con ninguna regla válida.
        if tipo_token == 'ERROR':
            # En una implementación real, aquí se reportaría el
            # número de línea y columna.
            print(f"Error Léxico: Carácter inesperado '{lexema}'")
            continue

        # 6. Generación de Token
        # Si es un token válido y no debe ignorarse, lo agregamos a la lista.
        tokens_generados.append((tipo_token, lexema))
    
    # 7. Fin del Archivo
    # Agregamos un token especial para marcar el fin del análisis.
    tokens_generados.append(('EOF', 'End-Of-File'))
    
    return tokens_generados

# --- Ejemplo de Uso ---

# Código fuente de prueba
codigo_ejemplo = """
var x = 10;
var y = 20;

# Esto es un comentario que será ignorado
if (x > y) {
    x = y + 5;
} else {
    y = x * 2;
}

# Prueba de error
$ hola
"""

# Ejecutar el analizador
tokens = analizar(codigo_ejemplo)

# Imprimir los resultados
print("--- Resultados del Análisis Léxico ---")
for token in tokens:
    print(token)