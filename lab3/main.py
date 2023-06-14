from ast_builder import AstTreeBuilder
from tokenizer import tokenize

def validate_expression(expression):
        tokenized_expression = tokenize(expression)

        ast = AstTreeBuilder()
        ast.build(tokenized_expression)

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
