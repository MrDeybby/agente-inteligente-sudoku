# Agente Inteligente para Sudoku

Un agente inteligente capaz de resolver puzzles de Sudoku implementando diferentes técnicas de resolución como pares desnudos (naked pairs).

## Estructura del Proyecto

```
project/
├── sudoku_agent.ipynb     # Notebook principal con el agente inteligente 
├── sudoki_solver.py       # Módulo con la implementación del solver
├── tablero_facil.txt      # Tablero de ejemplo (fácil)
└── tablero_facil_naked_twins.txt  # Tablero para probar naked pairs
```

## Características

- Implementa técnicas de resolución de Sudoku:
  - Pares desnudos (naked pairs)
  - Análisis de candidatos
  - Seleccion unica
  
- Visualización del tablero y proceso de resolución
- Validación de movimientos
- Detección automática de pares desnudos
- Interfaz gráfica para mostrar el progreso

## Requisitos

- Python 3.11+
- Bibliotecas requeridas listadas en requirements.txt:
  - matplotlib

## Uso

1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar el notebook `sudoku_agent.ipynb`
4. El tablero se puede especificar en un archivo de texto con formato:
   - 9 líneas con 9 dígitos cada una
   - Usar 0 para casillas vacías

## Referencias

- [Técnica del Par Desnudo](https://www.sudoku.academy/es/learn/naked-pairs/)
- [Técnica de los Tríos Desnudos](https://www.sudoku.academy/es/learn/naked-triples/)

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE.md para más detalles.