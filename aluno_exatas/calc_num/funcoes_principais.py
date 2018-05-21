import numpy as np
from typing import Callable

def metodo_bisseccao (f: Callable[[float], float], a, b):
    '''método da bissecção para uma função f qualquer, dado o intervalo [a,b]
    retorna novo intervalo: a,b = metodo_bisseccao(f, a, b)'''
    fa = f(a)
    #fb = f(b)
    c = (a+b)/2
    fc = f(c)
    if (np.sign(fa)*np.sign(fc) < 0):
        return a, c
    else:
        return c, b

def metodo_newton (f: Callable[[float], float], flinha: Callable[[float], float], x):
    '''método de newton para uma função f qualquer, com derivada flinha e aproximação inicial x
    retorna novo x: x = metodo_newton(f, flinha, x)'''
    return x - f(x)/flinha(x)

def metodo_secante (f: Callable[[float], float], x, xo):
    '''método da secante para uma função f qualquer, com aproximações iniciais x e xo
    retorna novo x: x,xo = metodo_secante(f, x, xo)'''
    if np.abs(x-xo) == 0:
        return x,xo
    return x - f(x) * (x - xo) / (f(x) - f(xo)), x