import time
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMainWindow, \
    QStackedWidget, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QScrollArea, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys
import controller
import search as search
import os

def ruta_absoluta(nombre_archivo):
    """Devuelve la ruta correcta del archivo empaquetado o en desarrollo."""
    if hasattr(sys, '_MEIPASS'):
        # Modo empaquetado
        return os.path.join(sys._MEIPASS, nombre_archivo)
    # Modo desarrollo
    return os.path.join(os.path.abspath("."), nombre_archivo)

def filter_options(text, combo_box, options):
    filtered_options = [option for option in options if text.lower() in option.lower()]
    combo_box.clear()
    combo_box.addItems(filtered_options)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        #Configuramos el area de resultados
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        #Obtenemos la lista de estaciones
        self.conn = controller.createDB()
        self.cursor = self.conn.cursor()
        consulta = "SELECT nombre_estacion FROM estacion;"
        self.cursor.execute(consulta)
        res = self.cursor.fetchall()
        self.todas_estaciones = [fila[0] for fila in res]
        self.todas_estaciones.sort()

        #Creamos estructuras para mostrar resultados
        self.estaciones = []
        self.colores = {
            "A": "#09b3dc",
            "B": "#f04236",
            "C": "#0c6fb4",
            "D": "#00836a",
            "E": "#7b2e90"
        }

        #Configuramos las páginas y ventanas de la interfaz
        self.setWindowTitle("Metro de Buenos Aires")
        self.setStyleSheet("background-color: #e0e0e0")

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.ppal = QWidget(self)
        self.p_mapa = QWidget(self)
        self.p_calcular = QWidget(self)
        self.p_res = QWidget(self)

        self.stacked_widget.addWidget(self.ppal)
        self.stacked_widget.addWidget(self.p_mapa)
        self.stacked_widget.addWidget(self.p_calcular)
        self.stacked_widget.addWidget(self.p_res)

        self.setup_pagina_principal()
        self.setup_pagina_1()
        self.setup_pagina_2()

    def setup_pagina_principal(self):
        # Layout principal
        layout_principal = QHBoxLayout(self.ppal)
        layout_principal.addSpacing(50)

        # Foto en la parte izquierda
        label_imagen = QLabel(self.ppal)
        label_imagen.setPixmap(icon)
        label_imagen.setScaledContents(True)
        label_imagen.setFixedSize(400, 400)

        #Creamos un layout para los botones y el titulo
        layout_central = QVBoxLayout()

        #Creamos el titulo
        label_titulo = QLabel("METRO DE BUENOS AIRES")
        label_titulo.setStyleSheet("font-size: 55px; font-weight: bold; color: black")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botón 1 para abrir Ventana 1
        boton1 = QPushButton("ABRIR MAPA")
        boton1.setFixedSize(500, 200)
        boton1.setStyleSheet("font-size: 35px; background-color: #f6cd19; border-radius: 20px; color: black")
        boton1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_mapa))


        # Botón 2 para abrir Ventana 2
        boton2 = QPushButton("CALCULAR TRAYECTO")
        boton2.setFixedSize(500, 200)
        boton2.setStyleSheet("font-size: 35px; background-color: #f6cd19; border-radius: 20px; color: black")
        boton2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_calcular))

        #Añadimos botones y titulo al layout
        layout_central.addStretch(1)
        layout_central.addWidget(label_titulo, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_central.addSpacing(40)
        layout_central.addWidget(boton1, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_central.addSpacing(40)
        layout_central.addWidget(boton2, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_central.addStretch(2)

        #Añadimos layout al layout principal
        layout_principal.addWidget(label_imagen)
        layout_principal.addLayout(layout_central)

    def setup_pagina_1(self):
        layout = QVBoxLayout(self.p_mapa)

        label = QLabel("MAPA DEL METRO DE BUENOS AIRES")
        label.setStyleSheet("font-size: 35px; font-weight: bold; color: black")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_map = QLabel()
        mapa = QPixmap(ruta_absoluta("imagenes/mapa.png"))
        label_map.setPixmap(mapa)
        label_map.setScaledContents(True)
        label_map.setFixedSize(420, 625)

        # Botón para volver a la página principal
        boton_volver = QPushButton("Inicio")
        boton_volver.setFixedSize(215, 80)
        boton_volver.setStyleSheet("font-size: 25px; background-color: #f6cd19; border-radius: 20px; color: black")
        boton_volver.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.ppal))

        # Botón para cambiar a Calcular
        boton_calcular = QPushButton("Calcular Trayecto")
        boton_calcular.setFixedSize(215, 80)
        boton_calcular.setStyleSheet("font-size: 25px; background-color: #f6cd19; border-radius: 20px; color: black")
        boton_calcular.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_calcular))


        button_layout = QHBoxLayout()
        button_layout.addWidget(boton_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        button_layout.addStretch()
        button_layout.addWidget(boton_calcular, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addWidget(label)
        layout.addSpacing(20)
        layout.addWidget(label_map, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(50)
        layout.addStretch()
        layout.addLayout(button_layout)

    def setup_pagina_2(self):
        layout = QVBoxLayout(self.p_calcular)

        label = QLabel("CALCULAR TRAYECTO")
        label.setStyleSheet("font-size: 35px; font-weight: bold; color: black")

        label_icon = QLabel()
        label_icon.setPixmap(icon)
        label_icon.setScaledContents(True)
        label_icon.setFixedSize(100, 100)
        left_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        right_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        #Creamos los recuadros para introducir los nombres de las estaciones
        text_input = QLineEdit()
        text_input.setPlaceholderText("Estación de origen")
        text_input.setStyleSheet("background-color: white; color: black")
        text_input.setFixedSize(450, 30)

        text_input2 = QLineEdit()
        text_input2.setPlaceholderText("Estación de destino")
        text_input2.setStyleSheet("background-color: white; color: black")
        text_input2.setFixedSize(450, 30)

        text_layout = QHBoxLayout()
        text_layout.addItem(left_spacer)
        text_layout.addWidget(text_input, alignment=Qt.AlignmentFlag.AlignLeft)
        text_layout.addStretch()
        text_layout.addWidget(text_input2, alignment=Qt.AlignmentFlag.AlignRight)
        text_layout.addItem(right_spacer)


        # Añadimos las cajas de opciones
        combo_box = QComboBox()
        combo_box.setEditable(False)
        combo_box.setStyleSheet("background-color: white; color: black")
        combo_box.setFixedSize(450, 30)
        combo_box.addItems(self.todas_estaciones)
        text_input.textChanged.connect(lambda text: filter_options(text, combo_box, self.todas_estaciones))


        combo_box2 = QComboBox()
        combo_box2.setEditable(False)
        combo_box2.setStyleSheet("background-color: white; color: black")
        combo_box2.setFixedSize(450, 30)
        combo_box2.addItems(self.todas_estaciones)
        text_input2.textChanged.connect(lambda text: filter_options(text, combo_box2, self.todas_estaciones))


        #Creamos un layout para los comboBox
        combo_layout = QHBoxLayout()
        combo_layout.addItem(left_spacer)
        combo_layout.addWidget(combo_box, alignment=Qt.AlignmentFlag.AlignLeft)
        combo_layout.addStretch()
        combo_layout.addWidget(combo_box2, alignment=Qt.AlignmentFlag.AlignRight)
        combo_layout.addItem(right_spacer)

        message = QLabel()
        message.setStyleSheet("font-size: 25px; font-weight: bold; color: black")

        boton_calcular = QPushButton("Calcular")
        boton_calcular.setFixedSize(300, 100)
        boton_calcular.setStyleSheet("font-size: 25px; background-color: #f6cd19; border-radius: 20px; color: black")
        boton_calcular.clicked.connect(lambda: self.calcular(message, combo_box.currentText(), combo_box2.currentText(),
                                                             combo_box, combo_box2))

        # Botón para volver a la página principal
        boton_volver = QPushButton("Volver")
        boton_volver.setFixedSize(215, 80)
        boton_volver.setStyleSheet("font-size: 25px; background-color: #f6cd19; border-radius: 20px; color: black")
        boton_volver.clicked.connect(lambda: self.volver(message, combo_box, combo_box2))

        # Botón para cambiar a Calcular
        boton_mapa = QPushButton("Mapa")
        boton_mapa.setFixedSize(215, 80)
        boton_mapa.setStyleSheet("font-size: 25px; background-color: #f6cd19; border-radius: 20px; color: black")
        boton_mapa.clicked.connect(lambda: self.mapa(message, combo_box, combo_box2))

        button_layout = QHBoxLayout()
        button_layout.addWidget(boton_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        button_layout.addStretch()
        button_layout.addWidget(boton_mapa, alignment=Qt.AlignmentFlag.AlignRight)




        # Añadir los elementos al layout
        layout.addWidget(label_icon, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(70)
        layout.addLayout(text_layout)
        layout.addLayout(combo_layout)
        layout.addSpacing(50)
        layout.addWidget(boton_calcular, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(50)
        layout.addWidget(message, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        layout.addLayout(button_layout)

    def setup_pagina_3(self):
        layout = QVBoxLayout(self.p_res)

        # Botón para volver a la página principal
        boton_volver = QPushButton("Volver")
        boton_volver.setFixedSize(215, 80)
        boton_volver.setStyleSheet("font-size: 25px; background-color: #f6cd19; border-radius: 20px; color: black")
        boton_volver.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_calcular))

        # Botón para cambiar a la ventana de inicio
        boton_mapa = QPushButton("Inicio")
        boton_mapa.setFixedSize(215, 80)
        boton_mapa.setStyleSheet("font-size: 25px; background-color: #f6cd19; border-radius: 20px; color: black")
        boton_mapa.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.ppal))

        button_layout = QHBoxLayout()
        button_layout.addWidget(boton_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        button_layout.addStretch()
        button_layout.addWidget(boton_mapa, alignment=Qt.AlignmentFlag.AlignRight)


        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Eliminamos los widgets anteriores
        for i in reversed(range(container_layout.count())):
            widget = container_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Añadimos las estaciones al widget
        for i, (station, line, line_change) in enumerate(self.estaciones):
            column_estaciones = QHBoxLayout()
            column_estaciones.setAlignment(Qt.AlignmentFlag.AlignCenter)

            label_linea = QLabel(line)
            label_linea.setFixedSize(24, 24)
            label_linea.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_linea.setStyleSheet(f" background-color: {self.color_linea(station)}; border: 2px solid black;" +
                "border-radius: 12px; color: black; font-weight: bold;")
            column_estaciones.addWidget(label_linea)

            # Añadimos nombre de la estación
            station_label = QLabel(station)
            station_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            station_label.setStyleSheet("font-size: 16px; color: black;")
            column_estaciones.addWidget(station_label)

            # Agregamos la fila de estación al contenedor principal
            container_layout.addLayout(column_estaciones)

            # Añadir cambio de línea
            if line_change is not None:
                label_trans = QLabel(f"Cambio a {line_change}")
                label_trans.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label_trans.setStyleSheet("font-size: 14px; color: red; font-weight: bold; color: black")
                container_layout.addWidget(label_trans)


            if i < len(self.estaciones) - 1:
                flecha = QLabel("↓")
                flecha.setAlignment(Qt.AlignmentFlag.AlignCenter)
                flecha.setStyleSheet("font-size: 50px; color: #f6cd19; font-weight: bold; color: black")
                container_layout.addWidget(flecha)


        # Configurar el contenedor en el área de scroll
        container.setLayout(container_layout)
        self.scroll_area.setWidget(container)

        layout.addWidget(self.scroll_area)
        layout.addLayout(button_layout)

    def getLine(self, estacion):
        script = """
                        SELECT linea.nombre_linea
                        FROM estacion
                        INNER JOIN linea ON estacion.id_linea = linea.id_linea
                        WHERE estacion.nombre_estacion = ?;
                        """
        self.cursor.execute(script, (estacion,))
        res = self.cursor.fetchone()
        return res["nombre_linea"]
    def color_linea(self, estacion):
        return self.colores.get(self.getLine(estacion), "gray")
    def calcular (self, message : QLabel, origen, destino, combo1 :QComboBox, combo2:QComboBox):
        if origen == destino or self.hay_trans(origen, destino):
            message.clear()
            time.sleep(0.25)
            message.setText("Selecciona un origen distinto a tu destino")
        else:
            message.clear()
            busqueda = search.find_route(combo1.currentText(), combo2.currentText())
            self.estaciones = self.tratamiento_resultado(busqueda)
            combo1.setCurrentIndex(0)
            combo2.setCurrentIndex(0)
            self.setup_pagina_3()
            self.stacked_widget.setCurrentWidget(self.p_res)
    def volver(self, message :QLabel, combo1 :QComboBox, combo2:QComboBox):
        message.clear()
        combo1.setCurrentIndex(0)
        combo2.setCurrentIndex(0)
        self.stacked_widget.setCurrentWidget(self.ppal)
    def mapa (self, message, combo1 :QComboBox, combo2:QComboBox):
        message.clear()
        combo1.setCurrentIndex(0)
        combo2.setCurrentIndex(0)
        self.stacked_widget.setCurrentWidget(self.p_mapa)
    def tratamiento_resultado(self, path):
            resultado = []
            for i in range(len(path)):
                estacion_actual = path[i]

                # Obtenemos la linea de la estacion
                consulta_linea = """
                    SELECT linea.nombre_linea
                    FROM estacion
                    INNER JOIN linea ON estacion.id_linea = linea.id_linea
                    WHERE estacion.nombre_estacion = ?;
                    """
                self.cursor.execute(consulta_linea, (estacion_actual,))
                resultado_linea_actual = self.cursor.fetchone()

                if not resultado_linea_actual:
                    raise ValueError(f"No se encontró la estación '{estacion_actual}' en la base de datos.")

                linea_actual = resultado_linea_actual["nombre_linea"]

                # Comprobamos si hay transbordos y los añadimos
                transbordo_linea = None
                if i < len(path) - 1:
                    estacion_siguiente = path[i + 1]
                    transbordo = self.hay_trans(estacion_actual, estacion_siguiente)
                    if transbordo:
                        transbordo_linea = self.getLine(estacion_siguiente)

                resultado.append((estacion_actual, linea_actual, transbordo_linea))
            return resultado
    def hay_trans(self, origen, destino):
        # Comprobamos si existe transbordo entre dos estaciones
        consulta_transbordo = """
                SELECT 1
                FROM transbordo
                INNER JOIN estacion e1 ON transbordo.id_estacion1 = e1.id_estacion
                INNER JOIN estacion e2 ON transbordo.id_estacion2 = e2.id_estacion
                WHERE (e1.nombre_estacion = ? AND e2.nombre_estacion = ?)
                   OR (e1.nombre_estacion = ? AND e2.nombre_estacion = ?);
                """
        self.cursor.execute(consulta_transbordo, (origen, destino, destino, origen))
        transbordo = self.cursor.fetchone()

        if transbordo:
            return True
        else:
            return False


app = QApplication(sys.argv)
icon = QPixmap(ruta_absoluta("imagenes/Subte-logo.png"))
app.setWindowIcon(icon)
ventana_principal = VentanaPrincipal()
ventana_principal.showMaximized()
sys.exit(app.exec())
