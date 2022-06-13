from io import open_code
from tkinter import *
from tkinter import messagebox #importo de tkinter para poder hacer una ventana emergente
from tkinter import ttk #Importo de tkinter para la creacion del scrollbar
import math #Para operaciones trigonométricas
import openpyxl #Importo openpyxl para trabajar con una planilla de Excel



root=Tk() #Creacion raiz


root.title("Calculo mecánico de conductores eléctricos-AEA 95301")
root.geometry ("1200x1200")

excel_document = openpyxl.load_workbook('prysalac.xlsx')  #Abro el documento Excel
sheet=excel_document.active #Seleccionamos el archivo

######################   CREACION DEL CANVAS QUE CONTENDRA LOS RESULTADOS    #####################

#Primero creamos un frame que contenga todo.
frameResultados=Frame (root) #Creacion del septimo frame.
frameResultados.pack(fill=BOTH,expand=1) #Empaquetamiento del septimo frame.

#Luego creamos un canvas (liezo)
miCanvas=Canvas (frameResultados)
miCanvas.pack (side=LEFT,fill=BOTH, expand=1)

#Agregamos el scrollbar al canvas
miBarra=ttk.Scrollbar (frameResultados,orient=VERTICAL, command=miCanvas.yview)
miBarra.pack(side=RIGHT, fill=Y)

#Configuramos el canvas
miCanvas.configure (yscrollcommand=miBarra.set)
miCanvas.bind ("<Configure>", lambda e: miCanvas.configure(scrollregion=miCanvas.bbox ("all")))

#Creamos otro frame dentro del canvas

resultados1=Frame (miCanvas)

#Agregamos el ultimo frame dentro del canvas

miCanvas.create_window((0,0),window=resultados1,anchor="nw")

#Creacion del label para el warning

warning1=Label(resultados1)
warning1.pack(side="left")

ingresoPeso=0
ingresoVano=0
ingresoDiamCable=0
ingresoVelMaxViento=0
ingresoZ=0
ingresoCantCondAl=0
ingresoCantCondAc=0
ingresoDiamAl=0
ingresoDiamAc=0
ingresoTensionRotura=0
ingresoCorriente=0
ingresoCorrienteAdmisible=0
zonaSeleccionada=0
nombre=0
descripcionproyecto=0
coefdil=0
moduloelastacidad=0
claseLinea=0
tipoExposicionL=0
FC=0



#***************************************************************FUNCIONES*******************************************************************
def SalirAplicacion (): #Funcion para que pregunta si se desea salir o no de la aplicacion.
    
    valor=messagebox.askquestion("Salir","Desea salir de la aplicacion?")

#Si el elijo si, la variable valor tiene el valor de "yes"

    if valor=="yes": 
        root.destroy() #Para  el programa.

def InfoAdicional(): #Funcion para mostrar aviso en una ventana emergente. Tengo que llamar con un command desde el subelemento
    #de AYUDA, Acerca de...
    
    messagebox.showinfo("Cálculo mecánico de conductores- Ing. Valentin Skinder","Datos utilizados de PRYSMIAN")

