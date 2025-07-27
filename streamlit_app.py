import pandas as pd
import streamlit as st
import plotly.express as px

# === 1. Lê os arquivos ===

# Preços da ação
df_precos = pd.read_csv('cota.csv')
df_precos.columns = df_precos.columns.str.strip()
df_precos['Data'] = pd.to_datetime(df_precos['Data'], dayfirst=True)
df_precos['Mínima'] = df_precos['Mínima'].str.replace(',', '.').astype(float)
df_precos['Mês'] = df_precos['Data'].dt.to_period('M')

# Dividendos pagos
df_divs = pd.read_csv('div.csv')
df_divs.columns = df_divs.columns.str.strip()
df_divs['Pagamento'] = pd.to_datetime(df_divs['Pagamento'], dayfirst=True)
df_divs['Valor'] = df_divs['Valor'].str.replace(',', '.').astype(float)
df_divs['Mês'] = df_divs['Pagamento'].dt.to_period('M')

# === 2. Simulação de compras mensais ===

quantidade_total = 0
investimento_total = 0.0
historico = []
acumulado_dividendos = 0  # Inicializa a variável de dividendos acumulados

# Ordena meses de forma crescente
meses = sorted(df_precos['Mês'].unique())

for mes in meses:
    dados_mes = df_precos[df_precos['Mês'] == mes]
    if dados_mes.empty:
        continue

    preco_compra = dados_mes['Mínima'].min()
    valor_mes = preco_compra * 10
    quantidade_total += 10
    investimento_total += valor_mes

    # Verifica dividendos naquele mês
    divs_mes = df_divs[df_divs['Mês'] == mes]
    total_proventos = (divs_mes['Valor'].sum()) * quantidade_total if not divs_mes.empty else 0
    
    # Atualiza o acumulado de dividendos
    acumulado_dividendos += total_proventos
    
    historico.append({
        'Mês': str(mes),
        'Preço Mínimo': round(preco_compra, 2),
        'Comprado': 10,
        'Valor Investido no Mês': round(valor_mes, 2),
        'Total Ações': quantidade_total,
        'Total Investido': round(investimento_total, 2),
        'Dividendos Recebidos': round(total_proventos, 2),
        'Total + Dividendos': round(investimento_total + acumulado_dividendos, 2)
    })

# === 3. Exibe o histórico mês a mês ===

df_resultado = pd.DataFrame(historico)

# Título da interface
st.title("Simulação de Investimentos - Petrobras")

# Exibe a tabela com os resultados
st.write("### Histórico de Compras e Dividendos", df_resultado)

# Gráfico total + dividendos
fig = px.line(df_resultado, x='Mês', y='Total + Dividendos', 
              title='Total Investido + Dividendos ao Longo do Tempo', 
              labels={'Mês': 'Mês', 'Total + Dividendos': 'Valor (R$)'})
st.plotly_chart(fig)

# Gráfico de barras com dividendos recebidos por mês
fig_dividendos = px.bar(df_resultado, x='Mês', y='Dividendos Recebidos',
                        title='Dividendos Recebidos por Mês',
                        labels={'Mês': 'Mês', 'Dividendos Recebidos': 'Dividendos (R$)'})
st.plotly_chart(fig_dividendos)

# Gráfico de total investido ao longo do tempo
fig_investido = px.line(df_resultado, x='Mês', y='Total Investido',
                        title='Total Investido ao Longo do Tempo',
                        labels={'Mês': 'Mês', 'Total Investido': 'Investimento (R$)'})
st.plotly_chart(fig_investido)
