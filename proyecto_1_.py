def BubbleSort_objeto(
    arr, Atributo
):  # Bubble sort original de https://www.geeksforgeeks.org/dsa/bubble-sort-algorithm/, modificado para trabajar con atributos de objetos
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):
        swapped = False

        # Last i elements are already in place
        for l in range(0, n - i - 1):
            valor_l = sum(getattr(arr[l], Atributo))
            valor_l1 = sum(getattr(arr[l + 1], Atributo))
            if valor_l < valor_l1:
                arr[l], arr[l + 1] = arr[l + 1], arr[l]
                swapped = True
        if swapped == False:
            break


def BubbleSort_lista_aux(
    arr,
):  # Bubble sort original de https://www.geeksforgeeks.org/dsa/bubble-sort-algorithm/, modificado para trabajar con lista auxiliar
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):
        swapped = False

        # Last i elements are already in place
        for l in range(0, n - i - 1):
            lmas1 = l + 1
            if arr[l][2] < arr[lmas1][2]:
                arr[l], arr[lmas1] = arr[lmas1], arr[l]
                swapped = True
        if swapped == False:
            break


class Deportista:  # Clase abstracta principal
    def __init__(self, id, nombre, edad, deporte):
        self._id = id
        self._nombre = nombre
        self._edad = edad
        self._deporte = deporte
        self._puntaje = []
        self._cantidad_de_competencias = []
        self._registro = None

    def obtener_informacion_basica(self):
        return f"id: {self._id}\nnombre: {self._nombre}\nedad: {self._edad}\ndeporte: {self._deporte}\npuntaje: {self._puntaje}\ncantidad_de_competencias: {len(self._cantidad_de_competencias)}\n"

    def registrom(
        self, lista
    ):  # Este metodo ayuda poder actualizar los puntajes para actualizar la tabla de rankings apenas se modifique un registro por los metodos
        self._registro = lista

    def obtener_estadisticas(self):
        l = 0
        for i in self._puntaje:
            l = i + l
        return f"Cantidad_de_competencias: {len(self._cantidad_de_competencias)}\nPuntaje total: {l}\n"

    def reiniciar_puntaje(
        self,
    ):  # Este metodo ademas de borra las competencias y puntaje del deportista reajusta el ranking a consecuencia de lo anterior
        self._cantidad_de_competencias.clear()
        self._puntaje.clear()
        if len(self._registro._deportistas) > 1:
            BubbleSort_objeto(self._registro._deportistas, "_puntaje")
            if self._deporte == "Tenis":
                self._registro.ordenar_ranking_atp()

    def actualizar_puntaje_y_competencias(
        self, nuevo_puntaje, competencia
    ):  # Este metodo ademas de agregar a las competencias y al puntaje del deportista reajusta el ranking a consecuencia de lo anterior
        self._puntaje.append(nuevo_puntaje)
        self._cantidad_de_competencias.append(competencia)
        if self._registro != 0:
            BubbleSort_objeto(self._registro._deportistas, "_puntaje")
            if self._deporte == "Tenis":
                self._registro.ordenar_ranking_atp()

    def __str__(self):
        return f"id: {self._id}\nnombre: {self._nombre}\nedad: {self._edad}\ndeporte: {self._deporte}\npuntaje: {self._puntaje}\ncantidad_de_competencias: {len(self._cantidad_de_competencias)}\n"


