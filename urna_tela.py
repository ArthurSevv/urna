import os
import aroeira as ar


ARQUIVO_CANDIDATOS = "consulta_cand_2026_BRASIL.csv"
ARQUIVO_VOTOS = "votos_urna.csv"
PASTA_IMAGENS = "imgs_organizadas"
CARGOS_COM_FOTO = ["DEPUTADO FEDERAL", "DEPUTADO ESTADUAL", "SENADOR", "GOVERNADOR", "PRESIDENTE"]

ETAPAS = [
    {"cargo": "Deputado Federal", "cargo_csv": "DEPUTADO FEDERAL", "digitos": 4, "usa_uf": False},
    {"cargo": "Deputado Estadual", "cargo_csv": "DEPUTADO ESTADUAL", "digitos": 5, "usa_uf": True},
    {"cargo": "Senador (1º voto)", "cargo_csv": "SENADOR", "digitos": 3, "usa_uf": True},
    {"cargo": "Senador (2º voto)", "cargo_csv": "SENADOR", "digitos": 3, "usa_uf": True},
    {"cargo": "Governador", "cargo_csv": "GOVERNADOR", "digitos": 2, "usa_uf": True},
    {"cargo": "Presidente", "cargo_csv": "PRESIDENTE", "digitos": 2, "usa_uf": False},
]


def carregar_candidatos():
    candidatos = []
    with open(ARQUIVO_CANDIDATOS, "r", encoding="cp1252") as arquivo:
        cabecalho = arquivo.readline().strip().split(";")
        cabecalho = [coluna.replace('"', "").strip() for coluna in cabecalho]
        idx_uf = cabecalho.index("SG_UF")
        idx_cargo = cabecalho.index("DS_CARGO")
        idx_numero = cabecalho.index("NR_CANDIDATO")
        idx_nome_urna = cabecalho.index("NM_URNA_CANDIDATO")
        idx_partido = cabecalho.index("SG_PARTIDO")

        for linha in arquivo:
            colunas = linha.strip().split(";")
            candidatos.append(
                {
                    "UF": colunas[idx_uf].replace('"', "").strip().upper(),
                    "CARGO": colunas[idx_cargo].replace('"', "").strip().upper(),
                    "NR_CANDIDATO": colunas[idx_numero].replace('"', "").strip(),
                    "NOME_URNA": colunas[idx_nome_urna].replace('"', "").strip(),
                    "PARTIDO": colunas[idx_partido].replace('"', "").strip(),
                }
            )
    return candidatos


def etapa_atual_obj():
    return ETAPAS[indice_etapa]

def obter_voto_primeiro_senador():
    for voto in votos_registrados:
        if voto["cargo"] == "Senador (1º voto)":
            return voto
    return None


def normalizar_texto(texto):
    texto = texto.upper()
    texto = texto.replace("Á", "A").replace("À", "A").replace("Ã", "A").replace("Â", "A")
    texto = texto.replace("É", "E").replace("Ê", "E")
    texto = texto.replace("Í", "I")
    texto = texto.replace("Ó", "O").replace("Ô", "O").replace("Õ", "O")
    texto = texto.replace("Ú", "U")
    texto = texto.replace("Ç", "C")
    texto_limpo = ""
    for caractere in texto:
        if caractere.isalnum():
            texto_limpo += caractere
        else:
            texto_limpo += "_"
    while "__" in texto_limpo:
        texto_limpo = texto_limpo.replace("__", "_")
    return texto_limpo.strip("_")


def buscar_foto_candidato(candidato):
    cargo = candidato["CARGO"].upper()
    if cargo not in CARGOS_COM_FOTO:
        return None

    pasta_cargo = normalizar_texto(cargo)
    caminho_pasta_cargo = os.path.join(PASTA_IMAGENS, pasta_cargo)
    if not os.path.isdir(caminho_pasta_cargo):
        return None

    numero_candidato = candidato["NR_CANDIDATO"]
    nome_candidato_slug = normalizar_texto(candidato["NOME_URNA"])
    primeira_opcao = None

    for nome_arquivo in os.listdir(caminho_pasta_cargo):
        caminho_arquivo = os.path.join(caminho_pasta_cargo, nome_arquivo)
        if not os.path.isfile(caminho_arquivo):
            continue

        nome_base, _extensao = os.path.splitext(nome_arquivo)
        partes = nome_base.split("_")
        if len(partes) < 4:
            continue
        if partes[0] != numero_candidato:
            continue

        nome_slug = "_".join(partes[1:-2])
        if primeira_opcao is None:
            primeira_opcao = os.path.abspath(caminho_arquivo)
        if nome_slug == nome_candidato_slug:
            return os.path.abspath(caminho_arquivo)

    return primeira_opcao


