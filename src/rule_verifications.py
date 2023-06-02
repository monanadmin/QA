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
   return True


def is_snake_case(word):
   if not word:
      return False
   if not word[0].isalpha():
      return False
    
   for char in word[0:]:
      if not char.isalpha() and not char.isdigit() and not char == "_":
         return False
   for char in word[0:]:
      if char.isupper():
         return False
   return True


def is_upper_snake_case(word):
   if not word:
      return False
   if not word[0].isalpha():
      return False
    
   for char in word[0:]:
      if not char.isalpha() and not char.isdigit() and not char == "_":
         return False
   for char in word[0:]:
      if char.islower():
         return False
   return True

def find_file_name(full_file_name):
   list_names = full_file_name.split("/")
   for lst in list_names:
      if lst.find(".F90") != -1:
         file_name = lst 
      elif lst.find(".f90") != -1:
         file_name = lst
   return file_name


def search_comments(sub):
   comments = {}
   line = []
   begin = []
   text_comment = []  

   # Cria um dicionário com a posição de comentários
   for com in sub.iter("comment"):
      line.append(int(com.get("line_begin")))
      begin.append(int(com.get("col_begin")))
      text_comment.append(com.get("text")) # adiciona a string dos comentários
   comments.update({"line":line, "col_begin":begin, "txt_comment":text_comment})
   return comments


def search_keywords(sub, keywords):
   used_keywords={}
   line = []
   col = []
   txt_key = []
       
   for key in keywords:
      if key != None:
         [str_keyword_prefix, key_stmt, str_keyword] = switch(key)
         for stmt in sub.iter(key_stmt + "-stmt"):
            line.append(int(stmt.get("line_begin")))
            col.append(int(stmt.get("col_begin")))
            txt_key.append(stmt.get(str_keyword_prefix + str_keyword))
#            print("UsedKeys:", stmt.get(str_keyword_prefix + str_keyword),"line:",stmt.get("line_begin"))
#            if stmt.get(str_keyword_prefix + str_keyword) == "enddo" or stmt.get(str_keyword_prefix + str_keyword) == "endif":
#               print ("Rule 4.26 : collapsed form", stmt.get(str_keyword_prefix + str_keyword) , ", line ", stmt.get("line_begin"))
               #points = points + 1.0
   
   used_keywords.update({"line":line, "col_begin":col, "keyword":txt_key})
   return used_keywords


def switch (key):
   if key == "goto":
            str_keyword_prefix = "go"
            key_stmt = key
            str_keyword = "Keyword"
   elif  key == "subroutine":
            str_keyword_prefix = ""
            key_stmt = key
            str_keyword= "keyword"
   elif  key == "if":
            str_keyword_prefix = "if"
            key_stmt = "if-then"
            str_keyword = "Keyword"
   elif  key == "end if":
            str_keyword_prefix = "end"
            key_stmt = "end-if"
            str_keyword = "Keyword"
   #elif  key == "endif":
   #         str_keyword_prefix = "end"
   #         key_stmt = "end-if"
   #         str_keyword = "Keyword"
   elif  key == "select":
            str_keyword_prefix = key
            key_stmt = "select-case"
            str_keyword = "Keyword"            
   elif  key == "end select":
            str_keyword_prefix = "end"
            key_stmt = "end-select"
            str_keyword = "Keyword"
   elif  key == "end module":
            str_keyword_prefix = "end"
            key_stmt = "end-module"
            str_keyword = "Keyword"
   elif  key == "end do":
            key_stmt = "end-do"
            str_keyword_prefix = "end"
            str_keyword = "Keyword"
   elif  key == "enddo":
            key_stmt = "end-do"
            str_keyword_prefix = "end"
            str_keyword = "Keyword"
   elif  key == "end subroutine":
            str_keyword_prefix = ""
            key_stmt = "end-subroutine"
            str_keyword = "keyword1"
            #str_keyword = "keyword2" #subroutine
   else:
            key_stmt = key
            str_keyword_prefix = key
            str_keyword = "Keyword"  
   return [str_keyword_prefix, key_stmt, str_keyword]


