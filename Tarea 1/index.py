# Importar librerías
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import pycountry

# Función para obtener el nombre completo del país a partir de su abreviatura
def get_country_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except AttributeError:
        return None



# Leer los datos
df = pd.read_csv('Tarea 1/Salaries.csv')

# Definir colores y fuente
font_family = 'Arial'
text_color = 'rgb(69,69,69)'
background_color = 'rgb(240,240,240)'
title_size = 50
padding = '15%'

# Función para crear un gráfico según la pregunta
def create_chart(question,df=df):

    # Salario en USD promedio por año laboral
    if question == 1:
        df = df.groupby('work_year')['salary_in_usd'].mean().reset_index()
        df['work_year'] = df['work_year'].astype(str)
        title = 'Salario promedio en USD por año laboral'
        x_label = 'Año laboral'
        y_label = 'Salario en USD'
        color = 'rgb(69,69,69)'
        fig = px.line(df, x='work_year', y='salary_in_usd')
        
        # Modificar el color
        fig.update_traces(line_color=color, mode='lines+markers', marker_color=color, marker_size=10)
        # Modificar el color del área de trazado para blanco
        fig.update_layout(plot_bgcolor=background_color)
        # Cambiar leyenda x 
        fig.update_layout(xaxis_title=x_label)
        # Cambiar leyenda y
        fig.update_layout(yaxis_title=y_label)

        description = "A lo largo de los años, hemos observado una tendencia clara de crecimiento en el salario promedio en USD en el campo de Ciencia de Datos. Al analizar los datos recopilados, encontramos que el salario promedio ha experimentado un aumento constante en cada año laboral registrado. Al examinar la distribución de los salarios en diferentes años laborales, notamos que el promedio salarial ha ido en aumento gradual, lo que sugiere una demanda creciente de profesionales en el campo de Ciencia de Datos y un reconocimiento de su valor en diversas industrias."
    # Disparidades salariales entre niveles de experiencia
    elif question == 2:
        df = df.groupby('experience_level')['salary_in_usd'].mean().reset_index()
        df['experience_level'] = df['experience_level'].astype(str)
        title = 'Promedio de salario en USD por nivel de experiencia'
        x_label = 'Nivel de experiencia'
        y_label = 'Salario en USD'
        color = 'rgb(69,69,69)'
        fig = px.bar(df, x='experience_level', y='salary_in_usd')
        experience_levels = ['Nivel inicial', 'Nivel medio', 'Nivel superior', 'Nivel ejecutivo' ]

        # asignar valor en la barra en $USD
        fig.update_traces(text=round(df['salary_in_usd']), textposition='outside')

        # Modificar el color
        fig.update_traces(marker_color=color)
        # Modificar el color del área de trazado para blanco
        fig.update_layout(plot_bgcolor=background_color)
        # Cambiar leyenda x
        fig.update_layout(xaxis_title=x_label)
        # Cambiar leyenda y
        fig.update_layout(yaxis_title=y_label)
        # Cambiar valores en x
        fig.update_xaxes(ticktext=experience_levels, tickvals=[0, 1, 2, 3])

        description= "Al investigar la relación entre los niveles de experiencia y los salarios en el campo de Ciencia de Datos, encontramos que existe una clara diferencia en los salarios promedio para cada nivel de experiencia. Al analizar el grafico podemos notar que los más altos son los salarios medios y ejecutivos, seguidos por los salarios de nivel superior y nivel inicial. Esta disparidad salarial refleja la importancia de la experiencia y la especialización en el campo de Ciencia de Datos, donde los profesionales con mayor experiencia y habilidades especializadas tienden a recibir salarios más altos."
    
    # Impacto del tipo de empleo en los salarios
    elif question == 3:
        # Comparar los salarios promedio por tipo de empleo
        df = df.groupby('employment_type')['salary_in_usd'].mean().reset_index()
        df['employment_type'] = df['employment_type'].astype(str)
        title = 'Promedio de salario en USD por tipo de empleo'
        x_label = 'Tipo de empleo'
        y_label = 'Salario en USD'
        color = 'rgb(69,69,69)'
        # Crear un gráfico de barras horizontal
        fig = px.bar(df, x='salary_in_usd', y='employment_type', orientation='h')
        types = ['Tiempo Parcial (PT)', 'Tiempo Completo (FT)', 'Contrato (CT)','Freelance (FL)']
        # asignar valor en la dentro de la barra
        fig.update_traces(text=round(df['salary_in_usd']), textposition='inside')
        fig.update_traces(marker_color=color)
        # Modificar el color del área de trazado para blanco
        fig.update_layout(plot_bgcolor=background_color)
        # Cambiar leyenda x
        fig.update_layout(xaxis_title=y_label)
        # Cambiar leyenda y
        fig.update_layout(yaxis_title=x_label)

        # Cambiar valores en y
        fig.update_yaxes(ticktext=types, tickvals=[0, 1, 2, 3])

        description = "Al examinar los datos recopilados y representarlos visualmente, observamos que, en promedio, los empleados a tiempo parcial tienen el salario más alto, seguido por los empleados con contrato, los empleados a tiempo completo y, por último, los empleados autónomos o freelancers, que tienen el salario promedio más bajo. Este hallazgo sugiere que ciertos tipos de empleo tienden a ofrecer salarios más altos que otros. Específicamente, los empleados a tiempo parcial parecen disfrutar de salarios más altos en promedio en comparación con aquellos empleados a tiempo completo, por contrato o autónomos."
    # Disparidades salariales regionales
    elif question == 4:
        df = df.groupby('company_location')['salary_in_usd'].mean().reset_index()
        df['company_location'] = df['company_location'].astype(str)

        df['company_location'] = df['company_location'].apply(lambda x: get_country_name(x))

        title = 'Promedio de salario en USD por región'
        x_label = 'Región'
        y_label = 'Salario en USD'
        color = 'rgb(69,69,69)'
        fig = go.Figure(data=go.Choropleth(
            locations=df['company_location'],
            z = df['salary_in_usd'],
            locationmode = 'country names',
            colorscale = 'greys',
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title = "Salario en USD",
        ))

        # Modificar el color del área de trazado para blanco
        fig.update_layout(plot_bgcolor=background_color)

        description = "Al analizar los salarios promedio en USD por región, encontramos que los salarios varían significativamente entre diferentes regiones. En general, los profesionales en Rusia, USA, Canada y Australia destacan por tener los salarios promedio más altos en comparación con otros países. Por otro lado, los salarios promedio en India, Brasil y México son relativamente más bajos en comparación con otros países. Estas disparidades salariales regionales pueden estar influenciadas por factores económicos, políticos y culturales específicos de cada región, así como por la demanda y la oferta de profesionales en el campo de Ciencia de Datos."

    else:
        return None, None, None, None, None, None
    
    return fig, x_label, y_label, title, color, description