def limpar_voto_etapa():
    global digitado, voto_em_branco
    digitado = ""
    voto_em_branco = False
    texto_nome.conteudo = ""
    texto_partido.conteudo = ""
    texto_status.conteudo = ""
    foto_candidato.visivel = False
    atualizar_blocos()


def atualizar_blocos():
    quantidade = etapa_atual_obj()["digitos"]
    for i in range(len(blocos)):
        bloco = blocos[i]
        ativo = i < quantidade
        bloco.visivel = ativo
        bloco_textos[i].visivel = ativo
        if ativo and i < len(digitado):
            bloco_textos[i].conteudo = digitado[i]
        else:
            bloco_textos[i].conteudo = ""


def buscar_candidato(numero_digitado):
    etapa = etapa_atual_obj()
    cargo_csv = etapa["cargo_csv"]
    if etapa["usa_uf"] and estado_eleitor:
        for candidato in candidatos:
            if candidato["CARGO"] != cargo_csv:
                continue
            if candidato["NR_CANDIDATO"] != numero_digitado:
                continue
            if candidato["UF"] == estado_eleitor:
                return candidato

    for candidato in candidatos:
        if candidato["CARGO"] == cargo_csv and candidato["NR_CANDIDATO"] == numero_digitado:
            return candidato
    return None


def atualizar_preview_candidato():
    etapa = etapa_atual_obj()
    if voto_em_branco:
        texto_status.conteudo = "VOTO EM BRANCO"
        texto_nome.conteudo = ""
        texto_partido.conteudo = ""
        foto_candidato.visivel = False
        return

    if len(digitado) != etapa["digitos"]:
        texto_nome.conteudo = ""
        texto_partido.conteudo = ""
        texto_status.conteudo = ""
        foto_candidato.visivel = False
        return

    candidato = buscar_candidato(digitado)
    if candidato is None:
        texto_nome.conteudo = "NÚMERO NÃO ENCONTRADO"
        texto_partido.conteudo = ""
        texto_status.conteudo = "SE CONFIRMAR, O VOTO SERÁ NULO"
        foto_candidato.visivel = False
        return

    texto_nome.conteudo = "Nome: " + candidato["NOME_URNA"]
    texto_partido.conteudo = "Partido: " + candidato["PARTIDO"]
    texto_status.conteudo = ""
    caminho_foto = buscar_foto_candidato(candidato)
    if caminho_foto is None:
        foto_candidato.visivel = False
    else:
        foto_candidato.caminho = caminho_foto
        foto_candidato.visivel = True


def registrar_voto(tipo, numero, candidato):
    etapa = etapa_atual_obj()
    votos_registrados.append(
        {
            "cargo": etapa["cargo"],
            "tipo": tipo,
            "numero": numero,
            "nome_urna": "" if candidato is None else candidato["NOME_URNA"],
            "partido": "" if candidato is None else candidato["PARTIDO"],
            "uf_candidato": "" if candidato is None else candidato["UF"],
            "uf_eleitor": estado_eleitor,
        }
    )


def detectar_delimitador_csv(linha):
    if linha.count(";") >= linha.count(","):
        return ";"
    return ","


