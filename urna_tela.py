import aroeira as ar

tela = ar.Tela("Urna Eletrônica", 800, 600)

#funcoes---------------------
def criar_click(numero):
    def criado():
        global digitado, count, blocos
        if count < len(blocos):
            digitado += str(numero)
            antigo = blocos[count]
            tela.remover(antigo)
            novo = ar.Retangulo(antigo.origem, antigo.largura, antigo.altura, "branco", "preto")
            blocos[count] = novo
            tela.adicionar(novo)
            
            bloco_textos[count].conteudo = str(numero)
            count += 1
            
            print (digitado)
    return criado
#botoes valor------------
click1 = criar_click(1)
click2 = criar_click(2)
click3 = criar_click(3)
click4 = criar_click(4)
click5 = criar_click(5)
click6 = criar_click(6)
click7 = criar_click(7)
click8 = criar_click(8)
click9 = criar_click(9)
click0 = criar_click(0)

digitado = ""
count=0


#------------------------------------------------------------------------------

#retangulos-------------------
retangulo1 = ar.Retangulo(ar.Ponto(30, 40), 420, 400, "#D3D3D3", "preto")
retangulo2 = ar.Retangulo(ar.Ponto(480, 80), 280, 400, "#A9A9A9")
retangulo3 = ar.Retangulo(ar.Ponto(480, 30), 280, 50, "#D3D3D3")

#texto------------------------
justica = ar.Texto(ar.Ponto(507, 40), "JUSTIÇA ELEITORAL", 24, "preto", True)
seu_voto= ar.Texto(ar.Ponto(40,40),"Seu voto para:",20,'preto',True)
cargo1 = ar.Texto(ar.Ponto(42,60),'Deputado Federal',30,"preto",True)
numero = ar.Texto(ar.Ponto(40,130),'Número:',16,"preto",True)

#botoes numericos-----------------------
btn1 = ar.Botao(ar.Ponto(510, 150), "1", ao_clicar=click1, cor="preto", cor_texto="branco")
btn2 = ar.Botao(ar.Ponto(590, 150), "2", ao_clicar=click2, cor="preto", cor_texto="branco")
btn3 = ar.Botao(ar.Ponto(670, 150), "3", ao_clicar=click3, cor="preto", cor_texto="branco")

btn4 = ar.Botao(ar.Ponto(510, 200), "4", ao_clicar=click4, cor="preto", cor_texto="branco")
btn5 = ar.Botao(ar.Ponto(590, 200), "5", ao_clicar=click5, cor="preto", cor_texto="branco")
btn6 = ar.Botao(ar.Ponto(670, 200), "6", ao_clicar=click6, cor="preto", cor_texto="branco")

btn7 = ar.Botao(ar.Ponto(510, 250), "7", ao_clicar=click7, cor="preto", cor_texto="branco")
btn8 = ar.Botao(ar.Ponto(590, 250), "8", ao_clicar=click8, cor="preto", cor_texto="branco")
btn9 = ar.Botao(ar.Ponto(670, 250), "9", ao_clicar=click9, cor="preto", cor_texto="branco")

btn0 = ar.Botao(ar.Ponto(590, 300), "0", ao_clicar=click0, cor="preto", cor_texto="branco")



#botões do voto-----------------------
bloco1=ar.Retangulo(ar.Ponto(120,130),30,50,"branco","preto")
bloco2=ar.Retangulo(ar.Ponto(152,130),30,50,"branco","preto")
bloco3=ar.Retangulo(ar.Ponto(184,130),30,50,"branco","preto")
bloco4=ar.Retangulo(ar.Ponto(216,130),30,50,"branco","preto")
blocos = [bloco1, bloco2, bloco3, bloco4]

#Texto dos blocos-----------------------
texto1 = ar.Texto(ar.Ponto(120+6, 130+10), "", 20, "preto")
texto2 = ar.Texto(ar.Ponto(152+6, 130+10), "", 20, "preto")
texto3 = ar.Texto(ar.Ponto(184+6, 130+10), "", 20, "preto")
texto4 = ar.Texto(ar.Ponto(216+6, 130+10), "", 20, "preto")
bloco_textos = [texto1, texto2, texto3, texto4]



#botoes acao-----------------------
branco = ar.Botao(ar.Ponto(500, 350), "BRANCO", cor="branco", cor_texto="preto")
corrige = ar.Botao(ar.Ponto(640, 350), "CORRIGE", cor="laranja", cor_texto="preto")
confirma = ar.Botao(ar.Ponto(560, 400), "CONFIRMA", cor="verde", cor_texto="preto")

#basico--------------------
tela.adicionar(retangulo1)
tela.adicionar(retangulo2)
tela.adicionar(retangulo3)
tela.adicionar(justica)
tela.adicionar(cargo1)
tela.adicionar(seu_voto)
tela.adicionar(numero)

#botoes numericos add------------------
tela.adicionar(btn1)
tela.adicionar(btn2)
tela.adicionar(btn3)
tela.adicionar(btn4)
tela.adicionar(btn5)
tela.adicionar(btn6)
tela.adicionar(btn7)
tela.adicionar(btn8)
tela.adicionar(btn9)
tela.adicionar(btn0)

#texto blocos add------------------
tela.adicionar(texto1)
tela.adicionar(texto2)
tela.adicionar(texto3)
tela.adicionar(texto4)

#botoes acao-----------------------
tela.adicionar(branco)
tela.adicionar(corrige)
tela.adicionar(confirma)

#botões do voto add-----------------------
tela.adicionar(bloco1)
tela.adicionar(bloco2)
tela.adicionar(bloco3)
tela.adicionar(bloco4)




tela.executar()
