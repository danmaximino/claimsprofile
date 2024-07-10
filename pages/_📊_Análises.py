#############################################
############ Página 02: Análises ############
#############################################

# 01. Importação de Bibliotecas
import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import plotly.express as px
import plotly.graph_objects as go
import openpyxl

# 02. Chamando o DataFrame Nesta Página
df_claim_2 = st.session_state['df_claim_2']

# 03. Formatação de Página
st.set_page_config(layout = 'wide', page_title = 'Perfil de Sinistros', page_icon = '🧐', initial_sidebar_state = 'expanded')

# 04. Colocando Título na Página "Análises"
st.title('Perfil de Sinistros 🧐')

# 05. Definição da Paleta de Cores
color_palette = ['#00CED1', '#FFD700', '#FF6347', '#00CED1', '#00CED1']

# 06. Incluindo Título Para o Campo de Filtros
st.sidebar.markdown("### Filtros Disponíveis")

# 07. Definindo os Filtros

## 7.1 Filtro dos 'Anos'
years = df_claim_2['nr_ano'].unique()
years = sorted(years)
years_selected = st.sidebar.multiselect('Selecione o(s) ano(s)', years, default = years)

## 7.2 Filtro dos 'Meses'
months = df_claim_2['nm_mes'].unique()
months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
months_selected = st.sidebar.multiselect('Selecione o(s) meses(s)', months, default = months)

# 7.3 Filtro das Marcas dos Veículos
makes = df_claim_2['nm_marca'].unique()
makes_selected = st.sidebar.multiselect('Selecione a(s) marca(s)', makes, default = makes)

# 7.4 Filtro de Fraude
fraud_selected = st.sidebar.checkbox('Mostrar apenas fraudes', value = False)

# 7.5 Filtro de Idade
min_age = int(df_claim_2['nr_idade'].min())
max_age = int(df_claim_2['nr_idade'].max())
age_selected = st.sidebar.slider('Selecione o intervalo de idade do condutor', min_value = min_age, max_value = max_age, value = (min_age, max_age))

# 7.6 Aplicação dos Filtros (Criado Novo DataFrame "Filtrado")
df_filtered = df_claim_2[
    (df_claim_2['nr_ano'].isin(years_selected)) &
    (df_claim_2['nm_mes'].isin(months_selected)) &
    (df_claim_2['nm_marca'].isin(makes_selected)) &
    ((df_claim_2['fl_fraude'] == 'Sim') if fraud_selected else True) &
    (df_claim_2['nr_idade'].between(age_selected[0], age_selected[1]))
]

# 7.7 Mensagem Caso Algum Filtro Esteja Vazio
if df_filtered.empty:
    st.write('⚠️ **Nenhum dado disponível para os filtros selecionados. Verifique a inclusão de novos filtros!**')
else:

