import re
import tkinter as tk
from tkinter import messagebox

grammar = """
        start: var_s | main_s | ciclo_s | condicion_s | funcion_s

        p1: "("
        p2: ")"
        r: l r |
        k: "vos"
        i: "ira"
        h: n h |

        c: "contenido"
        c1: "{"
        c2: "}"
        o: "<" | ">" | "==" | "!=" | "<=" | ">="
        v: "->"
        m: "main"
        t: "tons"
        f: "act"
        e: "en"
        g: ","

        var_s: r a
        a: v h | v r

        main_s: f j
        j: m j1
        j1: p1 j2
        j2: p2 j3
        j3: c1 j4
        j4: c c2

        ciclo_s: k b
        b: r b1
        b1: e b2
        b2: p1 b3
        b3: h b4
        b4: g b5
        b5: h b6
        b6: p2 b7
        b7: c1 b8
        b8: c c2

        condicion_s: i w
        w: r w1 | h w1
        w1: o w2
        w2: r w3 | h w3
        w3: c1 w4
        w4: c w5
        w5: c2 | c2 w6
        w6: t w7
        w7: c1 w8
        w8: c c2

        funcion_s: f d
        d: r d1
        d1: p1 d2
        d2: r d3
        d3: p2 d4
        d4: c1 d5
        d5: c c2

        l: "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
                | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
                | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"

        n: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

        %import common.WS
        %ignore WS
    """


class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"


TOKEN_TYPES = {
    'K': r'\bvos\b', 'I': r'\bira\b', 'C': r'\bcontenido\b', 'V': r'->',
    'M': r'main', 'T': r'tons', 'F': r'act', 'E': r'en', 'G': r',',
    'L': r'[a-zA-Z]', 'N': r'\d', 'C1': r'\{', 'C2': r'\}',
    'P1': r'\(', 'P2': r'\)', 'OEQUALS': r'=', 'OEQUALS_EQUALS': r'==',
    'ONOT_EQUALS': r'!=', 'OLESS_EQUALS': r'<=', 'OGREATER_EQUALS': r'>=', 'OLESS_THAN': r'<',
    'OGREATER_THAN': r'>', 'WHITESPACE': r'\s', 'EOF': r'\$', 'EPSILON': r'\ε',
}


def tokenize(input_string):
    tokens = []
    while input_string:
        match = None
        # Primero intenta coincidir con palabras clave y símbolos
        for token_type, token_regex in TOKEN_TYPES.items():
            if token_type in ['WHITESPACE', 'L', 'N']:
                continue  # Estos se manejan más tarde

            regex_match = re.match(token_regex, input_string)
            if regex_match:
                match = regex_match
                tokens.append(Token(token_type, regex_match.group(0)))
                break

        # Luego intenta coincidir con letras y números
        if not match:
            for token_type in ['WHITESPACE', 'L', 'N']:
                regex_match = re.match(TOKEN_TYPES[token_type], input_string)
                if regex_match:
                    match = regex_match
                    if token_type != 'WHITESPACE':
                        tokens.append(Token(token_type, regex_match.group(0)))
                    break

        if not match:
            raise SyntaxError(f"Token inesperado: {input_string[0]}")

        input_string = input_string[match.end():]

    tokens.append(Token('EOF', '$'))
    return tokens


