import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO
# ============================================================

# ID da sua planilha Google Sheets (aparece na URL)
PLANILHA_ID = "15B9A_VCdgrBKJE27AF0oTzG4KCWOBnPfYRRdDHM8_9k"
NOME_ABA = "Dados"  # Nome da aba da planilha

# ============================================================
# CONECTAR AO GOOGLE SHEETS
# ============================================================

def conectar_planilha():
    """Autentica e conecta à planilha Google"""
    scope = ['https://spreadsheets.google.com/feeds', 
             'https://www.googleapis.com/auth/drive']
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope
    )
    client = gspread.authorize(creds)
    planilha = client.open_by_key(PLANILHA_ID)
    aba = planilha.worksheet(NOME_ABA)
    
    return aba

# ============================================================
# LER DADOS
# ============================================================

def ler_dados(aba):
    """Lê todos os registros da aba"""
    records = aba.get_all_records()
    return records

# ============================================================
# GERAR HTML
# ============================================================

def gerar_html(dados):
    """Cria a página HTML com formatação profissional"""
    
    data_atualizacao = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indicadores de Saúde Suplementar</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .info-timestamp {{
            text-align: right;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }}
        
        .card-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 8px;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        
        .card-value {{
            font-size: 1.8em;
            color: #667eea;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        
        .card-source {{
            font-size: 0.85em;
            color: #999;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        th {{
            background: #f0f0f0;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #ddd;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        
        tr:hover {{
            background: #fafafa;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Indicadores de Saúde Suplementar</h1>
            <p>Dados agregados em tempo real</p>
        </div>
        
        <div class="content">
            <div class="info-timestamp">
                ✓ Última atualização: <strong>{data_atualizacao}</strong>
            </div>
            
            <div class="grid">
"""
    
    # Adiciona cada indicador como um card
    for idx, linha in enumerate(dados):
        if idx >= 6:  # Limita a 6 cards na grid (2 linhas x 3 colunas)
            break
        
        indicador = linha.get('Indicador', 'N/A')
        valor = linha.get('Valor', 'N/A')
        fonte = linha.get('Fonte', 'N/A')
        
        html += f"""            <div class="card">
                <div class="card-label">{indicador}</div>
                <div class="card-value">{valor}</div>
                <div class="card-source">📍 {fonte}</div>
            </div>
"""
    
    html += """            </div>
            
            <h2 style="margin-top: 40px; margin-bottom: 20px; color: #333;">
                📋 Dados Completos
            </h2>
            
            <table>
                <thead>
                    <tr>
                        <th>Indicador</th>
                        <th>Valor</th>
                        <th>Fonte</th>
                        <th>Data</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Adiciona todas as linhas na tabela
    for linha in dados:
        indicador = linha.get('Indicador', 'N/A')
        valor = linha.get('Valor', 'N/A')
        fonte = linha.get('Fonte', 'N/A')
        data = linha.get('Data', 'N/A')
        
        html += f"""                    <tr>
                        <td>{indicador}</td>
                        <td><strong>{valor}</strong></td>
                        <td>{fonte}</td>
                        <td>{data}</td>
                    </tr>
"""
    
    html += """                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>🔄 Esta página é atualizada automaticamente quando há mudanças na planilha-fonte</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

# ============================================================
# SALVAR ARQUIVO
# ============================================================

def salvar_html(html, nome_arquivo="index.html"):
    """Salva o HTML em arquivo"""
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ Arquivo '{nome_arquivo}' gerado com sucesso!")

# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    print("🔄 Iniciando atualização de dados...")
    
    try:
        aba = conectar_planilha()
        print("✓ Conectado ao Google Sheets")
        
        dados = ler_dados(aba)
        print(f"✓ Lidos {len(dados)} registros")
        
        html = gerar_html(dados)
        print("✓ HTML gerado")
        
        salvar_html(html)
        print("✅ Processo concluído com sucesso!")
        
    except Exception as erro:
        print(f"❌ Erro: {erro}")
        exit(1)
