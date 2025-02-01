Panel de Clima en Tiempo Real
🌦️ Descripción :
Aplicación de escritorio desarrollada en Python que permite consultar y visualizar datos del clima en tiempo real de cualquier ciudad, obtenidos de la API de OpenWeatherMap. La aplicación muestra la temperatura, humedad y descripción del clima, junto con un gráfico dinámico de las temperaturas históricas. Además, permite guardar las consultas en un archivo CSV.

🚀 Características :
Consulta datos del clima en tiempo real.
Visualización de temperaturas mediante gráficos dinámicos.
Registro histórico de las consultas de clima.
Exportación del histórico a un archivo CSV.
Actualización automática cada 30 segundos.

🛠️ Tecnologías Utilizadas :
Python: Lenguaje principal.
Tkinter: Interfaz gráfica de usuario.
Matplotlib: Gráficos dinámicos.
Pandas: Manejo de datos tabulares.
Requests: Consulta a la API.


⚙️ Requisitos :
Python 3.7 o superior
Librerías necesarias:
bash
Copiar
Editar
pip install matplotlib pandas requests


📝 Configuración :
Clave de API:
Crea un archivo configuracion.py y añade tu clave de API de OpenWeatherMap:
python
Copiar
Editar
API_KEY = "tu_clave_api_aqui"
Ejecutar la aplicación:

bash
Copiar
Editar
python main.py



📊 Uso:
Introduce el nombre de la ciudad en la interfaz.
Haz clic en "Consultar Clima".
Observa los datos del clima y el gráfico de temperatura en tiempo real.
Haz clic en "Guardar Histórico" para exportar los datos a un CSV.
🎨 Captura de Pantalla

![image](https://github.com/user-attachments/assets/4887985b-664d-46f8-9951-84837e97bf1b)







💡 Mejoras Futuras:

Soporte para múltiples ciudades.
Predicciones del clima.
Gráficos más detallados.
