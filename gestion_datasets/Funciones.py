#######################################################################################################
#FUNCIONES PYTHON
#Autor: Jon Lorenzo Insausti
#Fecha: 23/10/2026
#En este script se incluyen todas las funciones implementadas en el documento de la entrega final, con una explicacion detallando sus entradas, salidas y funcionamiento interno.
#######################################################################################################


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##ALGORITMOS DE DISCRETIZACION
#discretizacion por igual anchura
def discretizeEW(x, num_bins):  #vector y numero de bloques como entradas
  """Discretiza un vector numerico en grupos de igual anchura.
  Entradas: x (vector numerico), num_bins (numero de intervalos).
  Salida: diccionario con solucion (etiquetas de intervalo) y limites.
  """
  clase = True
  if len(x) == 0: #comprueba que el vector no este vacio
    raise ValueError('El vector no puede estar vacio.')
  if type(num_bins) != int or num_bins <= 0: #comprueba que el numero de grupos sea un entero positivo
    raise ValueError('El numero de intervalos debe ser un entero positivo.') 

  for i in range(len(x)): #La funcion solo funciona para valores numericos o enteros
    if not isinstance(x[i], (int, float, np.integer, np.floating)):
        clase = False

  if clase==True: #si los valores son numericos, hace la discretizacion
    solucion = []
    longB = (max(x)-min(x))/num_bins  #la longitud de cada categoria de la discretizacion depende de los valores maximos y minimos a discretizar y del numero de grupos deseados
    limites = []
    etiquetas = []
    limites.append(float('-inf')) #define el limite inferior

    for i in range(1,num_bins): #define los limites entre grupos
        limites.append(min(x) + longB * i)
    limites.append(float('inf')) #define el limite superior

    for j in range(len(x)): #discretiza el vector, para ello recorre cada elemento
       for k in range(len(limites)-1): #recorre todos los limites que sirven como frontera
          if limites[k]<x[j] and x[j]<=limites[k+1]: #si el elemento de x esta entre esos dos limites que definen un grupo, entra al bucle
            etiquetas.append('I'+str(k+1)) #escribe el nombre del intervalo
            if limites[k+1]==float('inf'): #escribe la solucion del elemento si este pertenece al ultimo grupo (para poner parentesis al final y ser correctos matematicamente)
               solucion.append('(' + str(limites[k]) + ',' + str(limites[k + 1]) + ')')
            else: #escribe la solucion para todos los grupos menos el primero, y la mete en la lista de soluciones
               solucion.append('(' + str(limites[k]) + ',' + str(limites[k + 1]) + ']')
    return{'solucion' : solucion, 'etiquetas': etiquetas, 'limites' : limites} 
  #devuelve tres elementos: la solucion, las etiquetas que indican el numero de grupo de cada elemento y los limites usados para la discretizacion
  
  else: #si los elementos del vector no son numericos, provoca un error de tipo/clase.
    raise TypeError('Esta funcion solo sirve para vectores numericos.')


#funcion para ordenar los elementos de un vector (descendente o ascendente)
def ordenar(x, descendente=False): #dos entradas, el vector a ordenar y si el orden es descendente o no
    """Ordena manualmente un vector manteniendo indices originales (desde 0).
    Entradas: x (vector), descendente (booleano).
    Salida: diccionario con vector ordenado y orden de indices.
    """
    xx=list(range(len(x))) #se inicializan las variables para luego guardar los resultados
    orden= list(range(len(x)))

    for i in range(len(x)): #bucle que recorre todos los elementos del vector. Este elemento i es el que queremos ordenar
        posicion = 0 #inicializa la posicion en el vector ordenado
        for j in range(len(x)): #recorre el vector original y compara nuestro elemento i con cada elemento del vector
            if descendente==True and  (x[j] > x[i]): #si el orden deseado es descendente, suma +1 en la posicion en caso de que sea menor
               posicion +=1
            elif descendente==False and  (x[j] < x[i]): #si el orden deseado es ascendente, suma +1 en la posicion en caso de que sea mayor
               posicion += 1
        for j in range(i):  #recorre los elementos ya colocados antes de nuestro elemento a colocar
            if x[j] == x[i]: #en caso de igualdad, se guarda nuestro elemento una posicion mas adelante en el vector nuevo
               posicion += 1
        xx[posicion] = x[i] #guarda el elemento en su nueva posicion
        orden[posicion] = i #guarda la posicion original

    return {'vector': xx, 'orden': orden} #devuelve el vector ordenado y la posicion original


