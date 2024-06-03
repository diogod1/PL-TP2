# arith.py
from fca_grammar import ArithGrammar
from fca_eval import ArithEval
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(sort_dicts=False)

lg = ArithGrammar()
lg.build()


if len(sys.argv) == 2:
	with open(sys.argv[1], "r") as file:
		contents = file.read()
		try:
			tree = lg.parse(contents)
			pp.pprint(tree)
			resultado = ArithEval.evaluate(tree)
			print(f"<< {resultado}")
		except Exception as e:
			print(e, file=sys.stderr)
else:
	for expr in iter(lambda: input(">> "), ""):
		try:
			ast = lg.parse(expr)
			resultado = ArithEval.evaluate(ast)
			#if res is not None:
			print(f"<< {resultado}")
		except Exception as e:
			print(e)