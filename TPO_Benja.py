import random
def ValidarVendedor(Vendedor):
    return len(str(Vendedor)) == 6

def VerificarFecha(DD, MM, AA):
    '''
    Verifica que la fecha sea correcta, teniendo en cuenta años bisiestos y los dias en los meses correspondientes.
    '''
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

def LogoEmpresa(Empresa):
    Sigla = ""
    Siglas = Empresa.split(" ",len(Empresa))
    for Palabra in Siglas:
        Sigla = Sigla + Palabra[0].upper()
    return Empresa,Sigla

def GenerarVentas():
    '''
    Generador de ventas: Agarra de manera random un producto y genera una cantidad random de ventas, cada venta es guardada en un diccionario para 
    llevar un registro.
    Devuelve el diccionario para poder obtener el producto mas vendido por el vendedor y el producto mas caro.
    '''
    Productos = LeerProductos()
    VentasVendedor = {}
    TotalVentas = 0

    while TotalVentas < 50:
        Producto = random.choice(list(Productos.keys()))
        CantidadVentas = random.randint(1, 50 - TotalVentas)
        VentasVendedor[Producto] = CantidadVentas
        TotalVentas += CantidadVentas

    return VentasVendedor

def ObtenerProductosMasVendidoYCaro(VentasVendedor):
    '''
    Funcion que obtiene a travez del diccionario VentasVendedor el producto que mas vendio el vendedor y el producto mas caro.
    Devuelve las dos variables para que puedan ser incluidas en la matriz
    '''
    Productos = LeerProductos()
    ProductoMasVendido = max(VentasVendedor, key=VentasVendedor.get)
    ProductoMasCaro = max(VentasVendedor, key=lambda x: Productos[x])

    return ProductoMasVendido, ProductoMasCaro

def LeerProductos():
    DictProductos = {}
    try:
        ArcProductos = open("Productos.txt", "r")
        Linea = ArcProductos.readline()
        while Linea:
            Producto,Precio = Linea.split(";")
            DictProductos[Producto] = int(Precio)
            Linea = ArcProductos.readline()
        return DictProductos
    except FileNotFoundError:
        print("No se pudo encontrar el archivo 'Productos.txt'.")
        return None
    finally:
        try:
            ArcProductos.close()
        except NameError:
            pass

def CrearMatriz(Vendedores):
    try:
        Productos = LeerProductos()
        if Productos:
            Matriz = [[0] * Vendedores for _ in range(5)]
            LVendedores = set()

            for c in range(Vendedores):
                Intentos = 3
                while Intentos > 0:
                    CodVendedor = input("Ingrese el código del vendedor {} (6 dígitos): ".format(c + 1))
                    if ValidarVendedor(CodVendedor) and CodVendedor not in LVendedores:
                        LVendedores.add(CodVendedor)
                        break
                    else:
                        print("Código de vendedor no válido o ya utilizado.")
                        Intentos -= 1
                else:
                    print("Demasiados intentos fallidos. Saliendo del programa.")
                    return None  # Retorna None en caso de demasiados intentos fallidos

                Matriz[0][c] = CodVendedor  #Asigno la primera fila para el codigo de vendedor
                VentasVendedor = GenerarVentas()
                ProductoMasVendido, ProductoMasCaro = ObtenerProductosMasVendidoYCaro(VentasVendedor)
                #Obtener el producto más vendido, utilizando el diccionario VentasVendedor
                #Obtener el producto más caro vendido, utilizando el diccionario VentasVendedor

                Matriz[1][c] = sum(VentasVendedor.values()) #Asigno la segunda fila al total de ventas, uso la funcion sum.
                Matriz[2][c] = sum([VentasVendedor[Producto] * Productos[Producto] for Producto in VentasVendedor.keys()]) #Asigno la fila 3 al total en $ de ventas, utilizando nuevamente la funcion sum y una listra por compresion
                Matriz[3][c] = ProductoMasVendido  #Asigno la fila 4 al producto mas vendido
                Matriz[4][c] = ProductoMasCaro #Asigno la fila 5 al producto mas caro vendido por el vendedor

            Total_Ventas = sum(Matriz[1])
            Total_Dinero = sum(Matriz[2])
            return Matriz, Total_Ventas, Total_Dinero

    except FileNotFoundError: #En caso de no encontrar el archivo
        print("No se pudo encontrar el archivo 'Productos.txt'.") #Imprimo este mensaje de error.
        return None

