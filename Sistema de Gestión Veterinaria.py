"""
----------------------------------------------------------------------------------------------
Título: Sistema de Gestión Veterinaria
Fecha: 31/05/2025
Autor: Grupo 6

Descripción:
Sistema de gestión para ingresar, modificar, eliminar y listar propietarios y mascotas,
asociar atenciones, calcular estadísticas mensuales/anuales, y generar informes.

Pendientes:
----------------------------------------------------------------------------------------------
"""

#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
import time
import random
import json
import re 

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------

def cargar_json(nombre_archivo):
    """
    Carga datos desde un archivo JSON.

    Parametros:
        nombre_archivo: La ruta y el nombre del archivo JSON a cargar.

    Retorno:
        Un diccionario con los datos del archivo, o un diccionario vacío si el archivo no existe.
    """
    try:
        f = open(nombre_archivo, mode="r", encoding="utf-8")
        datos = json.load(f)
        f.close()
        return datos
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print("Error al cargar JSON:", error)
        return {}

def guardar_json(nombre_archivo, datos):
    """
    Guarda un diccionario de datos en un archivo con formato JSON.

    Parametros:
        nombre_archivo: La ruta y el nombre del archivo donde se guardarán los datos.
        datos: El diccionario con los datos a guardar.
    """
    try:
        f = open(nombre_archivo, mode="w", encoding="utf-8")
        json.dump(datos, f, ensure_ascii=False, indent=4)
        f.close()
    except (FileNotFoundError, OSError) as error:
        print("Error al guardar JSON:", error)

def generar_id():
    """
    Genera un número entero aleatorio de 8 dígitos para usar como ID de nascota.

    Retorno:
        int: Un número aleatorio entre 10000000 y 99999999.
    """
    return random.randint(10000000, 99999999)

def validar_telefono(tel):
    """
    Valida que un string de teléfono contenga exactamente 10 dígitos numéricos.

    Parametros:
        tel: La cadena de texto del teléfono a validar.

    Retorno:
        True si el teléfono es válido, False en caso contrario.
    """
    return tel.isdigit() and len(tel) == 10

def validar_email(email):
    """
    Valida si un string tiene el formato de un correo electrónico válido.

    Parametros:
        email: La cadena de texto del email a validar.

    Retorno:
        True si el email tiene un formato válido, False en caso contrario.
    """
    pat = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pat, email) is not None

def contiene_numeros(texto):
    """
    Verifica si una cadena de texto contiene al menos un dígito numérico.

    Parametros:
        texto: La cadena de texto a verificar.

    Retorno:
        True si el texto contiene algún número, False si no los tiene.
    """
    return any(char.isdigit() for char in texto)

def ingresar_propietario():
    """
    Pide datos de un nuevo propietario y lo agrega al archivo 'propietarios.json'. Verifica que todos los datos sean correctos antes de continuar. 
    """
    try:
        propietarios = cargar_json("propietarios.json") #Carga los datos del archivo 'propietarios.json'
    except Exception as e:
        print("Error al cargar propietarios:", e)
        return
    
    dni = input("Ingrese DNI del propietario (8 dígitos): ")
    while len(dni) != 8 or not dni.isdigit() or dni in propietarios:
        print("DNI inválido o ya registrado.")
        dni = input("Ingrese DNI del propietario (8 dígitos): ")
    
    nombre = input("Nombre completo: ").strip()
    while not nombre or contiene_numeros(nombre):
        print("El nombre no puede estar vacío ni contener números.")
        nombre = input("Nombre completo: ").strip()

    direccion = input("Dirección: ").strip()
    
    email = input("Email: ").strip()
    while not validar_email(email):
        print("Email inválido.")
        email = input("Email: ").strip()
    
    tel1 = input("Teléfono principal (10 dígitos): ").strip()
    while not validar_telefono(tel1):
        print("Teléfono inválido.")
        tel1 = input("Teléfono principal (10 dígitos): ").strip()
    
    tel_emergencia = input("Teléfono de emergencia (10 dígitos): ").strip()
    while not validar_telefono(tel_emergencia):
        print("Teléfono inválido.")
        tel_emergencia = input("Teléfono de emergencia (10 dígitos): ").strip()
    
    #Agrega nuevo propietario a diccionario
    propietarios[dni] = {
        "activo": True,
        "nombre": nombre,
        "direccion": direccion,
        "email": email,
        "telefonos": {
            "principal": tel1,
            "emergencia": tel_emergencia
        }
    }
    print(f"Propietario {nombre} registrado con éxito.")

    guardar_json("propietarios.json", propietarios) #Guarda el nuevo propietario al archivo json
    return 