def verify_file_name (points, file_name):
   if file_name.find(".F90") == -1:
      print("Rule XXX file extention - .F90")  #verificar regra
      points = points
   return(points)


def case_keywords(sub, keywords, points):       
   used_keywords = search_keywords(sub, keywords)

   for kwd in used_keywords.get("keyword"):
      if kwd != None:
         if kwd.isupper():
            line_kwd = element_dictionary(used_keywords, "keyword", "line", kwd)
            print ("Rule 4.5 : keyword Case", kwd, ", line ", line_kwd)
            points = points + 1.0    
   return points         
 
 
def element_dictionary(dictionary, name_col_base, name_col, element):
   element_dict =  dictionary.get(name_col)[dictionary.get(name_col_base).index(element)]
   return element_dict     
  
  
def keywords_in_line(sub, keywords, points):
   used_keywords = search_keywords(sub, keywords)
   lines_base = used_keywords.get("line")  
   lines_summary=[]

   for kwd_line in lines_base:
       count_words = 0
       count_words = lines_base.count(kwd_line)
       if count_words >= 2:
          if kwd_line not in lines_summary:
             lines_summary.append(kwd_line)
             print("Rule 4.20 : keywords > 2 line: ", kwd_line)
             points = points + 1.0
   return points
 
 
def search_variables(sub):
   used_variables={}
   line = []
   col = []
   txt_key = []

   for var in sub.iter("variable"):
      if var.get("name") != None:
         line.append(int(var.get("line_begin")))
         col.append(int(var.get("col_begin")))
         txt_key.append(var.get("name"))
         
   used_variables.update({"line":line, "col_begin":col, "name":txt_key})     
   return used_variables


def case_keyword_variables(sub, points, keywords, not_keywords, name_list):
   used_variables = search_variables (sub)
  
   for var in used_variables.get("name"):
      line_var = element_dictionary(used_variables, "name", "line", var)    
      col_var = element_dictionary(used_variables, "name", "col_begin", var)  
      if not is_snake_case(var) and var not in name_list:
         print('Rule 4.7: case variables : line', line_var, 
               'col_begin:', col_var, 'variable: ', var )
         points = points + 1.0
      if var in keywords:
         print("Rule 4.71 : variable keyword : line", line_var, var)
         points = points + 1.0
      if var in not_keywords:
         print("Rule 4.71 : variable keyword : line", line_var, var)
         points = points + 1.0
   return points


#------->> fazer teste
def search_namelist(sub):
   name_list = {}
   line = []
   col = []
   id = []

   for nam in sub.iter("namelist-group-object"):
      line.append(int(nam.get("line_begin")))
      col.append(int(nam.get("col_begin")))
      id.append(nam.get("id"))    
   
   name_list.update({"line":line, "col_begin":col, "id":id})     
   return name_list


def verify_name_list (points, name_list):
   for nam in name_list["id"]:
      if not nam.isupper() :
         print('Rule 4.18 : case namelist : line', nam.get("line_begin"), 
               'col_begin:', nam.get("col_begin"), 'id: ', nam.get("id") )
         points = points + 1.0
   return points


def verify_col_end(sub, points):
   col = []
   key_tree = ["comment", "statement", "declaration" ]
   
   for verif in key_tree : 
      for col_count in sub.iter(verif):   
         if col_count.get("col_end") != None:
            if int(col_count.get("col_end")) >= 80 and int(col_count.get("col_end")) < 132:
               col.append(int(col_count.get("col_end")))    
               print('Rule 4.21 : size col >= 80 < 132: line', col_count.get("line_begin") )
               points = points + 1.0
            elif int(col_count.get("col_end")) >= 132:
               col.append(int(col_count.get("col_end")))
               print('Rule 4.21.1 : size col > 132: line', col_count.get("line_begin") )
               points = points + 0.5   
   return points


