import matplotlib.pyplot as plt

class SudokuMatrix:
    
    def __init__(self, path_file:str):
        """
        Lee un archivo de texto con 9 líneas de 9 dígitos cada una para construir 
        el tablero inicial donde los 0 seran espacios a rellenar. También determina 
        las celdas bloqueadas (originales del puzzle).

        Parámetros:
        - path_file (str): Ruta del archivo de texto que contiene el tablero Sudoku.
        """
        with open(path_file, 'r') as f:    
            numbers = [list(map(int, list(linea.strip()))) for linea in f]
            sudoku_board = {letter:numbers[idx] for idx, letter in enumerate('ABCDEFGHI')}
            
        self._sudoku_board = sudoku_board
        self.__locked_cells(sudoku_board)
        
    
    def __locked_cells(self, board):
        locked_cells_list = set()
    
        for key, value in board.items():
            for i in range(9):
                if value[i]:
                    locked_cells_list.add((key, i))
        self._locked_cell = locked_cells_list
        
    # Validar si un número puede ser colocado en una mini cuadrícula 3x3 (no debe repetirse
    def __validate_mini_square(self, row:str, column:int, number:int) -> bool:
        row = 'ABCDEFGHI'.index(row)
        row_beging = row - row % 3
        column_begin = column - column % 3

        for i in range(3):
            for j in range(3):
                if self._sudoku_board['ABCDEFGHI'[row_beging + i]][column_begin + j] == number:
                    return False
        return True
    
    # Validar si un número puede ser colocado en una celda específica
    def _validate_play(self, row, column, number):
        LETTERS = 'ABCDEFGHI'
        if number in self._sudoku_board[row]:
            return False
        
        if number in [self._sudoku_board[i][column] for i in LETTERS]:
            return False
        
        if column == LETTERS.index(row):
            if number in [self._sudoku_board[j][i] for i, j in enumerate(LETTERS)]:
                return False

        if 8-column == LETTERS.index(row):
            if number in [self._sudoku_board[j][8-i] for i, j in enumerate(LETTERS)]:
                return False

        if not self.__validate_mini_square(row, column, number):
            return False
        
        if (row, column) in self._locked_cell:
            return False
        
        return True
    
    def play(self, cell, number, inplace=False):
        """
        Realiza un movimiento en el tablero de Sudoku.

        Entrada:
            board: Tablero de Sudoku en formato diccionario.
            locked_cells: cells bloqueadas del tablero.
            row: row donde se realiza el movimiento.
            column: Columna donde se realiza el movimiento.
            number: Número a colocar en la cell.

        Salida:
            board: Tablero de Sudoku actualizado con el movimiento realizado.
        """
        board = self._sudoku_board if inplace else {k: v[:] for k, v in self._sudoku_board.items()}
        row, column = cell[0], int(cell[1]) -1
        if self._validate_play(row, column, number):
            board[row][column] = number
        return board if not inplace else None

    @property
    def board(self):
        return self._sudoku_board
    
    @property
    def locked_cells(self):
        return self._locked_cell
    
    def graph_board(self):
        """
        Dibuja visualmente el tablero de Sudoku.

        - Los números bloqueados se muestran en azul.
        - Los números añadidos por el usuario en negro.
        - Posibles candidatos resaltan en rojo (si existen).
        """
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 9)
        ax.set_xticks(range(10))
        ax.set_yticks(range(10))
        ax.invert_yaxis()
        ax.xaxis.tick_top()

        # Cuadrícula 9×9 (línea gruesa cada 3)
        for i in range(10):
            lw = 2 if i % 3 == 0 else 0.5
            ax.axhline(i, color='black', lw=lw)
            ax.axvline(i, color='black', lw=lw)

        LETTERS = 'ABCDEFGHI'
        # ----- rellenar cells -----
        for row_letra in LETTERS:
            row_idx = LETTERS.index(row_letra)
            row = self._sudoku_board.get(row_letra) 

            for col_idx, valor in enumerate(row):
                x_centro = col_idx + 0.5
                y_centro = row_idx + 0.5

                if isinstance(valor, int) and 1 <= valor <= 9:
                    color_num = 'blue' if (row_letra, col_idx) in self._locked_cell else 'black'
                    ax.text(x_centro, y_centro, str(valor),
                            ha='center', va='center', fontsize=10, fontweight='bold', color=color_num)
                    
                elif isinstance(valor, str):
                    ax.text(x_centro, y_centro, str(valor),
                            ha='center', va='center', fontsize=10-len(valor), fontweight='bold', color='red')

        # Etiquetas columns 1-9
        for j in range(9):
            ax.text(j + 0.5, -0.4, str(j+1),
                    ha='center', va='center', fontsize=12)

        # Etiquetas rows A-I
        for i, letra in enumerate('ABCDEFGHI'):
            ax.text(-0.4, i + 0.5, letra,
                    ha='center', va='center', fontsize=12)

        ax.set_aspect('equal')
        plt.axis('off')
        plt.show()
        