#discretizacion por frecuencia
def discretizeEF(x, num_bins): #inputs: vector y numero de bloques
    """Discretiza un vector numerico en grupos de igual frecuencia.
    Entradas: x (vector numerico), num_bins (numero de grupos).
    Salida: diccionario con solucion, etiquetas y limites.
    """
    if len(x) == 0: #comprueba que el vector no este vacio 
        raise ValueError('El vector no puede estar vacio.') #si no es asi, provoca un error
    if type(num_bins) != int or num_bins <= 0 or num_bins > len(x): #comprueba que el numero de intervalos este dentro del rango permitido
        raise ValueError('El numero de intervalos debe estar entre 1 y len(x).') #aqui tambien provoca error en caso de no ser asi
    
    clase = True
    for i in range(len(x)): #comprueba que el vector este lleno de valores numericos
        if not isinstance(x[i], (int, float, np.integer, np.floating)):
            clase = False

    if clase == True: #si el vector es apropiado para la funcion, sigue adelante
        resultado = ordenar(x, False) #ordena los elementos del vector original
        xx = resultado['vector'] #guarda el vector ordenado
        orden = resultado['orden'] #guarda las posiciones originales
        longgrupo = len(x) // num_bins #longitud de cada grupo
        resto = len(x) % num_bins #resto de la division anterior
        limites = [float('-inf')] #se fija el limite inferior
        etiquetas = [] #inicializa para luego guardar resultados
        intervalos = []
        cont = 0

        for i in range(num_bins): #con el siguiente for se construye el vector de las soluciones, recorre el for tantas veces como grupos hay
            if i < resto: #si el numero de grupo es inferior al resto, el grupo tendra un elemento mas
                #si el resto es 0, todos los grupos seran iguales
                tamano = longgrupo + 1
            else: 
                tamano = longgrupo
            subgrupo = []

            for j in range(tamano): #recorre el for tamano veces, siendo tamano la longitud del grupo
                subgrupo.append(xx[cont]) # mete a cada elemento en el subgrupo correspondiente
                etiquetas.append('I' + str(i + 1)) #crea la etiqueta del grupo actual y la guarda
                cont += 1 #para guardar cada elemento del subgrupo bien
            limites.append(subgrupo[-1]) #suma a los limites el ultimo elemento de cada subgrupo

            for j in range(tamano): #recorre el for tamano veces
                if i == num_bins - 1: #si es el ultimo grupo, utiliza infinito como limite superior
                    intervalo = '(' + str(limites[i]) + ',inf)'
                else: #construye el intervalo usando los limites inferior y superior
                    intervalo = '(' + str(limites[i]) + ',' + str(limites[i+1]) + ']'
                intervalos.append(intervalo) #guarda el intervalo correspondiente a cada elemento
        limites[-1] = float('inf') #sustituye el ultimo limite superior por infinito
        solucion = list(range(len(x))) #inicializa el vector donde se guardaran los intervalos en el orden original
        etiquetas_final = list(range(len(x))) #inicializa el vector donde se guardaran las etiquetas en el orden original

        for i in range(len(x)): #recorre todos los elementos del vector ordenado
            solucion[orden[i]] = intervalos[i] #coloca el intervalo en la posicion original de cada elemento
            etiquetas_final[orden[i]] = etiquetas[i] #coloca la etiqueta en la posicion original de cada elemento
        return {'solucion': solucion, 'etiquetas': etiquetas_final, 'limites': limites} #devuelve los intervalos, las etiquetas y los limites

    else:
        raise TypeError('Esta funcion solo sirve para vectores numericos.') #provoca un error si el vector contiene elementos no numericos

#discretizacion para datasets, ya sea por igual anchura o por igual frecuencia
def discretize_dataset(x,num_bins, anchura=False):
  """Discretiza columnas numericas de un DataFrame por igual anchura o igual frecuencia, depende de la entrada.
  Entradas: x (DataFrame), num_bins (numero de grupos), .
  Salida: diccionario con solucion, etiquetas y limites por columna.
  """
  solucion= x.copy() #se hace una copia del dataset inicial
  limites= {} #inicializa para luego
  etiquetas= {}

  for columna in x.columns: #se recorre cada variable/columna del dataset
    clase= True
    for i in range(len(x[columna])): #ve que columnas/variables de x no son numericas
        if not isinstance(x[columna].iloc[i], (int, float, np.integer, np.floating)):
          clase= False
      #solo ha de discretizar las columnas numericas
    if clase==True: #si esa columna es numerica
        if anchura== True: #discretiza por ancura
            resultado= discretizeEW(list(x[columna]), num_bins)
        elif anchura== False: #discretiza por frecuencia
            resultado= discretizeEF(list(x[columna]), num_bins)
        solucion[columna]= resultado['solucion'] #guarda la solucion
        etiquetas[columna]= resultado['etiquetas'] #guarda las etiquetas
        limites[columna]= resultado['limites'] #guarda los limites

  return {'solucion': solucion, 'etiquetas':etiquetas, 'limites': limites} #devuelve un diccionario con las soluciones, etiquetas y limites de las columnas discretizadas