def verify_colapsed_keywords(points, used_keywords):         
   k = 0

   for kwd in used_keywords.get("keyword"):   
      if kwd != None:
         if kwd == "enddo" or kwd == "endif":
            print ("Rule 4.26 : collapsed form", kwd, ", line : ", 
                   used_keywords["line"][k] )
            points = points + 1.0 
      k = k + 1
      # uso do contador evita erro na numeração das linhas qdo há chaves repetidas
   return points


def verify_module_name(points, full_file_name, root):  
   file_name = find_file_name(full_file_name)        
   k = 0
   module_name = ""

   for mod in root.iter("module-stmt"):
      print("\n\nInspecionando a arquivo - módulo", file_name)
      print("---------------------------------------------------------")
      print("module line begin = ", int(mod.get("line_begin")))
      print("---------------------------------------------------------")    
      k = k + 1
      module_name = mod.get("id") #"Teste"
      print("module name: ", module_name)
   
   if k > 1:
      print ("Rule 4.32 module > 1")
      points = points + 1.0
   #elif k == 1:
   if file_name.find("mod") == -1:
      print ("Rule 4.32 module filename")
      points = points + 1.0
   if module_name.find("mod") == -1:
      print ("Rule 4.32 module name")
      points = points + 1.0

      print("Penalties in module :", points)
   return ()


def param_equation_lines(sub, points):
#rule 4.23 4.25
# assigment: mudança de linha usando "&" em equações e parametros não são documentada pelo xml
# precisa maiores análises

   points = points + 1.0  
   return()


def inout_param(sub, points):
# rule 4.27 
# no xml as chaves das operações são: <target> = <value>
# parametro de entrada que está em target -> saida
# parametro de entrada que está em <value> ->  entrada
# parametro de entrada que está em <target> e <value> -> entrada e saida  
   points = points + 1.0  
   return()


def verify_deallocate(sub,points):
   
   deallocated_list = {}
   allocated_list = {}
   line = []
   col = []
   id = []

   for deal in sub.iter("deallocate-stmt"):
      print("HERE")
      line.append(int(deal.get("line_begin")))
      col.append(int(deal.get("col_begin")))
      id.append(deal.get("deallocateKeyword")) 
   deallocated_list.update({"line":line, "col_begin":col, "id":id})  
   print(deallocated_list)

   for alloc in sub.iter("allocate-stmt"):
      print("here2")
      if alloc.get("deallocateKeyword") == True:
         line.append(int(alloc.get("line_begin")))
         col.append(int(alloc.get("col_begin")))
         id.append(alloc.get("deallocateKeyword")) 
   allocated_list.update({"line":line, "col_begin":col, "id":id})  
   print("allocated: ", allocated_list)
   
   if allocated_list !={}:
      for deal in deallocated_list.get("line"):
      #print(deal)
         if deal not in allocated_list.get("line"):
            print('Rule XXX deallocate line": ', line)
            points = points + 1.0

   # for alloc in allocated_list.get("line"):
   #     #print (alloc)
   #     if alloc not in deallocated_list:
   #        print('Rule XXX deallocate line": ', line)
   #        points = points + 1.0
         
   return(points)    


def verify_alocate(sub,points):
   
   deallocate_list = {}
   allocated_list = {}
   line = []
   col = []
   id = []

   for deal in sub.iter("deallocate"):
      line.append(int(deal.get("line_begin")))
      col.append(int(deal.get("col_begin")))
      id.append(deal.get("id")) 
   deallocate_list.update({"line":line, "col_begin":col, "id":id})  

   for alloc in sub.iter("allocate-stmt"):
      line.append(int(deal.get("line_begin")))
      col.append(int(deal.get("col_begin")))
      id.append(deal.get("id")) 
   allocated_list.update({"line":line, "col_begin":col, "id":id})  

   for deal in deallocate_list:
       if deal not in allocated_list:
          print('Rule XXX deallocate line": ', line)
          points = points + 1.0
   
   return(points)    





 # Para casos em que o conteúdo ao fim da linha é um string deve-se dividi-lo 
 # usando a concatenação de strings (“//”) e usar a continuação de linha (“&”).

