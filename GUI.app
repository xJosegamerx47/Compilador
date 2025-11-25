import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QPushButton, QLabel, 
                             QFileDialog, QSplitter, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QColor, QTextCursor

class CompilerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mini-Compiler IDE - Noel Edition")
        self.setGeometry(100, 100, 1200, 700)
        self.setAcceptDrops(True) # Habilitar Drag & Drop global

        # --- ESTILOS (CSS) ---
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #d4d4d4;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QTextEdit {
                background-color: #252526;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                border-radius: 5px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                padding: 10px;
            }
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #094771;
            }
            QFrame {
                border: none;
            }
        """)

        # --- LAYOUT PRINCIPAL ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # HEADER
        header_layout = QHBoxLayout()
        self.lbl_status = QLabel("📁 Arrastra tu archivo .src aquí o escribe código")
        header_layout.addWidget(self.lbl_status)
        main_layout.addLayout(header_layout)

        # SPLITTER (Dividir pantalla Editor | Consola)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- EDITOR DE CÓDIGO (Izquierda) ---
        editor_container = QWidget()
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_editor = QLabel("📝 CÓDIGO FUENTE (.src)")
        self.txt_editor = QTextEdit()
        self.txt_editor.setPlaceholderText("Escribe tu código aquí o arrastra un archivo...")
        
        editor_layout.addWidget(lbl_editor)
        editor_layout.addWidget(self.txt_editor)
        
        # --- CONSOLA DE SALIDA (Derecha) ---
        console_container = QWidget()
        console_layout = QVBoxLayout(console_container)
        console_layout.setContentsMargins(0, 0, 0, 0)

        lbl_console = QLabel("💻 SALIDA DEL COMPILADOR")
        self.txt_console = QTextEdit()
        self.txt_console.setReadOnly(True)
        self.txt_console.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444;")
        
        console_layout.addWidget(lbl_console)
        console_layout.addWidget(self.txt_console)

        # Agregar al splitter
        splitter.addWidget(editor_container)
        splitter.addWidget(console_container)
        splitter.setSizes([600, 600]) # Tamaño inicial 50/50
        
        main_layout.addWidget(splitter)

        # --- BOTONES (Abajo) ---
        btn_layout = QHBoxLayout()
        
        self.btn_run = QPushButton("▶ EJECUTAR COMPILADOR")
        self.btn_run.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_run.clicked.connect(self.run_compiler)
        
        self.btn_clear = QPushButton("🗑 LIMPIAR")
        self.btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear.setStyleSheet("background-color: #444;")
        self.btn_clear.clicked.connect(self.clear_all)

        btn_layout.addWidget(self.btn_run)
        btn_layout.addWidget(self.btn_clear)
        main_layout.addLayout(btn_layout)

    # --- LÓGICA DE DRAG & DROP ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            file_path = files[0]
            if file_path.endswith('.src') or file_path.endswith('.txt'):
                self.load_file(file_path)
            else:
                self.lbl_status.setText("⚠️ Archivo no soportado. Usa .src")

    def load_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.txt_editor.setPlainText(content)
            self.lbl_status.setText(f"📂 Archivo cargado: {os.path.basename(file_path)}")
        except Exception as e:
            self.lbl_status.setText(f"❌ Error al leer archivo: {str(e)}")

    # --- LÓGICA DE EJECUCIÓN ---
    def run_compiler(self):
        code = self.txt_editor.toPlainText()
        if not code.strip():
            self.print_console("⚠️ El editor está vacío.", "orange")
            return

        # 1. Guardar código en un archivo temporal
        temp_filename = "temp_gui_run.src"
        with open(temp_filename, "w", encoding="utf-8") as f:
            f.write(code)

        self.txt_console.clear()
        self.print_console("🚀 Iniciando compilación...\n", "cyan")

        # 2. Ejecutar main.py usando subprocess
        # Esto es vital para capturar stdout y stderr
        try:
            process = subprocess.Popen(
                [sys.executable, 'main.py', temp_filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8' # Forzar UTF-8
            )
            
            # Capturar salida en tiempo real
            stdout, stderr = process.communicate()

            # 3. Procesar y colorear la salida
            if stdout:
                self.format_output(stdout)
            
            if stderr:
                self.print_console("\n=== ERRORES DETECTADOS ===", "red")
                self.print_console(stderr, "#ff5555") # Rojo claro para errores
            
            if process.returncode == 0 and not stderr:
                 self.print_console("\n✨ Ejecución finalizada con éxito.", "#50fa7b")

        except Exception as e:
            self.print_console(f"❌ Error crítico al ejecutar main.py: {str(e)}", "red")
        
        # Limpieza
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    def format_output(self, text):
        """Analiza el texto línea por línea para ponerle colores bonitos"""
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            
            if "❌" in line or "Error" in line:
                self.print_console(line, "#ff5555") # Rojo
            elif "✅" in line:
                self.print_console(line, "#50fa7b") # Verde
            elif "📝" in line or "📐" in line or "🎯" in line or "⚡" in line or "🚀" in line:
                self.print_console(line, "#8be9fd") # Cyan (Headers de fases)
            elif line.startswith("t") and "=" in line and line[1].isdigit(): 
                # Es código TAC (t1 = ...)
                self.print_console(line, "#f1fa8c") # Amarillo
            elif "Variables finales" in line:
                self.print_console(line, "#bd93f9") # Púrpura
            elif "OUT:" in line:
                self.print_console(line, "#ffffff", bold=True) # Blanco brillante (Prints)
            else:
                self.print_console(line, "#d4d4d4") # Gris normal

    def print_console(self, text, color, bold=False):
        """Método auxiliar para escribir HTML en la consola"""
        weight = "bold" if bold else "normal"
        # Reemplazar saltos de línea con <br>
        formatted_text = text.replace("\n", "<br>")
        html = f'<span style="color:{color}; font-weight:{weight};">{formatted_text}</span>'
        self.txt_console.append(html)

    def clear_all(self):
        self.txt_editor.clear()
        self.txt_console.clear()
        self.lbl_status.setText("📁 Listo")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Fuente global bonita
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = CompilerGUI()
    window.show()
    sys.exit(app.exec())