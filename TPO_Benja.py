import random
def ValidarVendedor(Vendedor):
    return len(str(Vendedor)) == 6

def VerificarFecha(DD, MM, AA):
    if AA > 0:
        if MM >= 1 and MM <= 12:
            if MM == 4 or MM == 6 or MM == 9 or MM == 11:
                if DD >= 1 and DD <= 30:
                    return True
                else:
                    return False
            elif MM == 2:
                if AA % 4 == 0 and (AA % 100 != 0 or AA % 400 == 0):
                    if DD >= 1 and DD <= 29:
                        return True
                    else:
                        return False
                elif DD >= 1 and DD <= 28:
                    return True
                else:
                    return False
            else:
                if DD >= 1 and DD <= 31:
                    return True
                else:
                    return False
        else:
            return False
    else:
        return False

def CargarProductos():
    Productos = {
        "Televisor": 500,
        "Lavadora": 400,
        "Heladera": 600,
        "Microondas": 200,
        "Tostadora": 100,
        "Secadora":350,
        "Horno":400,
        "Cafetera":250,
        "Pymer":50
    } #Diccionario con los productos:precios 
    try:
        ArcProductos = open("Productos.txt", "w") #Abro el archivo Productos.txt, en modo escritura, si no existe el archivo lo crea, si existe lo sobreescribe
        LProductos = ";".join(Productos.keys()) + "\n" #Agarro los productos y los meto en una lista separados por ;
        Precios = ";".join(str(Productos[producto]) for producto in Productos.keys()) + "\n" #Agarro los precios y los meto en una lista separado por ;
        ArcProductos.write(LProductos) #Escribo en el archivo los productos
        ArcProductos.write(Precios) #Escribo en el archivo los precios
        print("Datos de productos guardados correctamente en el archivo 'Productos.txt'.") #Mensaje validando que el archivo fue creado exitosamente
        return Productos #Devuelvo el diccionario de productos, asi puede ser usado en la creacion de matriz
    except OSError: #En caso de error de sistema.
        print("Error al procesar el archivo.")

def LeerProductos():
    DictProductos = {}
    try:
        ArcProductos =  open("Productos.txt", "r")
        Productos = ArcProductos.readline().strip().split(";")
        Precios = ArcProductos.readline().strip().split(";")
        for i in range(len(Productos)):
            DictProductos[Productos[i]] = int(Precios[i])
        return DictProductos
    except FileNotFoundError:
        print("No se pudo encontrar el archivo 'Productos.txt'.")
        return None

def CrearMatriz(Vendedores):
    try:
        Productos = LeerProductos()
        if Productos:
            Matriz = [[0] * Vendedores for i in range(5)] #Creo una matriz por metodo de compresion, de columnas dinamicas y 5 filas.
            LVendedores = set()  #Conjuntos donde guardo los vendedores, para que no puedan ingresarse vendedores repetidos


            for c in range(Vendedores): #Para cada vendedor dentro del rango de vendedores(Cantidad de vendedores)
                Intentos = 3  #Intentos correctos para ingresar el codigo de vendedor
                while Intentos > 0:#Mientras que los intentos sean mayor a 0
                    CodVendedor = input("Ingrese el código del vendedor {} (6 dígitos): ".format(c + 1)) #Pido el codigo de vendedor, el c+1 actua como contador asi pregutna por vend: 1,2,etc
                    if ValidarVendedor(CodVendedor) and CodVendedor not in LVendedores:  #Si el codigo de vendedor no posee 6 digitos y no esta dentro del conjunto, es decir, no esta dentro del conjunto:
                        LVendedores.add(CodVendedor)  #Agrego el vendedor al conjunto
                        break #Corto el if
                    else: #En caso de que tenga menos o mas de 6 digitos o ya este usado
                        print("Código de vendedor no válido o ya utilizado.") #mensaje diciendole que lo tiene mal
                        Intentos -= 1#Resto un intento
                else: 
                    print("Demasiados intentos fallidos. Saliendo del programa.")  #Cuando los intentos llegan a 0 
                    return Matriz  #Devuelvo la matriz

                Matriz[0][c] = CodVendedor  #Asigno la primera fila para el codigo de vendedor

                VentasVendedor = {} #Diccionario donde guardo las ventas de cada vendedor, "Vendedor":Venta
                TotalVentas = 0 #Total de ventas, cada vendedor esta restringido a 10 ventas
                while TotalVentas < 10: # Asegurar que no se vendan más de 10 unidades
                    Producto = random.choice(list(Productos.keys())) #Elijo de manera random un producto del diccionario
                    CantidadVentas = random.randint(1, 10 - TotalVentas) # Limitar la cantidad de ventas al total permitido
                    VentasVendedor[Producto] = CantidadVentas
                    TotalVentas += CantidadVentas

                ProductoMasVendido = max(VentasVendedor, key=VentasVendedor.get) # Obtener el producto más vendido, utilizando el diccionario VentasVendedor
                ProductoMasCaro = max(VentasVendedor, key=lambda x: Productos[x]) # Obtener el producto más caro vendido, utilizando el diccionario VentasVendedor

                Matriz[1][c] = sum(VentasVendedor.values()) #Asigno la segunda fila al total de ventas, uso la funcion sum.
                Matriz[2][c] = sum([VentasVendedor[Producto] * Productos[Producto] for Producto in VentasVendedor.keys()]) #Asigno la fila 3 al total en $ de ventas, utilizando nuevamente la funcion sum y una listra por compresion
                Matriz[3][c] = ProductoMasVendido  #Asigno la fila 4 al producto mas vendido
                Matriz[4][c] = ProductoMasCaro #Asigno la fila 5 al producto mas caro vendido por el vendedor

            return Matriz

    except FileNotFoundError: #En caso de no encontrar el archivo
        print("No se pudo encontrar el archivo 'Productos.txt'.") #Imprimo este mensaje de error.
        return None