## Calculo de metricas
#funcion para el calculo de la varianza muestralde un vector
def varianza(x): #toma el vector como entrada
    """Calcula la varianza muestral de un vector numerico (n-1).
    Entrada: x (vector numerico de al menos dos valores).
    Salida: float, varianza muestral.
    """
    if len(x) < 2: #el vector no puede tener un solo elemento, de lo contrario provoca un error
        raise ValueError('Se necesitan al menos dos valores para calcular la varianza.')
    for i in range(len(x)): #el vector no puede contener elementos vacios, de lo contario provoca un error
        if x[i]!=x[i]:
            raise ValueError('El vector no puede contener NaN.')
    media= sum(x)/len(x) #calcula la media de los elementos del vector
    suma= 0

    for i in range(len(x)): #calcula el sumatorio requerido para obtener la varianza muestral
        suma+= (x[i]-media)**2
    return suma/(len(x) - 1) #devuelve la varianza muestral

#funcion para el calculo de la entropia de un vector
def entropia(x): #como input solo el vector
    """Calcula la entropia de Shannon en bits mediante frecuencias propias.
    Entrada: x (vector de categorias).
    Salida: float, entropia en bits.
    """
    if len(x) == 0: #el vector no puede estar vacio, sino no se puede calcular la entropia
        raise ValueError('El vector no puede estar vacio.') #de lo contrario, provoca error
    for i in range(len(x)): #el vector tampoco puede contener valores vacios, de lo contrario tambien provoca error de valor
        if x[i] != x[i]:
            raise ValueError('El vector contiene NaN.')

    valores= [] #inicializa para los posteriores for
    frecuencias= []
    for i in x: #recorre cada elemento de x, para quedarse con los valores sin repetir(unicos)
        if i in valores: #si ese elemento i de x ya esta en valores
            posicion= valores.index(i) #obtiene su posicion
            frecuencias[posicion]+= 1 #aumenta su numero de apariciones por 1 y lo guarda en la lista de frecuencias en la posicion adecuada
        else: #si el valor es nuevo, lo mete en ambas listas
            valores.append(i)
            frecuencias.append(1) #mete su frecuencia, que es 1 porque es nuevo
    solucion = 0 #inicializa la solucion
    for frecuencia in frecuencias: #para la frecuencia de cada valor unico
        prob= frecuencia/len(x) #calcula la probabilidad de que salga ese valor
        solucion-= prob*np.log2(prob) #calcula la contribucion de cada valor a la entropia
    return solucion #devuelve la entropia del vector

#funcion para calcular la entropia normalizada
def entropia_normalizada(x): #toma como entrada una variable/columna del dataset
    """Normaliza la entropia por log2(numero de categorias observadas).
    Entrada: x (vector categorico).
    Salida: float entre 0 y 1.
    """
    if len(x)==0: #para verificar que la columna no este vacia (de lo contrario salta un error)
            raise ValueError('El vector no puede estar vacio.')
    for i in range(len(x)): #para verificar que la columna no tenga valores vacios, de lo contrario, vuelve a lanzar el mismo error
            if x[i]!= x[i]:
                raise ValueError('El vector no puede contener NaN.')
    
    valores= []
    for i in x: #para obtener los valores unicos de la columna
        if not (i in valores):
            valores.append(i)
    solucion= entropia(x) #la entropia sin normalizar, mediante la funcion vista anteriormente
    if len(valores)< 2: #si solo hay un valor, devuelve 0, para que no de error al dividir entre 0
        return 0.0
    return solucion/np.log2(len(valores)) #devuelve la entropia normalizada

