import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, scrolledtext
from PIL import Image, ImageTk
from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import shutil
import subprocess

def generar_boleta_pdf(row, boleta_path, nombre_negocio="Minimarket", logo_path=None):
    from fpdf import FPDF
    import os

    pdf = FPDF("P", "mm", "A5")
    pdf.add_page()
    y = 10
    if logo_path and os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=y, w=28)
        y += 18
    else:
        y += 8

    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(37, 109, 133)
    pdf.cell(0, 14, nombre_negocio.upper(), 0, 1, "C")
    pdf.ln(2)
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 138, pdf.get_y())
    pdf.ln(2)

    row_dict = dict(row) # Asegurarse de que funcione con Series de pandas o dicts
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0,0,0)
    pdf.cell(70, 7, f"Fecha: {row_dict.get('Fecha', '')}", 0, 0, "L")
    pdf.cell(0, 7, f"N°: {row_dict.get('ID Venta', '')}", 0, 1, "R")
    pdf.cell(70, 7, f"Cliente: {row_dict.get('Cliente', '')}", 0, 0, "L")
    pdf.cell(0, 7, f"Vendedor: {row_dict.get('Vendedor', '')}", 0, 1, "R")
    pdf.cell(70, 7, f"Método de pago: {row_dict.get('Tipo Pago', '')}", 0, 1, "L")
    pdf.ln(3)

    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(37, 109, 133)
    pdf.set_text_color(255,255,255)
    th = 9
    pdf.cell(54, th, "Producto", 1, 0, "C", True)
    pdf.cell(18, th, "Cant.", 1, 0, "C", True)
    pdf.cell(34, th, "P. Unitario", 1, 0, "C", True)
    pdf.cell(34, th, "Subtotal", 1, 1, "C", True)
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0,0,0)
    pdf.cell(54, th, str(row_dict.get("Producto", "")), 1, 0, "C")
    pdf.cell(18, th, str(row_dict.get("Cantidad", "")), 1, 0, "C")
    pdf.cell(34, th, f"S/ {float(row_dict.get('Precio Unitario', 0)):.2f}", 1, 0, "C")
    pdf.cell(34, th, f"S/ {float(row_dict.get('Total', 0)):.2f}", 1, 1, "C")

    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(106, th, "TOTAL", 1, 0, "R", True)
    pdf.set_text_color(37, 109, 133)
    pdf.cell(34, th, f"S/ {float(row_dict.get('Total', 0)):.2f}", 1, 1, "C", True)
    pdf.set_text_color(0,0,0)
    pdf.ln(8)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(120,120,120)
    pdf.cell(0, 7, "Gracias por su preferencia. ¡Lo esperamos pronto!", 0, 1, "C")
    pdf.ln(2)
    pdf.set_font("Arial", "", 8)
    pdf.set_text_color(150,150,150)
    pdf.cell(0, 5, "Documento generado automáticamente por el sistema.", 0, 1, "C")

    pdf.output(boleta_path)

# ------------ CONFIGURACIÓN Y UTILIDADES -------------
DATA_DIR = "db"
REPORTES_DIR = "reportes"
IMG_DIR = os.path.join(DATA_DIR, "imagenes")
PRODUCTOS_FILE = os.path.join(DATA_DIR, "productos.xlsx")
VENTAS_FILE = os.path.join(DATA_DIR, "ventas.xlsx")
EMPLEADOS_FILE = os.path.join(DATA_DIR, "empleados.xlsx")
COMPRAS_FILE = os.path.join(DATA_DIR, "compras.xlsx")
CATEGORIAS_FILE = os.path.join(DATA_DIR, "categorias.xlsx")
DESPACHO_FILE = os.path.join(DATA_DIR, "despachos.xlsx")
MINIMARKET_NOMBRE = "Minimarket Jardines"

def asegurarse_archivos():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTES_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    if not os.path.exists(PRODUCTOS_FILE):
        pd.DataFrame(columns=["ID", "Nombre", "Categoría", "Tipo de Corte", "Precio", "Stock", "Stock Mínimo", "Imagen"]).to_excel(PRODUCTOS_FILE, index=False)
    if not os.path.exists(VENTAS_FILE):
        pd.DataFrame(columns=["ID Venta", "Fecha", "Cliente", "Producto", "Cantidad", "Precio Unitario", "Total", "Tipo Pago", "Vendedor"]).to_excel(VENTAS_FILE, index=False)
    if not os.path.exists(EMPLEADOS_FILE):
        df = pd.DataFrame(columns=["Usuario", "Contraseña", "Nombre", "Cargo", "Horario", "Funciones"])
        df.loc[0] = ["admin", "admin123", "Administrador", "Administrador", "08:00-20:00", "todos"]
        df.to_excel(EMPLEADOS_FILE, index=False)
    if not os.path.exists(COMPRAS_FILE):
        pd.DataFrame(columns=["ID Compra", "Fecha", "Proveedor", "Producto", "Cantidad", "Estado"]).to_excel(COMPRAS_FILE, index=False)
    if not os.path.exists(CATEGORIAS_FILE):
        pd.DataFrame(columns=["ID", "Nombre"]).to_excel(CATEGORIAS_FILE, index=False)
    if not os.path.exists(DESPACHO_FILE):
        pd.DataFrame(columns=["ID", "Fecha Reserva", "Cliente", "Producto", "Cantidad", "Estado", "Fecha Entrega"]).to_excel(DESPACHO_FILE, index=False)

def generar_id(prefix):
    return f"{prefix}{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}"

def cargar_categorias():
    try:
        df = pd.read_excel(CATEGORIAS_FILE)
        return df["Nombre"].dropna().tolist()
    except FileNotFoundError:
        return []

def agregar_categoria_rapido(parent=None):
    nombre = simpledialog.askstring("Nueva Categoría", "Nombre de la nueva categoría:", parent=parent)
    if not nombre:
        return None
    df = pd.read_excel(CATEGORIAS_FILE)
    if nombre in df["Nombre"].values:
        messagebox.showerror("Error", "Esa categoría ya existe.", parent=parent)
        return None
    nuevo_id = f"C{len(df)+1:03d}"
    df.loc[len(df)] = [nuevo_id, nombre]
    df.to_excel(CATEGORIAS_FILE, index=False)
    return nombre

def boton_grande(frame, texto, color, comando, icono=""):
    return tk.Button(frame, text=(icono + " " + texto if icono else texto), font=("Arial", 14, "bold"), bg=color, fg="white", activebackground=color, activeforeground="white", width=18, height=2, command=comando)

