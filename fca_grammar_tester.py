# arith.py
from fca_grammar import ArithGrammar
from pprint import PrettyPrinter
import json
 
pp = PrettyPrinter(sort_dicts=False)
 
teste = ArithGrammar()
teste.build()
 
exemplos = [ # exemplos a avaliar de forma independente...
            # 'ESCREVER("ola mundo!");',
            # 'ESCREVER(a+b);',
            # 'ESCREVER(ab_teste_23);',
            # 'ESCREVER(2+5);',
            # 'ESCREVER(a<>b);',
            # 'ESCREVER(a<>"abaaaaa");',
            # 'ESCREVER("PL " <> 2 <> "o ano de" <> "ESI");',
            # 'ESCREVER(2+2+2);',
            # 'vat_rest = 1234;',
            # 'vat_rest = "Ola teste";',
            # 'vat_rest = 2 * 2;',
            # 'vat_rest = lv_vr_teste;',
            # 'vat_rest = "ola1" <> "ola";',
            # 'vat_rest = "ola1" <> lt_Tb_regup;',
            # 'vat_rest = lt_Tb_mara <> lt_Tb_mhnd;',
            # 'ESCREVER(2+2+2); --GANDA REGEX COZINHADO NA HORA',
			# 'ESCREVER(2+2+2); {-e QUE FILHO\nGandas mamas-}',
            # 'ESCREVER("soma de " <> 9 <> "com " <> 3*4 <> "=" <> 9+2*3);',
            # 'FUNCAO teste(a): a+b;',
            # 'FUNCAO teste(a,b,12),: a+b;',
            # 'ESCREVER ("Ola, #{escola} #{inst}!");',
            # 'ESCREVER ("#{escola} #{inst}!");',
            # 'var_rest = ENTRADA() ;',
            # 'var_rest342 = ALEATORIO(13);',
            # 'FUNCAO soma2(c, b) :\nc = c+1 ;\nc+1 ;\nFIM',
            # "ESCREVER(valor);   -- conteúdo de valor é apresentado",
            # 'nome="diogo", idade=10;',
            # "FUNCAO soma(a,b) ,: a+b ;\nFUNCAO soma2(c) :\nc = c+1 ;\nc+1 ;\nFIM\nseis = soma(4,2);\noito = soma2(seis);",
            # "ESCREVER(\"Ola, \"<> curso); -- Ola, ESI",
            # "{- exemplo interpolação de strings\nOlá, EST IPCA! -}\nescola =\"EST\";\ninst = \"IPCA\";\nESCREVER (\"Olá, #{escola} #{inst}!\");",
            # "FUNCAO area(a,b),: a*b ;\nFUNCAO area(c),: area(c, c);\nd = area(10, 20);\ne = area(30);",
            # "FUNCAO fib( 0 ),: 0 ;\nFUNCAO fib( 1 ),: 0 ;\nFUNCAO fib( n ):\na = fib(n-1);\nb = fib(n-2);\na + b;\nFIM\nfib5 = fib(5);",
            # "lista = [ 1, 2, 3 ] ;\nESCREVER( lista ); -- [1,2,3];\nvazia = [] ;\nlista_str = [\"teste\"]",
            # "FUNCAO mais2( x ),: x + 2 ;\nFUNCAO soma( a, b ),: a + b ;\nlista1 = map( mais2, [] );\nlista2 = map( mais2, [ 1, 2, 3 ] );\nlista3 = fold( soma, [ 1, 2, 3 ], 0 );",
            "array = map(soma2,[1, 2, 3]);",
            # "FUNCAO somatorio( [] ),: 0 ;FUNCAO somatorio( x:xs[] ),: x + somatorio(xs) ;",
            ]
outputs = {}
for frase in exemplos:
    print(f"----------------------")
    print(f"--- frase '{frase}'")
    resposta = teste.parse( frase )
    print("resultado: ")
    pp.pprint(resposta)
    outputs[frase] = resposta  # Store the output in a dictionary using the phrase as a key

    # Writing the outputs to a JSON file
    with open('output.json', 'w') as json_file:
        json.dump(outputs, json_file, indent=4)