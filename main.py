# main.py
import os
import sys

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(__file__))

try:
    # Importar el analizador léxico
    from Analizador_lexico import analizar
    
    # Importar el parser
    from parser import Parser, parse_source
    
    # Importar el analizador semántico
    from analizador_semantico import SemanticAnalyzer
    
    # Importar componentes TAC (si los tienes)
    try:
        from tac_generator import TACGenerator
        from tac_interpreter import TACInterpreter
        TAC_AVAILABLE = True
    except ImportError:
        print("⚠️  Componentes TAC no disponibles - solo análisis")
        TAC_AVAILABLE = False
    
    def compilar_codigo_fuente(codigo_fuente):
        """Función principal de compilación"""
        print("=== INICIANDO COMPILACIÓN ===")
        print("Código fuente:")
        print(codigo_fuente)
        print("\n" + "="*50)
        
        try:
            # 1. ANÁLISIS LÉXICO
            print("\n1. 📝 ANÁLISIS LÉXICO")
            tokens = analizar(codigo_fuente)
            print(f"✅ Tokens generados: {len(tokens)}")
            for i, token in enumerate(tokens):
                print(f"   {i+1:2d}. {token}")
            
            # 2. ANÁLISIS SINTÁCTICO
            print("\n2. 📐 ANÁLISIS SINTÁCTICO")
            ast = parse_source(codigo_fuente)
            print("✅ AST generado exitosamente")
            print(f"   Tipo: {type(ast)}")
            
            # 3. ANÁLISIS SEMÁNTICO
            print("\n3. 🎯 ANÁLISIS SEMÁNTICO")
            analyzer = SemanticAnalyzer()
            analyzer.visit(ast)
            print("✅ Análisis semántico completado")
            
            # 4. GENERACIÓN DE CÓDIGO (si está disponible)
            if TAC_AVAILABLE:
                print("\n4. ⚡ GENERACIÓN DE CÓDIGO TAC")
                tac_gen = TACGenerator()
                tac_code = tac_gen.generate(ast)
                print("✅ Código TAC generado:")
                print(tac_code)
                
                print("\n5. 🚀 EJECUCIÓN")
                interpreter = TACInterpreter()
                resultado = interpreter.execute(tac_code)
                print("✅ Ejecución completada")
                print("   Variables finales:")
                for variable, valor in resultado.items():
                    print(f"   - {variable} = {valor}")
            else:
                print("\n✅ COMPILACIÓN COMPLETADA (solo análisis)")
                
            return True
            
        except Exception as e:
            print(f"❌ Error durante la compilación: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Código de prueba
    if __name__ == "__main__":
        codigo_ejemplo = """
        var int x = 10;
        var int y = 20;
        x = x + y;
        """
        
        compilar_codigo_fuente(codigo_ejemplo)

except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n📋 Asegúrate de tener estos archivos en la misma carpeta:")
    print("   - Analizador_lexico.py")
    print("   - parser.py") 
    print("   - analizador_semantico.py")
    print("\n💡 Si tu archivo léxico se llama 'Analizador lexico.py', renómbralo a 'Analizador_lexico.py'")