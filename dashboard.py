import streamlit as st
import plotly.express as px
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')
import openpyxl
import datetime
from datetime import date, timedelta


st.set_page_config(page_title='El Pollo Loco Dashboard', page_icon=":rooster:", layout='wide')

st.title(":chicken: Dashboard")
st.sidebar.image("polloloco.png", use_column_width=True)

# load CSS Style
with open('styles.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


with st.sidebar:
    fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))

    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_excel(filename)
    else:
        #st.warning('Devi caricare un file', icon="⚠️")
        os.chdir(r"E:\Corso_Python\ElpolloLoco")
        df = pd.read_excel("test.xlsx")

df["Anno"] = df["Data"].dt.year
df["Mese"] = df["Data"].dt.month
# convert datetime column to just date
df['Data_okok'] = pd.to_datetime(df['Data']).dt.date
df["Anno_Mese"] = pd.to_datetime(df['Anno'].astype(str) + df['Mese'].astype(str), format='%Y%m')

df["Tot_entrate"] = df[(df["Flusso"]=="Entrata")]["Importo"]
df["Tot_uscite"] = df[(df["Flusso"]=="Uscita")]["Importo"]

df["Tot_dipendenti"] = df[(df["Categoria_uscite"]=="Dipendenti")]["Importo"]
df["Tot_alimentari"] = df[(df["Categoria_uscite"]=="Alimentari")]["Importo"]
df["Tot_banca"] = df[(df["Categoria_uscite"]=="Banca")]["Importo"]

with st.sidebar:
    Filtro_anno = st.multiselect(label= "Seleziona anno",
                                options=df["Anno"].unique(),
                                default=df["Anno"].unique())

    Filtro_mese = st.multiselect(label='Seleziona il mese',
                            options=df['Mese'].unique(),
                            default=df['Mese'].unique())
    
    Filtro_flusso = st.multiselect(label='Seleziona Entrata/Uscita',
                            options=df['Flusso'].unique(),
                            default=df['Flusso'].unique())


st.sidebar.markdown('''
---
Created with ❤️ by Legno.
''')

df1 = df.query("Anno == @Filtro_anno & Mese == @Filtro_mese & Flusso == @Filtro_flusso")


# PARTE DI INSERIMENTO ENTRATE-USCITE

with st.expander("__Clicca per registrare entrate ed uscite__"):

    Tab_entrate, Tab_uscite = st.tabs([':chart_with_upwards_trend: Entrate',':chart_with_downwards_trend: Uscite'])