class SimpleParser:

    def __init__(self, grammar, input_string, terminal):
        self.terminal = terminal
        self.grammar = grammar  # Almacenar la gramática.
        self.tokens = tokenize(input_string)  # Convertir la cadena de entrada en tokens
        self.tokens.append(Token('EOF', '$'))  # Agregar un token de fin de archivo al final
        self.stack = ['$', 'start']  # Inicializar la pila con el símbolo de inicio y fin.
        self.pointer = 0  # Establecer el apuntador a la lista de tokens.

    def parse(self):
        while self.stack[-1] != '$':  # Mientras el tope de la pila no sea el símbolo de fin
            top = self.stack[-1]  # Observamos el símbolo de la cima de la pila
            current_token = self.tokens[self.pointer]


            print(f"Top de la pila: {top}, Token actual: {current_token}, Posición: {self.pointer}")
            cadena = ", ".join(self.stack)
            terminal.insert(tk.END, "[" + cadena + "]" + "\n")
            print(self.stack)

            if top == 'EPSILON':  # Si el top de la pila es EPSILON, simplemente lo removemos.
                self.stack.pop()
                continue
            elif self.is_terminal(top):
                if top == current_token.tipo:  # Comparamos el tipo del token
                    self.stack.pop()  # Extraemos X de la pila
                    self.pointer += 1  # Avanzamos al siguiente token
                    print(self.stack)
                else:
                    self.error("Error de sintaxis")

            else:
                production = self.get_production(top, current_token.tipo)
                if production:
                    self.stack.pop()
                    self.push_production(production)
                else:
                    self.error("Error de producción")

    def peek_next_token(self):
        if self.pointer + 1 < len(self.tokens):
            return self.tokens[self.pointer + 1]
        else:
            return Token('EOF', '$')

    def is_terminal(self, token_type):
        terminals = [
            "K", "I", "C", "V",
            "M", "T", "F", "E", "G",
            "L", "N", "C1", "C2",
            "P1", "P2", "OEQUALS", "OEQUALS_EQUALS",
            "ONOT_EQUALS", "OLESS_EQUALS", "OGREATER_EQUALS", "OLESS_THAN",
            "OGREATER_THAN", "WHITESPACE", "EOF", "EPSILON",
        ]

        return token_type in terminals

    def get_production(self, non_terminal, current_token):
        productions = {
            "start": ["var_s", "main_s", "ciclo_s", "condicion_s", "funcion_s"],

            "p1": ["("],
            "p2": [")"],
            "r": ["l r", "ε"],
            "k": ["vos"],
            "i": ["ira"],
            "h": ["n h", "ε"],

            "c": ["contenido"],
            "c1": ["{"],
            "c2": ["}"],
            "o": ["<", ">", "==", "!=", "<=", ">="],
            "v": ["->"],
            "m": ["main"],
            "t": ["tons"],
            "f": ["act"],
            "e": ["en"],
            "g": [","],

            "var_s": ["r a"],
            "a": ["v h", "v r"],

            "main_s": ["f j"],
            "j": ["m j1"],
            "j1": ["p1 j2"],
            "j2": ["p2 j3"],
            "j3": ["var_ j4", "c1 j4"],
            "j4": ["c c2"],

            "ciclo_s": ["k b"],
            "b": ["l b1"],
            "b1": ["e b2"],
            "b2": ["p1 b3"],
            "b3": ["h b4"],
            "b4": ["g b5"],
            "b5": ["h b6"],
            "b6": ["p2 b7"],
            "b7": ["c1 b8"],
            "b8": ["c c2"],

            "condicion_s": ["i w"],
            "w": ["r w1", "h w1"],
            "w1": ["o w2"],
            "w2": ["r w3", "h w3"],
            "w3": ["c1 w4"],
            "w4": ["c w5"],
            "w5": ["c2", "c2 w6"],
            "w6": ["t w7"],
            "w7": ["c1 w8"],
            "w8": ["c c2"],

            "funcion_s": ["f d"],
            "d": ["r d1"],
            "d1": ["p1 d2"],
            "d2": ["r d3"],
            "d3": ["p2 d4"],
            "d4": ["c1 d5"],
            "d5": ["c c2"],
            "l": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                  "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],

            "n": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        }

        # Producciones para operadores de comparación
        comparison_operators = {
            "EQUALS_EQUALS": "==", "NOT_EQUALS": "!=", "LESS_EQUALS": "<=",
            "GREATER_EQUALS": ">=", "LESS_THAN": "<", "GREATER_THAN": ">"
        }

        if non_terminal == "start":
            if current_token == "L":
                return ["var_s"]
            elif current_token == "K":
                return ["ciclo_s"]
            elif current_token == "F":
                if self.peek_next_token().tipo == "M":
                    return ["main_s"]
                else:
                    return ["funcion_s"]
            elif current_token == "I":
                return ["condicion_s"]

        elif non_terminal == "var_s":
            return ["r", "a"]
        elif non_terminal == "r":
            if current_token in ["V", "P1", "P2", "B1", "E", "OREQUALS", "OREQUALS_EQUALS", "ONOT_EQUALS",
                                 "OLESS_EQUALS", "OGREATER_EQUALS", "OLESS_THAN", "OGREATER_THAN"]:
                return ["EPSILON"]
            else:
                return ["l", "r"]
        elif non_terminal == "l":
            return ["L"]
        elif non_terminal == "a":
            if self.peek_next_token().tipo == "N":
                return ["v", "h"]
            elif self.peek_next_token().tipo == "L":
                return ["v", "r"]
            else:
                return ["EPSILON"]
        elif non_terminal == "v":
            return ["V"]
        elif non_terminal == "h":
            if current_token == "N":
                return ["n", "h"]
            else:
                return ["EPSILON"]
        elif non_terminal == "i":
            return ["I"]
        elif non_terminal == "e":
            return ["E"]
        elif non_terminal == "g":
            return ["G"]
        elif non_terminal == "k":
            return ["K"]
        elif non_terminal == "n":
            return ["N"]
        elif non_terminal == "f":
            return ["F"]
        elif non_terminal == "m":
            return ["M"]
        elif non_terminal == "p1":
            return ["P1"]
        elif non_terminal == "p2":
            return ["P2"]
        elif non_terminal == "c1":
            return ["C1"]
        elif non_terminal == "c2":
            return ["C2"]
        elif non_terminal == "c":
            return ["C"]
        elif non_terminal == "main_s":
            return ["f", "j"]
        elif non_terminal == "j":
            return ["m", "j1"]
        elif non_terminal == "j1":
            return ["p1", "j2"]
        elif non_terminal == "j2":
            return ["p2", "j3"]
        elif non_terminal == "j3":
            return ["c1", "j4"]
        elif non_terminal == "j4":
            if current_token == "L":
                return ["var_s", "c2"]
            else:
                return ["c", "c2"]
        elif non_terminal == "funcion_s":
            return ["f", "d"]
        elif non_terminal == "d":
            return ["r", "d1"]
        elif non_terminal == "d1":
            return ["p1", "d2"]
        elif non_terminal == "d2":
            return ["r", "d3"]
        elif non_terminal == "d3":
            return ["p2", "d4"]
        elif non_terminal == "d4":
            return ["c1", "d5"]
        elif non_terminal == "d5":
            if current_token == "L":
                return ["var_s", "c2"]
            else:
                return ["c", "c2"]
        elif non_terminal == "ciclo_s":
            return ["k", "b"]
        elif non_terminal == "b":
            return ["r", "b1"]
        elif non_terminal == "b1":
            return ["e", "b2"]
        elif non_terminal == "b2":
            return ["p1", "b3"]
        elif non_terminal == "b3":
            return ["h", "b4"]
        elif non_terminal == "b4":
            return ["g", "b5"]
        elif non_terminal == "b5":
            return ["h", "b6"]
        elif non_terminal == "b6":
            return ["p2", "b7"]
        elif non_terminal == "b7":
            return ["c1", "b8"]
        elif non_terminal == "b8":
            if current_token == "L":
                return ["var_s", "c2"]
            else:
                return ["c", "c2"]
        elif non_terminal == "condicion_s":
            return ["i", "w"]
        elif non_terminal == "w":
            if current_token == "L":
                return ["r", "w1"]
            else:
                return ["h", "w1"]
        elif non_terminal == "w1":
            return ["o", "w2"]
        elif non_terminal == "o":
            if current_token == "OEQUALS":
                return ["OEQUALS"]
            elif current_token == "OEQUALS_EQUALS":
                return ["OEQUALS_EQUALS"]
            elif current_token == "ONOT_EQUALS":
                return ["ONOT_EQUALS"]
            elif current_token == "OLESS_EQUALS":
                return ["OLESS_EQUALS"]
            elif current_token == "OGREATER_EQUALS":
                return ["OGREATER_EQUALS"]
            elif current_token == "OLESS_THAN":
                return ["OLESS_THAN"]
            elif current_token == "OGREATER_THAN":
                return ["OGREATER_THAN"]
        elif non_terminal == "w2":
            if current_token == "L":
                return ["r", "w3"]
            else:
                return ["h", "w3"]
        elif non_terminal == "w3":
            return ["c1", "w4"]
        elif non_terminal == "w4":
            if current_token == "L":
                return ["var_s", "w5"]
            else:
                return ["c", "w5"]
        elif non_terminal == "w5":
            if self.peek_next_token().tipo == "T":
                return ["c2", "w6"]
            else:
                return ["c2"]
        elif non_terminal == "w6":
            return ["t", "w7"]
        elif non_terminal == "w7":
            return ["c1", "w8"]
        elif non_terminal == "w8":
            if current_token == "L":
                return ["var_s", "c2"]
            else:
                return ["c", "c2"]
        elif non_terminal == "t":
            return ["T"]
        elif non_terminal in productions:
            production_rule = productions[non_terminal]
            expanded_production = []

            for element in production_rule:
                if element == "comparison_operator" and current_token in comparison_operators:
                    expanded_production.append(current_token)
                elif element.endswith("*"):
                    # Maneja la repetición. Esto es simplificado; la lógica real dependerá de tu implementación.
                    element_base = element.rstrip('*')
                    expanded_production.extend(
                        [element_base, element])  # Repite el elemento y sí mismo para posibles repeticiones adicionales
                else:
                    expanded_production.append(element)

            return expanded_production
        else:

            return None

    def push_production(self, production):
        # La producción es una lista de símbolos (tipos de tokens o no terminales) a ser añadidos a la pila.
        for symbol in reversed(production):
            self.stack.append(symbol)

    def error(self, message):
        if self.pointer < len(self.tokens):
            current_token = self.tokens[self.pointer]
            raise SyntaxError(
                f"{message} en la posición {self.pointer} (Token: {current_token.tipo}, Valor: '{current_token.valor}')")
        else:
            raise SyntaxError(f"{message} al final de la entrada")

