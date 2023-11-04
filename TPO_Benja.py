import os
import random
def GenerarCodigoVendedor():
    vendedores_existentes = set()
    while True:
        codigo_vendedor = str(random.randint(10000, 99999))
        if codigo_vendedor not in vendedores_existentes:
            vendedores_existentes.add(codigo_vendedor)
            return codigo_vendedor

def GenerarProductos():
    productos = [["Heladera", 250, 500],
                 ["Horno", 200, 450],
                 ["Televisor", 400, 650],
                 ["Microondas", 100, 350],
                 ["Lavavajilla", 300, 550]]
    try:
        if os.path.exists("Productos.txt"):
            os.remove("Productos.txt")
        with open("Productos.txt", "a") as archivo_productos:
            for producto in productos:
                stock = random.randint(80, 200)
                nombre, precio_lista, precio = producto
                archivo_productos.write(f"{nombre};{precio_lista};{precio};{stock}\n")
        print("Archivo de productos creado correctamente.")
    except Exception as e:
        print(f"Error al crear el archivo de productos: {e}")

def ProductoExistente(producto, productos):
    with open("Productos.txt", "r") as ArcProductos:
        for linea in ArcProductos:
            nombre_producto = linea.strip().split(";")[0]
            if nombre_producto == producto:
                return True
    return False

def AgregarProducto(Nombre, PrecioLista, Precio, productos):
    try:
        if not ProductoExistente(Nombre, productos):
            with open("Productos.txt", "a") as ArcProductos:
                Stock = random.randint(80, 200)
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
                codigo_producto,precio_lista, precio, stock = Linea.strip().split(";")
                Productos.append([codigo_producto, int(precio_lista), int(precio), int(stock)])
                Linea = ArcProductos.readline()
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
                if Stock > 0:
                    CantVendida = random.randint(1, min(80, Stock))
                    CantVendida = min(CantVendida, Stock)
                    if CantVendida > 0:
                        Producto[3] -= CantVendida
                        VentasVendedor.append([CodigoProducto, CantVendida, Precio])
            VentasMes.append(VentasVendedor)
        with open("Productos.txt", "w") as ArcProductos:
            for Producto in Productos:
                ArcProductos.write(f"{Producto[0]};{Producto[1]};{Producto[2]};{Producto[3]}\n")
        return VentasMes
    else:
        print("No se pudieron cargar los productos.")
        return None

def ImprimirStock(productos):
    if productos:
        print("Stock de Productos:")
        for producto in productos:
            nombre, precio_lista, precio, stock = producto
            if stock < 10:
                estado_stock = "Restock"
            else:
                estado_stock = "Suficiente"
            print(f"Producto: {nombre}, Stock: {stock}, Estado: {estado_stock}")
    else:
        print("No se pudieron cargar los datos de productos.")

def ProductoMasVendido():
    ProductosVendidos = {}
    try:
        with open("VentasMensuales.txt", "r") as ArcVentas:
            for Linea in ArcVentas:
                valores = Linea.strip().split(";")
                if len(valores) == 4:
                    CodVendedor, Producto, Cantidad, PrecioVenta = valores
                    Cantidad = int(Cantidad)
                    ProductosVendidos[Producto] = ProductosVendidos.get(Producto, 0) + Cantidad
                else:
                    print(f"Error: La línea '{Linea.strip()}' no tiene el formato esperado.")
        if ProductosVendidos:
            Producto_Mas_Vendido = max(ProductosVendidos, key=ProductosVendidos.get)
            Cantidad = ProductosVendidos[Producto_Mas_Vendido]
            print(f"Producto más vendido: {Producto_Mas_Vendido} (Cantidad vendida: {Cantidad})")
        else:
            print("No hay datos de ventas disponibles.")
    except FileNotFoundError:
        print("No se pudo encontrar el archivo 'VentasMensuales.txt'.")
    except Exception as e:
        print(f"Error: {e}")

def OpcionesGerente():
    ProductoMasVendido()