def GuardarJornada(Matriz, Vendedores, DD, MM, AA):
    NombreArchivo = "Jornada-{}-{}-{}.txt".format(DD, MM, AA) #Creo nombre de archivo dependiendo la fecha otorgada por el usuario
    try:
        Jornada = open(NombreArchivo, "w") # Abro el archivo en modo escritura y lo guardo en la variable Jornada. Si no existe se crea, si existe se sobreescribe
        # Escribir la fecha en el archivo
        Jornada.write("{}/{}/{}\n".format(DD,MM,AA))
        # Escribir los datos de la jornada en el archivo
        for i in range(Vendedores): # Para cada vendedor
            Jornada.write("{};{};{};{};{}\n".format(Matriz[0][i], Matriz[1][i], Matriz[2][i], Matriz[3][i], Matriz[4][i])) # Escribo en una línea cada dato.
        print("Datos de la jornada guardados correctamente en el archivo 'Jornada.txt'.") # Imprimo mensaje de que se guardó correctamente el archivo.
        return NombreArchivo
    except OSError:
        print("Error al procesar el archivo.")
    
def LeerArchivo(Jornada):
    try:
        Jornada = open(Jornada, "r")
        # Leer la fecha de la primera línea
        Fecha = Jornada.readline().strip()
        print("Fecha:", Fecha)  # Imprimir la fecha
        print("-" * 40)
        # Leer las líneas restantes y procesar los datos
        for Linea in Jornada:
            Cod_Vendedor, Cant_Ventas, Total_Ventas, Prod_Cant, Prod_Caro = Linea.strip().split(";")
            while Linea: #Mientras que linea sea True, es decir, mientras tenga un dato va a reproducir lo siguiente:
                Cod_Vendedor, Cant_Ventas, Total_Ventas, Prod_Cant, Prod_Caro = Linea.split(";") #Desampaqueto la linea en las 5 variables. Esto se puede realizar debido a que siempre tenemos 5 datos para cada linea
                print(f'Cod.Vendedor: {str(Cod_Vendedor).rjust(25," ")}') #Impresion del codigo de vendedor y ajustado a la derecha por 25 lugares
                print(f'Cant. Ventas: {str(Cant_Ventas).rjust(25," ")}') #Impresion de la cantidad de ventas y ajustado a la derecha por 25 lugares
                print(f'Total de $: {str(Total_Ventas).rjust(27," ")}') #Impresion del total de ventas y ajustado a la derecha por 27 lugares
                print(f'Producto mas vendido: {str(Prod_Cant).rjust(17," ")}') #Impresion del producto mas vendido por vendedor y ajustado a la derecha por 17 lugares
                print(f'Producto mas caro vendido: {str(Prod_Caro).rjust(13," ")}') #Impresion del producto mas caro vendido por vendedor y ajustado a la derecha por 13 lugares
                print("-" * 40)  # Separador entre vendedores
                Linea = Jornada.readline() #Leo la siguiente linea del archivo Jornada.txt
    except FileNotFoundError as MensajeError: #En caso de que no encuentre el archivo salta el siguiente except con su mensaje de error.
        print("No se puede abrir el archivo:", MensajeError)
    except OSError as MensajeError: #En caso de algun error de sistema, salta el siguiente except con su mensaje de error.
        print("Error de sistema:",MensajeError)

def MostrarMatriz(Matriz, Vendedores):
    for f in range(5):
        print(" ".join(f"{Matriz[f][c]:<10}" for c in range(Vendedores)))

def main():
    CantVendedores = int(input("Ingrese la cantidad de vendedores activos:")) #Pregunto cantidad de vendedores activos
   
    while True: #Mientras que sea verdadero, realizo lo siguiente
        Dia = int(input("Ingrese el día: ")) #Pido el dia
        Mes = int(input("Ingrese el mes: ")) #Pido el mes
        Año = int(input("Ingrese el año: ")) #Pido el año
        if VerificarFecha(Dia, Mes, Año): #Verifico la fecha
            break #En caso que sea correcta, corto el ciclo while.
        else:
            print("Fecha inválida. Por favor, ingrese una fecha válida.") #En caso que sea incorrecta, muestro mensaje y vuelvo a pedir la fecha

    #CargarProductos() #Creo archivo productos
    Matriz = CrearMatriz(CantVendedores) #Creo matriz
    Jornada = GuardarJornada(Matriz, CantVendedores,Dia,Mes,Año) #Guardo la matriz en un txt, con la fecha como nombre de archivo
    LeerArchivo(Jornada) #Leo el archivo en formato de impresion
    #MostrarMatriz(Matriz, CantVendedores)

if __name__ == "__main__":
    main()