def salvar_votos_csv():
    campos = ["cargo", "tipo", "numero", "nome_urna", "partido", "uf_candidato", "uf_eleitor"]
    delimitador = ";"
    escrever_cabecalho = False

    if not os.path.exists(ARQUIVO_VOTOS):
        escrever_cabecalho = True
    else:
        primeira_linha = ""
        with open(ARQUIVO_VOTOS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    primeira_linha = linha
                    break
        if not primeira_linha:
            escrever_cabecalho = True
        else:
            delimitador = detectar_delimitador_csv(primeira_linha)

    with open(ARQUIVO_VOTOS, "a", encoding="utf-8") as arquivo:
        if escrever_cabecalho:
            arquivo.write(delimitador.join(campos) + "\n")
        for voto in votos_registrados:
            linha = []
            for campo in campos:
                valor = str(voto[campo]).replace("\n", " ")
                if delimitador == ";":
                    valor = valor.replace(";", ",")
                else:
                    valor = valor.replace(",", " ")
                linha.append(valor)
            arquivo.write(delimitador.join(linha) + "\n")


def normalizar_cargo_apuracao(cargo):
    if cargo.startswith("Senador"):
        return "Senador"
    return cargo


def montar_identificador_apuracao(voto):
    tipo = voto["tipo"].strip().upper()
    if tipo == "VALIDO":
        numero = voto["numero"].strip()
        nome = voto["nome_urna"].strip()
        if numero and nome:
            return numero + " - " + nome
        if nome:
            return nome
        if numero:
            return numero
        return "VALIDO"
    if tipo == "BRANCO":
        return "BRANCO"
    return "NULO"


def montar_relatorio_apuracao():
    if not os.path.exists(ARQUIVO_VOTOS):
        return "Nenhum voto encontrado no arquivo."

    delimitador = ";"
    primeira_linha_valida = True
    totais = {}

    with open(ARQUIVO_VOTOS, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha == "":
                continue

            if primeira_linha_valida:
                delimitador = detectar_delimitador_csv(linha)
                primeira_linha_valida = False

            colunas = linha.split(delimitador)
            if len(colunas) < 4:
                continue

        
            cargo_linha, tipo_linha, numero_linha, nome_linha = colunas[:4]

            cargo_linha = cargo_linha.strip()
            tipo_linha = tipo_linha.strip()
            numero_linha = numero_linha.strip()
            nome_linha = nome_linha.strip()

        
            if cargo_linha.lower() == "cargo" and tipo_linha.lower() == "tipo":
                continue

            voto = {
                "cargo": cargo_linha,
                "tipo": tipo_linha,
                "numero": numero_linha,
                "nome_urna": nome_linha,
            }
            cargo = normalizar_cargo_apuracao(voto["cargo"])
            candidato = montar_identificador_apuracao(voto)

         
            if cargo not in totais:
                totais[cargo] = {}

           
            totais[cargo][candidato] = totais[cargo].get(candidato, 0) + 1

    if len(totais) == 0:
        return "Nenhum voto encontrado no arquivo."

   
    ordem = ["Deputado Federal", "Deputado Estadual", "Senador", "Governador", "Presidente"]
    cargos_extras = []
    for cargo in totais:
        if cargo not in ordem:
            cargos_extras.append(cargo)
    cargos_extras.sort()

    blocos = []
    for cargo in ordem + cargos_extras:
        if cargo not in totais:
            continue

        bloco = cargo + ":"
        for candidato in totais[cargo]:
            bloco = bloco + "\n" + candidato + ":" + str(totais[cargo][candidato])
        blocos.append(bloco)

   
    return "\n\n".join(blocos)

def finalizar_apuracao():
    relatorio = montar_relatorio_apuracao()
    with open("resultado_apuracao.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio + "\n")
    texto_status_fim.conteudo = "Apuração salva em resultado_apuracao.txt"


def finalizar_votacao():
    global votacao_finalizada
    votacao_finalizada = True
    salvar_votos_csv()
    retangulo_fim.visivel = True
    texto_fim.visivel = True
    texto_status_fim.visivel = True
    retangulo1.visivel = False
    retangulo2.visivel = False
    retangulo3.visivel = False
    justica.visivel = False
    seu_voto.visivel = False
    cargo1.visivel = False
    numero.visivel = False
    texto_nome.visivel = False
    texto_partido.visivel = False
    texto_status.visivel = False
    texto_estado.visivel = False
    foto_candidato.visivel = False
    for botao_numero in botoes_numericos:
        botao_numero.visivel = False
    for bloco in blocos:
        bloco.visivel = False
    for texto_bloco in bloco_textos:
        texto_bloco.visivel = False
    branco.ativo = False
    branco.visivel = False
    corrige.ativo = False
    corrige.visivel = False
    confirma.ativo = False
    confirma.visivel = False
    reiniciar_btn.visivel = True
    reiniciar_btn.ativo = True
    finalizar_btn.visivel = True
    finalizar_btn.ativo = True


def avancar_etapa():
    global indice_etapa
    indice_etapa += 1
    if indice_etapa >= len(ETAPAS):
        finalizar_votacao()
        return
    carregar_etapa()


def confirmar_voto():
    etapa = etapa_atual_obj()

    if voto_em_branco:
        registrar_voto("BRANCO", "", None)
        avancar_etapa()
        return

    if len(digitado) != etapa["digitos"]:
        texto_status.conteudo = "DIGITE " + str(etapa["digitos"]) + " NÚMEROS"
        return

    candidato = buscar_candidato(digitado)
    if etapa["cargo"] == "Senador (2º voto)" and candidato is not None:
        primeiro_voto_senador = obter_voto_primeiro_senador()
        if primeiro_voto_senador is not None and primeiro_voto_senador["tipo"] == "VALIDO":
            mesmo_numero = primeiro_voto_senador["numero"] == digitado
            mesmo_nome = primeiro_voto_senador["nome_urna"] == candidato["NOME_URNA"]
            if mesmo_numero and mesmo_nome:
                texto_status.conteudo = "2º SENADOR DEVE SER DIFERENTE DO 1º"
                return

    if candidato is None:
        registrar_voto("NULO", digitado, None)
    else:
        registrar_voto("VALIDO", digitado, candidato)
    avancar_etapa()


def correcao():
    if votacao_finalizada:
        return
    limpar_voto_etapa()


def criar_click(numero_digitado):
    def clicado():
        global digitado, voto_em_branco

        if votacao_finalizada:
            return

        etapa = etapa_atual_obj()
        if len(digitado) >= etapa["digitos"]:
            return

        if voto_em_branco:
            voto_em_branco = False
            texto_status.conteudo = ""

        digitado += str(numero_digitado)
        atualizar_blocos()
        atualizar_preview_candidato()

    return clicado


def clique_confirma():
    if votacao_finalizada:
        return
    confirmar_voto()


def voto_branco_confirmavel():
    global digitado, voto_em_branco
    if votacao_finalizada:
        return
    voto_em_branco = True
    digitado = ""
    atualizar_blocos()
    atualizar_preview_candidato()


def reiniciar_votacao():
    global indice_etapa, votos_registrados, votacao_finalizada
    indice_etapa = 0
    votos_registrados = []
    votacao_finalizada = False
    retangulo_fim.visivel = False
    texto_fim.visivel = False
    texto_status_fim.visivel = False
    retangulo1.visivel = True
    retangulo2.visivel = True
    retangulo3.visivel = True
    justica.visivel = True
    seu_voto.visivel = True
    cargo1.visivel = True
    numero.visivel = True
    texto_nome.visivel = True
    texto_partido.visivel = True
    texto_status.visivel = True
    texto_estado.visivel = True
    foto_candidato.visivel = False
    for botao_numero in botoes_numericos:
        botao_numero.visivel = True
    branco.ativo = True
    branco.visivel = True
    corrige.ativo = True
    corrige.visivel = True
    confirma.ativo = True
    confirma.visivel = True
    reiniciar_btn.visivel = False
    finalizar_btn.visivel = False
    texto_status_fim.conteudo = "Votação encerrada. CSV salvo em " + ARQUIVO_VOTOS
    seu_voto.conteudo = "Seu voto para:"
    numero.conteudo = "Número:"
    carregar_etapa()


def carregar_etapa():
    etapa = etapa_atual_obj()
    cargo1.conteudo = etapa["cargo"]
    limpar_voto_etapa()
    atualizar_blocos()


estado_eleitor = "RS"
candidatos = carregar_candidatos()

digitado = ""
voto_em_branco = False
indice_etapa = 0
votos_registrados = []
votacao_finalizada = False

tela = ar.Tela("Urna Eletrônica", 800, 600)

# retangulos-------------------
retangulo1 = ar.Retangulo(ar.Ponto(30, 40), 420, 400, "#D3D3D3", "preto")
retangulo2 = ar.Retangulo(ar.Ponto(480, 80), 280, 400, "#A9A9A9")
retangulo3 = ar.Retangulo(ar.Ponto(480, 30), 280, 50, "#D3D3D3")

# texto------------------------
justica = ar.Texto(ar.Ponto(507, 40), "JUSTIÇA ELEITORAL", 24, "preto", True)
seu_voto = ar.Texto(ar.Ponto(40, 40), "Seu voto para:", 20, "preto", True)
cargo1 = ar.Texto(ar.Ponto(42, 60), "", 30, "preto", True)
numero = ar.Texto(ar.Ponto(40, 130), "Número:", 16, "preto", True)
texto_nome = ar.Texto(ar.Ponto(40, 220), "", 18, "preto", True)
texto_partido = ar.Texto(ar.Ponto(40, 250), "", 16, "preto")
texto_status = ar.Texto(ar.Ponto(40, 290), "", 16, "preto", True)
texto_estado = ar.Texto(ar.Ponto(40, 330), "UF do eleitor: " + (estado_eleitor if estado_eleitor else "NÃO INFORMADA"), 14, "preto")
foto_candidato = ar.Imagem(ar.Ponto(300, 205), "", 130, 160)
foto_candidato.visivel = False

# botoes valor------------
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

# botoes numericos-----------------------
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

# blocos do voto-----------------------
bloco1 = ar.Retangulo(ar.Ponto(120, 130), 30, 50, "branco", "preto")
bloco2 = ar.Retangulo(ar.Ponto(152, 130), 30, 50, "branco", "preto")
bloco3 = ar.Retangulo(ar.Ponto(184, 130), 30, 50, "branco", "preto")
bloco4 = ar.Retangulo(ar.Ponto(216, 130), 30, 50, "branco", "preto")
bloco5 = ar.Retangulo(ar.Ponto(248, 130), 30, 50, "branco", "preto")
blocos = [bloco1, bloco2, bloco3, bloco4, bloco5]

# texto dos blocos-----------------------
texto1 = ar.Texto(ar.Ponto(126, 140), "", 20, "preto")
texto2 = ar.Texto(ar.Ponto(158, 140), "", 20, "preto")
texto3 = ar.Texto(ar.Ponto(190, 140), "", 20, "preto")
texto4 = ar.Texto(ar.Ponto(222, 140), "", 20, "preto")
texto5 = ar.Texto(ar.Ponto(254, 140), "", 20, "preto")
bloco_textos = [texto1, texto2, texto3, texto4, texto5]

# botoes acao-----------------------
branco = ar.Botao(ar.Ponto(500, 350), "BRANCO", cor="branco", cor_texto="preto", ao_clicar=voto_branco_confirmavel)
corrige = ar.Botao(ar.Ponto(640, 350), "CORRIGE", cor="laranja", ao_clicar=correcao, cor_texto="preto")
confirma = ar.Botao(ar.Ponto(560, 400), "CONFIRMA", cor="verde", cor_texto="preto", ao_clicar=clique_confirma)
reiniciar_btn = ar.Botao(ar.Ponto(550, 460), "REINICIAR", cor="azul", cor_texto="branco", ao_clicar=reiniciar_votacao)
reiniciar_btn.visivel = False
finalizar_btn = ar.Botao(ar.Ponto(670, 460), "FINALIZAR", cor="verde", cor_texto="preto", ao_clicar=finalizar_apuracao)
finalizar_btn.visivel = False
botoes_numericos = [btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn0]
retangulo_fim = ar.Retangulo(ar.Ponto(0, 0), 800, 600, "#D3D3D3", "preto")
retangulo_fim.visivel = False
texto_fim = ar.Texto(ar.Ponto(245, 180), "FIM", 150, "preto", True)
texto_fim.visivel = False
texto_status_fim = ar.Texto(ar.Ponto(150, 370), "Votação encerrada. CSV salvo em " + ARQUIVO_VOTOS, 22, "preto", True)
texto_status_fim.visivel = False

# basico--------------------
tela.adicionar(retangulo1)
tela.adicionar(retangulo2)
tela.adicionar(retangulo3)
tela.adicionar(justica)
tela.adicionar(cargo1)
tela.adicionar(seu_voto)
tela.adicionar(numero)
tela.adicionar(texto_nome)
tela.adicionar(texto_partido)
tela.adicionar(texto_status)
tela.adicionar(texto_estado)
tela.adicionar(foto_candidato)

# botoes numericos add------------------
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

# texto blocos add------------------
tela.adicionar(texto1)
tela.adicionar(texto2)
tela.adicionar(texto3)
tela.adicionar(texto4)
tela.adicionar(texto5)

# botoes acao-----------------------
tela.adicionar(branco)
tela.adicionar(corrige)
tela.adicionar(confirma)
tela.adicionar(reiniciar_btn)
tela.adicionar(finalizar_btn)

# blocos do voto add-----------------------
tela.adicionar(bloco1)
tela.adicionar(bloco2)
tela.adicionar(bloco3)
tela.adicionar(bloco4)
tela.adicionar(bloco5)
tela.adicionar(retangulo_fim)
tela.adicionar(texto_fim)
tela.adicionar(texto_status_fim)

carregar_etapa()
tela.executar()
