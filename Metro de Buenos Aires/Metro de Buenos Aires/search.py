import controller
from queue import PriorityQueue
from geopy.distance import geodesic
import datetime


# Nos conectamos a la base de datos 
# Para poder obtener la informacion relevante a las estaciones, conexiones y trasbordos
def connectDB():
    return controller.createDB()

# Para calcular la heurística utilizamos la fórmula de distancia geodésica
def gformula(lat1, lon1, lat2, lon2):
    #Usamos kolkata y delhi, las cuales son variables de la libreria geopy
    kolkata = lat1, lon1
    delhi = lat2, lon2
    res = geodesic(kolkata,delhi).kilometers
    return res


# Cargar las estaciones, conexiones y transbordos de la Base de Datos SQL
def load_data(conn):
    #stations es un diccionario 
    # clave: id_estacion
    # valor: diccionario con: nombre, latitud y longitud de la estacion
    stations = {}
    # connections diccionario que representa el grafo entre estaciones
    # clave: id_estacion
    # valor: lista de tuplas con la estacion conectada y tiempo de viaje
    connections = {}
    cursor = conn.cursor()
    # Cargamos las estaciones de la base de datos, con su nombre y coordenadas
    cursor.execute("SELECT id_estacion, nombre_estacion, latitud, longitud FROM estacion") 
    # Guardamos los datos obtenidos en el diccionario stations
    for row in cursor.fetchall():
        station_id = row["id_estacion"]
        stations[station_id] = {
            "name": row["nombre_estacion"],
            "lat": row["latitud"],
            "lon": row["longitud"]
        }
    # Definimos el tiempo estimado que el metro espera en cada estacion
    tiempo_en_estacion = 30
    # Cargamos las conexiones entre estaciones y el tiempo en el que se tarde en ir de una a otra que se encuentra en la base de datos
    cursor.execute("SELECT id_estacion1, id_estacion2, tiempo FROM conexion")
    # Guardamos los datos obtenidos en el diccionario connections
    for row in cursor.fetchall():
        start, end, time = row["id_estacion1"], row["id_estacion2"], row["tiempo"]
        if start not in connections:
            connections[start] = []
        connections[start].append((end, time+tiempo_en_estacion))
        if end not in connections:
            connections[end] = []
        connections[end].append((start, time+tiempo_en_estacion))
    # Definimos el tiempo estimado que el metro espera en cada transbordo
    tiempo_en_transbordo = 20
    # Cargamos los transbordos y el tiempo que tarda en ir de uan estacion a otra que se encuentra en la base de datos
    cursor.execute("SELECT id_estacion1, id_estacion2, tiempo FROM transbordo")
    # Guardamos los datos obtenidos en el diccionario connections
    for row in cursor.fetchall():
        start, end, time = row["id_estacion1"], row["id_estacion2"], row["tiempo"]
        if start not in connections:
            connections[start] = []
        connections[start].append((end, time + hora_punta()*60+tiempo_en_transbordo))
        if end not in connections:
            connections[end] = []
        connections[end].append((start, time + hora_punta()*60+tiempo_en_transbordo))

    return stations, connections


# Implementacion del Algoritmo A*
def a_star_algorithm(origen, destino, stations, connections):
    open_set = PriorityQueue()
    open_set.put((0, origen))
    # camino: almacena las estaciones previas en el camino optimo
    camino = {}
    # g: g(n)
    g = {station: float("inf") for station in stations}
    g[origen] = 0
    #f: f(n)
    f = {station: float("inf") for station in stations}
    f[origen] = gformula(
        stations[origen]["lat"], stations[origen]["lon"], stations[destino]["lat"], stations[destino]["lon"]
    )
    # Itera hasta encontrar el destino o quedarse sin opciones
    while not open_set.empty():
        current = open_set.get()[1] 
        # Se ha llegado al destino, se devuelve la ruta reconstruida
        if current == destino:
            return reconstruct_path(camino, current)
        # Evalua las estaciones vecinas
        for next, h in connections.get(current, []):
            # f(n) = g(n) + h(n)
            coste = g[current] + h
            # Si el coste es menor que el registrado se actualiza, y se avanza
            if coste < g[next]:
                camino[next] = current
                g[next] = coste
                f[next] = coste + gformula(
                    stations[next]["lat"], stations[next]["lon"],
                    stations[destino]["lat"], stations[destino]["lon"]
                )
                open_set.put((f[next], next))
    # Ruta no encontrada
    return None 


