from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import re
from colorama import Fore, Style, init

# 初始化colorama
init(autoreset=True)

def format_math(expr_str, use_unicode=True):
    """
    格式化数学表达式为美观的输出字符串
    """
    try:
        # 提取表达式中的所有变量名
        variables = set(re.findall(r'\b([a-zA-Z_][a-zA-Z_0-9]*\b)', expr_str))
        
        # 预定义函数和常量
        known_terms = {
            'sin', 'cos', 'tan', 'cot', 'sec', 'csc',
            'asin', 'acos', 'atan', 'acot', 'asec', 'acsc',
            'sinh', 'cosh', 'tanh', 'coth', 'sech', 'csch',
            'asinh', 'acosh', 'atanh', 'acoth', 'asech', 'acsch',
            'exp', 'log', 'ln', 'sqrt', 'abs',
            'diff', 'integrate', 'limit', 'Sum', 'Product',
            'Matrix', 'Rational', 'factorial', 'binomial',
            'pi', 'oo', 'I', 'E', 'infty', 'inf'
        }
        
        # 创建符号字典
        local_dict = {}
        for var in variables:
            if var not in known_terms:
                local_dict[var] = Symbol(var)
        
        # 添加预定义函数和常量
        local_dict.update({
            'sin': sin, 'cos': cos, 'tan': tan,
            'asin': asin, 'acos': acos, 'atan': atan,
            'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
            'exp': exp, 'log': log, 'sqrt': sqrt, 'abs': Abs,
            'diff': diff, 'integrate': integrate, 'limit': limit,
            'Sum': Sum, 'Product': Product, 'Matrix': Matrix,
            'Rational': Rational, 'factorial': factorial,
            'pi': pi, 'oo': oo, 'I': I, 'E': E
        })
        
        # 解析并格式化表达式
        expr = parse_expr(expr_str, local_dict=local_dict)
        return pretty(expr, use_unicode=use_unicode, wrap_line=False)
        
    except Exception as e:
        # 如果解析失败，返回原始字符串
        return expr_str

def parse_key_value_pairs(expr_str, separator=","):
    """
    更健壮的键值对解析，处理各种格式
    """
    pairs = []
    current_pair = ""
    in_quotes = False
    bracket_depth = 0
    
    for char in expr_str:
        if char == '"' or char == "'":
            in_quotes = not in_quotes
            current_pair += char
        elif char in '([{':
            bracket_depth += 1
            current_pair += char
        elif char in ')]}':
            bracket_depth -= 1
            current_pair += char
        elif char == separator and not in_quotes and bracket_depth == 0:
            if current_pair.strip():
                pairs.append(current_pair.strip())
            current_pair = ""
        else:
            current_pair += char
    
    if current_pair.strip():
        pairs.append(current_pair.strip())
    
    return pairs

def colorize_math_expression(expr, use_colors=True):
    """
    给数学表达式添加颜色：函数黄色，变量青色
    """
    if not use_colors or not expr:
        return expr
    
    # 数学函数列表（黄色）
    math_functions = {
        'sin', 'cos', 'tan', 'cot', 'sec', 'csc',
        'asin', 'acos', 'atan', 'acot', 'asec', 'acsc',
        'sinh', 'cosh', 'tanh', 'coth', 'sech', 'csch',
        'asinh', 'acosh', 'atanh', 'acoth', 'asech', 'acsch',
        'exp', 'log', 'ln', 'sqrt', 'abs',
        'diff', 'integrate', 'limit', 'Sum', 'Product',
        'Rational', 'factorial', 'binomial'
    }
    
    # 常量列表（洋红色）
    constants = {'pi', 'oo', 'I', 'E', 'infty', 'inf'}
    
    colored_expr = expr
    
    # 先给函数添加颜色（黄色）
    for func in math_functions:
        colored_expr = re.sub(r'\b' + func + r'\b', 
                            f"{Fore.YELLOW}{func}{Style.RESET_ALL}", 
                            colored_expr)
    
    # 给常量添加颜色（洋红色）
    for const in constants:
        colored_expr = re.sub(r'\b' + const + r'\b', 
                            f"{Fore.MAGENTA}{const}{Style.RESET_ALL}", 
                            colored_expr)
    
    # 给变量添加颜色（青色）- 匹配单个字母变量
    colored_expr = re.sub(r'\b([a-zA-Z])\b', 
                        f"{Fore.CYAN}\\1{Style.RESET_ALL}", 
                        colored_expr)
    
    # 给多字母变量添加颜色（青色）
    colored_expr = re.sub(r'\b([a-zA-Z_][a-zA-Z_0-9]*)\b', 
                        f"{Fore.CYAN}\\1{Style.RESET_ALL}", 
                        colored_expr)
    
    return colored_expr

