from ast_builder import AstTreeBuilder
from parser import parse

def validate_expression(expression):
        parsed_expression = parse(expression)

        ast = AstTreeBuilder()
        ast.build(parsed_expression)

def main():
        try:
                with open('grammarTest.txt', 'r') as f:
                        expression = f.read()
                        validate_expression(expression)
                print(expression)
                print("Выражение валидно")
        except SyntaxError as e:
                print(f"Ошибка в синтаксисе {expression}")


if __name__ == '__main__':
        main()