def GuardarJornada(Matriz, Vendedores, DD, MM, AA,TotalVentas,TotalDinero,Empresa):
    NombreArchivo = "Jornada-{}-{}-{}.txt".format(DD, MM, AA) #Creo nombre de archivo dependiendo la fecha otorgada por el usuario
    try:
        Jornada = open(NombreArchivo, "w") # Abro el archivo en modo escritura y lo guardo en la variable Jornada. Si no existe se crea, si existe se sobreescribe
        # Escribir la fecha en el archivo
        Jornada.write("{}/{}/{}\n".format(DD,MM,AA))
        EmpresaF,Sigla = LogoEmpresa(Empresa)
        Jornada.write("{} - {}\n".format(EmpresaF,Sigla))
        # Escribir los datos de la jornada en el archivo
        for i in range(Vendedores): # Para cada vendedor
            Jornada.write("{};{};{};{};{}\n".format(Matriz[0][i], Matriz[1][i], Matriz[2][i], Matriz[3][i], Matriz[4][i])) # Escribo en una línea cada dato.
        print("Datos de la jornada guardados correctamente en el archivo 'Jornada.txt'.") # Imprimo mensaje de que se guardó correctamente el archivo.
        Jornada.write(str(TotalVentas)+";"+str(TotalDinero))
        return NombreArchivo
    except OSError:
        print("Error al procesar el archivo.")
    finally:
        try:
            Jornada.close()
        except NameError:
            pass
    
def LeerArchivo(Jornada):
    try:
        Archivo = open(Jornada, "r")
        # Leer la fecha de la primera línea
        Fecha = Archivo.readline().strip()
        Empresa = Archivo.readline().strip()
        print("Fecha:", Fecha)  # Imprimir la fecha
        print("{}".format(Empresa))
        print("-" * 40)
        # Leer las líneas restantes y procesar los datos
        TotalVentas = 0
        TotalDinero = 0
        Linea = Archivo.readline()
        while Linea:
            datos = Linea.split(";")
            if len(datos) == 5:  # Verificar si la línea tiene los 5 valores esperados
                Cod_Vendedor, Cant_Ventas, Total_Ventas, Prod_Cant, Prod_Caro = datos
                print(f'Cod.Vendedor: {str(Cod_Vendedor).rjust(25," ")}')
                print(f'Cant. Ventas: {str(Cant_Ventas).rjust(25," ")}')
                print(f'Total de $: {str(Total_Ventas).rjust(27," ")}')
                print(f'Producto mas vendido: {str(Prod_Cant).rjust(17," ")}')
                print(f'Producto mas caro vendido: {str(Prod_Caro).rjust(13," ")}')
                print("-" * 40)
                TotalVentas += int(Cant_Ventas)
                TotalDinero += int(Total_Ventas)
            Linea = Archivo.readline()
        print("Total de ventas de todos los vendedores:", TotalVentas)
        print("Total de dinero de todos los vendedores:", TotalDinero)
    except FileNotFoundError as MensajeError:
        print("No se puede abrir el archivo:", MensajeError)
    except OSError as MensajeError:
        print("Error de sistema:", MensajeError)
    finally:
        try:
            Archivo.close()
        except NameError:
            pass

def main():
    CantVendedores = int(input("Ingrese la cantidad de vendedores activos:")) #Pregunto cantidad de vendedores activos
    Empresa = "Grupo 7 Electrodomesticos"
    while True: #Mientras que sea verdadero, realizo lo siguiente
        Dia = int(input("Ingrese el día: ")) #Pido el dia
        Mes = int(input("Ingrese el mes: ")) #Pido el mes
        Año = int(input("Ingrese el año: ")) #Pido el año
        if VerificarFecha(Dia, Mes, Año): #Verifico la fecha
            break #En caso que sea correcta, corto el ciclo while.
        else:
            print("Fecha inválida. Por favor, ingrese una fecha válida.") #En caso que sea incorrecta, muestro mensaje y vuelvo a pedir la fecha
    
    Matriz,TotalVentas,TotalDinero = CrearMatriz(CantVendedores) #Creo matriz
    Jornada = GuardarJornada(Matriz, CantVendedores,Dia,Mes,Año,TotalVentas,TotalDinero,Empresa) #Guardo la matriz en un txt, con la fecha como nombre de archivo
    LeerArchivo(Jornada) #Leo el archivo en formato de impresion

if __name__ == "__main__":
    main()