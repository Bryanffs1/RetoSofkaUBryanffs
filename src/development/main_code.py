from flask import render_template, request      # flask
from development import app
import pandas as pd                         # pandas para el manejo de datos con dataframs y guardar datos enarchivo .csv
from IPython.display import HTML            # para enviar tablas html desde python

class Reg_Elim_Datos:                                       # clase para obtener datos de las naves, guardar y eliminar los datos de las naves
    def __init__(self, reg_nave):                           # obtiene los datos de entrada
        if isinstance(reg_nave, pd.DataFrame):              # optiene los datos de la nave en forma de dataframe
            self.datos_de_nave = reg_nave
        elif isinstance(reg_nave, str):                     # optiene variables de forma de string
            self.eliminar_datos_nave_name = reg_nave

    def guardar_registro(self):                             # metodo para registrar una nave en la base de datos NoSql formato csv
        self.datos_de_nave.reset_index(drop = True).to_csv('../data/Naves.csv',header=False, index=False, mode='a')     # guardar los datos en la base de datos de forma que se guarda en la ultima fila disponible
        print(self.datos_de_nave)

    def eliminar_registro(self):                             # metodo para eliminar solo una nave en la base de datos NoSql formato csv 
        df_naves= pd.read_csv('../data/Naves.csv')              # se obtiene la base de datos
        eliminar_nave=df_naves.loc[(df_naves)['NOMBRE']!=self.eliminar_datos_nave_name]     # se obtiene todos los datos menos el que se quiere eliminar
        eliminar_nave.reset_index(drop = True).to_csv('../data/Naves.csv',header=True, index=False)     # se guardan los datos menos el que se saco
        print(f'{self.eliminar_datos_nave_name} eliminado')

class Formato_tabla:                                         # clase para darle formato a las tablas en html para mostrar la informacion de las naves
    def tabla_html_naves():                                   # metodo para darle formato a las tablas donde se muestran todas las naves en el inventario
        pd.set_option('display.width', 1000)                   # configuracion en css para la tabla
        pd.set_option('display.colheader_justify', 'center')    
        df_naves=pd.read_csv('../data/Naves.csv')               # se obtiene la base de datos
        df = df_naves[['CLASE','NOMBRE','PAIS','DESCRIPCION']]  # se establecen las columnas que se mostraran
        tabla_naves = HTML(df.to_html(classes = 'table table- border table-striped table-hover table-condensed' )) # se guarda la tabla en una variable
        
        return tabla_naves                                      # retorna la tabla

    def tabla_busquda_html_naves():                            # metodo para darle formato a la tabla que se solicita el usuario para la busqueda o filtro del sistema
        datos_tabla = []
        for i in range(1,18):                                   # loop para agregar a una lista los datos que el usuario desea ver en la solicitud
            data_tabla_html = request.form.get(f'data_tabla{i}')

            if data_tabla_html != None:
                datos_tabla.append(data_tabla_html)                                

        if not datos_tabla:                                     # si el usuario no dice que datos desea ver, se establecen unos datos por default 
            datos_tabla =['CLASE','NOMBRE','PAIS','DESCRIPCION']

        return datos_tabla                                   # retorna las columnas que desea el usuario en la tabla de busqueda

class Naves:                                    # clase para dos comportamientos abstractos de las naves
    def despegue(self):                         # metodo de comportamiento abstracto de despegue de la nave
        pass
    def aterrizaje(self):                       # metodo de comportamiento abstracto de aterrizaje de la nave
        pass

class Nave_tripulada(Naves):                    # clase de comportamientos abstractos de las naves tripuladas
    def despegue(self):
        print("Nave tripulada despegando")

    def aterrizaje(self):
        print("Nave tripulada aterrizando")

class Nave_no_tripulada(Naves):                 # metodo de comportamiento abstracto de despegue de la naves no tripuladas
    def despegue(self):
        print("Nave no tripulada despegando")
        
    def aterrizaje(self):
        print("Nave no tripulada aterrizando")