#funcion para el calculo de AUC, se utiliza en calculometricas
def AUC(x, y): #como entradas, toma una columna numerica y otra columna logica/binaria
    """Calcula manualmente la curva ROC y su AUC con trapecios.
    Entradas: x (variable numericas), y (clase binaria).
    Salida: diccionario con auc, FPR y TPR.
    Las clases pueden ser booleanas o 0/1. True/1 es la positiva.
    """
    x=list(x) #convierte las variables en listas para facilitar el trabajar con ellas
    y= list(y)
    if len(x) != len(y) or len(x) == 0: #las variables han de tener una longitud determinada, de lo contrario, se provoca un error de valor
        raise ValueError('Los vectores deben tener igual longitud y no estar vacios.')
    for i in range(len(x)): #las funciones no pueden tener elementos vacios, de lo contrario, se provoca error de valor
            if x[i]!= x[i] or y[i]!= y[i]:
                raise ValueError('Ninguno de los dos vectores puede contener NaN.')
    for i in range(len(x)): #los elementos de la primera funcion deben ser numericos, y los de la segunda, binarios, sino, se induce error.
        if not isinstance(x[i], (int, float, np.integer, np.floating)):
            raise ValueError('x debe ser un vector numerico.')
        if y[i]!=True and y[i]!=False:
            raise ValueError('La clase debe ser binaria.') 
    resultado= ordenar(list(x), True) #ordena el vector numerico
    xx= resultado['vector'] #devuelve el vector numerico ordenado
    yy= []
    positivos= 0
    for i in resultado['orden']: #recorre las posiciones originales siguiendo el nuevo orden
        yy.append(y[i]) #coloca cada clase de y en la posicion correspondiente al valor ordenado de x
    for i in range(len(yy)): #recorre todas las clases para contar los elementos positivos
        if yy[i]==True:
            positivos+=1
    negativos= len(yy)-positivos #calcula los elementos negativos
    if positivos==0 or negativos==0: #hay que comprobar que existen tanto negativos como positivos, de lo contrario se da una division entre 0
        raise ValueError('La clase debe contener positivos y negativos.') #para evitar la division, salta este error
    FPR= [0.0] #inicializa la tasa de falsos positivos
    TPR= [0.0] #inicializa la tasa de verdaderos positivos
    umbrales = []

    for valor in xx: #se seleccionan como umbrales todos los valores distintos de x
        if valor not in umbrales:
            umbrales.append(valor)

    for umbral in umbrales: #para cada umbral, se calculara el valor de TPR y FPR
        TP = 0
        FP = 0
        for j in range(len(xx)): #calcula los verdaderos positivos y falsos positivos para cada elemento numerico dependiendo del umbral
            if xx[j] >= umbral: #si el valor del elemento es superior al del umbral, seria positivo
                #por lo que luego se evalua si es un falso positivo o no dependiendo del valor verdadero de y que le corresponde a ese elemento
                if yy[j]:
                    TP+= 1
                else:
                    FP+= 1
        TPR.append(TP / positivos) #se guarda cadavalor de TPR y FPR
        FPR.append(FP / negativos)
    auc= 0 #inicializa el area bajo la curva ROC
    for i in range(1, len(FPR)): #recorre todos los puntos de la curva ROC, y calcula el area de cada trapecio
        auc += (FPR[i]-FPR[i-1])*(TPR[i]+TPR[i-1])/2 #suma las areas de cada trapecio, dando una integral como resultado
    print('AUC:',auc) #printea el resultado de la integral
    return {'auc':auc,'FPR':FPR,'TPR':TPR} #devuelve el area bajo la curva ROC y las tasas de falsos y verdaderos positivos

#funcion para el plotteo del AUC, se utiliza en calculodemetricas
def plot_AUC(resultado, namex='x', namey='clase'): #como entradas, toma el resultado del AUC, ademas de los nombres de las variables numerica y logica utilizadas en el calculo del auc, respectivamente
    """Dibuja la curva ROC de la salida de AUC.
    Entrada: resultado (diccionario de AUC), namex (nombre variable numerica), namey (nombre variable logica).
    Salida: grafico matplotlib.
    """
    plt.figure() #crea la figura del grafico
    plt.plot(resultado['FPR'], resultado['TPR'], marker='o')#realiza el plot de la curva ROC, tomando como eje x la tasa de falsos positivos y como y la tasa de verdaderos positivos
    plt.plot([0, 1], [0, 1], linestyle='--')#representa la diagonal de referencia que corresponderia a una clasificacion random
    plt.xlim(0, 1) #limites del grafico
    plt.ylim(0, 1)
    plt.xlabel('False Positive Rate (FPR)') #etiquetas del grafico
    plt.ylabel('True Positive Rate (TPR)')
    plt.title(f'Curva ROC - {namex} vs {namey} - AUC = {resultado["auc"]:.3f}') #titulo del grafico con el valor de la integral bajo la curva
    plt.show()

