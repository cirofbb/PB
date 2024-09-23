import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

# Função para carregar o CSV
@st.cache_data
def load_data():
    data = pd.read_csv('C:/Users/User/Documents/CDD\PB/2249.xlsx - T  2249.csv')
    return data

# Função para gerar a nuvem de palavras com cache
@st.cache_data
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                          max_words=200, colormap='viridis',
                          stopwords=None, regexp=r'\b\w{4,}\b').generate(text)
    
    return wordcloud

# Função para carregar conteúdo do arquivo .txt
@st.cache_data
def load_txt_file():
    with open('C:\\Users\\User\\Documents\\CDD\\PB\\conteudo_reciclagem.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Configurando o estado de sessão para armazenar variáveis ao longo da interação
if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'wordcloud' not in st.session_state:
    st.session_state['wordcloud'] = None

# Função para fazer o upload de novos dados CSV
def upload_file():
    uploaded_file = st.file_uploader("Escolha um arquivo CSV para upload", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    return None

# Função para permitir o download dos dados modificados
def download_file(data):
    buffer = io.BytesIO()
    data.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

menu = st.sidebar.selectbox('Selecione um item:',
                            (
                                    'Página inicial',
                                    'Links úteis',
                                    'Tabela de dados',
                                    'Wikipedia',
                                    'Serviço de download/upload'
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

elif menu == 'Tabela de dados':
        st.subheader("Total do lixo recolhido através de coleta seletiva e total recuperado por tipo de material no Município do Rio de Janeiro entre 2002-2022")
        st.write("Fonte: https://www.data.rio/documents/4b74be782816403f9fda15df584d01f2/about")
        if st.session_state['data'] is None:
                st.session_state['data'] = load_data()
        st.dataframe(st.session_state['data'])
    
elif menu == 'Wikipedia':
    with open('C:\\Users\\User\\Documents\\CDD\\PB\\conteudo_reciclagem.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    # Exibir o conteúdo no Streamlit
    st.subheader("Conteúdo extraído da página sobre Reciclagem")
    if st.session_state['wordcloud'] is None:
        content = load_txt_file()
        st.session_state['wordcloud'] = generate_wordcloud(content)
        st.write(content[:500] + "...")
    st.write(content[:482] + "...")

    # Gerar e exibir a nuvem de palavras
    wordcloud = generate_wordcloud(content)
    st.subheader("Nuvem de Palavras")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(st.session_state['wordcloud'], interpolation='bilinear')
    ax.axis('off')

    # Mostrar a nuvem de palavras no Streamlit
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

    # Exibir os dados atualizados
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