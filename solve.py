import math
#一元二次方程
def equation1_2(a1,b1,c1):
    a = float(a1)
    b = float(b1)
    c = float(c1)
    p = b*b-4*a*c
    if p > 0:
        x1 = (-b+math.sqrt(b*b-4*a*c))/(2*a)
        x2 = (-b-math.sqrt(b*b-4*a*c))/(2*a)
        return x1,x2
    if p == 0:
        x = -(b/(2*a))
        return x
    if p < 0:
        return "nan"
#二元一次方程组
def equation2_1(a1, b1, c1, a2, b2, c2):
    D = a1 * b2 - a2 * b1
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1
    if D == 0:
        if Dx == 0 and Dy == 0:
            return "Infinite solutions"
        else:
            return "No solution"
    else:
        x = Dx / D
        y = Dy / D
        return x, y