1. Requisitos Previos
Herramientas Necesarias
Python: Instalar Python 3.8 o superior.

Descargar desde: Python Official Website.
Asegúrate de seleccionar la opción "Add Python to PATH" durante la instalación.

Tkinter:

Tkinter generalmente viene preinstalado con Python. Para verificar:
python -m tkinter
Si no está instalado:
Windows: Asegúrate de que el instalador de Python incluya Tcl/Tk.

MySQL: Instalar MySQL Server.

Descargar desde: MySQL Community Downloads.
Configura un usuario con permisos completos (por ejemplo, root).
Dependencias de Python:

Bibliotecas necesarias: Instalar usando pip:
pip install pymysql pandas openpyxl matplotlib

2. Configuración de la Base de Datos
Creación de la Base de Datos y la Tabla
Abre tu cliente MySQL (MySQL Workbench o consola MySQL).

Ejecuta el archivo ENCUESTAS.txt para crear la base de datos y la tabla:

Asegúrate de que MySQL esté ejecutándose y toma nota de tus credenciales de conexión (host, usuario, contraseña y nombre de la base de datos).

3. Configuración del Proyecto
Archivos de Configuración
Edita la función obtener_conexion en el código para que coincida con los detalles de tu configuración de MySQL:

def obtener_conexion():
    return ConexionBD(
        host="localhost",   # Cambia si MySQL no está en localhost
        user="root",        # Usuario configurado en MySQL
        password="curso", # Contraseña de tu usuario
        db="encuestas"    # Nombre de la base de datos
    )
4. Ejecución del Programa
Pasos para Ejecutar
Guarda todos los archivos de tu proyecto en una carpeta.

Desde la terminal o el IDE que uses (como PyCharm, VSCode), ejecuta el archivo principal del programa:

python interfaz.py
La interfaz gráfica de Tkinter se abrirá automáticamente.

5. Uso de la Aplicación
Operaciones CRUD
Agregar Encuestas:

Llena los campos requeridos (edad, sexo, consumo semanal, etc.) y haz clic en el botón de "Agregar".
Se mostrará un mensaje confirmando la operación.

Leer Encuestas:
Accede a la sección correspondiente en la aplicación para consultar todas las encuestas almacenadas.

Actualizar Encuestas:
Selecciona un registro existente, realiza los cambios y guarda para actualizarlo.

Eliminar Encuestas:
Selecciona un registro y elige la opción de eliminar.

Exportar a Excel
Haz clic en el botón "Exportar a Excel".
Selecciona la ubicación y el nombre del archivo.
El archivo con los datos exportados se guardará en formato .xlsx.

6. Visualización de Gráficos
En la aplicación, accede a la sección de gráficos.
Selecciona el tipo de gráfico deseado:
Consumo promedio por grupo de edad.
Elige el formato del gráfico (barras, pastel o líneas).
Haz clic en "Generar Gráfico". El gráfico aparecerá en una ventana emergente.

Asegúrate de instalar las dependencias con pip install.
