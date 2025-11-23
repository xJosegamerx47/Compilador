class Node:
    """Clase base para todos los nodos del AST"""
    pass

class Block(Node):
    """Representa un bloque de declaraciones o sentencias."""
    def __init__(self, children):
        self.children = children

class VarDecl(Node):
    """Declaración de variable (ej. 'int x')"""
    def __init__(self, var_type, var_name):
        self.var_type = var_type
        self.var_name = var_name

class Assign(Node):
    """Asignación (ej. 'x = 10')"""
    def __init__(self, target, value):
        self.target = target 
        self.value = value   

class BinOp(Node):
    """Operación binaria (ej. 'a + b')"""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Identifier(Node):
    """Un identificador (ej. el nombre de una variable)"""
    def __init__(self, name):
        self.name = name

class Num(Node):
    """Un número literal (ej. 5)"""
    def __init__(self, value):
        self.value = value

class String(Node):
    """Una cadena literal (ej. "hola")"""
    def __init__(self, value):
        self.value = value


class Symbol:
    """Clase para guardar la información de un símbolo"""
    def __init__(self, name, var_type):
        self.name = name
        self.type = var_type

class SymbolTable:
    def __init__(self):
        self.scope_stack = [{}]

    def enter_scope(self):
        """Entra a un nuevo ámbito (ej. al entrar a un bloque '{')"""
        self.scope_stack.append({})

    def exit_scope(self):
        """Sale del ámbito actual (ej. al salir de un bloque '}')"""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
        else:
            print("Error: No se puede salir del ámbito global.")

    def declare(self, symbol):
        """
        Declara un nuevo símbolo (variable) en el ÁMBITO ACTUAL.
        Retorna True si la declaración es exitosa, False si ya existe.
        """
        current_scope = self.scope_stack[-1]
        if symbol.name in current_scope:
            return False 
        current_scope[symbol.name] = symbol
        return True

    def lookup(self, name):
        """
        Busca un símbolo por nombre, desde el ámbito actual hacia afuera.
        Retorna el objeto Symbol si lo encuentra, o None si no.
        """
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        return None 

