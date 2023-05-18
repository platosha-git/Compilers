def eliminationUselessSymbs(grammar):
		# 1 - определение нетерминалов, которые могут порождать цепочки
		useful = set()
		newUseful = set([grammar['start']])
		terms = set(grammar['term'])

		while newUseful != useful:
				useful, newUseful = newUseful, useful
				for symbol, production in grammar['rules'].items():
						if symbol in useful:
								for p in production:
										for i in range(len(p)):
												if p[i] in terms:
														newUseful.add(p[i])
				newUseful |= useful

		for symbol, rule in grammar['rules'].items():
				if symbol not in useful:
						continue
				for p in rule:
						for i in range(len(p)):
								if p[i] in grammar['term']:
										continue
								useful.add(p[i])

		# 2 - устранение недостижимых символов
		newGrammar = {}
		rules = {}
		for symbol, rule in grammar['rules'].items():
				if symbol in useful:
						rules[symbol] = rule

		newGrammar['rules'] = rules
		return newGrammar