class Registro:  # Clase registro, sirve para llevar un registro, y ademas la utilizo como la tabla de ranking
    def __init__(self):
        self._deportistas = []
        self._atp = []  # Lista hecha exclusivamente para el ranking de tenis

    def añadir_deportista(self, deportista):
        if deportista in self._deportistas:
            print(f"Ya fue ingresado el deportista {deportista._nombre}\n")
        else:
            self._deportistas.append(deportista)
            deportista.registrom(self)

    def mostrar_deportistas(self):
        BubbleSort_objeto(self._deportistas, "_puntaje")
        for i in self._deportistas:
            i.obtener_informacion_basica()
            print("\n")

    def mostrar_ranking_por_deporte(
        self, deporte
    ):  # Esta funcion calcula la cantidad de deportistas del deporte y lo almacena en el n, para asi poder llamar a la funcion que imprimira el ranking
        n = 0
        for i in self._deportistas:
            if i._deporte == deporte:
                n = n + 1
        self.mostrar_n_mejores_deportistas(deporte, n)

    def mostrar_n_mejores_deportistas(self, deporte, n):
        l = []
        for i in self._deportistas:
            if i._deporte == deporte:
                l.append(i)
        for m in range(n):
            l[m].obtener_informacion_basica()

    def ordenar_ranking_atp(
        self,
    ):  # Metodo hecho exclusivamente para ordenar el ranking de tenis
        self._atp = []
        jugador = []
        for i in self._deportistas:
            if i._deporte == "Tenis":
                jugador = [i._id, i._nombre, i._ranking_atp]
                self._atp.append(jugador)
        BubbleSort_lista_aux(self._atp)

    def mostrar_ranking_atp(
        self,
    ):  # Metodo hecho exclusivamente para mostrar el ranking de tenis
        for i in range(len(self._atp)):
            print(f"Nombre: {self._atp[i][1]}, ranking: {self._atp[i][2]}")
        print("\n")

    def buscar_deportista(self, nombre):
        for i in self._deportistas:
            if i._nombre == nombre:
                print(i)
                print(f"Deprotista encontrado:\n\n{i.obtener_informacion_basica()}")
                return
        print(f"El deportistas {nombre} no esta ingresado\n")

    def __str__(self):
        return f"Deportistas: {self._deportistas}\n"


class Competencia:  # Esta funcion almacena detalles del evento
    def __init__(self, id, nombre, fecha, deporte, registro):
        self._id = id
        self._nombre = nombre
        self.__fecha = fecha
        self.__participantes = []
        self.__resultados = {}
        self._deporte = deporte
        self.__registro = registro

    def inscribir_participante(self, deportista):
        for d in self.__registro._deportistas:
            if d._nombre == deportista._nombre:
                if d._deporte == deportista._deporte:
                    self.__participantes.append(deportista)
                    return
        print("El deportista no esta en el registro")

    def registrar_resultado(
        self, resultado
    ):  # En la primera parte de la funcion se verifica que no allan datos negativos y que el deportista ingresado este con el mismo id y nombre en el registro
        for i in resultado.values():
            if i["_puntaje"] < 0:
                print(
                    f"Deportista {i['nombre']} tiene datos negativos, no se ingresara nada"
                )
                return
            m = 0
            for l in self.__registro._deportistas:
                if i["nombre"] == l._nombre and i["id"] == l._id:
                    m = m + 1
            if m == 0:
                print(
                    f"Deportista {i['nombre']} o tiene un id erroneo, no se registrara nada"
                )
                return

        for i in resultado.values():  # En la segunda parte de esta funcion se actualizan los puntajes, y se almacena el diccionario de resultados
            for l in self.__registro._deportistas:
                if i["nombre"] == l._nombre and i["id"] == l._id:
                    l.actualizar_puntaje_y_competencias(i["_puntaje"], self)

        self.__resultados = resultado

    def mostrar_resultado(self):
        print(f"Resultados competencia: {self._nombre}\n")
        for i in self.__resultados.values():
            print(f"Nombre: {i['nombre']}, Puntaje: {i['_puntaje']}")

    def mostrar_n_posiciones(
        self, n
    ):  # En esta funcion en su primera parte hace una lista sencilla  y se ordena
        lista = []
        jugador = []
        for i in self.__resultados.values():
            jugador = [i["id"], i["nombre"], i["_puntaje"]]
            lista.append(jugador)
        BubbleSort_lista_aux(lista)
        print(
            f"Mejores {n} deportistas de la competencia {self._nombre}:\n"
        )  # En esta segunda parte se imprime la lista
        for i in range(n):
            print(f"Nombre: {lista[i][1]}, puntaje: {lista[i][2]}")

    def __str__(self):
        return f"Competencia\nid: {self._id}\nNombre: {self._nombre}\nFecha: {self.__fecha}\nParticipantes: {self.__participantes}\nResultados: {self.__resultados}\nDeporte: {self._deporte}\nRegistro: {self.registro}"


