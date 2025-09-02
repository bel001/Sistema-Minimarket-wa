# Sistema de Gestión para Minimarket  🛒

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white) ![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange) ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)

Este es un sistema de Punto de Venta (POS) y gestión de inventario de escritorio, desarrollado para facilitar la administración de pequeños negocios como minimarkets. La aplicación está construida completamente en Python, utilizando la librería Tkinter para la interfaz gráfica.

![Captura de Pantalla del Dashboard]
<img width="1366" height="728" alt="image" src="https://github.com/user-attachments/assets/efd6dd85-cc24-4225-acc0-f91dd97bfd5d" />



---

## ✨ Características Principales

El sistema cuenta con varios módulos para una gestión integral del negocio:

*   📦 **Gestión de Inventario:** Permite agregar, eliminar y modificar productos. Controla el stock actual y un stock mínimo para alertar sobre productos que se están agotando.
*   🛒 **Módulo de Ventas:** Interfaz intuitiva para registrar ventas, seleccionar productos, cantidades y métodos de pago.
*   📄 **Generación de Boletas:** Al registrar una venta, se genera automáticamente una boleta en formato PDF lista para imprimir.
*   🚚 **Gestión de Despachos y Reservas:** Permite registrar pedidos de clientes para entrega futura, marcándolos como "Pendientes" o "Entregados", descontando el stock solo al momento de la entrega.
*   📝 **Control de Compras:** Registra las compras realizadas a proveedores y actualiza el stock de productos al marcar una compra como "Recibida".
*   📈 **Reportes y Estadísticas:** Módulo visual que genera gráficos sobre:
    *   Ventas totales por producto.
    *   Ganancias generadas por producto.
    *   Ranking de los productos más y menos vendidos.
*   👤 **Gestión de Empleados y Roles:** Soporta diferentes roles de usuario (Administrador y Vendedor) con distintos niveles de acceso a los módulos.

---

## 🛠️ Tecnologías Utilizadas

*   **Lenguaje de Programación:** Python 3
*   **Interfaz Gráfica (GUI):** Tkinter
*   **Manipulación de Datos:** Pandas (para gestionar los archivos Excel como bases de datos)
*   **Generación de Reportes PDF:** FPDF
*   **Visualización de Gráficos:** Matplotlib

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/bel001/Sistema-Minimarket-wa.git
    ```

2.  **Navega a la carpeta del proyecto:**
    ```bash
    cd Sistema-Minimarket-wa
    ```

3.  **Instala las dependencias:**
    Asegúrate de tener Python 3 instalado. Luego, instala las librerías necesarias ejecutando:
    ```bash
    pip install pandas openpyxl Pillow fpdf matplotlib
    ```

4.  **Ejecuta la aplicación:**
    ```bash
    python minimarket_jardines.py
    ```
    *El nombre del archivo principal debe coincidir con el de tu proyecto.*

---

## 🔑 Acceso al Sistema

El sistema viene con dos usuarios pre-configurados para que puedas probar las diferentes funcionalidades y roles:

| Rol           | Usuario | Contraseña |
| :------------ | :------ | :--------- |
| **Administrador** | `admin` | `admin`    |
| **Vendedor**      | `abel`  | `abel`     |

El rol de **Administrador** tiene acceso a todos los módulos, mientras que el **Vendedor** tiene un acceso más limitado, centrado principalmente en el módulo de ventas.

---

## ✍️ Autor

*   **Abel** - [bel001](https://github.com/bel001)