def string_lines(sub, points):
#rule 22/4.24- mudança de linha por string "&" ao final da linha  e "//" na continuação

   col = []
   key_tree = ["statement"]#, "declaration" ]
   
   # for verif in key_tree : 
   #    for col_count in sub.iter(verif):   
   #       if col_count.get("col_end") != None:
   #          if int(col_count.get("col_end")) >= 80 and int(col_count.get("col_end")) < 132:
   #             col.append(int(col_count.get("col_end")))    
   #             print('Rule 4.21 : size col >= 80 < 132: line', col_count.get("line_begin") )
   #             points = points + 1.0
   #          elif int(col_count.get("col_end")) >= 132:
   #             col.append(int(col_count.get("col_end")))
   #             print('Rule 4.21.1 : size col > 132: line', col_count.get("line_begin") )
   points = points + 0.5   
   # return points
   return(points)


def param_equation_lines(sub, points):
#rule 4.23 4.25
# assigment: mudança de linha usando "&" em equações e parametros não são documentada pelo xml
# precisa maiores análises

   points = points + 1.0  
   return()


def inout_param(sub, points):
# rule 4.27 
# no xml as chaves das operações são: <target> = <value>
# parametro de entrada que está em target -> saida
# parametro de entrada que está em <value> ->  entrada
# parametro de entrada que está em <target> e <value> -> entrada e saida

   
   points = points + 1.0  
   return()


def verify_deallocate(sub,points):
   
   deallocate_list = {}
   allocated_list = {}
   line = []
   col = []
   id = []

   for deal in sub.iter("deallocate"):
      line.append(int(deal.get("line_begin")))
      col.append(int(deal.get("col_begin")))
      id.append(deal.get("id"))
      deal_exist = True 
   deallocate_list.update({"line":line, "col_begin":col, "id":id})  
   print(deallocate_list)

   for aloc in sub.iter("allocate-stmt"):
      line.append(int(aloc.get("line_begin")))
      col.append(int(aloc.get("col_begin")))
      id.append(aloc.get("id")) 
      aloc_exist = True
   allocated_list.update({"line":line, "col_begin":col, "id":id})  
   
   #
   if aloc_exist and deal_exist:
      for aloc in allocated_list:
          if aloc not in deallocate_list:
             print('Rule XXX deallocate line": ', line)
             points = points + 1.0
   
   return(points)


def verify_allocate(sub,points):
   
   deallocated_list = {}
   allocated_list = {}
   line = []
   col = []
   id = []
   n_alloc = 0

   #encontra allocatables
   for dec in sub.iter ("declaration"):
      #print("FindAllocation", dec.get("line_begin"))
      allocatable = False
      for alloc in dec.iter("attribute-allocatable"):
         n_alloc = n_alloc + 1 
         #print( n_alloc, alloc.get("line_begin") )
         allocatable = True
      if allocatable == True:
          for var in dec.iter ("variable"):
             print("Allocatable: ", var.get("name"))
          
   #encontra allocates
   for aloc in sub.iter("allocate"):
       line.append(int(aloc.get("line_begin")))
       col.append(int(aloc.get("col_begin")))
       #id.append(aloc.get("id")) 
       for nam in aloc.iter("name"):
          id.append(nam.get("id")) 
   allocated_list.update({"line":line, "col_begin":col, "id":id})  

   #encontra deallocates       
   line = []
   col = []
   id = []
   for deal in sub.iter("deallocate"):
       line.append(int(deal.get("line_begin")))
       col.append(int(deal.get("col_begin")))
       #id.append(deal.get("name")) 
       for nam in deal.iter("name"):
          id.append(nam.get("id")) 
   deallocated_list.update({"line":line, "col_begin":col, "id":id})  
   print (allocated_list)
   # if not allocated_list["id"]==[]:
   #    if not allocated_list["id"] == deallocated_list["id"]:
   #       print('Rule XXX deallocate line": ', allocated_list["line"])
   #       points = points + 1.0
   
   # compara allocates e deallocates   
   for k in allocated_list ["id"]:
      if k not in deallocated_list["id"]:
         print('Rule XXX deallocate line": ', allocated_list["line"])
         points = points + 1.0
 
   return(points)    