class Futbolista(Deportista):  # Esta funcion hereda de la Funcion Deportista
    def __init__(self, id, nombre, edad, equipo, posicion):
        super().__init__(id=id, nombre=nombre, edad=edad, deporte="Futbol")
        self.__equipo = equipo
        self.__goles = 0
        self.__asistencias = 0
        self.__posicion = posicion

    def añadir_goles(self, goles):
        if goles < 1:
            print("Porfavor ingrese un numero positivo de goles o mayor a cero")
            return
        else:
            self.__goles = self.__goles + goles
            print(f"Se agregaron {goles} goles")

    def añadir_asistencias(self, asistencias):
        if asistencias < 1:
            print("Porfavor ingrese un numero positivo de asistencias o mayor a cero")
            return
        else:
            self.__asistencias = self.__asistencias + asistencias
            print(f"Se agregaron {asistencias} asistencias")

    def calcular_rendimiento(self):
        print(
            f"El redimiento del jugador: {self._nombre}, es: {(self.__goles * 2 + self.__asistencias * 0.7) / len(self.cantidad_de_competencias)}"
        )

    def cambiar_de_equipo(
        self, nuevo_equipo
    ):  # En esta funcion se reinicia el puntaje y competencias del deportista y se le cambia de equipo
        super().reiniciar_puntaje()
        self.__equipo = nuevo_equipo
        print(f"El jugador {self._nombre} se cambio al equipo: {self.__equipo}")

    def obtener_informacion_basica(self):
        print(
            f"{super().obtener_informacion_basica()}equipo: {self.__equipo}\ngoles: {self.__goles}\nasistencias: {self.__asistencias}\nposicion: {self.__posicion}\n"
        )

    def __str__(self):
        return "Utilize el metodo obtener_informacion_basica para ver la informacion del deportista\n"


class Tenista(Deportista):  # Esta funcion hereda de la Funcion Deportista
    def __init__(self, id, nombre, edad, pareja, ranking_atp):
        super().__init__(id=id, nombre=nombre, edad=edad, deporte="Tenis")
        self.__pareja = pareja
        self._ranking_atp = ranking_atp

    def actualizar_ranking(self, nueva_posicion):
        if nueva_posicion < 1:
            print("Porfavor ingrese una posicion positiva o mayor a cero\n")
            return
        else:
            self._ranking_atp = nueva_posicion
            self._registro.ordenar_ranking_atp()
            print(
                f"Se ingreso la nueva posicion {nueva_posicion} y se actualizo el ranking atp\n"
            )

    def actualizar_de_pareja(
        self, nueva_pareja
    ):  # En esta funcion se reinicia el puntaje y competencias del deportista y se le cambia la pareja
        super().reiniciar_puntaje()
        self.__pareja = nueva_pareja
        print(f"Se cambio la pareja {nueva_pareja}\n")

    def obtener_informacion_basica(self):
        print(
            f"{super().obtener_informacion_basica()}pareja: {self.__pareja}\nranking_atp: {self._ranking_atp}\n"
        )

    def __str__(self):
        return "Utilize el metodo obtener_informacion_basica para ver la informacion del deportista\n"


class Atleta(Deportista):  # Esta funcion hereda de la Funcion Deportista
    def __init__(self, id, nombre, edad, disciplina):
        super().__init__(id=id, nombre=nombre, edad=edad, deporte="Atletismo")
        self.__disciplina = disciplina
        self.mejores_tiempos = []

    def agregar_mejores_tiempos(self, tiempo):
        if tiempo < 0.01:
            print("Porfavor ingrese un tiempo realista\n")
            return
        else:
            self.mejores_tiempos.append(tiempo)
            print(f"Se ingreso un tiempo de {tiempo}\n")

    def obtener_informacion_basica(self):
        print(
            f"{super().obtener_informacion_basica()}disiplina: {self.__disciplina}\nmejores tiempos: {self.mejores_tiempos}\n"
        )

    def __str__(self):
        return "Utilize el metodo obtener_informacion_basica para ver la informacion del deportista\n"


# declaracion deportistas

# primero 22 futbolistas 11 por equipo

