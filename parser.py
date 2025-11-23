# ... (código existente del parser) ...

# ===============================================================
# COMPILADOR COMPLETO: LEXER, PARSER, SEMÁNTICO, TAC, EJECUCIÓN
# ===============================================================

from tac_generator import TACGenerator
from tac_interpreter import TACInterpreter

def compile_and_execute(source_code):
    """Función principal que compila y ejecuta código fuente"""
    try:
        # 1. Análisis Léxico
        print("=== ANÁLISIS LÉXICO ===")
        tokens = analizar(source_code)
        for token in tokens:
            print(f"Token: {token}")
        
        # 2. Análisis Sintáctico
        print("\n=== ANÁLISIS SINTÁCTICO ===")
        parser = Parser(tokens)
        ast = parser.parse()
        print("AST generado exitosamente")
        
        # 3. Análisis Semántico
        print("\n=== ANÁLISIS SEMÁNTICO ===")
        from analizador_semantico import SemanticAnalyzer
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(ast)
        print("Análisis semántico exitoso")
        
        # 4. Generación de Código TAC
        print("\n=== GENERACIÓN DE CÓDIGO TAC ===")
        tac_generator = TACGenerator()
        tac_code = tac_generator.generate(ast)
        print("Código TAC generado:")
        print(tac_code)
        
        # 5. Ejecución
        print("\n=== EJECUCIÓN ===")
        interpreter = TACInterpreter()
        result = interpreter.execute(tac_code)
        print("Resultado de la ejecución:")
        for var, value in result.items():
            print(f"  {var} = {value}")
            
        return {
            'tokens': tokens,
            'ast': ast,
            'tac_code': tac_code,
            'execution_result': result
        }
        
    except Exception as e:
        print(f"Error durante la compilación: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    source = """
    var int x = 10;
    var int y = 20;
    x = x + y;
    var int z = x * 2;
    """
    
    result = compile_and_execute(source)