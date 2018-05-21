# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 00:09:09 2017

@author: erico
"""

#__name__ = 'inicializacao'

import numpy as np
import scipy as scp
import sympy as sp

def input_matrix ():
    '''Essa função permite facilmente fazer input de uma matriz qualquer, no formato de
    np.array, e retorna a matriz'''
    r = int(input('rows: '))
    c = int(input('columns: '))

    a = np.zeros((r,c)) #é necessário inicializar a matriz

    for i in range(r):
        '''for j in range(c):
            a[i,j] = float(input()) #itens - ainda falta fazer input por linha'''
        a[i] = list(map(complex(input('linha ' + str(i+1) + ': ').split())))
    
    return a

secante = lambda x, xo, g: [x-g(x)*(x-xo)/(g(x)-g(xo)), x]
'''método da secante para uma função g qualquer, com aproximações iniciais x e xo
retorna novo x: x,xo = secante(x, xo, g)'''

#newton = lambda x, f, flinha: x - f(x)/flinha(x)
'''método de newton para uma função f qualquer, com derivada flinha e aproximação inicial x
retorna novo x: x = newton(x, f, flinha)'''
        
def bisseccao (f, a, b):
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

def propagacao (funcaoy, us):
    '''A partir de uma função funcaoy, retorna a propagação de incertezas (raiz quadrada da
    soma do produto dos quadrados das derivadas parciais e dos quadrados das incertezas)
    As incertezas são obtidas a partir de um dicionário us do formato: us = {var1:u1,...,varn:un}
    retorna f_uy: f_uy = propagacao(funcaoy, us)'''
    f_uy = 0
    for var in funcaoy.atoms(sp.Symbol):
        f_uy += funcaoy.diff(var)**2*us[var]**2
    return sp.sqrt(f_uy)

def substituicao (funcao, valor, valor_mantido = []):
    '''A partir de uma função funcao, retorna a substituição dos valores simbólicos pelos seus
    valores reais. As variáveis na lista valor_mantido continuam simbólicas.
    Os valores reais são obtidos a partir de um dicionário do formato: valor = {var1:valor1,...,varn:valorn}
    retorna funcao: funcao = substituicao(funcao, valor, valor_mantido)'''
    for var in funcao.atoms(sp.Symbol):
        if var in valor_mantido:
            continue
        funcao = funcao.subs(var, valor[var])
    return funcao

def retornar_fu (funcao, us, valor, variaveis = []):
    funcao = propagacao(funcao, us)
    funcao = substituicao(funcao, valor, variaveis)
    if variaveis is []:
        return funcao
    else:
        return funcao.lambdify(variaveis)