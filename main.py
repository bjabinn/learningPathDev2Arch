import streamlit as st
import pandas as pd
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

niveles_df = pd.read_csv('niveles.csv')
niveles = niveles_df['nombreNivel'].tolist()

st.sidebar.markdown("## Learning path <br>Cloud Advisory <br><br>", unsafe_allow_html=True)
nivel_seleccionado = st.sidebar.radio("Selecciona nivel:", niveles)

id_nivel = niveles_df[niveles_df['nombreNivel'] == nivel_seleccionado]['idNivel'].values[0]

contenido_df = pd.read_csv('learning_path_dev2architect.csv')
areas_df = pd.read_csv('areasConocimiento.csv')

contenido_filtrado = (contenido_df[contenido_df['idNivel'] == id_nivel].merge(
    areas_df[['idArea', 'NombreArea']],
    on='idArea',
    how='left'
).drop('idArea', axis=1))
                      # .sort_values(by='NombreArea', ignore_index=True))


st.title("Contenido del nivel seleccionado")

styled = (
    contenido_filtrado.iloc[:, 1:]
    .style
    .hide(axis="index")
    .set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#30363d'),
            ('color', '#ffffff'),
            ('font-family', 'Segoe UI'),
            ('font-size', '14px'),
            ('padding', '8px 12px')
        ]},
        {'selector': 'td', 'props': [
            ('color', '#ffffff'),
            ('font-family', 'Segoe UI'),
            ('font-size', '13px'),
            ('padding', '6px 12px'),
            ('border', 'none')
        ]},
        {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#1f242c')]},
        {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', '#262e38')]},
        {'selector': 'table', 'props': [
            ('border-collapse', 'collapse'),
            ('width', '100%')
        ]}
    ])
)

if 'NombreArea' in contenido_filtrado.columns:
    styled = styled.set_properties(subset=['NombreArea'], **{'width': '180px', 'font-weight': '600'})

html_string = f"""
<style>
    section[data-testid="stSidebar"] {{
            min-width: 415px;
            max-width: 415px;
            width: 415px;
    }}
    .custom-table {{
        width: 100%;
        overflow-x: auto;
    }}
    .custom-table table {{
        border-radius: 8px;
        overflow: hidden;
    }}
    .custom-table th, .custom-table td {{
        white-space: nowrap;
    }}
</style>
<div class="custom-table">
    {styled.to_html()}
</div>
"""

html(html_string, height=600, scrolling=True)
