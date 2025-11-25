class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.code = []
        self.symbol_table = {}  # Tabla de símbolos para variables
        
    def new_temp(self):
      """Genera un nuevo temporal"""
      self.temp_count += 1
      return f"temp_{self.temp_count}"
    
    def new_label(self):
        """Genera una nueva etiqueta"""
        self.label_count += 1
        return f"L{self.label_count}"
    
    def emit(self, instruction):
        """Emite una instrucción TAC"""
        self.code.append(instruction)
    
    def generate(self, ast):
        """Genera código TAC a partir del AST"""
        self.visit(ast)
        return "\n".join(self.code)
    
    def visit(self, node):
        """Método de visita para nodos del AST"""
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Visitante genérico"""
        if hasattr(node, 'children'):
            for child in node.children:
                self.visit(child)
    
    def visit_Block(self, node):
        for child in node.children:
            self.visit(child)
    
    def visit_VarDecl(self, node):
        # En TAC, las declaraciones no generan código directamente
        # Solo registramos la variable en la tabla de símbolos
        self.symbol_table[node.var_name] = node.var_type
    
    def visit_Assign(self, node):
        # Generar código para el valor
        value_temp = self.visit(node.value)
        # Emitir asignación
        self.emit(f"{node.target.name} = {value_temp}")
        return node.target.name
    
    def visit_BinOp(self, node):
        # Generar código para operandos
        left_temp = self.visit(node.left)
        right_temp = self.visit(node.right)
        
        # Crear temporal para resultado
        result_temp = self.new_temp()
        
        # Emitir operación
        self.emit(f"{result_temp} = {left_temp} {node.op} {right_temp}")
        
        return result_temp
    
    def visit_Identifier(self, node):
        return node.name
    
    def visit_Num(self, node):
        return str(node.value)
    
    def visit_String(self, node):
        return f'"{node.value}"'
    def visit_Print(self, node):
        # 1. Calculamos el valor de la expresión (esto genera temporales si es necesario)
        val_temp = self.visit(node.expression)
        
        # 2. Emitimos la instrucción 'print'
        self.emit(f"print {val_temp}")
    def visit_IfStatement(self, node):
        # Por ahora, solo visitas para que genere el código de las expresiones internas
        self.visit(node.condition)
        self.visit(node.then_block)
        if node.else_block:
            self.visit(node.else_block)
        # Aquí iría la lógica compleja de generación de etiquetas L1, L2 y saltos.