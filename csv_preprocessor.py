import pandas as pd
from pathlib import Path

def limpar_csv(csv_inicial, csv_tratado):
    tamanho_chunk = 1000 # Define quantas linhas do CSV serão lidas por vez.
    
    chunks = pd.read_csv(
        csv_inicial,
        encoding = "latin-1", # Permite ler arquivos com caracteres especiais que não estão em UTF-8.
        sep = ",", # Indica ao metodo que as colunas do CSV são separadas por vírgula.
        engine = "python", # Faz o pandas usar um leitor de CSV mais flexivel.
        quotechar = '"', # Indica ao metodo que o CSV protege os dados utilizando aspas duplas.
        doublequote = True, # Permite lidar com aspas duplicadas no CSV.
        on_bad_lines = "skip", # Ignora linhas com quantidade errada de colunas.
        chunksize = tamanho_chunk # Faz o CSV ser lido em blocos.
    )
    
    csv_tratado.parent.mkdir(parents=True, exist_ok=True) # Cria a pasta para o CSV tratado caso ela não exista.
    
    if csv_tratado.exists():
        csv_tratado.unlink() # Apaga o CSV tratado caso o arquivo ja exista.
        
    primeiro_chunk = True # Controla se o cabeçalho das colunas deve ser escrito no arquivo.
    
    total_linhas = 0
    total_colunas = 0
    
    for df in chunks:
        df.columns = (
            df.columns
            .str.strip() # Remove espaços em branco.
            .str.lower() # Deixa tudo em Lower Case.
            .str.replace(" ", "_") # 1º parametro define oque sera trocado, 2º parametro define oque vai ser colocado no lugar.
        )
        
        df = df.drop_duplicates() # Metodo que remove duplicatas.
        
        for coluna in df.columns:
            if df[coluna].dtype == "object": # Verfica se uma coluna é um texto.
                df[coluna] = df[coluna].astype(str).str.strip() # Transforma o texto em string e corta os espaços vazios.
                
        valores_nulos = ["", " ", "null", "none", "nan", "na", "n/a", "-", "nao informado"]
        
        df = df.replace(valores_nulos, pd.NA) # Troca valores vazios por NA.
            
        df.to_csv(
            csv_tratado,
            mode="a", # Adiciona cada bloco tratado no final do arquivo.
            index=False, # Impede o pandas de criar uma coluna extra com o índice das linhas.
            header=primeiro_chunk # Escreve o nome das colunas apenas no primeiro bloco.
        )
        
        primeiro_chunk = False
        total_linhas += df.shape[0]
        total_colunas = df.shape[1]
        
    print("CSV tratado!")
    print(f"Linhas: {total_linhas}") # Print para ver se tudo deu certo.
    print(f"Colunas: {total_colunas}")
 
    
BASE_DIR = Path(__file__).resolve().parent # Pega a pasta onde este arquivo python está salvo.

csv_inicial = BASE_DIR / "data" / "raw" / "ANON_nome_transcricao.csv"
csv_tratado = BASE_DIR / "data" / "processed" / "csv_tratado.csv" 
        
limpar_csv(csv_inicial, csv_tratado)