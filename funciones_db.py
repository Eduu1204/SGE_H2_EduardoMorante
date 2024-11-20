from tkinter import messagebox
from conexion_db import ConexionBD
import matplotlib.pyplot as plt

# Función para crear la conexión a la base de datos
def obtener_conexion():
    return ConexionBD(host="localhost", user="root", password="curso", db="encuestas")


def obtener_consumo_promedio_por_edad():
    try:
        query = '''
        SELECT 
            CASE 
                WHEN edad < 20 THEN 'Menores de 20'
                WHEN edad BETWEEN 20 AND 40 THEN '20-40 años'
                WHEN edad BETWEEN 41 AND 60 THEN '41-60 años'
                ELSE 'Mayores de 60'
            END AS GrupoEdad,
            AVG(BebidasSemana) AS ConsumoPromedio
        FROM encuesta
        GROUP BY GrupoEdad
        ORDER BY AVG(BebidasSemana) DESC
        '''
        db = obtener_conexion()  # Obtener conexión
        datos = db.obtener_datos(query)  # Ejecutar la consulta
        db.cerrar()
        return datos
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al obtener los datos: {str(e)}")
        return []

def obtener_encuestas_ordenadas(campo_orden):
    try:
        # Validar que el campo de orden esté permitido
        campos_validos = ['edad', 'Sexo', 'BebidasSemana', 'CervezasSemana', 'BebidasFinSemana',
                          'BebidasDestiladasSemana', 'VinosSemana', 'PerdidasControl', 'DiversionDependenciaAlcohol',
                          'ProblemasDigestivos', 'TensionAlta', 'DolorCabeza']

        if campo_orden not in campos_validos:
            raise ValueError(f"Campo de orden no válido: {campo_orden}")

        # Realizar la consulta SQL ordenada
        query = f"SELECT * FROM encuesta ORDER BY {campo_orden}"

        db = obtener_conexion()  # Obtener conexión
        encuestas_ordenadas = db.obtener_datos(query)  # Ejecutar consulta y obtener los datos
        db.cerrar()
        return encuestas_ordenadas
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al obtener las encuestas ordenadas: {str(e)}")
        return []

def obtener_encuestas_filtradas(filtro):
    try:
        # Condiciones para cada filtro
        if filtro == "Alta frecuencia de consumo de alcohol":
            query = "SELECT * FROM encuesta WHERE BebidasSemana > 15"  # Ajusta el umbral
        elif filtro == "Perdió el control más de 3 veces":
            query = "SELECT * FROM encuesta WHERE PerdidasControl > 3"
        elif filtro == "Problemas de salud (Dolor de cabeza o Presión alta)":
            query = "SELECT * FROM encuesta WHERE DolorCabeza = 1 OR TensionAlta = 1"
        else:
            return []

        db = obtener_conexion()  # Obtener conexión
        encuestas_filtradas = db.obtener_datos(query)  # Ejecutar consulta y obtener los datos
        db.cerrar()
        return encuestas_filtradas
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al aplicar el filtro: {str(e)}")
        return []

# Función para agregar una nueva encuesta
def agregar_encuesta(edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, bebidas_destiladas_semana,
                     vinos_semana, perdidas_control, diversion_dependencia_alcohol, problemas_digestivos,
                     tension_alta, dolor_cabeza):
    try:
        query = '''
        INSERT INTO encuesta (edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana,
                              VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, 
                              TensionAlta, DolorCabeza)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        db = obtener_conexion()  # Obtener conexión
        db.ejecutar_query   (query, (edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana,
                                  bebidas_destiladas_semana, vinos_semana, perdidas_control,
                                  diversion_dependencia_alcohol, problemas_digestivos, tension_alta, dolor_cabeza))
        db.cerrar()
        messagebox.showinfo("Éxito", "Encuesta agregada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al agregar la encuesta: {str(e)}")


# Función para obtener todas las encuestas
def obtener_encuestas():
    try:
        query = "SELECT * FROM encuesta"
        db = obtener_conexion()  # Obtener conexión
        encuestas = db.obtener_datos(query)
        db.cerrar()
        return encuestas
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al obtener las encuestas: {str(e)}")
        return []

# Función para actualizar una encuesta
def actualizar_encuesta(id_encuesta, edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana,
                        bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia_alcohol,
                        problemas_digestivos, tension_alta, dolor_cabeza):
    try:
        query = '''
        UPDATE encuesta 
        SET edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s, 
            BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, DiversionDependenciaAlcohol=%s,
            ProblemasDigestivos=%s, TensionAlta=%s, DolorCabeza=%s
        WHERE idEncuesta=%s
        '''
        db = obtener_conexion()  # Obtener conexión
        db.ejecutar_query(query, (edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana,
                                  bebidas_destiladas_semana, vinos_semana, perdidas_control,
                                  diversion_dependencia_alcohol, problemas_digestivos, tension_alta, dolor_cabeza, id_encuesta))
        db.cerrar()
        messagebox.showinfo("Éxito", "Encuesta actualizada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al actualizar la encuesta: {str(e)}")

# Función para eliminar una encuesta
def eliminar_encuesta(id_encuesta):
    try:
        query = "DELETE FROM encuesta WHERE idEncuesta=%s"
        db = obtener_conexion()  # Obtener conexión
        db.ejecutar_query(query, (id_encuesta,))
        db.cerrar()
        messagebox.showinfo("Éxito", "Encuesta eliminada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al eliminar la encuesta: {str(e)}")