class NodeVisitor:
    def visit(self, node):
        """Función de despacho principal"""
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        Visitador genérico: se llama si no hay un 'visit_TipoDeNodo' específico.
        Simplemente visita a todos los hijos.
        """
        if isinstance(node, Block):
            for child in node.children:
                self.visit(child)

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_Block(self, node):
        """Visita un bloque: entramos a un nuevo ámbito"""
        self.symbol_table.enter_scope()
        for child in node.children:
            self.visit(child)
        self.symbol_table.exit_scope()

    def visit_VarDecl(self, node):
        """
        Regla Semántica: Declaración de variable.
        1. ¿Ya existe en el ámbito actual?
        """
        print(f"Analizando declaración: {node.var_type} {node.var_name}")
        symbol = Symbol(name=node.var_name, var_type=node.var_type)
        
        if not self.symbol_table.declare(symbol):
            raise Exception(f"Error Semántico: Variable '{node.var_name}' ya declarada en este ámbito.")

    def visit_Assign(self, node):
        """
        Regla Semántica: Asignación.
        1. ¿Existe la variable destino?
        2. ¿Coinciden los tipos (el de la variable y el del valor)?
        """
        print(f"Analizando asignación para: {node.target.name}")
        
        var_symbol = self.symbol_table.lookup(node.target.name)
        if not var_symbol:
            raise Exception(f"Error Semántico: Variable '{node.target.name}' no ha sido declarada.")

        value_type = self.visit(node.value)

        if var_symbol.type != value_type:
            raise Exception(f"Error Semántico: Incompatibilidad de tipos. "
                            f"No se puede asignar tipo '{value_type}' a la variable '{var_symbol.name}' de tipo '{var_symbol.type}'.")

    def visit_BinOp(self, node):
        """
        Regla Semántica: Operación Binaria.
        1. ¿Qué tipo tienen los operandos?
        2. ¿Son compatibles para la operación?
        DEVUELVE: El tipo del resultado de la operación.
        """
        print(f"Analizando BinOp: {node.op}")
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if node.op == '+':
            if left_type == 'int' and right_type == 'int':
                return 'int' 
            else:
                raise Exception(f"Error Semántico: Operación '+' no válida para tipos '{left_type}' y '{right_type}'.")
        
        raise Exception(f"Error Semántico: Operador binario '{node.op}' no reconocido.")

    def visit_Identifier(self, node):
        """
        Regla Semántica: Uso de una variable (en una expresión).
        1. ¿Existe?
        DEVUELVE: El tipo de la variable.
        """
        print(f"Analizando identificador: {node.name}")
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            raise Exception(f"Error Semántico: Variable '{node.name}' no ha sido declarada.")
        
        return symbol.type

    def visit_Num(self, node):
        """Tipo de un literal numérico"""
        return 'int'

    def visit_String(self, node):
        """Tipo de un literal de cadena"""
        return 'string'


def main():
    

    ast_valido = Block([
        VarDecl('int', 'x'),
        Assign(Identifier('x'), Num(10)),
        VarDecl('string', 'y'),
        Assign(Identifier('y'), String("hola")),
        VarDecl('int', 'z'),
        Assign(Identifier('z'), BinOp(Identifier('x'), '+', Num(5)))
    ])

    print("--- ANALIZANDO AST VÁLIDO ---")
    try:
        analyzer_valido = SemanticAnalyzer()
        analyzer_valido.visit(ast_valido)
        print("ANÁLISIS SEMÁNTICO EXITOSO: El código es válido.")
    except Exception as e:
        print(f"ANÁLISIS FALLIDO: {e}")

    print("\n" + "="*30 + "\n")

    # --- EJEMPLO 2: ERROR (Tipo incompatible) ---
    # {
    #   int x;
    #   x = "hola"; // Error
    # }
    ast_error_tipo = Block([
        VarDecl('int', 'x'),
        Assign(Identifier('x'), String("hola"))
    ])

    print("--- ANALIZANDO AST CON ERROR DE TIPO ---")
    try:
        analyzer_error = SemanticAnalyzer()
        analyzer_error.visit(ast_error_tipo)
        print("ANÁLISIS SEMÁNTICO EXITOSO (¡Esto no debería pasar!).")
    except Exception as e:
        print(f"ANÁLISIS FALLIDO (CORRECTO): {e}")

    print("\n" + "="*30 + "\n")

    # --- EJEMPLO 3: ERROR (Variable no declarada) ---
    # {
    #   x = 10; // Error
    # }
    ast_error_no_decl = Block([
        Assign(Identifier('x'), Num(10))
    ])

    print("--- ANALIZANDO AST CON VARIABLE NO DECLARADA ---")
    try:
        analyzer_error = SemanticAnalyzer()
        analyzer_error.visit(ast_error_no_decl)
        print("ANÁLISIS SEMÁNTICO EXITOSO (¡Esto no debería pasar!).")
    except Exception as e:
        print(f"ANÁLISIS FALLIDO (CORRECTO): {e}")

    print("\n" + "="*30 + "\n")

    # --- EJEMPLO 4: ERROR (Variable re-declarada) ---
    # {
    #   int x;
    #   string x; // Error
    # }
    ast_error_redecl = Block([
        VarDecl('int', 'x'),
        VarDecl('string', 'x')
    ])

    print("--- ANALIZANDO AST CON VARIABLE RE-DECLARADA ---")
    try:
        analyzer_error = SemanticAnalyzer()
        analyzer_error.visit(ast_error_redecl)
        print("ANÁLISIS SEMÁNTICO EXITOSO (¡Esto no debería pasar!).")
    except Exception as e:
        print(f"ANÁLISIS FALLIDO (CORRECTO): {e}")


if __name__ == '__main__':
    main()