# ------------ LOGIN -------------
class LoginVentana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{MINIMARKET_NOMBRE} - Login")
        self.geometry("600x400")
        self.resizable(False, False)
        self.configure(bg="#f8f8f8")

        left_frame = tk.Frame(self, bg="#256d85", width=250, height=400)
        left_frame.place(x=0, y=0, relheight=1)

        right_frame = tk.Frame(self, bg="white", width=350, height=400)
        right_frame.place(x=250, y=0, relheight=1)

        user_icon = tk.Label(right_frame, text="👤", font=("Arial", 52), bg="white", fg="#256d85")
        user_icon.place(x=130, y=32)

        tk.Label(right_frame, text="Ingresa los datos", font=("Arial", 22, "bold"), bg="white", fg="#888").place(x=85, y=105)

        self.usuario_var = tk.StringVar()
        usuario_frame = tk.Frame(right_frame, bg="white")
        usuario_frame.place(x=40, y=160)
        tk.Label(usuario_frame, text="🧑", font=("Arial", 16), bg="white", fg="#256d85").pack(side="left")
        user_entry = tk.Entry(usuario_frame, textvariable=self.usuario_var, font=("Arial", 15), bd=0, width=20, bg="#f1f1f1")
        user_entry.pack(side="left", padx=8, ipady=6)

        self.contrasena_var = tk.StringVar()
        pass_frame = tk.Frame(right_frame, bg="white")
        pass_frame.place(x=40, y=210)
        tk.Label(pass_frame, text="🔒", font=("Arial", 16), bg="white", fg="#256d85").pack(side="left")
        pass_entry = tk.Entry(pass_frame, textvariable=self.contrasena_var, font=("Arial", 15), bd=0, width=20, show="*", bg="#f1f1f1")
        pass_entry.pack(side="left", padx=8, ipady=6)

        tk.Button(
            right_frame, text="INGRESAR", font=("Arial", 16, "bold"),
            bg="#256d85", fg="white", activebackground="#256d85", activeforeground="white",
            bd=0, width=18, height=2, command=self.login, cursor="hand2"
        ).place(x=55, y=280)

        self.resultado = None
        user_entry.focus_set()

    def login(self):
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get()
        try:
            empleados = pd.read_excel(EMPLEADOS_FILE)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo de empleados: {e}")
            return
        user = empleados[(empleados["Usuario"] == usuario) & (empleados["Contraseña"] == contrasena)]
        if user.empty:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            return
        self.resultado = user.iloc[0]
        self.destroy()

# ------------ DASHBOARD -------------
class Dashboard(tk.Tk):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title(f"{MINIMARKET_NOMBRE} - {usuario['Nombre']} ({usuario['Cargo']})")
        self.geometry("1200x750")
        self.minsize(1000, 650)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.setup_ui()

    def setup_ui(self):
        nav_frame = tk.Frame(self, bg="#256d85", width=210)
        nav_frame.pack(side="left", fill="y")
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", fill="both", expand=True)
        botones = [
            ("Inventario", self.mostrar_inventario, "#256d85", "📦"),
            ("Ventas", self.mostrar_ventas, "#256d85", "🛒"),
            ("Compras", self.mostrar_compras, "#256d85", "📝"),
            ("Reportes", self.mostrar_reportes, "#256d85", "📈"),
            ("Empleados", self.mostrar_empleados, "#256d85", "👤"),
            ("Categorías", self.mostrar_categorias, "#256d85", "🏷️"),
            ("Despacho", self.mostrar_despacho, "#1abc9c", "🚚"),
        ]
        for nombre, comando, color, icono in botones:
            if self.usuario["Cargo"].lower() != "administrador" and nombre not in ["Ventas"]:
                continue
            boton_grande(nav_frame, nombre, color, comando, icono).pack(fill="x", pady=7, padx=8)
        boton_grande(nav_frame, "Salir", "#e74c3c", self.on_exit, "🚪").pack(side="bottom", fill="x", pady=30, padx=10)
        self.mostrar_bienvenida()

    def limpiar_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_bienvenida(self):
        self.limpiar_main()
        tk.Label(self.main_frame, text=f"Bienvenido al sistema {MINIMARKET_NOMBRE}",
                 font=("Arial", 24), bg="white").pack(pady=40)
        tk.Label(self.main_frame, text="Seleccione un módulo en el panel izquierdo",
                 font=("Arial", 16), bg="white", fg="#256d85").pack(pady=10)

    def mostrar_inventario(self): self.limpiar_main(); InventarioFrame(self.main_frame)
    def mostrar_ventas(self): self.limpiar_main(); VentasFrame(self.main_frame, self.usuario)
    def mostrar_compras(self): self.limpiar_main(); ComprasFrame(self.main_frame)
    def mostrar_reportes(self): self.limpiar_main(); ReportesFrame(self.main_frame)
    def mostrar_empleados(self):
        if self.usuario["Cargo"].lower() == "administrador":
            self.limpiar_main(); EmpleadosFrame(self.main_frame)
        else: messagebox.showerror("Sin Permisos", "Solo el administrador puede acceder a este módulo.")
    def mostrar_categorias(self): self.limpiar_main(); CategoriaFrame(self.main_frame)
    def mostrar_despacho(self): self.limpiar_main(); DespachoFrame(self.main_frame)
    def on_exit(self): self.destroy()

