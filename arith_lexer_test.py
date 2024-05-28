# arith_lexer_test.py
from  fca_lexer import FCALexer

exemplos = [ # exemplos a avaliar de forma independente... 
            "ESCREVER(2+2+2); --GANDA REGEX COZINHADO NA HORA",
			"ESCREVER(2+2+2); {-e QUE FILHO\nGandas mamas-}"]

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