def NuevoProyecto(): #Función para abrir la ventana para cargar datos para la selección del cable.

    NuevoP=Toplevel() #Para que sea una ventana "hija"
    NuevoP.title("Ingreso de parámetros")
    NuevoP.geometry ("700x400")

    ########################################Pestañas#######################################

    #Incluimos panel para la pestañas

    pestanas= ttk.Notebook (NuevoP)
    pestanas.pack(fill="both", expand="yes")

    #Creamos pestañas
    p0=ttk.Frame(pestanas)
    p1=ttk.Frame(pestanas)
    p2=ttk.Frame(pestanas)
    p3=ttk.Frame(pestanas)
    p4=ttk.Frame(pestanas)
    p5=ttk.Frame(pestanas)

    #Agregamos pestañas

    pestanas.add (p0, text="Datos proyecto")
    pestanas.add (p1, text="Datos cable")
    pestanas.add (p2, text="Clases de líneas")
    pestanas.add (p3, text="Estados climáticos")
    pestanas.add (p4, text="Factor de terreno")
    pestanas.add (p5, text="CALCULAR")

    ################################### FUNCIONES PARA CALCULAR TODOS LOS PARÁMETROS  #############################
    
    def flecha(traccion,peso,vano,coefm): #Funcion para calcular la flecha vertical,horizontal y oblicua

        try:
            flechaR=((traccion/(peso*coefm))*(math.cosh((vano*peso*coefm)/(2*traccion))-1))

        except:

            flechaR=0

        return flechaR

    def cargaViento(factorTerreno,velocidadViento,factorCarga,factorRafaga,area):

        #factorTerreno (Zp)
        #velocidadViento(media o maxima en m/s)
        #factorCarga (FC)
        #factorRafaga (Gw)
        #area (con hielo y sin hielo)

        fv=round (((0.981)*(0.0613)*((factorTerreno*velocidadViento)**2)*factorCarga*factorRafaga*area),2)
        #Round sirve para redondear los decimales y recortarlos
        return fv

    def coeficientemyb(G, Fh, Fv):

        #G PESO DEL CABLE
        #Fh Carga por hielo
        #Fv Carga por viento
        
        m= (((((G + Fh)**2)+(Fv**2))**0.5)/G)
        b= math.degrees (math.atan (Fv/(Fh+G))) #Con degrees trabajo en grados. atan es arcotangente
        return m, b

    def ecuacionCubica (a,b,c,d): #Las entradas corresponden a: a´ , b´ y c´. Estos indices se obtienen
    #de hacer operaciones con la ecuación de cambio de estado.
    #a termino cubico, b termino cuadratico, c termino lineal, d termino independiente
    #En la ecuacion de cambio de estado no tenemos termino lineal

        p= ((3*a*c)-(b**2))/(3*(a**2))
        q= (((2*(b**3))-(9*a*b*c)+(27*(a**2)*d))/(27*(a**3)))
        delta= ((q**2)+ (4*(p**3)/27))

        if delta>0: #Una solucion real y dos complejas

            u= ((-q +(delta**0.5))/2)**(1/3)
            v= ((-q -(delta**0.5))/2)**(1/3)
            Th1=u+v-(b/(3*a))
            tension=Th1
        

        if delta==0: #Dos raices dobles y una simple

            Th1=((2*((-q/2)**(1/3)))-(b/(3*a)))
            Th2=(-((-q/2)**(1/3))-(b/(3*a))) #Esta es el mismo valor que Th3
            tension= max (Th1,Th2)
        
        
        if delta<0: #Tres soluciones reales

            tita=(math.acos(((3*q)/(2*p))*((-3/p)**(0.5))))
            Th1= 2 * ((-p/3)**(0.5)) * (math.cos(tita/3)) - (b/(3*a))
            Th2= 2 * ((-p/3)**(0.5)) * (math.cos((tita+2*math.pi)/3)) - (b/(3*a))
            Th3= 2 * ((-p/3)**(0.5)) * (math.cos((tita+4*math.pi)/3)) - (b/(3*a))
        
            tension= max (Th1,Th2,Th3) #Calcula el mayor de los tres valores
    
        return tension

    def ecuacionEstado(vano,pesoCable,alfa,temp,tempInicial,modElasticidad,seccionRealConductor,Th0,m0,m):

        #Realiza los calculos para los coeficientes de la ecuacion de estado.
        #Devuelve el valor de la tensión (raiz de la ecuacion de estado)
        #Vano [m]
        #pesoCable [Kg/m]
        #alfa (coeficiente de dilatacion lineal) [1/°C]
        #temp (temperatura del estado correspondiente)
        #tempInicial (temperatura del estado inicial V)
        #modElasticidad [Kg/mm2]
        #secionRealConductor [mm2]
        #Th0 (tension inicial)
        #m0 (coeficiente m del estado inicial V)
        #m (coeficiente m del estado correspondiente)

        termCubico= float ((1/(float (modElasticidad)*seccionRealConductor)))
        termCuadratico=float((alfa*(temp-tempInicial))-(Th0/((modElasticidad)*seccionRealConductor))+(((vano**2)*(m0**2)*(pesoCable**2))/((24*(Th0**2)))))
        terminoLineal=0
        terminoIndependiente=float (-(((vano**2)*(m**2)*(pesoCable**2))/((24))))

        tensionFinal=ecuacionCubica(termCubico,termCuadratico,terminoLineal,terminoIndependiente)
        
        return tensionFinal


    def Calculo ():

        global ingresoVano
        global ingresoPeso
        global ingresoVano
        global ingresoDiamCable
        global ingresoVelMaxViento
        global ingresoZ
        global ingresoCantCondAl
        global ingresoCantCondAc
        global ingresoDiamAl
        global ingresoDiamAc
        global ingresoTensionRotura
        global ingresoCorriente
        global ingresoCorrienteAdmisible
        global zonaSeleccionada
        global nombre
        global descripcionproyecto
        global coefdil
        global moduloelastacidad
        global claseLinea
        global tipoExposicionL
        global FC
        

            
        try:
            warning1.config(text="")
            # A continuación, las condiciones para seleccionar el tipo de cable

            if tipoC.get()==0: #cables "IRAM 2187"-coeficientes para el inicio del peso del cable

                a="H"   #Indice para la columna de peso del cable
                b=4     #Indice para ir iterando el numero de fila
                c="B"   #Indice para la columna del diametro de cable
                d="C"   #Indice para la columna de cantidad de conductores de aluminio
                e="E"   #Indice para la columna de cantidad de conductores de acero
                f="D"   #Indice para la columna de diametro de conductor de aluminio
                g="F"   #Indice para la columna de diametro de conductor de acero
                h="G"   #Indice para la columna de tension de rotura
                i="A"   #Indice para la columna de denominacion del cable
                j="J"   #Indice para la columna de corriente admisible del conductor
            
            
            else:   #cables "ASTM B232"-#coeficientes para el inicio del peso del cable

                a="J"    #Indice para la columna de peso del cable
                b=25     #Indice para ir iterando el numero de fila
                c="D"   #Indice para la columna del diametro de cable
                d="E"   #Indice para la columna de cantidad de conductores de aluminio
                e="G"   #Indice para la columna de cantidad de conductores de acero
                f="F"   #Indice para la columna de diametro de conductor de aluminio
                g="H"   #Indice para la columna de diametro de conductor de acero
                h="I"   #Indice para la columna de tension de rotura
                i="A"   #Indice para la columna de denominacion del cable
                j="L"   #Indice para la columna de corriente admisible del conductor
            
            # A continuación, se colocan los valores del factor de carga según la clase de línea

            if varOpcion.get()==0: #Clase de linea B

                FC=float (0.93)
                claseLinea="Clase B- Media Tensión (1 kV ≤ Vn ≤ 66 kV)"
            
            elif varOpcion.get()==1: #Clase de línea BB

                FC=float (1)
                claseLinea="Clase BB- Media Tensión con retorno por tierra (1 kV < Vn < 38 kV)"

            elif varOpcion.get()==2: #Clase de línea C

                FC=float (1.15)
                claseLinea="Clase C- Alta Tensión (66 kV ≤ Vn ≤ 220 kV)"

            elif varOpcion.get()==3: #Clase de línea D

                FC=float (1.30)
                claseLinea="Clase D- Extra Alta Tensión (220 kV ≤ Vn ≤ 800 kV)"

            elif varOpcion.get()==4: #Clase de línea E

                FC=float (1.4)
                claseLinea="Clase E- Ultra Alta Tensión ( Vn ≥ 800 kV)"

        # A continuación, las temperaturas segun los estados climáticos

            if listaDesplegable.current()==0:    #Zona climática A
            
                #[estado0,estadoI,estadoII,estadoIII,estadoIV,estadoV]
                temperaturas=[0,50,-5,10,20,20]
                esphielo=float (0)
                zonaSeleccionada="Zona A"

            elif listaDesplegable.current()==1:  #Zona climática B

                temperaturas=[50,45,-15,10,-5,16]
                esphielo=float (0)
                zonaSeleccionada="Zona B"

            elif listaDesplegable.current()==2:  #Zona climática C

                temperaturas=[50,45,-10,15,-5,16]
                esphielo=float (0)
                zonaSeleccionada="Zona C"

            elif listaDesplegable.current()==3:  #Zona climática D

                temperaturas=[50,35,-20,10,-5,8]
                esphielo=float (0.01)
                zonaSeleccionada="Zona D"

            elif listaDesplegable.current()==4:  #Zona climática E

                temperaturas=[50,35,-20,10,-5,9]
                esphielo=float (0)
                zonaSeleccionada="Zona E"

            elif listaDesplegable.current()==5:  #Ingreso de temperatura y hielo mediante cuadro de texto

                temperaturas=[float(labelT0E.get()),float(labelTIE.get()),float(labelTIIE.get()),float(labelTIIIE.get()),float(labelTIVE.get()),float(labelTVE.get())]
                esphielo=(float (labelMEE.get())/1000)
                zonaSeleccionada="Ingreso datos de forma personalizada"


        # A continuación, los distintos valores de ALPHA,K,LS y Zg segun el tipo de exposición

            if factorT.get()==0:    # Para exposición B

                ALPHA=float (4.5)
                K=float (0.010)
                LS=float (52)
                Zg=float (366)
                tipoExposicion="Exposición B-Zonas onduladas o forestadas, con numerosas obstrucciones de espacios cerrados, con la altura de las casas domésticas con promedio no superior a 10 m."

            elif factorT.get()==1:  # Para exposición C

                ALPHA=float (7.5)
                K=float (0.005)
                LS=float (67)
                Zg=float (274)
                tipoExposicion="Exposición C-Zonas llanas, poco onduladas con obstrucciones dispersas tales como cercas, árboles o construcciones muy aisladas,con alturas entre 1,5 y 10 m."


            elif factorT.get()==2:  # Para exposición D
            
                ALPHA=float (10)
                K=float (0.003)
                LS=float (76)
                Zg=float (213)
                tipoExposicion="Exposición D-Llanuras planas con pocas o ninguna obstrucción, con promedio de alturas de las posibles obstrucciones menor a 1,5 m."

            

            #Guardo en variables, los datos a ingresar en el bucle while

            ingresoPeso=float(sheet[str(a)+str(b)].value) #peso del cable [kg/m] de catálogo (Excel)
            ingresoVano=float(vanoE.get())  #vano [m]: Desde el entry "vanoE"
            ingresoDiamCable=float(sheet[str(c)+str(b)].value) #diámetro del cable [mm]
            ingresoVelMaxViento=float(entryViento.get())   #Velocidad máxima del viento, extraida el entry entryViento [m/s]
            ingresoZ=float (entryZ.get()) #Altura promedio a la que estara el cable, extraida del entry entryZ [m]
            ingresoCantCondAl=float(sheet[str(d)+str(b)].value) #cantidad de conductores de Aluminio de la tabla excel
            ingresoCantCondAc=float(sheet[str(e)+str(b)].value) #cantidad de conductores de Acero de la tabla excel
            ingresoDiamAl=float(sheet[str(f)+str(b)].value) #diametro del conductor de Aluminio de la tabla excel [mm]
            ingresoDiamAc=float(sheet[str(g)+str(b)].value) #diametro del conductor de Acero de la tabla excel [mm]
            ingresoTensionRotura=float(sheet[str(h)+str(b)].value) #Tension de rotura desde tabla excel [kg]
            ingresoCorriente=float(corrienteE.get()) #Corriente en A desde el entry "corrienteE"
            ingresoCorrienteAdmisible=float(sheet[str(j)+str(b)].value) #Corriente admisible del conductor desde tabla excel

            tensionE0=ingresoTensionRotura
            tensionEI=ingresoTensionRotura
            tensionEII=ingresoTensionRotura
            tensionEIII=ingresoTensionRotura
            tensionEIV=ingresoTensionRotura
            tensionEV=ingresoTensionRotura

            # Calculo las condiciones para ingresar en el bucle while

            condicion1=(ingresoTensionRotura*0.25)
            condicion2=(ingresoTensionRotura*0.70)

            while((ingresoCorriente>ingresoCorrienteAdmisible)or(tensionEV>(ingresoTensionRotura*0.25))or(tensionE0>condicion2)or(tensionEI>condicion2)or(tensionEII>condicion2)or(tensionEIII>condicion2)or(tensionEIV>condicion2)):
            
            #   Comienzo de los cálculos

                b=b+1   #Incremento el valor de b para iterar en las filas

                

                ingresoPeso=float(sheet[str(a)+str(b)].value) #peso del cable [kg/m] de catálogo (Excel)
                ingresoVano=float(vanoE.get())  #vano [m]: Desde el entry "vanoE"
                ingresoDiamCable=float(sheet[str(c)+str(b)].value) #diámetro del cable [mm]
                ingresoVelMaxViento=float(entryViento.get())   #Velocidad máxima del viento, extraida el entry entryViento [m/s]
                ingresoZ=float (entryZ.get()) #Altura promedio a la que estara el cable, extraida del entry entryZ [m]
                ingresoCantCondAl=float(sheet[str(d)+str(b)].value) #cantidad de conductores de Aluminio de la tabla excel
                ingresoCantCondAc=float(sheet[str(e)+str(b)].value) #cantidad de conductores de Acero de la tabla excel
                ingresoDiamAl=float(sheet[str(f)+str(b)].value) #diametro del conductor de Aluminio de la tabla excel [mm]
                ingresoDiamAc=float(sheet[str(g)+str(b)].value) #diametro del conductor de Acero de la tabla excel [mm]
                ingresoTensionRotura=float(sheet[str(h)+str(b)].value) #Tension de rotura desde tabla excel [kg]
                ingresoCorriente=float(corrienteE.get()) #Corriente en A desde el entry "corrienteE"
                ingresoCorrienteAdmisible=float(sheet[str(j)+str(b)].value) #Corriente admisible del conductor desde tabla excel


                pesodelCable=(ingresoPeso/1000)

                G=float ((pesodelCable)*(ingresoVano))    # CARGA PESO PROPIO DEL CABLE
                Fh=float ((3.141592)*(900)*ingresoVano*(esphielo)*(((ingresoDiamCable/1000))+esphielo))  # CARGA POR HIELO
                Zp=float ((1.61)*((ingresoZ/Zg)**(1/ALPHA)))   # Calculo del valor de Zp (factor de terreno)
                velMedia=float (ingresoVelMaxViento*0.40)  # Calculo del valor de velocidad media

                # Calculos para obtener el factor de ráfaga (Gw)

                E= float ((4.9)*(K**(0.5))*((10/ingresoZ)**(1/ALPHA)))
                Bw= float (1/ (1+(0.8* (ingresoVano/LS))))
                Gw= float (1+(2.7* E * (Bw**0.5)))

            # Calculos de la área expuesta al viento con y sin hielo

                areasinHielo= float (ingresoVano*(ingresoDiamCable/1000))
                
                areaconHielo= float (ingresoVano*((2*esphielo)+(ingresoDiamCable/1000))) # Área con hielo

            # CARGA POR VIENTO (SIN HIELO Y VIENTO MAXIMO)

                fv1=cargaViento (Zp,ingresoVelMaxViento,FC,Gw,areasinHielo)

            # CARGA POR VIENTO (SIN HIELO Y VIENTO MEDIO)

                fv2=cargaViento (Zp,velMedia,FC,Gw,areasinHielo)

            # CARGA POR VIENTO (CON HIELO Y VIENTO MEDIO)

                fv3=cargaViento (Zp,velMedia,FC,Gw,areaconHielo)

            
                if listaDesplegable.current()==0:    #Zona climática A

                # Coeficientes de sobrecarga "m" y "b". No lleva estado 0, porque ya tiene en el EI la temp. de 50°C
                
                    mE0, bE0= coeficientemyb (G,0,0)
                    mEI, bEI= coeficientemyb (G,0,0)
                    mEII, bEII= coeficientemyb (G,0,0)
                    mEIII, bEIII= coeficientemyb (G,0,fv1)
                    mEIV, bEIV= coeficientemyb (G,Fh,0)
                    mEV, bEV= coeficientemyb (G,0,0)

                    #Guardo los coeficientes obtenidos con la funcion "coeficientemyb" en dos listas apartes

                    coeficientesm=[mE0,mEI,mEII,mEIII,mEIV,mEV]
                    coeficientesb=[bE0,bEI,bEII,bEIII,bEIV,bEV]

                elif  listaDesplegable.current()==1:    #Zona climática B

                # Coeficientes de sobrecarga "m" y "b"

                    mE0, bE0= coeficientemyb (G,0,0)
                    mEI, bEI= coeficientemyb (G,0,0)
                    mEII, bEII= coeficientemyb (G,0,0)
                    mEIII, bEIII= coeficientemyb (G,0,fv1)

                    if esphielo==0:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv2)
                    else:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv3)

                    mEV, bEV= coeficientemyb (G,0,0)

                #Guardo los coeficientes obtenidos con la funcion "coeficientemyb" en dos listas apartes

                    coeficientesm=[mE0,mEI,mEII,mEIII,mEIV,mEV]
                    coeficientesb=[bE0,bEI,bEII,bEIII,bEIV,bEV]

                elif  listaDesplegable.current()==2:    #Zona climática C

                # Coeficientes de sobrecarga "m" y "b"

                    mE0, bE0= coeficientemyb (G,0,0)
                    mEI, bEI= coeficientemyb (G,0,0)
                    mEII, bEII= coeficientemyb (G,0,0)
                    mEIII, bEIII= coeficientemyb (G,0,fv1)
                    if esphielo==0:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv2)
                    else:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv3)
                    mEV, bEV= coeficientemyb (G,0,0)

                #Guardo los coeficientes obtenidos con la funcion "coeficientemyb" en dos listas apartes

                    coeficientesm=[mE0,mEI,mEII,mEIII,mEIV,mEV]
                    coeficientesb=[bE0,bEI,bEII,bEIII,bEIV,bEV]

                elif  listaDesplegable.current()==3:    #Zona climática D

                # Coeficientes de sobrecarga "m" y "b"

                    mE0, bE0= coeficientemyb (G,0,0)
                    mEI, bEI= coeficientemyb (G,0,0)
                    mEII, bEII= coeficientemyb (G,0,0)
                    mEIII, bEIII= coeficientemyb (G,0,fv1)
                    if esphielo==0:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv2)
                    else:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv3)
                    mEV, bEV= coeficientemyb (G,0,0)

                #Guardo los coeficientes obtenidos con la funcion "coeficientemyb" en dos listas apartes

                    coeficientesm=[mE0,mEI,mEII,mEIII,mEIV,mEV]
                    coeficientesb=[bE0,bEI,bEII,bEIII,bEIV,bEV]

                elif  listaDesplegable.current()==4:    #Zona climática E

                # Coeficientes de sobrecarga "m" y "b"

                    mE0, bE0= coeficientemyb (G,0,0)
                    mEI, bEI= coeficientemyb (G,0,0)
                    mEII, bEII= coeficientemyb (G,0,0)
                    mEIII, bEIII= coeficientemyb (G,0,fv1)
                    if esphielo==0:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv2)
                    else:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv3)
                    mEV, bEV= coeficientemyb (G,0,0)

                #Guardo los coeficientes obtenidos con la funcion "coeficientemyb" en dos listas apartes

                    coeficientesm=[mE0,mEI,mEII,mEIII,mEIV,mEV]
                    coeficientesb=[bE0,bEI,bEII,bEIII,bEIV,bEV]

                elif  listaDesplegable.current()==5:    #Ingreso de datos de forma personalizada

                # Coeficientes de sobrecarga "m" y "b"

                    mE0, bE0= coeficientemyb (G,0,0)
                    mEI, bEI= coeficientemyb (G,0,0)
                    mEII, bEII= coeficientemyb (G,0,0)
                    mEIII, bEIII= coeficientemyb (G,0,fv1)
                    if esphielo==0:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv2)
                    else:
                        mEIV, bEIV= coeficientemyb (G,Fh,fv3)
                    mEV, bEV= coeficientemyb (G,0,0)

                #Guardo los coeficientes obtenidos con la funcion "coeficientemyb" en dos listas apartes

                    coeficientesm=[mE0,mEI,mEII,mEIII,mEIV,mEV]
                    coeficientesb=[bE0,bEI,bEII,bEIII,bEIV,bEV]

            # Calculo y guardo en variables los valores maximos permitidos de tension que no deben pasar los valores calculados para cada estado

                condicion1=(ingresoTensionRotura*0.25)
                condicion2=(ingresoTensionRotura*0.70)

            #Calculo de la seccion del conjunto aluminio-acero y la real

                seccionAl=(math.pi*((ingresoDiamAl/2)**2)) #Calculo la seccion del Aluminio
                seccionAc=(math.pi*((ingresoDiamAc/2)**2)) #Calculo la seccion del Acero
                seccionReal=((ingresoCantCondAl*seccionAl)+(seccionAc*ingresoCantCondAc)) #Calculo de la seccion real del conjunto Aluminio-Acero
                tensionInicial= float (ingresoTensionRotura/4)

            #A continuacion calculo las tensiones finales para cada estado:

                tensionE0= ecuacionEstado (float(ingresoVano),pesodelCable,float(dillinealE.get()),temperaturas[0],temperaturas[5],float(modelasE.get()),seccionReal,tensionInicial,coeficientesm[5],coeficientesm[0])

                tensionEI= ecuacionEstado (float(ingresoVano),pesodelCable,float(dillinealE.get()),temperaturas[1],temperaturas[5],float(modelasE.get()),seccionReal,tensionInicial,coeficientesm[5],coeficientesm[1])

                tensionEII= ecuacionEstado (float(ingresoVano),pesodelCable,float(dillinealE.get()),temperaturas[2],temperaturas[5],float(modelasE.get()),seccionReal,tensionInicial,coeficientesm[5],coeficientesm[2])

                tensionEIII= ecuacionEstado (float(ingresoVano),pesodelCable,float(dillinealE.get()),temperaturas[3],temperaturas[5],float(modelasE.get()),seccionReal,tensionInicial,coeficientesm[5],coeficientesm[3])

                tensionEIV= ecuacionEstado (float(ingresoVano),pesodelCable,float(dillinealE.get()),temperaturas[4],temperaturas[5],float(modelasE.get()),seccionReal,tensionInicial,coeficientesm[5],coeficientesm[4])

                tensionEV= ecuacionEstado (float(ingresoVano),pesodelCable,float(dillinealE.get()),temperaturas[5],temperaturas[5],float(modelasE.get()),seccionReal,tensionInicial,coeficientesm[5],coeficientesm[5])

                listatensiones=[round (tensionE0,2),round (tensionEI,2),round (tensionEII,2),round (tensionEIII,2),round (tensionEIV,2),round (tensionEV,2)]

            cableSeleccionado=(sheet[str(i)+str(b)].value) #Obtengo el valor del cable seleccionado

            #####################   CALCULO DE FLECHAS  ##########################

            #VERTICAL mv=m*cos b    b es el coef. calculado junto con m

            flechaVE0=flecha(tensionE0,pesodelCable,ingresoVano,(mE0*(math.cos (math.radians (bE0)))))
            flechaVEI=flecha(tensionEI,pesodelCable,ingresoVano,(mEI*(math.cos (math.radians (bEI)))))
            flechaVEII=flecha(tensionEII,pesodelCable,ingresoVano,(mEII*(math.cos (math.radians (bEII)))))
            flechaVEIII=flecha(tensionEIII,pesodelCable,ingresoVano,(mEIII*(math.cos (math.radians (bEIII)))))
            flechaVEIV=flecha(tensionEIV,pesodelCable,ingresoVano,(mEIV*(math.cos (math.radians (bEIV)))))
            flechaVEV=flecha(tensionEV,pesodelCable,ingresoVano,(mEV*(math.cos (math.radians (bEV)))))

            #HORIZONTAL mv=m*sen b    b es el coef. calculado junto con m

            flechaHE0=flecha(tensionE0,pesodelCable,ingresoVano,(mE0*(math.sin (math.radians (bE0)))))
            flechaHEI=flecha(tensionEI,pesodelCable,ingresoVano,(mEI*(math.sin (math.radians (bEI)))))
            flechaHEII=flecha(tensionEII,pesodelCable,ingresoVano,(mEII*(math.sin (math.radians (bEII)))))
            flechaHEIII=flecha(tensionEIII,pesodelCable,ingresoVano,(mEIII*(math.sin (math.radians (bEIII)))))
            flechaHEIV=flecha(tensionEIV,pesodelCable,ingresoVano,(mEIV*(math.sin (math.radians (bEIV)))))
            flechaHEV=flecha(tensionEV,pesodelCable,ingresoVano,(mEV*(math.sin (math.radians (bEV)))))

            #OBLICUA 

            flechaOE0=flecha(tensionE0,pesodelCable,ingresoVano,mE0)
            flechaOEI=flecha(tensionEI,pesodelCable,ingresoVano,mEI)
            flechaOEII=flecha(tensionEII,pesodelCable,ingresoVano,mEII)
            flechaOEIII=flecha(tensionEIII,pesodelCable,ingresoVano,mEIII)
            flechaOEIV=flecha(tensionEIV,pesodelCable,ingresoVano,mEIV)
            flechaOEV=flecha(tensionEV,pesodelCable,ingresoVano,mEV)

            #Guardo los datos en listas para ser mostrados en la tabla

            flechasE0=[round (flechaVE0,2),round(flechaHE0,2),round(flechaOE0,2)]
            flechasEI=[round(flechaVEI,2),round(flechaHEI,2),round (flechaOEI,2)]
            flechasEII=[round(flechaVEII,2),round(flechaHEII,2),round(flechaOEII,2)]
            flechasEIII=[round (flechaVEIII,2),round (flechaHEIII,2),round(flechaOEIII,2)]
            flechasEIV=[round (flechaVEIV,2),round(flechaHEIV,2),round (flechaOEIV,2)]
            flechasEV=[round (flechaVEV,2),round(flechaHEV,2),round(flechaOEV,2)]
        #################################   RESULTADOS  ######################################

            label1=Label (resultados1,text="Datos del proyecto", font=("arial",18))
            label1.pack(anchor="center")

            nombre=nombreEntry.get()
            descripcionproyecto=(descripcionText.get('1.0', END))
            coefdil=dillinealE.get()
            moduloelastacidad=modelasE.get()
            tipoExposicionL=tipoExposicion

            label2=Label (resultados1,text="Proyectista: "+ nombre)
            label2.pack(anchor="center")

            label3=Message (resultados1,text="Descripcion del proyecto: "+ descripcionText.get('1.0', END),aspect=500)
            label3.pack(anchor="center")

            label4=Label (resultados1,text="Vano ingresado [m]: "+ str (ingresoVano))
            label4.pack(anchor="center")

            label5=Label (resultados1,text="La altura promedio del cable es [m]: "+str(ingresoZ))
            label5.pack(anchor="center")

            label6=Label (resultados1,text="Corriente del proyecto [A]: "+ str (ingresoCorriente))
            label6.pack(anchor="center")

            label7=Label (resultados1,text="Coeficiente de dilatacion lineal (alfa) [1/°C]: "+ str (coefdil))
            label7.pack(anchor="center")

            label8=Label (resultados1,text="Modulo de elasticidad [kg/mm2]: "+ str (moduloelastacidad))
            label8.pack(anchor="center")

            label9=Label (resultados1,text="La zona climática seleccionada es: "+str(zonaSeleccionada))
            label9.pack(anchor="center")

            label10=Label (resultados1,text="La velocidad máxima del viento es [m/s]: "+str(ingresoVelMaxViento))
            label10.pack(anchor="center")

            
            label11=Label (resultados1)
            label11.config (text="")
            label11.config (text=claseLinea)
            label11.pack(anchor="center")

            label12=Message (resultados1,text=tipoExposicion,aspect=800)
            label12.pack(anchor="center")

            #separadorR2=ttk.Separator(resultados,orient=HORIZONTAL)
            #separadorR2.grid (row=14,column=0,sticky="EW",columnspan=4)

            label13=Label (resultados1,text="Cable seleccionado", font=("arial",18))
            label13.pack(anchor="center")

        ################### TABLA PARA RESULTADO DEL CABLE SELECCIONADO ###################

            tabla=ttk.Treeview (resultados1,columns=[0,1,2,3,4],height=1) #Creo la tabla. Con la lista agregamos columnas
            tabla.pack(anchor="center")
        #Si bien la lista tiene dos elementos, el primer elemento es "#0"

        #DATOS DEL CONDUCTOR [diamExterior,seccionReal,peso unitario,cargaRotura,intensidadAdmisible]

            conductor=[ingresoDiamCable, round(seccionReal,2),ingresoPeso,ingresoTensionRotura,ingresoCorrienteAdmisible]


        #Asignamos a cada columna, un texto con "heading"
            tabla.heading("#0",text="Cable seleccionado")
            tabla.heading("0",text="Diámetro exterior [mm]")
            tabla.heading("1",text="Sección real [mm2]")
            tabla.heading("2",text="Masa aproximada [Kg/km]")
            tabla.heading("3",text="Carga de rotura [Kg]")
            tabla.heading("4",text="Corriente admisible [A]")

        #Ajustamos el ancho de las columnas de la tabla

            tabla.column ("#0",minwidth=120,width=120,anchor="center")
            tabla.column ("0",minwidth=150,width=150,anchor="center")
            tabla.column ("1",minwidth=150,width=150,anchor="center")
            tabla.column ("2",minwidth=150,width=150,anchor="center")
            tabla.column ("3",minwidth=150,width=150,anchor="center")
            tabla.column ("4",minwidth=150,width=150,anchor="center")

        #Coloco los valores del cable seleccionado en la tabla
            tabla.insert("", END, text=str(cableSeleccionado), values=(conductor))

        ################### TABLA PARA RESULTADO DEL CABLE SELECCIONADO ###################

            #[Temperatura,Peso propio,Carga hielo, Carga viento, m,b,Traccion]

            if listaDesplegable.current()==0:    #Zona climática A

                fila0=[temperaturas[0],0,0,0,0,0,round (tensionE0,2)]
            else:

                fila0=[temperaturas[0],G,0,0,round (mE0,2),round (bE0,2),round (tensionE0,2)]

            filaI=[temperaturas[1],round (G,2),0,0,round(mEI,2),round (bEI,2),round(tensionEI,2)]
            filaII=[temperaturas[2],round (G,2),0,0,round(mEII,2),round (bEII,2),round(tensionEII,2)]
            filaIII=[temperaturas[3],round (G,2),0,round (fv1,2),round (mEIII,2),round(bEIII,2),round(tensionEIII)]
            filaIV=[temperaturas[4],round (G,2),round (Fh,2),round (fv3,2),round (mEIV,2),round (bEIV,2),round(tensionEIV,2)]
            filaV=[temperaturas[5],round (G,2),0,0,round (mEV,2),round (bEV,2),round (tensionEV,2)]

            label14=Label (resultados1,text="Cargas y tracciones", font=("arial",18))
            label14.pack(anchor="center")

            tabla2=ttk.Treeview (resultados1,columns=[0,1,2,3,4,5,6],height=6) #Creo la tabla. Con la lista agregamos columnas
            tabla2.pack(anchor="center")

            tabla2.heading("#0",text="ESTADO")
            tabla2.heading("0",text="Temperatura [°C]")
            tabla2.heading("1",text="Peso propio (G)[Kg]")
            tabla2.heading("2",text="Carga por hielo (Fh)[Kg]")
            tabla2.heading("3",text="Carga por viento (Fv)[Kg]")
            tabla2.heading("4",text="Coef.m")
            tabla2.heading("5",text="Coef.b")
            tabla2.heading("6",text="Tracción [Kg]")
            
        #Ajustamos el ancho de las columnas de la tabla

            tabla2.column ("#0",minwidth=110,width=110,anchor="center")
            tabla2.column ("0",minwidth=120,width=120,anchor="center")
            tabla2.column ("1",minwidth=120,width=120,anchor="center")
            tabla2.column ("2",minwidth=135,width=135,anchor="center")
            tabla2.column ("3",minwidth=140,width=140,anchor="center")
            tabla2.column ("4",minwidth=90,width=90,anchor="center")
            tabla2.column ("5",minwidth=90,width=90,anchor="center")
            tabla2.column ("6",minwidth=110,width=110,anchor="center")
            
            tabla2.insert("", END, text="ESTADO 0", values=(fila0))
            tabla2.insert("", END, text="ESTADO I", values=(filaI))
            tabla2.insert("", END, text="ESTADO II", values=(filaII))
            tabla2.insert("", END, text="ESTADO III", values=(filaIII))
            tabla2.insert("", END, text="ESTADO IV", values=(filaIV))
            tabla2.insert("", END, text="ESTADO V", values=(filaV))

            label15=Label (resultados1,text="Calculo de flechas", font=("arial",18))
            label15.pack(anchor="center")

            tabla3=ttk.Treeview (resultados1,columns=[0,1,2],height=6) #Creo la tabla. Con la lista agregamos columnas
            tabla3.pack(anchor="center")

            tabla3.heading("#0",text="ESTADO")
            tabla3.heading("0",text="Flecha vertical [m]")
            tabla3.heading("1",text="Flecha horizontal [m]")
            tabla3.heading("2",text="Flecha oblicua [m]")
            
            #Ajustamos el ancho de las columnas de la tabla

            tabla3.column ("#0",minwidth=110,width=110,anchor="center")
            tabla3.column ("0",minwidth=120,width=120,anchor="center")
            tabla3.column ("1",minwidth=120,width=120,anchor="center")
            tabla3.column ("2",minwidth=135,width=135,anchor="center")

            tabla3.insert("", END, text="ESTADO 0", values=(flechasE0))
            tabla3.insert("", END, text="ESTADO I", values=(flechasEI))
            tabla3.insert("", END, text="ESTADO II", values=(flechasEII))
            tabla3.insert("", END, text="ESTADO III", values=(flechasEIII))
            tabla3.insert("", END, text="ESTADO IV", values=(flechasEIV))
            tabla3.insert("", END, text="ESTADO V", values=(flechasEV))
            
    
        except:

            warning1.config (text="Ha ingresado datos incorrectos. Verifique", font=("arial",18))   #Titulo         
  

    

    ######################################     DATOS PROYECTO   ##################################

    f0=Frame (p0)   #Frame para titulo
    f0.pack()

    t0= Label (f0, text="Datos del proyecto", font=("arial",18))   #Titulo
    t0.grid (row=0,column=0)

    separador1=ttk.Separator(f0,orient=HORIZONTAL)
    separador1.grid (row=1,column=0,sticky="EW",columnspan=4)

    f01=Frame (p0)   #Frame para carga de datos
    f01.pack()

    nombreLabel=Label (f01,text="Proyectista: ")
    nombreLabel.grid (row=0,column=0,padx=10,pady=10)

    nombreEntry=Entry (f01)
    nombreEntry.grid (row=0,column=1,padx=10,pady=10)
    nombreEntry.insert (0,"Nombre y Apellido")   #Para insertar el valor predeterminado
    
    vano=Label (f01, text="Vano [m]: ")  #Label para VANO
    vano.grid (row=1,column=0)

    vanoE= Entry (f01,justify="right")   #Cuadro de texto para VANO
    vanoE.grid (row=1,column=1,padx=10,pady=10)
    vanoE.insert (0,"0")   #Para insertar el valor predeterminado

    corriente=Label (f01, text="Corriente del proyecto [A]: ")  #Label para CORRIENTE
    corriente.grid (row=2,column=0)

    corrienteE= Entry (f01,justify="right")   #Cuadro de texto para CORRIENTE
    corrienteE.grid (row=2,column=1,padx=10,pady=10)
    corrienteE.insert (0,"0")   #Para insertar el valor predeterminado

    labelZ=Label (f01,text="Z-Altura promedio del conductor [m]: ")    #Label para indicar el Z.
    labelZ.grid (row=3,column=0)

    entryZ=Entry (f01,justify="right")  #Entry para ingresar el valor de Z.
    entryZ.grid (row=3,column=1)
    entryZ.insert (0,"0")   #Para insertar el valor predeterminado

    descripcionLabel=Label (f01,text="Descripcion del proyecto: ")
    descripcionLabel.grid (row=4,column=0,padx=10,pady=10)

    descripcionText=Text (f01, width=40, height=10)
    descripcionText.grid (row=4,column=1,padx=10,pady=10)

    Scrollbardescripcion=Scrollbar (f01,command=descripcionText.yview) #Con command indico que la barra de desplazamiento
    #va a pertenecer a "descripcionText" y va a ser vertical (yview)
    Scrollbardescripcion.grid (row=4,column=2,sticky="nsew")# Con sticky="nsew" hago que se adapte al alto del cuadro de texto

    ######################################     DATOS CABLE   #####################################

    f1=Frame (p1)   #Frame para titulo
    f1.pack()

    t1= Label (f1, text="Datos cable", font=("arial",18))   #Titulo
    t1.grid (row=0,column=0)

    separador2=ttk.Separator(f1,orient=HORIZONTAL)
    separador2.grid (row=1,column=0,sticky="EW",columnspan=4)

    tipoC=IntVar ()

    f2= Frame(p1)   #Frame para carga de datos
    f2.pack()
    
    vano=Label (f2, text="Tipo de cable PRYSMIAN: ")  #Label para TIPO DE CABLE
    vano.grid (row=0,column=0)

    r1=Radiobutton (f2, text="IRAM 2187",value=0,variable=tipoC,padx=10,pady=10)
    r1.grid (row=1,column=0)

    r2=Radiobutton (f2, text="ASTM B232",value=1,variable=tipoC,padx=10,pady=10)
    r2.grid (row=1,column=1)

    separador3=ttk.Separator(f2,orient=HORIZONTAL)
    separador3.grid (row=2,column=0,sticky="EW",columnspan=4)

    dillineal=Label (f2, text="Coeficiente de dilatación lineal (alfa) [1/°C]: ") #Label para coeficiente de dilatación lineal
    dillineal.grid (row=3,column=0)

    dillinealE= Entry (f2,justify="right")  #Cuadro de texto para coeficiente de dilatación lineal
    dillinealE.grid (row=3,column=1,padx=10,pady=10)
    dillinealE.insert (0,"0.0000189")   #Para insertar el valor predeterminado

    modelas=Label (f2, text="Modulo de elasticidad [kg/mm2]: ") #Label para modulo de elasticidad
    modelas.grid (row=4,column=0)

    modelasE= Entry (f2,justify="right")  #Cuadro de texto para modulo de elasticidad
    modelasE.grid (row=4,column=1,padx=10,pady=10)
    modelasE.insert (0,"7854")  #Para insertar el valor predeterminado

    separador2a=ttk.Separator(f2,orient=HORIZONTAL)
    separador2a.grid (row=5,column=0,sticky="EW",columnspan=4)

    f2a= Frame(p1)   #Frame para carga de datos
    f2a.pack()

    labelIRAM=Label (f2a,text="Para cables IRAM la corriente máxima a ingresar es 1000 A")
    labelIRAM.pack(anchor="center")
    labelASTM=Label (f2a,text="Para cables ASTM la corriente máxima a ingresar es 1232 A")
    labelASTM.pack(anchor="center")

    ############################################    CLASES DE LÍNEAS  ############################################

    f3=Frame (p2)   #Frame para titulo
    f3.pack()

    t2= Label (f3, text="Clases de líneas", font=("arial",18))   #Titulo
    t2.grid (row=0,column=0)

    separador4=ttk.Separator(f3,orient=HORIZONTAL)
    separador4.grid (row=1,column=0,sticky="EW",columnspan=4)

    f4=Frame (p2)   #Frame para radios button de clases de líneas
    f4.pack()

    ###################Creación de variable y función para determinar el factor de carga segun la clase de la línea###############

    f5=Frame (p2)   #Frame para indicar resultados del factor de carga
    f5.pack()

    labelFC=Label (f5)
    labelFC.grid (row=2, column=0)

    varOpcion= IntVar()

    # Creación de radios button para las clases de líneas

    cb= Radiobutton (f4, text="Clase B- Media Tensión (1 kV ≤ Vn ≤ 66 kV)",variable=varOpcion, value=0)
    cb.pack (anchor="center")

    cbb=Radiobutton (f4, text="Clase BB- Media Tensión con retorno por tierra (1 kV < Vn < 38 kV)",variable=varOpcion, value=1)
    cbb.pack (anchor="center")

    cc=Radiobutton (f4, text="Clase C- Alta Tensión (66 kV ≤ Vn ≤ 220 kV)",variable=varOpcion, value=2)
    cc.pack (anchor="center")

    cd=Radiobutton (f4, text="Clase D- Extra Alta Tensión (220 kV ≤ Vn ≤ 800 kV)",variable=varOpcion, value=3)
    cd.pack (anchor="center")

    ce=Radiobutton (f4, text="Clase E- Ultra Alta Tensión ( Vn ≥ 800 kV)",variable=varOpcion, value=4)
    ce.pack (anchor="center")

    ############################################    ESTADOS CLIMÁTICOS  ############################################

    f6=Frame (p3)   #Frame para titulo
    f6.pack()

    t3= Label (f6, text="Estados climáticos", font=("arial",18))   #Titulo
    t3.grid (row=0,column=0)

    f7=Frame (p3)   #Frame para radios button de estados climáticos
    f7.pack()

    def cambioTemp(event):  #Funcion para colocar los valores de temperatura en los entry

        def datos():

            labelT0E.insert (0,str(temperaturas[0]))  #Para insertar el valor predeterminado
            labelTIE.insert (0,str(temperaturas[1]))
            labelTIIE.insert (0,str(temperaturas[2]))
            labelTIIIE.insert (0,str(temperaturas[3]))
            labelTIVE.insert (0,str(temperaturas[4]))
            labelTVE.insert (0,str(temperaturas[5]))
            if listaDesplegable.current()==3: 
                labelMEE.insert (0,str(10))
            else:
                labelMEE.insert (0,str(0))
            labelT0E.config (state="readonly")
            labelTIE.config (state="readonly")
            labelTIIE.config (state="readonly")
            labelTIIIE.config (state="readonly")
            labelTIVE.config (state="readonly")
            labelTVE.config (state="readonly")
            labelMEE.config (state="readonly")

        labelT0E.config(state="normal") #Habilito los entry
        labelTIE.config(state="normal")
        labelTIIE.config(state="normal")
        labelTIIIE.config(state="normal")
        labelTIVE.config(state="normal")
        labelTVE.config(state="normal")
        labelMEE.config(state="normal")

        labelT0E.delete (0,END) #Borro lo ingresado en los cuadro de texto.
        labelTIE.delete (0,END)
        labelTIIE.delete (0,END)
        labelTIIIE.delete (0,END)
        labelTIVE.delete (0,END)
        labelTVE.delete (0,END)
        labelMEE.delete (0,END)

        #Dependiendo lo seleccionado en la lista desplegable ingreso los valores

        if listaDesplegable.current()==0:   #Zona A
            temperaturas=[0,50,-5,10,20,20]
            datos()
    
        elif listaDesplegable.current()==1: #Zona B

            temperaturas=[50,45,-15,10,-5,16]
            datos()

        elif listaDesplegable.current()==2: #Zona C

            temperaturas=[50,45,-10,15,-5,16]
            datos()
            
        elif listaDesplegable.current()==3: #Zona D

            temperaturas=[50,35,-20,10,-5,8]
            datos()
            
        elif listaDesplegable.current()==4: #Zona E

            temperaturas=[50,35,-20,10,-5,9]
            datos()
        
        elif listaDesplegable.current()==5: #Ingreso personalizado de valores.Habilito los entry

            labelT0E.config(state="normal") #Habilito los entry
            labelTIE.config(state="normal")
            labelTIIE.config(state="normal")
            labelTIIIE.config(state="normal")
            labelTIVE.config(state="normal")
            labelTVE.config(state="normal")
            labelMEE.config(state="normal")
            labelT0E.insert (0,str(0))  #Para insertar el valor predeterminado
            labelTIE.insert (0,str(0))
            labelTIIE.insert (0,str(0))
            labelTIIIE.insert (0,str(0))
            labelTIVE.insert (0,str(0))
            labelTVE.insert (0,str(0))
            labelMEE.insert (0,str(0))


    #Creación de la lista desplegable para los estados climáticos

    listaDesplegable=ttk.Combobox(f6,width=20)
    listaDesplegable.grid (row=0,column=1)

    opcionesLista=["Zona A","Zona B","Zona C","Zona D","Zona E","Ingreso de valores"]

    listaDesplegable["values"]=opcionesLista
    listaDesplegable.bind ("<<ComboboxSelected>>",cambioTemp)
    #Con "<<ComboboxSelected>>",cambioTemp" llamo a la funcion cada vez que cambio de opcion en la lista desplegable
    
    separador5=ttk.Separator(f6,orient=HORIZONTAL)
    separador5.grid (row=1,column=0,sticky="EW",columnspan=4)


    labelT0=Label (f7,text="Temperatura-E0 [°C]:")
    labelT0.grid (row=1,column=0,padx=5,pady=5)

    labelT0E=Entry (f7,justify="right",width=5,state="readonly")
    labelT0E.grid (row=1,column=1,padx=5,pady=5)
    
    labelTI=Label (f7,text="Temperatura-EI [°C]:")
    labelTI.grid (row=2,column=0,padx=5,pady=5)

    labelTIE=Entry (f7,justify="right",width=5,state="readonly")
    labelTIE.grid (row=2,column=1,padx=5,pady=5)

    labelTII=Label (f7,text="Temperatura-EII [°C]:")
    labelTII.grid (row=3,column=0,padx=5,pady=5)

    labelTIIE=Entry (f7,justify="right",width=5,state="readonly")
    labelTIIE.grid (row=3,column=1,padx=5,pady=5)

    labelTIII=Label (f7,text="Temperatura-EIII [°C]:")
    labelTIII.grid (row=4,column=0,padx=5,pady=5)

    labelTIIIE=Entry (f7,justify="right",width=5,state="readonly")
    labelTIIIE.grid (row=4,column=1,padx=5,pady=5)

    labelTIV=Label (f7,text="Temperatura-EIV [°C]:")
    labelTIV.grid (row=5,column=0,padx=5,pady=5)

    labelTIVE=Entry (f7,justify="right",width=5,state="readonly")
    labelTIVE.grid (row=5,column=1,padx=5,pady=5)

    labelTV=Label (f7,text="Temperatura-EV [°C]:")
    labelTV.grid (row=6,column=0,padx=5,pady=5)

    labelTVE=Entry (f7,justify="right",width=5,state="readonly")
    labelTVE.grid (row=6,column=1,padx=5,pady=5)

    labelMH=Label (f7,text="Espesor manguito de hielo [mm]:")
    labelMH.grid (row=7,column=0,padx=5,pady=5)

    labelMEE=Entry (f7,justify="right",width=5,state="readonly")
    labelMEE.grid (row=7,column=1,padx=5,pady=5)

    separador6=ttk.Separator(f7,orient=HORIZONTAL)
    separador6.grid (row=8,column=0,sticky="EW",columnspan=4)

    labelViento=Label (f7, text="Velocidad máxima del viento [m/s]: (ver isocletas) ",padx=10,pady=10)    #Label para velocidad del viento máxima
    labelViento.grid (row=9,column=0)

    entryViento= Entry (f7,justify="right",width=5) #Entry para colocar la velocidad del viento máxima
    entryViento.grid (row=9,column=1)

    separador7=ttk.Separator(f7,orient=HORIZONTAL)
    separador7.grid (row=10,column=0,sticky="EW",columnspan=4)

    def mostrarMapa(): #Función para mostrar la imagen del mapa de Argentina con los estados climáticos
        
        imagen=Toplevel () #Creacion de ventana que contiene la imagen con el mapa de Argentina y los estados climáticos
        imagen.title("Estados climáticos")
        imagen.geometry ("700x600")
        fondoimagen=PhotoImage (file="mapa.PNG")
        fondo=Label (imagen,image=fondoimagen).place(x=0,y=0)

        imagen.mainloop()

    
    f8a=Frame (p3)   #Frame para boton que muestra mapa con los estados climáticos
    f8a.pack()

    botonEC=Button (f8a,text="Mapa Argentina-Estados climáticos e isocletas",command=mostrarMapa,padx=10,pady=10)
    botonEC.pack()
    
    
