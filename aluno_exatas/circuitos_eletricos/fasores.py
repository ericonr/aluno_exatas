# -*- coding: utf-8 -*-
"""Esse módulo contém funções que permitem trabalhar-se 
facilmente com fasores, que normalmente são representados 
na forma polar.
"""

import numpy as np
from functools import partial


def polar_para_complexo(r: float, angle: float, degree=True):
    """Essa função converte números complexos representados 
    em coordenadas polares para números complexos normais. 
    Pode receber o ângulo em radianos ou em graus.
    """

    if degree:
        return r * np.exp(1j * np.deg2rad(angle))
    else:
        return r * np.exp(1j * angle)


def complexo_para_polar(n: complex, degree=True):
    """Essa função recebe números complexos e retorna 
    coordenadas polares. Pode retornar o ângulo em radianos 
    ou em graus.
    """

    if degree:
        return np.abs(n), np.rad2deg(np.angle(n))
    else:
        return np.abs(n), np.angle(n)


p2c = polar_para_complexo
c2p = complexo_para_polar

p2cr = partial(polar_para_complexo, degree=False)
p2cr.__doc__ = '''Faz a mesma coisa que p2c, mas está configurada
para ângulos em radianos como padrão.'''

c2pr = partial(complexo_para_polar, degree=False)
c2pr.__doc__ = '''Faz a mesma coisa que c2p, mas está configurada
para ângulos em radianos como padrão.'''