# ------------ INVENTARIO -------------
class InventarioFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)
        tk.Label(self, text="Inventario", font=("Arial", 22, "bold"), bg="white", fg="#256d85").pack(pady=10)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        style.map("Treeview", background=[("selected", "#d6eaf8")])

        columnas = ("ID", "Nombre", "Categoría", "Tipo de Corte", "Precio", "Stock", "Stock Mínimo", "Imagen")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", selectmode="browse")
        for col in columnas:
            ancho = 120
            if col in ("Nombre", "Categoría"): ancho = 180
            if col == "Tipo de Corte": ancho = 130
            if col == "Precio": ancho = 80
            if col == "Imagen": ancho = 110
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=30, pady=10)

        self.boton_frame = tk.Frame(self, bg="white")
        self.boton_frame.pack(pady=10)
        boton_grande(self.boton_frame, "Agregar Producto", "#2ecc71", self.abrir_panel_registro, "➕").pack(side="left", padx=10)
        boton_grande(self.boton_frame, "Eliminar Producto", "#e74c3c", self.eliminar_producto, "🗑️").pack(side="left", padx=10)
        boton_grande(self.boton_frame, "Actualizar Stock", "#f39c12", self.actualizar_stock, "🔄").pack(side="left", padx=10)
        boton_grande(self.boton_frame, "Refrescar", "#2980b9", self.mostrar_inventario, "🔃").pack(side="left", padx=10)

        self.img_label = tk.Label(self, bg="white")
        self.img_label.pack(pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.mostrar_imagen_producto)
        self.mostrar_inventario()

    def mostrar_inventario(self):
        self.tree.delete(*self.tree.get_children())
        try:
            self.df = pd.read_excel(PRODUCTOS_FILE)
        except:
            self.df = pd.DataFrame(columns=["ID", "Nombre", "Categoría", "Tipo de Corte", "Precio", "Stock", "Stock Mínimo", "Imagen"])
        for _, row in self.df.iterrows():
            precio = "" if pd.isna(row["Precio"]) else f"S/ {float(row['Precio']):.2f}"
            values = (
                row["ID"], row["Nombre"], row["Categoría"], row.get("Tipo de Corte", ""),
                precio,
                int(row["Stock"]) if not pd.isna(row["Stock"]) else "",
                int(row["Stock Mínimo"]) if not pd.isna(row["Stock Mínimo"]) else "",
                os.path.basename(row["Imagen"]) if pd.notna(row["Imagen"]) and str(row["Imagen"]).strip() else ""
            )
            self.tree.insert("", "end", values=values)
        self.img_label.config(image="")
        self.tkimg = None

    def mostrar_imagen_producto(self, event):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        values = item["values"]
        if len(values) < 8: return
        img_name = values[7]
        img_path = os.path.join(IMG_DIR, img_name) if img_name else ""
        if img_path and os.path.exists(img_path):
            img = Image.open(img_path).resize((120,120))
            self.tkimg = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.tkimg)
        else:
            self.img_label.config(image="")

    def abrir_panel_registro(self):
        AgregarProductoToplevel(self)

    def actualizar_stock(self):
        try:
            df = pd.read_excel(PRODUCTOS_FILE)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encuentra el archivo de productos.")
            return

        top = tk.Toplevel(self)
        top.title("Actualizar Stock")
        tk.Label(top, text="ID del producto:").grid(row=0, column=0, padx=5, pady=5)
        id_entry = tk.Entry(top)
        id_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(top, text="Entrada (e) o Salida (s):").grid(row=1, column=0, padx=5, pady=5)
        tipo_entry = tk.Entry(top)
        tipo_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(top, text="Cantidad:").grid(row=2, column=0, padx=5, pady=5)
        cant_entry = tk.Entry(top)
        cant_entry.grid(row=2, column=1, padx=5, pady=5)
        def guardar():
            idp = id_entry.get().strip()
            tipo = tipo_entry.get().strip().lower()
            try:
                cantidad = int(cant_entry.get())
            except:
                messagebox.showerror("Error", "Cantidad inválida.", parent=top)
                return
            if idp not in df["ID"].astype(str).values:
                messagebox.showerror("Error", "ID de producto inválido.", parent=top)
                return
            idx = df.index[df["ID"].astype(str) == idp][0]
            if tipo == "e":
                df.at[idx, "Stock"] += cantidad
            elif tipo == "s":
                if df.at[idx, "Stock"] < cantidad:
                    messagebox.showerror("Error", "Stock insuficiente.", parent=top)
                    return
                df.at[idx, "Stock"] -= cantidad
            else:
                messagebox.showerror("Error", "Tipo inválido (debe ser 'e' o 's').", parent=top)
                return
            df.to_excel(PRODUCTOS_FILE, index=False)
            messagebox.showinfo("Éxito", "Stock actualizado.", parent=top)
            top.destroy()
            self.mostrar_inventario()
        ttk.Button(top, text="Guardar", command=guardar).grid(row=3, columnspan=2, pady=10)

    def eliminar_producto(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Eliminar producto", "Selecciona un producto para eliminar.")
            return
        item = self.tree.item(sel[0])
        values = item["values"]
        id_prod = values[0]
        nombre_prod = values[1]
        if not messagebox.askyesno("Confirmar eliminación", f"¿Seguro que deseas eliminar el producto '{nombre_prod}'?"):
            return
        df = pd.read_excel(PRODUCTOS_FILE)
        df = df[df["ID"].astype(str) != str(id_prod)]
        df.to_excel(PRODUCTOS_FILE, index=False)
        self.mostrar_inventario()
        messagebox.showinfo("Producto eliminado", f"Producto '{nombre_prod}' eliminado correctamente.")

class AgregarProductoToplevel(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Producto")
        self.geometry("520x510")
        self.resizable(False, False)
        self.parent = parent
        self.config(bg="white")
        tk.Label(self, text="Registrar Producto", font=("Arial", 18), bg="white", fg="#256d85").pack(pady=10)
        campos = [("Nombre", ""), ("Precio", "0"), ("Stock inicial", "0"), ("Stock Mínimo", "0")]
        self.entries = {}
        for label, default in campos:
            f = tk.Frame(self, bg="white"); f.pack(pady=5)
            tk.Label(f, text=label+":", bg="white").pack(side="left")
            e = tk.Entry(f); e.insert(0, default); e.pack(side="left")
            self.entries[label] = e
        fcat = tk.Frame(self, bg="white"); fcat.pack(pady=5)
        tk.Label(fcat, text="Categoría:", bg="white").pack(side="left")
        self.categoria_var = tk.StringVar()
        self.categoria_cb = ttk.Combobox(fcat, textvariable=self.categoria_var, values=cargar_categorias(), state="readonly")
        self.categoria_cb.pack(side="left")
        ttk.Button(fcat, text="Nueva...", command=self.agregar_categoria_rapido).pack(side="left", padx=5)
        fcorte = tk.Frame(self, bg="white"); fcorte.pack(pady=5)
        tk.Label(fcorte, text="Tipo de Corte:", bg="white").pack(side="left")
        self.corte_var = tk.StringVar()
        self.corte_cb = ttk.Combobox(fcorte, textvariable=self.corte_var, values=["", "Entero", "Bistec", "Molida", "Churrasco", "Costilla", "Filete", "Pechuga", "Pierna", "Alitas", "Trozos", "Otros"], state="readonly")
        self.corte_cb.pack(side="left")
        self.img_var = tk.StringVar()
        fim = tk.Frame(self, bg="white"); fim.pack(pady=5)
        tk.Label(fim, text="Imagen (opcional):", bg="white").pack(side="left")
        ttk.Button(fim, text="Seleccionar", command=self.seleccionar_imagen).pack(side="left", padx=2)
        self.img_label = tk.Label(fim, text="", bg="white"); self.img_label.pack(side="left")
        bframe = tk.Frame(self, bg="white"); bframe.pack(pady=20)
        boton_grande(bframe, "Guardar Producto", "#2ecc71", self.guardar, "💾").pack(side="left", padx=5)
        boton_grande(bframe, "Cancelar", "#e74c3c", self.destroy, "❌").pack(side="left", padx=5)

    def agregar_categoria_rapido(self):
        nombre = agregar_categoria_rapido(self)
        if nombre:
            self.categoria_cb["values"] = cargar_categorias()
            self.categoria_var.set(nombre)

    def seleccionar_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if path:
            self.img_var.set(path)
            self.img_label.config(text=os.path.basename(path))

    def guardar(self):
        nombre = self.entries["Nombre"].get().strip()
        categoria = self.categoria_var.get()
        tipo_corte = self.corte_var.get().strip()
        try:
            precio = float(self.entries["Precio"].get())
            stock = int(self.entries["Stock inicial"].get())
            stock_min = int(self.entries["Stock Mínimo"].get())
        except Exception as e:
            messagebox.showerror("Error", f"Datos numéricos inválidos: {e}", parent=self); return
        if not nombre or not categoria:
            messagebox.showerror("Error", "Nombre y Categoría son obligatorios.", parent=self); return

        columnas_correctas = ["ID", "Nombre", "Categoría", "Tipo de Corte", "Precio", "Stock", "Stock Mínimo", "Imagen"]
        try:
            df = pd.read_excel(PRODUCTOS_FILE)
            df = df.reindex(columns=columnas_correctas)
        except:
            df = pd.DataFrame(columns=columnas_correctas)

        nuevo_id = generar_id("P")
        img_dest = ""
        if self.img_var.get():
            ext = os.path.splitext(self.img_var.get())[1]
            img_dest = os.path.join(IMG_DIR, f"{nuevo_id}{ext}")
            shutil.copy(self.img_var.get(), img_dest)

        nuevo_producto = pd.DataFrame([[nuevo_id, nombre, categoria, tipo_corte, precio, stock, stock_min, img_dest]], columns=columnas_correctas)
        df = pd.concat([df, nuevo_producto], ignore_index=True)
        
        try:
            df.to_excel(PRODUCTOS_FILE, index=False)
            messagebox.showinfo("Éxito", "Producto registrado.", parent=self)
            self.parent.mostrar_inventario()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error al guardar", f"{e}", parent=self)

# ----------- VENTAS -------------
class VentasFrame(tk.Frame):
    def __init__(self, parent, usuario):
        super().__init__(parent, bg="white")
        self.usuario = usuario
        self.pack(fill="both", expand=True)
        tk.Label(self, text="Ventas", font=("Arial", 22, "bold"), bg="white", fg="#256d85").pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("ID Venta", "Fecha", "Cliente", "Producto", "Cantidad", "Precio Unitario", "Total", "Tipo Pago", "Vendedor"), show="headings")
        for col in self.tree["columns"]:
            ancho = 120
            if col == "Producto": ancho = 180
            if col == "Cliente": ancho = 150
            if col == "Fecha": ancho = 115
            if col == "ID Venta": ancho = 110
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=30, pady=10)
        boton_frame = tk.Frame(self, bg="white")
        boton_frame.pack(pady=10)
        boton_grande(boton_frame, "Registrar Venta", "#2ecc71", self.registrar_venta, "➕").pack(side="left", padx=5)
        boton_grande(boton_frame, "Eliminar Venta", "#e74c3c", self.eliminar_venta, "🗑️").pack(side="left", padx=5)
        boton_grande(boton_frame, "Ver Boleta", "#34495e", self.ver_boleta, "📄").pack(side="left", padx=5)
        boton_grande(boton_frame, "Refrescar", "#2980b9", self.mostrar_ventas, "🔃").pack(side="left", padx=5)
        self.mostrar_ventas()

    def mostrar_ventas(self):
        self.tree.delete(*self.tree.get_children())
        try: df = pd.read_excel(VENTAS_FILE)
        except: return
        for _, row in df.iterrows():
            precio_unit = "" if pd.isna(row["Precio Unitario"]) else f"S/ {float(row['Precio Unitario']):.2f}"
            total = "" if pd.isna(row["Total"]) else f"S/ {float(row['Total']):.2f}"
            values = (row["ID Venta"], row["Fecha"], row["Cliente"], row["Producto"], int(row["Cantidad"]) if not pd.isna(row["Cantidad"]) else "", precio_unit, total, row["Tipo Pago"], row["Vendedor"])
            self.tree.insert("", "end", values=values)

    def registrar_venta(self): VentaToplevel(self, self.usuario)
    def eliminar_venta(self):
        sel = self.tree.selection()
        if not sel: return
        id_venta = self.tree.item(sel[0])["values"][0]
        df = pd.read_excel(VENTAS_FILE)
        df = df[df["ID Venta"] != id_venta]
        df.to_excel(VENTAS_FILE, index=False)
        self.mostrar_ventas()
        messagebox.showinfo("Venta eliminada", "Venta eliminada correctamente.")

    def ver_boleta(self):
        sel = self.tree.selection()
        if not sel: return
        id_venta = self.tree.item(sel[0])["values"][0]
        boleta_path = os.path.join(REPORTES_DIR, f"boleta_{id_venta}.pdf")
        df = pd.read_excel(VENTAS_FILE)
        row = df[df["ID Venta"] == id_venta]
        if row.empty: return
        generar_boleta_pdf(row.iloc[0], boleta_path)
        try:
            if os.name == "nt": os.startfile(boleta_path)
            elif os.name == "posix": subprocess.Popen(["xdg-open", boleta_path])
        except Exception as e: messagebox.showerror("Error", f"No se pudo abrir el PDF: {e}")

