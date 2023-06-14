from lexer import Lexer
from ast_builder import AstTreeBuilder

def validate_expression (expression):
        lexer = Lexer()
        lexer.lex(expression)

        ast = AstTreeBuilder()
        ast.build(lexer)

def main():
        try:
                with open('code.sps', 'r') as f:
                        expression = f.read()
                        validate_expression(expression)
                print(expression)
                print("Выражение валидно")
        except SyntaxError as e:
                print(f"Ошибка в синтаксисе {expression}")


if __name__ == '__main__':
        main()