def modificar_propietario():
    """
    Permite cambiar datos de un propietario activo.
    """
    try:
        propietarios = cargar_json("propietarios.json") #Carga los datos del archivo 'propietarios.json'
    except Exception as e:
        print("Error al cargar propietarios:", e)
        return
    
    dni = input("Ingrese DNI del propietario a modificar (0 para cancelar): ") 
    if dni == "0":  #Utiliza 0 para salir sin modificar 
        return 

    if dni in propietarios and propietarios[dni]["activo"]:  #Verifica que el propietario a mofificar este activo en el sistema 
        print("\nDatos actuales:")
        print(f"Nombre: {propietarios[dni]['nombre']}")
        print(f"Dirección: {propietarios[dni]['direccion']}")
        print(f"Email: {propietarios[dni]['email']}")
        print(f"Teléfono: {propietarios[dni]['telefonos']['principal']}")
        print(f"Teléfono emergencia: {propietarios[dni]['telefonos']['emergencia']}")
        
        print("\nIngrese nuevos datos (dejar vacío para mantener el actual):") 
        
        #Vuelve a pedir todos los datos
        nombre = input(f"Nombre [{propietarios[dni]['nombre']}]: ").strip()
        while nombre and contiene_numeros(nombre):
            print("El nombre no puede contener números.")
            nombre = input(f"Nombre [{propietarios[dni]['nombre']}]: ").strip()
        if nombre:
            propietarios[dni]["nombre"] = nombre
        
        direccion = input(f"Dirección [{propietarios[dni]['direccion']}]: ").strip()
        if direccion:
            propietarios[dni]["direccion"] = direccion
        
        email = input(f"Email [{propietarios[dni]['email']}]: ").strip()
        if email and validar_email(email):
            propietarios[dni]["email"] = email
        
        tel1 = input(f"Teléfono principal [{propietarios[dni]['telefonos']['principal']}]: ").strip()
        if tel1 and validar_telefono(tel1):
            propietarios[dni]["telefonos"]["principal"] = tel1

        tel_emergencia = input(f"Teléfono emergencia [{propietarios[dni]['telefonos']['emergencia']}]: ").strip()
        if tel_emergencia and validar_telefono(tel_emergencia):
            propietarios[dni]["telefonos"]["emergencia"] = tel_emergencia
        
        print("Propietario actualizado con éxito.")
    else:
        print("Propietario no encontrado o inactivo.")
    
    guardar_json("propietarios.json", propietarios) #Guarda el propietario modificado al archivo json
    return 

def eliminar_propietario():
    """
    Marca a un propietario como inactivo (no lo borra del sistema).    
    """
    try:
        propietarios = cargar_json("propietarios.json") #Carga los datos del archivo 'propietarios.json'
    except Exception as e:
        print("Error al cargar propietarios:", e)
        return

    dni = input("Ingrese DNI del propietario a eliminar (0 para cancelar): ")
    if dni == "0": #Utiliza 0 para salir sin modificar 
        return 

    if dni in propietarios and propietarios[dni]["activo"]:  #Verifica que el propietario este activo en el sistema 
        propietarios[dni]["activo"] = False  #Marca propietario como inactivo
        print("Propietario marcado como inactivo.")
    else:
        print("Propietario no encontrado o ya inactivo.")
    
    guardar_json("propietarios.json", propietarios) #Guarda el propietario inactivo al archivo json
    return 

def listar_propietarios_activos():
    """
    Muestra todos los propietarios que estén activos.    
    """
    try:
        propietarios = cargar_json("propietarios.json") #Carga los datos del archivo 'propietarios.json'
    except Exception as e:
        print("Error al cargar propietarios:", e)
        return
    
    activos = {k: v for k, v in propietarios.items() if v["activo"]}
    if not activos:
        print("No hay propietarios activos.")
    else:
        print("\n--- PROPIETARIOS ACTIVOS ---")
        for dni, datos in activos.items():
            print(f"\nDNI: {dni}")
            print(f"Nombre: {datos['nombre']}")
            print(f"Dirección: {datos['direccion']}")
            print(f"Email: {datos['email']}")
            print(f"Teléfono: {datos['telefonos']['principal']}")
            print(f"Teléfono emergencia: {datos['telefonos']['emergencia']}")
            print("----------------------")
    return

def ingresar_mascota():
    """
    Pide datos de una mascota y la asocia a un propietario activo.    
    """
    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return

    try:
        propietarios = cargar_json("propietarios.json") #Carga los datos del archivo 'propietarios.json'
    except Exception as e:
        print("Error al cargar propietarios:", e)
        return

    dni_prop = input("DNI del propietario (0 para cancelar): ").strip()
    if dni_prop == "0": #Utiliza 0 para salir sin modificar 
        return 

    while dni_prop not in propietarios or not propietarios[dni_prop]["activo"]: #Verifica que el propietario este activo en el sistema hasta que se ingrese uno activo
        print("Propietario no registrado o inactivo.")
        dni_prop = input("DNI del propietario (0 para cancelar): ").strip()
        if dni_prop == "0":
            return 
        
    #Una vez verificado el propietario, se piden todos los datos de la mascota con sus respectivas verificaciones
    nombre = input("Nombre de la mascota: ").strip()
    while not nombre or contiene_numeros(nombre):
        print("El nombre no puede estar vacío ni contener números.")
        nombre = input("Nombre de la mascota: ").strip()

    sexo = input("Sexo: ").strip()
    while not sexo or contiene_numeros(sexo):
        print("El sexo no puede estar vacío ni contener números.")
        sexo = input("Sexo: ").strip()

    especie = input("Especie: ").strip()
    while not especie or contiene_numeros(especie):
        print("La especie no puede estar vacía ni contener números.")
        especie = input("Especie: ").strip()

    raza = input("Raza: ").strip()
    while contiene_numeros(raza):
        print("La raza no puede contener números.")
        raza = input("Raza: ").strip()

    edad = input("Edad: ").strip()
    while not edad.isdigit():
        print("La edad debe ser un número.")
        edad = input("Edad: ").strip()
    
    peso = input("Peso (kg): ").strip()
    while not peso.replace('.', '').isdigit():
        print("El peso debe ser un número.")
        peso = input("Peso (kg): ").strip()
    
    id_mascota = str(generar_id()) #Genera un ID para la nueva mascota
    while id_mascota in mascotas:
        id_mascota = str(generar_id())
    
    #Agrega mascota a la lista
    mascotas[id_mascota] = {
        "activo": True,
        "nombre": nombre,
        "sexo": sexo,
        "especie": especie,
        "raza": raza,
        "edad": int(edad),
        "peso": float(peso),
        "propietario": dni_prop,
        "historial": []
    }
    print(f"Mascota {nombre} registrada con ID: {id_mascota}")

    guardar_json("mascotas.json", mascotas) #Guarda la nueva mascota al archivo json
    return 

