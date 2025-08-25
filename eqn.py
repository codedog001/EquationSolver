import sympy as sp
class EquationSolver:
    @staticmethod
    def solve_equation(equation_str, var='x'):
        """
        求解单个方程
        :param equation_str: 方程字符串，例如 'x**2 - 4 = 0'
        :param var: 变量名，默认为 'x'
        :return: 解的列表
        """
        x = sp.symbols(var)
        eq = sp.sympify(equation_str.replace('=', '-(') + ')')
        solutions = sp.solve(eq, x)
        return solutions

    @staticmethod
    def solve_system(equations, vars):
        """
        求解方程组
        :param equations: 方程字符串列表，例如 ['x + y = 2', 'x - y = 0']
        :param vars: 变量名列表，例如 ['x', 'y']
        :return: 解的字典
        """
        symbols = sp.symbols(vars)
        eqs = [sp.sympify(eq.replace('=', '-(') + ')') for eq in equations]
        solutions = sp.solve(eqs, symbols, dict=True)
        return solutions