# CLASE VentaToplevel (Solo una versión, la correcta)
class VentaToplevel(tk.Toplevel):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.title("Registrar Venta")
        self.geometry("420x420")
        self.resizable(False, False)
        self.parent = parent
        self.usuario = usuario
        self.config(bg="white")
        tk.Label(self, text="Registrar Venta", font=("Arial", 16), bg="white", fg="#256d85").pack(pady=10)
        campos = [("Cliente", ""), ("Cantidad", "1")]
        self.entries = {}
        for label, default in campos:
            f = tk.Frame(self, bg="white"); f.pack(pady=5)
            tk.Label(f, text=label+":", bg="white").pack(side="left")
            e = tk.Entry(f); e.insert(0, default); e.pack(side="left")
            self.entries[label] = e
        fprod = tk.Frame(self, bg="white"); fprod.pack(pady=5)
        tk.Label(fprod, text="Producto:", bg="white").pack(side="left")
        self.producto_var = tk.StringVar()
        self.productos = pd.read_excel(PRODUCTOS_FILE)
        self.producto_cb = ttk.Combobox(fprod, textvariable=self.producto_var, values=self.productos["Nombre"].tolist(), state="readonly")
        self.producto_cb.pack(side="left")
        fpago = tk.Frame(self, bg="white"); fpago.pack(pady=5)
        tk.Label(fpago, text="Tipo Pago:", bg="white").pack(side="left")
        self.pago_var = tk.StringVar(value="Efectivo")
        self.pago_cb = ttk.Combobox(fpago, textvariable=self.pago_var, values=["Efectivo", "Tarjeta", "Yape", "Plin"], state="readonly")
        self.pago_cb.pack(side="left")
        bframe = tk.Frame(self, bg="white"); bframe.pack(pady=20)
        boton_grande(bframe, "Registrar", "#2ecc71", self.guardar, "💾").pack(side="left", padx=5)
        boton_grande(bframe, "Cancelar", "#e74c3c", self.destroy, "❌").pack(side="left", padx=5)

    def guardar(self):
        cliente = self.entries["Cliente"].get().strip() or "Cliente Varios"
        try: cantidad = int(self.entries["Cantidad"].get())
        except: messagebox.showerror("Error", "Cantidad inválida", parent=self); return
        producto = self.producto_var.get()
        if not producto: messagebox.showerror("Error", "Debes elegir un producto", parent=self); return
        tipo_pago = self.pago_var.get()
        productos_df = pd.read_excel(PRODUCTOS_FILE)
        ventas_df = pd.read_excel(VENTAS_FILE)
        prod_row = productos_df[productos_df["Nombre"] == producto]
        if prod_row.empty: messagebox.showerror("Error", "Producto no encontrado", parent=self); return
        idx = prod_row.index[0]
        if productos_df.at[idx, "Stock"] < cantidad: messagebox.showerror("Error", "Stock insuficiente", parent=self); return
        
        productos_df.at[idx, "Stock"] -= cantidad
        productos_df.to_excel(PRODUCTOS_FILE, index=False)
        precio_unit = prod_row["Precio"].values[0]
        total = precio_unit * cantidad
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        id_venta = generar_id("V")
        nueva_venta = {"ID Venta":id_venta, "Fecha":fecha, "Cliente":cliente, "Producto":producto, "Cantidad":cantidad, "Precio Unitario":precio_unit, "Total":total, "Tipo Pago":tipo_pago, "Vendedor":self.usuario["Nombre"]}
        ventas_df = pd.concat([ventas_df, pd.DataFrame([nueva_venta])], ignore_index=True)
        ventas_df.to_excel(VENTAS_FILE, index=False)
        generar_boleta_pdf(nueva_venta, os.path.join(REPORTES_DIR, f"boleta_{id_venta}.pdf"))
        messagebox.showinfo("Venta Registrada", "Venta registrada con éxito y boleta generada.", parent=self)
        self.parent.mostrar_ventas()
        self.destroy()