def modificar_mascota():
    """
    Permite cambiar datos de una mascota activa (nombre, sexo, especie, raza, edad y peso).    
    """
    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return
        
    id_masc = input("Ingrese ID de la mascota a modificar (0 para cancelar): ")
    if id_masc == "0":  #Utiliza 0 para salir sin modificar 
        return 
    
    if id_masc in mascotas and mascotas[id_masc]["activo"]: #Verifica que la mascota ingresada este activo en el sistema 
        print("\nDatos actuales:")
        print(f"Nombre: {mascotas[id_masc]['nombre']}")
        print(f"Sexo: {mascotas[id_masc]['sexo']}")
        print(f"Especie: {mascotas[id_masc]['especie']}")
        print(f"Raza: {mascotas[id_masc]['raza']}")
        print(f"Edad: {mascotas[id_masc]['edad']} años")
        print(f"Peso: {mascotas[id_masc]['peso']} kg")
        print(f"Propietario: {mascotas[id_masc]['propietario']}")
        
        #Una vez verificada, se vuelve a pedir todos los datos de la mascota 
        print("\nIngrese nuevos datos (dejar vacío para mantener el actual):")
        
        nombre = input(f"Nombre [{mascotas[id_masc]['nombre']}]: ").strip()
        while nombre and contiene_numeros(nombre):
            print("El nombre no puede contener números.")
            nombre = input(f"Nombre [{mascotas[id_masc]['nombre']}]: ").strip()
        if nombre:
            mascotas[id_masc]["nombre"] = nombre
        
        sexo = input(f"Sexo [{mascotas[id_masc]['sexo']}]: ").strip()
        while sexo and contiene_numeros(sexo):
            print("El sexo no puede contener números.")
            sexo = input(f"Sexo [{mascotas[id_masc]['sexo']}]: ").strip()
        if sexo:
            mascotas[id_masc]["sexo"] = sexo

        especie = input(f"Especie [{mascotas[id_masc]['especie']}]: ").strip()
        while especie and contiene_numeros(especie):
            print("La especie no puede contener números.")
            especie = input(f"Especie [{mascotas[id_masc]['especie']}]: ").strip()
        if especie:
            mascotas[id_masc]["especie"] = especie

        raza = input(f"Raza [{mascotas[id_masc]['raza']}]: ").strip()
        while raza and contiene_numeros(raza):
            print("La raza no puede contener números.")
            raza = input(f"Raza [{mascotas[id_masc]['raza']}]: ").strip()
        if raza:
            mascotas[id_masc]["raza"] = raza

        edad = input(f"Edad [{mascotas[id_masc]['edad']}]: ").strip()
        if edad and edad.isdigit():
            mascotas[id_masc]["edad"] = int(edad)
        
        peso = input(f"Peso [{mascotas[id_masc]['peso']}]: ").strip()
        if peso and peso.replace('.', '').isdigit():
            mascotas[id_masc]["peso"] = float(peso)
        
        print("Mascota actualizada con éxito.")
    else:
        print("Mascota no encontrada o inactiva.")
    
    guardar_json("mascotas.json", mascotas) #Guarda la mascota modificada al archivo json
    return 

def eliminar_mascota():
    """
    Marca una mascota como inactiva (no la borra del diccionario)    
    """
    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return
        
    id_masc = input("Ingrese ID de la mascota a modificar (0 para cancelar): ")
    if id_masc == "0": #Utiliza 0 para salir sin modificar 
        return 
    
    if id_masc in mascotas and mascotas[id_masc]["activo"]: #Verifica que la mascota este activa en el sistema 
        mascotas[id_masc]["activo"] = False  #Marca mascota como inactiva
        print("Mascota marcada como inactiva.")
    else:
        print("Mascota no encontrada o ya inactiva.")
    
    guardar_json("mascotas.json", mascotas) #Guarda la mascota inactiva al archivo json
    return 

