import xml.etree.ElementTree as ET
#import open_fortran_parser

def is_pascal_case(word):
   if not word:
       return False
   if not word[0].isalpha():
       return False
   if not word[0].isupper():
       return False
   if word[1].isupper():
       return False
   for char in word[2:]:
       if not char.isalpha() and not char.isdigit():
           return False
   return True

def is_camel_case(word):
   if not word:
       return False
   if not word[0].isalpha():
       return False
   if word[0].isupper():
       return False
   for char in word[1:]:
       if not char.isalpha() and not char.isdigit():
           return False
   return True#

def is_snake_case(word):
   if not word:
       return False
   if not word[0].isalpha():
       return False
   for char in word[0:]:
       if not char.isalpha() and not char.isdigit() and not char=="_":
           return False
   for char in word[0:]:
       if char.isupper():
           return False
   return True#

def is_upper_snake_case(word):
   if not word:
       return False
   if not word[0].isalpha():
       return False
   for char in word[0:]:
       if not char.isalpha() and not char.isdigit() and not char=="_":
           return False
   for char in word[0:]:
       if char.islower():
           return False
   return True#

if __name__ == '__main__':

   # read the files and get fields
   tree = ET.parse('./xml/saida.xml')
   root = tree.getroot() # Pega a raiz do xml

   for file in root.iter("file"): #Pega o nome e caminho do arquivo fonte
      file_name = file.get("path")
   
   #Abre e lê o arquivo fonte
   fn = open(file_name,"r")
   lines = fn.readlines()
   lines_work = []
   c_lines_work = []

   comments = {}
   line = []
   begin = []

   # Cria um dicionário com a posição de comentários
   for com in root.iter("comment"):
      line.append(int(com.get("line_begin"))-1)
      begin.append(int(com.get("col_begin")))
   comments.update({"line":line,"col_begin":begin,})

   # Percorre as linhas de entrada e reescreve retirando os comentários
   for line in range(len(lines)):
      try:
         ndx = comments.get("line").index(line)
      except:
         lines_work.append(lines[line])
         continue
      lines_work.append(lines[line][0:comments.get("col_begin")[ndx]])

   c_comments = {}
   c_line = []
   c_begin = []
   c_end = []

   # Cria um dicionário com a posição de Literais char
   for clc in root.iter("char-literal-constant"):
      c_line.append(int(clc.get("line_begin"))-1)
      c_begin.append(int(clc.get("col_begin")))
      c_end.append(int(clc.get("col_end")))
   c_comments.update({"line":c_line,"col_begin":c_begin,"col_end":c_end})

   # Percorre as linhas de line_work e reescreve em c_line_work retirando os literais char
   for line in range(len(lines_work)):
      try:
         ndx = c_comments.get("line").index(line)
      except:
         c_lines_work.append(lines_work[line])
         continue
      #Copia a parte que está fora dos literais
      new_line = lines_work[line][0:c_comments.get("col_begin")[ndx]+1]+lines_work[line][c_comments.get("col_end")[ndx]-1:]
      c_lines_work.append(new_line)

   #Cria um dicionário com as linhas de atribuição
   assignments = {}
   a_line = []
   a_begin = []
   a_end = []

   #Cria uma lista com todas as linhas que tem atribuição
   for ass in root.iter("assignment"):
      a_line.append(int(ass.get("line_begin")))
      a_begin.append(int(ass.get("col_begin")))
      a_end.append(int(ass.get("col_end")))
   assignments.update({"line":a_line,"col_begin":a_begin,"col_end":a_end})

   #Tabela de palavras reservadas
   keywords = [ "abstract", "allocatable", "allocate", "assign", "associate", "asynchronous", "backspace,bind", 
               "block", "block data", "call", "case", "class", "close", "codimension", "common", "concurrent", 
               "contains", "contiguous", "continue", "critical", "cycle", "data", "deallocate", "deferred", 
               "dimension", "do", "elemental", "else", "elseif", "elsewhere", "end", "endfile", "endif", "entry", 
               "enum", "enumerator", "equivalence", "error", "exit", "extends", "external", "final", "flush", 
               "forall", "format", "function", "generic", "goto", "if", "implicit ", "import", "include ", "inquire", 
               "intent", "interface", "intrinsic", "lock", "memory", "module ", "namelist", "non_overridable", "nopass", 
               "nullify", "only", "open", "operator", "optional", "parameter", "pass", "pause", "pointer", "print", 
               "private", "procedure", "program", "protected", "public", "pure", "read", "recursive", "result", 
               "return", "rewind", "rewrite", "save", "select", "sequence", "stop", "submodule", "subroutine", 
               "sync", "sync all", "sync images", "target", "then", "unlock", "use ", "value", "volatile", "wait", 
               "where", "while", "write", "end do", "end if"]

   #Inicio do processo com a análise das subrotinas
   #Percorre a árvore para as declarações de subrotina
   for sub in root.iter("subroutine"):
      print("\n\nInspecionando a subrotina",sub.get("name"))
      print("---------------------------------------------------------")
      print("subroutine lines = ",int(sub.get("line_end"))-int(sub.get("line_begin")))
      print("---------------------------------------------------------")      

      points = 0.0

      #Verifica a primeira Rule de nome
      if not is_camel_case(sub.get("name")): #4.8 camelCase
         print("Rule 4.8 : camelCase : Linhas",sub.get("line_begin"), sub.get("line_end"))
         points = points + 1.0

      arguments = []
      intent_list = []
      #Inspeciona o header da subrotina
      for elem in sub.iter("header"):
         #Inspeciona os argumentos de chamada
         for args in elem.iter("arguments"):
            #Inspeciona o nome dos argumentos dentro das Rules
            for arg in args.iter("argument"):
               if type(arg.get("name")) != str: #Previne da leitura de não strings
                  continue

               # Prrenche a lista de argumentos de chamada da subrotina
               arguments.append(arg.get("name"))

               #Verifica a Rule de nome de variável e a Rule de nomes curtos
               if not is_snake_case(arg.get("name")): #4.7 snake_case
                  print("Rule 4.7 : snake_case : Linha",arg.get("line_begin"),arg.get("name"))
                  points = points + 1.0
      
      #Inspeciona o corpo da subrotina
      has_implicit = False
      has_use = False
      has_only = False
      for elem in sub.iter("body"):
         ##### Falta olhar os comentários
         for spc in elem.iter("specification"):
            for dec in spc.iter("declaration"):

               #Verificação da declaração de implicit
               for ist in dec.iter("implicit-stmt"): 
                  has_implicit = True #Informa que a declaração de implicit foi encontrada
                  #Verifica a Rule de implicit none obrigatório
                  if not ist.get("implicitKeyword")=="implicit" and not ist.get("noneKeyword")=="none": #4.28 - sem implicit
                     print("Rule 4.28 : no implicit : Linhas",spc.get("line_begin"),spc.get("line_end"))
                     points = points + 0.5

               #Verifica quais as linhas com delacaração de parameter
               #Guarda na lista lines_with_parameter
               lines_with_parameter = []
               for atp in dec.iter("attribute-parameter"):
                  lines_with_parameter.append(atp.get("line_begin"))

               for itt in dec.iter("intent"):
                  intent = itt.get("type")
                  itt_line_begin = itt.get("line_begin")
                  itt_line_end = itt.get("line_end")
                  intent_list.append(itt_line_begin)

               for vars in dec.iter("variables"):
                  for var in vars.iter("variable"):
                     if type(var.get("name")) != str: #Previne da leitura de não strings
                        continue
                     #Dados da variável: nome, linha
                     var_name = var.get("name")
                     line_begin = var.get("line_begin")
                     line_end = var.get("line_end")
                     # Se a variavel é inicializada
                     if var.get("hasInitialValue") == "true":
                        # E se ela não está em uma linha de parameter aplica a Rule 4.30
                        if not line_begin in lines_with_parameter:
                           print("Rule 4.30 : Initialized : Linhas",line_begin,line_end,var_name)
                           points = points + 1.0
                        else: #Ela está em uma linha de parameter verificar se o nome está adequado 4.12.1
                           if var_name[0:2] != "p_" and var_name[0:2] != "c_":
                              print(var_name[0:2])
                              print("Rule 4.12 : no prefix : Linhas",line_begin,line_end,var_name)
                              points = points + 1.0
                  
                     #Verifica a Rule de nome de variável e a Rule de nomes curtos
                     if not is_snake_case(var_name): #4.7 snake_case
                        print("Rule 4.7 : snake_case : Linha",line_begin,var_name)
                        points = points + 1.0
                     if len(var_name)<2:
                        print("Rule 5.18 : short name : Linha",line_begin,var_name)
                        points = points + 0.5
                     if var_name in keywords:
                        print("Rule 4.7.1 : reserved : Linha",line_begin,var_name)
                        points = points + 1.0

                     #Verifica se a variável é um argumento e se ela está com intent
                     if var_name in arguments:
                        if not line_begin in intent_list:
                           print("Rule 4.10 : intent : Linha",line_begin,var_name)
                           points = points + 1.0

                     #Verifica a declaração para verificar se ela é assumed-shape
                     for dis in var.iter("dimensions"):
                        for dim in dis.iter("dimension"):
                           if not dim.get("type")=="assumed-shape" and var_name in arguments:
                              print("Rule 4.27 : assumed : Linha",line_begin,var_name)
                              points = points + 1.0

         # Verifica o tamanho dos laços do - end do
         for loo in elem.iter("loop"):
            line_begin = loo.get("line_begin")
            line_end = loo.get("line_end")
            loop_size = int(line_end)-int(line_begin)+1
            if loop_size > 50:
               print("Rule 5.25 : loop size : ", loop_size, "Linha",line_begin,line_end)
               points = points + 0.5

         # Verifica o tamanho dos ifs - end if
         for ifs in elem.iter("if"):
            line_begin = ifs.get("line_begin")
            line_end = ifs.get("line_end")
            if_size = int(line_end)-int(line_begin)+1
            if if_size > 50:
               print("Rule 5.40 : if size : ", if_size, "Linha",line_begin,line_end)
               points = points + 0.5

         #Verificação de use em subrotinas
         for use in spc.iter("use"):
            has_use = True
            for onl in use.iter("only"):
               has_only = True

      if not has_implicit: #SE não encontrou a declaração de implicit
         print("Rule 4.28 : no implicit : Linhas",spc.get("line_begin"),spc.get("line_end"),sub.get("name"))
         points = points + 0.5

      if has_use:
         print("Rule 4.42 : has use : Linhas",spc.get("line_begin"),spc.get("line_end"),sub.get("name"))
         points = points + 1.0
         if not has_only:
            print("Rule 4.42.1 : no only : Linhas",spc.get("line_begin"),spc.get("line_end"),sub.get("name"))
            points = points + 1.0

      for i in range(int(sub.get("line_begin")), int(sub.get("line_end"))):
         # Verifica a Rule de espaços nas atribuições dentro da subrotina
         #Procura por um espaço na linha do código
         try:
            ndx = assignments.get("line").index(i)
         except:
            continue
         # Procura pelo sinal de igual apenas nas colunas de atribuição
         sub_linha = c_lines_work[i-1][assignments.get("col_begin")[ndx]:assignments.get("col_end")[ndx]]
         pos = sub_linha.find("=")
         if(pos > -1):
            #Verifica se tem espaço antes e depois quando for uma atribuição
            if sub_linha[pos-1] != " " or sub_linha[pos+1] != " ":
               print("Rule 4.58 : no space : Linha",i,c_lines_work[i-1])
               points = points + 1

      #Essa parte precisa ser substituida por algo mais eficiente e certo. 
      #Deveria usar os statments do parser
      for i in range(int(sub.get("line_begin")), int(sub.get("line_end"))):
         line_normal = c_lines_work[i-1]
         line_lower = c_lines_work[i-1].lower()
         for res in keywords:
            pos = line_lower.find(res)
            if pos<0:
               continue
            source_keyword = line_normal[pos:pos+len(res)]
            if res != source_keyword:
               print("Rule 4.5 : keyword Case : Linha",i)
               points = points + 1
            