#Funcion para el calculo de varias de las metricas de un dataset a la vez(varianza, AUC y entropia)
def calculodemetricas(x,varbinaria=None): #como entradas, el dataset y la opcion de especificar una variable binaria para el calculo del AUC
    """Muestra varianza, entropia y AUC por columnas de un DataFrame.
    Entradas: x (DataFrame), varbinaria (nombre opcional de clase binaria).
    Salida: resultados en pantalla y graficos ROC cuando se especifica clase.
    """
    if varbinaria!=None and varbinaria not in x.columns: #la variable binaria especificada debe pertenecer al dataset
        raise ValueError('La clase indicada no existe en el dataset.') #de lo contrario, salta un error
    if varbinaria!=None: #comprueba que la variable clase sea binaria, admitiendo True/False y 1/0, de lo contrario, se provocara un error de tipo
        for i in range(len(x[varbinaria])):
            if x[varbinaria].iloc[i]!=True and x[varbinaria].iloc[i]!=False:
                raise ValueError('La variable especificada debe ser binaria.')

    for columna in x.columns: #el bucle recorre cada columna del dataset
        if columna!=varbinaria: # si la columna es diferente a la variable binaria especificada, entra
            claseNum=True
            claseCat=True
            if isinstance(x[columna].dtype,pd.CategoricalDtype): #reconoce las columnas categoricas de pandas, aunque contengan numeros
                claseNum=False
                claseCat=True
            else:
                for i in range(len(x[columna])): #comprueba que los valores de la columna sean numericos o categoricos
                    if not isinstance(x[columna].iloc[i],(int,float,np.integer,np.floating)):
                        claseNum=False
                    if not isinstance(x[columna].iloc[i],(str,pd.Categorical)):
                        claseCat=False
            if claseNum==True: #si los valores de la columna son numericos, se calculara la varianza, y en caso de haber una variable binaria, pues el AUC tambien
                print('Variable:',columna) #muestra el nombre de la variable
                print('Varianza:',varianza(list(x[columna]))) #calcula la varianza de la variable
                if varbinaria!=None: #si se ha especificado una variable binaria
                    resultado=AUC(list(x[columna]),list(x[varbinaria])) #calcula el AUC de la variable numerica y la binaria
                    plot_AUC(resultado,columna,varbinaria) #grafica la curva ROC, mostrando el resultado del AUC
            elif claseCat==True: #si los valores de la columna son categoricos, calcula la entropia solamente
                print('Variable:',columna) #muestra el nombre de la variable
                print('Entropia:',entropia(list(x[columna]))) #calcula su entropia


#Funcion identica a la de arriba, pero con una entrada mas: el umbral.
#permite filtrar las variables de un dataset, eligiendo aquellas que superen un umbral (ya sea por su varianza, entropia o AUC)
def calculodemetricas_umbral(x,varbinaria=None, umbral=(0, 0.5, 0)): #mismas entradas que antes(dataset y posible variable binaria), a la que se les suma el umbral
    #este umbral debe ser un vector, con valor de umbral para la varianza, AUC y entropia, en ese orden
    """Filtra columnas por varianza, AUC y entropia normalizada.
    Entradas: x (DataFrame), varbinaria (opcional, por defecto None), umbral, para: (varianza, AUC, entropia).
    Salida: DataFrame con variables que superan los umbrales, sin columna clase.
    """
    nuevo_dataset = pd.DataFrame(index=x.index) #crea el nuevo dataset
    if varbinaria!=None and varbinaria not in x.columns: #misma comprobacion que en la funcion sin umbra, en caso de existir la variable binaria, debe pertenecer al dataset
        raise ValueError('La clase indicada no existe en el dataset.') #de lo contrario, provoca un error4
    if varbinaria!=None: #comprueba que la variable clase sea binaria, admitiendo True/False y 1/0, de lo contrario, se provocara un error de tipo
            for i in range(len(x[varbinaria])):
                if x[varbinaria].iloc[i]!=True and x[varbinaria].iloc[i]!=False:
                    raise ValueError('La variable especificada debe ser binaria.')
    for columna in x.columns: #recorre cada variable/columna del dataset original en el bucle
        if columna!=varbinaria:
            claseNum=True
            claseCat=True
            if isinstance(x[columna].dtype,pd.CategoricalDtype): #reconoce las columnas categoricas de pandas, aunque contengan numeros
                claseNum=False
                claseCat=True
            else:
                for i in range(len(x[columna])): #determina si la columna es categorica o numerica, como en la funcion sin umbral
                    if not isinstance(x[columna].iloc[i],(int,float,np.integer,np.floating)):
                        claseNum=False
                    if not isinstance(x[columna].iloc[i],(str,pd.Categorical)):
                        claseCat=False
            if claseNum==True: #en caso de que la columna/variable sea numerica
                varian = varianza(list(x[columna])) #calcula la varianza, pero en este caso guarda su valor para despues compararlo con el umbral
                print('Variable:',columna) #muestra el nombre de la variable
                print('Varianza:',varian) #muestra el valor de la varianza
                if varbinaria!=None: #si existe una variable logica elegida por el usuario, entra a calcular el AUC
                    resultado=AUC(list(x[columna]),list(x[varbinaria])) #calcula el AreaUndertheCurve con la variable numerica y la logica
                    plot_AUC(resultado,columna,varbinaria) #grafica el AUC
                    if varian>= umbral[0] and resultado['auc'] >=umbral[1]: #si tanto el valor de la varianza como el del AUC superan el umbral especificado
                        nuevo_dataset[columna]= x[columna] #la variable numerica pasa a formar parte del nuevo dataset
                elif varian>= umbral[0]: #en caso de no calcularse el auc, la variable solo tiene que cumplir la condicion correspondiente a la varianza para ser incluida en el nuevo dataset
                    nuevo_dataset[columna]= x[columna]

            elif claseCat==True: #en caso de que la columna/variable sea categorica
                entro= entropia_normalizada(list(x[columna])) #se calcula la entropia, en este caso se guarda su valor para despues compararlo con el umbral
                print('Variable:',columna) #se muestra el nombre de la variable
                print('Entropia:', entro) #se muestra el valor calculado de la entropia
                if entro>= umbral[2]: #si la entropia de la variable supera el umbral, la variable se incluye en el nuevo dataset
                    nuevo_dataset[columna]= x[columna]
    return nuevo_dataset #devuelve el dataset formado por las columnas que cumplen los umbrales establecidos

