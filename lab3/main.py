from exception import CompileError
from parser import parse
from tokenizer import tokenize

def validate_expression(expression):
        tokenized_expression = tokenize(expression)
        parse(tokenized_expression)

def main():
        try:
                with open('grammar.txt', 'r') as f:
                        expression = f.read()
                        validate_expression(expression)
                print(expression)
                print("Выражение валидно")
        except CompileError:
                print(expression)
                print("Выражение невалидно")


if __name__ == '__main__':
        main()
