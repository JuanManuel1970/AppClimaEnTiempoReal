
from configuracion import API_KEY
import requests
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import pandas as pd
from PIL import Image, ImageTk

from io import BytesIO


datos_historicos = []  


def obtener_datos_clima(ciudad):
    """Consulta la API para obtener datos del clima."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        temperatura = datos["main"]["temp"]
        humedad = datos["main"]["humidity"]
        descripcion = datos["weather"][0]["description"]
        icono_codigo = datos["weather"][0]["icon"]  # Obtiene el código del icono
        return temperatura, humedad, descripcion, icono_codigo
    else:
        return None



def mostrar_clima():
    """Muestra el clima actual y actualiza el gráfico."""
    ciudad = ciudad_entrada.get()
    if not ciudad:
        messagebox.showerror("Error", "Por favor, ingresa una ciudad.")
        return

    datos = obtener_datos_clima(ciudad)
    if datos:
        temperatura, humedad, descripcion, icono_codigo = datos
        resultado_var.set(
            f"Ciudad: {ciudad}\nTemperatura: {temperatura}°C\nHumedad: {humedad}%\nDescripción: {descripcion.capitalize()}"
        )

        mostrar_icono_clima(icono_codigo)  # Llamar a la función para mostrar el icono
        
        tiempo_actual = time.strftime("%Y-%m-%d %H:%M:%S")
        datos_historicos.append([tiempo_actual, ciudad, temperatura, humedad, descripcion])

        actualizar_grafico()
    else:
        messagebox.showerror("Error", "No se pudo obtener el clima. Verifica el nombre de la ciudad.")



def mostrar_icono_clima(icono_codigo):
    """Descarga y muestra el ícono del clima con mejor contraste."""
    url_icono = f"http://openweathermap.org/img/wn/{icono_codigo}@2x.png"
    response = requests.get(url_icono, stream=True)

    if response.status_code == 200:
        img = Image.open(response.raw).convert("RGBA")

        # Crear un fondo oscuro y pegar la imagen encima para contraste
        fondo = Image.new("RGBA", img.size, "black")  # O "gray"
        img = Image.alpha_composite(fondo, img)

        img = ImageTk.PhotoImage(img)
        canvas_icono.create_image(30, 30, image=img)
        canvas_icono.image = img  # Evita que la imagen sea eliminada por el recolector de basura

def actualizar_grafico():
    """Actualiza el gráfico de temperatura."""
    if not datos_historicos:
        return

 
    tiempos = [dato[0] for dato in datos_historicos]
    temperaturas = [dato[2] for dato in datos_historicos]

    ax.clear()
    ax.plot(tiempos[-10:], temperaturas[-10:], marker='o', color='orange')
    ax.set_title("Temperatura en Tiempo Real")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Temperatura (°C)")
    canvas.draw()


def guardar_historico():
    """Guarda el histórico de consultas en un archivo CSV."""
    if datos_historicos:
        df = pd.DataFrame(datos_historicos, columns=["Tiempo", "Ciudad", "Temperatura", "Humedad", "Descripción"])
        df.to_csv("historico_clima.csv", index=False)
        messagebox.showinfo("Información", "Histórico guardado exitosamente.")
    else:
        messagebox.showwarning("Advertencia", "No hay datos para guardar.")


def actualizar_automatico():
    """Actualiza el clima cada 30 segundos si se ingresó una ciudad."""
    ciudad = ciudad_entrada.get()
    if ciudad:  
        mostrar_clima()
    ventana.after(30000, actualizar_automatico)  




ventana = tk.Tk()
ventana.title("Panel de Control - Clima en Tiempo Real")

tk.Label(ventana, text="Ingrese la ciudad:").pack(pady=5)
ciudad_entrada = tk.Entry(ventana)
ciudad_entrada.pack(pady=5)


tk.Button(ventana, text="Consultar Clima", command=mostrar_clima).pack(pady=10)



resultado_var = tk.StringVar()
tk.Label(ventana, textvariable=resultado_var, justify="left").pack(pady=10)
# Canvas para ícono del clima
canvas_icono = tk.Canvas(ventana, width=60, height=60)
canvas_icono.pack(pady=5)

fig = Figure(figsize=(7, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack()


tk.Button(ventana, text="Guardar Histórico", command=guardar_historico).pack(pady=10)


actualizar_automatico()

ventana.mainloop()
