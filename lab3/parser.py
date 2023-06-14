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

        def token_check(self, token, expected_type):
                if token is None or token['type'] != expected_type:
                        raise CompileError()

        def parse(self):
                item = self.block()
                self.root.operations = None
                self.root.nodes = [item, None]
                self.root.node_name = self._get_name('p', None)

                if self.tokenized_expression.num < len(self.tokenized_expression.tokens):
                        raise CompileError()

        def block(self):
                token = self.tokenized_expression.next()
                self.token_check(token, 'OP_blockopenbrackets')

                item = self.operator_list()

                token = self.tokenized_expression.next()
                print(token['type'])
                self.token_check(token, 'OP_blockclosebrackets')

                return Node(None, [item, None], node_name = self._get_name('b', None))

        def operator_list(self):
                item = self.operator()
                items = [item]
                item = self.operator_list_tail()
                if item is not None:
                        items += item.nodes
                return Node(None, items, node_name = self._get_name('ol', None))

        def operator_list_tail(self):
                token = self.tokenized_expression.next()
                if token is None or token['type'] != 'OP_sep':
                        self.tokenized_expression.prev()
                        return None

                if token['type'] == 'OP_sep':
                        return None

                item = self.operator()
                if item is None:
                        raise CompileError()

                items = [item]
                item = self.operator_list_tail()
                if item is not None:
                        items += item.nodes

                return Node(None, items, node_name = self._get_name('olt', None))

        def operator(self):
                token = self.tokenized_expression.next()
                if token['type'] == 'OP_sep':
                        self.tokenized_expression.prev()
                        return None
                self.token_check(token, 'NAME')

                item1 = Node(None, [token, None], is_leaf = True, node_name = self._get_name('i', None, token))

                token = self.tokenized_expression.next()
                self.token_check(token, 'OP_assignment')

                op = token
                item2 = self.expression()
                if item2 is None:
                        raise CompileError()

                return Node(op, [item1, item2], node_name = self._get_name('o', op))

        def expression(self, ):
                item1 = self.arithmetic_expression()
                if item1 is None:
                        raise CompileError()

                item2 = None
                op = None
                token = self.tokenized_expression.next()
                if token is not None:
                        if token['type'] == 'OP_comparelike':
                                op = token
                                item2 = self.arithmetic_expression()
                                if item2 is None:
                                    raise CompileError()
                        elif token['type'] not in self.operations_after_expression:
                                raise CompileError()
                        else:
                                self.tokenized_expression.prev()
                return Node(op, [item1, item2], node_name = self._get_name('e', op))

        def arithmetic_expression(self):
                item1 = self.term()
                if item1 is None:
                        raise CompileError()

                item2 = None
                op = None
                token = self.tokenized_expression.next()
                if token is not None:
                        while token is not None and token['type'] == 'OP_addlike':
                                if item2 is not None:
                                        item1 = Node(op, [item1, item2], node_name = self._get_name('ae', op))
                                op = token
                                item2 = self.term()
                                if item2 is None:
                                        raise CompileError()

                                token = self.tokenized_expression.next()
                        else:
                                self.tokenized_expression.prev()
                return Node(op, [item1, item2], node_name = self._get_name('ae', op))

        def term(self):
                item1 = self.factor()
                if item1 is None:
                        raise CompileError()

                item2 = None
                op = None
                token = self.tokenized_expression.next()
                if token is not None:
                        while token is not None and token['type'] == 'OP_mullike':
                                if item2 is not None:
                                        item1 = Node(op, [item1, item2], node_name = self._get_name('t', op))
                                op = token
                                item2 = self.factor()
                                if item2 is None:
                                        raise CompileError()

                                token = self.tokenized_expression.next()
                        else:
                                self.tokenized_expression.prev()
                return Node(op, [item1, item2], node_name = self._get_name('t', op))

        def factor(self):
                token = self.tokenized_expression.next()
                if token is not None and token['type'] == 'OP_closebrackets':
                        raise CompileError()

                item = token
                is_leaf = True
                if token is not None and token['type'] == 'OP_openbrackets':
                        is_leaf = False
                        item = self.arithmetic_expression()
                        token = self.tokenized_expression.next()
                        if token is None or token['type'] != 'OP_closebrackets':
                                raise CompileError()
                if item is not None:
                        return Node(None, [item, None], is_leaf = is_leaf, node_name = self._get_name('f', None, item))
                return None

        def _get_name(self, name, op, val = None):
                new_name = name + str(self.count[name])
                self.count[name] += 1
                if op is not None:
                        new_name += ' op: ' + op['value']
                if val is not None and type(val) != Node:
                        new_name += 'v:' + val['value']
                return new_name