# arith_eval
import random

class ArithEval:

	symbols = {}
	funcoes = {}

	operators = {
		"+": lambda args: args[0] + args[1],
		"-": lambda args: args[0] - args[1],
		"*": lambda args: args[0] * args[1],
		"seq": lambda args: args[-1],
		"atribuicao": lambda args: ArithEval._attrib(args),
		"escrever": lambda args: print(args[0]),
		"number": lambda args: args[0],
		"parametro_id": lambda args: args[0],
		"parametro_number": lambda args: args[0],
		"string": lambda args: args[0],
		"string_interpol": lambda args: ArithEval._interpol(args),
		"comentario": lambda args: None,
		"concat": lambda args: f'{args[0]}{args[1]}',
		"entrada": lambda args: input(),
		"aleatorio": lambda args: random.randint(0,args[0]),
		"expressao_funcao": lambda args: args,
		"expressao_array": lambda args: args,
		"array": lambda args: ArithEval._array(args),
		"map": lambda args: ArithEval._map_array(args),
		"fold": lambda args: ArithEval._fold_array(args),
		"chama_funcao": lambda args: ArithEval._chama_funcao(args),
	}

	@staticmethod
	def _attrib(args):
		value = args[1]
		ArithEval.symbols[args[0]] = value   # symbols['A'] = 10
		# print(f'var: {args[0]}, value: {value}')
		return value

	@staticmethod
	def _interpol(args):
		str = ''
		for arg in args:
			str += arg
		return str

	@staticmethod
	def _array(args):
		if len(args) == 0:
			return []
		else:
			return args[0]

	@staticmethod
	def _map_array(args):
		func = args[0]
		array = args[1]
		result = []
		# Fazer loop aos elementos
		for element in array:
			func_result = ArithEval._chama_funcao([func, [element]])
			result.append(func_result)

		return result

	@staticmethod
	def _fold_array(args):
		func = args[0]
		array = args[1]
		number = args[2]
		array.append(number)
		is_first = True
		for element in reversed(array):
			if is_first:
				func_result = ArithEval._chama_funcao([func, [element, number]])
				is_first = False
			func_result = ArithEval._chama_funcao([func, [element, func_result]])

		print(f'result_fold: {func_result}')
		return func_result

	@staticmethod
	def _funcao(args):
		nome = args[0]
		parametro = args[1]
		conteudo = args[2]

		if nome not in ArithEval.funcoes:
			ArithEval.funcoes[nome] = []

		ArithEval.funcoes[nome].append({'parametro': parametro, 'conteudo': conteudo})

		return nome

	@staticmethod
	def _chama_funcao(args):
		funcao = args[0]
		parametros = args[1]

		if funcao not in ArithEval.funcoes:
			raise Exception(f"error: function '{funcao}' not assigned")

		param_valido = False

		temp_scope = ArithEval.symbols.copy()

		funcao_scope = ArithEval.symbols.copy()

		#Funcoes com multiplos nomes e parametros
		for funcao_item in ArithEval.funcoes[funcao]:
			if len(parametros) != len(funcao_item['parametro']):
				continue
				
			for_valid = True
				
			for parametro, valor in zip(funcao_item['parametro'], parametros):
				print(f'parametro: {parametro} , valor: {valor} \n')
				if 'var' in parametro:
					funcao_scope[parametro['var']] = ArithEval.evaluate(valor)
				if 'op' in parametro:
					if 'number' in parametro['op'] and valor not in parametro['args']:
						for_valid = False
						continue
			
			if for_valid == False:
				continue
			#if param_valido == False:
			#	raise Exception(f"error: no function {funcao} incorrect parameters")

			ArithEval.symbols = funcao_scope
   
			result = ArithEval.evaluate(funcao_item['conteudo'])
   
			ArithEval.symbols = temp_scope
   
			return result

	@staticmethod
	def evaluate(ast):
		if type(ast) is int:  # constant value, eg in (int, str)
			return ast
		if type(ast) is dict:  # { 'op': ... , 'args': ...}
			return ArithEval._eval_operator(ast)
		if type(ast) is str: 
			return ast
		if type(ast) is list:
			result = []
			for item in ast:
				result.append(ArithEval._eval_operator(item))
			return result
		raise Exception(f"Unknown AST type {ast}")

	@staticmethod
	def _eval_operator(ast):
		if 'op' in ast and ast['op'] == 'funcao':
			return ArithEval._funcao(ast['args'])

		if 'op' in ast:
			op = ast["op"]
			args = [ArithEval.evaluate(a) for a in ast['args']]
			if op in ArithEval.operators:
				func = ArithEval.operators[op]
				return func(args)
			else:
				raise Exception(f"Unknown operator {op}")

		if 'var' in ast:
			varid = ast["var"]
			if varid in ArithEval.symbols:
				return ArithEval.symbols[varid]
			raise Exception(f"error: local variable '{varid}' referenced before assignment") 
			#

		raise Exception('Undefined AST')