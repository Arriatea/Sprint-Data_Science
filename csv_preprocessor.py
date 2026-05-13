import pandas as pd
from pathlib import Path
import re

def montar_registro(texto_registro):
    texto_registro = texto_registro.strip() # Remove espaços vazios no começo e no final do registro.

    if texto_registro.startswith('"'): # Verifica se o registro começa com aspas duplas.
        texto_registro = texto_registro[1:] # Remove a primeira aspas do registro.

    if texto_registro.endswith('"'): # Verifica se o registro termina com aspas duplas.
        texto_registro = texto_registro[:-1] # Remove a última aspas do registro.

    partes_iniciais = texto_registro.split(",", 10) # Divide o registro nas 10 primeiras vírgulas, separando os campos iniciais.

    if len(partes_iniciais) < 11: # Verifica se o registro não possui a quantidade mínima de campos esperada.
        return None # Retorna vazio caso o registro esteja incompleto.

    campos_finais = partes_iniciais[10].rsplit(",", 7) # Divide o final do registro da direita para a esquerda, separando os últimos campos.

    if len(campos_finais) == 8: # Verifica se os campos finais foram separados corretamente.
        anon_transcricao = campos_finais[0] # Guarda o texto da transcrição.
        uf = campos_finais[1] # Guarda a UF.
        cnae = campos_finais[2] # Guarda o CNAE.
        nome_unidade = campos_finais[3] # Guarda o nome da unidade.
        nome_segmento = campos_finais[4] # Guarda o nome do segmento.
        faixa_faturamento_cliente_ec = campos_finais[5] # Guarda a faixa de faturamento do cliente.
        dt_ultima_pesquisa = campos_finais[6] # Guarda a data da última pesquisa.
        nota_nps = campos_finais[7] # Guarda a nota NPS.
    else:
        anon_transcricao = partes_iniciais[10] # Caso os campos finais não sejam separados, mantém o restante como transcrição.
        uf = pd.NA # Define UF como valor vazio.
        cnae = pd.NA # Define CNAE como valor vazio.
        nome_unidade = pd.NA # Define nome da unidade como valor vazio.
        nome_segmento = pd.NA # Define nome do segmento como valor vazio.
        faixa_faturamento_cliente_ec = pd.NA # Define faixa de faturamento como valor vazio.
        dt_ultima_pesquisa = pd.NA # Define data da última pesquisa como valor vazio.
        nota_nps = pd.NA # Define nota NPS como valor vazio.

    return { # Retorna um dicionário com os dados organizados em colunas.
        "id_meeting": partes_iniciais[0],
        "dt_meeting": partes_iniciais[1],
        "formato_meeting": partes_iniciais[2],
        "id_status_meeting": partes_iniciais[3],
        "status_meeting": partes_iniciais[4],
        "duracao_meeting": partes_iniciais[5],
        "codt": partes_iniciais[6],
        "tp_recurso": partes_iniciais[7],
        "flg_externo": partes_iniciais[8],
        "dt_criacao": partes_iniciais[9],
        "anon_transcricao": anon_transcricao.strip().strip('"').replace('""', '"'), # Limpa a transcrição e corrige aspas duplicadas.
        "uf": uf,
        "cnae": cnae,
        "nome_unidade": nome_unidade,
        "nome_segmento": nome_segmento,
        "faixa_faturamento_cliente_ec": faixa_faturamento_cliente_ec,
        "dt_ultima_pesquisa": dt_ultima_pesquisa,
        "nota_nps": nota_nps
    }


