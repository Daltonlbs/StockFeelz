import streamlit as st
import pandas as pd
import plotly.express as px
#import pydeck as pdk
import matplotlib.pyplot as plt
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go
from PIL import Image

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_icon=":chart_with_upwards_trend:", layout="wide")  #layout="wide"



@st.cache
def load_data():
    feelTop = pd.read_csv("feelTopStocks.csv", sep = ',', index_col=0)
    feelUp = pd.read_csv("feelUpStocks.csv", sep = ',', index_col=0)
    feelDown = pd.read_csv("feelDownStocks.csv", sep = ',', index_col=0)
    varTot = pd.read_csv("varTot.csv")
    total = pd.read_csv("toth.csv")
    top = pd.read_csv("toph.csv")
    rVarTot = varTot.sort_values(by=['Diff'], ascending=True)
    varTot.Diff = varTot.Diff.astype(int)
    rVarTot.Diff = rVarTot.Diff.astype(int)
    feelTopT = feelTop.T.sort_values(by=['Intensidade_Media'])
    feelUpT = feelUp.T.sort_values(by=['Intensidade_Media'])
    feelDownT = feelDown.T.sort_values(by=['Intensidade_Media'])
    return feelTop, feelUp, feelDown, varTot, total, top, rVarTot, feelTopT, feelUpT, feelDownT

feelTop, feelUp, feelDown, varTot, total, top, rVarTot, feelTopT, feelUpT, feelDownT  = load_data()

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)


dt_end = datetime.today()


#intervals=['Daily','Weekly']
#interval = 'Daily'

def trad(txt):
    if txt == "sell":
        cor = "inverse"
        return "VENDA"
    else:
        cor="normal"
        return "COMPRA"

def cor(txt):
    if txt == "sell":
        return "inverse"
    else:
        return "normal"

@st.cache
def infoStock(stock):
    sInfo = ip.get_stock_information(stock, country='Brazil')
    rev = int(sInfo.iloc[0]["Revenue"] / 1000000)
    rev = str(rev)
    if len(rev) > 3:
        rev = rev[:-3] + "." + rev[-3:]
    techInfo = ip.technical_indicators(stock, country='Brazil', product_type='stock')
    return sInfo,rev,techInfo

@st.cache
def consultar_acao(acao, dt_start):
    df= ip.get_stock_historical_data(stock=acao,
                                 country='Brazil',
                                 from_date=format_date(dt_start),
                                 to_date=format_date(dt_end),
                                 interval='Daily')
    return df

def plotCandleStick(df, acao='ticket'):
  tracel = {
      'x': df.index,
      'open': df.Open,
      'close': df.Close,
      'high': df.High,
      'low': df.Low,
      'type': 'candlestick',
      'name': acao,
      'showlegend': False
  }
  data = [tracel]
  layout = go.Layout()
  fig = go.Figure(data=data, layout=layout)
  return fig


st.sidebar.title("Opções")
st.sidebar.markdown("Escolha o que você quer ver.")
#st.sidebar.info("Opções")

pagSel = st.sidebar.selectbox('Selecione uma opção', ["Home","Ações mais mencionadas","Maiores acréscimos de menções","Maiores decréscimos de menções","Mostrar lista das ações mencionadas"])


if pagSel == "Home":
    st.title("Sentimento das ações")
    stk = Image.open('stocks.jpg')
    twp = Image.open('tweepy2.png')

    left_column,right_column = st.columns(2)
    with left_column:
        st.markdown(
            """
             O **Twitter** é uma ferramenta muito usada para a troca de idéias
             entre gestores, analistas e até investidores individuais.
             Esse constante fluxo de informações torna possível a **análise
             do sentimento** geral dos investidores sobre a bolsa e sobre ações específicas.
             """
        )
        st.title("")
        st.title("")
        st.title("")
        st.title("")
        st.image(twp)#, caption='Sunrise by the mountains')
    with right_column:
        st.image(stk)


stock_select = "PETR4"
sInfo, rev, techInfo = infoStock(stock_select)






