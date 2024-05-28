# arith_lexer_test.py
from  fca_lexer import FCALexer

exemplos = [ # exemplos a avaliar de forma independente... 
            "ESCREVER(valor);",
			"ESCREVER(365 * 2); ",
			"ESCREVER(\"Ola Mundo\"); ",
			"curso = \"ESI\";",
			"ESCREVER(\"Olá, \" <> curso);",
			"FUNCAO soma(a,b): a+b ;"]

for frase in exemplos:
	print(f"----------------------")
	print(f"frase: '{frase}'")
	al = FCALexer()
	al.build()
	al.input(frase)
	print('tokens: ',end="")
	while True:
		tk = al.token() 
		if not tk: 
			break
		print(tk,end="")
	print()	
