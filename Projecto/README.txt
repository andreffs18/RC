RC 2015
Projecto "Online Questionnaire"

Nº 75455 - André Silva
Nº 75787 - Zé Diogo Oliveira
Nº 75966 - Frederico Moura

Visto que o projecto está em Python, nao é convencional criar uma makefile, entao, de forma a correr o user.py, tes.py e ecp.py apenas tem de ser executado o seguinte comando para cada ficheiro:

$ python <nome_do_ficheiro>.py [commandos]

ou seja, testando cada ficheiro em separadores do terminal diferentes usariamos:

[Terminal1] $ python user.py SID [-n ECPname] [-p ECPport]
[Terminal2] $ python ecp.py [-p ECPport]
[Terminal3] $ python tes.py [-p TESport] [-n ECPname] [-e ECPport]
