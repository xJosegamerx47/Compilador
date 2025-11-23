class TACInterpreter:
    def __init__(self):
        self.memory = {}  # Memoria para variables
        self.temps = {}   # Valores de temporales
        
    def execute(self, tac_code):
        """Ejecuta código TAC"""
        lines = tac_code.strip().split('\n')
        pc = 0  # Program counter
        
        while pc < len(lines):
            line = lines[pc].strip()
            if not line:
                pc += 1
                continue
                
            # Parsear instrucción
            parts = line.split()
            
            if len(parts) >= 3 and parts[1] == '=':
                # Asignación: x = valor o t1 = a + b
                target = parts[0]
                if len(parts) == 3:
                    # Asignación simple: x = y
                    value = self.get_value(parts[2])
                    self.store_value(target, value)
                elif len(parts) == 5:
                    # Operación binaria: t1 = a + b
                    left = self.get_value(parts[2])
                    op = parts[3]
                    right = self.get_value(parts[4])
                    result = self.apply_operator(left, op, right)
                    self.store_value(target, result)
            
            pc += 1
        
        return self.memory
    
    def get_value(self, identifier):
        """Obtiene el valor de una variable o temporal"""
        # Si es un número
        if identifier.isdigit() or (identifier[0] == '-' and identifier[1:].isdigit()):
            return int(identifier)
        
        # Si es un string entre comillas
        if identifier.startswith('"') and identifier.endswith('"'):
            return identifier[1:-1]
        
        # Buscar en memoria de variables
        if identifier in self.memory:
            return self.memory[identifier]
        
        # Buscar en temporales
        if identifier in self.temps:
            return self.temps[identifier]
        
        # Si no existe, retornar 0
        return 0
    
    def store_value(self, target, value):
        """Almacena un valor en variable o temporal"""
        if target.startswith('t'):
            self.temps[target] = value
        else:
            self.memory[target] = value
    
    def apply_operator(self, left, op, right):
        """Aplica un operador a dos valores"""
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left // right if right != 0 else 0
        else:
            raise ValueError(f"Operador no soportado: {op}")