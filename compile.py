#!/usr/bin/env python3
import sys

# Importamos los componentes que SÍ existen en tus otros archivos
try:
    from Analizador_lexico import analizar
    from parser import parse_source
    from analizador_semantico import SemanticAnalyzer
    from tac_generator import TACGenerator
    from tac_interpreter import TACInterpreter
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Asegúrate de que los archivos (Analizador_lexico.py, parser.py, etc.) estén en la misma carpeta.")
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Uso correcto: python3 compile.py <archivo.src>")
        return
    
    filename = sys.argv[1]
    
    try:
        # 1. Leer el archivo
        with open(filename, 'r') as f:
            source_code = f.read()
        
        print(f"--- Compilando: {filename} ---")
        
        # 2. Análisis Léxico
        print("1. Ejecutando Lexer...")
        tokens = analizar(source_code)
        
        # 3. Análisis Sintáctico (Parser)
        print("2. Ejecutando Parser...")
        try:
            ast = parse_source(source_code)
        except Exception as e:
            print(f"❌ Error Sintáctico: {e}")
            return

        # 4. Análisis Semántico
        print("3. Ejecutando Semántico...")
        try:
            analyzer = SemanticAnalyzer()
            analyzer.visit(ast)
        except Exception as e:
            print(f"❌ Error Semántico: {e}")
            return

        # 5. Generación de Código Intermedio (TAC)
        print("4. Generando TAC...")
        tac_gen = TACGenerator()
        tac_code = tac_gen.generate(ast)
        print("\n--- CÓDIGO TAC GENERADO ---")
        print(tac_code)
        print("---------------------------")

        # 6. Ejecución (Intérprete)
        print("5. Ejecutando...")
        interpreter = TACInterpreter()
        resultado = interpreter.execute(tac_code)
        
        print("\n✅ EJECUCIÓN EXITOSA.")
        print("Memoria final:")
        for k, v in resultado.items():
            if not k.startswith('t'): # Ocultamos temporales para limpiar la salida
                print(f"  {k} = {v}")
            
    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()