# ----------- DESPACHO / RESERVAS -------------
class DespachoFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)
        tk.Label(self, text="Despacho / Reservas", font=("Arial", 22, "bold"), bg="white", fg="#256d85").pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("ID", "Fecha Reserva", "Cliente", "Producto", "Cantidad", "Estado", "Fecha Entrega"), show="headings")
        for col in self.tree["columns"]:
            ancho = 120
            if col == "Producto": ancho = 180
            if col == "Cliente": ancho = 150
            if "Fecha" in col: ancho = 130
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=30, pady=10)
        boton_frame = tk.Frame(self, bg="white")
        boton_frame.pack(pady=10)
        boton_grande(boton_frame, "Registrar Reserva", "#2ecc71", self.registrar_reserva, "➕").pack(side="left", padx=5)
        boton_grande(boton_frame, "Marcar Entregado", "#27ae60", self.marcar_entregado, "✅").pack(side="left", padx=5)
        boton_grande(boton_frame, "Marcar No Entregado", "#e67e22", self.marcar_no_entregado, "❌").pack(side="left", padx=5)
        boton_grande(boton_frame, "Refrescar", "#2980b9", self.mostrar_despachos, "🔃").pack(side="left", padx=5)
        self.mostrar_despachos()

    def mostrar_despachos(self):
        self.tree.delete(*self.tree.get_children())
        try: df = pd.read_excel(DESPACHO_FILE)
        except: return
        for _, row in df.iterrows():
            values = (row["ID"], row["Fecha Reserva"], row["Cliente"], row["Producto"], int(row["Cantidad"]) if not pd.isna(row["Cantidad"]) else "", row["Estado"], row["Fecha Entrega"] if not pd.isna(row["Fecha Entrega"]) else "")
            self.tree.insert("", "end", values=values)

    def registrar_reserva(self): ReservaToplevel(self)
    def marcar_entregado(self): self._marcar_estado("Entregado")
    def marcar_no_entregado(self): self._marcar_estado("No entregado")
    def _marcar_estado(self, estado):
        sel = self.tree.selection()
        if not sel: return
        id_reserva = self.tree.item(sel[0])["values"][0]
        df = pd.read_excel(DESPACHO_FILE)
        idx_list = df.index[df["ID"] == id_reserva].tolist()
        if not idx_list: return
        idx = idx_list[0]
        df.loc[idx, "Estado"] = estado
        df.loc[idx, "Fecha Entrega"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if estado == "Entregado":
            producto, cantidad = df.loc[idx, "Producto"], int(df.loc[idx, "Cantidad"])
            productos_df = pd.read_excel(PRODUCTOS_FILE)
            prod_idx_list = productos_df.index[productos_df["Nombre"] == producto].tolist()
            if prod_idx_list:
                prod_idx = prod_idx_list[0]
                if productos_df.loc[prod_idx, "Stock"] >= cantidad:
                    productos_df.loc[prod_idx, "Stock"] -= cantidad
                    productos_df.to_excel(PRODUCTOS_FILE, index=False)
                else: messagebox.showwarning("Stock insuficiente", f"El stock de '{producto}' es insuficiente.")
        df.to_excel(DESPACHO_FILE, index=False)
        self.mostrar_despachos()
        messagebox.showinfo("Estado actualizado", f"Reserva marcada como {estado}.")

class ReservaToplevel(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Reserva"); self.geometry("400x350"); self.resizable(False, False)
        self.parent = parent; self.config(bg="white")
        tk.Label(self, text="Registrar Reserva", font=("Arial", 16), bg="white", fg="#256d85").pack(pady=10)
        self.entries = {}
        for label, default in [("Cliente", ""), ("Cantidad", "1")]:
            f = tk.Frame(self, bg="white"); f.pack(pady=5)
            tk.Label(f, text=label+":", bg="white").pack(side="left")
            e = tk.Entry(f); e.insert(0, default); e.pack(side="left")
            self.entries[label] = e
        fprod = tk.Frame(self, bg="white"); fprod.pack(pady=5)
        tk.Label(fprod, text="Producto:", bg="white").pack(side="left")
        self.producto_var = tk.StringVar()
        try: nombres = pd.read_excel(PRODUCTOS_FILE)["Nombre"].tolist()
        except: nombres = []
        self.producto_cb = ttk.Combobox(fprod, textvariable=self.producto_var, values=nombres, state="readonly")
        self.producto_cb.pack(side="left")
        bframe = tk.Frame(self, bg="white"); bframe.pack(pady=20)
        boton_grande(bframe, "Guardar Reserva", "#2ecc71", self.guardar, "💾").pack(side="left", padx=5)
        boton_grande(bframe, "Cancelar", "#e74c3c", self.destroy, "❌").pack(side="left", padx=5)

    def guardar(self):
        cliente, producto = self.entries["Cliente"].get().strip(), self.producto_var.get()
        try: cantidad = int(self.entries["Cantidad"].get())
        except: messagebox.showerror("Error", "Cantidad inválida.", parent=self); return
        if not producto or not cliente: messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=self); return
        id_reserva = generar_id("R")
        fecha_reserva = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        fila = {"ID": id_reserva, "Fecha Reserva": fecha_reserva, "Cliente": cliente, "Producto": producto, "Cantidad": cantidad, "Estado": "Pendiente", "Fecha Entrega": ""}
        df = pd.read_excel(DESPACHO_FILE)
        df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
        df.to_excel(DESPACHO_FILE, index=False)
        messagebox.showinfo("Éxito", "Reserva registrada.", parent=self)
        self.parent.mostrar_despachos()
        self.destroy()

# ----------- EMPLEADOS -------------
class EmpleadosFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)
        tk.Label(self, text="Empleados", font=("Arial", 22, "bold"), bg="white", fg="#256d85").pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("Usuario", "Nombre", "Cargo", "Horario", "Funciones"), show="headings")
        for col in self.tree["columns"]:
            ancho = 120
            if col == "Nombre": ancho = 180
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=30, pady=10)
        boton_frame = tk.Frame(self, bg="white"); boton_frame.pack(pady=10)
        boton_grande(boton_frame, "Agregar Empleado", "#2ecc71", self.agregar_empleado, "➕").pack(side="left", padx=5)
        boton_grande(boton_frame, "Eliminar Empleado", "#e74c3c", self.eliminar_empleado, "🗑️").pack(side="left", padx=5)
        boton_grande(boton_frame, "Refrescar", "#2980b9", self.mostrar_empleados, "🔃").pack(side="left", padx=5)
        self.mostrar_empleados()

    def mostrar_empleados(self):
        self.tree.delete(*self.tree.get_children())
        try: df = pd.read_excel(EMPLEADOS_FILE)
        except: return
        for _, row in df.iterrows(): self.tree.insert("", "end", values=(row["Usuario"], row["Nombre"], row["Cargo"], row["Horario"], row["Funciones"]))
    def agregar_empleado(self): EmpleadoToplevel(self)
    def eliminar_empleado(self):
        sel = self.tree.selection()
        if not sel: return
        usuario = self.tree.item(sel[0])["values"][0]
        if usuario == "admin": messagebox.showwarning("Acción no permitida", "No puedes eliminar al administrador."); return
        df = pd.read_excel(EMPLEADOS_FILE)
        df = df[df["Usuario"] != usuario]
        df.to_excel(EMPLEADOS_FILE, index=False)
        self.mostrar_empleados()
        messagebox.showinfo("Empleado eliminado", "Empleado eliminado correctamente.")