def listar_mascotas_activas():
    """
    Muestra todas las mascotas que estén activas.    
    """
    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return
    
    activas = {k: v for k, v in mascotas.items() if v["activo"]}
    if not activas:
        print("No hay mascotas activas.")
    else:
        print("\n--- MASCOTAS ACTIVAS ---")
        for id_masc, datos in activas.items():
            print(f"\nID: {id_masc}")
            print(f"Nombre: {datos['nombre']}")
            print(f"Sexo: {datos['sexo']}")
            print(f"Especie: {datos['especie']}")
            print(f"Raza: {datos['raza']}")
            print(f"Edad: {datos['edad']} años")
            print(f"Peso: {datos['peso']} kg")
            print(f"Propietario: {datos['propietario']}")
            print("----------------------")
    return

def registrar_atencion():
    """
    Registra una nueva atención para una mascota activa con detalle de costos separados.
    """
    try:
        atenciones = cargar_json("atenciones.json") #Carga los datos del archivo 'atenciones.json'
    except Exception as e:
        print("Error al cargar atenciones:", e)
        return

    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return
    
    id_masc = input("ID de la mascota atendida (0 para cancelar): ")
    if id_masc == "0":  #Utiliza 0 para salir sin modificar 
        return 

    while id_masc not in mascotas or not mascotas[id_masc]["activo"]: #Verifica que la mascota este activa en el sistema hasta que se ingrese una valida
        print("Mascota no registrada o inactiva.")
        id_masc = input("ID de la mascota atendida (0 para cancelar): ")
        if id_masc == "0":
            return 
    
    dni_prop = mascotas[id_masc]["propietario"]
    
    motivo = input("Motivo de la consulta: ").strip()
    while not motivo:
        print("El motivo no puede estar vacío.")
        motivo = input("Motivo de la consulta: ").strip()
    
    diagnostico = input("Diagnóstico: ").strip()
    tratamiento = input("Tratamiento indicado: ").strip()
    
    costo_vet = input("Costo del veterinario: ").strip()
    while not costo_vet.replace('.', '').isdigit():
        print("Debe ingresar un número.")
        costo_vet = input("Costo del veterinario: ").strip()
    
    costo_med = input("Costo de medicamentos: ").strip()
    while not costo_med.replace('.', '').isdigit():
        print("Debe ingresar un número.")
        costo_med = input("Costo de medicamentos: ").strip()
    
    costo_total = float(costo_vet) + float(costo_med)  
    
    id_atencion = time.strftime("%Y.%m.%d %H.%M.%S")  #Crea un id con la fecha y hora actual de la computadora (formato: AAAA.MM.DD HH.MM.SS)

    #Agrega atencion a diccionario
    atenciones[id_atencion] = {
        "mascota": id_masc,
        "propietario": dni_prop,
        "motivo": motivo,
        "diagnostico": diagnostico,
        "tratamiento": tratamiento,
        "costo_veterinario": float(costo_vet),
        "costo_medicamentos": float(costo_med),
        "costo": costo_total
    }
    
    mascotas[id_masc]["historial"].append(id_atencion)
    print(f"Atención registrada con ID: {id_atencion}")

    guardar_json("atenciones.json", atenciones) #Guarda la nueva atencion al archivo json
    guardar_json("mascotas.json", mascotas) #Guarda la mascota al archivo json
    return 


def listar_atenciones():
    """
    Muestra todas las atenciones guardadas con datos completos.
    """
    try:
        atenciones = cargar_json("atenciones.json") #Carga los datos del archivo 'atenciones.json'
    except Exception as e:
        print("Error al cargar atenciones:", e)
        return
    
    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return
    
    if not atenciones:
        print("No hay atenciones registradas.")
    else:
        print("\n--- TODAS LAS ATENCIONES ---")
        for id_atencion, datos in atenciones.items():
            print(f"\nID: {id_atencion}")
            print(f"Mascota: {datos['mascota']} ({mascotas[datos['mascota']]['nombre']})")
            print(f"Propietario: {datos['propietario']}")
            print(f"Motivo: {datos['motivo']}")
            print(f"Diagnóstico: {datos['diagnostico']}")
            print(f"Tratamiento: {datos['tratamiento']}")
            print(f"Costo veterinario: ${datos['costo_veterinario']:.2f}")
            print(f"Costo medicamentos: ${datos['costo_medicamentos']:.2f}")
            print(f"Total: ${datos['costo']:.2f}")
            print("----------------------")
    return 


