from exception import CompileError

def parse(expression):
        ast = AstTreeBuilder()
        ast.build(expression)

class Node():
        def __init__(self, operations = None, nodes = None, is_leaf = False, node_name = 'NO_NAME'):
                self.operations = operations
                self.nodes = nodes
                self.is_leaf = is_leaf
                self.node_name = node_name
    
class AstTreeBuilder():
        def __init__(self):
                self.lexer = None
                self.root = Node()
                self.operations_after_expression = {'OP_blockopenbrackets', 'OP_blockclosebrackets', 'OP_sep'}
                self.count = {'f': 0, 'i': 0, 't': 0, 'ae': 0,
                                      'e': 0, 'o': 0, 'olt': 0,
                                      'ol': 0, 'b': 0, 'p': 0}

        def _get_name(self, name, op, val = None):
            new_name = name + str(self.count[name])
            self.count[name] += 1
            if op is not None:
                new_name += ' op: ' + op['value']
            if val is not None and type(val) != Node:
                new_name += 'v:' + val['value']
            return new_name

        def factor(self):
            lex = self.lexer.next()
            if lex is not None and lex['type'] == 'OP_closebrackets':
                raise CompileError()
            item = lex
            is_leaf = True
            if lex is not None and lex['type'] == 'OP_openbrackets':
                is_leaf = False
                item = self.arithmetic_expression()
                lex = self.lexer.next()
                # print('s', self.lexer.num)
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
            lex = self.lexer.next()
            if lex is not None:
                while lex is not None and lex['type'] == 'OP_mullike':
                    if item2 is not None:
                        item1 = Node(op, [item1, item2],
                                    node_name = self._get_name('t', op))
                    op = lex
                    item2 = self.factor()
                    if item2 is None:
                        raise CompileError()

                    lex = self.lexer.next()
                else:
                    self.lexer.prev()

            res = Node(op, [item1, item2],
                        node_name = self._get_name('t', op))
            return res


        def arithmetic_expression(self):
            item1 = self.term()
            if item1 is None:
                raise CompileError()
            item2 = None
            op = None
            lex = self.lexer.next()
            if lex is not None:
                while lex is not None and lex['type'] == 'OP_addlike':
                    if item2 is not None:
                        item1 = Node(op, [item1, item2], node_name = self._get_name('ae', op))
                    op = lex
                    item2 = self.term()
                    if item2 is None:
                        raise CompileError()

                    lex = self.lexer.next()
                else:
                    self.lexer.prev()
            return Node(op, [item1, item2], node_name = self._get_name('ae', op))

        def expression(self, ):
            item1 = self.arithmetic_expression()
            item2 = None
            if item1 is None:
                raise CompileError()
            op = None
            # print(self.lexer.num)
            # print(len(self.lexer.tokens))
            lex = self.lexer.next()
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
                    self.lexer.prev()

            return Node(op, [item1, item2], node_name = self._get_name('e', op))


        def operator(self):
            lex = self.lexer.next()
            if lex is None or lex['type'] != 'NAME':
                raise CompileError()
            item1 = Node(None, [lex, None], is_leaf = True, node_name = self._get_name('i', None, lex))
            lex = self.lexer.next()
            if lex is None or lex['type'] != 'OP_assignment':
                raise CompileError()

            op = lex
            item2 = self.expression()

            if item2 is None:
                raise CompileError()

            return Node(op, [item1, item2], node_name = self._get_name('o', op))

        def operator_list_tail(self):
            items = []
            lex = self.lexer.next()
            if lex is None or lex['type'] != 'OP_sep':
                self.lexer.prev()
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
            lex = self.lexer.next()
            if lex is None or lex['type'] != 'OP_blockopenbrackets':
                raise CompileError()
            item = self.operator_list()
            lex = self.lexer.next()

            if lex is None or lex['type'] != 'OP_blockclosebrackets':
                raise CompileError()

            return Node(None, [item, None], node_name = self._get_name('b', None))

        def programm(self):
            item = self.block()
            self.root.operations = None
            self.root.nodes = [item, None]
            self.root.node_name = self._get_name('p', None)

        def build(self, lexer):
            self.lexer = lexer
            self.programm()
            if self.lexer.num < len(self.lexer.tokens):
                raise CompileError()