futobolista_1 = Futbolista(
    id=1, nombre="Alejandro", edad="22", equipo="Los_castores", posicion="Portero"
)
futobolista_2 = Futbolista(
    id=2, nombre="Juan", edad="23", equipo="Los_castores", posicion="Linea de defensa"
)
futobolista_3 = Futbolista(
    id=3, nombre="Pepe", edad="20", equipo="Los_castores", posicion="Linea de defensa"
)
futobolista_4 = Futbolista(
    id=4, nombre="Pedro", edad="30", equipo="Los_castores", posicion="Linea de defensa"
)
futobolista_5 = Futbolista(
    id=5, nombre="Peter", edad="32", equipo="Los_castores", posicion="Linea de defensa"
)
futobolista_6 = Futbolista(
    id=6, nombre="Pablo", edad="30", equipo="Los_castores", posicion="Medio centro"
)
futobolista_7 = Futbolista(
    id=7, nombre="Jose", edad="40", equipo="Los_castores", posicion="Medio centro"
)
futobolista_8 = Futbolista(
    id=8, nombre="Carlos", edad="60", equipo="Los_castores", posicion="Medio centro"
)
futobolista_9 = Futbolista(
    id=9, nombre="Raul", edad="45", equipo="Los_castores", posicion="Delantero"
)
futobolista_10 = Futbolista(
    id=10, nombre="Leonel", edad="40", equipo="Los_castores", posicion="Delantero"
)
futobolista_11 = Futbolista(
    id=11, nombre="Cristiano", edad="40", equipo="Los_castores", posicion="Delantero"
)
futobolista_12 = Futbolista(
    id=12, nombre="Jhon", edad="28", equipo="Los_anti_castores", posicion="Portero"
)
futobolista_13 = Futbolista(
    id=13,
    nombre="Mike",
    edad="35",
    equipo="Los_anti_castores",
    posicion="Linea de defensa",
)
futobolista_14 = Futbolista(
    id=14,
    nombre="James",
    edad="40",
    equipo="Los_anti_castores",
    posicion="Linea de defensa",
)
futobolista_15 = Futbolista(
    id=15,
    nombre="Sawao",
    edad="40",
    equipo="Los_anti_castores",
    posicion="Linea de defensa",
)
futobolista_16 = Futbolista(
    id=16,
    nombre="Luffy",
    edad="20",
    equipo="Los_anti_castores",
    posicion="Linea de defensa",
)
futobolista_17 = Futbolista(
    id=17, nombre="Zoro", edad="24", equipo="Los_anti_castores", posicion="Medio centro"
)
futobolista_18 = Futbolista(
    id=18,
    nombre="Bartolomeo",
    edad="56",
    equipo="Los_anti_castores",
    posicion="Medio centro",
)
futobolista_19 = Futbolista(
    id=19,
    nombre="Antonio",
    edad="20",
    equipo="Los_anti_castores",
    posicion="Medio centro",
)
futobolista_20 = Futbolista(
    id=20,
    nombre="Fernando",
    edad="20",
    equipo="Los_anti_castores",
    posicion="Delantero",
)
futobolista_21 = Futbolista(
    id=21, nombre="Julian", edad="30", equipo="Los_anti_castores", posicion="Delantero"
)
futobolista_22 = Futbolista(
    id=22,
    nombre="Cleveland",
    edad="30",
    equipo="Los_anti_castores",
    posicion="Delantero",
)

# 5 tenistas 8 parejas de las ATP Finals

tenista_1 = Tenista(
    id=23, nombre="Cleveland_Jr", edad="18", pareja="Quacmire", ranking_atp=1
)
tenista_2 = Tenista(
    id=24, nombre="Quacmire", edad="30", pareja="Cleveland Jr", ranking_atp=3
)
tenista_3 = Tenista(id=25, nombre="Joe", edad="30", pareja="Stewie", ranking_atp=5)
tenista_4 = Tenista(id=26, nombre="Stewie", edad="18", pareja="Joe", ranking_atp=6)
tenista_5 = Tenista(id=27, nombre="Brian", edad="40", pareja="Chris", ranking_atp=4)
tenista_6 = Tenista(id=27, nombre="Chris", edad="40", pareja="Brian", ranking_atp=2)