##Normalizacion y estandarizacion
#Funcion para la normalizacion de un vector
def normalizacion(x): #como entrada, el vector a normalizar
    """Normaliza vector numerico entre 0 y 1; conserva vectores no numericos.
    Entrada: x (vector).
    Salida: lista de valores transformados o entrada original.
    """
    if len(x) == 0: #comprueba que el vector no este vacio, de lo contrario, provoca un error
        raise ValueError('El vector no puede estar vacio.')
    for i in range(len(x)): #comprueba que los elementos del vector sean numericos
        if not isinstance(x[i],(int,float,np.integer,np.floating)):
            print('La variable no es numerica. Se devuelve sin modificar.') #de lo contrario, se limita a devolver el vector sin normalizar
            return x

    xnorm= []
    for i in range(len(x)): #bucle que normaliza el vector
        if max(x) == min(x): #en caso de que todos los valores sean iguales, se crea un vector de ceros, ya que la resta entre cada valor y el valor minimo siempre sera cero
            xnorm.append(0) 
        else: #si existe un maximo diferente al minimo, se normaliza cada elemento de la siguiente manera
            xnorm.append((x[i]-min(x))/(max(x)-min(x))) #simplemente se suma cada elemento al vector normalizado
    return xnorm #devuelve el vector normalizado

#Funcion para la normalizacion de un dataset
def normalizacion_dataset(x): #como entrada toma el dataset a normalizar
    """Normaliza las columnas numericas de un DataFrame.
    Entrada: x (DataFrame).
    Salida: nuevo DataFrame con el resto de columnas sin modificar.
    """
    solucion= x.copy() #crea una copia del dataframe 
    for columna in x.columns: #para cada columna del dataframe
        clase =True #inicializa la clase como la correcta
        for i in range(len(x)): #recorre cada elemento de la columna para ver si todos sus elementos son numericos
            if not isinstance(x[columna].iloc[i],(int,float,np.integer,np.floating)):
                print('La variable no es numerica. Se devuelve sin modificar.')
                clase=False #si no lo son, se devuelve el siguiente aviso, ademas de la columna sin cambios
                #De esta manera, no se eliminan los elementos categoricos del dataset, simplemente se devuelven sin normalizar
        if clase ==True: #si todos los elementos son numericos
            solucion[columna]= normalizacion(list(x[columna])) #incluye en la solucion la columna normalizada, reemplazando a la columna sin normalizar
    return solucion #devuelve el dataset con las variables normalizadas

#Funcion para la estandarizacion de un vector
def estandarizacion(x): #toma como entrada ese vector
    """Estandariza vector con media y desviacion tipica muestral propias.
    Entrada: x (vector).
    Salida: lista estandarizada o entrada original si no es numerica.
    """
    if len(x) == 0: #provoca un error si el vector esta vacio
            raise ValueError('El vector no puede estar vacio.')
    for i in range(len(x)): #comprueba si cada elemento del vector es un valor numerico
        if not isinstance(x[i],(int,float,np.integer,np.floating)):
            print('La variable no es numerica, por lo que se devolvera sin modificar.')
            return x #de lo contrario, imprime un aviso y devuelve el vector sin estandarizar
    media= sum(x)/len(x) #calcula la media del vector
    xesta= []
    if len(x) < 2 or max(x) == min(x): #para vectores con menos de dos elementos o con todos los valores iguales
        return [0]*len(x) #devuelve una lista de ceros de la longitud del vector (un 0)
    desviacion = np.sqrt(varianza(x)) #calcula la desviacion del vector mediante la funcion de la varianza muestral
    for i in range(len(x)): #para cada valor de x
        xesta.append((x[i]-media)/desviacion) #estandariza cada elemento del vector y lo incluye en la solucion
    return xesta #devuelve el vector estandarizado