with Tab_uscite:
    with st.form("Registrazione uscite", clear_on_submit= True):
       st.write("REGISTRAZIONE DELLE USCITE")
       Data = st.date_input("Data della spesa", value=None)
       Flusso = st.text_input("Tipo di spesa", value="Uscita", disabled=True)
       #Flusso = st.selectbox("Seleziona il flusso", ("Uscita",), index=None, placeholder="Seleziona una voce", disabled=True)
       Categoria_uscite = st.selectbox("Seleziona il tipo di spesa", ("Alimentari",
"Bevande",
"Non alimentari",
"Dipendenti",
"Manutenzione",
"Bollette",
"Banca",
"Varie"), index=None, placeholder="Seleziona una voce"
)
       Dipendente = st.selectbox("Seleziona il dipendente", ("Denise",
"Claudia",
"Cecilia",
"Shary",
"Giulia",
"Cameriera",
"Nando",
"Patrizia",
"Ariel",
"Aiuto",
"Elmar",
"Sandra",
"Felipe"), index=None, placeholder="Seleziona una voce"
)
       Importo = st.number_input("Importo della spesa (€€,€€)", value=None, placeholder="Inserisci l'importo speso")
       Note = st.text_input("Eventuali Note")
   #Pasto = st.text_input("Pasto")

       submitted = st.form_submit_button("Registra la spesa")
       if submitted:
           if Data is None:
               st.error("Attenzione il campo DATA è obbligatorio")
           elif Flusso is None:
               st.error("Attenzione il campo FLUSSO è obbligatorio")
           elif Categoria_uscite is None:
               st.error("Attenzione il campo TIPO DI SPESA è obbligatorio")
           elif Categoria_uscite == "Dipendenti" and (Dipendente is None or Dipendente ==''):
               st.error("Attenzione il campo DIPENDENTE è obbligatorio")
           elif Categoria_uscite == "Alimentari" and Dipendente is not None:
               st.error("Attenzione il campo DIPENDENTE non va compilato se si seleziona la categoria ALIMENTARE")
           elif Categoria_uscite == "Bevande" and Dipendente is not None:
               st.error("Attenzione il campo DIPENDENTE non va compilato se si seleziona la categoria BEVANDE")
           elif Categoria_uscite == "Non alimentari" and Dipendente is not None:
               st.error("Attenzione il campo DIPENDENTE non va compilato se si seleziona la categoria NON ALIMENTARI")
           elif Categoria_uscite == "Manutenzione" and Dipendente is not None:
               st.error("Attenzione il campo DIPENDENTE non va compilato se si seleziona la categoria MANUTENZIONE")
           elif Categoria_uscite == "Bollette" and Dipendente is not None:
               st.error("Attenzione il campo DIPENDENTE non va compilato se si seleziona la categoria BOLLETTE")
           elif Categoria_uscite == "Banca" and Dipendente is not None:
               st.error("Attenzione il campo DIPENDENTE non va compilato se si seleziona la categoria BANCA")
           elif Categoria_uscite == "Varie" and Dipendente is not None:
               st.error("Attenzione il campo DIPENDENTE non va compilato se si seleziona la categoria VARIE")
           elif Importo is None:
               st.error("Attenzione il campo IMPORTO è obbligatorio")
           else:
                Data_ok = pd.to_datetime(Data)
                st.write(Data, Flusso, Categoria_uscite, Dipendente, Importo, Note)
                new_data = pd.DataFrame({'Data': [Data_ok], 'Flusso': [Flusso], 'Categoria_uscite': [Categoria_uscite], 'Dipendente': [Dipendente], 'Importo': [Importo], 'Note': [Note]} )
                st.write(new_data)
                df = pd.concat([df, new_data])
                st.write(df)
                writer = pd.ExcelWriter('test.xlsx')
                df.to_excel(writer, sheet_name="foglio1", index= False)
                writer.close()

with Tab_entrate:
    with st.form("Registrazione entrate", clear_on_submit= True):
       st.write("REGISTRAZIONE DELLE ENTRATE")
       Data = st.date_input("Data dell'incasso", value=None)
       Flusso = st.text_input("Tipo di entrata", value="Entrata", disabled=True)
       #Flusso = st.selectbox("Seleziona il flusso", ("Uscita",), index=None, placeholder="Seleziona una voce", disabled=True)
       Pasto = st.selectbox("Seleziona il tipo di entrata", ("Pranzo","Cena"), index=None, placeholder="Seleziona una voce")
       Importo = st.number_input("Importo dell'incasso (€€,€€)", value=None, placeholder="Inserisci l'importo incassato")
       Note = st.text_input("Eventuali Note")
   #Pasto = st.text_input("Pasto")

       submitted = st.form_submit_button("Registra incasso")
       if submitted:
           if Data is None:
               st.error("Attenzione il campo DATA è obbligatorio")
           elif Flusso is None:
               st.error("Attenzione il campo FLUSSO è obbligatorio")
           elif Pasto is None:
               st.error("Attenzione il campo TIPO DI ENTRATA è obbligatorio")
           elif Importo is None:
               st.error("Attenzione il campo IMPORTO è obbligatorio")
           else:
                Data_ok = pd.to_datetime(Data)
                st.write(Data, Flusso, Importo, Note)
                new_data = pd.DataFrame({'Data': [Data_ok], 'Flusso': [Flusso], 'Pasto': [Pasto], 'Importo': [Importo], 'Note': [Note]} )
                st.write(new_data)
                df = pd.concat([df, new_data])
                st.write(df)
                writer = pd.ExcelWriter('test.xlsx')
                df.to_excel(writer, sheet_name="foglio1", index= False)
                writer.close()



