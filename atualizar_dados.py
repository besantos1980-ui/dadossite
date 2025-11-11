import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# --- Configurações ---
NOME_PLANILHA_GOOGLE = "Dados"
# Nome da aba específica que você quer ler (ex: 'Página1' ou 'Sheet1')
NOME_DA_ABA = "Página1" 
ARQUIVO_CREDENCIAL = 'credentials.json'
ARQUIVO_SAIDA_HTML = 'index.html' # O nome do arquivo HTML que será gerado
# ---------------------

def autenticar():
    """Autentica no Google usando o arquivo JSON de credenciais."""
    try:
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(ARQUIVO_CREDENCIAL, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Erro ao autenticar: {e}")
        print("Verifique se o 'credentials.json' está presente e se a API Google Sheets está ativa.")
        return None

def buscar_dados(client):
    """Busca os dados da planilha especificada."""
    try:
        planilha = client.open(NOME_PLANILHA_GOOGLE).worksheet(NOME_DA_ABA)
        # Pega todos os valores da aba
        dados = planilha.get_all_values() 
        return dados
    except gspread.exceptions.WorksheetNotFound:
        print(f"Erro: A aba '{NOME_DA_ABA}' não foi encontrada na planilha '{NOME_PLANILHA_GOOGLE}'.")
        return None
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return None

def gerar_html(dados):
    """Gera uma string HTML formatada como uma tabela a partir dos dados."""
    if not dados:
        return "<html><body><p>Nenhum dado encontrado.</p></body></html>"

    # Assume a primeira linha como cabeçalho
    cabecalho = dados[0]
    linhas_de_dados = dados[1:]

    # --- Início do HTML ---
    html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dados Atualizados</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 90%; margin: auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f4f4f4; color: #333; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>Relatório de Dados Automatizado</h1>
    <table>
"""
    # --- Cabeçalho da Tabela ---
    html += "        <thead>\n            <tr>\n"
    for item in cabecalho:
        html += f"                <th>{item}</th>\n"
    html += "            </tr>\n        </thead>\n"

    # --- Corpo da Tabela ---
    html += "        <tbody>\n"
    for linha in linhas_de_dados:
        html += "            <tr>\n"
        for item in linha:
            html += f"                <td>{item}</td>\n"
        html += "            </tr>\n"
    html += "        </tbody>\n"

    # --- Fim do HTML ---
    html += """
    </table>
</body>
</html>
"""
    return html

def salvar_arquivo(conteudo):
    """Salva o conteúdo HTML no arquivo de saída."""
    try:
        with open(ARQUIVO_SAIDA_HTML, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"Sucesso! Arquivo '{ARQUIVO_SAIDA_HTML}' gerado.")
    except Exception as e:
        print(f"Erro ao salvar arquivo HTML: {e}")

# --- Execução Principal ---
if __name__ == "__main__":
    if not os.path.exists(ARQUIVO_CREDENCIAL):
        print(f"Erro fatal: Arquivo de credenciais '{ARQUIVO_CREDENCIAL}' não encontrado.")
        print("Certifique-se de que o workflow do GitHub está criando este arquivo a partir do Secret.")
    else:
        client = autenticar()
        if client:
            dados = buscar_dados(client)
            if dados:
                html_content = gerar_html(dados)
                salvar_arquivo(html_content)
