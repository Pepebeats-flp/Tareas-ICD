from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
# pip install pycountry
import pycountry

# Función para obtener el nombre completo del país a partir de su abreviatura
def get_country_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name
    except AttributeError:
        return None


# Leer el conjunto de datos
df = pd.read_csv('Salaries.csv')

# Establecer el estilo de la aplicación
font_family = 'Monaco'
text_color = 'rgb(69,69,69)'
background_color = 'rgb(240,240,240)'
title_size = 50
padding = '15%'

# Función para responder a la pregunta 1
def p1(question,df=df):
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
    return fig, x_label, y_label, title, color, description

# Función para responder a la pregunta 2
def p2(question,df=df):
    df = df.groupby('experience_level')['salary_in_usd'].mean().reset_index()
    df['experience_level'] = df['experience_level'].astype(str)
    title = 'Promedio de salario en USD por nivel de experiencia'
    x_label = 'Nivel de experiencia'
    y_label = 'Salario en USD'
    color = 'rgb(69,69,69)'
    fig = px.bar(df, x='experience_level', y='salary_in_usd')
    experience_levels = ['Nivel inicial', 'Nivel medio', 'Nivel superior', 'Nivel ejecutivo' ]

    # asignar valor en la barra
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

    return fig, x_label, y_label, title, color, description

# Función para responder a la pregunta 3
def p3(question,df=df):
    df = df.groupby('employment_type')['salary_in_usd'].mean().reset_index()
    df['employment_type'] = df['employment_type'].astype(str)
    title = 'Promedio de salario en USD por tipo de empleo'
    x_label = 'Tipo de empleo'
    y_label = 'Salario en USD'
    color = 'rgb(69,69,69)'
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

    return fig, x_label, y_label, title, color, description

#Función para responder a la pregunta 4
def p4(question,df=df):
    company = df.groupby('company_location')['salary_in_usd'].mean().reset_index()
    employee = df.groupby('employee_residence')['salary_in_usd'].mean().reset_index()

    #unir los dataframes
    df = pd.merge(company, employee, left_on='company_location', right_on='employee_residence', how='inner')
    df['salary_in_usd'] = (df['salary_in_usd_x'] + df['salary_in_usd_y']) / 2
    df = df[['company_location', 'salary_in_usd']]
    df = df.dropna()

    # Obtener el nombre completo del país a partir de la abreviatura
    df['company_location'] = df['company_location'].apply(lambda x: get_country_name(x))

    title = 'Promedio de salario entre Desarrolladores y Empresas por región'
    x_label = 'Región'
    y_label = 'Salario en USD'
    color = 'rgb(69,69,69)'
    fig = go.Figure(data=go.Choropleth(
        locations=df['company_location'],
        z = df['salary_in_usd'],
        locationmode = 'country names',
        colorscale = 'greys',
        colorbar_title = "Salario en USD",
    ))
    # Modificar el color del área de trazado para blanco
    fig.update_layout(plot_bgcolor=background_color)

    description = "Al analizar los salarios promedio en USD por región, encontramos que los salarios varían significativamente entre diferentes regiones. En general, los profesionales en Rusia, USA, Canada y Australia destacan por tener los salarios promedio más altos en comparación con otros países. Por otro lado, los salarios promedio en India, Brasil y México son relativamente más bajos en comparación con otros países. Estas disparidades salariales regionales pueden estar influenciadas por factores económicos, políticos y culturales específicos de cada región, así como por la demanda y la oferta de profesionales en el campo de Ciencia de Datos."
    return fig, x_label, y_label, title, color, description

#función para responder a la pregunta 5
def p5(question,df=df):
    df['remote_ratio'] = df['remote_ratio'].map({0: 'No Remoto', 50: 'Mixto', 100: 'Remoto Total'})
    title = 'Promedio de salario en USD por tipo de trabajo remoto'
    x_label = 'Tipo de trabajo remoto'
    y_label = 'Salario en USD'
    color = 'rgb(69,69,69)'

    fig = px.violin(df,y=df['salary_in_usd'] , x=df['remote_ratio'],hover_data=df.columns)

    # Modificar el color
    fig.update_traces(marker_color=color)

    # Modificar el color del área de trazado para blanco
    fig.update_layout(plot_bgcolor=background_color)

    # Cambiar leyenda x
    fig.update_layout(xaxis_title=x_label)
    # Cambiar leyenda y
    fig.update_layout(yaxis_title=y_label)

    # Mostrar el valor de la mediana
    fig.update_traces(box_visible=False, meanline_visible=True)
    fig.update_traces(meanline_color='rgb(69,69,69)', meanline_width=2)



    description = "Al analizar los datos, encontramos que los que trabajan de forma mixta son los que menos ganan en promedio, seguidos por los que trabajan de forma presencial y los que trabajan de forma remota total. Este hallazgo sugiere que el trabajo remoto puede tener un impacto significativo en los salarios de los profesionales en el campo de la Ciencia de Datos. Los profesionales que trabajan de forma remota total tienden a tener salarios más altos en promedio en comparación con aquellos que trabajan de forma mixta o presencial, lo que puede reflejar la flexibilidad y la demanda de habilidades especializadas en el campo de la Ciencia de Datos."

    return fig, x_label, y_label, title, color, description


