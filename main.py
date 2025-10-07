import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import re

st.set_page_config(layout="wide")

def formatear_nota_pie(texto, nota):
    texto = str(texto)
    if pd.notna(nota):
        texto += f' <span style="font-size:10px;color:#aaa;">({int(nota)})</span>'
    return re.sub(r'\((\d)\)', r'<span style="font-size:10px;color:#aaa;">(\1)</span>', texto)

def obtener_enlaces(conocimiento):
    conocimiento_limpio = re.sub(r'<.*?>', '', conocimiento)
    cursos = cursos_df[cursos_df['Conocimiento'] == conocimiento_limpio]
    enlaces = []
    for _, row in cursos.iterrows():
        nota_val = row.get("Nota")
        if pd.notna(nota_val):
            try:
                nota_int = int(float(nota_val))
                nota = f' <span style="font-size:10px;color:#aaa;">({nota_int})</span>'
            except ValueError:
                nota = f' <span style="font-size:10px;color:#aaa;">({nota_val})</span>'
        else:
            nota = ""
        enlace = f'<a href="{row["URL"]}" target="_blank">{row["CursoSugeridoUdemy"]}</a>{nota}'
        enlaces.append(enlace)
    return "<br>".join(enlaces) if enlaces else "Sin cursos"

niveles_df = pd.read_csv('niveles.csv')
niveles = niveles_df['nombreNivel'].tolist()

st.sidebar.markdown("## Learning path <br>Cloud Advisory <br><br>", unsafe_allow_html=True)
nivel_seleccionado = st.sidebar.radio("Selecciona nivel:", niveles)

id_nivel = niveles_df[niveles_df['nombreNivel'] == nivel_seleccionado]['idNivel'].values[0]

contenido_df = pd.read_csv('learning_path_dev2architect.csv')
areas_df = pd.read_csv('areasConocimiento.csv')
cursos_df = pd.read_csv('cursos.csv')

areas_df = areas_df.rename(columns={'NombreArea': 'Area'})

contenido_filtrado = (contenido_df[contenido_df['idNivel'] == id_nivel].merge(
    areas_df[['idArea', 'Area']],
    on='idArea',
    how='left'
).drop('idArea', axis=1))

# Aplica el formateo a la columna de Conocimiento, concatenando la nota al pie
contenido_filtrado['Conocimiento'] = contenido_filtrado.apply(
    lambda row: formatear_nota_pie(row['Conocimiento'], row.get('notasCurso')), axis=1
)
contenido_filtrado['Cursos'] = contenido_filtrado['Conocimiento'].apply(obtener_enlaces)

if 'notasCurso' in contenido_filtrado.columns:
    contenido_filtrado = contenido_filtrado.drop(columns=['notasCurso'])

st.title("Contenido del nivel seleccionado")

st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        display: none !important;
    }
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

if 'Area' in contenido_filtrado.columns:
    styled = styled.set_properties(subset=['Area'], **{'width': '180px', 'font-weight': '600'})

tabla_html = styled.to_html(escape=False)

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
    a {{
        color: #58a6ff;
        text-decoration: underline;
    }}
</style>
<div class="custom-table">
    {tabla_html}
</div>
"""

html(html_string, height=770, scrolling=True)

# Nota al pie compacta
notas_css = """
<style>
.nota-pie {
    font-size: 12px;
    color: #aaa;
    margin-bottom: 0;
    padding: 0;
    background: none;
    border: none;
    text-align: left;
}
.nota-pie span {
    margin-right: 18px;
    white-space: nowrap;
}
</style>
"""

notas_html = """
<div class="nota-pie">
    <span>Nota:</span>
    <span>(1) Curso que cubre varios conocimientos</span>
    <span>(2) Solo uno de ellos es necesario</span>
</div>
"""

html(notas_css + notas_html, height=33, scrolling=False)
