import pandas as pd
from pathlib import Path

def limpar_csv(csv_inicial, csv_tratado):
    df = pd.read_csv(
        csv_inicial,
        encoding = "latin-1", # Permite ler arquivos com caracteres especiais que não estão em UTF-8.
        sep = ",", # Indica ao metodo que as colunas do CSV é separado por ,
        engine = "python", #Faz o pandas usar um leitor de CSV mais flexivel.
        quotechar = '"', # Indica o metodo que o CSV protege os dados utilizando aspas duplas. 
        doublequote = True, # Permite lidar com aspas duplicadas no CSV.
        on_bad_lines = "skip" # Ignora linhas com quantidade errada de colunas.
    )
    
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
        
    csv_tratado.parent.mkdir(parents = True, exist_ok = True) # 1º parametro cria a pasta para o CSV tratado 2º parametro evita erro caso o arquivo ja exista.
        
    df.to_csv(csv_tratado, index = False) # 1º parametro é onde o arquivo sera salvo 2º parametro impede o pandas de criar uma coluna extra com o índice das linhas.
        
    print("CSV tratado!")
    print(f"Linhas: {df.shape[0]} ") # Print para ver se tudo deu certo.
    print(f"Colunas: {df.shape[1]} ")
 
        
    
BASE_DIR = Path (__file__).resolve().parent #Pega a pasta onde este arquivo python está salvo.     
csv_inicial = BASE_DIR / "data" / "raw" / "ANON_nome_transcricao.csv"
csv_tratado = BASE_DIR / "data" / "processed" / "csv_tratado.csv" 
        
        
limpar_csv(csv_inicial, csv_tratado)

