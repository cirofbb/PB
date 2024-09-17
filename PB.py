import streamlit as st
import pandas as pd

st.title("Projeto Reciclagem")

st.write("""
A gestão inadequada de resíduos sólidos urbanos representa um dos grandes desafios ambientais e sociais das cidades modernas. Muitos resíduos recicláveis ainda acabam em aterros sanitários, contribuindo para a degradação ambiental, aumento das emissões de gases de efeito estufa e desperdício de recursos valiosos. Além disso, a falta de incentivo para a população adotar práticas de reciclagem e a dificuldade em conectar pessoas e empresas que podem reutilizar materiais recicláveis intensificam o problema.

A proposta para diminuir este problema é o desenvolvimento de uma aplicação cujos dois principais objetivos são:

- Facilitar a troca de materiais recicláveis: Criar uma plataforma que conecta indivíduos e empresas que têm materiais recicláveis com aqueles que podem reutilizá-los, promovendo uma economia circular.
- Incentivar a reciclagem: Através de um sistema de pontuação que recompensa os usuários por reciclar corretamente, promovendo a participação ativa da comunidade.

""")

st.markdown("---")

st.subheader("Links úteis:\n")

st.markdown("""
        - [Reciclaê](https://institutolegado.org/blog/reciclae-o-aplicativo-que-conecta-catadores-a-materiais-reciclaveis/?gad_source=1&gclid=Cj0KCQjwrKu2BhDkARIsAD7GBoslHXWS7usjo0ZVHRyI4sS05_EZePli0gYdD2bhWSjTsY9qwVVMqFoaArkcEALw_wcB)
        - [Cataki](https://www.cataki.org/)
        - [Pimp my carroça](https://pimpmycarroca.com/)
""")


st.markdown("---")

df = pd.read_csv('C:\\Users\\User\\Documents\\CDD\Streamlit\\2249.xlsx - T  2249.csv')
st.subheader("Total do lixo recolhido através de coleta seletiva e total recuperado por tipo de material no Município do Rio de Janeiro entre 2002-2022")
st.dataframe(df)
st.write("Fonte: https://www.data.rio/documents/4b74be782816403f9fda15df584d01f2/about")
