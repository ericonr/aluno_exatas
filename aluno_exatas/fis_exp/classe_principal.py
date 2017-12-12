#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sympy as sp

class FisExp:

	def __init__ (self, funcao, valores_conhecidos=dict(), incertezas_conhecidas=dict()):
		'''Inicializacao da funcao, em que configura a funcao principal, armazena os dicionarios e
		configura valores.
		'''
		if type(funcao) is str:
			self.__funcao = sp.sympify(funcao)
		else:
			self.__funcao = funcao

		self.__variaveis = self.__funcao.atoms(sp.Symbol)
		self.__incertezas = {}
		for simbolo in self.__variaveis:
			incerteza = sp.symbols('u_' + str(simbolo))
			self.__incertezas[simbolo] = incerteza

		self.__funcao_substituida = self.__funcao
		self.__valores_conhecidos = dict()
		self.valores_conhecidos = valores_conhecidos

		self._propagacao()
		self.__incertezas_conhecidas = dict()
		self.incertezas_conhecidas = incertezas_conhecidas

	@property
	def funcao (self):
		return self.__funcao
	@funcao.setter
	def funcao (self, nova_funcao):
		self.__init__(nova_funcao)

	@property
	def variaveis (self):
		return self.__variaveis
	@variaveis.setter
	def variaveis(self, a):
		pass

	@property
	def incertezas (self):
		return self.__incertezas
	@incertezas.setter
	def incertezas (self, a):
		pass

	@property
	def valores_conhecidos (self):
		return self.__valores_conhecidos
	@valores_conhecidos.setter
	def valores_conhecidos (self, valores_conhecidos):
		'''Gera o atributo "funcao_substituida", que é a função com os valores conhecidos para algumas variáveis
		É chamado por self.valores_conhecidos = dict com valores
		Para apagar os valores substituídos, é necessário usar self.valores_conhecidos = {}
		'''
		#for var in valores_conhecidos.keys():
		#	self.__valores_conhecidos[var] = valores_conhecidos[var]
		self.__valores_conhecidos = valores_conhecidos

		if not valores_conhecidos:
			self.__valores_conhecidos = dict()
			self.__funcao_substituida = self.__funcao
		else:
			self.__funcao_substituida = self.__funcao.subs(self.__valores_conhecidos)
		
	@property
	def funcao_substituida (self):
		return self.__funcao_substituida
	@funcao_substituida.setter
	def funcao_substituida (self, a):
		pass

	@property
	def incertezas_conhecidas (self):
		return self.__incertezas_conhecidas
	@incertezas_conhecidas.setter
	def incertezas_conhecidas (self, incertezas_conhecidas):
		'''Gera o atributo "propagacao_substituida", que é a função de propagação com os valores 
		conhecidos para algumas variáveis.
		É chamado por self.incertezas_conhecidas = dict com valores
		'''
		#for inc in incertezas_conhecidas.keys():
		#	self.__incertezas_conhecidas[inc] = incertezas_conhecidas[inc]
		self.__incertezas_conhecidas = incertezas_conhecidas

		incertezas_chaves_corretas = dict()
		for chave_variavel in self.__variaveis:
			if str(chave_variavel) in self.__incertezas_conhecidas.keys():
				incertezas_chaves_corretas[str(self.__incertezas[chave_variavel])] = self.__incertezas_conhecidas[str(chave_variavel)]

		propagacao_substituida = self.__propagacao.subs(incertezas_chaves_corretas)
		propagacao_substituida = propagacao_substituida.subs(self.__valores_conhecidos)

		self.__propagacao_substituida = propagacao_substituida

	@property
	def propagacao (self):
		return self.__propagacao
	@propagacao.setter
	def propagacao (self, a):
		pass

	@property
	def propagacao_substituida (self):
		return self.__propagacao_substituida
	@propagacao_substituida.setter
	def propagacao_substituida (self, a):
		pass

	def _propagacao (self):
		'''Calcula a propagação de incertezas da instância do objeto. A propagação utilizada é do tipo
		"raiz quadrada da soma do produto dos quadrados das derivadas parciais e dos quadrados das incertezas
		e utiliza como nome para cada incerteza "u_VARIAVEL".
		'''
		propagacao = sp.sympify('0')
		for var in self.__variaveis:
			propagacao += self.derivar(str(var))**2*self.__incertezas[var]**2

		self.__propagacao = sp.sqrt(propagacao)

	def gerar_funcao (self, variaveis_mantidas):
		'''Gera uma funcao que tem como argumentos as variaveis em variaveis_mantidas, e permite
		avaliar a funcao principal nos pontos escolhidos.
		'''
		variaveis = list()
		for var in variaveis_mantidas:
			variaveis.append(self._gerar_simbolo(var))

		self.funcao_gerada = sp.lambdify(variaveis, self.__funcao_substituida)

	def gerar_propagacao (self, variaveis_mantidas):
		'''Gera uma funcao que tem como argumentos as variaveis em variaveis_mantidas, e permite
		avaliar a propagacao nos pontos escolhidos.
		'''
		variaveis = list()
		for var in variaveis_mantidas:
			variaveis.append(self._gerar_simbolo(var))

		self.propagacao_gerada = sp.lambdify(variaveis, self.__propagacao_substituida)

	def integrar (self, var, limites=None, substituir=False):
		'''Permite integrar facilmente a função na variável "var" (que deve vir como string), e
		se o parâmetro "limites" for utilizado, retorna	a integral avaliada nesses pontos.
		'''
		self._gerar_simbolo(var)
		if limites is None:
			if substituir:
				return self.__funcao.integrate(self._ultimo_simbolo).subs(self.valores_conhecidos)
			else:
				return self.__funcao.integrate(self._ultimo_simbolo)
		else:
			if substituir:
				return self.__funcao.integrate((self._ultimo_simbolo, limites[0], limites[1])).subs(self.valores_conhecidos)
			else:
				return self.__funcao.integrate((self._ultimo_simbolo, limites[0], limites[1]))

	def derivar (self, var, ponto_avaliado=None, indice=1, substituir=False):
		'''Permite derivar facilmente a função na variável "var" (que deve vir como string), e
		se o parâmetro "ponto_avaliado" for configurado, avalia a função derivada naquele ponto.
		Se o parâmetro "indice" for utilizado, será calculada a derivada daquele grau
		'''
		if var is not str:
			self._ultimo_simbolo = var
		else:
			self._gerar_simbolo(var)

		if ponto_avaliado is None:
			if substituir:
				return self.__funcao.diff(self._ultimo_simbolo, indice).subs(self.valores_conhecidos)
			else:
				return self.__funcao.diff(self._ultimo_simbolo, indice)
		else:
			if substituir:
				return self.__funcao.diff(self._ultimo_simbolo, indice).subs(self._ultimo_simbolo, ponto_avaliado).subs(self.valores_conhecidos)
			else:
				return self.__funcao.diff(self._ultimo_simbolo, indice).subs(self._ultimo_simbolo, ponto_avaliado)		

	def _gerar_simbolo (self, var):
		'''Para permitir a interação com os símbolos internos do programa, é gerado um símbolo
		referente à "var" (que deve vir como string). Esse símbolo é guardado em "_ultimo_simbolo"
		para permitir que seja utilizado de maneira fácil
		'''
		self._ultimo_simbolo = sp.symbols(str(var))
		return self._ultimo_simbolo

	def __str__ (self):
		return str(self.__funcao)

	def __repr__ (self):
		return ('FisExp(\'' + str(self) + '\', ' + str(self.__valores_conhecidos) + ', ' + str(self.__incertezas_conhecidas) + ')')


