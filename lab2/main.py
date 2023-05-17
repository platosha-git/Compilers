from parser import parse
from handlers import  outputGrammar
from interface import eliminationLeftRecursion

def main():
		filenameGrammar = 'gr_lf.txt'
		inGrammar = parse(filenameGrammar)

		outputGrammar('Grammar', inGrammar)

		#1. Устранение левой рекурсии
		outGrammar = eliminationLeftRecursion(inGrammar)
		outputGrammar('Left recursion', outGrammar)

		# grammatic = elimination_of_recursion_immediate_1(grammar)
		# grammatic = elimination_of_recursion_indirect(grammar)
		# grammatic = remove_unattainable_symbols(grammar)

if __name__ == "__main__":
		main()