def GuardarVentasMensuales(VentasMes):
    try:
        ArcVentas = open("VentasMensuales.txt", "w")
        for VentasVendedor in VentasMes:
            codigo_vendedor = GenerarCodigoVendedor()
            for producto, cantidad, precio in VentasVendedor:
                total_venta = cantidad * precio
                ArcVentas.write(f"{codigo_vendedor};{producto};{cantidad};{total_venta}\n")
        print("Ventas mensuales guardadas correctamente en 'VentasMensuales.txt'.")
    except Exception as e:
        print(f"Error al guardar las ventas mensuales: {e}")

def LeerVentasMensuales():
    ventas_mensuales = []
    try:
        with open("VentasMensuales.txt", "r") as archivo_ventas:
            vendedor_actual = None
            linea = archivo_ventas.readline().strip()
            while linea:
                if ";" in linea:
                    valores = linea.split(";")
                    vendedor, producto, cantidad, total_venta = valores[0], valores[1], int(valores[2]), int(valores[3])
                    
                    if vendedor_actual is None or vendedor != vendedor_actual["Vendedor"]:
                        if vendedor_actual:
                            ventas_mensuales.append(vendedor_actual)
                        vendedor_actual = {"Vendedor": vendedor, "Productos": []}
                    
                    vendedor_actual["Productos"].append({
                        "Producto": producto,
                        "Cantidad": cantidad,
                        "Total Venta": total_venta
                    })
                
                linea = archivo_ventas.readline().strip()
            
            if vendedor_actual:
                ventas_mensuales.append(vendedor_actual)
                
            return ventas_mensuales
    
    except FileNotFoundError:
        print("No se pudo encontrar el archivo 'VentasMensuales.txt'.")
        return None

def main():
    productos = LeerProductos()
    TotalDinero = 0
    if productos:
        while True:
            print("-" * 40)
            print("Menu")
            print("1: Generar archivo productos\n2: Agregar Producto\n3: Generar Ventas Mensuales\n4: Leer ventas\n5: OpcionesGerente\n6: Imprimir stock\n7: Salir")
            print("-" * 40)
            Selec = int(input())
            print("-" * 40)

            if Selec == 1:
                GenerarProductos()
            elif Selec == 2:
                Producto = input("Ingrese el nombre de producto:")
                PrecioLista = int(input("Ingrese el precio de lista:"))
                Precio = int(input("Ingrese el precio:"))
                AgregarProducto(Producto, PrecioLista, Precio, productos)
                productos.append([Producto, PrecioLista, Precio])
            elif Selec == 3:
                CantVendedores = int(input("Ingrese el número de vendedores: "))
                VentasMes = GenerarVentasMensuales(CantVendedores)
                if VentasMes:
                    GuardarVentasMensuales(VentasMes)
                else:
                    print("No se generaron ventas mensuales.")
            elif Selec == 4:
                ventas_mensuales = LeerVentasMensuales()
                if ventas_mensuales:
                    for vendedor in ventas_mensuales:
                        total_productos_vendidos = 0
                        print(f"Vendedor: {vendedor['Vendedor']}")
                        for producto in vendedor["Productos"]:
                            print(f"Producto: {producto['Producto']} | Cantidad: {producto['Cantidad']} | Total Venta: {producto['Total Venta']}")
                            total_productos_vendidos += producto['Cantidad']
                            TotalDinero += producto['Total Venta']
                        print(f"Total de productos vendidos por este vendedor: {total_productos_vendidos}")
                        print("-" * 40)
                    print(f"Total de dinero del mes por todos los vendedores: {TotalDinero}")
                    print("-" * 40)
                else:
                    print("No se pudieron cargar los datos de ventas mensuales.")
            elif Selec == 5:
                OpcionesGerente()
            elif Selec == 6:
                productos = LeerProductos()
                ImprimirStock(productos)
            elif Selec == 7:
                print("Saliendo del programa.")
                break
            else:
                print("Opción inválida. Por favor, ingrese 1, 2, 3, 4, 5 o 6")

if __name__ == "__main__":
    main()