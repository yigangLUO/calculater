# 词法分析器
def lexer(expression):
    tokens = expression.replace("(", " ( ").replace(")", " ) ").split()
    return tokens

# 语法分析器
def parser(tokens):
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }
    # 递归下降语法分析
    def expression():
        nonlocal token_index # nonlocal 声明一个变量是非局部变量，即它位于当前函数的外层函数的作用域中
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
                sub_experssion_result = expression()

                if token_index < len(tokens) and tokens[token_index] == ')':
                    token_index += 1
                    return sub_experssion_result
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

# 中间代码生成
def generate_intermediate_code(expression):
    return parser(lexer(expression))

# 目标代码生成
def generate_target_code(intermediate_code):
    return str(intermediate_code)

# 测试计算器
expression = input("Enter an arithmetic expression: ")
intermediate_code = generate_intermediate_code(expression)
target_code = generate_target_code(intermediate_code)
print("Intermediate Code:", intermediate_code)
print("Target Code:", target_code)