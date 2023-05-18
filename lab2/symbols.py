def eliminationUselessSymbs(grammar):
		new_nterms = set(grammar['start'])

		for symbol, rule in grammar['rules'].items():
				if symbol not in new_nterms:
						continue
				for p in rule:
						for i in range(len(p)):
								if p[i] in grammar['term']:
										continue
								new_nterms.add(p[i])

		rules = {}
		for symbol, rule in grammar['rules'].items():
				if symbol in new_nterms:
						rules[symbol] = rule

		grammar['rules'] = rules
		return grammar
