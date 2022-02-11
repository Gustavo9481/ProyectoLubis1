from tkinter import*
from tkinter import messagebox
import sqlite3


root=Tk()
root.title("Lubi's Huevos")
ancho_ventana=400
alto_ventana=560
root.config(bg="#FFF212")
root.rowconfigure(1, weight=1)
root.columnconfigure(1, weight=1)
x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)



reg=[]


#---------- FUNCIONES
#----- MENU BBDD
#--- CREAR
def newBBDD():
    crear=messagebox.askquestion("Lubi's Huevos", "Desea crear una nueva Base de Datos?")
    if crear=="yes":
        conexion=sqlite3.connect("LubisHuevos")
        puntero=conexion.cursor()
        puntero.execute('''
            CREATE TABLE CLIENTES(
            ID_CLIENTE INTEGER PRIMARY KEY AUTOINCREMENT,  
            NOMBRE VARCHAR(50),
            PASSWORD VARCHAR(20),
            TELEFONO VARCHAR(20),
            COMENTARIOS VARCHAR(150))
        ''')
        messagebox.showinfo("Lubi's Huevos", "Se ha creado una Nueva Base de Datos\nBBDD LubisHuevos")

        conexion.commit()
        conexion.close()
#--- SALIR
def salida():
    respuesta= messagebox.askquestion("Lubi's Huevos", "Desea salir de la aplicación?")
    if respuesta=="yes":
        root.destroy()

#----- MENU Editar
def limpiar():
    obj3.delete(0,END)
    obj4.delete(0,END)
    obj5.delete(0,END)
    obj6.delete(0,END)
    obj7.delete("1.0",END) 
    

#----- MENU CRUD
#--- NUEVO
def newRegistro():
    global reg
    conexion=sqlite3.connect("LubisHuevos")
    puntero=conexion.cursor()
    reg=[(obj4.get(),obj5.get(),obj6.get(),obj7.get("1.0", END))]
    puntero.executemany("INSERT INTO CLIENTES VALUES (NULL,?,?,?,?)",reg)
    messagebox.showinfo("Lubi's Huevos", "Se ha creado un nuevo registro")
    limpiar()
    conexion.commit()
    conexion.close()

#--- CONSULTAR

def consulta2():
    conexion=sqlite3.connect("LubisHuevos")
    puntero=conexion.cursor()
    puntero.execute("SELECT * FROM CLIENTES WHERE ID_CLIENTE="+obj3.get())
    cons=puntero.fetchall()
    for i in cons:
        identificacion.set(i[0])
        nombreCliente.set(i[1])
        contraseña.set(i[2])
        contacto.set(i[3])
        obj7.insert(1.0,i[4])
    conexion.commit()
    conexion.close()


#--- ACTUALIZAR 
def actual():
    conexion=sqlite3.connect("LubisHuevos")
    puntero=conexion.cursor()
    reg=nombreCliente.get(),contraseña.get(),contacto.get(),obj7.get("1.0", END)
    puntero.execute("UPDATE CLIENTES SET NOMBRE=?, PASSWORD=?, TELEFONO=?, COMENTARIOS=?"+
        "WHERE ID_CLIENTE="+identificacion.get(),(reg))
    messagebox.showinfo("Lubi's Huevos", "Se ha actualizado el cliente")
    limpiar()
    conexion.commit()
    conexion.close()

#--- ELIMINAR
def elim():
    crear=messagebox.askquestion("Lubi's Huevos", "Desea eliminar el cliente?")
    if crear=="yes":
        conexion=sqlite3.connect("LubisHuevos")
        puntero=conexion.cursor()
        puntero.execute("DELETE FROM CLIENTES WHERE ID_CLIENTE="+ obj3.get())
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Lubi's Huevos", "Se ha eliminado el cliente")
        limpiar()

#----- MENU AYUDA
def ayudamenu():
    messagebox.showinfo("Lubi's Huevos", "Powered by Gustavo Colmenares  \nLicencia OpenSource")

#---------- MENU
BarraMenu = Menu(root)
root.config(menu=BarraMenu)

base = Menu(BarraMenu, tearoff=0) 
base.add_command(label="Conectar", command=newBBDD)
base.add_separator()            
base.add_command(label="Salir", command=salida)