class EmpleadoToplevel(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Agregar Empleado"); self.geometry("420x370"); self.resizable(False, False); self.parent = parent
        self.config(bg="white"); tk.Label(self, text="Agregar Empleado", font=("Arial", 16), bg="white", fg="#256d85").pack(pady=10)
        self.entries = {}
        for label, default in [("Usuario", ""), ("Contraseña", ""), ("Nombre", ""), ("Cargo", ""), ("Horario", "08:00-20:00"), ("Funciones", "ventas")]:
            f = tk.Frame(self, bg="white"); f.pack(pady=5)
            tk.Label(f, text=label+":", bg="white").pack(side="left")
            e = tk.Entry(f); e.insert(0, default); e.pack(side="left")
            self.entries[label] = e
        bframe = tk.Frame(self, bg="white"); bframe.pack(pady=20)
        boton_grande(bframe, "Guardar", "#2ecc71", self.guardar, "💾").pack(side="left", padx=5)
        boton_grande(bframe, "Cancelar", "#e74c3c", self.destroy, "❌").pack(side="left", padx=5)

    def guardar(self):
        fila = [self.entries[label].get().strip() for label in ["Usuario", "Contraseña", "Nombre", "Cargo", "Horario", "Funciones"]]
        if any(not val for val in fila): messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=self); return
        df = pd.read_excel(EMPLEADOS_FILE)
        if fila[0] in df["Usuario"].values: messagebox.showerror("Error", "Ese usuario ya existe.", parent=self); return
        df.loc[len(df)] = fila
        df.to_excel(EMPLEADOS_FILE, index=False)
        messagebox.showinfo("Éxito", "Empleado registrado.", parent=self)
        self.parent.mostrar_empleados(); self.destroy()

# ----------- CATEGORIAS -------------
class CategoriaFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)
        tk.Label(self, text="Categorías", font=("Arial", 22, "bold"), bg="white", fg="#256d85").pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre"), show="headings")
        for col in self.tree["columns"]:
            ancho = 130 if col == "Nombre" else 80
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=30, pady=10)
        boton_frame = tk.Frame(self, bg="white"); boton_frame.pack(pady=10)
        boton_grande(boton_frame, "Agregar Categoría", "#2ecc71", self.agregar_categoria, "➕").pack(side="left", padx=5)
        boton_grande(boton_frame, "Eliminar Categoría", "#e74c3c", self.eliminar_categoria, "🗑️").pack(side="left", padx=5)
        boton_grande(boton_frame, "Refrescar", "#2980b9", self.mostrar_categorias, "🔃").pack(side="left", padx=5)
        self.mostrar_categorias()

    def mostrar_categorias(self):
        self.tree.delete(*self.tree.get_children())
        try: df = pd.read_excel(CATEGORIAS_FILE)
        except: return
        for _, row in df.iterrows(): self.tree.insert("", "end", values=(row["ID"], row["Nombre"]))
    def agregar_categoria(self):
        nombre = simpledialog.askstring("Nueva Categoría", "Nombre de la categoría:", parent=self)
        if not nombre: return
        df = pd.read_excel(CATEGORIAS_FILE)
        if nombre in df["Nombre"].values: messagebox.showerror("Error", "Esa categoría ya existe.", parent=self); return
        nuevo_id = f"C{len(df)+1:03d}"
        df.loc[len(df)] = [nuevo_id, nombre]
        df.to_excel(CATEGORIAS_FILE, index=False)
        self.mostrar_categorias()
        messagebox.showinfo("Éxito", "Categoría agregada correctamente.", parent=self)
    def eliminar_categoria(self):
        sel = self.tree.selection()
        if not sel: return
        nombre = self.tree.item(sel[0])["values"][1]
        df = pd.read_excel(CATEGORIAS_FILE)
        df = df[df["Nombre"] != nombre]
        df.to_excel(CATEGORIAS_FILE, index=False)
        self.mostrar_categorias()
        messagebox.showinfo("Categoría eliminada", "Categoría eliminada correctamente.", parent=self)

