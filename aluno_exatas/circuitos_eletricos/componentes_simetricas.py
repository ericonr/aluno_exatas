# -*- coding: utf-8 -*-

"""Esse módulo define constantes que são úteis para trabalhar-se
com componentes simétricas em circuitos elétricos trifásicos.
"""

import numpy as np
from aluno_exatas.circuitos_eletricos.fasores import p2c

# relação entre fases
alpha = p2c(1,120)

# matriz que multiplica a matriz de componentes
T = [[1, 1, 1],
     [1, alpha**2, alpha],
     [1, alpha, alpha**2]]
T = np.array(T)

# inversa de T
T_i = [[1, 1, 1],
       [1, alpha, alpha**2],
       [1, alpha**2, alpha]]
T_i = 1/3 * np.array(T_i)
