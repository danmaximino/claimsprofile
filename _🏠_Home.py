#############################################
############## Página 01: Home ##############
#############################################

# 01. Importação de Bibliotecas
import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import plotly.express as px
import openpyxl

# 02. Chamada da Página Web
st.set_page_config(layout = 'wide', page_title = 'Perfil de Sinistros', page_icon = '🧐', initial_sidebar_state = 'expanded')

# 03. Importação do Dataset (Formato Excel .xlsx)
df_claim = pd.read_csv('sinistros.csv', encoding='utf-8', sep = ';')

# 04. Transformações no Dataset

## 4.1 Reordenar as Colunas

df_claim = df_claim[['nr_apolice', 'nm_tipo_apolice', 'nr_ano', 'nm_mes', 'nm_dia', 'nm_tipo_trecho', 'nm_sexo', 'nm_status_marital', 'nr_idade', 'nm_cat_motorista', 'nm_marca', 'nm_categoria_veiculo', 'nm_preco_veiculo', 'nr_idade_veiculo', 'fl_fraude', 'fl_culpa_terceiros', 'nr_outros_sinistros', 'fl_testemunhas', 'nr_carros_envolvidos']]

## 4.2 Transformar '0 e 1' em 'Sim e Não' (colunas fl_culpa_terceiros, fl_fraude e nm_testemunhas)
df_colunas_sub = ['fl_culpa_terceiros', 'fl_fraude', 'fl_testemunhas']
df_claim[df_colunas_sub] = df_claim[df_colunas_sub].replace({0: 'Não', 1: 'Sim'})

## 4.3 Checagem de Linhas Nulas e Formato das Colunas (Verificar Se Precisa Alterar Algo)
df_claim.info() # sem linhas nulas para as colunas (alterar apenas formato das colunas "nr_apolice" e "nr_ano" str)

## 4.4 Alterando o Formato das Colunas "nr_apolice" e "nr_ano" para String
df_claim['nr_apolice'] = df_claim['nr_apolice'].astype(str)
df_claim['nr_ano'] = df_claim['nr_ano'].astype(str)

# 05. Comando Para Replicar DataFrame Nas Demais Páginas
st.session_state['df_claim_2'] = df_claim

# 06. Descrição do Dashboard (Title e Markdown)

## 6.1 Incluindo o Título da Página "Home"

st.title('Perfil de Sinistros 🧐')

## 6.2 Incluindo o Texto Introdutório na Página "Home"

st.markdown('''
<div style='font-size: 20px;'>
    Olá 👋🏻 </br>
    Esse dash apresenta as <b>principais características</b> (perfil) dos sinistros de <b>automóvel</b> ocorridos entre os anos de <b>2021 e 2023</b> 🚘 </br>
</div>
''', unsafe_allow_html = True)

st.markdown("<h2 style='font-size: 20px;'>Dicas Importantes 🎖️</h2>", unsafe_allow_html = True)

st.markdown('''
<div style='font-size: 20px;'>
    <div style="margin-left: 2em;">
        → Se quiser ir direto para os gráficos, basta ir até o menu lateral e selecionar a opção "📊 <b>Análises</b>"
    </div>
    <div style="margin-left: 2em;">
        → Se tiver dúvidas de conceitos, veja abaixo o "<b>Dicionário de Dados</b> 📕"
    </div>
    <div style="margin-left: 2em;">
        → Caso queira ver ou fazer o download da base de dados, vá até o final desta página no item "<b>Base de Dados Para Download</b> ⤵️"
    </div>
</div> </br>
''', unsafe_allow_html = True)

# 07. Dicionário de Dados

## 7.1 Título Para Identificar o Dicionário de Dados
st.subheader('Dicionário de Dados 📕')

