from handlers import  inputGrammar, outputGrammar
from recursion import eliminationLeftRecursion
from recursion import eliminationImmediateRecursion
from recursion import eliminationIndirectRecursion
from symbols import eliminationUselessSymbs

def main():
		# 1. Устранение левой рекурсии
		inLGr = inputGrammar('left.txt')
		outputGrammar('Grammar', inLGr)

		outLGr = eliminationLeftRecursion(inLGr)
		outputGrammar('Left recursion', outLGr)

		# 2. Устранение непосредственной рекурсии
		inImGr = inputGrammar('immediate.txt')
		outputGrammar('Grammar', inImGr)

		outImGr = eliminationImmediateRecursion(inImGr)
		outputGrammar('Immediate recursion', outImGr)

		# 3. Устранение косвенной рекурсии
		inIGr = inputGrammar('indirect.txt')
		outputGrammar('Grammar', inIGr)

		outIGr = eliminationIndirectRecursion(inIGr)
		outputGrammar('Indirect recursion', inIGr)

		# 4. Удаление бесполезных символов
		inUGr = inputGrammar('useless.txt')
		outputGrammar('Grammar', inUGr)

		outUGr = eliminationUselessSymbs(inUGr)
		outputGrammar('Useless symbols', outUGr)

		# grammatic = elimination_of_recursion_immediate_1(grammar)
		# grammatic = elimination_of_recursion_indirect(grammar)
		# grammatic = remove_unattainable_symbols(grammar)

if __name__ == "__main__":
		main()