################################################    FACTOR DE TERRENO   ##########################################
  
    f9=Frame (p4)   #Frame para el titulo de factor de terreno
    f9.pack()

    t4= Label (f9, text="Factor de terreno", font=("arial",18))   #Titulo
    t4.grid (row=0,column=0)

    separador8=ttk.Separator(f9,orient=HORIZONTAL)
    separador8.grid (row=1,column=0,sticky="EW",columnspan=4)

    f10=Frame (p4)   #Frame para los radio button de factor de terreno
    f10.pack()

    factorT=IntVar()

    # Creación de variables que contienen el texto para los labels para cada exposición

    textoexpB="""Zonas onduladas o forestadas, con numerosas obstrucciones de espacios cerrados, con la altura de las casas
     domésticas con promedio no superior a 10 m. Por ejemplo áreas industriales o suburbios de grandes ciudades. 
     Es necesario que la línea este a menos de 500 m, o 10 veces la altura libre de la estructura, dentro de esta zona."""
    textoexpC="""Zonas llanas, poco onduladas con obstrucciones dispersas tales como cercas, árboles o construcciones muy aisladas,
     con alturas entre 1,5 y 10 m. Por ejemplo: campo abierto, granjas o sembrados. Esta exposición es la representativa del terreno 
     de aeropuertos donde son efectuadas las mediciones de la velocidad del viento."""
    textoexpD="""Llanuras planas con pocas o ninguna obstrucción, con promedio de alturas de las posibles obstrucciones menor a 1,5 m.
     Es necesario que la línea este a no más de 100 m. Por ejemplo: fajas costeras, llanuras sin árboles, mesetas desérticas o 
     pantanos"""
    
    #Creación de radios button para Factores de terreno

    expb=Radiobutton (f10, text="Exposición B",variable=factorT, value=0,padx=10,pady=10)
    expb.grid (row=0,column=0)

    labelexpB=Label (f10, text=textoexpB,wraplength=1000,padx=10,pady=10)    #Label exposición B
    labelexpB.grid (row=1, column=0)

    separador9=ttk.Separator(f10,orient=HORIZONTAL)
    separador9.grid (row=2,column=0,sticky="EW",columnspan=4)

    expc=Radiobutton (f10, text="Exposición C",variable=factorT,value=1,padx=10,pady=10)
    expc.grid (row=3,column=0)

    labelexpC=Label (f10, text=textoexpC,wraplength=1000,padx=10,pady=10)    #Label exposición C
    labelexpC.grid (row=4, column=0)

    separador10=ttk.Separator(f10,orient=HORIZONTAL)
    separador10.grid (row=5,column=0,sticky="EW",columnspan=4)

    expd=Radiobutton (f10, text="Exposición D",variable=factorT, value=2,padx=10,pady=10)
    expd.grid (row=6,column=0)

    labelexpD=Label (f10, text=textoexpD,wraplength=1000,padx=10,pady=10)    #Label exposición D
    labelexpD.grid (row=7, column=0)