edicion = Menu(BarraMenu, tearoff=0)
edicion.add_command(label="Borrar Campos", command=limpiar)


crud = Menu(BarraMenu, tearoff=0)
crud.add_command(label="Nuevo", command=newRegistro)
crud.add_command(label="Consultar", command=consulta2)
crud.add_command(label="Actualizar", command=actual)
crud.add_command(label="Eliminar", command=elim)

inf = Menu(BarraMenu, tearoff=0)
inf.add_command(label="Acerca de", command=ayudamenu)


BarraMenu.add_cascade(label="BBDD", menu=base)
BarraMenu.add_cascade(label="Borrar", menu=edicion)
BarraMenu.add_cascade(label="CRUD", menu=crud)
BarraMenu.add_cascade(label="Info", menu=inf)

#---------- VARIABLES DE TEXTOS
identificacion=StringVar()
nombreCliente=StringVar()
contraseña=StringVar()
contacto=StringVar()

#---------- LOGO
logo=PhotoImage(file="Lubis2.gif").subsample(3,3)
obj1=Label(root, image=logo, bd=0, bg="#FFF212")
obj1.grid(row=0, column=0, rowspan=2, columnspan=4, pady=5)

#---------- TITULO
obj2=Label(root, text="Registro de Clientes",bg="#FFF212", bd=0, font=(10))
obj2.grid(row=2, column=0, columnspan=4, sticky="nsew")

#---------- IDENTIFICACIÓN
ident=Label(root, text="ID (Número de Registro Cliente)",bg="#FFF212", width="25", anchor="e")
ident.grid(row=3, column=0, columnspan=2, pady=10, padx=5)
obj3=Entry(root, width="25", textvariable=identificacion)
obj3.grid(row=3, column=2, columnspan=2, pady=10, padx=5, sticky="w")

#---------- NOMBRE
nombre=Label(root, text="Nombre y Apellidos",bg="#FFF212", width="25", anchor="e")
nombre.grid(row=4, column=0, columnspan=2, pady=10)
obj4=Entry(root, width="25", textvariable=nombreCliente)
obj4.grid(row=4, column=2, columnspan=2, pady=10, padx=5, sticky="w")

#---------- PASSWORD
clave=Label(root, text="Password de acceso", bg="#FFF212", width="25", anchor="e")
clave.grid(row=5, column=0, columnspan=2, pady=10)
obj5=Entry(root, width="25", show="*", textvariable=contraseña)
obj5.grid(row=5, column=2, columnspan=2, pady=10, padx=5, sticky="w")

#---------- DIRECCION
direccion=Label(root, text="Teléfono de contacto",bg="#FFF212", width="25", anchor="e")
direccion.grid(row=6, column=0, columnspan=2, pady=10)
obj6=Entry(root, width="25", textvariable=contacto)
obj6.grid(row=6, column=2, columnspan=2, pady=10, padx=5, sticky="w")

#---------- COMENTARIOS
Comentarios=Label(root, text="Comentarios Adicionales",bg="#FFF212", width="25", anchor="e")
Comentarios.grid(row=7, column=0, columnspan=2, pady=10)
obj7=Text(root, width=17, height=3)
obj7.grid(row=7, column=2, columnspan=2, pady=10, padx=10, sticky="w")
scroll=Scrollbar(root,command=obj7.yview)
scroll.grid(row=7, column=3, sticky="nse", pady=11, padx=13)
obj7.config(yscrollcommand=scroll.set)


#---------- MENU BOTONES
bot1=Button(root, text="Nuevo",borderwidth=0, bg="#fff771", width=10, command=newRegistro)
bot1.grid(row=8, column=0, pady=10, padx=5)

bot2=Button(root, text="Consultar", borderwidth=0, bg="#fff771", width=10, command=consulta2)
bot2.grid(row=8, column=1, pady=10, padx=5)

bot3=Button(root, text="Actualizar", borderwidth=0, bg="#fff771", width=10, command=actual)
bot3.grid(row=8, column=2, pady=10, padx=5)

bot4=Button(root, text="Eliminar", borderwidth=0, bg="#fff771", width=10, activebackground="#FFF212", command=elim)
bot4.grid(row=8, column=3, pady=10, padx=5)


root.mainloop() 