@app.route('/')                                     # ruta raiz del sitio web
@app.route('/inicio')                               # ruta inicio del sitio web
def inicio():                                       # metodo de inicio el cual redirecciona al archivo inicio.html con algunos parametros como el titulo de la pagina y una variable para un atributo en el html
    
    print("inicio")
    return render_template("inicio.html", title='Inicio', segment='Inicio')

@app.route('/registro', methods=['GET','POST'])     # ruta registro del sitio web con metodo GET POST, metodo get para cuando carga la pagina y post cuando hay una accion como un formulario de la pagina
def registro():                                # metodo que obtiene datos del sitio web de registro de la nave 
    
    if request.method == 'POST':            # para cuando el usuario envia los datos
            
        nombrestr = str(request.form.get('nombre'))         # obtiene los datos del html

        df_naves= pd.read_csv('../data/Naves.csv')   
        datos_nombre_naves = df_naves['NOMBRE'].tolist()       # enlista los nombres que hay en la base de datos
        verificacion_nave = nombrestr in datos_nombre_naves     # verifiva si la nave esta en la base de datos o no con el fin de no guardar datos que ya se encuentran registrados

        if not verificacion_nave:                                # si la nave no esta en la base de datos, entra y obtine todos los datos del html
            clase = str(request.form.get('clase'))
            clase=pd.DataFrame({'CLASE':[clase]})               # guarda los datos en un datagrame
            nombre=pd.DataFrame({'NOMBRE':[nombrestr]})
            pais = str(request.form.get('pais'))
            pais=pd.DataFrame({'PAIS':[pais]})
            fecha_ini = request.form.get('fecha_ini')
            if fecha_ini: fecha_ini = int(fecha_ini)            # hay datos numericos que no se conocen de alguna naves, por lo que si se ingresa se le da formato de int y si no, que lo ponga como None
            else: fecha_ini = None
            fecha_ini=pd.DataFrame({'FECHA INICIAL':[fecha_ini]})
            fecha_fin = request.form.get('fecha_fin')
            if fecha_fin: fecha_fin = int(fecha_fin)
            else: fecha_fin = None
            fecha_fin=pd.DataFrame({'FECHA FINAL':[fecha_fin]})
            combustible = str(request.form.get('combustible'))
            combustible=pd.DataFrame({'COMBUSTIBLE':[combustible]})
            peso_nave = request.form.get('peso_nave')
            if peso_nave: peso_nave = int(peso_nave)
            else: peso_nave = None
            peso_nave=pd.DataFrame({'PESO NAVE(T)':[peso_nave]})
            peso_max_carga = request.form.get('peso_max_carga')
            if peso_max_carga: peso_max_carga = int(peso_max_carga)
            else: peso_max_carga = None
            peso_max_carga=pd.DataFrame({'PESO MAX DE CARGA(T)':[peso_max_carga]})
            empuje = request.form.get('empuje')
            if empuje: empuje = int(empuje)
            else: empuje = None
            empuje=pd.DataFrame({'EMPUJE(T)':[empuje]})
            altura = request.form.get('altura')
            if altura: altura = int(altura)
            else: altura = None
            altura=pd.DataFrame({'ALTURA(M)':[altura]})
            potencia = request.form.get('potencia')  
            if potencia: potencia = int(potencia)
            else: potencia = None  
            potencia=pd.DataFrame({'POTENCIA(CABALLOS)':[potencia]})   
            velocidad_aprox = request.form.get('velocidad_aprox')
            if velocidad_aprox: velocidad_aprox = int(velocidad_aprox)
            else: velocidad_aprox = None
            velocidad_aprox=pd.DataFrame({'VELOCIDAD APROX(KM)':[velocidad_aprox]})
            cap_persona = request.form.get('cap_persona')
            if cap_persona: cap_persona = int(cap_persona)
            else: cap_persona = None
            cap_persona=pd.DataFrame({'CAPACIDAD PERSONAL':[cap_persona]})
            planeta = str(request.form.get('planeta'))
            planeta=pd.DataFrame({'PLANETA':[planeta]})
            dist_tierra = request.form.get('dist_tierra')
            if dist_tierra: dist_tierra = int(dist_tierra)
            else: dist_tierra = None
            dist_tierra=pd.DataFrame({'DISTANCIA TIERRA(KM)':[dist_tierra]})
            cel_fotovoltaicas = str(request.form.get('cel_fotovoltaicas'))
            cel_fotovoltaicas=pd.DataFrame({'CELDA FOTOVOLTAICA':[cel_fotovoltaicas]})
            descripcion = str(request.form.get('descripcion'))
            descripcion=pd.DataFrame({'DESCRIPCION':[descripcion]})
            
            #------------ concatena todos los datos para guardarlos mas facil en la base de datos -----------
            datos_nave = pd.concat([clase,nombre,pais,fecha_ini,fecha_fin,combustible,peso_nave,peso_max_carga,empuje,altura,potencia,velocidad_aprox,cap_persona,planeta,dist_tierra,cel_fotovoltaicas,descripcion], axis=1,)
           
            #------------- se envian los datos a la clase de Reg_Elim_Datos y el metodo guardar_registro para guardar los datos en la base de datos
            registro_nave_Data = Reg_Elim_Datos(datos_nave)
            registro_nave_Data.guardar_registro()            
            
            info = f"Nave "+nombrestr+" registrada satisfactoriamente."         # variable que se envia como informacion para el usuario en el pagina web
            
        elif verificacion_nave:                                                 # si la nave ya esta registrada, se le informa al usuario
            info= "La Nave "+nombrestr+" ya se encuentra registrada"
    
        tabla_naves = Formato_tabla.tabla_html_naves()                          # tabla configurada en la clase Formato_tabla y metodo tabla_html_naves para mostrar todas las naves en el inventario
                                                                                # asi se puede reutilizar este codigo para cada vez que se quiera mostrar todas las naves en el inventario
        return render_template("Registro.html", info=info, title='Registro', segment='Registro', tabla_naves=tabla_naves)
        
    tabla_naves = Formato_tabla.tabla_html_naves()          # mostrando todas las naves en el inventario de forma que reutiliza un fragmento de codigo que se encuentra en la clase y metodo Formato_tabla.tabla_html_naves()
    return render_template("Registro.html", title='Prueba', segment='Registro', tabla_naves=tabla_naves) 