# 5 atetlas de carrera 100 metros planos

atleta_1 = Atleta(id=39, nombre="Peach", edad="30", disciplina="100 metros planos")
atleta_2 = Atleta(id=40, nombre="Bowser", edad="30", disciplina="100 metros planos")
atleta_3 = Atleta(id=41, nombre="Bowser jr", edad="18", disciplina="100 metros planos")
atleta_4 = Atleta(id=42, nombre="Giorno", edad="18", disciplina="100 metros planos")
atleta_5 = Atleta(id=43, nombre="German", edad="30", disciplina="100 metros planos")


# registro de registro

# registro futbol

lista_futbol = Registro()
lista_futbol.añadir_deportista(futobolista_1)
lista_futbol.añadir_deportista(futobolista_2)
lista_futbol.añadir_deportista(futobolista_3)
lista_futbol.añadir_deportista(futobolista_4)
lista_futbol.añadir_deportista(futobolista_5)
lista_futbol.añadir_deportista(futobolista_6)
lista_futbol.añadir_deportista(futobolista_7)
lista_futbol.añadir_deportista(futobolista_8)
lista_futbol.añadir_deportista(futobolista_9)
lista_futbol.añadir_deportista(futobolista_10)
lista_futbol.añadir_deportista(futobolista_11)
lista_futbol.añadir_deportista(futobolista_12)
lista_futbol.añadir_deportista(futobolista_13)
lista_futbol.añadir_deportista(futobolista_14)
lista_futbol.añadir_deportista(futobolista_15)
lista_futbol.añadir_deportista(futobolista_16)
lista_futbol.añadir_deportista(futobolista_17)
lista_futbol.añadir_deportista(futobolista_18)
lista_futbol.añadir_deportista(futobolista_19)
lista_futbol.añadir_deportista(futobolista_20)
lista_futbol.añadir_deportista(futobolista_21)
lista_futbol.añadir_deportista(futobolista_22)

# registro tenis atletismo

lista_de_deportes_varios = Registro()
lista_de_deportes_varios.añadir_deportista(tenista_1)
lista_de_deportes_varios.añadir_deportista(tenista_2)
lista_de_deportes_varios.añadir_deportista(tenista_3)
lista_de_deportes_varios.añadir_deportista(tenista_4)
lista_de_deportes_varios.añadir_deportista(tenista_5)
lista_de_deportes_varios.añadir_deportista(tenista_6)
lista_de_deportes_varios.añadir_deportista(atleta_1)
lista_de_deportes_varios.añadir_deportista(atleta_2)
lista_de_deportes_varios.añadir_deportista(atleta_3)
lista_de_deportes_varios.añadir_deportista(atleta_4)
lista_de_deportes_varios.añadir_deportista(atleta_5)

# declarar competencia

competencia_futbol = Competencia(
    id=1,
    nombre="Final mundial 2020",
    fecha=10 / 7 / 2020,
    deporte="Futbol",
    registro=lista_futbol,
)
comparacion_atletismo_tenis = Competencia(
    id=2,
    nombre="Comaparacion atletismo tenis 2020",
    fecha=5 / 3 / 2020,
    deporte="Tenis",
    registro=lista_de_deportes_varios,
)

# inscribir participante

# inscripcion futbol

competencia_futbol.inscribir_participante(futobolista_1)
competencia_futbol.inscribir_participante(futobolista_2)
competencia_futbol.inscribir_participante(futobolista_3)
competencia_futbol.inscribir_participante(futobolista_4)
competencia_futbol.inscribir_participante(futobolista_5)
competencia_futbol.inscribir_participante(futobolista_6)
competencia_futbol.inscribir_participante(futobolista_7)
competencia_futbol.inscribir_participante(futobolista_8)
competencia_futbol.inscribir_participante(futobolista_9)
competencia_futbol.inscribir_participante(futobolista_10)
competencia_futbol.inscribir_participante(futobolista_11)
competencia_futbol.inscribir_participante(futobolista_12)
competencia_futbol.inscribir_participante(futobolista_13)
competencia_futbol.inscribir_participante(futobolista_14)
competencia_futbol.inscribir_participante(futobolista_15)
competencia_futbol.inscribir_participante(futobolista_16)
competencia_futbol.inscribir_participante(futobolista_17)
competencia_futbol.inscribir_participante(futobolista_18)
competencia_futbol.inscribir_participante(futobolista_19)
competencia_futbol.inscribir_participante(futobolista_20)
competencia_futbol.inscribir_participante(futobolista_21)
competencia_futbol.inscribir_participante(futobolista_22)

