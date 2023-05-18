# Алгоритм 2.13 из книги АХО А., УЛЬМАН Дж. Теория синтаксического анализа, перевода и компиляции: В 2-х томах. Т.1.: Синтаксический анализ. - М.: Мир, 1978.
from itertools import combinations


def eliminationImmediateRecursion(grammatic):
		new_rules = grammatic['rules'].copy()
		new_nonterminal = set(grammatic['nterm'])

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
						new_nonterminal.add(new_symbol)
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
		grammatic['nterm'] = list(new_nonterminal)
		return grammatic

# Алгоритм 4.8 из книги АХО А.В, ЛАМ М.С., СЕТИ Р., УЛЬМАН Дж.Д. Компиляторы: принципы, технологии и инструменты. – М.: Вильямс, 2008
def elimination_of_recursion_immediate_2(rules):
		# print('rules = ', rules)
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

				# print('alpha = ', alpha, 'beta = ', beta)
				if len(beta) == 0:
						beta.append([])
				# print('alpha =', alpha)
				# print('beta =', beta)
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
		new_nonterminal_arr = grammatic['nterm'].copy()
		# print(nonterminal)
		for i in range(len(nonterminal)):
				Ai = nonterminal[i]
				for j in range(i):
						ai_production_array = rules[Ai]
						Aj = nonterminal[j]
						aj_production_array = rules[Aj]

						new_production_array = []

						for k in range(len(ai_production_array)):
								new_production = []
								if ai_production_array[k][0] == Aj:
										for aj_production in aj_production_array:
												if aj_production[-1] == 'eps':
														aj_production = aj_production[:-1]
												new_production_array.append(aj_production + ai_production_array[k][1:])
								else:
										new_production.extend(ai_production_array[k])

								if len(new_production) > 0:
										new_production_array.append(new_production)
						rules[Ai] = new_production_array
				# print('AAA')
				new_rules, new_nonterminal = elimination_of_recursion_immediate_2({Ai: rules[Ai]})
				new_nonterminal_arr += list(new_nonterminal)
				for a in new_rules:
						rules[a] = new_rules[a]

		grammatic['rules'] = rules
		grammatic['nterm'] = new_nonterminal_arr
		return grammatic


# Алгоритм 2.8 АХО А., УЛЬМАН Дж. Теория синтаксического анализа, перевода и компиляции: В 2-х томах. Т.1.: Синтаксический анализ. - М.: Мир, 1978.
def remove_unattainable_symbols(grammatic):
		nonterminal = set(grammatic['nterm'])
		V_pred = set()
		V_next = set([grammatic['start']])
		while V_next != V_pred:
				V_pred, V_next = V_next, V_pred
				for symbol, production in grammatic['rules'].items():
						if symbol in V_pred:
								for p in production:
										for i in range(len(p)):
												if p[i] in nonterminal:
														V_next.add(p[i])
				V_next |= V_pred

		new_grammatic = {}
		new_grammatic['nterm'] = list(nonterminal.intersection(V_next))
		new_grammatic['start'] = grammatic['start']
		terminal = set()
		rules = {}
		for symbol, production in grammatic['rules'].items():
				if symbol in V_next:
						rules[symbol] = production
						for p in production:
								for i in range(len(p)):
										if p[i] not in nonterminal and p[i] != 'eps':
												terminal.add(p[i])


		new_grammatic['term'] = list(terminal)
		new_grammatic['rules'] = rules
		return new_grammatic


def getLongestPrefix(rules):
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

						betaArr, gammaArr = [], []
						for p in rule:
								if prefix == p[:len(prefix)]:
										beta = p[len(prefix):]
										if len(beta) > 0:
												betaArr.append(beta)
										else:
												epsilon[newSymbol] = True
								else:
										gammaArr.append(p)

						grammar['nterm'].append(newSymbol)

						rules[symbol] = [prefix + [newSymbol]] + gammaArr
						rules[newSymbol] = betaArr

						production = rules[symbol]
						prefix = getLongestPrefix(production)

		for symbol in rules:
				grammar['rules'][symbol] = rules[symbol]
				if symbol in epsilon and epsilon[symbol]:
						grammar['rules'][symbol].append(['eps'])

		return grammar

def get_subsets(symbols):
    """
    Возвращает все подмножества множества symbols.
    """
    subsets = [[]]
    for symbol in symbols:
        subsets += [subset + [symbol] for subset in subsets]
    return subsets

def eliminationEpsilonRules(tx):
		grammar = [
				("S", ["A", "B", "C", "d"]),
				("A", ["a"]),
				("A", ["epsilon"]),
				("B", ["A", "C"]),
				("C", ["c"]),
				("C", ["epsilon"]),
		]

		nullable = set()
		for head, body in grammar:
				if not body:
						nullable.add(head)

		# Пока мы можем найти нетерминалы, которые могут выводить эпсилон, заменяем эпсилон-правила
		while True:
				new_nullable = set(nullable)
				for head, body in grammar:
						if all(symbol in nullable for symbol in body):
								new_nullable.add(head)
				if new_nullable == nullable:
						break
				nullable = new_nullable

		# Создаем новую грамматику без эпсилон-правил
		new_grammar = []
		for head, body in grammar:
				for subset in get_subsets(body):
						if all(symbol in nullable or symbol == "" for symbol in subset):
								new_body = [symbol for symbol in body if symbol not in subset]
								if not new_body:
										new_body = [""]  # заменяем пустое тело на символ эпсилон
								new_grammar.append((head, new_body))

		print(new_grammar)
		return new_grammar

def cnf_grammer(G):
    # step 1
    S = G.start()
    P = G.productions()
    N = set(G.nonterminals())
    T = set(G.terminals())
    new_S = S.symbol() + "'"
    while new_S in N:
        new_S += "'"
    P.append(new_S + " -> " + S.symbol())
    N.add(new_S)

    # step 2
    for p in P:
        if len(p.rhs()) > 1:
            rhs = p.rhs()
            new_rhs = []
            for s in rhs:
                if s in T:
                    new_rhs.append(s)
                else:
                    new_s = s.symbol() + "_"
                    while new_s in N:
                        new_s += "_"
                    N.add(new_s)
                    new_rhs.append(new_s)
                    P.append(new_s + " -> " + s.symbol())
            P.remove(p)
            new_p = p.lhs().symbol() + " -> " + "".join(new_rhs)
            P.append(new_p)

    # step 3
    for p in P:
        if len(p.rhs()) > 2:
            rhs = p.rhs()
            new_rhs = [rhs[0]]
            for s in rhs[1:]:
                new_s = s.symbol() + "_"
                while new_s in N:
                    new_s += "_"
                N.add(new_s)
                P.append(new_s + " -> " + s.symbol())
                new_rhs.append(new_s)
            P.remove(p)
            new_p = p.lhs().symbol() + " -> " + new_rhs[0].symbol() + " " + new_rhs[1].symbol()
            for s in new_rhs[2:]:
                new_p += " " + s.symbol()
            P.append(new_p)

    # return new grammar
    new_G = CFG(S, T, P, new_S)
    return new_G