### Seguir creando funciones para las preguntas restantes...

def p6(question, df=df):
    sueldo_promedio_groupby = df.groupby("company_size")["salary_in_usd"].mean()
    # fig = px.scatter(sueldo_promedio_groupby, size="pop")
    fig = go.Figure(data=[go.Scatter(
        x=sueldo_promedio_groupby.index, y=sueldo_promedio_groupby,
        mode='markers',
        marker=dict(
            color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)',
                   'rgb(44, 160, 101)'],
            opacity=[1, 0.8, 0.6],
            size=[df[df.company_size == "L"].count()[0]/2, df[df.company_size == "M"].count()[0]/2,df[df.company_size == "S"].count()[0]/2],
            )
        )])
    x_label = "tamaño de la empresa"
    y_label = "sueldo en dolares"
    title = "Sueldo promedio en dolares de cientistas de datos según el tamaño de empresa"
    color = 'rgb(69,69,69)'
    description= "Se puede observar que los cientistas de datos que trabajan en empresas de mediano o gran tamaño tienen un sueldo promedio en dolares bastante similar, observando un incremento de menos de tres mil dolares al año al incrementar el tamaño de la empresa. No obstante el cambio desde una empresa pequeña a una mediana significa en promedio un incremento de casi cuarenta mil dolares al año"
    return fig, x_label, y_label, title, color, description

def p7(question,df=df):
    # Comparamos salary_currency con salary_in_usd grafico de barras
    data = df.groupby("job_title")["salary_in_usd"].mean()
    data.sort_values(ascending=False, inplace=True)
    title = 'Salario promedio por titulo laboral'
    x_label = 'Titulo Laboral'
    y_label = 'Salario en USD'
    color = 'rgb(69,69,69)'
    fig = px.scatter(data)
    description= "Se puede observar que los titulos con salarios mas altos son Data Analytics Lead y Financial Data Analyst, por otro lado los puestos con menor remuneracion promedio anual en dolares son Product Data Analyst y Computer Vision Engineer."
    return fig, x_label, y_label, title, color, description

# Funcion para responder la pregunta 8
def p8(question,df=df):
    # Análisis de conversión de moneda
    ''' Evalúe el impacto de las fluctuaciones monetarias en los salarios de la ciencia de datos comparando los salarios en diferentes monedas con sus valores equivalentes en USD. Identifique cualquier diferencia significativa en los niveles salariales después de la conversión de moneda.
    '''
    # Comparamos salary_currency con salary_in_usd grafico de barras
    df = df.groupby('salary_currency')['salary_in_usd'].mean().reset_index()
    df['salary_currency'] = df['salary_currency'].astype(str)

    title = 'Promedio de salario en USD por moneda'
    x_label = 'Moneda'
    y_label = 'Salario en USD'
    color = 'rgb(69,69,69)'
    fig = px.bar(df, x='salary_currency', y='salary_in_usd')

    # asignar valor en la barra
    fig.update_traces(text=round(df['salary_in_usd']), textposition='outside')

    # Modificar el color
    fig.update_traces(marker_color=color)
    # Modificar el color del área de trazado para blanco
    fig.update_layout(plot_bgcolor=background_color)
    # Cambiar leyenda x
    fig.update_layout(xaxis_title=x_label)
    # Cambiar leyenda y
    fig.update_layout(yaxis_title=y_label)

    description= "Podemos notar que los promedios de sueldos más altos son los de las monedas USD (Dolar), CHF (Franco Suizo) y SGD (Dolar de Singapur), mientras que los promedios más bajos son los de las monedas BRL (Real Brasileño), MXN (Peso Mexicano) y TRY (Lira Turca). Esto puede deberse a la fortaleza de la economía de los países que utilizan estas monedas, así como a la demanda de profesionales en el campo de la Ciencia de Datos en estos países."
    return fig, x_label, y_label, title, color, description