## 7.2 Criação do Dicionário de Dados
df_data_dictionary = {
    'nome do campo': [
        'número da apólice', 'tipo de apólice', 'ano do sinistro', 'mês do sinistro', 
        'dia do sinistro', 'tipo de trecho', 'sexo do condutor', 'status marital do condutor', 
        'idade do condutor', 'categoria do motorista', 'marca do veículo', 'categoria do veículo',
        'faixas de preço do veículo', 'idade do veículo', 'indicador de fraude', 
        'sinistro causado por terceiros', 'outros sinistros na apólice', 'fl_testemunhas', 'nr_carros_envolvidos'
    ], 
    'nome snake_case': [
        'nr_apolice', 'nm_tipo_apolice', 'nr_ano', 'nm_mes', 'nm_dia', 
        'nm_tipo_trecho', 'nm_sexo', 'nm_status_marital', 'nr_idade', 'nm_cat_motorista', 'nm_marca',
        'nm_categoria_veiculo', 'nm_preco_veiculo', 'nr_idade_veiculo', 'fl_fraude', 
        'fl_culpa_terceiros', 'nr_outros_sinistros', 'fl_testemunhas', 'nr_carros_envolvidos'
    ], 
    'definição do campo': [
        'número da apólice (contrato de seguro)', 
        'nome do tipo de apólice (quais coberturas o contrato possui → se cobre só segurado, só terceiro ou ambos)', 
        'ano da ocorrência do sinistro', 'mês de ocorrência do sinistro', 
        'dia da semana em que aconteceu o sinistro', 
        'tipo de local que aconteceu o sinistro → se foi trecho urbano ou rural', 
        'sexo do condutor → se mulher ou homem', 
        'status marital do condutor → se é solteiro, casado, divorciado ou viúvo', 
        'idade do condutor no momento do sinistro', 
        'categoria do motorista segurado (capturado pela telemetria)',
        'marca do veículo no qual ocorreu o sinistro',
        'categoria do veículo no qual ocorreu o sinistro (esportivo, sedan ou utilitário)', 
        'faixas de preço do veículo no qual ocorreu o sinistro', 
        'faixas de idade do veículo no qual ocorreu o sinistro', 
        'indica se foi constatada fraude no sinistro (se marcado "Sim", possui fraude)', 
        'indica se o sinistro foi causado pelo próprio segurado ("Não") ou por terceiros ("Sim")',
        'faixas de outros sinistros relacionados à mesma apólice', 
        'indica se houve testemunhas no momento do sinistro ("Sim") ou não houvve ("Não")', 
        'faixas para quantificar os carros envolvidos no sinistro'
    ]
}

## 7.3 Transformação do Dicionário em DataFrame
df_data_dictionary = pd.DataFrame(df_data_dictionary)

## 7.4 Define o "Index" Começando em 01
df_data_dictionary.index = df_data_dictionary.index + 1

## 7.5 Alterando a Coluna "Index" Para o Nome "ID"
df_data_dictionary.index.name = 'id'

## 7.6 Plotando o Dicionário de Dados na Página "Home"
st.dataframe(df_data_dictionary, use_container_width = True)

# 08. Disponibilização da Base de Dados

## 8.1 Título Para Identificar a Base de Dados
st.subheader('Base de Dados Para Download ⤵️')

st.markdown('''
<div style='font-size: 20px;'>
    Aqui está a base de dados que alimenta o dashboard. Fique à vontade caso queira fazer o download dela - basta "passar o mouse" sobre a base e aparecerá a opção de <i>download</i>!
</div> </br>
''', unsafe_allow_html = True)

## 8.2 Define o "Index" Começando em 01
df_claim.index = df_claim.index + 1

## 8.3 Alterando a Coluna "Index" Para o Nome "ID"
df_claim.index.name = 'id'

## 8.4 Plotando a Base de Dados (DataFrame)
st.dataframe(df_claim, use_container_width = True)

# 9. Mensagem Final (Dev)
st.markdown('''
<div style='font-size: 17px;'>
    <br>
    <b>Desenvolvido por:</b> Danielle B. Maximino<br>
    <b>Objetivo:</b> Estudo das Bibliotecas Streamlit e Plotly
</div> </br>
''', unsafe_allow_html = True)