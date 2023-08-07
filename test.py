# 词法分析器
def lexer(expression):
    tokens = expression.replace("(", " ( ").replace(")", " ) ").split()
    return tokens

# 语法分析器
def parser(tokens):
    # 更新运算符优先级字典
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3,  # 添加指数运算符
        '%': 2   # 添加取余运算符
    }

    # 解析函数
    def expression():
        nonlocal token_index
        nonlocal tokens

        term_result = term()

        while (token_index < len(tokens) and tokens[token_index] in ('+', '-')
               and precedence[tokens[token_index]] >= 1):
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
               and tokens[token_index] in ('*', '/', '%')
               and precedence[tokens[token_index]] >= 2):
            operator = tokens[token_index]
            token_index += 1
            factor_result = (operator, factor_result, factor())

        return factor_result

    def factor():
        nonlocal token_index
        nonlocal tokens

        base_result = base()

        while (token_index < len(tokens)
               and tokens[token_index] == '^'
               and precedence[tokens[token_index]] >= 3):
            operator = tokens[token_index]
            token_index += 1
            exponent_result = factor()
            base_result = (operator, base_result, exponent_result)

        return base_result

    def base():
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

    def evaluate(ast):
        if isinstance(ast, int):
            return ast
        elif isinstance(ast, tuple):
            operator = ast[0]
            left_operand = evaluate(ast[1])
            right_operand = evaluate(ast[2])

            if operator == '+':
                return left_operand + right_operand
            elif operator == '-':
                return left_operand - right_operand
            elif operator == '*':
                return left_operand * right_operand
            elif operator == '/':
                return left_operand / right_operand
            elif operator == '^':
                return left_operand ** right_operand
            elif operator == '%':
                return left_operand % right_operand
            else:
                raise ValueError("Invalid operator: " + operator)
        else:
            raise ValueError("Invalid AST node")

    # 初始化token索引
    token_index = 0

    # 开始解析
    ast = expression()
    result = evaluate(ast)
    return {ast, result}

# 测试计算器
expression = input("Enter an arithmetic expression: ")
tokens = lexer(expression)
code, result = parser(tokens)
print("Result:", result)
print("code:", code)