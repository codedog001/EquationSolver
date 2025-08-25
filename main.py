from colorama import *
from eqn import *
import os
import re
import platform
import format_math
init()
def smart_multiply(expression):
    # 常见数学函数列表
    math_functions = ['sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt']
    # 先处理数字后跟字母/括号的情况
    expression = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expression)
    # 处理右括号后跟字母/数字/括号的情况
    expression = re.sub(r'(\))([a-zA-Z(\d])', r'\1*\2', expression)
    # 避免在函数名内部添加乘号
    for func in math_functions:
        expression = expression.replace(f"*{func}", func)
    return expression
def extract_unique_letters(s):
    unique_letters = set()
    for char in s:
        if char.isalpha():
            unique_letters.add(char.lower())
    return list(unique_letters)
def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
def pause():
    input(Fore.WHITE + "输入回车键继续...")
    clear()
def main():
    clear()
    print("方程求解器 | Equation Solver")
    print(Fore.YELLOW + "-"*30)
    print(Fore.YELLOW + "请全屏使用")
    print(Fore.YELLOW + "Windows10请用\"终端\"软件打开")
    print(Fore.YELLOW + "方程组用 \" , \" 分隔")
    print(Fore.YELLOW + "平方用 \" ^ \" 表示, 乘法不能省略乘号")
    print(Fore.YELLOW + "输入 \" exit \" 退出")
    print(Fore.YELLOW + "输入 \" about \" 了解更多")
    print(Fore.YELLOW + "-"*30)
    j = 1
    while True:
        eqn = input(Fore.CYAN+f"eqn[{j}]: ")
        if eqn !="cls" and eqn !="clear" and eqn != "about" and eqn != "exit":
            j += 1
        eqn = smart_multiply(eqn)
        eqn = eqn.replace("**", "^")
        if eqn == "exit":
            break
        elif eqn == "about":
            print(Fore.GREEN+"这是一个方程求解器")
        elif eqn == "clear" or eqn == "cls":
            clear()
            continue
        else:
            try:
                unknowns = extract_unique_letters(eqn)
                if len(unknowns) == 0 or "=" not in eqn:
                    print(Fore.RED+"此方程无效")
                    print(Fore.BLUE+"*"*30)
                    continue
                if "," not in eqn and len(unknowns) == 1:
                    ans = EquationSolver.solve_equation(eqn, unknowns)
                    for i in range(len(ans)):
                        print(Fore.GREEN+unknowns[0]+": "+Fore.WHITE+format_math.format_colored_math(str(ans[i])))
                        if i < len(ans) - 1 and len(ans) > 1:
                            print(Fore.GREEN+"----------OR----------")
                if len(unknowns)>1:
                    eqns = re.split(r"[,]", eqn)
                    ans = EquationSolver.solve_system(eqns, unknowns)
                    for i in range(len(ans)):
                        print(Fore.GREEN+format_math.format_colored_math(str(ans[i])[1:-1]))
                        if len(ans)>1 and i < len(ans) - 1:
                            print(Fore.GREEN+"----------OR----------")
            except Exception as e:
                print(Fore.RED + f"发生错误: {e}")
            print(Fore.BLUE+"*"*30)
            del eqn
            continue
if __name__ == "__main__":
    main()