# Funcion para responder la pregunta 9
def p9(question,df=df):
    df = df[(df["employment_type"] == "FT") & (df["remote_ratio"] == 50)].copy()
    df.sort_values(by="salary_in_usd", ascending=False, inplace=True)

    title = 'Satisfacción Laboral'
    x_label = 'Titulo Laboral'
    y_label = 'Salario en USD'
    color = 'rgb(69,69,69)'

    fig = px.sunburst(df, path=['company_size', 'experience_level', 'job_title'], values='salary_in_usd')
    description= "Para considerar la satisfacción laboral de los cientistas de datos se consideran primero ciertos criterios predeterminados. Se filtran los datos por los trabajos que ofrecen un 50% de asistencia remota y bajo un contrato full time, dado que estas condiciones permiten un balance entre certeza financiera y relación trabajo-ocio para los trabajadores. Una vez aplicado el filtro se desagregan los datos según el tamaño de la empresa, la experiencia solicitada para los cargos y la acumulación de los salarios para brindar una mejor perspectiva de los trabajos que cumplen con estas condiciones y cuanto dinero invierten las empresas según su tamaño y la experiencia del trabajador a estas oportunidades."
    return fig, x_label, y_label, title, color, description


def p10(question,df=df):
    df = df.groupby(["company_size", "remote_ratio"]).count()
    df = df["Unnamed: 0"].copy()
    df2 = df.reset_index()
    df2['company_size'] = df2['company_size']
    df2["count"] = df2["Unnamed: 0"]
    df2.drop(['Unnamed: 0'], axis=1, inplace=True)

    title = 'Relación entre trabajo remoto y tamaño de la empresa'
    x_label = 'Titulo Laboral'
    y_label = 'Salario en USD'
    color = 'rgb(69,69,69)'

    fig = px.treemap(df2, path=['company_size', 'remote_ratio'], values='count')
    description= "Se observa la relación entre el tamaño de la empresa y la cantidad de trabajo remoto. En todo tamaño de empresa lidera el trabajo cien por ciento remoto, ocupando un mayor área del gráfico. Notar que en las empresas de tamaño mediano se encuentra una menor porporción de trabajo híbrido, donde es más común el trabajo o completamente remoto o completamenre presencial para los trabajos relacionados a la ciencia de datos."
    return fig, x_label, y_label, title, color, description
# Función para crear el gráfico
def create_chart(question,df=df):
    if question == 1: fig, x_label, y_label, title, color, description = p1(question)
    elif question == 2: fig, x_label, y_label, title, color, description = p2(question)
    elif question == 3: fig, x_label, y_label, title, color, description = p3(question)
    elif question == 4: fig, x_label, y_label, title, color, description = p4(question)
    elif question == 5: fig, x_label, y_label, title, color, description = p5(question)
    elif question == 6: fig, x_label, y_label, title, color, description = p6(question)
    elif question == 7: fig, x_label, y_label, title, color, description = p7(question)
    elif question == 8: fig, x_label, y_label, title, color, description = p8(question)
    elif question == 9: fig, x_label, y_label, title, color, description = p9(question)
    elif question == 10: fig, x_label, y_label, title, color, description = p10(question)
    # Agregar más opciones según sea necesario
    else:
        return None, None, None, None, None, None

    fig.update_layout(font_family=font_family)
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
            {'label': '4. Disparidades salariales regionales', 'value': 4},
            {'label': '5. Trabajo Remoto y Salario', 'value': 5},
            {'label': '6. Tamaño de la empresa y salario', 'value': 6},
            {'label': '7. Títulos de trabajo y salario', 'value': 7},
            {'label': '8. Análisis de conversión de moneda', 'value': 8},
            {'label': '9. Análisis de satisfacción salarial', 'value': 9},
            {'label': '10. Disparidades salariales regionales', 'value':10},
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
            html.H2(children=title, style={'textAlign': 'center', 'font-family': font_family, 'color': text_color, 'padding-top': '10px'}),
            html.P(children=description, style={'textAlign': 'justify', 'font-family': font_family, 'color': text_color, 'padding-top': '5px'}),
            dcc.Graph(figure=fig)
        ]
    else:
        return html.H2(children='Pregunta no válida', style={'textAlign': 'center', 'font-family': font_family, 'color': text_color, 'padding-top': '30px'})


# Correr la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
