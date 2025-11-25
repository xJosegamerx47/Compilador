from flask import Flask, render_template, request, jsonify
import sys
import os
import io
from contextlib import redirect_stdout

# --- IMPORTAMOS TUS MÓDULOS ---
# Nos aseguramos de que Python encuentre los archivos
sys.path.append(os.path.dirname(__file__))

try:
    from Analizador_lexico import analizar
    from parser import parse_source
    from analizador_semantico import SemanticAnalyzer
    from tac_generator import TACGenerator
    from tac_interpreter import TACInterpreter
except ImportError as e:
    print(f"Error importando módulos: {e}")

app = Flask(__name__)

# --- LÓGICA DE COMPILACIÓN ADAPTADA PARA WEB ---
def ejecutar_compilador(codigo_fuente):
    # Creamos un buffer para capturar los print()
    buffer = io.StringIO()
    
    # Todo lo que ocurra dentro del 'with' se guardará en 'buffer' en vez de salir a consola
    with redirect_stdout(buffer):
        print("=== INICIANDO COMPILACIÓN WEB ===\n")
        try:
            # 1. Léxico
            print("1. 📝 ANÁLISIS LÉXICO")
            tokens = analizar(codigo_fuente)
            print(f"✅ Tokens generados: {len(tokens)}")
            
            # 2. Sintáctico
            print("\n2. 📐 ANÁLISIS SINTÁCTICO")
            ast = parse_source(codigo_fuente)
            print("✅ AST generado exitosamente")
            
            # 3. Semántico
            print("\n3. 🎯 ANÁLISIS SEMÁNTICO")
            analyzer = SemanticAnalyzer()
            analyzer.visit(ast)
            print("✅ Análisis semántico completado")
            
            # 4. TAC y Ejecución
            print("\n4. ⚡ GENERACIÓN TAC Y EJECUCIÓN")
            tac_gen = TACGenerator()
            tac_code = tac_gen.generate(ast)
            
            interpreter = TACInterpreter()
            resultado = interpreter.execute(tac_code)
            
            print("\n[ CÓDIGO INTERMEDIO GENERADO ]")
            print(tac_code)
            
            print("\n[ MEMORIA FINAL ]")
            for k, v in resultado.items():
                if "temp_" not in k: # Tu filtro de temporales
                    print(f"   - {k} = {v}")
                    
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO: {str(e)}")
            # Opcional: imprimir traceback si quieres debuggear en web
            # import traceback
            # traceback.print_exc()

    # Devolvemos todo el texto capturado
    return buffer.getvalue()

# --- RUTAS DE FLASK ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.json
    codigo = data.get('code', '')
    
    if not codigo:
        return jsonify({'output': "⚠️ No enviaste código."})
    
    resultado_texto = ejecutar_compilador(codigo)
    return jsonify({'output': resultado_texto})

# Necesario para Vercel
if __name__ == '__main__':
    app.run(debug=True)