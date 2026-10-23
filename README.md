# Tratamiento de datasets
Paquete de Python desarrollado para la asignatura de Software Matemático y Estadístico del máster KISA.
Este paquete contiene una serie de funciones implementadas para realizar distintas operaciones de tratamiento y análisis estadístico de datos.

## Funcionalidades
Las funciones incluidas permiten realizar:

- **Discretización:** discretización de variables numéricas por igual anchura (EW) e igual frecuencia (EF).
- **Cálculo de métricas:** varianza muestral, entropía de Shannon y área bajo la curva ROC (AUC).
- **Filtrado de variables:** selección de atributos mediante umbrales de varianza, entropía normalizada y AUC.
- **Normalización y estandarización:** transformación de variables numéricas y datasets.
- **Análisis de correlación:** correlación de Pearson e información mutua entre variables.
- **Visualización:** representación de curvas ROC y matrices de correlación.

## Requisitos
Para utilizar las funciones son necesarias las siguientes librerías:
- NumPy
- pandas
- Matplotlib
Estas dependencias se especifican en el archivo `setup.py`.

## Instalación
Desde una terminal situada en la carpeta principal del proyecto, ejecutar:

```bash
python -m pip install -e .
```

## Ejemplo de uso
Una vez instalado el paquete, las funciones pueden importarse de la siguiente manera:

```python
from gestion_datasets.Funciones import varianza, entropia

x=[1,2,3,4,5]
print(varianza(x))

categorias=['A','B','A','B']
print(entropia(categorias))
```

## Documentación
El archivo `Entrega_Final.ipynb` incluye explicaciones teóricas y ejemplos de utilización de las funciones.
El código de las funciones se encuentra documentado en `gestion_datasets/Funciones.py`, incluyendo sus entradas, salidas y funcionamiento interno.

## Autor
Jon Lorenzo Insausti
