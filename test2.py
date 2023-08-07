# 词法分析器
def lexer(expression):
    tokens = expression.replace("(", " ( ").replace(")", " ) ").split()
    return tokens

# 语法分析器
def parser(tokens):
    # 运算符优先级字典
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }

    # 递归下降语法分析
    def expression():
        nonlocal token_index
        nonlocal tokens

        term_result = term()

        while token_index < len(tokens) and tokens[token_index] in ('+', '-'):
            operator = tokens[token_index]
            operator_precedence = precedence[operator]
            token_index += 1
            right_term_result = term()

            while (token_index < len(tokens)
                   and tokens[token_index] in ('+', '-')
                   and precedence[tokens[token_index]] >= operator_precedence):
                next_operator = tokens[token_index]
                token_index += 1
                right_term_result = (next_operator, right_term_result, term())

            term_result = (operator, term_result, right_term_result)

        return term_result

    def term():
        nonlocal token_index
        nonlocal tokens

        factor_result = factor()

        while (token_index < len(tokens)
               and tokens[token_index] in ('*', '/')
               and precedence[tokens[token_index]] >= 2):
            operator = tokens[token_index]
            token_index += 1
            factor_result = (operator, factor_result, factor())

        return factor_result

    def factor():
        nonlocal token_index
        nonlocal tokens

        if token_index < len(tokens):
            token = tokens[token_index]
            token_index += 1

            if token.isdigit():
                return int(token)
            elif token == '(':
                sub_expression_result = expression()

                if token_index < len(tokens) and tokens[token_index] == ')':
                    token_index += 1
                    return sub_expression_result
                else:
                    raise ValueError("Missing closing parenthesis")
            else:
                raise ValueError("Invalid token: " + token)
        else:
            raise ValueError("Unexpected end of expression")

    # 初始化token索引
    token_index = 0

    # 开始解析
    return expression()

# 测试计算器
expression = input("Enter an arithmetic expression: ")
tokens = lexer(expression)
ast = parser(tokens)
print("Abstract Syntax Tree:", ast)