
# Verificação de regras de codificação estabelecidas pelo documento DTN-01 
(https://docs.google.com/document/d/1B17T78DMXWCESnl8y0y1-Cv1gIGTGAtjOt49rCkBAzw/edit)

A codificação de verificação: Linguagem Python

## Estrutura de arquivos:

* code_under_test - codigos fortran para análises

* src - códigos em python de verificação (QA.py)

* xml - arquivos .xml gerados pelo parser   

## Uso do parser (open_fortran_parser), para gerar arquivo .xml 

    $cd  src 
    $python3 -m open_fortran_parser ../code_under_test/teste.F90 ../xml/saida.xml


## Instalação open-fortran-parser

    $pip install open-fortran-parser

https://pypi.org/project/open-fortran-parser/
