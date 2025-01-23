GRUPO 24 ~ Metro de Buenos Aires

Instrucción de ejecución de la aplicación
1. Ir al directorio Metro de Buenos Aires\Metro de Buenos Aires
2. Ejecutar dentro del directorio Metro de Buenos Aires\Metro de Buenos Aires en una terminal:
	- pip install PySide6
	- pip install geopy
	- python app.py
3. A disfrutar de la aplicación

Instrucción de creación del ejecutable
1. Cambiar lo escrito como "Ruta personal a …" por su ruta en su computadora
2. Ejecutar el siguiente mandato en una terminal
pyinstaller --noconfirm --onefile --windowed ^
    --icon "Ruta personal a \Metro de Buenos Aires\logo.ico" ^
    --name "Metro de Buenos Aires" ^
    --add-data "Ruta personal a \Metro de Buenos Aires\imagenes\mapa.png;imagenes" ^
    --add-data "Ruta personal a \Metro de Buenos Aires\imagenes\Subte-logo.png;imagenes" ^
    "Ruta personal a \Metro de Buenos Aires\app.py"
3. A disfrutar del ejecutable