if pagSel == "Ações mais mencionadas":
    left_column,right_column = st.columns(2)
    with left_column:
        st.header("")
        st.header("Ações mais mencionadas")

        #st.write(total)
        zz=st.slider("Número de ações",5,100,15) #len(total)
        #l = top
        l=total[:zz]
        l1 = int(l.iloc[0][1])
        l2 = int(l1 / 2)
        l3 = int(l1 / 4*3)
        l4 = int(l1 / 4)

        plt.figure(figsize=(32, 20))
        plt.bar(l['word'], l['count'], color='lightsteelblue', edgecolor='navy', linewidth=2.8)
        plt.title('Ações mais mencionadas da fintwit', fontsize='48')
        plt.ylabel('Menções', fontsize='36')
        plt.yticks([l1, l2, l3, l4], fontsize='24')
        if zz <= 50:
            plt.xlabel('Tickers', fontsize='36')
            plt.xticks( fontsize='24', rotation = 45)
        else:
            plt.xticks(fontsize='0.5')

        plt.show()
        st.pyplot();

    with right_column:
        if st.checkbox("Mostrar sentimento (principais)"):
            st.header("Sentimento médio")
            st.header("")
            st.header("")
            st.header("")
            plt.figure(figsize=(16, 11))
            #feelTopT = feelTop.T.sort_values(by=['Intensidade_Media'])

            plt.barh(feelTopT.index, feelTopT["Intensidade_Media"], color='khaki', edgecolor='darkgoldenrod', linewidth=2.4)
            plt.title('Sentimento das ações', fontsize='24')
            plt.xlabel('Sentimento médio', fontsize='20')
            plt.ylabel('Tickers', fontsize='20')
            plt.xticks(fontsize='16')
            plt.yticks(fontsize='16')
            plt.show()
            st.pyplot();

    if st.checkbox("Analisar ações"):
        left_column,right_column = st.columns(2)
        with left_column:
            #acoes = total['word']
            acoes = feelTopT.index
            stock_select = st.selectbox("Seleciona a ação", acoes)
            sInfo, rev, techInfo = infoStock(stock_select)
            st.header("Gráfico de " + stock_select.upper())
            atraso = st.slider("Período de análise", 5, 365, 30)
            dt_start = datetime.today() - timedelta(days=atraso)
            df = consultar_acao(stock_select, dt_start)
            fig = plotCandleStick(df)
            st.plotly_chart(fig)
        with right_column:
            st.subheader("Indicadores Fundamentalistas")
            st.metric(label="Fechamento", value=sInfo.iloc[0]['Prev. Close'])
            st.metric(label="Preço/Lucro", value=sInfo.iloc[0]['P/E Ratio'])
            st.metric(label="Variação (12m):", value=sInfo.iloc[0]['1-Year Change'])
            st.metric(label="Dividendo (DY)", value=sInfo.iloc[0]['Dividend (Yield)'])
            st.metric(label="Volume médio (3m)", value=sInfo.iloc[0]['Average Vol. (3m)'])
            st.metric(label="Receita (milhões R$)", value=rev)

        st.subheader("Indicadores técnicos")
        col1, col2, col3,col4 = st.columns(4)
        col1.metric(label="IFR", value=techInfo.iloc[0][1], delta=trad(techInfo.iloc[0][2]), delta_color=cor((techInfo.iloc[0][2])))
        col2.metric(label="STOCH:", value=techInfo.iloc[1][1], delta=trad(techInfo.iloc[1][2]), delta_color=cor((techInfo.iloc[1][2])))
        col3.metric(label="MACD:", value=techInfo.iloc[3][1], delta=trad(techInfo.iloc[3][2]), delta_color=cor((techInfo.iloc[3][2])))
        col4.metric(label="ADX:", value=techInfo.iloc[4][1], delta=trad(techInfo.iloc[4][2]), delta_color=cor((techInfo.iloc[4][2])))