def gerar_chunks_corrigidos(csv_inicial, tamanho_chunk):
    registros = [] # Lista que guarda os registros tratados antes de formar um chunk.
    registro_atual = [] # Lista que guarda as linhas da reunião atual.

    with open(csv_inicial, "r", encoding="latin-1") as arquivo: # Abre o CSV usando latin-1 para evitar erro com caracteres especiais.
        next(arquivo) # Pula o cabeçalho do CSV.

        for linha in arquivo: # Percorre o arquivo linha por linha.
            linha = linha.rstrip("\n") # Remove a quebra de linha do final.

            if re.match(r'^"?\d+,\d{4}-\d{2}-\d{2}', linha): # Verifica se a linha indica o começo de uma nova reunião.
                if registro_atual: # Verifica se já existe uma reunião sendo montada.
                    registro = montar_registro("\n".join(registro_atual)) # Junta as linhas da reunião e transforma em um registro organizado.

                    if registro is not None: # Verifica se o registro foi montado corretamente.
                        registros.append(registro) # Adiciona o registro tratado na lista.

                    if len(registros) >= tamanho_chunk: # Verifica se a quantidade de registros atingiu o tamanho do chunk.
                        yield pd.DataFrame(registros) # Retorna um DataFrame com os registros do chunk.
                        registros = [] # Limpa a lista para começar o próximo chunk.

                registro_atual = [linha] # Começa uma nova reunião com a linha atual.

            else:
                registro_atual.append(linha) # Adiciona a linha atual como continuação da transcrição.

        if registro_atual: # Verifica se ainda existe uma reunião montada no final do arquivo.
            registro = montar_registro("\n".join(registro_atual)) # Monta o último registro do arquivo.

            if registro is not None: # Verifica se o último registro foi montado corretamente.
                registros.append(registro) # Adiciona o último registro na lista.

        if registros: # Verifica se ainda existem registros que não foram salvos em um chunk.
            yield pd.DataFrame(registros) # Retorna o último chunk.


def limpar_csv(csv_inicial, csv_tratado):
    tamanho_chunk = 1000 # Define quantas reuniões serão tratadas por vez.

    csv_tratado.parent.mkdir(parents=True, exist_ok=True) # Cria a pasta para o CSV tratado caso ela não exista.

    if csv_tratado.exists(): # Verifica se o CSV tratado já existe.
        csv_tratado.unlink() # Apaga o CSV tratado caso o arquivo já exista.

    primeiro_chunk = True # Controla se o cabeçalho das colunas deve ser escrito no arquivo.

    total_linhas = 0 # Guarda a quantidade total de linhas tratadas.
    total_colunas = 0 # Guarda a quantidade total de colunas tratadas.

    for df in gerar_chunks_corrigidos(csv_inicial, tamanho_chunk): # Percorre cada chunk corrigido do CSV.
        df.columns = (
            df.columns
            .str.strip() # Remove espaços em branco.
            .str.lower() # Deixa tudo em lower case.
            .str.replace(" ", "_") # 1º parametro define oque sera trocado, 2º parametro define oque vai ser colocado no lugar.
        )

        df = df.drop_duplicates() # Metodo que remove duplicatas.

        for coluna in df.columns:
            if df[coluna].dtype == "object": # Verfica se uma coluna é um texto.
                df[coluna] = df[coluna].astype(str).str.strip() # Transforma o texto em string e corta os espaços vazios.

        valores_nulos = ["", " ", "null", "none", "nan", "na", "n/a", "-", "nao informado", "não informado"]

        df = df.replace(valores_nulos, pd.NA) # Troca valores vazios por NA.

        df.to_csv(
            csv_tratado,
            mode="a", # Adiciona cada bloco tratado no final do arquivo.
            index=False, # Impede o pandas de criar uma coluna extra com o índice das linhas.
            header=primeiro_chunk # Escreve o nome das colunas apenas no primeiro bloco.
        )

        primeiro_chunk = False # Depois do primeiro chunk, impede que o cabeçalho seja escrito novamente.
        total_linhas += df.shape[0] # Soma a quantidade de linhas tratadas no total.
        total_colunas = df.shape[1] # Guarda a quantidade de colunas do CSV tratado.

    print("CSV tratado!")
    print(f"Linhas: {total_linhas}") # Print para ver se tudo deu certo.
    print(f"Colunas: {total_colunas}") # Print para ver se tudo deu certo.


BASE_DIR = Path(__file__).resolve().parent # Pega a pasta onde este arquivo python está salvo.

csv_inicial = BASE_DIR / "data" / "raw" / "ANON_nome_transcricao.csv" # Define o caminho do CSV original.
csv_tratado = BASE_DIR / "data" / "processed" / "csv_tratado.csv" # Define o caminho onde o CSV tratado será salvo.

limpar_csv(csv_inicial, csv_tratado) # Chama a função para iniciar o tratamento do CSV.