class SudokuAgent:
    
    def _fill_board(sudoku_board:SudokuMatrix):
        for key, value in sudoku_board.board.items():
            for i in range(9):
                if (key, i) not in sudoku_board.locked_cells and (value[i] == 0 or isinstance(value[i], str)):
                    value[i] = '123456789'
                    posibles = [str(n) for n in range(1, 10) if sudoku_board._validate_play(key, i, n)]
                    value[i] = ''.join(posibles)
        return sudoku_board

    @classmethod
    def only_choise(cls, sudoku_board:SudokuMatrix, naked:bool=False, view_board:bool=True):
        LETTERS = 'ABCDEFGHI'
        lock = False
        solved = False
        sudoku_board.graph_board() if view_board else None
        
        while not lock and not solved:
            previous = {k: v.copy() for k, v in sudoku_board.board.items()}
            cls._fill_board(sudoku_board) if not naked else None
            sudoku_board.graph_board() if view_board else None

            filled = 0
            for row in LETTERS:
                for i in range(9):
                    val = sudoku_board.board[row][i]
                    if isinstance(val, int):
                        filled += 1
                        continue
                    if len(val) == 1:
                        if val.isdigit() and sudoku_board._validate_play(row, i, int(val)):
                            sudoku_board.board[row][i] = int(val)
                        else:
                            raise ValueError(f"Invalid move at {row}{i} with value {val}")
                    elif len(val) == 0:
                        lock = True
            
            if previous == sudoku_board.board:
                lock = True
            if filled == 81:
                solved = True

        return sudoku_board

    @staticmethod
    def _is_pair(value:str) -> bool:
        return isinstance(value, str) and len(value) == 2

    @staticmethod
    def _get_elements():
        LETTERS = "ABCDEFGHI"
        units = []

        for row in LETTERS:
            units.append([(row, col) for col in range(9)])

        for col in range(9):
            units.append([(row, col) for row in LETTERS])

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                units.append([
                    (LETTERS[box_row + i], box_col + j)
                    for i in range(3) for j in range(3)
                ])
        return units

    @staticmethod
    def _find_naked_twins(sudoku_board:SudokuMatrix, unit):
        seen = {}
        twins = []

        for (f, c) in unit:
            val = sudoku_board.board[f][c]
            if isinstance(val, str) and len(val) == 2:
                key = frozenset(val)
                if key in seen:
                    other = seen[key]
                    twins.append((key, [(f, c), other]))
                else:
                    seen[key] = (f, c)

        return twins

    @staticmethod
    def _delete_numbers_pair(sudoku_board:SudokuMatrix, unit, pair, cells):
        for (f, c) in unit:
            if (f, c) in cells:
                continue
            val = sudoku_board.board[f][c]
            if isinstance(val, str) and len(val) > 1:
                nueva = ''.join(sorted(set(val) - pair))
                if nueva != val:
                    print(f"Eliminando {pair} de ({f}{c}): '{val}' -> '{nueva}'")
                    sudoku_board.board[f][c] = nueva

    @classmethod
    def _solve_naked_twins(cls, sudoku_board:SudokuMatrix):
        for unit in cls._get_elements():
            twins = cls._find_naked_twins(sudoku_board, unit)
            for pair, cells in twins:
                
                print(f"Par gemelo: {cells[0][0], cells[0][1]+1} y {cells[1][0], cells[1][1]+1} con valores {set(pair)}")
                cls._delete_numbers_pair(sudoku_board, unit, set(pair), cells)
        return sudoku_board

    @classmethod
    def solve_sudoku(cls, sudoku_board:SudokuMatrix):
        previous_board = {}
        sudoku_board.graph_board()
        cls._fill_board(sudoku_board)

        while True:
            if previous_board == sudoku_board.board:
                break
            previous_board = {k: v.copy() for k, v in sudoku_board.board.items()}

            cls.only_choise(sudoku_board, naked=True, view_board=False)
            cls._fill_board(sudoku_board)
            cls._solve_naked_twins(sudoku_board)

            if previous_board != sudoku_board.board:
                sudoku_board.graph_board()

        return sudoku_board