if pagSel == "Maiores acréscimos de menções":
    left_column,right_column = st.columns(2)
    with left_column:
        st.header("")
        st.header("Maiores acréscimos de menções")
        v = varTot[:15]
        v1 = int(v.iloc[0][1])
        v2 = int(v1 / 2)

        plt.figure(figsize=(18, 12))
        plt.bar(v['word'], v['Diff'], color='mediumseagreen', edgecolor='darkgreen', linewidth=2.4)
        plt.title('Maiores acréscimos de menções', fontsize='24')
        plt.xlabel('Tickers', fontsize='18')
        plt.ylabel('Aumento de menções', fontsize='20')
        plt.xticks(fontsize='14')
        plt.yticks([v1, v2], fontsize='18')
        plt.show()
        st.pyplot();

    with right_column:
        if st.checkbox("Mostrar sentimento "):
            st.header("Sentimento médio")
            plt.figure(figsize=(16, 11))
            #feelUpT = feelUp.T.sort_values(by=['Intensidade_Media'])

            plt.barh(feelUpT.index, feelUpT["Intensidade_Media"], color='khaki', edgecolor='darkgoldenrod', linewidth=2.4)
            plt.title('Sentimento das ações', fontsize='20')
            plt.xlabel('Sentimento médio', fontsize='16')
            plt.ylabel('Tickers', fontsize='19')
            plt.xticks(fontsize='16')
            plt.yticks(fontsize='16')
            plt.show()
            st.pyplot();

    if st.checkbox("Analisar ações"):
        left_column, right_column = st.columns(2)
        with left_column:

            acoes = feelUpT.index
            stock_select = st.selectbox("Seleciona a ação", acoes)
            sInfo, rev, techInfo = infoStock(stock_select)
            st.header("Gráfico de " + stock_select.upper())
            atraso = st.slider("Período de análise", 5, 365, 30)
            dt_start = datetime.today() - timedelta(days=atraso)
            df = consultar_acao(stock_select, dt_start)
            fig = plotCandleStick(df)
            st.plotly_chart(fig)
        with right_column:
            st.subheader("Indicadores Fundamentalistas")
            st.metric(label="Fechamento", value=sInfo.iloc[0]['Prev. Close'])
            st.metric(label="Preço/Lucro", value=sInfo.iloc[0]['P/E Ratio'])
            st.metric(label="Variação (12m):", value=sInfo.iloc[0]['1-Year Change'])
            st.metric(label="Dividendo (DY)", value=sInfo.iloc[0]['Dividend (Yield)'])
            st.metric(label="Volume médio (3m)", value=sInfo.iloc[0]['Average Vol. (3m)'])
            st.metric(label="Receita (milhões R$)", value=rev)

        st.subheader("Indicadores técnicos")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="IFR", value=techInfo.iloc[0][1], delta=trad(techInfo.iloc[0][2]),
                    delta_color=cor((techInfo.iloc[0][2])))
        col2.metric(label="STOCH:", value=techInfo.iloc[1][1], delta=trad(techInfo.iloc[1][2]),
                    delta_color=cor((techInfo.iloc[1][2])))
        col3.metric(label="MACD:", value=techInfo.iloc[3][1], delta=trad(techInfo.iloc[3][2]),
                    delta_color=cor((techInfo.iloc[3][2])))
        col4.metric(label="ADX:", value=techInfo.iloc[4][1], delta=trad(techInfo.iloc[4][2]),
                    delta_color=cor((techInfo.iloc[4][2])))




