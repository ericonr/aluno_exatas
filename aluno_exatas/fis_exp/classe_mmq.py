import enum
import numpy as np

class SizeError (Exception):
	'''Classe para exceção relacionada a erros de tamanho de vetores
	'''
	pass

class Incertezas (enum.Enum):
	iguais = enum.auto()
	variaveis = enum.auto()

class CoefLinear (enum.Enum):
	com = enum.auto()
	sem = enum.auto()

class MMQ:
	def __init__ (self, incertezas=Incertezas.iguais, coef_linear=CoefLinear.com):
		'''Classe para automatizar o processo de calcular MMQs para funções lineares, da
		forma y = a + bx
		'''
		self.__incertezas = incertezas
		self.__coef_linear = coef_linear

		self.__x = np.ndarray((0))
		self.__y = np.ndarray((0))
		self.__incertezas_y = np.ndarray((0))

	def __exception_type (self, numero):
		if numero is 1:
			raise TypeError('Deve ser numpy.ndarray ou list')
		if numero is 2:
			raise SizeError('Os vetores x_value e y_value devem ter o mesmo tamanho')
		if numero is 3:
			raise SizeError('Os vetores x_value, y_value e incertezas_y devem ter o mesmo tamanho')

	@property
	def x_values (self):
		return self.__x
	@x_values.setter
	def x_values (self, x_values):
		'''Garante que os valores são do tipo correto
		'''
		if type(x_values) is list:
			self.__x = np.array(x_values)
		elif type(x_values) is np.ndarray:
			self.__x = x_values
		else:
			self.__exception_type(1)

	@property
	def y_values (self):
		return self.__y
	@y_values.setter
	def y_values (self, y_values):
		if type(y_values) is list:
			self.__y = np.array(y_values)
		elif type(y_values) is np.ndarray:
			self.__y = y_values
		else:
			self.__exception_type(1)

	@property
	def incertezas_y (self):
		return self.__incertezas_y
	@incertezas_y.setter
	def incertezas_y (self, incertezas_y):
		if self.__incertezas is Incertezas.variaveis:
			if type(incertezas_y) is list:
				self.__incertezas_y = np.array(incertezas_y)
			elif type(incertezas_y) is np.ndarray:
				self.__incertezas_y
			else:
				self.__exception_type(1)
		elif self.__incertezas is Incertezas.iguais:
			self.__incertezas_y = incertezas_y

	def coeficientes (self):
		'''Propriedade que calcula os coeficientes, e os retorna, juntamente com as incertezas.
		Vem no formato [a,b], onde y = a + b*x
		(isso permite que seja facilmente utilizado no módulo numpy.polynomials.polynomials)
		'''
		coef = np.ndarray((2))
		incert = np.ndarray((2))

		if self.__incertezas is Incertezas.iguais and self.__coef_linear is CoefLinear.sem:
			pass
		elif self.__incertezas is Incertezas.iguais:
			if self.__x.size is not self.__y.size:
				self.__exception_type(2)

			N = self.__x.size
			sx = self.__x.sum()
			sy = self.__y.sum()
			sxy = (self.__x * self.__y).sum()
			sx2 = (self.__x **2).sum()
			delta = N * sx2 - sx**2
			
			coef[0] = (sy*sx2-sxy*sx)/delta
			coef[1] = (N*sxy-sx*sy)/delta

			incert[0] = (np.sqrt(sx2/delta))*self.__incertezas_y
			incert[1] = (np.sqrt(N/delta))*self.__incertezas_y

		elif self.__incertezas is Incertezas.variaveis:
			if self.__x.size is not self.__y.size or self.__x.size is not self.__incertezas_y.size:
				self.__exception_type(3)

			w = 1 / self.__incertezas_y
			sw = w.sum()
			swx = (w * self.__x).sum()
			swy = (w * self.__y).sum()
			swx2 = (w * self.__x **2).sum()
			swxy = (w * self.__x * self.__y).sum()
			delta = delta = sw*swx2 - swx**2

			coef[0] = (swy*swx2 - swxy*swx) / delta
			coef[1] = (sw*swxy - swx*swy) / delta

			incert[0] = swx2 / delta
			incert[1] = sw / delta

		return coef, incert