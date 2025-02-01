
from configuracion import API_KEY
import requests
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import pandas as pd


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
        return temperatura, humedad, descripcion
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
        temperatura, humedad, descripcion = datos
        resultado_var.set(
            f"Ciudad: {ciudad}\nTemperatura: {temperatura}°C\nHumedad: {humedad}%\nDescripción: {descripcion.capitalize()}"
        )
       
        tiempo_actual = time.strftime("%Y-%m-%d %H:%M:%S")
        datos_historicos.append([tiempo_actual, ciudad, temperatura, humedad, descripcion])

      
        actualizar_grafico()

    else:
        messagebox.showerror("Error", "No se pudo obtener el clima. Verifica el nombre de la ciudad.")


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

fig = Figure(figsize=(7, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack()


tk.Button(ventana, text="Guardar Histórico", command=guardar_historico).pack(pady=10)


actualizar_automatico()

ventana.mainloop()