root = tk.Tk()
root.config(bg='#1e1e1e')
root.title("Mi Editor de Código")
root.geometry("800x600")
frame = tk.Frame(root, bg='#1e1e1e')
frame.pack(fill=tk.BOTH, expand=True)

editor = tk.Text(frame, bg='#1e1e1e', fg='#d4d4d4', insertbackground='white')
editor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
editor.config(height=10, font=("Arial", 15))

terminal = tk.Text(frame, bg='#0c0c0c', fg='#d4d4d4')
terminal.pack(side=tk.BOTTOM, fill=tk.X)
terminal.config(height=10)

texto = tk.StringVar()

def validar():
    texto.set(editor.get("1.0", tk.END))
    parser = SimpleParser(grammar, texto.get(), terminal)
    terminal.delete("1.0", tk.END)
    try:
        parser.parse()
        messagebox.showinfo("🎈", "Ta bien tu gramatica pichi 10/10")
        print("Análisis sintáctico completado con éxito.")
    except SyntaxError as e:
        messagebox.showerror("🤣", "Checale, checale tu puedes")
        print(f"Error en el análisis: {e}")


boton_validar = tk.Button(root, text="Validar", command=validar, bg='#007acc', fg='white', height=2, width=200)
boton_validar.pack(side=tk.BOTTOM)

root.mainloop()