def atenciones_mes():
    """
    Muestra las atenciones realizadas en el mes actual en formato tabular.
    """
    try:
        atenciones = cargar_json("atenciones.json") #Carga los datos del archivo 'atenciones.json'
    except Exception as e:
        print("Error al cargar atenciones:", e)
        return
    
    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return
    
    try:
        propietarios = cargar_json("propietarios.json") #Carga los datos del archivo 'propietarios.json'
    except Exception as e:
        print("Error al cargar propietarios:", e)
        return
    
    mes_actual = time.strftime("%Y.%m")
    atenciones_mes = {k: v for k, v in atenciones.items() if k.startswith(mes_actual)}

    if not atenciones_mes:
        print(f"No hay atenciones registradas en el mes actual ({mes_actual}).") 
    
    #Crea una tabla mostrando todos los datos de las atenciones del mes
    else:
        print(f"\nATENCIONES DEL MES {mes_actual}")
        print("-" * 90)
        print(f"{'Fecha/Hora':<20} {'Cliente':<25} {'Mascota':<15} {'Vet.':>7} {'Med.':>7} {'Total':>10}")
        print("-" * 90)

        for id_at, datos in atenciones_mes.items():
            nombre_mascota = mascotas[datos["mascota"]]["nombre"]
            nombre_cliente = propietarios[datos["propietario"]]["nombre"]
            print(f"{id_at:<20} {nombre_cliente:<25} {nombre_mascota:<15} "
                  f"{datos['costo_veterinario']:>7.2f} {datos['costo_medicamentos']:>7.2f} {datos['costo']:>10.2f}")
    return 

def resumen_anual_atenciones_cantidades():
    """
    Muestra una matriz con la cantidad de atenciones por mascota y mes del año solicitado.
    """
    try:
        atenciones = cargar_json("atenciones.json") #Carga los datos del archivo 'atenciones.json'
    except Exception as e:
        print("Error al cargar atenciones:", e)
        return
    
    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return

    anio = input("Ingrese el año a consultar (formato AAAA): ").strip()
    while not anio.isdigit() or len(anio) != 4:
        print("Año inválido.")
        anio = input("Ingrese el año a consultar (formato AAAA): ").strip()

    #Crea estructura base
    matriz = {}
    for id_masc, datos in mascotas.items():
        nombre = datos["nombre"]
        matriz[nombre] = {m: 0 for m in range(1, 13)}

    #Completa datos
    for fecha, datos in atenciones.items():
        if fecha.startswith(anio):
            mes = int(fecha[5:7])
            nombre = mascotas[datos["mascota"]]["nombre"]
            matriz[nombre][mes] += 1

    #Muestra encabezado
    print("\nCANTIDADES TOTALES POR MES")
    print("-" * 145)
    nombres_meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
    encabezado = f"{'Mascota':<27}" + "".join([f"{nombre}.{anio[-2:]:<6}" for nombre in nombres_meses])
    print(encabezado)
    print("-" * 145)

    #Muestra filas
    for mascota, meses in matriz.items():
        fila = f"{mascota:<20}"
        for m in range(1, 13):
            fila += f"{meses[m]:>10}"
        print(fila)
    return 

def resumen_anual_atenciones_pesos():
    """
    Muestra una matriz con los montos totales de atención por mascota y mes del año solicitado.
    """
    try:
        atenciones = cargar_json("atenciones.json") #Carga los datos del archivo 'atenciones.json'
    except Exception as e:
        print("Error al cargar atenciones:", e)
        return
    
    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return

    anio = input("Ingrese el año a consultar (formato AAAA): ").strip()
    while not anio.isdigit() or len(anio) != 4:
        print("Año inválido.")
        anio = input("Ingrese el año a consultar (formato AAAA): ").strip()

    #Crea estructura base
    matriz = {}
    for id_masc, datos in mascotas.items():
        nombre = datos["nombre"]
        matriz[nombre] = {m: 0.0 for m in range(1, 13)}

    #Completa datos
    for fecha, datos in atenciones.items():
        if fecha.startswith(anio):
            mes = int(fecha[5:7])
            nombre = mascotas[datos["mascota"]]["nombre"]
            matriz[nombre][mes] += datos["costo"]

    #Muestra encabezado
    print("\nPESOS TOTALES POR MES")
    print("-" * 145)
    nombres_meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
    encabezado = f"{'Mascota':<27}" + "".join([f"{nombre}.{anio[-2:]:<6}" for nombre in nombres_meses])
    print(encabezado)
    print("-" * 145)

    #Muestra filas
    for mascota, meses in matriz.items():
        fila = f"{mascota:<20}"
        for m in range(1, 13):
            fila += f"{int(meses[m]):>10}"
        print(fila)
    return 

def historial_mascota():
    """
    Muestra el historial completo con todas las atenciones de la mascota ingresada.
    """
    try:
        atenciones = cargar_json("atenciones.json") #Carga los datos del archivo 'atenciones.json'
    except Exception as e:
        print("Error al cargar atenciones:", e)
        return
    
    try:
        mascotas = cargar_json("mascotas.json") #Carga los datos del archivo 'mascotas.json'
    except Exception as e:
        print("Error al cargar mascotas:", e)
        return

    id_masc = input("ID de la mascota (0 para cancelar): ")
    if id_masc == "0":
        return

    if id_masc in mascotas:
        print(f"\nHISTORIAL MÉDICO DE {mascotas[id_masc]['nombre'].upper()}")
        print(f"Especie: {mascotas[id_masc]['especie']}")
        print(f"Edad: {mascotas[id_masc]['edad']} años")
        print(f"Propietario: {mascotas[id_masc]['propietario']}\n")
        
        if not mascotas[id_masc]["historial"]:
            print("No hay atenciones registradas.")
        else:
            for id_atencion in mascotas[id_masc]["historial"]:
                if id_atencion in atenciones:
                    print(f"\nFecha: {id_atencion}")
                    print(f"Motivo: {atenciones[id_atencion]['motivo']}")
                    print(f"Diagnóstico: {atenciones[id_atencion]['diagnostico']}")
                    print(f"Tratamiento: {atenciones[id_atencion]['tratamiento']}")
                    print(f"Costo veterinario: ${atenciones[id_atencion]['costo_veterinario']:.2f}")
                    print(f"Costo medicamentos: ${atenciones[id_atencion]['costo_medicamentos']:.2f}")
                    print(f"Total: ${atenciones[id_atencion]['costo']:.2f}")
                    print("----------------------")
    else:
        print("Mascota no encontrada.")
    return 