@app.route('/Eliminar', methods=['GET','POST'])
def Eliminar():                     # metodo para obtener los datos necesarios para eliminar una nave en la base de datos
    
    if request.method == 'POST':

        nombre = str(request.form.get('nombre'))
        df_naves= pd.read_csv('../data/Naves.csv')
        datos_nombre_naves = df_naves['NOMBRE'].tolist()
        verificacion_nave = nombre in datos_nombre_naves        # verificacion de si la nave a eliminar existe en la base de datos

        if verificacion_nave:                                   # si existe la nave 
            registro_nave_Data = Reg_Elim_Datos(nombre)         # envia a la clase Reg_Elim_Datos el dato con el nombre de la nave a eliminar para luego con el metodo eliminar_registro() de la misma clase, eliminar la nave de la base de datos
            registro_nave_Data.eliminar_registro()  
            
            info = "Nave "+nombre+" eliminada del inventario"

        elif not verificacion_nave:                         # si no existe la nave 
            info= "El nombre "+nombre+" no corresponde con algúna nave existente."

        tabla_naves = Formato_tabla.tabla_html_naves()                  # tabla que muestra todas las naves en el inventario
        return render_template("Eliminar.html", info=info, title='Eliminar', segment='Eliminar', tabla_naves=tabla_naves)

    tabla_naves = Formato_tabla.tabla_html_naves()
    return render_template("Eliminar.html", title='Eliminar', segment='Eliminar', tabla_naves=tabla_naves)