# Crear la aplicación
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1(children='Salarios en Ciencia de Datos', style={'textAlign': 'center', 'font-family': font_family, 'color': text_color, 'font-size': title_size}),
    
    # Dropdown para seleccionar la pregunta
    dcc.Dropdown(
        id='question-dropdown',
        options=[
            {'label': '1. Tendencias salariales a lo largo del tiempo', 'value': 1},
            {'label': '2. Disparidades salariales entre niveles de experiencia', 'value': 2},
            {'label': '3. Impacto del tipo de empleo en los salarios', 'value': 3},
            {'label': '4. Disparidades salariales regionales', 'value': 4}
            # Agregar más opciones según sea necesario
        ],
        value=1,  # Pregunta predeterminada
        clearable=False,
        style={'width': '80%', 'margin': 'auto', 'font-family': font_family, 'color': text_color}
    ),
    
    # Div para mostrar el gráfico
    html.Div(id='graph-container'),
],style={'padding-left': '15%', 'padding-right': '15%'})

# Callback para actualizar el gráfico cuando cambia la pregunta seleccionada
@app.callback(
    Output('graph-container', 'children'),
    Input('question-dropdown', 'value')
)
def update_graph(question):
    fig, x_label, y_label, title, color, description = create_chart(question)
    if fig:
        return [
            html.H2(children=title, style={'textAlign': 'center', 'font-family': font_family, 'color': text_color, 'padding-top': '30px'}),
            html.P(children=description, style={'textAlign': 'justify', 'font-family': font_family, 'color': text_color, 'padding-top': '5px'}),
            dcc.Graph(figure=fig)
        ]
    else:
        return html.H2(children='Pregunta no válida', style={'textAlign': 'center', 'font-family': font_family, 'color': text_color, 'padding-top': '30px'})

# Correr la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