#<type-declaration-stmt col_begin="68" col_end="69" eos="&#10;" line_begin="96" line_end="96" numAttributes="1" rule="501"/>
#<use-stmt col_begin="3" col_end="168" eos="&#10;" hasModuleNature="false" hasOnly="true" hasRenameList="false" id="modGate" line_begin="57" line_end="57" onlyKeyword="only" rule="1109" useKeyword="use"/>
#<access-spec col_begin="3" col_end="10" keyword="private" line_begin="69" line_end="69" rule="508" type="804"/>
#<type-declaration-stmt col_begin="68" col_end="69" eos="&#10;" line_begin="96" line_end="96" numAttributes="1" rule="501"/>
#<derived-type-stmt col_begin="3" col_end="20" eos="&#10;" hasGenericNameList="false" hasTypeAttrSpecList="false" id="t_hcts_vars" keyword="type" line_begin="388" line_end="388" rule="430"/>
#<data-component-def-stmt col_begin="17" col_end="18" eos="&#10;" hasSpec="false" line_begin="391" line_end="391" rule="440"/>
#<contains-stmt col_begin="0" col_end="9" eos="&#10;" keyword="contains" line_begin="405" line_end="405" rule="1237"/>
#<subroutine-stmt col_begin="3" col_end="3470" eos="&#10;" hasArgSpecifier="true" hasBindingSpec="false" hasDummyArgList="true" hasPrefix="false" keyword="subroutine" line_begin="408" line_end="408" name="mo
#<if-stmt col_begin="6" col_end="8" ifKeyword="if" line_begin="699" line_end="699" rule="807"/>
#<do-stmt col_begin="6" col_end="22" digitString="" doKeyword="do" eos="&#10;" hasLoopControl="true" id="" line_begin="702" line_end="702" rule="827"/>
#<end-do-stmt col_begin="9" col_end="16" doKeyword="do" endKeyword="end" eos="&#10;" id="" line_begin="726" line_end="726" rule="834"/>
#<if-then-stmt col_begin="9" col_end="30" eos="&#10;" id="" ifKeyword="if" line_begin="731" line_end="731" rule="803" thenKeyword="then"/>
#<stop-stmt col_begin="32" col_end="74" eos="&#10;" hasStopCode="true" line_begin="732" line_end="732" rule="849" stopKeyword="stop"/>
#<cycle-stmt col_begin="63" col_end="69" cycleKeyword="cycle" do-construct-name="" eos="&#10;" line_begin="784" line_end="784" rule="843"/>
# <call-stmt callKeyword="call" col_begin="12" col_end="3965" eos="&#10;" hasActualArgSpecList="false" line_begin="1018" line_end="1018" rule="1218"/>
#<exit-stmt col_begin="12" col_end="17" do-construct-name="" eos="&#10;" exitKeyword="exit" line_begin="5111" line_end="5111" rule="844"/>
#<continue-stmt col_begin="0" col_end="12" continueKeyword="continue" eos="&#10;" label="30" line_begin="47" line_end="47" rule="848"/>
#<goto-stmt col_begin="6" col_end="14" eos="&#10;" goKeyword="goto" line_begin="45" line_end="45" rule="845" target_label="30" toKeyword=""/>
#<select-case-stmt caseKeyword="case" col_begin="3" col_end="19" eos="&#10;" id="" line_begin="54" line_end="54" rule="809" selectKeyword="select"/>
#<case-stmt caseKeyword="case" col_begin="3" col_end="16" eos="&#10;" id="" line_begin="59" line_end="59" rule="810"/>
#<print-stmt col_begin="6" col_end="19" eos="&#10;" hasOutputItemList="true" line_begin="56" line_end="56" printKeyword="print" rule="912"/>
#<end-select-stmt col_begin="3" col_end="14" endKeyword="end" eos="&#10;" id="" line_begin="61" line_end="61" rule="811" selectKeyword="select"/>
#<open-stmt col_begin="3" col_end="63" eos="&#10;" line_begin="39" line_end="39" openKeyword="open" rule="904"/>
#<close-stmt closeKeyword="close" col_begin="3" col_end="18" eos="&#10;" line_begin="43" line_end="43" rule="908"/>
#<write-stmt col_begin="3" col_end="23" eos="&#10;" hasOutputItemList="true" line_begin="41" line_end="41" rule="911" writeKeyword="write"/>
      print("Penalties in subroutine: ", points)


   