#st.write(df1)

#esempio di bar chart
#st.bar_chart(df1['Data'])
#st.line_chart(df1['Mese'])

#https://www.youtube.com/watch?v=pWxDxhWXJos
#https://www.youtube.com/watch?v=OkodDZxsN1I

Totale_entrate = df1[(df1["Flusso"]=="Entrata")]["Importo"].sum()
Totale_uscite = df1[(df1["Flusso"]=="Uscita")]["Importo"].sum()
Max_entrata = df1[(df1["Flusso"]=="Entrata")]["Importo"].max()
Max_uscita= df1[(df1["Flusso"]=="Uscita")]["Importo"].max()
Ricavo = Totale_entrate - Totale_uscite

Media_pranzo = round(df1[(df1["Pasto"]=="Pranzo")]["Importo"].mean(),2)
Media_cena = round(df1[(df1["Pasto"]=="Cena")]["Importo"].mean(),2)

total1,total2,total3,total4,Media_p,Media_c = st.columns(6,gap='large')

with total1:
    st.metric(label = '📈 Totale Entrate', value= f"€ {round(Totale_entrate, 2)}", delta=f"€ {round(Ricavo, 2)}")

with total2:
    st.metric(label='📉 Totale Uscite', value= f"€ {round(Totale_uscite, 2)}")

with total3:
    st.metric(label= '⬆ Maggior entrata',value= f"€ {round(Max_entrata, 2)}")

with total4:
    st.metric(label='⬇ Spesa maggiore',value= f"€ {round(Max_uscita, 2)}")


#Media_p,Media_c = st.columns(2,gap='large')

with Media_p:
    st.metric(label='🌮 Importo medio PRANZO', value= f"€ {(Media_pranzo)}")

with Media_c:
    st.metric(label='🍔 Importo medio CENA', value= f"€ {(Media_cena)}")

#st.markdown("---")

total4,total5 = st.columns(2,gap='large')

with total4:
    category_df = df1.groupby(by = ["Flusso"], as_index = False)["Importo"].sum()
    #st.subheader("Valore complessivo Entrate/Uscite")
    fig = px.bar(category_df, x = "Flusso", y = "Importo", text = ['€{:,.2f}'.format(x) for x in category_df["Importo"]],
                 template = "none",
                 title='Valore complessivo Entrate/Uscite'
    )
    fig.update_layout(#margin=dict(t=100, b=30, l=0, r=0), 
                        plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                        title_font=dict(size=30, color='#555', family="Lato, sans-serif"))
    st.plotly_chart(fig,use_container_width=True)

#fig = px.pie(df1, values="Importo", names="Flusso", hole=0.7, title=" ",
#             color_discrete_sequence=['Green', 'Red'])
#fig.update_traces(hovertemplate=None, textposition='outside', textinfo='percent+label', rotation=50)
#fig.update_layout(margin=dict(t=100, b=30, l=0, r=0), showlegend=False,
#                        plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
#                        title_font=dict(size=39, color='#555', family="Lato, sans-serif"),
#                        font=dict(size=17, color='#8a8d93'),
#                        hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))