#Funcion para la estandarizacion de un dataset
def estandarizacion_dataset(x): #toma como entrada el dataset
    """Estandariza las columnas numericas de un DataFrame.
    Entrada: x (DataFrame).
    Salida: nuevo DataFrame con columnas no numericas originales.
    """
    solucion= x.copy() #crea una copia del dataset sobre la que posteriormente se trabajara
    for columna in x.columns: #para cada columna del dataset
        clase = True
        for i in range(len(x)): #comprueba que dicha variable/columna este compuesta unicamente
            if not isinstance(x[columna].iloc[i],(int,float,np.integer,np.floating)):
                clase =False #si no se cumple la condicion, marca la clase como falsa, ya que no es una columna compuesta unicamente por elementos numericos
        if clase == True: #si la columna solo tiene elementos numericos, la estandariza
            solucion[columna] = estandarizacion(list(x[columna])) #emplea la funcion de estandarizar vectores, sustituyendo a la columna sin estandarizar de la solucion
    return solucion #devuelve el dataset estandarizado

##Calculo de la correlacion 
#Funcion para el calculo de la covarianza muestral, se emplea en el calculo de la correlacion de pearson
def covarianza(x, y): #toma como  entradas dos vectores
    """Calcula covarianza muestral mediante operaciones basicas.
    Entradas: x, y (vectores numericos de igual longitud).
    Salida: float, covarianza.
    """
    if len(x) != len(y) or len(x) < 2:
        raise ValueError('Se requieren vectores de igual longitud, y con una longitud minima de 2.')
    for i in range(len(x)): #La funcion solo funciona para valores numericos o enteros
        if not isinstance(x[i],(int,float,np.integer,np.floating)) or not isinstance(y[i],(int,float,np.integer,np.floating)):
            raise ValueError('La funcion solo funciona con vectores numericos.') #si alguno de los dos vectores tiene valores no numericos, provoca un error
    mediax = sum(x)/len(x) #calcula la media de cada vector
    mediay = sum(y)/len(y)
    suma = 0
    for i in range(len(x)): #durante la longitud de ambos vectores (ya que len(x)==len(y)), recorre el bucle
        suma+= (x[i]-mediax)*(y[i]-mediay) #suma valores al sumatorio que se emplea para el calculo de la covarianza
    return suma/(len(x)-1) #devuelve la covarianza de x e y

#funcion para el calculo de la correlacion, posteriormente utilizada en la funcion ,matriz_correlacion
def correlacion_pearson(x, y): #como entrada, toma dos variables numericas
    """Calcula correlacion de Pearson reutilizando covarianza y varianza.
    Entradas: x, y (vectores numericos).
    Salida: coeficiente entre -1 y 1 o NaN si hay varianza cero.
    """
    for i in range(len(x)): #La funcion solo funciona para valores numericos o enteros
            if not isinstance(x[i],(int,float,np.integer,np.floating)) or not isinstance(y[i],(int,float,np.integer,np.floating)):
                raise ValueError('La funcion solo funciona con vectores numericos.') #si alguno de los dos vectores tiene valores no numericos, provoca un error
    denominador= np.sqrt(varianza(x))*np.sqrt(varianza(y)) #calcula el denominador de la formula de la correlacion de pearson, mediante el uso de la funcion varianza
    if denominador==0: #si el denominador es 0, devuelve un NaN para que no de error a la hora de dividir
        return float('NaN')
    return covarianza(x, y)/denominador #devuelve el resultado de la correlacion de pearson, haciendo uso de la funcion de covarianza y del denominador calculado

#Funcion para el calculo de la informacion mutua, posteriormente utilizada en matriz_correlacion
def inf_mutua(x, y, normalizada =False): #toma como entrada dos variables categoricas
    """Calcula informacion mutua normalizada de dos vectores categoricos.
    Entradas: x, y (vectores categoricos de la misma longitud).
    Salida: float, informacion mutua normalizada (en caso de especificarse asi) por raiz de entropias.
    """
    if len(x) != len(y) or len(x) == 0: #comprueba que las variables tengan la longitud apropiada
        raise ValueError('Los vectores deben tener la misma longitud positiva.') #de lo contrario, provoca un error
    claseCatX=isinstance(x,pd.Categorical) or (isinstance(x,pd.Series) and isinstance(x.dtype,pd.CategoricalDtype))
    claseCatY=isinstance(y,pd.Categorical) or (isinstance(y,pd.Series) and isinstance(y.dtype,pd.CategoricalDtype))
    x=list(x) #convierte a lista despues de comprobar si el vector es categorico de pandas
    y=list(y)
    if claseCatX==False:
        claseCatX=True
        for i in range(len(x)):
            if not isinstance(x[i],str):
                claseCatX=False
    if claseCatY==False:
        claseCatY=True
        for i in range(len(y)):
            if not isinstance(y[i],str):
                claseCatY=False
    if claseCatX==False or claseCatY==False:
        raise TypeError('Las dos variables deben ser categoricas.')
    xy = []
    for i in range(len(x)): #crea un vector uniendo los valores x e y correspondientes a la misma observacion
        xy.append((x[i], y[i]))
    hx = entropia(x) #calcula la entropia de x
    hy = entropia(y) #calcula la entropia de y
    hxy = entropia(xy) #calcula la entropia del recien creado xy
    inf = hx+hy-hxy #calcula el valor de la informacion mutua
    if normalizada==True: #si se ha especificado que se desea la informacion mutua normalizada, se normaliza
        if hx*hy>0: #si ni la entropia de x ni la de y son iguales a 0, normaliza la informacion mutua
            return inf/np.sqrt(hx*hy) #devuelve informacion mutua normalizada
        return 0.0 #si alguna entropia es 0, devuelve 0 y asi evita dividir
    return inf #si no se especifica que se desea la normalizada, se devuelve la inf mutua sin normalizar


