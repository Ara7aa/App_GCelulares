from config import conectar_db
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END, messagebox

# Crear Repuesto
def crear_repuesto():
    try:
        id_celular = int(entry_id_celular.get())
        descripcion = entry_descripcion.get()
        costo = float(entry_costo.get())
        if id_celular and descripcion and costo >= 0:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO repuestos (id_celular, descripcion, costo) VALUES (%s, %s, %s)", (id_celular, descripcion, costo))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Repuesto agregado exitosamente.")
            entry_id_celular.delete(0, END)
            entry_descripcion.delete(0, END)
            entry_costo.delete(0, END)
            mostrar_repuestos()
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos correctamente.")
    except ValueError:
        messagebox.showerror("Error", "El ID del celular debe ser un número entero y el costo un valor numérico.")

# Leer Repuestos
def obtener_repuestos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT repuestos.id_repuesto, repuestos.id_celular, repuestos.descripcion, repuestos.costo
        FROM repuestos
        JOIN celulares ON repuestos.id_celular = celulares.id_celular
    """)
    repuestos = cursor.fetchall()
    conn.close()
    return repuestos

# Mostrar Repuestos en Listbox
def mostrar_repuestos():
    lista_repuestos.delete(0, END)
    for repuesto in obtener_repuestos():
        lista_repuestos.insert(END, f"{repuesto[0]} - {repuesto[1]} - {repuesto[2]} - {repuesto[3]}")

# Actualizar Repuesto
def actualizar_repuesto():
    try:
        id_repuesto = int(entry_id_repuesto.get())
        descripcion = entry_descripcion.get()
        costo = float(entry_costo.get())
        if descripcion and costo >= 0:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE repuestos SET descripcion=%s, costo=%s WHERE id_repuesto=%s", (descripcion, costo, id_repuesto))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Repuesto actualizado exitosamente.")
            entry_id_repuesto.delete(0, END)
            entry_id_celular.delete(0, END)
            entry_descripcion.delete(0, END)
            entry_costo.delete(0, END)
            mostrar_repuestos()
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos correctamente.")
    except ValueError:
        messagebox.showerror("Error", "El ID del repuesto debe ser un número entero y el costo un valor numérico.")

# Eliminar Repuesto
def eliminar_repuesto():
    try:
        id_repuesto = int(entry_id_repuesto.get())
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM repuestos WHERE id_repuesto=%s", (id_repuesto,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Repuesto eliminado exitosamente.")
        entry_id_repuesto.delete(0, END)
        entry_id_celular.delete(0, END)
        entry_descripcion.delete(0, END)
        entry_costo.delete(0, END)
        mostrar_repuestos()
    except ValueError:
        messagebox.showerror("Error", "Por favor, selecciona un repuesto válido.")

# Función para manejar la selección en la lista
def seleccionar_repuesto(event):
    seleccion = lista_repuestos.get(lista_repuestos.curselection())
    id_repuesto, id_celular, descripcion, costo = seleccion.split(" - ")
    entry_id_repuesto.delete(0, END)
    entry_id_repuesto.insert(END, id_repuesto)
    entry_id_celular.delete(0, END)
    entry_id_celular.insert(END, id_celular)
    entry_descripcion.delete(0, END)
    entry_descripcion.insert(END, descripcion)
    entry_costo.delete(0, END)
    entry_costo.insert(END, costo)

# Configuración de la ventana principal
root = Tk()
root.title("Gestión de Repuestos")
root.geometry("500x500")

# Widgets para el CRUD de Repuestos
Label(root, text="ID Repuesto").pack()
entry_id_repuesto = Entry(root)
entry_id_repuesto.pack()

Label(root, text="ID Celular").pack()
entry_id_celular = Entry(root)
entry_id_celular.pack()

Label(root, text="Descripción").pack()
entry_descripcion = Entry(root)
entry_descripcion.pack()

Label(root, text="Costo").pack()
entry_costo = Entry(root)
entry_costo.pack()

# Botones de acción
Button(root, text="Agregar Repuesto", command=crear_repuesto).pack(pady=5)
Button(root, text="Actualizar Repuesto", command=actualizar_repuesto).pack(pady=5)
Button(root, text="Eliminar Repuesto", command=eliminar_repuesto).pack(pady=5)

# Listbox para mostrar repuestos
lista_repuestos = Listbox(root, width=60)
lista_repuestos.pack(pady=10)

# Scrollbar para Listbox
scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")
lista_repuestos.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lista_repuestos.yview)

# Cargar lista de repuestos y manejar selección
lista_repuestos.bind("<<ListboxSelect>>", seleccionar_repuesto)
mostrar_repuestos()

# Iniciar el loop de Tkinter
root.mainloop()