# 08. Construção dos Gráficos (São 10 Gráficos Divididos Em 05 Blocos, Ou Seja: De 02 em 02 Gráficos Por "Linha")

    ## 8.1 Formatação de Divisão de Página (02 Colunas) > Primeira "Linha" de Gráficos
    col1, col2 = st.columns(2)

    # Gráfico 1: Quantidade de Sinistros Por Ano

    ## Criando a Métrica
    fig_month_year = df_filtered.groupby(['nm_mes', 'nr_ano']).size().reset_index(name='Quantidade')

    ## Aplicando a Ordem dos Meses (Método "Categorical")
    fig_month_year['nm_mes'] = pd.Categorical(fig_month_year['nm_mes'], categories = months, ordered = True)
    fig_month_year = fig_month_year.sort_values('nm_mes')

    ## Calculando Mínimos e Máximos Para Eixo "Y" do Gráfico
    min_qty_year = fig_month_year['Quantidade'].min()
    max_qty_year = fig_month_year['Quantidade'].max()

    ## Criando o Gráfico (Plot)
    plt_month_year = px.line(fig_month_year, x = 'nm_mes', y = 'Quantidade', color = 'nr_ano', category_orders = { 'nr_ano': years}, title = 'Quantidade de Sinistros por Mês e Ano', color_discrete_sequence = color_palette)
    plt_month_year.update_layout(xaxis_title = '', yaxis_title = '', legend=dict(orientation = 'h', yanchor = 'bottom', y = 1.02, xanchor = 'center', x = 0.5, title = None))
    plt_month_year.update_traces(hoverinfo = 'text+name', mode = 'lines+markers')
    plt_month_year.update_yaxes(range = [min_qty_year - 100, max_qty_year + 100])

    ## Exibindo o Gráfico no Streamlit (Na Primeira Coluna)
    with col1:
        st.plotly_chart(plt_month_year)

    # Gráfico 2: Quantidade de Sinistros Por Dia

    ## Criando a Métrica
    fig_days = df_filtered.groupby(['nm_dia', 'nr_ano']).size().reset_index(name = 'Quantidade')

    ## Definindo a Ordem dos Dias da Semana (Seg-Dom)
    day_order = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

    ## Aplicando a Ordem dos Meses (Método "Categorical")
    fig_days['nm_dia'] = pd.Categorical(fig_days['nm_dia'], categories=day_order, ordered=True)
    fig_days = fig_days.sort_values('nm_dia')

    ## Calculando Mínimos e Máximos Para Eixo "Y" do Gráfico
    min_qty_days = fig_days['Quantidade'].min()
    max_qty_days = fig_days['Quantidade'].max()

    ## Criando o Gráfico (Plot)
    plt_days = px.line(fig_days, x = 'nm_dia', y = 'Quantidade', color = 'nr_ano', category_orders = {'nm_dia': day_order}, title = 'Quantidade de Sinistros por Dia e Ano', color_discrete_sequence = color_palette)
    plt_days.update_layout(xaxis_title = '', yaxis_title = '', legend=dict(orientation = 'h', yanchor = 'bottom', y = 1.02, xanchor = 'center', x = 0.5, title = None))
    plt_days.update_traces(hoverinfo = 'text+name', mode = 'lines+markers')
    plt_days.update_yaxes(range = [min_qty_days - 200, max_qty_days + 200])

    ## Exibindo o Gráfico no Streamlit (Na Segunda Coluna)
    with col2:
        st.plotly_chart(plt_days)
    
    ## Terminado o Bloco 01 de Gráficos ##

    ## 8.2 Formatação de Divisão de Página (02 Colunas) > Segunda "Linha" de Gráficos
    col3, col4 = st.columns(2)

    # Gráfico 3: Boxplot de Idade de Condutores (Homens x Mulheres)

    # Definindo Cores Para a Categoria "nm_sexo"
    boxplot_colors = {'Homem': '#00CED1',  'Mulher': '#FFD700'}

    # Criando a Métrica
    fig_ages = df_filtered[['nm_sexo', 'nr_idade']]
    fig_ages.columns = ['Sexo', 'Idade']

    # Setando As Cores Para as Variáveis 'Mulher' e 'Homem'
    unique_sex = fig_ages['Sexo'].unique()
    for sex in unique_sex:
        if sex not in boxplot_colors:
            raise ValueError(f"Sexo '{sex}' não tem cor definida em 'boxplot_colors'.")

    # Criando o Gráfico (Plot)
    plt_ages = px.box(fig_ages, x = 'Sexo', y = 'Idade', title = 'Idade do Condutor: Mulheres x Homens', color = 'Sexo', color_discrete_map = boxplot_colors)
    plt_ages.update_xaxes(title_text = '', showgrid = False)
    plt_ages.update_yaxes(title_text = '', showgrid = False)

    # Cria Linha Para Mostrar "Média" e "Mediana"
    for sex in unique_sex:
        group = fig_ages[fig_ages['Sexo'] == sex]['Idade']
        mean_value = group.mean()
        median_value = group.median()
        
        # Aplica Cor da Barra da Mediana (Não Existe Originalmente no BoxPlot)
        border_color = boxplot_colors[sex]
        
        # Define Posição da Linha da Média e Mediana
        if sex == 'Homem':
            x0 = -0.25
            x1 = 0.25
        else:
            x0 = 0.75
            x1 = 1.25

        # Adição da Linha da Média no BoxPlot
        plt_ages.add_shape(type = 'line', x0 = x0, y0 = mean_value, x1 = x1, y1 = mean_value, xref = 'x', yref = 'y', line = dict(color = border_color, width = 2))
        
        # Adição da Média no BoxPlot
        plt_ages.add_annotation(x = sex, y = mean_value, text = f'<b>Média</b>: {mean_value:.0f}', showarrow = False, yshift = 10,font = dict(color = 'black'))

        # Adição da Mediana no BoxPlot
        plt_ages.add_annotation(x = sex, y = median_value, text=f'<b>Mediana</b>: {median_value:.0f}', showarrow = False, yshift = -10, font = dict(color = 'black'))

    # Atualizações de Formato
    plt_ages.update_layout(xaxis = dict(title_text = '', showgrid = False, zeroline = False), yaxis = dict(title_text = '', showgrid = False, zeroline = False))

    ## Exibindo o Gráfico no Streamlit (Na Primeira Coluna)
    with col3:
        st.plotly_chart(plt_ages)

    # Gráfico 4: Classificação do Motorista

    # Criando a Métrica
    fig_category = df_filtered['nm_cat_motorista'].value_counts().reset_index()
    fig_category.columns = ['Categoria Motorista', 'Quantidade']
    fig_category['Percentual'] = ((fig_category['Quantidade'] / fig_category['Quantidade'].sum()) * 100).round(1)
    fig_category['% Percentual'] = fig_category['Percentual'].astype(str) + '%'

    # Criando o Gráfico (Plot)
    plt_category = px.funnel(fig_category, x = 'Percentual', y = 'Categoria Motorista', text = '% Percentual', title = 'Padrão de Direção (Categoria Telemetria)', color_discrete_sequence = color_palette)
    plt_category.update_yaxes(title_text = '', showgrid = False)
    plt_category.update_layout(xaxis_tickformat = '%')
    plt_category.update_traces(texttemplate = '%{text}', textposition = 'inside', textfont = dict(color = 'white'))

    ## Exibindo o Gráfico no Streamlit (Na Segunda Coluna)
    with col4:
        st.plotly_chart(plt_category)

    ## Terminado o Bloco 02 de Gráficos ##

    ## 8.3 Formatação de Divisão de Página (02 Colunas) > Terceira "Linha" de Gráficos
    col5, col6 = st.columns(2)

    # Gráfico 5: Distribuição das Marcas dos Veículos Sinistrados

    # Criando a Métrica
    fig_make = df_filtered['nm_marca'].value_counts().reset_index()
    fig_make.columns = ['Marca', 'Quantidade']
    fig_make['Percentual'] = ((fig_make['Quantidade'] / fig_make['Quantidade'].sum()) * 100).round(1)

    # Criando o Gráfico (Plot)
    plt_make = px.bar(fig_make, x = 'Marca', y = 'Percentual', color_discrete_sequence = color_palette, title = 'Distribuição por Marca', text = 'Percentual')
    plt_make.update_traces(texttemplate = '%{y:.1f}%', textposition = 'outside')
    plt_make.update_xaxes(title_text = 'Marca', showgrid = False)
    plt_make.update_yaxes(title_text = 'Percentual', showgrid = False)
    plt_make.update_layout(yaxis = dict( tickmode = 'array', tickvals = [i for i in range(0, 101, 10)], ticktext = [f'{i}%' for i in range(0, 101, 10)], range = [0, fig_make['Percentual'].max() + 10]), bargap = 0.02)

    ## Exibindo o Gráfico no Streamlit (Na Primeira Coluna)
    with col5:
        st.plotly_chart(plt_make)

    # Gráfico 6: Histograma dos Valores dos Veículos Sinistrados

    # Criando a Métrica
    fig_vhc_price = df_filtered['nm_preco_veiculo'].value_counts().reset_index()
    fig_vhc_price.columns = ['Preço do Veículo', 'Quantidade']
    fig_vhc_price['Percentual'] = ((fig_vhc_price['Quantidade'] / fig_vhc_price['Quantidade'].sum()) * 100).round(1)
    price_order = ['< 30K', '30K até 49K', '50K até 69K', '70K até 89K', '90K até 150K', '> 150K']

    # Criando o Gráfico (Plot)
    plt_vhc_price = px.histogram(fig_vhc_price, x = 'Preço do Veículo', y = 'Percentual', category_orders = {'Preço do Veículo': price_order}, title = 'Histograma - Preço dos Veículos', color_discrete_sequence = color_palette)

    # Incluindo os Números Acima das Barras
    for index, row in fig_vhc_price.iterrows():
        plt_vhc_price.add_trace(
            go.Scatter(x = [row['Preço do Veículo']], y = [row['Percentual'] + 1], text = [f"{row['Percentual']}%"], mode = 'text', showlegend = False))

    # Demais Personalizações do Gráficoå
    plt_vhc_price.update_xaxes(title_text = 'Faixas de Preço do Veículo', showgrid = False)
    plt_vhc_price.update_yaxes(title_text = 'Percentual', showgrid = False, tickformat = '')
    plt_vhc_price.update_layout(bargap = 0.02)


    ## Calculando Máximos Para Eixo "Y"
    max_perc = fig_vhc_price['Percentual'].max()
    max_perc_margin = (max_perc // 10 + 1) * 10 # Aumento da Margem Para Melhor Visualização do Usuário

    ## Atualização do Plot do Gráfico
    plt_vhc_price.update_layout(yaxis = dict(tickmode = 'array', tickvals = [i for i in range(0, int(fig_vhc_price['Percentual'].max()) + 10, 10)], ticktext = [f"{i}%" for i in range(0, int(fig_vhc_price['Percentual'].max()) + 10, 10)], range = [0, max_perc_margin]))

    ## Exibindo o Gráfico no Streamlit (Na Segunda Coluna)
    with col6:
        st.plotly_chart(plt_vhc_price)

    ## Terminado o Bloco 03 de Gráficos ##
    
    ## 8.4 Formatação de Divisão de Página (02 Colunas) > Quarta "Linha" de Gráficos
    col7, col8 = st.columns(2)

    # Gráfico 7: Categoria de Veículos

    # Criando a Métrica
    fig_cat_cars = df_filtered['nm_categoria_veiculo'].value_counts().reset_index()
    fig_cat_cars.columns = ['Categoria do Veículo', 'Quantidade']

    # Criando o Gráfico (Plot)
    plt_cat_cars = px.pie(fig_cat_cars, values = 'Quantidade', names = 'Categoria do Veículo', hole = 0.6, title = '% Por Categoria do Veículo', color_discrete_sequence = color_palette)
    plt_cat_cars.update_traces(textposition = 'outside', textinfo = 'percent')
    plt_cat_cars.update_layout(legend = dict(orientation = 'h', yanchor = 'bottom', y = 1.05, xanchor = 'center', x = 0.5, title = None))

    ## Exibindo o Gráfico no Streamlit (Na Primeira Coluna)
    with col7:
        st.plotly_chart(plt_cat_cars)

    # Gráfico 8: Sinistros em Trechos Rurais x Urbanos

    # Criando a Métrica
    fig_accident = df_filtered['nm_tipo_trecho'].value_counts().reset_index()
    fig_accident.columns = ['Tipo de Trecho', 'Quantidade']

    # Criando o Gráfico (Plot)
    plt_accident = px.pie(fig_accident, values = 'Quantidade', names = 'Tipo de Trecho', hole = 0.6, title = '% Trechos Urbanos vs Rurais', color_discrete_sequence = color_palette)
    plt_accident.update_traces(textposition = 'outside', textinfo = 'percent')
    plt_accident.update_layout(legend = dict(orientation = 'h', yanchor = 'bottom', y = 1.05, xanchor = 'center', x = 0.5, title = None))

    ## Exibindo o Gráfico no Streamlit (Na Segunda Coluna)
    with col8:
        st.plotly_chart(plt_accident)

    ## Terminado o Bloco 04 de Gráficos ##

    ## 8.5 Formatação de Divisão de Página (02 Colunas) > Quinta "Linha" de Gráficos
    col9, col10 = st.columns(2)

    # Gráfico 9: Culpabilidade de Terceiros

    # Criando a Métrica
    fig_fault = df_filtered['fl_culpa_terceiros'].value_counts().reset_index()
    fig_fault.columns = ['Culpa de Terceiros', 'Quantidade']

    # Criando o Gráfico (Plot)
    plt_fault = px.pie(fig_fault, values = 'Quantidade', names = 'Culpa de Terceiros', hole = 0.6, title = '% Culpa de Terceiros', color_discrete_sequence = color_palette)
    plt_fault.update_traces(textposition = 'outside', textinfo = 'percent')
    plt_fault.update_layout(legend = dict(orientation = 'h', yanchor = 'bottom', y = 1.05, xanchor = 'center', x = 0.5, title = None))

    ## Exibindo o Gráfico no Streamlit (Na Primeira Coluna)
    with col9:
        st.plotly_chart(plt_fault)

    # Gráfico 10: Sinistros Fraudulentos

    # Criando a Métrica
    fig_fraud = df_filtered['fl_fraude'].value_counts().reset_index()
    fig_fraud.columns = ['Sinistros de Fraude', 'Quantidade']

    # Criando o Gráfico (Plot)
    plt_fraud = px.pie(fig_fraud, values = 'Quantidade', names = 'Sinistros de Fraude', hole = 0.6, title = '% Sinistros de Fraude', color_discrete_sequence = color_palette)
    plt_fraud.update_traces(textposition = 'outside', textinfo = 'percent')
    plt_fraud.update_layout(legend = dict(orientation = 'h', yanchor = 'bottom', y = 1.05, xanchor = 'center', x = 0.5, title = None))

    ## Exibindo o Gráfico no Streamlit (Na Segunda Coluna)
    with col10:
        st.plotly_chart(plt_fraud)

# 09. Mensagem Final (Dev)
st.markdown('''
<div style='font-size: 17px;'>
    <br>
    <b>Desenvolvido por:</b> Danielle B. Maximino<br>
    <b>Objetivo:</b> Estudo das Bibliotecas Streamlit e Plotly
</div> </br>
''', unsafe_allow_html = True)