#funcion para el calculo de la correlacion e informacion mutua
def matriz_correlacion(data): #como entrada, el dataset
    """Calcula Pearson para pares numericos/bool, MI para pares categoricos.
    Entrada: data (DataFrame).
    Salida: DataFrame cuadrado; NaN para combinaciones incompatibles.
    """
    nombres = list(data.columns) #guarda los nombres de cada columna
    cormat = pd.DataFrame(float('NaN'), index=nombres, columns=nombres) #crea una matriz de correlaciones, vacia por el momento
    for i in nombres: #recorre cada columna
        claseNumI =True #inicializa las clases como correctas, permaneceran asi a no ser que se demuestre lo contrario
        claseCatI =True
        xi = data[i] #accede a cada columna del dataset inicial
        if isinstance(xi.dtype,pd.CategoricalDtype): #reconoce categorias de pandas, incluso cuando contienen numeros
            claseNumI=False
            claseCatI=True
        else:
            for k in range(len(xi)): #comprueba que dicha columna este unicamente compuesta por valores numericos
                if not isinstance(xi.iloc[k],(int,float,np.integer,np.floating,bool,np.bool_)):
                    claseNumI = False #de lo contrario, la claseNum pasa a ser falsa
            for k in range(len(xi)): #comprueba que dicha columna este unicamente compuesta por valores categoricos
                if not isinstance(xi.iloc[k],str):
                    claseCatI = False #de lo contrario, la claseCat pasa a ser falsa

        for j in nombres: #ahora, recorre cada columna, para compararla con la columna elegida en el bucle de fuera
            claseNumJ = True
            claseCatJ = True
            xj = data[j]
            if isinstance(xj.dtype,pd.CategoricalDtype): #reconoce categorias de pandas, incluso cuando contienen numeros
                claseNumJ=False
                claseCatJ=True
            else:
                for l in range(len(xj)): #comprueba que dicha columna este unicamente compuesta por valores numericos
                    if not isinstance(xj.iloc[l],(int,float,np.integer,np.floating,bool,np.bool_)):
                        claseNumJ = False #de lo contrario, la claseNum pasa a ser falsa
                for l in range(len(xj)): #comprueba que dicha columna este unicamente compuesta por valores categoricos
                    if not isinstance(xj.iloc[l],str):
                        claseCatJ = False #de lo contrario, la claseCat pasa a falsa

            if claseNumI==True and claseNumJ==True: #si ambas columnas/variables son numericas, se calcula la correlacion de pearson entre ellas
                            cormat.loc[i, j] = correlacion_pearson(list(xi), list(xj)) #el valor de la correlacion se guarda en la matriz de correlaciones
            elif claseCatI==True and claseCatJ==True: #si ambas columnas/variables son categoricas, se calcula la inf mutua entre ellas
                cormat.loc[i, j] = inf_mutua(xi, xj, True) #se puede elegir normalizar el valor de inf mutua escribiendo True. 
                #Se guarda el valor de inf mutua en la matriz de correlaciones
    return cormat #se devuelve la matriz de correlaciones

#Funcion para graficar la matriz de correlaciones
def plot_correlacion(matriz_cor): #como entrada, la matriz a graficar
    """Representa la matriz de correlacion/MI como un mapa de calor.
    Entrada: matriz_cor (DataFrame cuadrado).
    Salida: grafico matplotlib.
    """
    nombres = list(matriz_cor.columns) #obtiene los nombres de las variables de la matriz
    fig, ax = plt.subplots()#crea la figura y los ejes del mapa de calor
    imagen = ax.imshow(matriz_cor.to_numpy(dtype=float), vmin=-1, vmax=1, cmap='coolwarm') #convierte la matriz a numpy para representar los valores con colores
    ax.set_xticks(range(len(nombres)), labels=nombres, rotation=90) #leyenda en x
    ax.set_yticks(range(len(nombres)), labels=nombres) #leyenda en y
    fig.colorbar(imagen, ax=ax) #barra lateral para leyenda de colores
    fig.tight_layout()
    plt.show() #muestra la grafica


