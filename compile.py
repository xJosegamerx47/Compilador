#!/usr/bin/env python3
import sys
from parser import compile_and_execute

def main():
    if len(sys.argv) != 2:
        print("Uso: python compile.py <archivo.src>")
        return
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            source_code = f.read()
        
        print(f"Compilando: {filename}")
        result = compile_and_execute(source_code)
        
        if result:
            print("\n✅ Compilación y ejecución exitosas!")
        else:
            print("\n❌ Error en la compilación")
            
    except FileNotFoundError:
        print(f"Error: Archivo {filename} no encontrado")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()