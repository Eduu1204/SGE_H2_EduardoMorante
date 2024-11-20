import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from tkinter import filedialog

import pandas as pd

from funciones_db import agregar_encuesta, actualizar_encuesta, eliminar_encuesta, obtener_encuestas, obtener_conexion, \
    obtener_encuestas_filtradas, obtener_encuestas_ordenadas, \
    obtener_consumo_promedio_por_edad


class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Encuestas de Consumo de Alcohol")
        self.root.geometry("1400x800")  # Ajustamos el tamaño de la ventana
        self.root.resizable(True, True)  # Permite cambiar el tamaño de la ventana

        # Botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(side=tk.TOP, fill=tk.X)

        # Botones en la parte superior, centrados y espaciados
        self.boton_agregar = tk.Button(frame_botones, text="Agregar Encuesta", command=self.mostrar_ventana_encuesta, width=20, height=2)
        self.boton_agregar.grid(row=0, column=0, padx=5, pady=5)

        self.boton_actualizar = tk.Button(frame_botones, text="Actualizar Encuesta", command=self.actualizar_encuesta, width=20, height=2)
        self.boton_actualizar.grid(row=0, column=1, padx=5, pady=5)

        self.boton_eliminar = tk.Button(frame_botones, text="Eliminar Encuesta", command=self.eliminar_encuesta, width=20, height=2)
        self.boton_eliminar.grid(row=0, column=2, padx=5, pady=5)

        self.boton_mostrar = tk.Button(frame_botones, text="Mostrar Encuestas", command=self.mostrar_encuestas, width=20, height=2)
        self.boton_mostrar.grid(row=0, column=3, padx=5, pady=5)

        self.boton_consultar = tk.Button(frame_botones, text="Consultar Encuestas", command=self.abrir_consulta, width=20, height=2)
        self.boton_consultar.grid(row=0, column=4, padx=5, pady=5)

        self.boton_filtros = tk.Button(frame_botones, text="Aplicar Filtro", command=self.abrir_filtro, width=20, height=2)
        self.boton_filtros.grid(row=0, column=5, padx=5, pady=5)

        self.boton_grafico = tk.Button(frame_botones, text="Visualizar en Gráfico", command=self.abrir_graficos, width=20, height=2)
        self.boton_grafico.grid(row=0, column=6, padx=5, pady=5)

        self.boton_exportar_excel = tk.Button(frame_botones, text="Exportar a Excel", command=self.exportar_a_excel, width=20, height=2)
        self.boton_exportar_excel.grid(row=0, column=7, padx=5, pady=5)

        frame_tabla = tk.Frame(self.root)
        frame_tabla.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=0)

        # Treeview para mostrar las encuestas
        self.treeview = ttk.Treeview(frame_tabla, columns=("ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana",
                                                           "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana",
                                                           "PerdidasControl", "DiversionDependenciaAlcohol",
                                                           "ProblemasDigestivos", "TensionAlta", "DolorCabeza"),
                                     show="headings")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Configuración de las columnas del Treeview con anchos ajustados
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Edad", text="Edad")
        self.treeview.heading("Sexo", text="Sexo")
        self.treeview.heading("BebidasSemana", text="Bebidas/semana")
        self.treeview.heading("CervezasSemana", text="Cervezas/semana")
        self.treeview.heading("BebidasFinSemana", text="Bebidas fin de semana")
        self.treeview.heading("BebidasDestiladasSemana", text="Bebidas destiladas")
        self.treeview.heading("VinosSemana", text="Vinos/semana")
        self.treeview.heading("PerdidasControl", text="Pérdidas control")
        self.treeview.heading("DiversionDependenciaAlcohol", text="Diversión/Dependencia")
        self.treeview.heading("ProblemasDigestivos", text="Problemas digestivos")
        self.treeview.heading("TensionAlta", text="Tensión alta")
        self.treeview.heading("DolorCabeza", text="Dolor de cabeza")

        # Ajustar los anchos de las columnas
        self.treeview.column("ID", width=50, anchor="center")
        self.treeview.column("Edad", width=60, anchor="center")
        self.treeview.column("Sexo", width=80, anchor="center")
        self.treeview.column("BebidasSemana", width=120, anchor="center")
        self.treeview.column("CervezasSemana", width=120, anchor="center")
        self.treeview.column("BebidasFinSemana", width=150, anchor="center")
        self.treeview.column("BebidasDestiladasSemana", width=150, anchor="center")
        self.treeview.column("VinosSemana", width=100, anchor="center")
        self.treeview.column("PerdidasControl", width=120, anchor="center")
        self.treeview.column("DiversionDependenciaAlcohol", width=200, anchor="center")
        self.treeview.column("ProblemasDigestivos", width=150, anchor="center")
        self.treeview.column("TensionAlta", width=150, anchor="center")
        self.treeview.column("DolorCabeza", width=150, anchor="center")

    def exportar_a_excel(self):
        try:
            # Obtener las encuestas (puedes personalizar la consulta según lo que quieras exportar)
            encuestas = obtener_encuestas()
            if not encuestas:
                messagebox.showerror("Error", "No hay encuestas para exportar.")
                return

            # Convertir los datos en un DataFrame de pandas
            columnas = ['ID', 'Edad', 'Sexo', 'Bebidas Semana', 'Cervezas Semana', 'Bebidas Fin Semana',
                        'Bebidas Destiladas Semana', 'Vinos Semana', 'Perdidas Control',
                        'Diversión Dependencia Alcohol', 'Problemas Digestivos', 'Tensión Alta', 'Dolor Cabeza']
            df = pd.DataFrame(encuestas, columns=columnas)

            # Pedir al usuario que seleccione la ubicación y el nombre del archivo
            archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

            if archivo:
                # Guardar el DataFrame como archivo Excel
                df.to_excel(archivo, index=False, engine='openpyxl')
                messagebox.showinfo("Éxito", f"Encuestas exportadas correctamente a {archivo}")

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al exportar a Excel: {str(e)}")


    def abrir_graficos(self):
        ventana_graficos = tk.Toplevel(self.root)
        ventana_graficos.title("Visualización de Gráficos")
        ventana_graficos.geometry("400x300")

        # Selección del gráfico
        etiqueta = tk.Label(ventana_graficos, text="Selecciona el gráfico a generar:")
        etiqueta.pack(pady=10)

        opciones_grafico = ["Consumo Promedio por Grupo de Edad"]
        grafico_seleccionado = tk.StringVar()

        combo_graficos = ttk.Combobox(ventana_graficos, textvariable=grafico_seleccionado, values=opciones_grafico, state="readonly")
        combo_graficos.pack(pady=10)

        # Selección del tipo de gráfico
        etiqueta_tipo = tk.Label(ventana_graficos, text="Selecciona el tipo de gráfico:")
        etiqueta_tipo.pack(pady=10)

        opciones_tipo = ["Barras", "Pastel", "Líneas"]
        tipo_grafico = tk.StringVar()

        combo_tipo = ttk.Combobox(ventana_graficos, textvariable=tipo_grafico, values=opciones_tipo, state="readonly")
        combo_tipo.pack(pady=10)

        # Botón para generar gráfico
        boton_generar = tk.Button(
            ventana_graficos,
            text="Generar Gráfico",
            command=lambda: self.generar_grafico(grafico_seleccionado.get(), tipo_grafico.get(), ventana_graficos)
        )
        boton_generar.pack(pady=10)



    def generar_grafico(self, grafico_seleccionado, tipo_grafico, ventana_graficos):
        try:
            if not grafico_seleccionado or not tipo_grafico:
                messagebox.showerror("Error", "Debes seleccionar el gráfico y el tipo de gráfico.")
                return

            # Consumo promedio por grupo de edad
            if grafico_seleccionado == "Consumo Promedio por Grupo de Edad":
                datos = obtener_consumo_promedio_por_edad()
                if not datos:
                    raise ValueError("No hay datos disponibles para esta consulta.")

                grupos = [fila[0] for fila in datos]
                consumos = [fila[1] for fila in datos]

                plt.figure(figsize=(8, 5))
                if tipo_grafico == "Barras":
                    plt.bar(grupos, consumos, color='skyblue')
                    plt.ylabel("Consumo Promedio (Bebidas/semana)")
                elif tipo_grafico == "Líneas":
                    plt.plot(grupos, consumos, marker='o', color='blue', linestyle='--')
                    plt.ylabel("Consumo Promedio (Bebidas/semana)")
                elif tipo_grafico == "Pastel":
                    plt.pie(consumos, labels=grupos, autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)

                plt.title("Consumo Promedio por Grupo de Edad")
                if tipo_grafico != "Pastel":
                    plt.xlabel("Grupo de Edad")
                plt.show()

            else:
                messagebox.showerror("Error", "Selecciona un gráfico válido.")
                return

            ventana_graficos.destroy()  # Cerrar la ventana después de mostrar el gráfico

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {str(e)}")


    def abrir_filtro(self):
        ventana_filtro = tk.Toplevel(self.root)
        ventana_filtro.title("Aplicar Filtro")
        ventana_filtro.geometry("350x250")

        etiqueta = tk.Label(ventana_filtro, text="Selecciona el filtro:")
        etiqueta.pack(pady=10)

        filtro_seleccionado = tk.StringVar()
        filtros = [
            "Alta frecuencia de consumo de alcohol",
            "Perdió el control más de 3 veces",
            "Problemas de salud (Dolor de cabeza o Presión alta)"
        ]

        combo_filtros = ttk.Combobox(ventana_filtro, textvariable=filtro_seleccionado, values=filtros, state="readonly")
        combo_filtros.pack(pady=10)

        boton_aplicar = tk.Button(ventana_filtro, text="Aplicar Filtro", command=lambda: self.aplicar_filtro(filtro_seleccionado.get(), ventana_filtro))
        boton_aplicar.pack(pady=10)

    def aplicar_filtro(self, filtro, ventana_filtro):
        try:
            # Llamar a la función de filtro en funciones_bd.py
            encuestas_filtradas = obtener_encuestas_filtradas(filtro)

            # Limpiar el Treeview
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            # Mostrar los resultados filtrados en el Treeview
            for encuesta in encuestas_filtradas:
                self.treeview.insert("", "end", values=encuesta)

            ventana_filtro.destroy()  # Cerrar la ventana de filtro

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al aplicar el filtro: {str(e)}")


    def abrir_consulta(self):
        ventana_consulta = tk.Toplevel(self.root)
        ventana_consulta.title("Seleccionar Campo de Orden")
        ventana_consulta.geometry("350x250")

        etiqueta = tk.Label(ventana_consulta, text="Selecciona el campo por el cual ordenar las encuestas:")
        etiqueta.pack(pady=10)

        campo_ordenado = tk.StringVar()
        campos = [
            "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
            "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
            "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"
        ]

        combo_campos = ttk.Combobox(ventana_consulta, textvariable=campo_ordenado, values=campos, state="readonly")
        combo_campos.pack(pady=10)

        boton_aplicar = tk.Button(ventana_consulta, text="Aplicar Consulta", command=lambda: self.aplicar_consulta(campo_ordenado.get(), ventana_consulta))
        boton_aplicar.pack(pady=10)

    def aplicar_consulta(self, campo_orden, ventana_consulta):
        try:
            # Llamar a la función de consulta en funciones_bd.py para obtener las encuestas ordenadas
            encuestas_ordenadas = obtener_encuestas_ordenadas(campo_orden)

            # Limpiar el Treeview
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            # Mostrar los resultados ordenados en el Treeview
            for encuesta in encuestas_ordenadas:
                self.treeview.insert("", "end", values=encuesta)

            ventana_consulta.destroy()  # Cerrar la ventana de consulta

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al aplicar la consulta: {str(e)}")

    def mostrar_ventana_encuesta(self):
        # Crear una ventana secundaria para ingresar la encuesta
        ventana_secundaria = tk.Toplevel(self.root)
        ventana_secundaria.title("Formulario Encuesta")
        ventana_secundaria.geometry("400x500")  # Ajusta el tamaño según tus necesidades

        # Campos de la encuesta en la ventana secundaria
        etiqueta_edad = tk.Label(ventana_secundaria, text="Edad:")
        etiqueta_edad.grid(row=0, column=0, sticky="w", pady=5)
        entrada_edad = tk.Entry(ventana_secundaria)
        entrada_edad.grid(row=0, column=1, pady=5)

        etiqueta_sexo = tk.Label(ventana_secundaria, text="Sexo:")
        etiqueta_sexo.grid(row=1, column=0, sticky="w", pady=5)
        entrada_sexo = ttk.Combobox(ventana_secundaria, values=["Hombre", "Mujer"], state="readonly")
        entrada_sexo.set("Hombre")
        entrada_sexo.grid(row=1, column=1, pady=5)

        etiqueta_bebidas_semana = tk.Label(ventana_secundaria, text="Bebidas Semana:")
        etiqueta_bebidas_semana.grid(row=2, column=0, sticky="w", pady=5)
        entrada_bebidas_semana = tk.Entry(ventana_secundaria)
        entrada_bebidas_semana.grid(row=2, column=1, pady=5)

        etiqueta_cervezas_semana = tk.Label(ventana_secundaria, text="Cervezas Semana:")
        etiqueta_cervezas_semana.grid(row=3, column=0, sticky="w", pady=5)
        entrada_cervezas_semana = tk.Entry(ventana_secundaria)
        entrada_cervezas_semana.grid(row=3, column=1, pady=5)

        etiqueta_bebidas_fin_semana = tk.Label(ventana_secundaria, text="Bebidas Fin de Semana:")
        etiqueta_bebidas_fin_semana.grid(row=4, column=0, sticky="w", pady=5)
        entrada_bebidas_fin_semana = tk.Entry(ventana_secundaria)
        entrada_bebidas_fin_semana.grid(row=4, column=1, pady=5)

        etiqueta_bebidas_destiladas_semana = tk.Label(ventana_secundaria, text="Bebidas Destiladas Semana:")
        etiqueta_bebidas_destiladas_semana.grid(row=5, column=0, sticky="w", pady=5)
        entrada_bebidas_destiladas_semana = tk.Entry(ventana_secundaria)
        entrada_bebidas_destiladas_semana.grid(row=5, column=1, pady=5)

        etiqueta_vinos_semana = tk.Label(ventana_secundaria, text="Vinos Semana:")
        etiqueta_vinos_semana.grid(row=6, column=0, sticky="w", pady=5)
        entrada_vinos_semana = tk.Entry(ventana_secundaria)
        entrada_vinos_semana.grid(row=6, column=1, pady=5)

        etiqueta_perdidas_control = tk.Label(ventana_secundaria, text="Perdidas de Control:")
        etiqueta_perdidas_control.grid(row=7, column=0, sticky="w", pady=5)
        entrada_perdidas_control = tk.Entry(ventana_secundaria)
        entrada_perdidas_control.grid(row=7, column=1, pady=5)

        etiqueta_diversion_dependencia_alcohol = tk.Label(ventana_secundaria, text="Diversión/Dependencia Alcohol:")
        etiqueta_diversion_dependencia_alcohol.grid(row=8, column=0, sticky="w", pady=5)
        entrada_diversion_dependencia_alcohol = tk.Entry(ventana_secundaria)
        entrada_diversion_dependencia_alcohol.grid(row=8, column=1, pady=5)

        etiqueta_problemas_digestivos = tk.Label(ventana_secundaria, text="Problemas Digestivos:")
        etiqueta_problemas_digestivos.grid(row=9, column=0, sticky="w", pady=5)
        entrada_problemas_digestivos = tk.Entry(ventana_secundaria)
        entrada_problemas_digestivos.grid(row=9, column=1, pady=5)

        etiqueta_tension_alta = tk.Label(ventana_secundaria, text="Tensión Alta:")
        etiqueta_tension_alta.grid(row=10, column=0, sticky="w", pady=5)
        entrada_tension_alta = tk.Entry(ventana_secundaria)
        entrada_tension_alta.grid(row=10, column=1, pady=5)

        etiqueta_dolor_cabeza = tk.Label(ventana_secundaria, text="Dolor de Cabeza:")
        etiqueta_dolor_cabeza.grid(row=11, column=0, sticky="w", pady=5)
        entrada_dolor_cabeza = tk.Entry(ventana_secundaria)
        entrada_dolor_cabeza.grid(row=11, column=1, pady=5)

        # Botón para guardar la encuesta
        boton_guardar = tk.Button(ventana_secundaria, text="Guardar Encuesta", command=lambda: self.guardar_encuesta(
            ventana_secundaria, entrada_edad, entrada_sexo, entrada_bebidas_semana, entrada_cervezas_semana,
            entrada_bebidas_fin_semana, entrada_bebidas_destiladas_semana, entrada_vinos_semana,
            entrada_perdidas_control, entrada_diversion_dependencia_alcohol, entrada_problemas_digestivos,
            entrada_tension_alta, entrada_dolor_cabeza))
        boton_guardar.grid(row=12, column=0, columnspan=2, pady=10)

    def guardar_encuesta(self, ventana, *entradas):
        # Recolectamos los datos de las entradas
        edad = entradas[0].get()
        sexo = entradas[1].get()
        bebidas_semana = entradas[2].get()
        cervezas_semana = entradas[3].get()
        bebidas_fin_semana = entradas[4].get()
        bebidas_destiladas_semana = entradas[5].get()
        vinos_semana = entradas[6].get()
        perdidas_control = entradas[7].get()
        diversion_dependencia_alcohol = entradas[8].get()
        problemas_digestivos = entradas[9].get()
        tension_alta = entradas[10].get()
        dolor_cabeza = entradas[11].get()

        # Validar que todos los campos estén llenos
        if not all([edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana, bebidas_destiladas_semana,
                    vinos_semana, perdidas_control, diversion_dependencia_alcohol, problemas_digestivos,
                    tension_alta, dolor_cabeza]):
            messagebox.showerror("Error", "Por favor ingrese todos los datos.")
            return
        try:
            edad_int = int(edad)
            if edad_int < 18:
                messagebox.showerror("Error", "La edad debe ser igual o mayor a 18 años.")
                return
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return

        # Llamar a la función para agregar la encuesta a la base de datos
        agregar_encuesta(edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana,
                         bebidas_destiladas_semana, vinos_semana, perdidas_control, diversion_dependencia_alcohol,
                         problemas_digestivos, tension_alta, dolor_cabeza)

        ventana.destroy()  # Cerrar la ventana secundaria


    def actualizar_encuesta(self):
        try:
            # Obtener el ID de la encuesta seleccionada
            item = self.treeview.selection()[0]
            id_encuesta = self.treeview.item(item, "values")[0]

            # Crear una ventana emergente para seleccionar el campo a actualizar
            campos = [
                "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
                "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"
            ]

            # Crear un combo box para seleccionar el campo a actualizar
            ventana_seleccion = tk.Toplevel(self.root)
            ventana_seleccion.title("Seleccionar Campo a Actualizar")
            ventana_seleccion.geometry("300x150")

            etiqueta = tk.Label(ventana_seleccion, text="Selecciona el campo a actualizar:")
            etiqueta.pack(pady=10)

            campo_seleccionado = tk.StringVar()
            combo_campos = ttk.Combobox(ventana_seleccion, textvariable=campo_seleccionado, values=campos, state="readonly")
            combo_campos.pack(pady=10)

            boton_aceptar = tk.Button(ventana_seleccion, text="Aceptar", command=lambda: self.mostrar_entrada(ventana_seleccion, campo_seleccionado, id_encuesta))
            boton_aceptar.pack(pady=10)

        except IndexError:
            messagebox.showerror("Error", "Por favor seleccione una encuesta para actualizar.")

    def mostrar_entrada(self, ventana_seleccion, campo_seleccionado, id_encuesta):
        campo = campo_seleccionado.get()

        # Cerrar la ventana de selección
        ventana_seleccion.destroy()

        # Crear una nueva ventana para ingresar el nuevo valor
        ventana_ingreso = tk.Toplevel(self.root)
        ventana_ingreso.title(f"Ingresar nuevo valor para {campo}")
        ventana_ingreso.geometry("300x150")

        etiqueta_ingreso = tk.Label(ventana_ingreso, text=f"Ingrese el nuevo valor para {campo}:")
        etiqueta_ingreso.pack(pady=10)

        entrada_nuevo_valor = tk.Entry(ventana_ingreso, width=30)
        entrada_nuevo_valor.pack(pady=10)

        boton_guardar = tk.Button(ventana_ingreso, text="Actualizar", command=lambda: self.guardar_actualizacion(id_encuesta, campo, entrada_nuevo_valor, ventana_ingreso))
        boton_guardar.pack(pady=10)

    def guardar_actualizacion(self, id_encuesta, campo, entrada_nuevo_valor, ventana_ingreso):
        nuevo_valor = entrada_nuevo_valor.get()

        # Verificar que se haya ingresado un valor
        if nuevo_valor:
            try:
                # Actualizar el campo seleccionado en la base de datos
                query = f"UPDATE encuesta SET {campo}=%s WHERE idEncuesta=%s"
                db = obtener_conexion()  # Obtener conexión
                db.ejecutar_query(query, (nuevo_valor, id_encuesta))
                db.cerrar()

                messagebox.showinfo("Éxito", f"{campo} actualizado correctamente.")

                # Preguntar si se desea actualizar más campos
                respuesta = messagebox.askyesno("Actualizar más", "¿Deseas actualizar otro campo?")
                if respuesta:
                    self.actualizar_encuesta()  # Llamar de nuevo a la función para permitir seleccionar otro campo a actualizar
                else:
                    ventana_ingreso.destroy()  # Cerrar la ventana de ingreso

            except Exception as e:
                messagebox.showerror("Error", f"Hubo un error al actualizar {campo}: {str(e)}")
        else:
            messagebox.showerror("Error", "Por favor ingrese un valor.")

    def eliminar_encuesta(self):
        try:
            item = self.treeview.selection()[0]
            id_encuesta = self.treeview.item(item, "values")[0]

            if messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta encuesta?"):
                eliminar_encuesta(id_encuesta)
                self.treeview.delete(item)
        except IndexError:
            messagebox.showerror("Error", "Por favor seleccione una encuesta para eliminar.")


    def mostrar_encuestas(self):
        # Limpiar la vista previa
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        encuestas = obtener_encuestas()
        for encuesta in encuestas:
            self.treeview.insert("", "end", values=encuesta)


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
