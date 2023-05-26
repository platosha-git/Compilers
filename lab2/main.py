from handlers import  inputGrammar, outputGrammar
from recursion import eliminationLeftRecursion
from recursion import eliminationIndirectRecursion
from symbols import eliminationUselessSymbs

def main():
		# 1. Устранение левой рекурсии
		inLGr = inputGrammar('examples/left3.txt')
		outputGrammar('Grammar', inLGr)

		outLGr = eliminationLeftRecursion(inLGr)
		outputGrammar('Left recursion', outLGr)

		# 2. Устранение косвенной рекурсии
		inIGr = inputGrammar('examples/indirect.txt')
		outputGrammar('Grammar', inIGr)

		outIGr = eliminationIndirectRecursion(inIGr)
		outputGrammar('Indirect recursion', outIGr)

		# 3. Удаление бесполезных символов
		inUGr = inputGrammar('examples/useless.txt')
		outputGrammar('Grammar', inUGr)

		outUGr = eliminationUselessSymbs(inUGr)
		outputGrammar('Useless symbols', outUGr)


if __name__ == "__main__":
		main()
