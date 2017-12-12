import numpy as np

def metodo_bisseccao (f, a, b):
    '''método da bissecção para uma função f qualquer, dado o intervalo [a,b]
    retorna novo intervalo: a,b = bisseccao(f, a, b)'''
    fa = f(a)
    #fb = f(b)
    c = (a+b)/2
    fc = f(c)
    if (np.sign(fa)*np.sign(fc) < 0):
        return a, c
    else:
        return c, b

def metodo_newton (f, flinha, x):
    '''método de newton para uma função f qualquer, com derivada flinha e aproximação inicial x
    retorna novo x: x = newton(f, flinha, x)'''
    return x - f(x)/flinha(x)