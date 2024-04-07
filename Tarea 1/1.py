'''
Tendencias salariales a lo largo del tiempo: 

Analice cómo han evolucionado los salarios en ciencia de datos a lo largo de 
los años examinando la distribución de los salarios en diferentes años laborales. 
Identifique cualquier tendencia o patrón significativo en el crecimiento o 
disminución del salario a lo largo del tiempo.
'''

# Importar librerías
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('Tarea 1/Salaries.csv')

# Salario en USD promedio por año laboral
df = df.groupby('work_year')['salary_in_usd'].mean().reset_index()
df['work_year'] = df['work_year'].astype(str)

# Crear la figura
fig = px.bar(df, x='work_year', y='salary_in_usd', title='Salario promedio en USD por año laboral')
fig.update_layout(xaxis_title='Año laboral', yaxis_title='Salario en USD')

# Modificar el color de las barras para blanco y negro
fig.update_traces(marker_color='rgb(69,69,69)')
# Modificar el color del área de trazado para blanco y negro
fig.update_layout(plot_bgcolor='rgb(240,240,240)')
# Modificar el color del título del gráfico
fig.update_layout(title_font_color='rgb(69,69,69)')

# Crear el layout
layout = html.Div([
    html.H1(children='Tendencias salariales a lo largo del tiempo', 
    style={'textAlign':'center', 'font-size':50, 'font-family':'Arial', 'color':'rgb(69,69,69)'}),
    dcc.Graph(figure=fig)
])

# Crear la aplicación
app = Dash(__name__)
app.layout = layout

# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)




