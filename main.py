import math
import os
import solve
import keyboard
import platform
from colorama import Fore, init
init()
def clear():
    current_os = platform.system()
    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')
clear()
while True:
    print("=============EquationSolver | 方程求解器=============")
    print("选择方程(组)类型:")
    print("[1]一元二次方程  [2]二元一次方程组\n[0]退出  [9]关于")
    n = input("输入序号:")
    if n == "1":
        clear()
        print("<一元二次方程求解>")
        print(Fore.YELLOW+"### 此程序不能求出方程的精确解 ###")
        print(Fore.WHITE+"ax^2 + bx + c = 0")
        str_a = input("输入已知数(a):")
        str_b = input("输入已知数(b):")
        str_c = input("输入已知数(c):")
        a = float(str_a)
        b = float(str_b)
        c = float(str_c)
        out = solve.equation1_2(a,b,c)
        if out == "nan":
            print(Fore.RED+"结果非实数!!!")
        if len(out) == 2:
            print(Fore.GREEN+"x1 = "+str(out[0]))
            print(Fore.GREEN+"x2 = "+str(out[1]))
        if len(out) == 1:
            print(Fore.GREEN+"x = "+str(out))
        print(Fore.WHITE)
        os.system("pause")
        clear()
    elif n == "2":
        clear()
        print("<二元一次方程组求解>")
        print(Fore.WHITE+"(a1)x + (b1)y = (c1)\n(a2)x + (b2)y = (c2)")
        str_a1 = input("输入已知数(a1):")
        str_b1 = input("输入已知数(b1):")
        str_c1 = input("输入已知数(c1):")
        str_a2 = input("输入已知数(a2):")
        str_b2 = input("输入已知数(b2):")
        str_c2 = input("输入已知数(c2):")
        a1 = float(str_a1)
        b1 = float(str_b1)
        c1 = float(str_c1)
        a2 = float(str_a2)
        b2 = float(str_b2)
        c2 = float(str_c2)
        ans = solve.equation2_1(a1,b1,c1,a2,b2,c2)
        if ans == "Infinite solutions":
            print(Fore.GREEN+"所有实数")
        elif ans == "No solution":
            print(Fore.RED+"无解")
        else:
            print(Fore.GREEN+"x = "+str(ans[0]))
            print(Fore.GREEN+"y = "+str(ans[1]))
        print(Fore.WHITE)
        os.system("pause")
        clear()
    elif n == "0":
        break
    elif n == "9":
        clear()
        print(Fore.GREEN+"本程序由codedog开发")
        n = input(Fore.WHITE+"[0]退出  [1]返回 :")
        if n == "0":
            break
        else:
            clear()
    else:
        clear()