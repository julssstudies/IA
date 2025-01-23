import sqlite3 as sql

script = '''
DROP TABLE IF EXISTS conexion;
DROP TABLE IF EXISTS transbordo;
DROP TABLE IF EXISTS estacion;
DROP TABLE IF EXISTS linea;

CREATE TABLE linea (
    id_linea INT,
    nombre_linea CHAR(1),
    PRIMARY KEY (id_linea)
);

CREATE TABLE estacion (
    id_estacion INT,
    nombre_estacion VARCHAR(100),
    latitud DOUBLE,
    longitud DOUBLE,
    transbordo INT,
    id_linea INT,
    PRIMARY KEY (id_estacion),
    FOREIGN KEY (id_linea) REFERENCES linea (id_linea)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE transbordo (
    id_estacion1 INT,
    id_estacion2 INT,
    lineas CHAR(2),
    distancia DOUBLE,
    velocidad DOUBLE,
    tiempo DOUBLE,
    PRIMARY KEY (id_estacion1, id_estacion2),
    FOREIGN KEY (id_estacion1) REFERENCES estacion (id_estacion)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_estacion2) REFERENCES estacion (id_estacion)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE conexion (
    id_estacion1 INT,
    id_estacion2 INT,
    -- id_direccion INT,
    -- 0 es Oeste a Este, Sur a Norte
    -- 1 es Este a Oeste, Norte a Sur
    distancia DOUBLE,
    curvatura INT,
    velocidad INT,
    tiempo DOUBLE,
    PRIMARY KEY (id_estacion1, id_estacion2/*,id_direccion*/),
    FOREIGN KEY (id_estacion1) REFERENCES estacion (id_estacion)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_estacion2) REFERENCES estacion (id_estacion)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Lineas
INSERT INTO linea(id_linea,nombre_linea) VALUES (1,"A");
INSERT INTO linea(id_linea,nombre_linea) VALUES (2,"B");
INSERT INTO linea(id_linea,nombre_linea) VALUES (3,"C");
INSERT INTO linea(id_linea,nombre_linea) VALUES (4,"D");
INSERT INTO linea(id_linea,nombre_linea) VALUES (5,"E");

-- Las estaciones estan ordenadas en orden alfabetico de linea y en orden geografico (NORTE - SUR verticales, OESTE - ESTE horizontales)
-- Estaciones Linea A
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (1,"Alberti",-34.6098605,-58.4007125,0,1);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (2,"Pasco",-34.6096669,-58.398378,0,1);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (3,"Congreso",-34.6092078,-58.3925665,0,1);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (4,"Sáenz Peña",-34.6093868,-58.3867496,0,1);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (5,"Lima",-34.6091121,-58.3827226,1,1);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (6,"Piedras",-34.6088236,-58.3785247,0,1);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (7,"Perú",-34.6085662,-58.3745075,1,1);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (8,"Plaza de Mayo - Casa Rosada",-34.6088931,-58.3709023,0,1);

-- Estaciones linea B
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (9,"Pasteur AMIA",-34.6046381,-58.3994751,0,2);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (10,"Callao",-34.6044648,-58.392748,0,2);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (11,"Uruguay",-34.6040622,-58.3870794,0,2);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (12,"Carlos Pellegrini",-34.6037478,-58.3812659,1,2);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (13,"Florida",-34.6033847,-58.3745602,0,2);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (14,"Leandro N. Alem",-34.6029364,-58.3693763,0,2);

-- Estaciones Linea C
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (15,"Retiro",-34.5913724,-58.3742199,0,3);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (16,"General San Martín",-34.5950166,-58.3779067,0,3);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (17,"Esmeralda y Lavalle",-34.6017398,-58.3781287,0,3);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (18,"Diagonal Norte",-34.6047638,-58.3793047,1,3);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (19,"Avenida de Mayo",-34.6090453,-58.3806717,1,3);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (20,"Moreno",-34.6124404,-58.3805521,0,3);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (21,"Independencia",-34.6180921,-58.3801521,1,3);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (22,"San Juan",-34.6225018,-58.3799266,0,3);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (23,"Constitución",-34.6277051,-58.3811232,0,3);

-- Estaciones Linea D
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (24,"Facultad de Medicina",-34.5997341,-58.3977423,0,4);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (25,"Callao - Raquel Liberman",-34.5996542,-58.3926737,0,4);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (26,"Tribunales - Teatro Colón",-34.6018429,-58.3848681,0,4);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (27,"9 de Julio",-34.6044437,-58.3802989,1,4);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (28,"Catedral",-34.6077055,-58.3740029,0,4);

-- Estaciones Linea E
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (29,"Bolívar",-34.6097009,-58.3741388,1,5);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (30,"Belgrano",-34.6130289,-58.377724,0,5);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (31,"Independencia - Santa Mama Antula",-34.6181114,-58.3814855,1,5);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (32,"San José",-34.6224189,-58.3852133,0,5);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (33,"Entre Ríos - Rodolfo Walsh",-34.6227286,-58.3914512,0,5);
INSERT INTO estacion(id_estacion,nombre_estacion,latitud,longitud,transbordo,id_linea) VALUES (34,"Pichincha",-34.6232012,-58.397575,0,5);

-- transbordos 
-- Lima (A) <-> Avenida de Mayo (C)
INSERT INTO transbordo(id_estacion1,id_estacion2,lineas,distancia,velocidad,tiempo) VALUES (5,19,'AC',140.016,3.5,144.016);
-- Independencia (C) <-> Independencia - Santa Mama Antula (E)
INSERT INTO transbordo(id_estacion1,id_estacion2,lineas,distancia,velocidad,tiempo) VALUES (21,31,'CE',121.759,3.5,125.238);
-- Perú (A) <-> Catedral (D)
INSERT INTO transbordo(id_estacion1,id_estacion2,lineas,distancia,velocidad,tiempo) VALUES (7,28,'AD',135.278,3.5,139.143);
-- Perú (A) <-> Bolívar(E)
INSERT INTO transbordo(id_estacion1,id_estacion2,lineas,distancia,velocidad,tiempo) VALUES (7,29,'AE',121.048,3.5,124.507);
-- Catedral (D) <-> Bolívar (E)
INSERT INTO transbordo(id_estacion1,id_estacion2,lineas,distancia,velocidad,tiempo) VALUES (28,29,'DE',214.826,3.5,220.964);
-- Carlos Pellegrini (B) <-> Diagonal Norte (C)
INSERT INTO transbordo(id_estacion1,id_estacion2,lineas,distancia,velocidad,tiempo) VALUES (12,18,'BC',206.010,3.5,211.896);
-- Carlos Pellegrini (B) <-> 9 de Julio (D)
INSERT INTO transbordo(id_estacion1,id_estacion2,lineas,distancia,velocidad,tiempo) VALUES (12,27,'BD',57.826,3.5,59.478);
-- Diagonal Norte(C) <-> 9 de Julio (D)
INSERT INTO transbordo(id_estacion1, id_estacion2,lineas,distancia,velocidad,tiempo) VALUES (18,27,'CD',79.492,3.5,81.763);

-- distancias entre estaciones
-- linea A
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (1,2,214.615,1,22,35.119);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (2,3,548.669,0,48,41.15);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (3,4,543.376,2,35,55.89);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (4,5,370.507,0,38,35.101);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (5,6,386.0425,0,38,36.572);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (6,7,369.222,0,38,34.979);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (7,8,334.434,2,25,48.158);

-- linea B
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (9,10,611.327,1,42,52.399);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (10,11,521.073,1,42,44.663);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (11,12,534.526,0,48,40.089);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (12,13,615.547,0,48,46.166);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (13,14,478.046,1,32,53.78);

-- linea C
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (15,16,528.294,1,42,45.282);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (16,17,761.385,2,35,78.314);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (17,18,421.794,3,22,69.021);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (18,19,572.617,3,32,64.419);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (19,20,378.113,1,32,42.538);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (20,21,630.158,0,48,47.262);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (21,22,491.938,0,38,46.605);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (22,23,603.185,2,35,62.042);

-- linea D
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (24,25,464.647,0,38,44.019);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (25,26,787.515,2,35,81.002);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (26,27,510.028,1,42,43.717);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (27,28,681.908,0,48,51.143);

-- linea E
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (29,30,563.531,1,42,48.303);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (30,31,573.631,2,35,59.002);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (31,32,722.346,3,32,81.264);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (32,33,667.277,0,48,50.046);
INSERT INTO conexion(id_estacion1,id_estacion2,distancia,curvatura,velocidad,tiempo) VALUES (33,34,495.04,1,32,55.692);
'''
# Función para crear la Base de Datos
def createDB():
    conn = sql.connect('subte.db')
    cursor = conn.cursor()
    cursor.executescript(script)
    conn.row_factory = sql.Row
    return conn