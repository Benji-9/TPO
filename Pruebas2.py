import os
import random
def GenerarProductos():
    Productos = [[43135, 250, 500],
                 [12527, 200, 450],
                 [63127, 400, 650],
                 [91800, 100, 350],
                 [60920, 300, 550]]
    try:
        if os.path.exists("Productos.txt"):
            os.remove("Productos.txt")
        with open("Productos.txt", "a") as ArcProductos:
            for Producto in Productos:
                Stock = random.randint(5,100)
                Nombre, PrecioLista, Precio = Producto
                ArcProductos.write(f"{Nombre};{PrecioLista};{Precio};{Stock}\n")
        print("Archivo creado correctamente.")
    except Exception as e:
        print(f"Error al crear el archivo: {e}")

def ProductoExistente(producto, productos):
    for prod in productos:
        if prod[0] == producto:
            return prod
    return None

def AgregarProducto(Nombre, PrecioLista, Precio, productos):
    try:
        if not ProductoExistente(Nombre, productos):
            with open("Productos.txt", "a") as ArcProductos:
                Stock = random.randint(5, 100)
                ArcProductos.write(f"{Nombre};{PrecioLista};{Precio};{Stock}\n")
            print("Producto agregado correctamente.")
        else:
            print("El producto ya existe en el archivo.")
    except Exception as e:
        print(f"Error al agregar el producto: {e}")

def LeerProductos():
    Productos = []
    try:
        with open("Productos.txt", "r") as ArcProductos:
            Linea = ArcProductos.readline()
            while Linea:
                nombre, precio_lista, precio, stock = Linea.strip().split(";")
                Productos.append([nombre, int(precio_lista), int(precio), int(stock)])
                Linea = ArcProductos.readline()  # Obtener la próxima línea del archivo
        return Productos
    except FileNotFoundError:
        print("No se pudo encontrar el archivo 'Productos.txt'.")
        return None

def GenerarVentasMensuales(Vendedores):
    Productos = LeerProductos()
    if Productos:
        VentasMes = []
        for _ in range(Vendedores):
            VentasVendedor = []
            for Producto in Productos:
                CodigoProducto, PrecioLista, Precio, Stock = Producto
                CantVendida = random.randint(1, Stock)
                if CantVendida > 0:
                    VentasVendedor.append([CodigoProducto, CantVendida, Precio])
                    Stock -= CantVendida
            VentasMes.append(VentasVendedor)
        return VentasMes
    else:
        print("No se pudieron cargar los productos.")
        return None

def main():
    productos = []
    while True:
        print("-" * 40)
        print("Menu")
        print("1:Generar archivo productos\n2:Agregar Producto\n3:Generar Ventas Mensuales\n4:Salir")
        print("-" * 40)
        Selec = int(input())
        print("-" * 40)

        if Selec == 1:
            GenerarProductos()
        elif Selec == 2:
            Producto = input("Ingrese el codigo de producto:")
            PrecioLista = int(input("Ingrese el precio de lista:"))
            Precio = int(input("Ingrese el precio:"))
            AgregarProducto(Producto, PrecioLista, Precio, productos)
            productos.append([Producto, PrecioLista, Precio])
        elif Selec == 3:
            CantVendedores = int(input("Ingrese el número de vendedores: "))
            VentasMes = GenerarVentasMensuales(CantVendedores)
            if VentasMes:
                Vendedori = 1
                for VentasVendedor in VentasMes:
                    print(f"Vendedor {Vendedori}:")
                    Vendedori += 1
                    for Producto, Cantidad, Precio in VentasVendedor:
                        total_venta = Cantidad * Precio
                        print(f"Producto: {Producto}, Cantidad: {Cantidad}, Total Venta: {total_venta}")
            else:
                print("No se generaron ventas mensuales.")
        elif Selec == 4:
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, ingrese 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()