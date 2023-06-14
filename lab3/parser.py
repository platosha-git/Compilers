from exception import CompileError
Ok = True

def parse(tokenized_expression):
        Parser(tokenized_expression)
    
class Parser:
        def __init__(self, tokenized_expression):
                self.tokenized_expression = tokenized_expression
                self.operations_after_expression = {'OP_blockopenbrackets', 'OP_blockclosebrackets', 'OP_sep'}
                self.parse()

        def token_check(self, token, expected_type):
                if token is None or token['type'] != expected_type:
                        raise CompileError()

        def parse(self):
                self.block()
                if self.tokenized_expression.num < len(self.tokenized_expression.tokens):
                        raise CompileError()

        def block(self):
                token = self.tokenized_expression.next()
                self.token_check(token, 'OP_blockopenbrackets')

                token = self.tokenized_expression.next()
                while token['type'] != 'OP_blockclosebrackets':
                    self.tokenized_expression.prev()
                    self.operator_list()
                    token = self.tokenized_expression.next()

                self.token_check(token, 'OP_blockclosebrackets')

        def operator_list(self):
                self.operator()
                self.operator_list_tail()

        def operator(self):
                token = self.tokenized_expression.next()
                if token['type'] == 'OP_sep':
                        self.tokenized_expression.prev()
                        return
                self.token_check(token, 'NAME')

                token = self.tokenized_expression.next()
                self.token_check(token, 'OP_assignment')

                item2 = self.expression()
                if item2 is None:
                        raise CompileError()

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

                self.operator_list_tail()
                return Ok

        def expression(self, ):
                item1 = self.arithmetic_expression()
                if item1 is None:
                        raise CompileError()

                token = self.tokenized_expression.next()
                if token is not None:
                        if token['type'] == 'OP_comparelike':
                                item2 = self.arithmetic_expression()
                                if item2 is None:
                                    raise CompileError()
                        elif token['type'] not in self.operations_after_expression:
                                raise CompileError()
                        else:
                                self.tokenized_expression.prev()
                return Ok

        def arithmetic_expression(self):
                item1 = self.term()
                if item1 is None:
                        raise CompileError()

                token = self.tokenized_expression.next()
                if token is not None:
                        while token is not None and token['type'] == 'OP_addlike':
                                item = self.term()
                                if item is None:
                                        raise CompileError()
                                token = self.tokenized_expression.next()
                        else:
                                self.tokenized_expression.prev()
                return Ok

        def term(self):
                item1 = self.factor()
                if item1 is None:
                        raise CompileError()

                token = self.tokenized_expression.next()
                if token is not None:
                        while token is not None and token['type'] == 'OP_mullike':
                                item = self.factor()
                                if item is None:
                                        raise CompileError()
                                token = self.tokenized_expression.next()
                        else:
                                self.tokenized_expression.prev()
                return Ok

        def factor(self):
                token = self.tokenized_expression.next()
                if token is not None and token['type'] == 'OP_closebrackets':
                        raise CompileError()

                item = token
                if token is not None and token['type'] == 'OP_openbrackets':
                        item = self.arithmetic_expression()
                        token = self.tokenized_expression.next()
                        if token is None or token['type'] != 'OP_closebrackets':
                                raise CompileError()

                return Ok if item is not None else None
