def inputGrammar(filename):
		term, nterm = [], []
		start = None
		rules = {}

		with open(filename, 'r') as file:
				nterm = file.readline().strip(' ').strip('\n').split(' ')
				term = file.readline().strip(' ').strip('\n').split(' ')
				start = file.readline().strip(' ').strip('\n')

				for line in file:
						inRules = line.strip(' ').strip('\n').split('|')
						rule = inRules[0].strip(' ').strip('\n').split(' ')
						lSymb = rule[0]

						if lSymb not in rules:
								rules[lSymb] = [rule[2:]]
						else:
								rules[lSymb].append(rule[2:])

						for rRules in inRules[1:]:
								rule = rRules.strip(' ').strip('\n').split(' ')
								rules[lSymb].append(rule)

		grammar = {
				'nterm': nterm,
				'term': term,
				'start': start,
				'rules': rules
		}

		return grammar


def outputGrammar(msg, grammar):
		print(msg)
		print('---------------')

		print('non terminal:', end=' ')
		print(grammar['nterm'])

		print('terminal:', end=' ')
		print(grammar['term'])

		print('start symbol:', end=' ')
		print(grammar['start'])
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