@app.route('/Buscar', methods=['GET','POST'])
def Buscar():                                   # metodo para la busqueda sencilla y avanzada de naves segun sus caracteristicas en la base de datos
    
    if request.method == 'POST':

        clase1 = str(request.form.get('vehicle1'))
        clase2 = str(request.form.get('vehicle2'))
        clase3 = str(request.form.get('vehicle3'))
        pais = str(request.form.get('pais'))
        columna1 = str(request.form.get('columna1'))
        dato_buscar1 = request.form.get('dato_buscar1')
        try: dato_buscar1 = int(dato_buscar1)               # si el dato es string se activa el except para dejar su formato, pero si el dato es un numero... 
        except ValueError: pass                             # ...le pone formato de int para poder realizar las busquedas correctamente diferenciando entre formatos str o int...
        columna2 = str(request.form.get('columna2'))        #... todo esto porque el usuario escoge que dato poner, como por ejemplo filtrar por pais o filtrar por año o por muchas mas opciones
        dato_buscar2 = request.form.get('dato_buscar2')
        try: dato_buscar2 = int(dato_buscar2)
        except ValueError: pass
        columna3 = str(request.form.get('columna3'))
        dato_buscar3 = request.form.get('dato_buscar3')
        try: dato_buscar3 = int(dato_buscar3)
        except ValueError: pass

        operador1 = str(request.form.get('operador1'))     # el operador es para filtrar los datos bien sea con comparadores de AND ó OR, el usuario puede escoger cual utilizar
        operador2 = str(request.form.get('operador2'))

        pd.set_option('display.width', 1000)
        pd.set_option('display.colheader_justify', 'center')
        df_naves= pd.read_csv('../data/Naves.csv')

        #---------------------cantidad de columnas para mostrar en tabla en html--------------------------
        datos_tabla = Formato_tabla.tabla_busquda_html_naves()      # se utiliza Formato_tabla.tabla_busquda_html_naves() con el fin de que el usuario ingrese los datos que desea ver como resultado de la busqueda

        #---------------------filtro clase--------------------------

        if clase1 == 'Vehiculo lanzadera' and clase2 == 'None' and clase3 == 'None':           # busqueda cuando el usuario desea filtar por clase de naves
            df_naves_fclase = df_naves.loc[(df_naves)['CLASE'] == clase1]                       # se busca los datos con la clase seleccionada y se guardan en una variable
            print("solo clases 1 ingresada")
        elif clase1 == 'None' and clase2 == 'Nave Espacial Tripulada' and clase3 == 'None':     # cada if o elif es para que el usuario seleccione las clases de naves que desee filtrar y la cantidad de clase que quiera
            df_naves_fclase = df_naves.loc[(df_naves)['CLASE'] == clase2]
            print("solo clases 2 ingresada")
        elif clase1 == 'None' and clase2 == 'None' and clase3 == 'Nave Espacial No Tripulada':
            df_naves_fclase = df_naves.loc[(df_naves)['CLASE'] == clase3]
            print("solo clases 3 ingresada")
        elif clase1 == 'Vehiculo lanzadera' and clase2 == 'Nave Espacial Tripulada' and clase3 == 'None':
            df_naves_fclase = df_naves.loc[(df_naves)['CLASE'] != 'Nave Espacial No Tripulada']
            print("las 1 y 2 clas ingresadas"        )
        elif clase1 == 'None' and clase2 == 'Nave Espacial Tripulada' and clase3 == 'Nave Espacial No Tripulada':
            df_naves_fclase = df_naves.loc[(df_naves)['CLASE'] != 'Vehiculo lanzadera']
            print("las 2 y 3 clas ingresadas")
        elif clase1 == 'Vehiculo lanzadera' and clase2 == 'None' and clase3 == 'Nave Espacial No Tripulada':
            df_naves_fclase = df_naves.loc[(df_naves)['CLASE'] != 'Nave Espacial Tripulada']
            print("las 1 y 3 clase ingresadas")
        #--------- si no se selecciona ninguna clase, se guardara los datos tal cual como estan el la base de datos -------------------------------- 
        elif clase1 == 'Vehiculo lanzadera' and clase2 == 'Nave Espacial Tripulada' and clase3 == 'Nave Espacial No Tripulada' or clase1 == 'None' and clase2 == 'None' and clase3 == 'None':
            df_naves_fclase = df_naves      
            print("Todas las clase ingresadas o clases en default")
        
        #---------------------filtro de pais--------------------------
        if pais:                                                            # filtro cuando el usuario desea filtar por pais de las naves
            df_naves_fclase_pais = df_naves_fclase.loc[(df_naves_fclase)['PAIS'] == pais]
            print("Pais ingresado")
        else:
            df_naves_fclase_pais = df_naves_fclase
            print("No ingreso pais")        
                    
        #---------------------filtro avanzado datos generales--------------------------
        if columna1 and dato_buscar1 and not columna2 and not dato_buscar2 and not columna3 and not dato_buscar3:      # filtro si se pone una clase de dato y el dato correspondiente a buscar
            df_naves_fclase_pais_datos = df_naves_fclase_pais.loc[(df_naves_fclase_pais)[columna1] == dato_buscar1]
            info = f"Columna '{columna1}' y dato '{dato_buscar1}' ingresado"       
        elif columna1 and dato_buscar1 and columna2 and dato_buscar2 and not columna3 and not dato_buscar3:             # filtro si se pone dos clases de datos y los datos correspondientes a buscar
            if operador1 == '&':        #si el usuario seleciona el comparador AND entonces realiza la busqueda del dato uno y que tambien tenga el dato dos
                df_naves_fclase_pais_datos = df_naves_fclase_pais.loc[((df_naves_fclase_pais)[columna1] == dato_buscar1) & ((df_naves_fclase_pais)[columna2] == dato_buscar2)]
                info = f"Columna '{columna1}' dato '{dato_buscar1}' y columna '{columna2}' dato '{dato_buscar2}' ingresado con operador 'AND'"
            elif operador1 == '|':      #si el usuario seleciona el comparador OR entonces realiza la busqueda del dato uno ó que tambien tenga el dato dos
                df_naves_fclase_pais_datos = df_naves_fclase_pais.loc[((df_naves_fclase_pais)[columna1] == dato_buscar1) | ((df_naves_fclase_pais)[columna2] == dato_buscar2)]   
                info = f"Columna '{columna1}' dato '{dato_buscar1}' ó columna '{columna2}' dato '{dato_buscar2}' ingresado con operador 'OR'" 
            else:
                df_naves_fclase_pais_datos = df_naves_fclase_pais
                info = f"No se selecciono un operador 'OR' ó 'AND'"
            print("Datos 1 y 2 ingresados")
        elif columna1 and dato_buscar1 and columna2 and dato_buscar2 and columna3 and dato_buscar3:                      # filtro si se pone tres clases de datos y los datos correspondientes a buscar
            if operador1 == '&' and operador2 == '&': #si el usuario solo seleciona el comparador AND entonces realiza la busqueda del dato uno y que tambien tenga el dato dos y tambien tenga el dato tres
                df_naves_fclase_pais_datos = df_naves_fclase_pais.loc[((df_naves_fclase_pais)[columna1] == dato_buscar1) & ((df_naves_fclase_pais)[columna2] == dato_buscar2) & ((df_naves_fclase_pais)[columna3] == dato_buscar3)]
                info = f"Columna '{columna1}' dato '{dato_buscar1}' y columna '{columna2}' dato '{dato_buscar2}' y columna '{columna3}' dato '{dato_buscar3}' ingresado solo con operador 'AND'" 
            elif operador1 == '&' and operador2 == '|': #si el usuario seleciona el comparador AND y OR entonces realiza la busqueda del dato uno y que tambien tenga el dato dos ó tenga el dato tres
                df_naves_fclase_pais_datos = df_naves_fclase_pais.loc[((df_naves_fclase_pais)[columna1] == dato_buscar1) & ((df_naves_fclase_pais)[columna2] == dato_buscar2) | ((df_naves_fclase_pais)[columna3] == dato_buscar3)]
                info = f"Columna '{columna1}' dato '{dato_buscar1}' y columna '{columna2}' dato '{dato_buscar2}' ó columna '{columna3}' dato '{dato_buscar3}' ingresado con operador 'AND' y 'OR'"
            elif operador1 == '|' and operador2 == '&': #si el usuario seleciona el comparador OR y AND entonces realiza la busqueda del dato uno o que tenga el dato dos y tambien tenga el dato tres
                df_naves_fclase_pais_datos = df_naves_fclase_pais.loc[((df_naves_fclase_pais)[columna1] == dato_buscar1) | ((df_naves_fclase_pais)[columna2] == dato_buscar2) & ((df_naves_fclase_pais)[columna3] == dato_buscar3)]
                info = f"Columna '{columna1}' dato '{dato_buscar1}' ó columna '{columna2}' dato '{dato_buscar2}' y columna '{columna3}' dato '{dato_buscar3}' ingresado con operador 'OR' y 'AND'"
            elif operador1 == '|' and operador2 == '|': #si el usuario solo seleciona el comparador OR entonces realiza la busqueda del dato uno ó que tenga el dato dos ó tenga el dato tres
                df_naves_fclase_pais_datos = df_naves_fclase_pais.loc[((df_naves_fclase_pais)[columna1] == dato_buscar1) | ((df_naves_fclase_pais)[columna2] == dato_buscar2) | ((df_naves_fclase_pais)[columna3] == dato_buscar3)]
                info = f"Columna '{columna1}' dato '{dato_buscar1}' ó columna '{columna2}' dato '{dato_buscar2}' ó columna '{columna3}' dato '{dato_buscar3}' ingresado solo con operador 'OR'"            
            else:       # si no selecciona algun comparador pero pone datos en la busqueda avanzada, se le informa al ususario
                df_naves_fclase_pais_datos = df_naves_fclase_pais
                info = f"No se selecciono todos los operadores 'OR' ó 'AND'"
                
            print("Datos 1 2 y 3 ingresados")
        elif not columna1 and not dato_buscar1 and not columna2 and not dato_buscar2 and not columna3 and not dato_buscar3: # filtro si no se ponen clases de datos y los datos correspondientes a buscar
            df_naves_fclase_pais_datos = df_naves_fclase_pais
            print("Datos no ingresados")
            info = ""
        else:                                       # si se ingresan mal los datos, se le informa al usario
            df_naves_fclase_pais_datos = df_naves_fclase_pais
            info = "Datos mal ingresados, intente de nuevo"
                
        df = df_naves_fclase_pais_datos[datos_tabla]        # tabla con los datos que el usuario quiere ver o saber con ayuda de Formato_tabla.tabla_busquda_html_naves() y la busquedas seleccionadas
        tabla_filtro = HTML(df.to_html(classes = 'table table- border table-striped table-hover table-condensed' ))
        
        tabla_naves = Formato_tabla.tabla_html_naves()
        return render_template("Busqueda.html", info=info, title='Buscar', segment='Buscar', tabla_naves=tabla_naves, tabla_filtro=tabla_filtro)

    tabla_naves = Formato_tabla.tabla_html_naves()
    return render_template("Busqueda.html", title='Buscar', segment='Buscar', tabla_naves=tabla_naves)