# ----------- COMPRAS -------------
class ComprasFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)
        tk.Label(self, text="Compras", font=("Arial", 22, "bold"), bg="white", fg="#256d85").pack(pady=10)
        self.tree = ttk.Treeview(self, columns=("ID Compra", "Fecha", "Proveedor", "Producto", "Cantidad", "Estado"), show="headings")
        for col in self.tree["columns"]:
            ancho = 120
            if col == "Producto": ancho = 180
            if col == "Proveedor": ancho = 150
            if col == "Fecha": ancho = 120
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=30, pady=10)
        boton_frame = tk.Frame(self, bg="white"); boton_frame.pack(pady=10)
        boton_grande(boton_frame, "Registrar Compra", "#2ecc71", self.registrar_compra, "➕").pack(side="left", padx=5)
        boton_grande(boton_frame, "Eliminar Compra", "#e74c3c", self.eliminar_compra, "🗑️").pack(side="left", padx=5)
        boton_grande(boton_frame, "Refrescar", "#2980b9", self.mostrar_compras, "🔃").pack(side="left", padx=5)
        boton_grande(boton_frame, "Marcar Completada", "#16a085", self.marcar_completada, "✅").pack(side="left", padx=5)
        boton_grande(boton_frame, "Marcar Cancelada", "#8e44ad", self.marcar_cancelada, "❌").pack(side="left", padx=5)
        self.mostrar_compras()

    def mostrar_compras(self):
        self.tree.delete(*self.tree.get_children())
        try: df = pd.read_excel(COMPRAS_FILE)
        except: return
        for _, row in df.iterrows(): self.tree.insert("", "end", values=(row["ID Compra"], row["Fecha"], row["Proveedor"], row["Producto"], int(row["Cantidad"]) if not pd.isna(row["Cantidad"]) else "", row["Estado"]))
    def registrar_compra(self): CompraToplevel(self)
    def eliminar_compra(self):
        sel = self.tree.selection()
        if not sel: return
        id_compra = self.tree.item(sel[0])["values"][0]
        df = pd.read_excel(COMPRAS_FILE)
        df = df[df["ID Compra"] != id_compra]
        df.to_excel(COMPRAS_FILE, index=False)
        self.mostrar_compras()
        messagebox.showinfo("Compra eliminada", "Compra eliminada correctamente.")
    def marcar_completada(self):
        sel = self.tree.selection()
        if not sel: return
        id_compra = self.tree.item(sel[0])["values"][0]
        self._actualizar_estado_compra(id_compra, "Recibido")
    def marcar_cancelada(self):
        sel = self.tree.selection()
        if not sel: return
        id_compra = self.tree.item(sel[0])["values"][0]
        self._actualizar_estado_compra(id_compra, "Cancelada")
    def _actualizar_estado_compra(self, id_compra, nuevo_estado):
        df = pd.read_excel(COMPRAS_FILE)
        idx_list = df.index[df["ID Compra"] == id_compra].tolist()
        if not idx_list: return
        idx = idx_list[0]
        if nuevo_estado == "Recibido":
            producto, cantidad = df.loc[idx, "Producto"], int(df.loc[idx, "Cantidad"])
            productos_df = pd.read_excel(PRODUCTOS_FILE)
            prod_idx_list = productos_df.index[productos_df["Nombre"] == producto].tolist()
            if prod_idx_list:
                prod_idx = prod_idx_list[0]
                productos_df.loc[prod_idx, "Stock"] += cantidad
                productos_df.to_excel(PRODUCTOS_FILE, index=False)
        df.loc[idx, "Estado"] = nuevo_estado
        df.to_excel(COMPRAS_FILE, index=False)
        self.mostrar_compras()
        messagebox.showinfo("Estado actualizado", f"Compra marcada como {nuevo_estado}.")

