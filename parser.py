import importlib.util
import os

# ===============================================================
# IMPORTAR TU ANALIZADOR LÉXICO
# ===============================================================

LEXER_PATH = os.path.join(os.path.dirname(__file__), "Analizador_lexico.py")

def importar_lexer(path=LEXER_PATH):
    """Carga dinámica para importar tu lexer"""
    try:
        name = "lexer_usuario"
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error importando lexer: {e}")
        return None

# Importar el lexer
lexer_module = importar_lexer()
if lexer_module:
    analizar = lexer_module.analizar
else:
    # Fallback si no se puede importar
    def analizar(codigo):
        return [('ERROR', 'Lexer no disponible')]

# ===============================================================
# IMPORTAR TU AST Y ANALIZADOR SEMÁNTICO
# ===============================================================

try:
    from analizador_semantico import (
        Block, VarDecl, Assign, BinOp, Identifier, Num, String
    )
except ImportError:
    print("Error: No se pudo importar analizador_semantico")
    # Definir clases básicas como fallback
    class Node: pass
    class Block(Node):
        def __init__(self, children): self.children = children
    class VarDecl(Node):
        def __init__(self, var_type, var_name): 
            self.var_type = var_type; self.var_name = var_name
    class Assign(Node):
        def __init__(self, target, value): 
            self.target = target; self.value = value
    class BinOp(Node):
        def __init__(self, left, op, right): 
            self.left = left; self.op = op; self.right = right
    class Identifier(Node):
        def __init__(self, name): self.name = name
    class Num(Node):
        def __init__(self, value): self.value = value
    class String(Node):
        def __init__(self, value): self.value = value

# ===============================================================
# TOKEN STREAM
# ===============================================================

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', 'End-Of-File')

    def next(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def expect(self, tipo, lexema=None):
        t, l = self.peek()

        if t != tipo:
            raise Exception(f"Error sintáctico: se esperaba token '{tipo}', llegó '{t}' ({l})")

        if lexema is not None and l != lexema:
            raise Exception(f"Error sintáctico: se esperaba lexema '{lexema}', llegó '{l}'")

        return self.next()

    def accept(self, tipo, lexema=None):
        t, l = self.peek()
        if t == tipo and (lexema is None or l == lexema):
            return self.next()
        return None

# ===============================================================
# PARSER PRINCIPAL (DESCENSO RECURSIVO)
# ===============================================================

class Parser:
    def __init__(self, tokens):
        self.ts = TokenStream(tokens)

    def parse(self):
        """
        Punto de entrada del parser.
        Crea un bloque principal (programa).
        """
        return self.parse_block()

    # -----------------------------------------------------------
    # BLOQUES
    # -----------------------------------------------------------

    def parse_block(self):
        """
        block -> '{' stmt* '}'   |   stmt* (si no hay llaves)
        """
        children = []

        # Caso: bloque con llaves
        if self.ts.accept('LLAVE_IZQ'):
            while not self.ts.accept('LLAVE_DER'):
                children.append(self.parse_statement())
            return Block(children)

        # Caso: bloque sin llaves (nivel raíz)
        while self.ts.peek()[0] != 'EOF' and self.ts.peek()[0] != 'LLAVE_DER':
            children.append(self.parse_statement())

        return Block(children)

    # -----------------------------------------------------------
    # SENTENCIAS
    # -----------------------------------------------------------

    def parse_statement(self):
        tipo, lex = self.ts.peek()

        # var tipo name = expr ;
        if tipo == 'PALABRA_RESERVADA' and lex == 'var':
            return self.parse_var_decl()

        # assignment: IDENTIFICADOR = expr ;
        if tipo == 'IDENTIFICADOR':
            return self.parse_assign()

        raise Exception(f"Error sintáctico: sentencia no reconocida '{tipo}' '{lex}'")

    def parse_var_decl(self):
        """
        var TIPO NOMBRE = EXPR ;
        Ejemplo:
            var int x = 10;
        """
        self.ts.expect('PALABRA_RESERVADA', 'var')

        # TIPO:
        var_type = self.ts.expect('IDENTIFICADOR')[1]

        # NOMBRE:
        var_name = self.ts.expect('IDENTIFICADOR')[1]

        self.ts.expect('OPERADOR_ASIGN', '=')

        # Valor inicial:
        value = self.parse_expr()

        self.ts.expect('PUNTO_Y_COMA')

        # OJO: Tu semántico espera que VarDecl tenga SOLO (tipo, nombre)
        # y *NO* recibe el valor inicial.
        #
        # Así que aquí hacemos:
        #
        # VarDecl(tipo, nombre)
        # Assign(nombre, valor)
        #
        asignacion = Assign(Identifier(var_name), value)
        return Block([VarDecl(var_type, var_name), asignacion])

    def parse_assign(self):
        """
        NOMBRE = EXPR ;
        """
        name = self.ts.expect('IDENTIFICADOR')[1]

        self.ts.expect('OPERADOR_ASIGN')

        value = self.parse_expr()

        self.ts.expect('PUNTO_Y_COMA')

        return Assign(Identifier(name), value)

    # -----------------------------------------------------------
    # EXPRESIONES
    # -----------------------------------------------------------

    def parse_expr(self):
        return self.parse_add()

    def parse_add(self):
        """
        expr -> term { '+' term }
        """
        node = self.parse_term()

        while True:
            t, l = self.ts.peek()
            if t == 'OPERADOR_ARIT' and l == '+':
                self.ts.next()
                right = self.parse_term()
                node = BinOp(node, "+", right)
            else:
                break

        return node

    def parse_term(self):
        """
        term -> NUMBER | IDENT | '(' expr ')'
        """
        t, l = self.ts.peek()

        if t == 'NUMERO_ENTERO':
            self.ts.next()
            return Num(int(l))

        if t == 'IDENTIFICADOR':
            self.ts.next()
            return Identifier(l)

        if t == 'PARENTESIS_IZQ':
            self.ts.next()
            expr = self.parse_expr()
            self.ts.expect('PARENTESIS_DER', ')')
            return expr

        raise Exception(f"Error sintáctico: expresión inválida '{t}' '{l}'")

# ===============================================================
# FUNCIÓN DE UTILIDAD
# ===============================================================

def parse_source(source_code):
    tokens = analizar(source_code)
    parser = Parser(tokens)
    return parser.parse()

# ===============================================================
# EJECUCIÓN DIRECTA (PRUEBAS)
# ===============================================================

if __name__ == "__main__":
    src = """
    var int x = 10;
    var string y = "hola";
    x = x + 5;
    """

    print("=== PRUEBA DEL PARSER ===")
    print("Código fuente:")
    print(src)
    
    try:
        ast = parse_source(src)
        print("✅ AST GENERADO EXITOSAMENTE")
        print(f"Tipo: {type(ast)}")
        if hasattr(ast, 'children'):
            print(f"Número de hijos: {len(ast.children)}")
    except Exception as e:
        print(f"❌ Error: {e}")