def colorize_key_value(key, value, max_key_length, use_colors=True):
    """
    给键值对添加颜色：键和冒号绿色，值中的函数黄色，变量青色
    """
    if use_colors:
        colored_key = f"{Fore.GREEN}{key}{Style.RESET_ALL}"
        colored_colon = f"{Fore.GREEN}:{Style.RESET_ALL}"
    else:
        colored_key = key
        colored_colon = ":"
    
    if value is not None:
        # 给值中的数学表达式添加颜色
        colored_value = colorize_math_expression(value, use_colors)
        
        if '\n' in colored_value:
            value_lines = colored_value.split('\n')
            aligned_line = f"{colored_key:<{max_key_length}} {colored_colon} {value_lines[0]}"
            lines = [aligned_line]
            for line in value_lines[1:]:
                lines.append(f"{' ':>{max_key_length + 3}}{line}")
            return lines
        else:
            return [f"{colored_key:<{max_key_length}} {colored_colon} {colored_value}"]
    else:
        return [key]

def robust_format_key_value_math(expr_str, use_unicode=True, use_colors=True, add_separators=True):
    """
    更健壮的键值对格式化函数，支持多种颜色和分隔线
    """
    try:
        # 使用更健壮的解析
        pairs = parse_key_value_pairs(expr_str)
        
        formatted_lines = []
        max_key_length = 0
        key_value_pairs = []
        
        # 第一遍：解析所有键值对并计算最大键长度
        for pair in pairs:
            if ':' in pair:
                # 找到第一个冒号
                colon_pos = pair.find(':')
                key = pair[:colon_pos].strip()
                value_str = pair[colon_pos + 1:].strip()
                
                # 尝试美化值，如果失败则使用原始值
                try:
                    formatted_value = format_math(value_str, use_unicode)
                except:
                    formatted_value = value_str
                
                key_value_pairs.append((key, formatted_value))
                max_key_length = max(max_key_length, len(key))
            else:
                # 不是键值对，可能是注释或其他内容
                key_value_pairs.append((pair, None))
                max_key_length = max(max_key_length, len(pair))
        
        # 第二遍：格式化输出并添加颜色
        for i, (key, formatted_value) in enumerate(key_value_pairs):
            if add_separators and i > 0:
                # 添加分隔线（20个绿色的-）
                separator_line = f"{Fore.GREEN}{'-' * 20}{Style.RESET_ALL}" if use_colors else '-' * 20
                formatted_lines.append(separator_line)
            
            # 添加颜色并格式化
            lines = colorize_key_value(key, formatted_value, max_key_length, use_colors)
            formatted_lines.extend(lines)
        
        return '\n'.join(formatted_lines)
        
    except Exception as e:
        return f"格式化错误: {str(e)}"

def format_colored_math(expr_str, use_unicode=True):
    """
    带颜色的数学公式格式化函数，支持键值对和普通表达式
    """
    # 检查是否是键值对格式
    if ':' in expr_str and (',' in expr_str or '\n' in expr_str):
        return robust_format_key_value_math(expr_str, use_unicode, use_colors=True, add_separators=True)
    else:
        # 对于普通数学表达式
        try:
            result = format_math(expr_str, use_unicode)
            # 给普通表达式添加颜色
            return colorize_math_expression(result, use_colors=True)
        except:
            return expr_str

# 使用示例
if __name__ == "__main__":
    # 测试各种键值对格式
    test_cases = [
        "x: 6, y: 4",
        "a: 2, b: 3, c: sin(x)**2/3",
        "radius: 5, area: pi * radius**2, circumference: 2 * pi * radius",
        "matrix: [[1, 2], [3, 4]], determinant: -2",
        "variables: x=3, y=4, distance: sqrt(x**2 + y**2)",
        "f(x): x**2 + 2*x + 1, derivative: 2*x + 2, integral: (x**3)/3 + x**2 + x",
        "complex: sin(alpha) * cos(beta) + exp(-gamma*t)",
        "special: pi + E + I, infinity: oo"
    ]
    
    print("多彩键值对公式美化示例:")
    print("=" * 60)
    print(f"{Fore.GREEN}键和冒号{Style.RESET_ALL} {Fore.YELLOW}函数{Style.RESET_ALL} {Fore.CYAN}变量{Style.RESET_ALL} {Fore.MAGENTA}常量{Style.RESET_ALL}")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n示例 {i}: {test_case}")
        print("-" * 40)
        result = format_colored_math(test_case)
        print(result)
        print()
    
    # 测试普通数学表达式
    print("\n普通数学表达式示例:")
    print("=" * 40)
    math_exprs = [
        "sin(x)**2/3 + cos(y)*sqrt(z)",
        "pi * r**2 + exp(-alpha*t)",
        "Sum(1/n**2, (n, 1, oo))",
        "diff(sin(x)*cos(y), x, y)"
    ]
    
    for expr in math_exprs:
        print(f"\n表达式: {expr}")
        print("美化结果:")
        result = format_colored_math(expr)
        print(result)
        print("-" * 30)
    
    # 测试不带颜色的版本
    print("\n\n不带颜色的版本:")
    print("=" * 40)
    for test_case in test_cases[:2]:
        print(f"\n{test_case}")
        print("-" * 20)
        result = robust_format_key_value_math(test_case, use_colors=False, add_separators=True)
        print(result)