# Reconstruir camino del Algoritmo A*
# Reconstruye el camino desde el destino hasta el origen
def reconstruct_path(camino, current):
    path = [current]
    while current in camino:
        current = camino[current]
        path.append(current)
    path.reverse()
    return path

# Funcion para determinar el tiempo medio de espera en los transbordos
# teniendo en cuenta el dia de la semana y la hora a la que se realiza la
# solicitud
def hora_punta():
    dias_diario = ['Monday', 'Tuesday','Wednesday','Thursday','Friday']
    # Obtener el valor numerico de la hora a la que se esta realizando la consulta
    hora_actual = int(datetime.datetime.now().strftime('%H'))
    # Idem con el dia de la semana
    dia_actual = datetime.date.today().strftime('%A')
    tiempo_transbordo = 0
    # Determinar si se trata de un dia de diario o no
    es_dia_diario = False
    for dia in dias_diario:
        if dia == dia_actual:
            es_dia_diario = True

    # El Subte cierra de 23:00 a 5:30 aprox, por lo que las peticiones en ese rango de hora
    # el sistema las interpreta como una peticion en la que no importa la hora, y da un tiempo 
    # medio de espera mayor al de la hora punta pero menor al de los tiempos laxos
    if (hora_actual <= 5 or hora_actual >= 23):
        return 3
    if(es_dia_diario):
        # Si se trata de la hora punta, el tiempo de espera en transbordo sera menor
        if ((hora_actual >= 7 and hora_actual <= 9) or (hora_actual >= 16 and hora_actual <= 20)):
            tiempo_transbordo = 1
        # Si no es hora punta, hay menor frecuencia de trenes, por lo que hay que esperar mas
        else:
            tiempo_transbordo = 4
    # En dias de fin de semana, hay menor frecuencia de trenes y los tiempos de espera suelen ser mayores
    else:
        tiempo_transbordo = 6
    
    return tiempo_transbordo


# Función para encontrar la ruta
def find_route(origen, destino):
    # Conecta con la base de datos y carga la informacion
    conn = connectDB()
    stations, connections = load_data(conn)
    # Busca el identificador de la estacion origen en el diccionario stations
    for id, data in stations.items():
        if data["name"] == origen:
            idorigen = id
            break  
    # Busca el identificador de la estacion destino en el diccionario stations
    for id, data in stations.items():
        if data["name"] == destino:
            iddestino = id
            break
    # Llamma al Algoritmo A* para calcular la ruta mas corta
    path = a_star_algorithm(idorigen, iddestino, stations, connections)
    # Caso en el que no se encuentre ninguna ruta para los datos dados
    if path is None:
        return "No se ha encontrado ninguna ruta."
    else:
        #------------------------------------IGNORAR
        tiempo_total = 0
        for i in range(0,len(path)-1):
            for connect in connections[path[i]]:
                if path[i+1] == connect[0]:
                    #print(connect[1])
                    tiempo_total += connect[1]
        
        #print(tiempo_total/60, "min")
        # ------------------------------------IGNORAR
        # Caso en el que se encuentre la ruta
        # Se traducen y se retorna el resultado
        route = [stations[station_id]["name"] for station_id in path]
        conn.close()
        return route


# Para probar se cambia la estación origen y destino
# if __name__ == "__main__":
#     print (find_route("Pasco", "Pichincha"))
