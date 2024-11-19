import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from fastapi import FastAPI
from pydantic import BaseModel

# Carregando o CSV
@st.cache_data
def load_data():
    data = pd.read_csv('lixo.csv')
    data90 = pd.read_csv('C:/Users/User/Documents/CDD/PB/1481.xlsx - Dom-1990-1999.csv')
    data00 = pd.read_csv('C:/Users/User/Documents/CDD/PB/1481.xlsx - Dom-2000-2009.csv')
    data10 = pd.read_csv('C:/Users/User/Documents/CDD/PB/1481.xlsx - Dom-2010-2019.csv')
    data20 = pd.read_csv('C:/Users/User/Documents/CDD/PB/1481.xlsx - Dom-2020-2023.csv')
    return data, data90, data00, data10, data20

# Gerando a nuvem de palavras com cache
@st.cache_data
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                          max_words=200, colormap='viridis',
                          stopwords=None, regexp=r'\b\w{4,}\b').generate(text)
    
    return wordcloud

# Carregando o conteúdo do arquivo .txt
@st.cache_data
def load_txt_file():
    with open('C:\\Users\\User\\Documents\\CDD\\PB\\conteudo_reciclagem.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Configurando o estado de sessão para armazenar variáveis ao longo da interação
if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'data90' not in st.session_state:
    st.session_state['data90'] = None
if 'data00' not in st.session_state:
    st.session_state['data00'] = None
if 'data10' not in st.session_state:
    st.session_state['data10'] = None
if 'data20' not in st.session_state:
    st.session_state['data20'] = None
if 'wordcloud' not in st.session_state:
    st.session_state['wordcloud'] = None

# Raspando o conteúdo de uma notícia a partir da URL
def scrape_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Identificando os parágrafos principais da notícia
    paragraphs = soup.find_all('p')
    
    # Extraindo o texto dos parágrafos
    news_text = ' '.join([p.get_text() for p in paragraphs if len(p.get_text()) > 20])
    
    return news_text

# Upload de novos dados CSV
def upload_file():
    uploaded_file = st.file_uploader("Escolha um arquivo CSV para upload", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    return None

# Download dos dados modificados
def download_file(data):
    buffer = io.BytesIO()
    data.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

menu = st.sidebar.selectbox('Selecione um item:',
                            (
                                    'Página inicial',
                                    'Links úteis',
                                    'Notícias recentes',
                                    'Tabela de dados',
                                    'Wikipedia',
                                    'Serviço de download/upload',
                                    'Recursos de IA via LLM'
                            ))

if menu == 'Página inicial':
        st.title("Projeto Reciclagem")
        st.write("""
        A gestão inadequada de resíduos sólidos urbanos representa um dos grandes desafios ambientais e sociais das cidades modernas. Muitos resíduos recicláveis ainda acabam em aterros sanitários, contribuindo para a degradação ambiental, aumento das emissões de gases de efeito estufa e desperdício de recursos valiosos. Além disso, a falta de incentivo para a população adotar práticas de reciclagem e a dificuldade em conectar pessoas e empresas que podem reutilizar materiais recicláveis intensificam o problema.

        A proposta para diminuir este problema é o desenvolvimento de uma aplicação cujos dois principais objetivos são:

        - Facilitar a troca de materiais recicláveis: Criar uma plataforma que conecta indivíduos e empresas que têm materiais recicláveis com aqueles que podem reutilizá-los, promovendo uma economia circular.
        - Incentivar a reciclagem: Através de um sistema de pontuação que recompensa os usuários por reciclar corretamente, promovendo a participação ativa da comunidade.

        """)

        st.markdown("---")

elif menu == 'Links úteis':
        st.subheader("Links úteis:\n")

        st.markdown("""
                - [Reciclaê](https://institutolegado.org/blog/reciclae-o-aplicativo-que-conecta-catadores-a-materiais-reciclaveis/?gad_source=1&gclid=Cj0KCQjwrKu2BhDkARIsAD7GBoslHXWS7usjo0ZVHRyI4sS05_EZePli0gYdD2bhWSjTsY9qwVVMqFoaArkcEALw_wcB)
                - [Cataki](https://www.cataki.org/)
                - [Pimp my carroça](https://pimpmycarroca.com/)
        """)


        st.markdown("---")

elif menu == 'Notícias recentes':
     st.subheader('Notícias recentes')
     st.write('Notícias publicadas recentemente que dão a dimensão do problema do recolhimento e tratamento de resíduos no RJ')

     st.markdown("---")
     
     url1 = 'https://vejario.abril.com.br/cidade/menos-de-1-do-lixo-produzido-no-rio-de-janeiro-passa-por-coleta-seletiva'
     url2 = 'https://www.ecodebate.com.br/2023/04/14/o-rio-de-janeiro-tem-um-dos-piores-indices-de-recuperacao-de-residuos/'
     url3 = 'https://orlario.com.vc/esg/sustentabilidade/producao-diaria-de-lixo-no-rio-de-janeiro-chega-a-17-mil-toneladas/'

     news1 = scrape_news(url1)
     news2 = scrape_news(url2)
     news3 = scrape_news(url3)
     
     st.subheader("1. Menos de 1% do lixo produzido no Rio passa por coleta seletiva")
     st.write(news1)
     st.markdown(f"[Leia mais]({url1})")

     st.markdown("---")
     
     st.subheader("2. O Rio de Janeiro tem um dos piores índices de recuperação de resíduos")
     st.write(news2)
     st.markdown(f"[Leia mais]({url2})")
     
     st.markdown("---")
     
     st.subheader("3. Produção diária de lixo no Rio de Janeiro chega a 17 mil toneladas")
     st.write(news3)
     st.markdown(f"[Leia mais]({url3})")


elif menu == 'Tabela de dados':
        st.subheader("Total do lixo recolhido através de coleta seletiva e total recuperado por tipo de material no Município do Rio de Janeiro entre 2002-2022")
        st.write("Fonte: https://www.data.rio/documents/4b74be782816403f9fda15df584d01f2/about")
        if st.session_state['data'] is None:
                (st.session_state['data'], st.session_state['data90'], 
                 st.session_state['data00'], st.session_state['data10'], 
                 st.session_state['data20']) = load_data()
        st.dataframe(st.session_state['data'])

        st.markdown("---")

        st.subheader('Total do lixo domiciliar (em toneladas) coletado por ano, segundo  Áreas de Planejamento (AP), Regiões de Planejamento (RP) e  Regiões Administrativas (RA) -  Município do Rio de Janeiro -  1990 -2023')
        st.write("Fonte: https://www.data.rio/documents/PCRJ::-total-do-lixo-domiciliar-e-p%C3%BAblico-coletados-por-ano-segundo-%C3%A1reas-de-planejamento-ap-regi%C3%B5es-de-planejamento-rp-e-regi%C3%B5es-administrativas-ra-no-munic%C3%ADpio-do-rio-de-janeiro-entre-1990-2023/about")
        st.write('Período: 1990-1999')
        st.dataframe(st.session_state['data90'])

        st.markdown("---")

        st.write('Período: 2000-2009')
        st.dataframe(st.session_state['data00'])

        st.markdown("---")

        st.write('Período: 2010-2019')
        st.dataframe(st.session_state['data10'])

        st.markdown("---")

        st.write('Período: 2020-2023')
        st.dataframe(st.session_state['data20'])

    
elif menu == 'Wikipedia':
    with open('C:\\Users\\User\\Documents\\CDD\\PB\\conteudo_reciclagem.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # Exibindo o conteúdo no Streamlit
    st.subheader("Conteúdo extraído da página sobre Reciclagem")
    if st.session_state['wordcloud'] is None:
        content = load_txt_file()
        st.session_state['wordcloud'] = generate_wordcloud(content)
        st.write(content[:500] + "...")
    st.write(content[:482] + "...")

    # Gerando e exibir a nuvem de palavras
    wordcloud = generate_wordcloud(content)
    st.subheader("Nuvem de Palavras")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(st.session_state['wordcloud'], interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

elif menu == 'Serviço de download/upload':
      st.title('Serviço de download/upload')
      st.subheader('Tabela de dados')
      if st.session_state['data'] is None:
           st.session_state['data'] = load_data()
      st.dataframe(st.session_state['data'])

      data = load_data()

    # Serviço de upload de arquivos CSV
      st.subheader("Upload de Novos Dados")
      uploaded_data = upload_file()

    # Se o usuário fez upload de novos dados, concatenar com os dados existentes
      if uploaded_data is not None:
        st.write("Novos dados adicionados:")
        st.dataframe(uploaded_data)

        # Concatenar os dados existentes com os dados enviados pelo usuário
        data = pd.concat([data, uploaded_data], ignore_index=True)

    # Exibindo os dados atualizados
      st.subheader("Dados Atualizados")
      st.dataframe(data)

    # Serviço de download dos dados atualizados
      st.subheader("Download dos Dados Atualizados")
      st.download_button(
           label="Baixar CSV",
           data=download_file(data),
           file_name="dados_atualizados.csv",
           mime="text/csv"
           )
      
elif menu == 'Recursos de IA via LLM':
    st.title('Recursos de IA via LLM')

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    if prompt := st.chat_input("Tire aqui sua dúvida sobre reciclagem:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Estou pensando"):
                req = requests.post("http://localhost:8000/chat/", 
                                    json={"message": prompt} )
                response = req.json()
                st.markdown(response["response"])
        st.session_state.messages.append({"role": "assistant",
                                        "content": response["response"]})