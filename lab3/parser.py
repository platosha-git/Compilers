from exception import CompileError

def parse(tokenized_expression):
        Parser(tokenized_expression)

class Node():
        def __init__(self, operations = None, nodes = None, is_leaf = False, node_name = 'NO_NAME'):
                self.operations = operations
                self.nodes = nodes
                self.is_leaf = is_leaf
                self.node_name = node_name
    
class Parser():
        def __init__(self, tokenized_expression):
                self.tokenized_expression = tokenized_expression
                self.root = Node()
                self.operations_after_expression = {'OP_blockopenbrackets', 'OP_blockclosebrackets', 'OP_sep'}
                self.count = {'f': 0, 'i': 0, 't': 0, 'ae': 0,
                                      'e': 0, 'o': 0, 'olt': 0,
                                      'ol': 0, 'b': 0, 'p': 0}
                self.parse()

        def _get_name(self, name, op, val = None):
            new_name = name + str(self.count[name])
            self.count[name] += 1
            if op is not None:
                new_name += ' op: ' + op['value']
            if val is not None and type(val) != Node:
                new_name += 'v:' + val['value']
            return new_name

        def factor(self):
            lex = self.tokenized_expression.next()
            if lex is not None and lex['type'] == 'OP_closebrackets':
                raise CompileError()
            item = lex
            is_leaf = True
            if lex is not None and lex['type'] == 'OP_openbrackets':
                is_leaf = False
                item = self.arithmetic_expression()
                lex = self.tokenized_expression.next()
                # print('s', self.tokenized_expression.num)
                if lex is None or lex['type'] != 'OP_closebrackets':
                    raise CompileError()
            res = None
            if item is not None:
                res = Node(None, [item, None], is_leaf = is_leaf,
                           node_name = self._get_name('f', None, item))
            return res

        def term(self):
            item1 = self.factor()
            if item1 is None:
                raise CompileError()
            item2 = None
            op = None
            lex = self.tokenized_expression.next()
            if lex is not None:
                while lex is not None and lex['type'] == 'OP_mullike':
                    if item2 is not None:
                        item1 = Node(op, [item1, item2],
                                    node_name = self._get_name('t', op))
                    op = lex
                    item2 = self.factor()
                    if item2 is None:
                        raise CompileError()

                    lex = self.tokenized_expression.next()
                else:
                    self.tokenized_expression.prev()

            res = Node(op, [item1, item2],
                        node_name = self._get_name('t', op))
            return res


        def arithmetic_expression(self):
            item1 = self.term()
            if item1 is None:
                raise CompileError()
            item2 = None
            op = None
            lex = self.tokenized_expression.next()
            if lex is not None:
                while lex is not None and lex['type'] == 'OP_addlike':
                    if item2 is not None:
                        item1 = Node(op, [item1, item2], node_name = self._get_name('ae', op))
                    op = lex
                    item2 = self.term()
                    if item2 is None:
                        raise CompileError()

                    lex = self.tokenized_expression.next()
                else:
                    self.tokenized_expression.prev()
            return Node(op, [item1, item2], node_name = self._get_name('ae', op))

        def expression(self, ):
            item1 = self.arithmetic_expression()
            item2 = None
            if item1 is None:
                raise CompileError()
            op = None
            # print(self.tokenized_expression.num)
            # print(len(self.tokenized_expression.tokens))
            lex = self.tokenized_expression.next()
            if lex is not None:
                if lex['type'] == 'OP_comparelike':
                    op = lex
                    item2 = self.arithmetic_expression()
                    if item2 is None:
                        raise CompileError()
                elif lex['type'] not in self.operations_after_expression:
                    # print(lex)
                    raise CompileError()
                else:
                    self.tokenized_expression.prev()

            return Node(op, [item1, item2], node_name = self._get_name('e', op))


        def operator(self):
            lex = self.tokenized_expression.next()
            if lex is None or lex['type'] != 'NAME':
                raise CompileError()
            item1 = Node(None, [lex, None], is_leaf = True, node_name = self._get_name('i', None, lex))
            lex = self.tokenized_expression.next()
            if lex is None or lex['type'] != 'OP_assignment':
                raise CompileError()

            op = lex
            item2 = self.expression()

            if item2 is None:
                raise CompileError()

            return Node(op, [item1, item2], node_name = self._get_name('o', op))

        def operator_list_tail(self):
            items = []
            lex = self.tokenized_expression.next()
            if lex is None or lex['type'] != 'OP_sep':
                self.tokenized_expression.prev()
                return None
            item = self.operator()
            if item is None:
                raise CompileError()



            items = [item]
            item = self.operator_list_tail()
            if item is not None:
                items += item.nodes

            return Node(None, items, node_name = self._get_name('olt', None))

        def operator_list(self):
            item = self.operator()
            items = [item]
            item = self.operator_list_tail()
            if item is not None:
                items += item.nodes
            return Node(None, items, node_name = self._get_name('ol', None))

        def block(self):
            lex = self.tokenized_expression.next()
            if lex is None or lex['type'] != 'OP_blockopenbrackets':
                raise CompileError()
            item = self.operator_list()
            lex = self.tokenized_expression.next()

            if lex is None or lex['type'] != 'OP_blockclosebrackets':
                raise CompileError()

            return Node(None, [item, None], node_name = self._get_name('b', None))

        def parse(self):
                self.programm()
                if self.tokenized_expression.num < len(self.tokenized_expression.tokens):
                    raise CompileError()

        def programm(self):
            item = self.block()
            self.root.operations = None
            self.root.nodes = [item, None]
            self.root.node_name = self._get_name('p', None)
