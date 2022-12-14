######           Analisador Léxico    ######
# Autor 1: Lucas Vinicius dos Santos Assis
# Autor 2: Andressa Moura de Souza
# Modificações: Larissa Ribeiro Sardinha

import sys
import os.path
import string

class AnalisadorLexico():

  def __init__(self):
    self.arquivo_e = "programa.txt"
    self.arquivo_s = "resultado-lexico.txt"

  def mudaEntrada(self, string):
    self.arquivo_e = string

  def getEntrada(self):
    return self.arquivo_e

  def getSaida(self):
    return self.arquivo_s

  def ehDelimitador(self, caracter):
    delimitadores = ";,(){}[]"
    if caracter in delimitadores:
      return True
    return False

  def qualTokenDelimitador(self, entrada):
    delimitadores = ";,(){}[]"
    posicao = delimitadores.find(entrada)
    return "tok20"+str(posicao)

  def ehLetra (self, caracter):
    letra = string.ascii_letters
    if caracter in letra:
      return True
    return False

  def ehDigito (self, caracter):
    digito = '0123456789'
    if caracter in digito:
      return True
    return False

  def ehSimbolo(self, caracter):
    simbolos = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz{|}~'''
    if(caracter in simbolos):
      return True
    return False

  def ehOperador(self, entrada):
    operadores = ': - * > ='.split()
    if entrada in operadores:
      return True
    return False
  
  def qualTokenOperador(self, entrada):
    operadores = ': - * > ='.split()
    posicao = 0
    for x in operadores:
      if x == entrada:
        break
      posicao += 1
    if(posicao > 9):
      return "tok1"+str(posicao)
    else:
      return "tok10"+str(posicao)
  
  def ehReservada(self, entrada):
    reservadas = "declaracoes algoritmo int real atribuir a ler imprimir se entao enquanto inicio fim e ou".split()
    if entrada in reservadas:
      return True
    return False

  def qualTokenReservada(self, entrada):
    reservadas = '''declaracoes algoritmo int real atribuir a ler imprimir se entao enquanto inicio fim e ou'''.split()
    posicao = 0
    for x in reservadas:
      if x == entrada:
        break
      posicao += 1
    if(posicao > 9):
      return "tok6"+str(posicao)
    else:
      return "tok60"+str(posicao)

  def analisa(self):
    arquivo_saida = open(self.arquivo_s, 'w')
    if not os.path.exists(self.arquivo_e):
      arquivo_saida.write("Arquivo de entrada inexistente")
      return

    arquivo = open(self.arquivo_e, 'r')

    linha_programa = arquivo.readline()

    numero_linha = 1
    
    while linha_programa:
      i = 0
      tamanho_linha = len(linha_programa)
      while i < tamanho_linha: 
        caracter_atual = linha_programa[i] 
        caractere_seguinte = None
        if ((i+1) < tamanho_linha):
          caractere_seguinte = linha_programa[i+1] 

        if (self.ehDelimitador(caracter_atual)):
          arquivo_saida.write(self.qualTokenDelimitador(caracter_atual)+'_'+caracter_atual+'->'+str(numero_linha)+'\n')

        elif (caracter_atual == '/' and caractere_seguinte == '/'):
          i = tamanho_linha

        elif (caracter_atual == '/' and caractere_seguinte == '*'):
          cont = True 
          linha_comeco = numero_linha 
          while cont and not (caracter_atual == '*' and caractere_seguinte == '/'):
            if ((i+2) < tamanho_linha):
              i += 1
              caracter_atual = linha_programa[i]
              caractere_seguinte = linha_programa[i+1]                   
            else:
              linha_programa = arquivo.readline() 
              tamanho_linha = len(linha_programa)
              numero_linha += 1
              i = -1
              if (not linha_programa):
                arquivo_saida.write ("Erro Lexico - Comentario de bloco nao fechado - linha: %d\n" %linha_comeco)
                cont = False
          i += 1 
        elif caractere_seguinte != None and self.ehOperador(caracter_atual+caractere_seguinte):
          arquivo_saida.write(self.qualTokenOperador(caracter_atual+caractere_seguinte)+'_'+caracter_atual+caractere_seguinte+'->'+str(numero_linha)+'\n')
          i += 1
        elif self.ehOperador(caracter_atual):
          arquivo_saida.write(self.qualTokenOperador(caracter_atual)+'_'+caracter_atual+'->'+str(numero_linha)+'\n')


        elif (caracter_atual == string.punctuation[6]):

          if (linha_programa[i+1] == '\n') or (not (string.punctuation[6] in linha_programa[i+1:])):
            arquivo_saida.write('Erro Lexico - Caractere nao fechado - Linha: %d\n' %numero_linha)
            i = tamanho_linha
          elif self.ehSimbolo(linha_programa[i+1]) and linha_programa[i+1] != string.punctuation[6] and linha_programa[i+2] == string.punctuation[6]:
            arquivo_saida.write('tok400_'+linha_programa[i+1]+'->'+str(numero_linha)+'\n')
            i+=2
          elif linha_programa[i+1] == string.punctuation[6] and linha_programa[i+2] == string.punctuation[6]:
            arquivo_saida.write('Erro Lexico - Caractere nao pode ser aspas simples - Linha: %d\n' %numero_linha)
            i+=2
          elif linha_programa[i+1] == string.punctuation[6]:
            arquivo_saida.write('Erro Lexico - Caractere nao pode ser vazio - Linha: %d\n' %numero_linha)
            i+=1
          else:
            arquivo_saida.write('Erro Lexico - Tamanho ou simbolo do Caractere invalido - Linha: %d\n' %numero_linha)
            i=linha_programa[i+1:].find(string.punctuation[6])+1


        elif (caracter_atual == string.punctuation[1]):
          i+=1 
          ehValido = True

          if (linha_programa[i:].find(string.punctuation[1]) == -1):
            arquivo_saida.write('Erro Lexico - String nao fechada - Linha: %d\n' %numero_linha)
            i = tamanho_linha
          else:
            fim_cadeia = i+linha_programa[i:].find(string.punctuation[1])
            nova_cadeia = linha_programa[i:fim_cadeia]
            i = fim_cadeia
            for x in nova_cadeia:
              if(not self.ehSimbolo(x)):
                ehValido = False
                arquivo_saida.write('Erro Lexico - String com simbolo invalido (Nao ascii) - Linha: %d\n' %numero_linha)
                break
            if(ehValido):
              arquivo_saida.write('tok700_'+nova_cadeia+'->'+str(numero_linha)+'\n')
        elif (self.ehDigito(caracter_atual)):
          string_temp = caracter_atual
          i += 1
          j = 0 
          caracter_atual = linha_programa[i]
          while (self.ehDigito(caracter_atual) and (i+1 < tamanho_linha)):
            string_temp += caracter_atual
            i += 1
            caracter_atual = linha_programa[i]

          if (caracter_atual == '.'):
            if ((i+1) < tamanho_linha):
              string_temp += caracter_atual
              i += 1
              caracter_atual = linha_programa[i]
              while self.ehDigito(caracter_atual) and i+1 < tamanho_linha:
                j += 1
                string_temp += caracter_atual
                i += 1
                caracter_atual = linha_programa[i]

              if(caracter_atual == '.'):
                j = 0
                while (i+1 < tamanho_linha):
                  i += 1
                  caracter_atual = linha_programa[i]
                  if self.ehDelimitador(caracter_atual) or caracter_atual == ' ':
                    i -= 1 
                    break
            else:
              arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %numero_linha)

            if (j > 0):
              arquivo_saida.write('tok301_'+string_temp+'->'+str(numero_linha)+'\n')
            else: 
              arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %numero_linha)
          else:
            arquivo_saida.write('tok300_'+string_temp+'->'+str(numero_linha)+'\n')
            if(not self.ehDigito(caracter_atual)):
              i -= 1

        elif (self.ehLetra(caracter_atual)):
          string_temp = caracter_atual
          i += 1
          algum_erro = False
          while i < tamanho_linha:
            caractere_seguinte = None
            caracter_atual = linha_programa[i]
            if(i+1 < tamanho_linha):
              caractere_seguinte = linha_programa[i+1]
            if (self.ehLetra(caracter_atual) or self.ehDigito(caracter_atual) or caracter_atual == '_'):
              string_temp += caracter_atual
            elif (self.ehDelimitador(caracter_atual) or caracter_atual == ' ' or caracter_atual == '\t' or caracter_atual == '\r'):
              i -= 1 
              break
            elif(caractere_seguinte != None and self.ehOperador(caracter_atual+caractere_seguinte)) or self.ehOperador(caracter_atual):
              i-=1
              break
            elif caracter_atual != '\n':
              arquivo_saida.write("Erro Lexico - Identificador com caracter invalido: "+caracter_atual+" - linha: %d\n" %numero_linha)
              algum_erro = True
              break
            i += 1 
            

          if (algum_erro):
            while (i+1 < tamanho_linha):
              i += 1
              caracter_atual = linha_programa[i]
              if self.ehDelimitador(caracter_atual) or caracter_atual == ' ' or caracter_atual == '\t' or caracter_atual == '\r' or caracter_atual == '/':
                i -= 1 
                break
          else: 
            if (self.ehReservada(string_temp)):
              arquivo_saida.write(self.qualTokenReservada(string_temp)+'_'+string_temp+'->'+str(numero_linha)+'\n')
            else:
              arquivo_saida.write('tok500_'+string_temp+'->'+str(numero_linha)+'\n')
          

        elif caracter_atual != '\n' and caracter_atual != ' ' and caracter_atual != '\t' and caracter_atual != '\r':
          arquivo_saida.write('Erro Lexico - Caracter Invalido: ' + caracter_atual + ' - linha: %d\n' %numero_linha)
        
        i += 1 

      linha_programa = arquivo.readline() 
      numero_linha += 1
    arquivo_saida.write('$')
    arquivo.close()
    arquivo_saida.close


lex = AnalisadorLexico()
lex.analisa()