if __name__ is "__main__":
	f = sp.sympify('x*a+b+c')
	f_a = FisExp(f)
	print ("Funcao: ", str(f_a))
	print ("Propagacao: ", f_a.propagacao)
	variaveis = {'a':4, 'b':3, 'x':2}
	asd = {'a':1, 'b':3, 'c':1, 'x':3}
	f_a.valores_conhecidos = variaveis
	f_a.incertezas_conhecidas = asd
	print ("Substituicao: ", f_a.funcao_substituida)
	f_a.funcao_substituida = 'bla'
	print("Teste de substituicao: ", f_a.funcao_substituida)
	variaveis1 = dict()
	f_a.valores_conhecidos = variaveis1
	f_a.valores_conhecidos = variaveis
	print("Teste de substituicao 2: ", f_a.funcao_substituida)
	print ('Propagacao substituida: ', f_a.propagacao_substituida)
	print ('Integral em x: ', f_a.integrar('x'))
	print ('Derivada em x: ', f_a.derivar('x'))
	f_a.gerar_funcao(['c'])
	f_a.gerar_propagacao(['c'])
	print ('Funcao gerada avaliada em c=5: ', f_a.funcao_gerada(5))
	print ('Propagacao gerada avaliada em c=5: ', f_a.propagacao_gerada(5))