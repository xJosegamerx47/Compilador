from analizador_semantico import NodeVisitor

class TACGenerator(NodeVisitor):
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def emit(self, code):
        self.code.append(code)

    def get_code(self):
        return "\n".join(self.code)

    def visit_Block(self, node):
        for child in node.children:
            self.visit(child)

    def visit_VarDecl(self, node):
        # Las declaraciones no generan código TAC
        pass

    def visit_Assign(self, node):
        # Asignación: target = value
        value_temp = self.visit(node.value)
        self.emit(f"{node.target.name} = {value_temp}")

    def visit_BinOp(self, node):
        left_temp = self.visit(node.left)
        right_temp = self.visit(node.right)
        result_temp = self.new_temp()
        self.emit(f"{result_temp} = {left_temp} {node.op} {right_temp}")
        return result_temp

    def visit_Identifier(self, node):
        return node.name

    def visit_Num(self, node):
        return str(node.value)

    def visit_String(self, node):
        return f'"{node.value}"'

class TACInterpreter:
    def __init__(self):
        self.memory = {}

    def execute(self, code):
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Dividir la línea en partes
            parts = line.split()

            # Asignación simple: x = 5
            if len(parts) == 3 and parts[1] == '=':
                var = parts[0]
                value_str = parts[2]

                # Si el valor es un número, convertirlo
                if value_str.isdigit():
                    self.memory[var] = int(value_str)
                else:
                    # Si es un string entre comillas, guardar como string
                    if value_str.startswith('"') and value_str.endswith('"'):
                        self.memory[var] = value_str[1:-1]
                    else:
                        # Es un identificador o temporal
                        self.memory[var] = self.memory.get(value_str, 0)

            # Operación binaria: t1 = a + b
            elif len(parts) == 5 and parts[1] == '=' and parts[3] in ['+', '-', '*', '/']:
                var = parts[0]
                left_str = parts[2]
                op = parts[3]
                right_str = parts[4]

                # Obtener valor izquierdo
                if left_str.isdigit():
                    left_val = int(left_str)
                else:
                    left_val = self.memory.get(left_str, 0)

                # Obtener valor derecho
                if right_str.isdigit():
                    right_val = int(right_str)
                else:
                    right_val = self.memory.get(right_str, 0)

                # Realizar operación
                if op == '+':
                    self.memory[var] = left_val + right_val
                elif op == '-':
                    self.memory[var] = left_val - right_val
                elif op == '*':
                    self.memory[var] = left_val * right_val
                elif op == '/':
                    self.memory[var] = left_val // right_val  # División entera

        # Imprimir resultados
        print("Execution completed. Memory state:")
        for var, value in self.memory.items():
            print(f"  {var} = {value}")
