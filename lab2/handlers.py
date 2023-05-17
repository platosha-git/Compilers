def outputGrammar(msg, grammar):
		print(msg)
		print('---------------')

		print('non terminal:', end=' ')
		print(grammar['nonterminal'])

		print('terminal:', end=' ')
		print(grammar['terminal'])

		print('start symbol:', end=' ')
		print(grammar['startsymbol'])
		print()

		for symbol, production in grammar['rules'].items():
				print(symbol, '->', end=' ')
				for i in range(len(production)):
						for pi in production[i]:
								print(pi, end=' ')
						if i < len(production) - 1:
								print('|', end=' ')
				print()

		print('\n')