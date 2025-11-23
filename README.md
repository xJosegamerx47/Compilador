Language Compiler
A complete compiler implementation for a mini imperative language, built for the Theory of Computation course at Universidad de las Américas Puebla.
## Features
- **Lexical Analysis**: Regex-based tokenizer with comprehensive token definitions.
- **Syntax Analysis**: Recursive descent parser for a context-free grammar.
- **Semantic Analysis**: Type checking, scope management, and symbol table.
- **Error Handling**: Detailed error reporting for lexical, syntactic, and semantic errors.
- **Three-Address Code (TAC) Generation**: Translation of AST to TAC for a virtual machine.
## Project Structure
Compilador/
├── src/ # Source code
│ ├── parser.py
│ ├── analizador_semantico.py
│ └── lexer.py
