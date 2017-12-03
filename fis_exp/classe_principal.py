import sympy as sp

class FisExp:

	def __init__ (self, funcao, valores_conhecidos={}):
		
		if type(funcao) is str:
			self.funcao = sp.sympify(funcao)
		else:
			self.funcao = funcao

		self.variaveis = self.funcao.atoms(sp.Symbol)
		self.incertezas = {}
		for simbolo in self.variaveis:
			incerteza = sp.symbols('u_' + str(simbolo))
			self.incertezas[simbolo] = incerteza

		self.funcao_substituida = self.funcao
		self.valores_conhecidos = dict()
		self.substituicao(valores_conhecidos)
		self._propagacao()

	def substituicao (self, valores_conhecidos):
		'''Gera o atributo funcao_substituida, que é a função com os valores conhecidos para algumas variáveis
		'''
		for var in valores_conhecidos.keys():
			self.valores_conhecidos[var] = valores_conhecidos[var]
			self.funcao_substituida = self.funcao.subs(self.valores_conhecidos)
		return self.funcao_substituida

	def _propagacao (self):
		'''Calcula a propagação de incertezas da instância do objeto. A propagação utilizada é do tipo
		"raiz quadrada da soma do produto dos quadrados das derivadas parciais e dos quadrados das incertezas
		e utiliza como nome para cada incerteza "u_VARIAVEL".
		'''
		propagacao = sp.sympify('0')
		for var in self.variaveis:
			propagacao += self.derivar(str(var))**2*self.incertezas[var]**2

		self.propagacao = sp.sqrt(propagacao)

	def integrar (self, var, limites=None):
		'''Permite integrar facilmente a função na variável "var" (que deve vir como string), e
		se o parâmetro "limites" for utilizado, retorna	a integral avaliada nesses pontos.
		'''
		self._gerar_simbolo(var)
		if limites is None:
			return self.funcao.integrate(self._ultimo_simbolo)
		else:
			return self.funcao.integrate((simboloelf._ultimo_simbolo, limites[0], limites[1]))

	def derivar (self, var, ponto_avaliado=None, indice=1):
		'''Permite derivar facilmente a função na variável "var" (que deve vir como string), e
		se o parâmetro "ponto_avaliado" for configurado, avalia a função derivada lá.
		Se o parâmetro "indice" for utilizado, será calculada a derivada daquele grau
		'''
		if var is not str:
			self._ultimo_simbolo = var
		else:
			self._gerar_simbolo(var)
		if ponto_avaliado is None:
			return self.funcao.diff(self._ultimo_simbolo, indice)
		else:
			return self.funcao.diff(self._ultimo_simbolo, indice).subs(self._ultimo_simbolo, ponto_avaliado)

	def _gerar_simbolo (self, var):
		'''Para permitir a interação com os símbolos internos do programa, é gerado um símbolo
		referente à "var" (que deve vir como string). Esse símbolo é guardado em "_ultimo_simbolo"
		para permitir que seja utilizado de maneira fácil
		'''
		self._ultimo_simbolo = sp.symbols(str(var))
		return self._ultimo_simbolo

	def __str__ (self):
		return str(self.funcao)

'''def gerarSimbolos (lista, dict):
	exec ('import sympy as sp')
	for simbolo in lista.split():
		exec( simbolo + ' = ' + 'sp.symbols("' + simbolo + '")' )''' 
#ideia a ser implementada

if __name__ is "__main__":
	f = sp.sympify('a+b+c')
	f_a = FisExp(f)
	print ("Funcao: ", f_a.funcao)
	print ("Propagacao: ", f_a.propagacao)
	variaveis = {'a':4}
	print ("Substituicao: ", f_a.substituicao(variaveis))