def mostrar_menu_principal():
    """
    Imprime el menú principal del sistema con las opciones disponibles.
    """
    print("\n" + "="*50)
    print("SISTEMA DE GESTIÓN VETERINARIA")
    print("="*50)
    print("[1] Gestión de Propietarios")
    print("[2] Gestión de Mascotas")
    print("[3] Gestión de Atenciones")
    print("[4] Informes")
    print("[0] Salir del sistema")
    print("="*50)
    return 

def mostrar_submenu(titulo, opciones):
    """
    Imprime un submenú con un título y las opciones que pasan como diccionario.    
    Los parámetros:
        -titulo: texto que se muestra arriba
        -opciones: diccionario con clave = número de opción, valor = descripción    
    Siempre agrega 0 Volver al menú anterior.
    """
    print("\n" + "="*50)
    print(titulo)
    print("="*50)
    for key, value in opciones.items():
        print(f"[{key}] {value}")
    print("[0] Volver al menú anterior")
    print("="*50)
    return 

#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    """
    Función principal:
        1) Carga datos de ejemplo en diccionarios: propietarios, mascotas y atenciones.
        2) Muestra el menú principal y permite navegar a submenu:
        - 1:Gestión de Propietarios
        - 2:Gestión de Mascotas
        - 3:Gestión de Atenciones
        - 4:Informes
        - 0:Salir del programa
        3) Cada submenú se repite hasta que el usuario elige '0' para volver.
    """
    #-------------------------------------------------
    # Inicialización de variables
    #----------------------------------------------------------------------------------------------
    
    """
    #Diccionario de propietarios activos e inactivos. Cada propietario se identifica por su DNI
    propietarios = {
        "38111222": {
            "activo": True,
            "nombre": "Juan José Galván",
            "direccion": "Av. Siempreviva 742",
            "email": "juan.galvan@email.com",
            "telefonos": {
                "principal": "1122334455",
                "emergencia": "1198765432"
            }
        },
        "40233455": {
            "activo": True,
            "nombre": "María Luisa Pérez",
            "direccion": "Calle Falsa 123",
            "email": "maria.perez@email.com",
            "telefonos": {
                "principal": "1155667788",
                "emergencia": "1199887766"
            }
        },
        "39128473": {
            "activo": True,
            "nombre": "Carlos Daniel Ruiz",
            "direccion": "Av. Libertador 4587",
            "email": "carlos.ruiz@email.com",
            "telefonos": {
                "principal": "1144556677",
                "emergencia": "1166778899"
            }
        },
        "40399284": {
            "activo": True,
            "nombre": "Lucía Fernández",
            "direccion": "Calle 1234",
            "email": "lucia.fernandez@email.com",
            "telefonos": {
                "principal": "1188997766",
                "emergencia": "1155443322"
            }
        },
        "37283910": {
            "activo": True,
            "nombre": "Martín Alejandro López",
            "direccion": "Av. Corrientes 3456",
            "email": "martin.lopez@email.com",
            "telefonos": {
                "principal": "1133445566",
                "emergencia": "1177889900"
            }
        },
        "38902764": {
            "activo": True,
            "nombre": "Sofía Beatriz Ramos",
            "direccion": "Av. Santa Fe 2100",
            "email": "sofia.ramos@email.com",
            "telefonos": {
                "principal": "1199887766",
                "emergencia": "1122334455"
            }
        },
        "41392847": {
            "activo": True,
            "nombre": "Nicolás Emiliano Gómez",
            "direccion": "Av. Rivadavia 7890",
            "email": "nicolas.gomez@email.com",
            "telefonos": {
                "principal": "1166554433",
                "emergencia": "1144332211"
            }
        },
        "40567219": {
            "activo": True,
            "nombre": "Valentina Herrera",
            "direccion": "Av. Belgrano 456",
            "email": "valentina.herrera@email.com",
            "telefonos": {
                "principal": "1177665544",
                "emergencia": "1133221100"
            }
        },
        "39384756": {
            "activo": True,
            "nombre": "Julián Castro",
            "direccion": "Av. Pueyrredón 1200",
            "email": "julian.castro@email.com",
            "telefonos": {
                "principal": "1144887766",
                "emergencia": "1199554433"
            }
        },
        "38472918": {
            "activo": True,
            "nombre": "Carla Noemí Torres",
            "direccion": "Av. Callao 876",
            "email": "carla.torres@email.com",
            "telefonos": {
                "principal": "1122778899",
                "emergencia": "1166554433"
            }
        }
    }

    #Diccionario de mascotas con su historial. Cada mascota tiene un ID único y pertenece a un propietario.
    mascotas = {
        "10000001": {
            "activo": True,
            "nombre": "Max",
            "sexo": "Masculino",
            "especie": "Perro",
            "raza": "Labrador",
            "edad": 5,
            "peso": 28.5,
            "propietario": "38111222",
            "historial": ["2023.05.10 10.30.00", "2023.06.15 11.00.00"]
        },
        "10000002": {
            "activo": True,
            "nombre": "Luna",
            "sexo": "Femenino",
            "especie": "Gato",
            "raza": "Siamés",
            "edad": 3,
            "peso": 4.2,
            "propietario": "40233455",
            "historial": ["2023.05.12 09.15.00"]
        },
        "10000003": {
            "activo": True,
            "nombre": "Bella",
            "sexo": "Femenino",
            "especie": "Perro",
            "raza": "Caniche",
            "edad": 7,
            "peso": 6.8,
            "propietario": "39128473",
            "historial": ["2023.04.20 16.45.00", "2023.05.25 10.30.00"]
        },
        "10000004": {
            "activo": True,
            "nombre": "Simba",
            "sexo": "Masculino",
            "especie": "Gato",
            "raza": "Persa",
            "edad": 2,
            "peso": 5.1,
            "propietario": "40399284",
            "historial": []
        },
        "10000005": {
            "activo": True,
            "nombre": "Rocky",
            "sexo": "Masculino",
            "especie": "Perro",
            "raza": "Bulldog",
            "edad": 4,
            "peso": 22.3,
            "propietario": "37283910",
            "historial": ["2023.06.01 14.00.00"]
        },
        "10000006": {
            "activo": True,
            "nombre": "Milo",
            "sexo": "Masculino",
            "especie": "Gato",
            "raza": "Mestizo",
            "edad": 1,
            "peso": 3.5,
            "propietario": "38902764",
            "historial": []
        },
        "10000007": {
            "activo": True,
            "nombre": "Coco",
            "sexo": "Masculino",
            "especie": "Perro",
            "raza": "Golden Retriever",
            "edad": 6,
            "peso": 30.0,
            "propietario": "41392847",
            "historial": ["2023.03.15 11.30.00", "2023.05.20 09.45.00"]
        },
        "10000008": {
            "activo": True,
            "nombre": "Lola",
            "sexo": "Femenino",
            "especie": "Gato",
            "raza": "Angora",
            "edad": 4,
            "peso": 4.8,
            "propietario": "40567219",
            "historial": ["2023.05.05 17.30.00"]
        },
        "10000009": {
            "activo": True,
            "nombre": "Toby",
            "sexo": "Masculino",
            "especie": "Perro",
            "raza": "Beagle",
            "edad": 2,
            "peso": 12.5,
            "propietario": "39384756",
            "historial": []
        },
        "10000010": {
            "activo": True,
            "nombre": "Mía",
            "sexo": "Femenino",
            "especie": "Gato",
            "raza": "Bengalí",
            "edad": 3,
            "peso": 4.0,
            "propietario": "38472918",
            "historial": ["2023.04.10 10.00.00", "2023.06.05 15.30.00"]
        }
    }

    #Diccionario de atenciones registradas con informacion de la visita y el costo
    atenciones = {
    "2023.05.10 10.30.00": {
        "mascota": "10000001",
        "propietario": "38111222",
        "motivo": "Control anual",
        "diagnostico": "Saludable",
        "tratamiento": "Vacuna antirrábica",
        "costo_veterinario": 1500.00,
        "costo_medicamentos": 1000.00,
        "costo": 2500.00
    },
    "2023.06.15 11.00.00": {
        "mascota": "10000001",
        "propietario": "38111222",
        "motivo": "Dolor articular",
        "diagnostico": "Artritis incipiente",
        "tratamiento": "Antiinflamatorio",
        "costo_veterinario": 2000.00,
        "costo_medicamentos": 1200.00,
        "costo": 3200.00
    },
    "2023.05.12 09.15.00": {
        "mascota": "10000002",
        "propietario": "40233455",
        "motivo": "Castración",
        "diagnostico": "Pre-operatorio normal",
        "tratamiento": "Cirugía",
        "costo_veterinario": 3000.00,
        "costo_medicamentos": 1500.00,
        "costo": 4500.00
    },
    "2023.07.01 15.00.00": {
        "mascota": "10000003",
        "propietario": "39128473",
        "motivo": "Revisión posoperatoria",
        "diagnostico": "Buena recuperación",
        "tratamiento": "Antibióticos",
        "costo_veterinario": 1200.00,
        "costo_medicamentos": 800.00,
        "costo": 2000.00
    },
    "2023.07.10 13.30.00": {
        "mascota": "10000004",
        "propietario": "40399284",
        "motivo": "Fiebre",
        "diagnostico": "Infección leve",
        "tratamiento": "Antibióticos",
        "costo_veterinario": 1800.00,
        "costo_medicamentos": 700.00,
        "costo": 2500.00
    },
    "2023.08.05 11.15.00": {
        "mascota": "10000005",
        "propietario": "37283910",
        "motivo": "Control de peso",
        "diagnostico": "Sobrepeso leve",
        "tratamiento": "Dieta balanceada",
        "costo_veterinario": 1400.00,
        "costo_medicamentos": 0.00,
        "costo": 1400.00
    },
    "2023.08.20 17.45.00": {
        "mascota": "10000006",
        "propietario": "38902764",
        "motivo": "Vacunación",
        "diagnostico": "Saludable",
        "tratamiento": "Vacuna triple felina",
        "costo_veterinario": 1000.00,
        "costo_medicamentos": 600.00,
        "costo": 1600.00
    },
    "2023.09.02 09.50.00": {
        "mascota": "10000007",
        "propietario": "41392847",
        "motivo": "Herida en pata",
        "diagnostico": "Corte leve",
        "tratamiento": "Curación + antibiótico",
        "costo_veterinario": 2200.00,
        "costo_medicamentos": 900.00,
        "costo": 3100.00
    },
    "2023.09.15 16.10.00": {
        "mascota": "10000008",
        "propietario": "40567219",
        "motivo": "Consulta por vómitos",
        "diagnostico": "Malestar digestivo",
        "tratamiento": "Dieta + antiemético",
        "costo_veterinario": 1700.00,
        "costo_medicamentos": 650.00,
        "costo": 2350.00
    },
    "2023.10.03 14.20.00": {
        "mascota": "10000009",
        "propietario": "39384756",
        "motivo": "Chequeo general",
        "diagnostico": "Sin novedades",
        "tratamiento": "Vitaminas",
        "costo_veterinario": 1300.00,
        "costo_medicamentos": 500.00,
        "costo": 1800.00
    }
    }
    """

    #-------------------------------------------------
    # Bloque de menú
    #----------------------------------------------------------------------------------------------
    while True:
        mostrar_menu_principal()
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "0":
            print("\nSaliendo del sistema...")
            break
            
        elif opcion == "1":  # Gestión de Propietarios
            while True:
                mostrar_submenu("GESTIÓN DE PROPIETARIOS", {
                    "1": "Ingresar Propietario",
                    "2": "Modificar Propietario",
                    "3": "Eliminar Propietario",
                    "4": "Listado de Propietarios Activos"
                })
                
                sub_opcion = input("\nSeleccione una opción: ")
                
                if sub_opcion == "0":
                    break
                elif sub_opcion == "1":
                    propietarios = ingresar_propietario()
                elif sub_opcion == "2":
                    propietarios = modificar_propietario()
                elif sub_opcion == "3":
                    propietarios = eliminar_propietario()
                elif sub_opcion == "4":
                    listar_propietarios_activos()
                else:
                    print("Opción inválida.")
                
                input("\nPresione ENTER para continuar...")
                
        elif opcion == "2":  # Gestión de Mascotas
            while True:
                mostrar_submenu("GESTIÓN DE MASCOTAS", {
                    "1": "Ingresar Mascota",
                    "2": "Modificar Mascota",
                    "3": "Eliminar Mascota",
                    "4": "Listado de Mascotas Activas"
                })
                
                sub_opcion = input("\nSeleccione una opción: ")
                
                if sub_opcion == "0":
                    break
                elif sub_opcion == "1":
                    mascotas = ingresar_mascota()
                elif sub_opcion == "2":
                    mascotas = modificar_mascota()
                elif sub_opcion == "3":
                    mascotas = eliminar_mascota()
                elif sub_opcion == "4":
                    listar_mascotas_activas()
                else:
                    print("Opción inválida.")
                
                input("\nPresione ENTER para continuar...")
                
        elif opcion == "3":  # Gestión de Atenciones
            while True:
                mostrar_submenu("GESTIÓN DE ATENCIONES", {
                    "1": "Registro de Atención Veterinaria",
                    "2": "Listado de Todas las Atenciones"
                })
                
                sub_opcion = input("\nSeleccione una opción: ")
                
                if sub_opcion == "0":
                    break
                elif sub_opcion == "1":
                    atenciones = registrar_atencion()
                elif sub_opcion == "2":
                    listar_atenciones()
                else:
                    print("Opción inválida.")
                
                input("\nPresione ENTER para continuar...")
                
        elif opcion == "4":  # Informes
            while True:
                mostrar_submenu("INFORMES", {
                    "1": "Atenciones del Mes",
                    "2": "Resumen Anual de Atenciones por Mascota (Cantidades)",
                    "3": "Resumen Anual de Atenciones por Mascota (Pesos)",
                    "4": "Historial médico completo de una Mascota"
                })

                sub_opcion = input("\nSeleccione una opción: ")

                if sub_opcion == "0":
                    break
                elif sub_opcion == "1":
                    atenciones_mes()
                elif sub_opcion == "2":
                    resumen_anual_atenciones_cantidades()
                elif sub_opcion == "3":
                    resumen_anual_atenciones_pesos()
                elif sub_opcion == "4":
                    historial_mascota()
                else:
                    print("Opción inválida.")

                input("\nPresione ENTER para continuar...")

        else:
            print("Opción inválida.")
            input("\nPresione ENTER para continuar...")

# Punto de entrada al programa
main()