if pagSel == "Maiores decréscimos de menções":
    left_column,right_column = st.columns(2)
    with left_column:
        st.header("")
        st.header("Maiores decréscimos de menções")

        d = rVarTot[:15]
        d1 = int(d.iloc[0][1])
        d2 = int(d1 / 2)

        plt.figure(figsize=(18, 12))
        plt.bar(d['word'], d['Diff'], color='tomato', edgecolor='firebrick', linewidth=2.4)
        plt.title('Maiores decréscimos de menções', fontsize='24')
        plt.xlabel('Tickers', fontsize='20')
        plt.ylabel('Queda de menções', fontsize='20')
        plt.xticks(fontsize='18')
        plt.yticks([d1, d2], fontsize='18')
        plt.show()
        st.pyplot();

    with right_column:
        if st.checkbox("Mostrar sentimento "):

            st.header("Sentimento médio")

            plt.figure(figsize=(16, 10))
            #feelDownT = feelDown.T.sort_values(by=['Intensidade_Media'])
            plt.barh(feelDownT.index, feelDownT["Intensidade_Media"], color='khaki', edgecolor='darkgoldenrod', linewidth=2.4)
            plt.title('Sentimento das ações', fontsize='20')
            plt.xlabel('Sentimento médio', fontsize='16')
            plt.ylabel('Tickers', fontsize='20')
            plt.xticks(fontsize='16')
            plt.yticks(fontsize='18')
            plt.show()
            st.pyplot();

    if st.checkbox("Analisar ações"):
        left_column,right_column = st.columns(2)
        with left_column:

            acoes = feelDownT.index
            stock_select = st.selectbox("Seleciona a ação", acoes)
            sInfo, rev, techInfo = infoStock(stock_select)
            st.header("Gráfico de " + stock_select.upper())
            atraso = st.slider("Período de análise", 5, 365, 30)
            dt_start = datetime.today() - timedelta(days=atraso)
            df = consultar_acao(stock_select, dt_start)
            fig = plotCandleStick(df)
            st.plotly_chart(fig)
        with right_column:
            st.subheader("Indicadores Fundamentalistas")
            st.metric(label="Fechamento", value=sInfo.iloc[0]['Prev. Close'])
            st.metric(label="Preço/Lucro", value=sInfo.iloc[0]['P/E Ratio'])
            st.metric(label="Variação (12m):", value=sInfo.iloc[0]['1-Year Change'])
            st.metric(label="Dividendo (DY)", value=sInfo.iloc[0]['Dividend (Yield)'])
            st.metric(label="Volume médio (3m)", value=sInfo.iloc[0]['Average Vol. (3m)'])
            st.metric(label="Receita (milhões R$)", value=rev)

        st.subheader("Indicadores técnicos")
        col1, col2, col3,col4 = st.columns(4)
        col1.metric(label="IFR", value=techInfo.iloc[0][1], delta=trad(techInfo.iloc[0][2]), delta_color=cor((techInfo.iloc[0][2])))
        col2.metric(label="STOCH:", value=techInfo.iloc[1][1], delta=trad(techInfo.iloc[1][2]), delta_color=cor((techInfo.iloc[1][2])))
        col3.metric(label="MACD:", value=techInfo.iloc[3][1], delta=trad(techInfo.iloc[3][2]), delta_color=cor((techInfo.iloc[3][2])))
        col4.metric(label="ADX:", value=techInfo.iloc[4][1], delta=trad(techInfo.iloc[4][2]), delta_color=cor((techInfo.iloc[4][2])))

if pagSel == "Mostrar lista das ações mencionadas":
    st.header("Ações mais mencionadas")
    st.write(total)
    if st.checkbox("Analisar ações"):
        left_column,right_column = st.columns(2)
        with left_column:
            acoes = total['word']

            stock_select = st.selectbox("Seleciona a ação", acoes)
            sInfo, rev, techInfo = infoStock(stock_select)
            st.header("Gráfico de " + stock_select.upper())
            atraso = st.slider("Período de análise", 5, 365, 30)
            dt_start = datetime.today() - timedelta(days=atraso)
            df = consultar_acao(stock_select, dt_start)
            fig = plotCandleStick(df)
            st.plotly_chart(fig)
        with right_column:
            st.subheader("Indicadores Fundamentalistas")
            st.metric(label="Fechamento", value=sInfo.iloc[0]['Prev. Close'])
            st.metric(label="Preço/Lucro", value=sInfo.iloc[0]['P/E Ratio'])
            st.metric(label="Variação (12m):", value=sInfo.iloc[0]['1-Year Change'])
            st.metric(label="Dividendo (DY)", value=sInfo.iloc[0]['Dividend (Yield)'])
            st.metric(label="Volume médio (3m)", value=sInfo.iloc[0]['Average Vol. (3m)'])
            st.metric(label="Receita (milhões R$)", value=rev)

        st.subheader("Indicadores técnicos")
        col1, col2, col3,col4 = st.columns(4)
        col1.metric(label="IFR", value=techInfo.iloc[0][1], delta=trad(techInfo.iloc[0][2]), delta_color=cor((techInfo.iloc[0][2])))
        col2.metric(label="STOCH:", value=techInfo.iloc[1][1], delta=trad(techInfo.iloc[1][2]), delta_color=cor((techInfo.iloc[1][2])))
        col3.metric(label="MACD:", value=techInfo.iloc[3][1], delta=trad(techInfo.iloc[3][2]), delta_color=cor((techInfo.iloc[3][2])))
        col4.metric(label="ADX:", value=techInfo.iloc[4][1], delta=trad(techInfo.iloc[4][2]), delta_color=cor((techInfo.iloc[4][2])))













