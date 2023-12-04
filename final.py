from flask import Flask, render_template, request
from lark import Lark
import re

app = Flask(__name__)
pila=[]

@app.route('/')
def pagina():
    return render_template('formulario.html', bandera='')

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
#L, N, P1, P2, K, I, C, C1, C2, O, V, M, T, F, E, G, 

def tokenize(input_string):
    tokens = []
    while input_string:
        match = None
        for token_type, token_regex in TOKEN_TYPES.items():
            if token_type in ['WHITESPACE', 'L', 'N']:
                continue

            regex_match = re.match(token_regex, input_string)
            if regex_match:
                match = regex_match
                tokens.append(Token(token_type, regex_match.group(0)))
                break

        if not match:
            for token_type in ['L', 'N', 'WHITESPACE']:
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
   
    def __init__(self, grammar, input_string):
        self.grammar = grammar
        self.tokens = tokenize(input_string)
        self.tokens.append(Token('EOF', '$'))
        self.stack = ['$', 'start']
        self.pointer = 0

    def parse(self):
        while self.stack[-1] != '$':
            top = self.stack[-1]
            current_token = self.tokens[self.pointer]

            print(f"Top de la pila: {top}, Token actual: {current_token}, Posición: {self.pointer}")
            print("~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.")
            print(self.stack)
            pila.append(self.stack.copy())
            print("~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.")

            if self.is_terminal(top):
                if top == current_token.tipo:
                    self.stack.pop()
                    self.pointer += 1
                    pila.append(self.stack.copy())
                else:
                    self.error("Error de sintaxis")
            elif top == 'EPSILON':
                self.stack.pop()
                pila.append(self.stack.copy())
                continue
            else:
                production = self.get_production(top, current_token.tipo)
                if production:
                    self.stack.pop()
                    self.push_production(production)
                    pila.append(self.stack.copy())
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
            if non_terminal == "start":
                next_token = self.peek_next_token()

                if current_token == "L":
                    return ["r", "a"]
                elif current_token == "K":
                    return ["k", "b"]
                elif current_token == "I":
                    return ["i", "w"]
                else:
                    if next_token.tipo == "M":
                        return ["f", "j"]
                    else:
                        return ["f", "d"]
            
            elif current_token == "L":
                return ["L"]

            elif non_terminal == "p2":
                return ["P2"]

            elif non_terminal == "r":
                return ["l", "r"]
            
            elif non_terminal == "k":
                return ["K"]

            elif non_terminal == "i":
                return ["I"]

            elif non_terminal == "h":
                return ["n", "h"]

            elif non_terminal == "c":
                return ["C"]

            elif non_terminal == "c1":
                return ["C1"]

            elif non_terminal == "c2":
                return ["C2"]

            elif non_terminal == "<":
                return ["OLESS_THAN"]

            elif non_terminal == ">":
                return ["OGREATER_THAN"]

            elif non_terminal == "==":
                return ["OEQUALS_EQUALS"]
            
            elif non_terminal == "!=":
                return ["ONOT_EQUALS"]
            
            elif non_terminal == "<=":
                return ["OLESS_EQUALS"]
            
            elif non_terminal == ">=":
                return ["OGREATER_EQUALS"]
            
            elif non_terminal == "v":
                return ["V"]

            elif non_terminal == "m":
                return ["M"]
            
            elif non_terminal == "t":
                return ["T"]

            elif non_terminal == "f":
                return ["F"]

            elif non_terminal == "e":
                return ["E"]

            elif non_terminal == "g":
                return ["G"]

            elif non_terminal == "f":
                return ["F"]
            
            elif non_terminal == "j":
                return ["m", "j1"]
            
            elif non_terminal == "j1":
                return ["p1", "j2"]

            elif non_terminal == "j2":
                return ["p2", "j3"]
            
            elif non_terminal == "j3":
                return ["c1", "j4"]
            
            elif non_terminal == "j4":
                return ["c", "c2"]

            elif non_terminal == "(":
                return ["P1"]

            elif non_terminal == ")":
                return ["P2"]

            elif current_token == "P1":
                return ["P1"]

            elif current_token == "P2":
                return ["P2"]

            elif non_terminal == "k":
                return ["K"]

            elif non_terminal == "b":
                return ["l", "b1"]
            
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
                return ["c", "c2"]
            
            elif non_terminal == "i":
                return ["I"]
            
            elif non_terminal == "w":
                if current_token == "L":
                    return ["r w1"]
                if current_token == "N":
                    return ["h w1"]
            
            elif non_terminal == "w1":
                return ["o", "w2"]

            elif non_terminal == "w2":
                if current_token == "L":
                    return ["r w3"]
                if current_token == "N":
                    return ["h w3"]
            
            elif non_terminal == "w3":
                return ["c1", "w4"]
            
            elif non_terminal == "w4":
                return ["c", "w5"]
            
            elif non_terminal == "w5":
                next_token = self.peek_next_token()

                if next_token == "T":
                    return ["c2", "w6"]
                else:
                    return ["c2"]
            
            elif non_terminal == "w6":
                return ["t", "w7"]

            elif non_terminal == "w7":
                return ["c1", "w8"]

            elif non_terminal == "w8":
                return ["c", "c2"]
            
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
                return ["c", "c2"]
            
            

    def push_production(self, production):
        for symbol in reversed(production):
                self.stack.append(symbol)

    def error(self, message):
        if self.pointer < len(self.tokens):
            current_token = self.tokens[self.pointer]
            raise SyntaxError(f"{message} en la posición {self.pointer} (Token: {current_token.tipo}, Valor: '{current_token.valor}')")
        else:
            raise SyntaxError(f"{message} al final de la entrada")

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    texto = request.form.get('texto')
    
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
        b: l b1
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

    try:
        parser = SimpleParser(grammar, texto)
    except SyntaxError as e:
        print(f"Error en el análisis: {e}")

    try:
        parser.parse()
        print("Análisis sintáctico completado con éxito.")
    except SyntaxError as e:
        print(f"Error en el análisis: {e}")

    parser = Lark(grammar, start='start')

    try:
        tree = parser.parse(texto)
        print(tree.pretty())
        print("tu codigo si funcia")
        bandera = True
    except Exception as e:
        print(f"tu codigo no funcia: {e}")
        bandera = False
        print(bandera)
    return render_template('formulario.html', bandera=bandera, texto=texto, pila=pila)

if __name__ == '__main__':
    app.run(debug=True)