# registro tenis atletismo

comparacion_atletismo_tenis.inscribir_participante(tenista_1)
comparacion_atletismo_tenis.inscribir_participante(tenista_2)
comparacion_atletismo_tenis.inscribir_participante(tenista_3)
comparacion_atletismo_tenis.inscribir_participante(tenista_4)
comparacion_atletismo_tenis.inscribir_participante(tenista_5)
comparacion_atletismo_tenis.inscribir_participante(atleta_1)
comparacion_atletismo_tenis.inscribir_participante(atleta_2)
comparacion_atletismo_tenis.inscribir_participante(atleta_3)
comparacion_atletismo_tenis.inscribir_participante(atleta_4)

# resultados

# resultados futbol

resultado_futbol = {
    "futbolista_1": {"id": 1, "nombre": "Alejandro", "_puntaje": 1011},
    "futbolista_2": {"id": 2, "nombre": "Juan", "_puntaje": 1220},
    "futbolista_3": {"id": 3, "nombre": "Pepe", "_puntaje": 1320},
    "futbolista_4": {"id": 4, "nombre": "Pedro", "_puntaje": 4120},
    "futbolista_5": {"id": 5, "nombre": "Peter", "_puntaje": 1205},
    "futbolista_6": {"id": 6, "nombre": "Pablo", "_puntaje": 1250},
    "futbolista_7": {"id": 7, "nombre": "Jose", "_puntaje": 1620},
    "futbolista_8": {"id": 8, "nombre": "Carlos", "_puntaje": 7120},
    "futbolista_9": {"id": 9, "nombre": "Raul", "_puntaje": 1208},
    "futbolista_10": {"id": 10, "nombre": "Leonel", "_puntaje": 1290},
    "futbolista_11": {"id": 11, "nombre": "Cristiano", "_puntaje": 11020},
    "futbolista_12": {"id": 12, "nombre": "Jhon", "_puntaje": 11120},
    "futbolista_13": {"id": 13, "nombre": "Mike", "_puntaje": 12012},
    "futbolista_14": {"id": 14, "nombre": "James", "_puntaje": 12130},
    "futbolista_15": {"id": 15, "nombre": "Sawao", "_puntaje": 11420},
    "futbolista_16": {"id": 16, "nombre": "Luffy", "_puntaje": 15120},
    "futbolista_17": {"id": 17, "nombre": "Zoro", "_puntaje": 12016},
    "futbolista_18": {"id": 18, "nombre": "Bartolomeo", "_puntaje": 12170},
    "futbolista_19": {"id": 19, "nombre": "Antonio", "_puntaje": 11820},
    "futbolista_20": {"id": 20, "nombre": "Fernando", "_puntaje": 19120},
    "futbolista_21": {"id": 21, "nombre": "Julian", "_puntaje": 12020},
    "futbolista_22": {"id": 22, "nombre": "Cleveland", "_puntaje": 12210},
}

# resultados tenis atletismo

resultado_tenis_atletimso = {
    "tenista_1": {"id": 23, "nombre": "Cleveland_Jr", "_puntaje": 10111},
    "tenista_2": {"id": 24, "nombre": "Quacmire", "_puntaje": 10121},
    "tenista_3": {"id": 25, "nombre": "Joe", "_puntaje": 10311},
    "tenista_4": {"id": 26, "nombre": "Stewie", "_puntaje": 14011},
    "tenista_5": {"id": 27, "nombre": "Brian", "_puntaje": 51011},
    "atleta_1": {"id": 39, "nombre": "Peach", "_puntaje": 11116},
    "atleta_2": {"id": 40, "nombre": "Bowser", "_puntaje": 11126},
    "atleta_3": {"id": 41, "nombre": "Bowser jr", "_puntaje": 13016},
    "atleta_4": {"id": 42, "nombre": "Giorno", "_puntaje": 10164},
    "atleta_5": {"id": 43, "nombre": "German", "_puntaje": 51011},
}