########################################### CALCULAR ##################################################

    f11=Frame (p5)   #Frame para el titulo de CALCULAR
    f11.pack()

    t5= Label (f11, text="Calcular", font=("arial",18))   #Titulo
    t5.grid (row=0,column=0)

    separador11=ttk.Separator(f11,orient=HORIZONTAL)
    separador11.grid (row=1,column=0,sticky="EW",columnspan=4)

    f12=Frame (p5)   #Frame para el botón de calcular
    f12.pack()

    botonCalcular=Button (f12, text="CALCULAR",command=Calculo)
    botonCalcular.grid (row=0,column=0)
    botonCalcular.config(width=35,height=2)


    NuevoP.mainloop()
#****************************************************************Creación del menu**********************************************************

#Creacion del menu.

barraMenu=Menu (root) #Creacion de variable, y le decimos a donde va a pertenecer (root).

root.config (menu=barraMenu, width=300,height=300)

#Establecemos cuantos elementos va a contener el menu.

#Elemento ARCHIVO

archivoMenu=Menu (barraMenu,tearoff=0) #Con tearoff es para eliminar una linea dentro del submenu.

archivoMenu.add_command(label="Nuevo proyecto", command=NuevoProyecto) #Para agregar un subelemento al elemento ARCHIVO. A continuacion agregamos otros subelementos:

archivoMenu.add_separator() #Esto es para hacer una linea que separa los elementos del submenu. Tenemos que colocarla en la parte del codigo
#que querramos separar.

archivoMenu.add_command(label="Salir",command=SalirAplicacion)

#Elemento AYUDA

archivoAyuda=Menu (barraMenu,tearoff=0)

#Creamos subelementos para AYUDA

archivoAyuda.add_command(label="Acerca de...",command=InfoAdicional)#Con command llamo a la funcion para mostrar la ventana emergente.

#Especificamos los nombres de cada elemento del menu de la siguiente manera:

barraMenu.add_cascade (label="Archivo",menu=archivoMenu) #El elemento archivo menu, perteneciente a la barra menu, tendra el nombre de archivo.

barraMenu.add_cascade (label="Ayuda",menu=archivoAyuda)











root.mainloop()