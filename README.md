# Aluno de exatas

Conjunto de funções que têm como objetivo facilitar a vida de um aluno de exatas.
Atualmente, o módulo tem implementada as funções relacionadas à disciplina de física
experimental, que fornecem um módulo para ser utilizado principalmente na propagação
de incertezas.

## fis_exp

Esse módulo pode ser usado da seguinte forma:

```python
import aluno_exatas.fis_exp as fe

f = fe.FisExp('a+b*c') #inicializa o objeto com 'a+b*c' como funcao principal
f.valores_conhecidos = {'a':10, 'b':20} #mostra quais valores sao constantes
f.incertezas_conhecidas = {'a':1, 'b':2, 'c':3} #mostra as incertezas conhecidas

f.gerar_funcao(['c']) #gera funcao que vai ser avaliada em diferentes valores de c
f.gerar_propagacao(['c'] #gera propagacao que vai ser avaliada em diferentes valores de c

f5 = f.funcao_gerada(5) #avalia a funcao principal em c=5
p5 = f.propagacao_gerada(5) #avalia a propagacao em c=5
```