class CompraToplevel(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Compra"); self.geometry("400x340"); self.resizable(False, False)
        self.parent = parent; self.config(bg="white")
        tk.Label(self, text="Registrar Compra", font=("Arial", 16), bg="white", fg="#256d85").pack(pady=10)
        self.entries = {}
        for label, default in [("Proveedor", ""), ("Cantidad", "1")]:
            f = tk.Frame(self, bg="white"); f.pack(pady=5)
            tk.Label(f, text=label+":", bg="white").pack(side="left")
            e = tk.Entry(f); e.insert(0, default); e.pack(side="left")
            self.entries[label] = e
        fprod = tk.Frame(self, bg="white"); fprod.pack(pady=5)
        tk.Label(fprod, text="Producto:", bg="white").pack(side="left")
        self.producto_var = tk.StringVar()
        try: nombres = pd.read_excel(PRODUCTOS_FILE)["Nombre"].tolist()
        except: nombres = []
        self.producto_cb = ttk.Combobox(fprod, textvariable=self.producto_var, values=nombres, state="readonly")
        self.producto_cb.pack(side="left")
        festado = tk.Frame(self, bg="white"); festado.pack(pady=5)
        tk.Label(festado, text="Estado:", bg="white").pack(side="left")
        self.estado_var = tk.StringVar(value="Pendiente")
        self.estado_cb = ttk.Combobox(festado, textvariable=self.estado_var, values=["Pendiente", "Recibido"], state="readonly")
        self.estado_cb.pack(side="left")
        bframe = tk.Frame(self, bg="white"); bframe.pack(pady=20)
        boton_grande(bframe, "Registrar", "#2ecc71", self.guardar, "💾").pack(side="left", padx=5)
        boton_grande(bframe, "Cancelar", "#e74c3c", self.destroy, "❌").pack(side="left", padx=5)

    def guardar(self):
        proveedor = self.entries["Proveedor"].get().strip()
        try: cantidad = int(self.entries["Cantidad"].get())
        except: messagebox.showerror("Error", "Cantidad inválida.", parent=self); return
        producto = self.producto_var.get()
        if not producto or not proveedor: messagebox.showerror("Error", "Todos los campos son obligatorios", parent=self); return
        estado = self.estado_var.get()
        if estado == "Recibido":
            productos_df = pd.read_excel(PRODUCTOS_FILE)
            prod_row = productos_df[productos_df["Nombre"] == producto]
            if not prod_row.empty:
                idx = prod_row.index[0]
                productos_df.loc[idx, "Stock"] += cantidad
                productos_df.to_excel(PRODUCTOS_FILE, index=False)
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        id_compra = generar_id("C")
        fila = {"ID Compra":id_compra, "Fecha":fecha, "Proveedor":proveedor, "Producto":producto, "Cantidad":cantidad, "Estado":estado}
        compras_df = pd.read_excel(COMPRAS_FILE)
        compras_df = pd.concat([compras_df, pd.DataFrame([fila])], ignore_index=True)
        compras_df.to_excel(COMPRAS_FILE, index=False)
        messagebox.showinfo("Éxito", "Compra registrada.", parent=self)
        self.parent.mostrar_compras(); self.destroy()

# ----------- REPORTES -------------
class ReportesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)
        tk.Label(self, text="Reportes", font=("Arial", 22, "bold"), bg="white", fg="#256d85").pack(pady=10)
        boton_frame = tk.Frame(self, bg="white"); boton_frame.pack(pady=10)
        boton_grande(boton_frame, "Ventas por producto", "#2980b9", self.reporte_ventas_producto, "📊").pack(side="left", padx=5)
        boton_grande(boton_frame, "Ganancias por producto", "#27ae60", self.reporte_ganancias_producto, "💰").pack(side="left", padx=5)
        boton_grande(boton_frame, "Más/Menos vendidos", "#8e44ad", self.reporte_mas_menos_vendidos, "🏆").pack(side="left", padx=5)
        self.tabla_frame = tk.Frame(self, bg="white"); self.tabla_frame.pack(fill="x", padx=10, pady=(10, 0))
        self.grafico_frame = tk.Frame(self, bg="white"); self.grafico_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def limpiar_canvas(self):
        for widget in self.tabla_frame.winfo_children(): widget.destroy()
        for widget in self.grafico_frame.winfo_children(): widget.destroy()

    def reporte_ventas_producto(self):
        self.limpiar_canvas()
        try: ventas = pd.read_excel(VENTAS_FILE)
        except: messagebox.showinfo("Sin datos", "No hay ventas registradas."); return
        if ventas.empty: messagebox.showinfo("Sin datos", "No hay ventas registradas."); return
        df = ventas.groupby("Producto")["Cantidad"].sum().reset_index().sort_values("Cantidad", ascending=False)
        tree = ttk.Treeview(self.tabla_frame, columns=("Producto", "Cantidad"), show="headings", height=min(15, len(df)))
        tree.heading("Producto", text="Producto"); tree.heading("Cantidad", text="Cantidad Vendida")
        tree.column("Producto", width=500, anchor="w"); tree.column("Cantidad", width=120, anchor="center")
        for _, row in df.iterrows(): tree.insert("", "end", values=(row["Producto"], row["Cantidad"]))
        tree.pack(fill="x", pady=2)
        fig, ax = plt.subplots(figsize=(14, 5)); df.set_index("Producto")["Cantidad"].plot(kind="bar", ax=ax)
        ax.set_ylabel("Cantidad vendida"); ax.set_title("Ventas por producto")
        ax.set_xticklabels(df["Producto"], rotation=30, ha='right', fontsize=10, wrap=True); fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame); canvas.get_tk_widget().pack(fill="both", expand=True); canvas.draw()

    def reporte_ganancias_producto(self):
        self.limpiar_canvas()
        try: ventas = pd.read_excel(VENTAS_FILE)
        except: messagebox.showinfo("Sin datos", "No hay ventas registradas."); return
        if ventas.empty: messagebox.showinfo("Sin datos", "No hay ventas registradas."); return
        ventas["Ganancia"] = ventas["Cantidad"] * ventas["Precio Unitario"]
        df = ventas.groupby("Producto")["Ganancia"].sum().reset_index().sort_values("Ganancia", ascending=False)
        tree = ttk.Treeview(self.tabla_frame, columns=("Producto", "Ganancia"), show="headings", height=min(15, len(df)))
        tree.heading("Producto", text="Producto"); tree.heading("Ganancia", text="Ganancia (S/)")
        tree.column("Producto", width=500, anchor="w"); tree.column("Ganancia", width=150, anchor="center")
        for _, row in df.iterrows(): tree.insert("", "end", values=(row["Producto"], f"{row['Ganancia']:.2f}"))
        tree.pack(fill="x", pady=2)
        fig, ax = plt.subplots(figsize=(14, 5)); df.set_index("Producto")["Ganancia"].plot(kind="bar", ax=ax, color="#27ae60")
        ax.set_ylabel("Ganancia total"); ax.set_title("Ganancias por producto")
        ax.set_xticklabels(df["Producto"], rotation=30, ha='right', fontsize=10, wrap=True); fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame); canvas.get_tk_widget().pack(fill="both", expand=True); canvas.draw()

    def reporte_mas_menos_vendidos(self):
        self.limpiar_canvas()
        try: ventas = pd.read_excel(VENTAS_FILE)
        except: messagebox.showinfo("Sin datos", "No hay ventas registradas."); return
        if ventas.empty: messagebox.showinfo("Sin datos", "No hay ventas registradas."); return
        df = ventas.groupby("Producto")["Cantidad"].sum().reset_index().sort_values("Cantidad", ascending=False)
        N = min(5, len(df))
        if N == 0: messagebox.showinfo("Sin datos", "No hay suficientes productos vendidos para este reporte."); return
        tabla_inner = tk.Frame(self.tabla_frame, bg="white"); tabla_inner.pack(fill="x")
        tk.Label(tabla_inner, text="Top 5 más vendidos", font=("Arial", 12, "bold"), bg="white").pack(side="left", padx=10)
        tk.Label(tabla_inner, text="Top 5 menos vendidos", font=("Arial", 12, "bold"), bg="white").pack(side="right", padx=10)
        tree1 = ttk.Treeview(self.tabla_frame, columns=("Producto", "Cantidad"), show="headings", height=N); tree1.heading("Producto", text="Producto"); tree1.heading("Cantidad", text="Cantidad"); tree1.column("Producto", width=350, anchor="w"); tree1.column("Cantidad", width=100, anchor="center")
        for _, row in df.head(N).iterrows(): tree1.insert("", "end", values=(row["Producto"], row["Cantidad"]))
        tree1.pack(side="left", fill="x", expand=True, padx=(0, 20))
        tree2 = ttk.Treeview(self.tabla_frame, columns=("Producto", "Cantidad"), show="headings", height=N); tree2.heading("Producto", text="Producto"); tree2.heading("Cantidad", text="Cantidad"); tree2.column("Producto", width=350, anchor="w"); tree2.column("Cantidad", width=100, anchor="center")
        for _, row in df.tail(N).iterrows(): tree2.insert("", "end", values=(row["Producto"], row["Cantidad"]))
        tree2.pack(side="left", fill="x", expand=True)
        fig, ax = plt.subplots(1, 2, figsize=(14, 5)); df.head(N).set_index("Producto")["Cantidad"].plot(kind="bar", ax=ax[0], color="#2ecc71")
        ax[0].set_title("Top productos más vendidos"); ax[0].set_ylabel("Cantidad"); ax[0].set_xticklabels(df.head(N)["Producto"], rotation=30, ha='right', fontsize=10, wrap=True)
        df.tail(N).set_index("Producto")["Cantidad"].plot(kind="bar", ax=ax[1], color="#e74c3c")
        ax[1].set_title("Top productos menos vendidos"); ax[1].set_ylabel("Cantidad"); ax[1].set_xticklabels(df.tail(N)["Producto"], rotation=30, ha='right', fontsize=10, wrap=True)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame); canvas.get_tk_widget().pack(fill="both", expand=True); canvas.draw()

# ----------- MAIN -------------
if __name__ == "__main__":
    asegurarse_archivos()
    login = LoginVentana()
    login.mainloop()
    if login.resultado is not None:
        app = Dashboard(login.resultado)
        app.mainloop()