with total5:
    #st.subheader("Suddivisione % Entrate/Uscite")
    pie_chart_entrate_uscite = px.pie(df1,
                title='Suddivisione % Entrate/Uscite',
                values='Importo',
                names='Flusso',
                hole=0.5)
    pie_chart_entrate_uscite.update_traces(hovertemplate=None, textposition='auto', textinfo='percent+label', rotation=500)
    pie_chart_entrate_uscite.update_layout(margin=dict(t=100, b=30, l=0, r=0), 
                        plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                        title_font=dict(size=30, color='#555', family="Lato, sans-serif"),
                        font=dict(size=16, color='#8a8d93'),
                        hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))
    st.plotly_chart(pie_chart_entrate_uscite, use_container_width= True)


#st.write(df1)

figg = px.bar(
    data_frame = df1,
    x = "Anno_Mese",
    y = ["Tot_entrate","Tot_uscite"],
    opacity = 0.9,
    orientation = "v",
    barmode = 'group',
    title='Entrate Vs Uscite',
    #color_discrete_map={ # replaces default color mapping by value
    #            "Tot_entrate": "Green", "Tot_uscite": "Red"
    #        },
    labels={ # replaces default labels by column name
                "variable": "Entrate - Uscite"
            },
    )
figg.update_layout(margin=dict(t=100, b=30, l=0, r=0), 
                        plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                        title_font=dict(size=30, color='#555', family="Lato, sans-serif"),
                        font=dict(size=16, color='#8a8d93'),
                        hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))
st.plotly_chart(figg, use_container_width=True)

#st.markdown("---")

a,b =st.columns(2, gap='large')

with a:
    category_df = df1.groupby(by = ["Categoria_uscite"], as_index = False)["Importo"].sum()
    #st.subheader("Valore complessivo Entrate/Uscite")
    figa = px.bar(category_df, x = "Categoria_uscite", y = "Importo", text = ['€{:,.2f}'.format(x) for x in category_df["Importo"]],
                 template = "none",
                 title='Valore complessivo Entrate/Uscite'
    )
    figa.update_layout(#margin=dict(t=100, b=30, l=0, r=0), 
                        plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                        title_font=dict(size=30, color='#555', family="Lato, sans-serif"))
    st.plotly_chart(figa,use_container_width=True)

with b:
    pie_chart = px.pie(df1,
                title='Voci di spesa',
                values='Tot_uscite',
                names='Categoria_uscite',
                hole=0.5)
    pie_chart.update_traces(hovertemplate=None, textposition='auto', textinfo='percent+label', rotation=500)
    pie_chart.update_layout(margin=dict(t=100, b=30, l=0, r=0), 
                        plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                        title_font=dict(size=30, color='#555', family="Lato, sans-serif"),
                        font=dict(size=16, color='#8a8d93'),
                        hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))
    st.plotly_chart(pie_chart, use_container_width= True)

# Creating column to distinguish month/year date
df1["MONTH"] = pd.DatetimeIndex(df1["Data"]).month.map("{:02}".format).astype(str)
df1["YEAR"] = pd.DatetimeIndex(df1["Data"]).year.astype(str)
df1["MONTH_YEAR"] = df1["YEAR"] + '-' + df1["MONTH"]

#st.write(df1)


#figg = px.bar(
#    data_frame = df1,
#    x = "Anno_Mese",
#    y = ["Tot_entrate","Tot_uscite"],
#    opacity = 0.9,
#    orientation = "v",
#    barmode = 'group',
#    title='Entrate Vs Uscite',
#    color_discrete_map={ # replaces default color mapping by value
#                "Tot_entrate": "Green", "Tot_uscite": "Red"
#            },
#    labels={ # replaces default labels by column name
#                "variable": "Entrate - Uscite"
#            },
#)
#st.plotly_chart(figg)

#with total6:
#    category_df = df1.groupby(by = ["Categoria_uscite"], as_index = False)["Importo"].sum()
#    st.subheader("Suddivisione Uscite")
#    fig = px.bar(category_df, x = "Categoria_uscite", y = "Importo", text = ['€{:,.2f}'.format(x) for x in category_df["Importo"]],
#                 template = "none")
#    st.plotly_chart(fig)