# registro los resultados

competencia_futbol.registrar_resultado(resultado_futbol)
comparacion_atletismo_tenis.registrar_resultado(resultado_tenis_atletimso)

# una vez con todo escrito procedo a probar los otros metodos

# primero pruebo metodos de la clase registro
print("\n\nAhora pruebo los metodos de registro que faltan probar\n")
print("Inicio con anadir deportista que como ya esta ingresado deberia fallar\n")
lista_futbol.añadir_deportista(futobolista_1)

print("Continuo con mostrar deportistas\n")

lista_futbol.mostrar_deportistas()

print("Continuo con mostrar ranking por deporte en este caso 'tenis'\n")

lista_de_deportes_varios.mostrar_ranking_por_deporte("Tenis")

print("Continuo con mostrar n mejores deportistas en este caso 'atletismo'\n")

lista_de_deportes_varios.mostrar_n_mejores_deportistas("Atletismo", 3)

print(
    "Continuo con buscar deportista, primero un deportista existente luego uno inexistente\n"
)

lista_futbol.buscar_deportista("peter")

print("\n")

lista_futbol.buscar_deportista("peter2")

print("\n")

print("Continuo con la lista de ranking de tenistas\n")

lista_de_deportes_varios.mostrar_ranking_atp()

print("\n")

# ahora pruebo metodos de la clase competencia

print("Ahora pruebo los metodos de competencia que faltan probar\n")
print("Inicio con mostrar resultados\n")

competencia_futbol.mostrar_resultado()

print("\n")
print("Continuo con mostrar n posiciones\n")

comparacion_atletismo_tenis.mostrar_n_posiciones(7)

print("\n")

# ahora pruebo metodos de la clase abstracta deportista atravez de la clase futbolista
print(
    "Ahora pruebo el metodo que falta probar de la clase abstracta deportista atravez de la clase futbolista\n"
)
print("Inicio con obtener estadistica\n")

print(futobolista_1.obtener_estadisticas())

print("\n")

# ahora pruebo metodos de la clase futbolista
print("Ahora pruebo los metodos que faltan probar de la clase futbolista\n")
print(
    "Inicio con anadir goles, primero un ejemplo correcto, luego un ejemplo erroneo\n"
)

futobolista_1.añadir_goles(3)

print("\n")

futobolista_1.añadir_goles(-3)

print("\n")
print(
    "Continuo con anadir asistencias, primero un ejemplo correcto, luego un ejemplo erroneo\n"
)

futobolista_1.añadir_asistencias(3)

print("\n")

futobolista_1.añadir_asistencias(-3)

print("\n")
print("Continuo con cambio de equipo\n")

futobolista_1.cambiar_de_equipo("los_anti_castores")

print("\n")
print("Continuo con obtener informacion basica\n")

futobolista_1.obtener_informacion_basica()

print("\n")

# ahora pruebo metodos de la clase tenista
print("Ahora pruebo los metodos que faltan probar de la clase tenista\n")
print(
    "Inicio con actualizar ranking, primero un ejemplo correcto, luego un ejemplo erroneo\n"
)

tenista_1.actualizar_ranking(10)

print("\n")

tenista_1.actualizar_ranking(-10)

print("\n")
print("Continuo con actualizar de pareja\n")

tenista_1.actualizar_de_pareja("joe")

print("\n")
print("Continuo con obtener informacion basica\n")

tenista_1.obtener_informacion_basica()

print("\n")

# ahora pruebo metodos de la clase atleta
print("Ahora pruebo los metodos que faltan probar de la clase atleta\n")
print(
    "Inicio con agregar mejores tiempos, primero un ejemplo correcto, luego un ejemplo erroneo\n"
)

atleta_1.agregar_mejores_tiempos(0.22)

print("\n")

atleta_1.agregar_mejores_tiempos(-0.22)

print("\n")
print("Continuo con obtener informacion basica\n")

atleta_1.obtener_informacion_basica()

print("\n")

print("Esos serian todos los metodos faltantes de probar")
