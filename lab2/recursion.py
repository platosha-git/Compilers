def getLongestPrefix(rules):
		# 1 - Расположить нетерминалы в порядке
		production_string_array = []
		for p in rules:
				s = ''
				for i in range(len(p)):
						s += p[i] + '|'
				production_string_array.append(s)
		production_string_array.sort()

		max_prefix = ''
		for i in range(len(production_string_array) - 1):
				p1 = production_string_array[i]
				p2 = production_string_array[i + 1]
				prefix = ''

				for j in range(min(len(p1), len(p2))):
						if p1[j] == p2[j]:
								prefix += p1[j]
						else:
								if len(prefix) > len(max_prefix):
										max_prefix = prefix
								prefix = ''
								break
				if len(prefix) > len(max_prefix):
						max_prefix = prefix

		max_prefix_arr = max_prefix.split('|')[:-1]

		return max_prefix_arr


def eliminationLeftRecursion(grammar):
		rules, epsilon = {}, {}

		for symbol, rule in grammar['rules'].items():
				epsilon[symbol] = False

				prefix = getLongestPrefix(rule)
				if len(prefix) == 0:
						continue

				newSymbol = symbol
				while len(prefix) > 0:
						newSymbol += '1'

						alphaArr, bettaArr = [], []
						for p in rule:
								if prefix == p[:len(prefix)]:
										alpha = p[len(prefix):]
										if len(alpha) > 0:
												alphaArr.append(alpha)
										else:
												epsilon[newSymbol] = True
								else:
										bettaArr.append(p)

						grammar['nterm'].append(newSymbol)

						rules[symbol] = [prefix + [newSymbol]] + bettaArr
						rules[newSymbol] = alphaArr

						production = rules[symbol]
						prefix = getLongestPrefix(production)

		for symbol in rules:
				grammar['rules'][symbol] = rules[symbol]
				if symbol in epsilon and epsilon[symbol]:
						grammar['rules'][symbol].append(['eps'])

		return grammar

def eliminationImmediateRecursion(grammatic):
		new_rules = grammatic['rules'].copy()
		new_nonterm = set(grammatic['nterm'])

		for left, right in grammatic['rules'].items():
				add_index = 1
				alpha = []
				beta = []
				for i in range(len(right)):
						if right[i][0] == left and len(right[i]) > 1:
								alpha.append(right[i][1:])
						else:
								beta.append(right[i])

				if len(alpha) > 0:
						new_symbol = left + str(add_index)
						new_nonterm.add(new_symbol)
						new_rules[left] = []
						new_rules[new_symbol] = []
						if len(beta) == 0:
								new_rules[left] = [[new_symbol]]

						for i in range(len(beta)):
								if beta[i][-1] == 'eps':
										new_rules[left].append([new_symbol])
										new_rules[left].append(beta[i])
								else:
										new_rules[left].append(beta[i])
										new_rules[left].append(beta[i] + [new_symbol])
						for i in range(len(alpha)):
								new_rules[new_symbol].append(alpha[i])
								new_rules[new_symbol].append(alpha[i] + [new_symbol])

		grammatic['rules'] = new_rules
		grammatic['nterm'] = list(new_nonterm)
		return grammatic


# Алгоритм 4.8 из книги АХО А.В, ЛАМ М.С., СЕТИ Р., УЛЬМАН Дж.Д. Компиляторы: принципы, технологии и инструменты. – М.: Вильямс, 2008
def elimination_of_recursion_immediate_2(rules):
		new_rules = rules.copy()
		new_nonterminal = set()
		epsilon = 'eps'

		for left, right in rules.items():
				add_index = 1
				alpha = []
				beta = []
				for i in range(len(right)):
						if right[i][0] == left and len(right[i]) >= 1:
								alpha.append(right[i][1:])
						else:
								beta.append(right[i])

				if len(beta) == 0:
						beta.append([])
				if len(alpha) > 0:
						new_symbol = left + str(add_index)
						new_nonterminal.add(new_symbol)
						new_rules[left] = []
						new_rules[new_symbol] = []

						for i in range(len(beta)):
								symbol = beta[i]
								if beta[i] == [epsilon]:
										symbol = []
								new_rules[left].append(symbol + [new_symbol])
						for i in range(len(alpha)):
								new_rules[new_symbol].append(alpha[i] + [new_symbol])

						new_rules[new_symbol].append([epsilon])

		return new_rules, new_nonterminal


def eliminationIndirectRecursion(grammatic):
		rules = grammatic['rules']
		nonterminal = list(rules.keys())
		newNonterminal = grammatic['nterm'].copy()

		for i in range(len(nonterminal)):
				Ai = nonterminal[i]
				for j in range(i):
						Aj = nonterminal[j]
						aiArray = rules[Ai]
						ajArray = rules[Aj]

						new_production_array = []
						for k in range(len(aiArray)):
								new_production = []
								if aiArray[k][0] == Aj:
										for aj_production in ajArray:
												if aj_production[-1] == 'eps':
														aj_production = aj_production[:-1]
												new_production_array.append(aj_production + aiArray[k][1:])
								else:
										new_production.extend(aiArray[k])

								if len(new_production) > 0:
										new_production_array.append(new_production)
						rules[Ai] = new_production_array

				new_rules, new_nonterminal = elimination_of_recursion_immediate_2({Ai: rules[Ai]})
				newNonterminal += list(new_nonterminal)
				for a in new_rules:
						rules[a] = new_rules[a]

		grammatic['rules'] = rules
		grammatic['nterm'] = newNonterminal
		return grammatic


