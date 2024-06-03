# arith_eval
import random

class ArithEval:

	symbols = {}

	operators = {
		"+": lambda args: args[0] + args[1],
		"-": lambda args: args[0] - args[1],
		"*": lambda args: args[0] * args[1],
		"seq": lambda args: args[-1],
		"atribuicao": lambda args: ArithEval._attrib(args),
		"escrever": lambda args: print(args[0]),
		"number": lambda args: args[0],
  		"parametro_id": lambda args: args,
  		"parametro_number": lambda args: args,
  		"string": lambda args: args[0],
		"string_interpol": lambda args: ArithEval._interpol(args),
		"comentario": lambda args: None,
		"concat" : lambda args: f'{args[0]}{args[1]}',
		"entrada": lambda args: input(),
  		"aleatorio": lambda args: random.randint(0,args[0]),
	}

	@staticmethod
	def _attrib(args): # A=10   {'op':'atr'  args: [ "A", 10 ]} 
		value = args[1]
		ArithEval.symbols[args[0]] = value   # symbols['A'] = 10
		# print(f'var: {args[0]}, value: {value}')
		#return None
		return value
    
	@staticmethod
	def _interpol(args):
		str = ''
		for arg in args:
			str += arg
   
		return str
    
	@staticmethod
	def evaluate(ast):
		if type(ast) is int:  # constant value, eg in (int, str)
			return ast
		if type(ast) is dict: # { 'op': ... , 'args': ...}
			return ArithEval._eval_operator(ast)
		if type(ast) is str: 
			return ast
		raise Exception(f"Unknown AST type {ast}")
        
	@staticmethod
	def _eval_operator(ast):
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

