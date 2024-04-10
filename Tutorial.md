# Variables


```python
# Uncomment lo siguiente para usarlo en Colab
# %%capture
# !pip install ipympl
# !git clone https://github.com/nico-tombolato/FormuLab temp
# !mv temp/* .

# from google.colab import output
# output.enable_custom_widget_manager()
```


```python
from formulab.objects import *
```

Los objetos de tipo `objects.var` son variables que almacenan todos los atributos que tendría una variable estadística.\
Para inicializar, los argumentos necesarios son el nombre en formato string (puede contener subíndices y simbolos de latex, pero sin el backlash `\`) y el conjunto de mediciones realizados en una lista o un `dict`.\
Tambien se puede introducir un único valor, pero en este caso no podra calcular nada.


```python
x = var('x_m', [1.1, 1.2, 1.1, 1.0], unit='m')
rho = var('rho', {'val': 10, 'sd': 1, 'n': 5}, unit='Omega m')
```


$\displaystyle x_{m} = (1.10 \pm 0.04) \, m$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad x_{m \, 95\%}=(1.10 \pm 0.13) \, m$



$\displaystyle \rho = (10.0 \pm 0.4) \, \Omega m$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad \rho_{ \, 95\%}=(10.0 \pm 1.2) \, \Omega m$


Las posibles entradas del `dict` son: 
* `values`: Lista de valores (como los de `x`)
* `val`: Valor medio
* `sd`: Desviación estándar
* `sdm`: Desviación estándar de la media
* `n`: Cantidad de mediciones
* `nu`: Grados de libertad
* `u`: Incertidumbre
* `valr`: Valor medio redondeado
* `u_st`: Intervalo de confianza con t de Student

Con los datos ingresados, el programa calculará toda la información posible. Si no se especifica, supondrá `nu = n-1`, si no se dió la desviación estándar `sd = sdm` y si se envía un único valor `n = 1`.

Hay argumentos adicionnales para la función:
* `alpha`: El nivel de significancia para el intervalo de confianza con t de Student, el `default` es `0.05` y puede ser modificado permanentemente en el archivo `formulab/config.py`. `0` Evita que se calcule
* `vbs`: El nivel de verbosidad, con `0` no mostrará nada al ejecutarse, `1` solo el valor final, `2` los pasos intermedios


```python
y = var('y_2', [20,23,20,21,23,20], alpha=0.02, vbs=2)
z = var('z', 1, vbs=0) #No se muestra porque vbs=0
```


$\displaystyle \overline{y_{2}} = 21.166666666666668 \, \mathtt{\text{}}$



$\displaystyle s_{y2} = 1.4719601443879746 \quad s_{\overline{y2}} = 0.6009252125773317 \quad \nu_{y2} = 5$



$\displaystyle y_{2} = (21.2 \pm 0.6) \, \mathtt{\text{}}$



$\displaystyle \text{Intervalo de confianza de 98\,\%\,:}\quad y_{2 \, 98\%}=(21.2 \pm 2.0) \, \mathtt{\text{}}$


Acceder a los atributos de cada variable es simple, solo hay que llamarlos por su nombre, iguales a las entradas de `dict`.


```python
x.n
```




    4




```python
rho.nu
```




    4




```python
y.sdm
```




    0.6009252125773317



Y si se necesita el símbolo de la variable o de alguno de los atributos, hay que agregar `sym` previo al atributo.


```python
x
```




$\displaystyle x_{m}$




```python
rho.sym.nu
```




$\displaystyle \nu_{\rho}$




```python
y.sym.sdm
```




$\displaystyle s_{\overline{y2}}$



También se puede volver a calcular una variable con el método `calc`, e imprimirla con el método `display`.


```python
z.calc([5,5.1,4.9,5.5], vbs=0)
```




$\displaystyle z$




```python
z.display(vbs=2)
```


$\displaystyle \overline{z} = 5.125 \, \mathtt{\text{}}$



$\displaystyle s_{z} = 0.2629955639676582 \quad s_{\overline{z}} = 0.1314977819838291 \quad \nu_{z} = 3$



$\displaystyle z = (5.1 \pm 0.1) \, \mathtt{\text{}}$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad z_{ \, 95\%}=(5.1 \pm 0.4) \, \mathtt{\text{}}$


# Parámetros

Para cantidades que no tienen incertidumbre, como constantes universales, o valores de referencia, se utiliza el objeto de tipo `objects.param`. Adicionalmente, la librería `sympy` (Ya importada en el primer bloque) tiene constantes almacenadas.


```python
c = param('c', 299792458, 'm/s')
```


$\displaystyle c = 299792458 \, \frac{m}{s}$



```python
c
```




$\displaystyle c$




```python
c.val
```




    299792458




```python
sp.pi
```




$\displaystyle \pi$



# Funciones

Una funcion de tipo `objects.func` es inicializada de forma similar a una variable, indicando el nombre y la expresión es suficiente. Será automáticamente evaluada por defecto


```python
f = func('f', rho/x, 'Omega', vbs=2)
```


$\displaystyle f = \frac{\rho}{x_{m}}$



$\displaystyle f({\rho: 10, x_{m}: 1.1}) = 9.09090909090909 \, \Omega$



$\displaystyle \frac{\partial f}{\partial \rho} = \frac{1}{x_{m}} = 0.909090909090909 \, \frac{1}{m}$



$\displaystyle \frac{\partial f}{\partial x_{m}} = - \frac{\rho}{x_{m}^{2}} = -8.26446280991735 \, \frac{\Omega}{m}$



$\displaystyle s_{\overline{f}} = \sqrt{\frac{\partial f}{\partial \rho}^{2} s_{\overline{\rho}}^{2} + \frac{\partial f}{\partial x_{m}}^{2} s_{\overline{xm}}^{2}}$



$\displaystyle s_{\overline{f}} = 0.528322659075423 \, \Omega$



$\displaystyle f = (9.1 \pm 0.5) \, \Omega$



$\displaystyle \nu_{f} = \frac{s_{\overline{f}}^{4}}{\frac{\frac{\partial f}{\partial \rho}^{4} s_{\overline{\rho}}^{4}}{\nu_{\rho}} + \frac{\frac{\partial f}{\partial x_{m}}^{4} s_{\overline{xm}}^{4}}{\nu_{xm}}} = 6.98772522225855 \approx 6$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad f_{ \, 95\%}=(9.1 \pm 1.3) \, \Omega$


Sus argumentos adicionales son:
* `alpha`: Ya mencionado
* `calcEv`: Evaluar la expresión, `True` o `False`
* `calcU`: Calcular la incertidumbre (mediante propagación con derivadas parciales)
* `vbs`: Ya mencionado

Para evaluarla con otros valores se llama a la función directamente con un `dict` indicando los nuevos valores, utilizara los iniciales para aquellos que no sean específicados, retorna `dict` o `list` de `dict` (esto último si fue evaluado en una lista de valores).


```python
f_1 = f({x: 3})
```


$\displaystyle f = (3.3 \pm 0.2) \, \Omega$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad f_{ \, 95\%}=(3.3 \pm 0.4) \, \Omega$



```python
f_2 = f({rho: [1,2,3], x.sym.sdm:10}, vbs=2)
```


$\displaystyle \text{Evaluando con}\quad {\rho: 1}$



$\displaystyle f = \frac{\rho}{x_{m}}$



$\displaystyle f({\rho: 1, x_{m}: 1.1}) = 0.909090909090909 \, \Omega$



$\displaystyle \frac{\partial f}{\partial \rho} = \frac{1}{x_{m}} = 0.909090909090909 \, \frac{1}{m}$



$\displaystyle \frac{\partial f}{\partial x_{m}} = - \frac{\rho}{x_{m}^{2}} = -0.826446280991735 \, \frac{\Omega}{m}$



$\displaystyle s_{\overline{f}} = \sqrt{\frac{\partial f}{\partial \rho}^{2} s_{\overline{\rho}}^{2} + \frac{\partial f}{\partial x_{m}}^{2} s_{\overline{xm}}^{2}}$



$\displaystyle s_{\overline{f}} = 8.27445676722680 \, \Omega$



$\displaystyle f = (1 \pm 8) \, \Omega$



$\displaystyle \nu_{f} = \frac{s_{\overline{f}}^{4}}{\frac{\frac{\partial f}{\partial \rho}^{4} s_{\overline{\rho}}^{4}}{\nu_{\rho}} + \frac{\frac{\partial f}{\partial x_{m}}^{4} s_{\overline{xm}}^{4}}{\nu_{xm}}} = 3.01452432850479 \approx 3$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad f_{ \, 95\%}=(1 \pm 26) \, \Omega$



$\displaystyle \text{Evaluando con}\quad {\rho: 2}$



$\displaystyle f = \frac{\rho}{x_{m}}$



$\displaystyle f({\rho: 2, x_{m}: 1.1}) = 1.81818181818182 \, \Omega$



$\displaystyle \frac{\partial f}{\partial \rho} = \frac{1}{x_{m}} = 0.909090909090909 \, \frac{1}{m}$



$\displaystyle \frac{\partial f}{\partial x_{m}} = - \frac{\rho}{x_{m}^{2}} = -1.65289256198347 \, \frac{\Omega}{m}$



$\displaystyle s_{\overline{f}} = \sqrt{\frac{\partial f}{\partial \rho}^{2} s_{\overline{\rho}}^{2} + \frac{\partial f}{\partial x_{m}}^{2} s_{\overline{xm}}^{2}}$



$\displaystyle s_{\overline{f}} = 16.5339248638134 \, \Omega$



$\displaystyle f = (0 \pm 20) \, \Omega$



$\displaystyle \nu_{f} = \frac{s_{\overline{f}}^{4}}{\frac{\frac{\partial f}{\partial \rho}^{4} s_{\overline{\rho}}^{4}}{\nu_{\rho}} + \frac{\frac{\partial f}{\partial x_{m}}^{4} s_{\overline{xm}}^{4}}{\nu_{xm}}} = 3.00363027352217 \approx 3$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad f_{ \, 95\%}=(0 \pm 50) \, \Omega$



$\displaystyle \text{Evaluando con}\quad {\rho: 3}$



$\displaystyle f = \frac{\rho}{x_{m}}$



$\displaystyle f({\rho: 3, x_{m}: 1.1}) = 2.72727272727273 \, \Omega$



$\displaystyle \frac{\partial f}{\partial \rho} = \frac{1}{x_{m}} = 0.909090909090909 \, \frac{1}{m}$



$\displaystyle \frac{\partial f}{\partial x_{m}} = - \frac{\rho}{x_{m}^{2}} = -2.47933884297521 \, \frac{\Omega}{m}$



$\displaystyle s_{\overline{f}} = \sqrt{\frac{\partial f}{\partial \rho}^{2} s_{\overline{\rho}}^{2} + \frac{\partial f}{\partial x_{m}}^{2} s_{\overline{xm}}^{2}}$



$\displaystyle s_{\overline{f}} = 24.7967215390414 \, \Omega$



$\displaystyle f = (0 \pm 20) \, \Omega$



$\displaystyle \nu_{f} = \frac{s_{\overline{f}}^{4}}{\frac{\frac{\partial f}{\partial \rho}^{4} s_{\overline{\rho}}^{4}}{\nu_{\rho}} + \frac{\frac{\partial f}{\partial x_{m}}^{4} s_{\overline{xm}}^{4}}{\nu_{xm}}} = 3.00161338747177 \approx 3$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad f_{ \, 95\%}=(0 \pm 80) \, \Omega$


Notar que esto no modifica los valores almacenados en `x` o `rho`, para ello existe el método `calc` dentro de cada objeto.

Adicionalmente, se puede acceder a la expresión, a las derivadas parciales, sus expresiones, valores y símbolos que las representan.


```python
f.f
```




$\displaystyle \frac{\rho}{x_{m}}$




```python
f.expr.d[x]
```




$\displaystyle - \frac{\rho}{x_{m}^{2}}$




```python
f.d[x]
```




$\displaystyle -2.47933884297521$




```python
f.sym.d[x]
```




$\displaystyle \frac{\partial f}{\partial x_{m}}$



# Variables correlacionadas

Si se tienen dos cantidades correlacionadas, uno puede definir la covarianza entre ellas con la funcion `stats.set_cov`, permitiendo que realice el cálculo, o enviando como algumento el valor de la covarianza.\
Luego se puede acceder al atributo `cov` de una variable, que es un `dict` con la covarianza de esta con el resto.


```python
from formulab import stats
```


```python
a = var('a', [1,2,3,4], 'cm')
b = var('b', [4.3,5.7,5.3,5], 'cm')
```


$\displaystyle a = (2.5 \pm 0.6) \, c m$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad a_{ \, 95\%}=(2.5 \pm 2.1) \, c m$



$\displaystyle b = (5.1 \pm 0.3) \, c m$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad b_{ \, 95\%}=(5.1 \pm 0.9) \, c m$



```python
stats.set_cov(a, b, 20)
b.cov[a]
```




    20




```python
stats.set_cov(a, b)
a.cov[b]
```




    0.2833333333333333



Luego esto se reflejará en el cálculo de la incertidumbre de una funcion. Aunque en este caso no es apropiado determinar los grados de libertad efectivos mediante la expresión de Welch-Satterthwaite, el código lo determina de todos modos.


```python
g = func('g', sp.pi*a*b+a**2, unit='cm^2', vbs=2)
```


$\displaystyle g = a^{2} + \pi a b$



$\displaystyle g({b: 5.075, a: 2.5}) = 46.1089567924205 \, c m^{2}$



$\displaystyle \frac{\partial g}{\partial b} = \pi a = 7.85398163397448 \, m$



$\displaystyle \frac{\partial g}{\partial a} = 2 a + \pi b = 20.9435827169682 \, m$



$\displaystyle s_{\overline{g}} = \sqrt{\frac{\partial g}{\partial a}^{2} s_{\overline{a}}^{2} + 2 \frac{\partial g}{\partial a} \frac{\partial g}{\partial b} s_{\overline{ab}} + \frac{\partial g}{\partial b}^{2} s_{\overline{b}}^{2}}$



$\displaystyle s_{\overline{g}} = 16.7737862121351 \, c m^{2}$



$\displaystyle g = (50 \pm 20) \, c m^{2}$



$\displaystyle \nu_{g} = \frac{s_{\overline{g}}^{4}}{\frac{\frac{\partial g}{\partial a}^{4} s_{\overline{a}}^{4}}{\nu_{a}} + \frac{2 \frac{\partial g}{\partial a}^{3} \frac{\partial g}{\partial b} s_{\overline{ab}} s_{\overline{a}}^{2}}{\nu_{a}} + \frac{\frac{\partial g}{\partial a}^{2} \frac{\partial g}{\partial b}^{2} s_{\overline{ab}}^{2}}{\nu_{b}} + \frac{\frac{\partial g}{\partial a}^{2} \frac{\partial g}{\partial b}^{2} s_{\overline{ab}}^{2}}{\nu_{a}} + \frac{2 \frac{\partial g}{\partial a} \frac{\partial g}{\partial b}^{3} s_{\overline{ab}} s_{\overline{b}}^{2}}{\nu_{b}} + \frac{\frac{\partial g}{\partial b}^{4} s_{\overline{b}}^{4}}{\nu_{b}}} = 4.29353572447403 \approx 4$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad g_{ \, 95\%}=(50 \pm 50) \, c m^{2}$


Y se puede acceder a la Matrix de covarianzas simbólica


```python
g.sym.covMatrix
```




$\displaystyle \left[\begin{matrix}s_{\overline{b}}^{2} & s_{\overline{ab}}\\s_{\overline{ab}} & s_{\overline{a}}^{2}\end{matrix}\right]$



# Listas de Variables

Si se realizan N conjuntos de mediciones de una cantidad, es conveniente almacenarlas juntas, en el tipo `objects.varList`. Y acceder a ellas llamando a la variable con el respectivo subíndice.


```python
T = varList('T', [[23,23,23,24], [25,25,27,27,28], [30,30,28,29,30]], 'C')
```


$\displaystyle T_{1} = (23.2 \pm 0.2) \, C$



$\displaystyle T_{2} = (26.4 \pm 0.6) \, C$



$\displaystyle T_{3} = (29.4 \pm 0.4) \, C$



```python
T(1)
```




$\displaystyle T_{1}$




```python
T(2).val
```




    26.4




```python
T.u
```




    array([0.2, 0.6, 0.4])



# Tablas

Los archivos de datos a introducir deben tener dos columnas para cada variable, el valor y la incertidumbre. Se debe inicializar una variable de tipo `objects.table` indicando el nombre del archivo, y en caso de no estar presente en el archivo, los nombres de las variables. \
Las variables se almacenaran en tipo `objects.varList` y son atributo de la tabla con el nombre que se les dio.


```python
tabla = table('examples/data.dat', vbs=0)
```


```python
tabla
```


|    | $V\, [V]$   | $u_{V}\, [V]$   | $l\, [m]$   | $u_{l}\, [m]$   |
|---:|:------------|:----------------|:------------|:----------------|
|  0 | $1.0$       | $0.1$           | $2.0$       | $0.1$           |
|  1 | $2.0$       | $0.1$           | $3.0$       | $0.1$           |
|  2 | $3.0$       | $0.1$           | $4.0$       | $0.1$           |
|  3 | $4.0$       | $0.1$           | $5.0$       | $0.1$           |
|  4 | $5.0$       | $0.1$           | $6.0$       | $0.1$           |





    None




```python
tabla.V
```




$\displaystyle V$




```python
tabla.l.val, tabla.V.u
```




    (array([2., 3., 4., 5., 6.]), array([0.1, 0.1, 0.1, 0.1, 0.1]))



A continuación se muestra el caso en que el archivo no tiene los nombres de las variables.


```python
tabla = table('examples/datanh.dat', varNames='V [V], l [m]', vbs=0)
```


```python
tabla
```


|    | $V\, [V]$   | $u_{V}\, [V]$   | $l\, [m]$   | $u_{l}\, [m]$   |
|---:|:------------|:----------------|:------------|:----------------|
|  0 | $1.0$       | $0.1$           | $2.0$       | $0.1$           |
|  1 | $2.0$       | $0.1$           | $3.0$       | $0.1$           |
|  2 | $3.0$       | $0.1$           | $4.0$       | $0.1$           |
|  3 | $4.0$       | $0.1$           | $5.0$       | $0.1$           |
|  4 | $5.0$       | $0.1$           | $6.0$       | $0.1$           |





    None




```python
tabla.V()
```


|    | $V\, [V]$   |
|---:|:------------|
|  0 | $1.0$       |
|  1 | $2.0$       |
|  2 | $3.0$       |
|  3 | $4.0$       |
|  4 | $5.0$       |





$\displaystyle V$



# Funciones de ajuste

Las funciones de ajuste son de tipo `objects.funcFit` y se requiere que los parámetros de ajuste sean de tipo `objects.var` y tanto la variable independiente, como la dependiente sean de tipo `objects.varList`. \
El cálculo retorna los valores apropiados de los parámetros de ajuste, la tabla de restos y los graficos interactivos de la función y los restos.


```python
# Configuración inicial para gráficos interactivos
%matplotlib widget
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10, 5)
```


```python
a, b, c = var('a', -1), var('b', 2), var('c', 5)

x = varList('x', [{'val': -0.59, 'sd':0.1, 'n':6}, {'val': 0.27, 'sd':0.1, 'n':6}, {'val': 0.98, 'sd':0.1, 'n':6}, {'val': 1.87, 'sd':0.1, 'n':6}], 'm', vbs=0)

h = varList('h', [{'val': 0.55, 'sd':0.1, 'n':6}, {'val': 3.78, 'sd':0.1, 'n':6}, {'val': 4, 'sd':0.1, 'n':6}, {'val': 1.62, 'sd':0.1, 'n':6}], 'm', vbs=0)
```


```python
h_f = funcFit('h', a*x**2+b*x+c, h)
```


$\displaystyle h = a x^{2} + b x + c$



$\displaystyle b = (3.01 \pm 0.07) \, \mathtt{\text{}}$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad b_{ \, 95\%}=(3.01 \pm 0.87) \, \mathtt{\text{}}$



$\displaystyle a = (-2.03 \pm 0.05) \, \mathtt{\text{}}$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad a_{ \, 95\%}=(-2.03 \pm 0.58) \, \mathtt{\text{}}$



$\displaystyle c = (3.05 \pm 0.04) \, \mathtt{\text{}}$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad c_{ \, 95\%}=(3.05 \pm 0.55) \, \mathtt{\text{}}$



|    | $r\, [m]$   |
|---:|:------------|
|  0 | $-0.02$     |
|  1 | $0.06$      |
|  2 | $-0.06$     |
|  3 | $0.02$      |




<div style="display: inline-block;">
    <div class="jupyter-widgets widget-label" style="text-align: center;">
        Figure
    </div>
    <img src='data:image/png;base64,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6YX2PICyiE8tAIAS63xqqp5auVK1vv5aC48d00ft2+vXhx/WIw0bMmIO5EM1Dw993bWrYkaMULi/v0YsWaJG33+v+UePimmKCiYlKVPblybkmrU9LTlDz7X4Rr+8t15n9x/TL++t13MtvslVpOe13d1av369mjRpkqtt8ODBqlWrlt566y1J0rhx47RixQotXrz4tqekR0VFSZImTZqkl156SdHR0apSpYrGjBmTq1+zZs20bds2paenF9pzAcoarkEHAJQ4adeu6eNduzRh61bZWCx6/Z579FRYGDNTA3eotre3ZvXura2xsRqzbp16zZ6tewIC9E6bNronIMDseCVKQvz/F98LJ23V6QMXZGT//5cdpw9c0PQ3N6v7qOY39C8sJ0+eVKVKlXK1WSwWjR8/Xv3795e/v78mTpyo9evXKyAfv9+oqCh5eXlpxowZ8vHxkST16tVLX3zxRa5+lSpVUkZGhuLi4lS1atXCe0JAGUKBDgAoMbINQ1P279fLGzYoNiVFoxo10isREaxjDhSS5hUratXAgVp64oTGrl+vVtOmqU+NGnqvbVvV8PQ0O16JsPzHczn/H7PibJ59ti48q5T0M0WWIS0tLc+Z53v06KG6devq9ddf17Jly1SvXr187S8qKkq9e/fOKc4l6fjx46pRo0aufs5//C1OTU29i/RA2UaBDgAoEVaePKnn167V7nPn1L9WLU1o3ZqCASgCFotFXYOD1SUoSNMPHtSYdetU99tv9XTjxno5IkLujo5mR7Rq15dSk6Ryjmf1y/5jN/Rp3j1A3UdVlqScJdgKk4+PjxISblx/fcmSJTp48KCysrLk5+eX7/1FRUXphRdeuKGtTZs2udouXbokSapQocIdpAYgcQ06AMDKHUlIUK/Zs9Vp5kw52tpq45AhmtmrF8U5UMRsLBbdX6eODj70kP4dEaFPo6JU46uv9HlUlDKZSO6mri+l5hvopMEvRyiwjo8sNpacW2AdHw1+OSKnz/VivjCFhYVp//79udp27dqlgQMH6uuvv1bHjh31yiuv5GtfV65c0bFjxxQWFparPSoqSo0aNcrVFhMTo8qVK+caaQdQMIygAwAKXUpiZp4THpVzy70m8K0kZ2Tora1b9cGOHfJ3cdFPPXpoQEiILBZLYccFcAsu9vZ6OSJCDzVooJfWr9cTK1bok9279VH79upcSGtslwbl3OwUHumpcm7//zfOubyDPtjykKa/uVlbF55V8+4BGvxyhJzLO9xyu7sVGRmpsWPHKiEhQZ6enjpx4oS6d++ul156SUOGDFG1atUUERGhXbt2qXHjxrfcV3R0tGxtbdWgQYOctpMnTyohIeGGAn39+vXq0qVLoT0PoCyiQAcAFLqYzYnavvTG0yvDIz3VvKv3Lbc1DEPTDx7U82vX6uLVqxrbrJleaNZMLvb2RRUXQD5UKl9ek7t10+iwMP1j9Wp1mTVLfWrU0Mft26vqbWYBLwvKudvl+ffNubyDuo9qrpT0M+o+qnKu4vxW292NBg0aqHHjxpoxY4YGDBigrl27qnfv3jmzrjdv3lzdunXTSy+9pCVLlkiSJk+erJEjR94we39UVJRCQkJyXdO+e/dueXh4KOhPX9BcvXpVc+bMydkfgDtjMVhDo0xJSkqSu7u7EhMT5ebmZnYcACVQSmKmYjYnqn6E+01Hw1MSM3UxNlULPtmuPWvj1bCtn3qMDpd3RZdbbrNixW/6JHmbVpw/oftq1tT77dopiA/+gNUxDEM/HTqk59asUcLVq3q5RQs917SpHO1Kz9jP1atXdfz4cQUHB+c54VpBnDt9VTM+PKOBz1aWb+Dd7Su/Fi5cqOeff14xMTGysbn9Va3jxo3T2rVrtWbNmjt6vM8++0yzZ8/WsmXL7mh7FJ1bHcvUBtan9PwVBQAUi+tr9gbXK3fTYtvGNltv95+q0wcuSJLO7j+mmDWH9cGWh/Lsn5SerjdWblPVDRWVUSNbywcMUCeW6AGslsVi0eDatdW9WjW9tmmT/r1xo77bt0+TOnXivfsn1y/3ub6U2vX/FuRynzvVvXt3HT58WGfPnlVgYOBt+y9evFiffPLJHT+evb29Jk6ceMfbA/gdBToA4I7cau3e/Kz9e92Kkyf13vbtckl1UFVV1LQePVSpqkuR5QZQeFwdHPR+u3YaUa+eRq9cqc4zZ2pArVr6sH17VXZ1NTue6f56uc/12drzc7lPYXjmmWfy3Xfbtm139ViPPPLIXW0P4HcU6ACAO3KrZYEKtvavrR5Wi5yf7PJxKiYA61K/QgWtHjRIUw8c0HNr1qj2N99ofKtWGh0WJtsy/J6uH+Gu4HrlbmgvzAnhAJQu/HUAANyRP6/1+1e3Wvs38olKmrJ/v77cs0ceTk56oVkzta1cuUjWAgZQfCwWi4bWrase1avrX+vX6x+rV2vqgQP6KjJSDcroutjl3Iv+VHYApQt/MQAAd+T6Wr95GfxyhLYvOJBzDbokBdbxUY1HghW5eoYOXLyop5s11mv33KPyDoW/BjAA87g7OuqTTp10f506enTZMjX+4Qe9EB6uVyIi5FSKJpEDgKLAX0kAQIHkZ83e7CwbjZl1f84s7vXa+OpsK3v1+mWeqld01/YHHlCYn1+B9wug5GgZEKDdw4bp7a1bNX7rVs389Vf9r3NntatSxexoAGC1WGatjGEpBQDFYeuSi3mug55RL1V/f6g+15kDZcyBixf12LJl2nD2rB5p0EDvt2snd0dHs2Pd0vWlqYKCguTs7Gx2HOCOpaWl6cSJEyyzVkIwTAEAKHT1I9zlF+Koibt2acahQwqtUEHjWrZU3cpBFOdAGVTH21trBw/W/6Kj9cK6dVp64oS+joxU56Ags6PdlL29vSQpNTWVAh0lWmpqqqT/P6Zh3SjQAQCFblPCGT26fJnOp6ZqQtc2GtWoUZmeyRmAZGOx6PFGjdQtOFgPL12qLrNm6W+hoXqvbVu5WuFcFLa2tvLw8NC5c79PXuni4iKLxWJyKiD/DMNQamqqzp07Jw8PD9na2podCfnAKe5lDKexAChKKRkZenHdOk2KilL7wEB9FRmpah4eZscCYGUMw9AX0dH659q18nF21jddu6qDFV6bbhiG4uLidPnyZbOjAHfMw8ND/v7+eX7BRG1gfSjQyxjehACKytbYWD24aJHOXLmid9u00ZNhYbJhtAnALRy/fFkPLV2qNadP68lGjfROmzZWubJDVlaWrl27ZnYMoMDs7e1vOXJObWB9KNDLGN6EAArbtawsvb55s97aulVN/fz0/b33KsTLy+xYAEqIbMPQp7t368V161SpfHlN6d5dzStWNDsWUCZQG1gfLggEANyx/RcuqMXUqXp72za92rKlNt5/P8U5gAKxsVg0unFjRQ0fLi8nJ90zdape37RJmdnZZkcDgGJHgQ4AKDDDMPSfnTvV+IcflHbtmrbcf79eiYhghnYAd6ymp6c2DBmil5o312ubN6vN9Ok6yrXfAMoYPkkBAArkXEqKevzyi55ZvVqPh4Zq54MPqom/v9mxAJQC9ra2er1VK60fPFhxKSlq9N13+nbvXnFFJoCyggIdAJBvy06cUMPvvtP2uDgt6tdPH3foIGfWVQVQyFoGBChq2DDdV6uWHlq6VAPmzdOltDSzYwFAkaNABwDcVkZWlp5fs0aRs2Yp1NdXe0aMULdq1cyOBaAUc3N01ORu3TSjZ0+tOn1ajb7/XpvOnjU7FgAUKQp0AMAtHU5IUMupU/WfXbv0Xtu2WnzfffIvV87sWADKiAEhIYoaNkyBrq5qM326JmzdqmxOeQdQSlGgAwBuasr+/Qr7/nslZWRo8/3365/h4axtDqDYVXFz05pBg/RCs2b61/r16vbzz4pPSTE7FgAUOgp0AMAN0q5d02PLlunBRYvUr2ZN7WIiOAAms7e11VutW2tp//6KOndOjb7/XitPnjQ7FgAUKgp0AEAuhxMSFDF1qn7Yv19fRUbqu27dVN7BwexYACBJ6hwUpOjhw1XP21udZ87UKxs2sGY6gFKDAh0AkGPmoUNq8sMPSs3M1NahQ/VwgwaycEo7ACvjX66clvbvrzdatdJbW7cqctYsneOUdwClAAU6AEDpmZl6auVKDZw/X/cGB2vHAw+oYYUKZscCgJuytbHRv1q00MoBAxRz4YIa//ADs7wDKPEo0AGgjDuVlKTW06frf3v2aFLHjprWo4fcHB3NjgUA+dKuShXtHjZMQe7uavvTT/rvrl0ymOUdQAlFgW6Szz77TA0bNpSbm5vc3NwUERGhxYsX37T/5MmTZbFYct2cnJyKMTGA0mjVqVNq8sMPOp+aqo1DhujJsDBOaQdQ4lQqX16rBw7UU2FhenrVKg1ZsEDJGRlmxwKAAqNAN0nlypX19ttva+fOndqxY4c6dOig3r17a9++fTfdxs3NTbGxsTm3k8xcCuAOGYah97dvV+eZMxXm66sdDz6opszSDqAEs7e11Yft22tGz55aeOyYmk2ZogMXL5odCwAKxM7sAGVVz549c/08fvx4ffbZZ9qyZYvq1auX5zYWi0X+fIAGcJeSMzL08NKlmnHokMY0a6Y3W7WSrQ3f1wIoHQaEhKiBj4/umzdPzaZM0Q/33qs+NWuaHQsA8oVPZFYgKytL06dPV0pKiiIiIm7aLzk5WVWrVlVgYOBtR9sBIC/Xl1BbdOyYZvXqpQlt2lCcAyh1ant7a+vQoYoMClLfuXP16saNyua6dAAlACPoJtq7d68iIiJ09epVlS9fXrNnz1bdunXz7BsSEqJvvvlGDRs2VGJiot5//321bNlS+/btU+XKlW/6GOnp6UpPT8/5OSkpqdCfB4CSYeHRoxq6aJH8XFy0dehQ1fXxMTsSABSZ8g4Omtmrl97aulWvbNig6PPn9f2998rVwcHsaABwUxaDaS5Nk5GRoVOnTikxMVGzZs3SV199pbVr1960SP+za9euqU6dOhoyZIjeeOONm/Z79dVX9dprr93QnpiYKDc3t7vKD6BkMAxD72zbppfWr1fP6tX1/b33yp1Z2gGUIfOPHtXQhQsV6OqquX36qIanp9mRAKuQlJQkd3d3agMrQoFuRTp16qTq1avriy++yFf/AQMGyM7OTtOmTbtpn7xG0AMDA3kTAmXE1cxMPbJ0qX48cED/atFCr99zj2yYpR1AGXTw4kX1njNH51JTNb1HD0UGB5sdCTAdBbr14cJDK5KdnZ2rmL6VrKws7d27VxUrVrxlP0dHx5yl3K7fAJQNscnJajt9un4+fFjTevTQm61aUZwDKLOuX5feslIl3fvLL3p/+3bWSwdgdbgG3SRjx45Vt27dVKVKFV25ckVTp07VmjVrtHTpUknSsGHDFBAQoAkTJkiSXn/9dbVo0UI1atTQ5cuX9d577+nkyZN65JFHzHwaAKzUjrg49ZkzR4ak9YMHs4QaAEjycHLSvL599fKGDXp+7VodvHRJn3bqJAdbW7OjAYAkCnTTnDt3TsOGDVNsbKzc3d3VsGFDLV26VJ07d5YknTp1SjZ/mlk5ISFBjz76qOLi4uTp6akmTZpo06ZN+bpeHUDZ8tPBgxqxZIka+vhoTp8+qli+vNmRAMBq2NrYaEKbNqrj7a1Hly3TkYQE/dy7t7ydnc2OBgBcg17WcJ0JUHoZhqFxGzfqjS1b9EDduvqySxc52fE9LADczIYzZ9R37ly5OzpqQd++qu3tbXYkoFhRG1gfrkEHgFLgamamHli0SG9s2aK3WrfW9926UZwDwG20qlxZW4cOlaOtrVpMnaoVJ0+aHQlAGUeBDgAl3IXUVHWeOVM///qrZvTsqbHNm8vCZHAAkC/VPDy06f771aJiRXWdNUufR0WZHQlAGUaBDgAl2OGEBEVMnapDly5p9aBBGhASYnYkAChx3B0dtaBfPz3ZqJGeWLFCz61erWyuAgVgAs5/BIASav2ZM+ozZ458XVy0ZehQVfPwMDsSAJRYdjY2+m/Hjqrp6amnV63SqStX9H23bnK2tzc7GoAyhBF0ACiBfty/X51mzlRohQradP/9FOcAUEieatxYs/v00cJjx9Rp5kxdSE01OxKAMoQCHQBKEMMwNH7LFj2waJHur11bS/r3l6eTk9mxAKBU6V2jhlYPGqTDCQlqOW2ajl6+bHYkAGUEBToAlBBZ2dkatWKFXt6wQa+1bKlvunaVg62t2bEAoFRqXrGiNg8dKkmK+PFHbY2NNTkRgLKAAh0ASoC0a9fUf948/W/PHn0VGal/t2zJTO0AUMSqe3ho05AhqunpqfY//aS5R46YHQlAKUeBDgBW7lJamjrPmqWlJ05obp8+erhBA7MjAUCZ4ePiohUDBuje4GD1nTNHX0RHmx0JQClGgQ4AVuxUUpJaTZuWs4xa9+rVzY4EAGWOs729ZvTqpdFhYXp8+XK9vmmTDJZhA1AEWGYNAKzUnvPn1e3nn+Voa6uNQ4aolpeX2ZEAoMyysVj0nw4d5FeunF7esEHnUlP1nw4dZGvDeBeAwkOBDgBWaN3p0+o5e7ZqeHpqYb9+8i9XzuxIAFDmWSwW/atFC/m6uOjx5ct1Pi1N33frJkc7PlIDKBx85QcAVmbB0aOK/PlnNfX315pBgyjOAcDKPNqwoX7u1UtzjxxR919+0ZWMDLMjASglKNABwIr8uH+/+syZo27BwVrYr59cHRzMjgQAyEOfmjW1rH9/7YiPV7ufftK5lBSzIwEoBSjQAcBKTNy1Sw8sWqRh9eppRs+ecuKUSQCwam0CA7Vu8GD9lpyse6ZN08nERLMjASjhKNABwGSGYei1TZv091Wr9FzTpvo6MlJ2TDoEACVCwwoVtGnIEGUbhlpPn65fL10yOxKAEoxPgABgomzD0NOrVunVTZv0VuvWeq9tW1ksFrNjAQAKINjDQ+uHDJGrg4NaT5+u6HPnzI4EoISiQAcAk2RmZ2vE4sX6ZPdufdapk8Y2b05xDgAlVKXy5bV20CAFurqq3U8/afNvv5kdCUAJRIEOACbIyMrS4PnzNe3gQU3t0UOPN2pkdiQAwF3ycXHRyoEDVd/HR51nztTKkyfNjgSghKFAB4BidjUzU/3mztX8Y8f0c69eGly7ttmRAACFxN3RUUv791frgAB1/+UXzTtyxOxIAEoQCnQAKEYpGRnqOXu2Vp06pfl9+6pXjRpmRwIAFDIXe3vN7dtXPapVU7+5czXtwAGzIwEoISjQAaCYJKWnq9svv2jLb79p8X33qUtQkNmRAABFxMHWVtN79tQDdevqgUWL9F1MjNmRAJQALLILAMUg4epVdZ01S4cSErR8wAC1qFTJ7EgAgCJmZ2Ojb7p2lb2NjUYuWaJMw9DDDRqYHQuAFaNAB4Aidj41VV1mzdLpK1e0auBANfbzMzsSAKCY2Fgs+qJLF9nb2OiRpUt1LSuLiUEB3BQFOgAUoXMpKeowY4YupKVpzcCBql+hgtmRAADFzMZi0aROneRga6snVqxQRna2/t64sdmxAFghCnQAKCLxfxTnCVevau3gwQrx8jI7EgDAJBaLRR+1by97Gxs9vWqVrmVl6bnwcLNjAbAyFOgAUAT+XJyvHjSI4hwAIIvFonfbtpWDra3+uXatMrKzNbZ5c7NjAbAiFOgAUMjiUlLU4aeflJiRoTWDBqkWxTkA4A8Wi0VvtmolB1tbvbR+vbINQ/9q0cLsWACsBAU6ABSiuJQUtf/pJyX9UZzX9PQ0OxIAwMpYLBaNa9lSthaLXt6wQbYWi8Ywkg5AFOgAUGhik5PVYcYMXaE4BwDkw8sREcrMztbY9etla7Ho+WbNzI4EwGQU6ABQCGKTk9V+xgwl/1Gc16A4BwDkw7iWLZVlGHph3TrZ2tjo2aZNzY4EwEQU6ABwl86lpKgjxTkA4A5YLBa9fs89yjIMPbdmjWwsFj3TpInZsQCYhAIdAO7CxbQ0dZo5Uwnp6VpLcQ4AuAMWi0XjW7VSVna2/rF6tWwtFj3FOulAmUSBDgB36PLVq+oya5biUlKYrR0AcFcsFovebtNGWYahv69aJRuLRaPCwsyOBaCYUaADwB1ISk9X159/1onERK0eNEh1fXzMjgQAKOEsFovea9tW2Yah0StXysHWVo82bGh2LADFiAIdAAooOSND3X/5RQcvXdLKAQPUsEIFsyMBAEoJi8WiD9q1U3pWlv62bJnK2dvr/jp1zI4FoJhQoANAAaRdu6Zes2cr6tw5LR8wQE38/c2OBAAoZSwWiyZ27KjUa9c0bNEiOdvZqW/NmmbHAlAMbMwOUFZ99tlnatiwodzc3OTm5qaIiAgtXrz4ltvMnDlTtWvXlpOTkxo0aKBFixYVU1oAkpSemam+c+dqa2ysFt13n1pUqmR2JABAKWVjseiryEjdV6uWBs2fryXHj5sdCUAxoEA3SeXKlfX2229r586d2rFjhzp06KDevXtr3759efbftGmThgwZoocffli7d+9Wnz591KdPH8XExBRzcqBsyszO1pCFC7Xm9GnN69tXrStXNjsSAKCUs7Wx0ZR771XX4GD1nTtXa06dMjsSgCJmMQzDMDsEfufl5aX33ntPDz/88A33DRo0SCkpKVqwYEFOW4sWLdSoUSN9/vnn+X6MpKQkubu7KzExUW5uboWSGyjtsg1DIxcv1tSDBzW7d2/1qF7d7EgAgDLkamames6erc2//aYVAwZwBhcKDbWB9WEE3QpkZWVp+vTpSklJUURERJ59Nm/erE6dOuVqi4yM1ObNm4sjIlBmGYahp1et0g/79+uHe++lOAcAFDsnOzvN6d1bYb6+6vrzz9odH292JABFhALdRHv37lX58uXl6Oioxx9/XLNnz1bdunXz7BsXFyc/P79cbX5+foqLi7vlY6SnpyspKSnXDUD+vbJxoz7ZvVufd+6swbVrmx0HAFBGlXNw0MJ+/VTTw0NdZs3SoUuXzI4EoAhQoJsoJCREUVFR2rp1q5544gkNHz5c+/fvL9THmDBhgtzd3XNugYGBhbp/oDR7b9s2jd+yRe+2aaPHQkPNjgMAKOPcHB21pH9/+bq4qPPMmTrNwAtQ6lCgm8jBwUE1atRQkyZNNGHCBIWGhuo///lPnn39/f0V/5fTmeLj4+V/myWexo4dq8TExJzb6dOnCy0/UJp9ER2tF9at079atNDzzZqZHQcAAEmSt7OzlvXvLxuLRV1mzdKF1FSzIwEoRBToViQ7O1vp6el53hcREaGVK1fmalu+fPlNr1m/ztHRMWcpt+s3ALc27cABPbF8uZ4KC9Mb99xjdhwAAHIJcHXV8gEDdOnqVXX7+Wcl3eTzI4CShwLdJGPHjtW6det04sQJ7d27V2PHjtWaNWs0dOhQSdKwYcM0duzYnP5PP/20lixZog8++EAHDx7Uq6++qh07dmj06NFmPQWgVFpy/LiGLV6sB+vW1ccdOshisZgdCQCAG9T09NTS/v31a0KC+syZo6uZmWZHAlAIKNBNcu7cOQ0bNkwhISHq2LGjtm/frqVLl6pz586SpFOnTik2Njanf8uWLTV16lT973//U2hoqGbNmqU5c+aofv36Zj0FoNTZGhur++bOVdegIH3dtatsKM4BAFaska+vFvTrp82xsRq8YIEys7PNjgTgLrEOehnDWodA3g5cvKhW06apjre3lvXvLxd7e7MjAQCQLwuPHlWfuXP1QJ06fMGMAqE2sD6MoAMo804nJSly1ixVKl9e8/v2pTgHAJQo3atX13fduum7ffv0wtq1ZscBcBfszA4AAGa6mJamyFmzZGOxaMl998nTycnsSAAAFNj9deroYlqa/r5qlSqVL69nmzY1OxKAO0CBDqDMSsnIUI9fftH5tDRtGDJEAa6uZkcCAOCOPdW4sWJTUvTcmjWqWK6chtSpY3YkAAVEgQ6gTLqWlaUB8+dr74ULWj1woEK8vMyOBADAXRvfqpV+S07W8MWLVcHFRZ2qVjU7EoAC4Bp0AGWOYRh6dNkyrTh5Ur/07q3wihXNjgQAQKGwWCz6sksXdaxSRX3nzNHu+HizIwEoAAp0AGXOvzdu1Hf79mlyt27qEhRkdhwAAAqVva2tZvbqpTre3ur28886dvmy2ZEA5BMFOoAy5YvoaL25ZYveadNG93NtHgCglCrv4KCF/frJ1cFBkbNm6VxKitmRAOQDBTqAMmPB0aN6csUKjQ4L0/Ph4WbHAQCgSFVwcdHS/v11JSNDPWbPVnJGhtmRANwGBTqAMmFbbKwGzZ+vXtWr6+P27WWxWMyOBABAkavm4aFF992nAxcvavCCBcrMzjY7EoBboEAHUOodvXxZPX75RaG+vpravbtsbfjTBwAoOxr7+WlWr15acvy4/r5ypQzDMDsSgJvgUyqAUu18aqq6zpolTycnzevTR8729mZHAgCg2EUGB+vzzp31WXS03t++3ew4AG6CddABlFqp166p1+zZSsrI0Ob775ePi4vZkQAAMM0jDRvqeGKiXli3TlXd3DSwdm2zIwH4Cwp0AKVStmHogUWLtOf8ea0dPFjVPDzMjgQAgOnebNVKJ5KSNGzxYgW4uuqegACzIwH4E05xB1Aqvbh2reYeOaLpPXuqqb+/2XEAALAKFotF30RGqkXFiuo1e7Z+vXTJ7EgA/oQCHUCp80V0tN7fsUMftW+vntWrmx0HAACr4mhnp9l9+sjXxUXdfv6ZNdIBK0KBDqBUWXr8uEatWKGnwsL098aNzY4DAIBV8nRy0qJ+/ZRy7Zp6zZmjtGvXzI4EQBToAEqRvefPa8D8+eoaHKyP2rc3Ow4AAFYt2MNDC/r1057z5zV88WJls/waYDoKdAClQmxysrr/8ouqe3hoeo8erHUOAEA+NPX315R779XMX3/VuI0bzY4DlHl8ggVQ4qVkZKjX7NnKNgwt6NtX5R0czI4EAECJ0a9WLb3durXe3LJFU/bvNzsOUKaxzBqAEu36cmoHLl3ShiFDFODqanYkAABKnBeaNdOhhAQ9vHSpgtzc1KpyZbMjAWUSI+gASrSX1q/XvKNHNb1HDzXy9TU7DgAAJZLFYtHnnTurRcWK6jt3ro5dvmx2JKBMokAHUGJ9FxOjd7Zt0/tt26oHy6kBAHBXHGxt9Uvv3vJwdFSPX37R5atXzY4ElDkU6ABKpE1nz+qx5cv1cIMGeqZJE7PjAABQKng7O2tBv36KTUnRwPnzdS0ry+xIQJlCgQ6gxDmZmKg+c+aoRcWK+rRTJ1ksFrMjAQBQaoR4eenn3r21+vRpPb1qldlxgDKFAh1AiXIlI0M9Z89WeQcH/dyrlxxsbc2OBABAqdOhShV91qmTPouO1qe7d5sdBygzmMUdQImRbRh6YOFCnUhK0ub775ePi4vZkQAAKLUeadhQey9c0N9XrVJtb291qFLF7EhAqccIOoAS46X167Xg2DH91KOH6vn4mB0HAIBS74N27dS+ShUNmDdPR5nZHShyFOgASoTv9+3LmbG9W7VqZscBAKBMsLOx0U89esjLyUm9Zs9WUnq62ZGAUo0CHYDV2/Lbb3p02TJmbAcAwARezs6a37evzly5ogcWLVJWdrbZkYBSiwIdgFX7LTlZ/ebOVbi/PzO2AwBgktre3preo4cWHD2qlzdsMDsOUGpRoAOwWlczM9Vv7lzZ2tgwYzsAACbrVq2a3m3bVm9v26apBw6YHQcolZjFHYBVMgxDTyxfrujz57V+8GD5lStndiQAAMq855o21d7z5/Xw0qWq6eGh8IoVzY4ElCqMoAOwShN379bkffv0ZZcuaurvb3YcAAAgyWKx6IsuXdSoQgX1nTtXcSkpZkcCShUKdABWZ9WpU3p29Wo917SpHqhb1+w4AADgT5zs7PRz797KMgwNmDdPGVlZZkcCSg0KdABW5fjlyxowb546VKmit9u0MTsOAADIQ6Xy5fVzr17aGhurf6xebXYcoNSgQAdgNZIzMtRn7lx5Ojlpeo8esrPhTxQAANaqZUCAJnbsqE+jovTN3r1mxwFKBSaJA2AVDMPQQ0uW6Njly9oydKi8nJ3NjgQAAG7jb6Gh2hkfrydWrFB9Hx81Y9I44K4wPGWSCRMmKDw8XK6urvL19VWfPn106NChW24zefJkWSyWXDcnJ6diSgwUrQ927NDMX3/Vd926qZ6Pj9lxAABAPk3s0EFN/PzUj0njgLtGgW6StWvXatSoUdqyZYuWL1+ua9euqUuXLkq5zR81Nzc3xcbG5txOnjxZTImBorPq1Cm9uG6dxjZvrn61apkdBwAAFICjnZ1m9erFpHFAIeAUd5MsWbIk18+TJ0+Wr6+vdu7cqTa3mBjLYrHInyWnUIqcSkrSoPnz1bFKFb1xzz1mxwEAAHfg+qRx7X76Sf9YvVqTOnUyOxJQIjGCbiUSExMlSV5eXrfsl5ycrKpVqyowMFC9e/fWvn37btk/PT1dSUlJuW6Atbiaman75s5VOXt7TevRQ7ZMCgcAQIn150njvmXSOOCOMIJ+G/PmzSvwNp07d5ZzASa4ys7O1jPPPKN77rlH9evXv2m/kJAQffPNN2rYsKESExP1/vvvq2XLltq3b58qV66c5zYTJkzQa6+9VuDnABQ1wzA0asUKxVy8qI1DhsibSeEAACjx/hYaqu1xcXpy5Uo18vVVmJ+f2ZGAEsViGIZhdghrZlPAET2LxaLDhw+rWrVq+d7miSee0OLFi7Vhw4abFtp5uXbtmurUqaMhQ4bojTfeyLNPenq60tPTc35OSkpSYGCgEhMT5ebmlu/HAgrbF9HRenz5ck3u2lXDb/HFFAAAKFmuZmaq1bRpunT1qnY88AArs1ixpKQkubu7UxtYEc4nzYe4uDhlZ2fn6+bi4lKgfY8ePVoLFizQ6tWrC1ScS5K9vb3CwsJ05MiRm/ZxdHSUm5tbrhtgti2//aanVq7Uk40aUZwDAFDKOP0xaVxieroeXLRI2YwHAvlGgX4bw4cPL9Dp6g888EC+imDDMDR69GjNnj1bq1atUnBwcIGzZWVlae/evarIepMoQeJTUnTfvHlq6u+vj9q3NzsOAAAoAkHu7vqxe3ctPn5cb27ebHYcoMTgFHeTPPnkk5o6darmzp2rkJCQnHZ3d/ecLwSGDRumgIAATZgwQZL0+uuvq0WLFqpRo4YuX76s9957T3PmzNHOnTtVt27dfD0up7HATJnZ2eoyc6b2X7yoXcOGqVL58mZHAgAARej1TZv06qZNWnTffep6BwNSKFrUBtaHSeIKICkpSd9++63i4uIUHBys0NBQNWjQoMCntUvSZ599Jklq165drvZvv/1WI0aMkCSdOnUq1zXwCQkJevTRRxUXFydPT081adJEmzZtyndxDpjt3xs3au2ZM1o5YADFOQAAZcDLERHaGhuroQsXaueDDyrI3d3sSIBVYwS9ADp16qTo6GiFh4fr1KlTOnTokCSpevXqCg0N1U8//WRywtvjWzKYZf7Ro+o1e7bebt1aLzZvbnYcAABQTC6lpanplCnycnLShiFD5GTHGKG1oDawPrw7CmDz5s1as2aNwsPDJf0+Q/revXsVFRWl6Ohok9MB1uv45csatmiRelWvruebNTM7DgAAKEZezs76uVcvtZw2TU+tXKkvIyPNjgRYLQr0AmjYsKHs/vSNn6Ojo5o2baqmTZuamAqwblczM9V//nx5OjlpcrdusrFYzI4EAACKWZifnz7r1EkjlyzRPQEBGsEqLkCemMW9AN599139+9//zrWuOIBbe3rVKu27cEE/9+olTycns+MAAACTjKhfXw83aKAnV6zQ3vPnzY4DWCUK9AIICgpSUlKS6tatq5deeknz5s3T6dOnzY4FWK3v9+3T//bs0ScdOyrMz8/sOAAAwGQTO3RQTU9PDZg/X1cyMsyOA1gdCvQCuO+++3TixAndc8892rRpk4YPH66goCBVqFBBXbp0MTseYFX2nj+vx5cv14h69fRwgwZmxwEAAFbA2d5eM3v21G/JyXps2TIxXzWQG9egF0BMTIw2b96s0NDQnLYTJ05o9+7d2rNnj4nJAOuSlJ6u/vPmqaanpyZ16iQL150DAIA/1PLy0lddumjQggVqW7myHm/UyOxIgNWgQC+A8PBwpaSk5GoLCgpSUFCQ+vbta1IqwLoYhqG/LV+u2JQU7XzwQbnY25sdCQAAWJmBtWtr/dmzenr1aoX7+6uJv7/ZkQCrwCnuBfD000/r1Vdf1eXLl82OAlitL/fs0fSDB/Vlly6q6elpdhwAAGCl3m/bVg19fDRg/nxdvnrV7DiAVbAYXPiRbzY2v3+f4e3trb59+6p58+YKCwtT/fr15eDgYHK6/ElKSpK7u7sSExPl5uZmdhyUMtHnzqn5jz/qofr19WnnzmbHAQAAVu745ctq/MMPahcYqF969+ayuGJGbWB9GEEvgOPHj2vOnDl66qmndPHiRb311lsKDw+Xq6urGjZsaHY8wFRXMjI0YP581fH21oft25sdBwAAlADBHh76rls3zTlyRB/t3Gl2HMB0XINeAFWrVlXVqlXVq1evnLYrV64oKiqKSeJQphmGob8tW6bY5GTtGjZMTnb8aQEAAPnTq0YNPR8erhfXrdM9AQFqXrGi2ZEA0zCCfht79uxRdnb2Te93dXVV69atNWrUKEnSvn37lJmZWVzxAKvw1d69mnbwoL6MjOS6cwAAUGDjW7VSUz8/DeZ6dJRxFOi3ERYWposXL+a7f0REhE6dOlWEiQDrEn3unJ5auVKPh4ZqcO3aZscBAAAlkL2trab16KHL6el6ZOlS1kdHmcV5qLdhGIZeeeUVubi45Kt/RkZGEScCrMeVjAwNnD9ftb289BHXnQMAgLsQ5O6uryMjdd+8efo8OlpPsD46yiAK9Nto06aNDh06lO/+ERERcnZ2LsJEgHUwDENPLF+u35KTtfPBB7nuHAAA3LV+tWppVKNG+sfq1YqoVEmNfH3NjgQUKz5R38aaNWvMjgBYpe/27dOPBw7ox+7dVcvLy+w4AACglHi/XTtt/O03DZo/XzsffFDlS8hyxkBh4Bp0AAV26NIljVqxQiPr19f9deqYHQcAAJQiTnZ2+qlHD51NTtaTK1aYHQcoVhToAAokPTNTgxcsUKCbmyZ26GB2HAAAUArV8vLS550764f9+/VdTIzZcYBiQ4EOoEBeWLdO+y9e1PQePVSOU84AAEAReaBuXY2sX19PrlihgwVYVQkoySjQC2D79u3q2LGjGjZsqH79+un111/XvHnzWFYNZcb8o0f131279H7btkzaAgAAitzEDh1U1c1NgxYs0NXMTLPjAEWOAr0AHnzwQdna2uqxxx5TcHCw1q5dq5EjRyooKEje3t5mxwOK1NkrVzRyyRL1ql5do8PCzI4DAADKgHIODprWo4cOXrqkMevWmR0HKHLM4l4Ap0+f1sKFC1W9evVc7SdPnlRUVJQ5oYBikJWdrQcWLZKTra2+6dpVFovF7EgAAKCMCPX11Xtt2+rpVavUJShI91arZnYkoMgwgl4A99xzj86cOXNDe9WqVdW7d28TEgHFY8LWrVp7+rSm3HuvvJ2dzY4DAADKmKfCwnRvcLBGLF6s2ORks+MARYYC/Tb69eunV199VbNnz9bjjz+uN954QwkJCWbHAorNxrNn9eqmTXq5RQu1q1LF7DgAAKAMslgs+rZrV9lYLBqxZImyDcPsSECR4BT326hevbo2btyoTz/9VBcuXJAk1apVS71791aLFi0UFhamBg0ayIHZrFEKXb56VUMXLlSLSpX075YtzY4DAADKMN9y5fT9vfcqctYsfbRjh54LDzc7ElDoLIbB10/5dfbsWUVFReW6HTt2THZ2dgoJCdGePXvMjnhbSUlJcnd3V2Jiotzc3MyOAys3dOFCLTh6VHuGD1dVd3ez4wAAAOj5NWv0n127tPn++9XE39/sOCUatYH1YQS9AAICAhQQEKDu3bvntCUnJysqKkrR0dEmJgMK35T9+zX1wAFN7d6d4hwAAFiN8a1ba9Xp0xqycKF2PfigynMmK0oRrkG/S+XLl1erVq00atQos6MAheb45ct6csUKPVC3robUqWN2HAAAgBwOtraa1r27fktO1tOrVpkdByhUFOgAcsn8Y0k1H2dnTerY0ew4AAAAN6jl5aWJHTrom5gYzTx0yOw4QKGhQAeQy/gtW7QlNlZT7r1Xbo6OZscBAADI04j69TWgVi39bflynblyxew4QKGgQAeQY9PZs3p982a90qKFWgYEmB0HAADgpiwWiz7v3FkudnYasXgxS6+hVKBAByBJSkpP1wOLFql5xYp6OSLC7DgAAAC35eXsrO+6ddPKU6f08c6dZscB7hoFOgBJ0uiVK3UhLU1T7r1Xdjb8aQAAACVDx6pV9WyTJhq7fr32nD9vdhzgrvApHICmHzyoH/bv16SOHVXNw8PsOAAAAAUyvnVrhXh6aujChbqamWl2HOCOUaADZdyZK1f0xPLlGhgSogfq1jU7DgAAQIE52dnpx+7ddTghQWPXrzc7DnDHKNCBMizbMDRi8WK52Nvrs06dZLFYzI4EAABwRxpUqKC327TRxzt3avmJE2bHAe4IBTpQhn2ye7dWnjqlyV27ysvZ2ew4AAAAd+XvjRurU9WqGrFkiS6mpZkdBygwCnSTTJgwQeHh4XJ1dZWvr6/69OmjQ4cO3Xa7mTNnqnbt2nJyclKDBg20aNGiYkiL0mj/hQt6cd06PRUWps5BQWbHAQAAuGs2Fou+69ZNVzMz9diyZTJYeg0lDAW6SdauXatRo0Zpy5YtWr58ua5du6YuXbooJSXlptts2rRJQ4YM0cMPP6zdu3erT58+6tOnj2JiYooxOUqDjKwsPbh4sYLc3PR2mzZmxwEAACg0lcqX1/+6dNEvhw/rh/37zY4DFIjF4Gslq3D+/Hn5+vpq7dq1anOTgmnQoEFKSUnRggULctpatGihRo0a6fPPP8/X4yQlJcnd3V2JiYlyc3MrlOwoeV7esEHvbNumLfffryb+/mbHAQAAKHTDFi3S3CNHtHfECFXhc2+eqA2sDyPoViIxMVGS5OXlddM+mzdvVqdOnXK1RUZGavPmzTfdJj09XUlJSbluKNs2nT2rCVu36tWWLSnOAQBAqfXfDh3k5uiokUuWKJsxSZQQFOhWIDs7W88884zuuece1a9f/6b94uLi5Ofnl6vNz89PcXFxN91mwoQJcnd3z7kFBgYWWm6UPMkZGXpw0SI1r1hRLzZrZnYcAACAIuPh5KTJXbtq1alT+mT3brPjAPlCgW4FRo0apZiYGE2fPr3Q9z127FglJibm3E6fPl3oj4GS49k1axSfmqrvu3WTnQ1vfwAAULp1rFpVf2/cWC+uW6eDFy+aHQe4LT6hm2z06NFasGCBVq9ercqVK9+yr7+/v+Lj43O1xcfHy/8Wpyk7OjrKzc0t1w1l08KjR/Xlnj36sF071fD0NDsOAABAsZjQurWqurnpwUWLdC0ry+w4wC1RoJvEMAyNHj1as2fP1qpVqxQcHHzbbSIiIrRy5cpcbcuXL1dERERRxUQpcTEtTY8sW6ZuwcF6tGFDs+MAAAAUGxd7e33frZt2nzunt7ZuNTsOcEsU6CYZNWqUpkyZoqlTp8rV1VVxcXGKi4tTWlpaTp9hw4Zp7NixOT8//fTTWrJkiT744AMdPHhQr776qnbs2KHRo0eb8RRQgjy1cqXSs7L0VWSkLBaL2XEAAACKVbOKFfWvFi30xubN2nGL+ZsAs1Ggm+Szzz5TYmKi2rVrp4oVK+bcfvrpp5w+p06dUmxsbM7PLVu21NSpU/W///1PoaGhmjVrlubMmXPLieWAmYcOadrBg/qkY0dVKl/e7DgAAACmeLlFC4X6+urBRYuUdu2a2XGAPLEOehnDWodlS3xKiupNnqx2lStrZq9ejJ4DAIAybf+FC2r8ww96PDRUH3foYHYc01EbWB9G0IFSyjAMPbZsmWwkfda5M8U5AAAo8+r6+GhC69b6z65dWsvqRrBCFOhAKfXD/v2ad/So/teliyq4uJgdBwAAwCo83aSJWleurIeWLFFyRobZcYBcKNCBUuh0UpL+vmqVHqxbV31q1jQ7DgAAgNWwsVj0TWSk4lJSNGbdOrPjALlQoAOljGEYenjpUpW3t9d/uLYKAADgBjU8PfVOmzaaFBWlVadOmR0HyEGBDpQyX0RHa/nJk/o6MlKeTk5mxwEAALBKT4aFqV1goB5askRXONUdVoICHShFjl++rH+uXavHGjZUZHCw2XEAAACs1vVT3S+kpen5tWvNjgNIokAHSo3sP05t93F21vvt2pkdBwAAwOoFe3jo/bZt9UV0tJadOGF2HIACHSgt/hcdrdWnT+vryEi5OjiYHQcAAKBE+FtoqDpVrapHli5VYnq62XFQxlGgA6XAicREPb92rf4WGqqOVauaHQcAAKDEsFgs+qpLF11OT9dza9aYHQdlHAU6UMIZhqFHli6Vl5OT3m3Txuw4AAAAJU5Vd3d92K6dvt67V4uOHTM7DsowCnSghPtyzx6tPHVKX0VGys3R0ew4AAAAJdLDDRooMihIjy1bxqnuMA0FOlCCnUxM1HNr1ujRhg3VOSjI7DgAAAAllsVi0f+6dFFSRgazusM0FOhACWUYhh5dtkyeTk56v21bs+MAAACUeFXc3PRe27b6cs8erTh50uw4KIMo0IES6uu9e7X85El92aULp7YDAAAUkkcbNlT7wEA9unSpkjMyzI6DMoYCHSiBTiUl6dk1a/RQ/fqKDA42Ow4AAECpYWOx6MvISJ1LTdXY9evNjoMyhgIdKGEMw9Dfli2Tm4ODPmjXzuw4AAAApU51Dw+91bq1Ptm9W+vPnDE7DsoQCnSghJmyf7+WnDihLzp3loeTk9lxAAAASqXRYWFqWamSHlqyRKnXrpkdB2UEBTpQgsSnpOiZ1as1tE4dda9e3ew4AAAApZatjY2+6dpVp69c0biNG82OgzKCAh0oQZ5auVI2Fos+bt/e7CgAAAClXoiXl16/5x59uHOntsbGmh0HZQAFOlBCzD58WDN//VUTO3aUj4uL2XEAAADKhGebNlVjX189tGSJ0jMzzY6DUo4CHSgBEq5e1ZMrVqhn9eoaFBJidhwAAIAyw87GRt927arDCQl6c8sWs+OglKNAB0qAf65Zo9Rr1/RZp06yWCxmxwEAAChT6leooJeaN9fb27Zp7/nzZsdBKUaBDli55SdO6JuYGL3frp0CXF3NjgMAAFAmjW3eXDU9PPTI0qXKys42Ow5KKQp0wIolZ2TosWXL1D4wUI80aGB2HAAAgDLL0c5OX3ftqu1xcZq4e7fZcVBK2ZkdAMDNvbxhg+JTU7V8wABObQcAADBZRKVKGh0Wpn+tX69I32B568aJe8u52amcO2UW7gxHDmClNv/2m/67a5fea9tWNTw9zY4DAAAASeNbt9acI0f06cz9Cjntf8P94ZGeat7V24RkKA04xR2wQhlZWXp06VI18fPT002amB0HAACgTElJzNTWJReVknjjsmquDg76onNnfX9ttxy7pMrm2knFrNgmm2sn1etvvqof4X7H+wYYQQes0DvbtungpUva+eCDsrPhezQAAIDilJKUqe1LExRcr1yep6t3q1ZN3atX1bSH56tcvCFJOrv/mGLWHNYHWx66q32jbOOIAKzMoUuX9OaWLfpneLhCfX3NjgMAAFBmJcRn3PS+VltctDAuW4bx/22nD1zQ9Dc3q/uo5ne0T4ACHbAi2Yahx5YtU6Crq8ZFRJgdBwAAoExb/uO5m94Xs+KcbCwWGX+u0CVtXXhWKelnijoaSikKdMCKfLN3r9adOaMVAwbI2d7e7DgAAABlWuehvvL0c8jzvnKOZ/XL/mM3tDfvHqDuoyrfdJ8J8Rm3LPxRtlGgA1YiLiVFz69dq+H16qlj1apmxwEAACjzPP0c5BvolOd9g1+O0PYFB3T6wIWctsA6Phr8coScy+dd1AO3Q4EOWIm/r1wpexsbfdCundlRAAAAyrRybnYKj/RUObebl0vZWTYaM+t+Lfhku/asjVfDtn7qMTpc2Vm3nuA3P/tG2WUx/nrRBEq1pKQkubu7KzExUW5ubmbHwR/mHz2qXrNn68fu3XV/nTpmxwEAAMBtbF1yUduXJtzQXpLWQac2sD58bQOY7EpGhp5csUJdg4I0pHZts+MAAAAgH+pHuCu4Xrkb2hkZx93g6AFM9vKGDbqUlqbPOneWxWIxOw4AAADyoZy7HeuYo9Dd+gIJFKl169apZ8+eqlSpkiwWi+bMmXPL/mvWrJHFYrnhFhcXVzyBUei2xcZq4q5deqNVKwW5u5sdBwAAAICJKNBNlJKSotDQUE2aNKlA2x06dEixsbE5N19f3yJKiKKUmZ2tvy1frka+vvp748ZmxwEAAABgMs7JMFG3bt3UrVu3Am/n6+srDw+Pwg+EYvXfXbsUfe6ctg4dKjsbvisDAAAAyjqqghKoUaNGqlixojp37qyNGzeaHQd34FRSkv69caNGhYUpvGJFs+MAAAAAsAKMoJcgFStW1Oeff66mTZsqPT1dX331ldq1a6etW7eq8U1OkU5PT1d6enrOz0lJScUVF7fw91Wr5ObgoDdbtTI7CgAAAAArQYFegoSEhCgkJCTn55YtW+ro0aP66KOP9MMPP+S5zYQJE/Taa68VV0Tkw9wjRzT3yBHN7NlT7o6OZscBAAAAYCU4xb2Ea9asmY4cOXLT+8eOHavExMSc2+nTp4sxHf7qSkaGRq9cqXuDg3VfrVpmxwEAAABgRRhBL+GioqJU8RbXMDs6OsqRUVqrMW7jRl1MS9OkTp1Y8xwAAABALhToJkpOTs41+n38+HFFRUXJy8tLVapU0dixY3X27Fl9//33kqSPP/5YwcHBqlevnq5evaqvvvpKq1at0rJly8x6CiiA3fHx+s+uXXqLNc8BAAAA5IEC3UQ7duxQ+/btc35+9tlnJUnDhw/X5MmTFRsbq1OnTuXcn5GRoeeee05nz56Vi4uLGjZsqBUrVuTaB6xT1h9rntf19tazTZuaHQcAAACAFbIYhmGYHQLFJykpSe7u7kpMTJSbm5vZccqMSbt3a/TKldo4ZIhaBgSYHQcAAACgNrBCTBIHFLHY5GS9tH69Hm3YkOIcAAAAwE1RoANF7J9r18rB1lZvt25tdhQAAAAAVoxr0IEitOrUKU09cEDfdu0qL2dns+MAAAAAsGKMoANFJCMrS0+uWKFWAQEaVq+e2XEAAAAAWDlG0IEi8sGOHTqSkKCZPXvKhjXPAQAAANwGI+hAETiRmKg3Nm/WM02aqEGFCmbHAQAAAFACUKADReDpVavk5eSkcS1bmh0FAAAAQAnBKe5AIZt35IjmHT2qmT17ytXBwew4AAAAAEoIRtCBQpR67Zr+vmqVIoOCdF+tWmbHAQAAAFCCMIIOFKLxW7YoLiVFKwYMkIWJ4QAAAAAUACPoQCE5ePGi3tu+XWOaNVMNT0+z4wAAAAAoYSjQgUJgGIZGr1ypQFdXvdismdlxAAAAAJRAnOIOFIJZv/6qladOaUHfvnK2tzc7DgAAAIASiBF04C4lZ2To2TVr1LN6dXWvXt3sOAAAAABKKAp04C69tXWrzqem6uP27c2OAgAAAKAEo0AH7sKvly7p/T8mhqvm4WF2HAAAAAAlGAU6cIcMw9DfV61SQPnyTAwHAAAA4K4xSRxwh+YcOaKlJ05oTp8+TAwHAAAA4K4xgg7cgdRr1/SP1avVLThYvZgYDgAAAEAhYAQduANvb92q2JQUrRgwQBaLxew4AAAAAEoBRtCBAjp6+bLe3b5dz4eHq4anp9lxAAAAAJQSFOhAAT29apX8XFz0UvPmZkcBAAAAUIpwijtQAAuOHtXCY8c0q1cvuTAxHAAAAIBCxAg6kE/pmZl6ZvVqdapaVf1q1jQ7DgAAAIBShhF0IJ8+3rlTJxITNa9PHyaGAwAAAFDoGEEH8uG35GS9sWWLnmrcWHV9fMyOAwAAAKAUokAH8uHFdevkYmencRERZkcBAAAAUEpxijtwG5vOntWU/fv1ZZcu8nByMjsOAAAAgFKKEXTgFrKys/X3VavUxM9PI+vXNzsOAAAAgFKMEXTgFr6NidHO+HhtHDJEtjZ8nwUAAACg6FBxADdx+epVjV2/Xg/UrauWAQFmxwEAAABQylGgAzfx2ubNSsvM1Dtt2pgdBQAAAEAZQIEO5GH/hQuauGuXXmnRQpXKlzc7DgAAAIAygAId+AvDMPT06tUKdnfXM02amB0HAAAAQBnBJHHAX8w7elQrTp7UvL595WjHWwQAAABA8WAEHfiT9MxMPbdmjboEBalHtWpmxwEAAABQhjA8CPzJf3ft0onERM3r00cWi8XsOAAAAADKEEbQTbRu3Tr17NlTlSpVksVi0Zw5c267zZo1a9S4cWM5OjqqRo0amjx5cpHnLCviU1L0xpYteqJRI9X18TE7DgAAAIAyhgLdRCkpKQoNDdWkSZPy1f/48ePq3r272rdvr6ioKD3zzDN65JFHtHTp0iJOWja8vGGD7Gxs9GrLlmZHAQAAAFAGcYq7ibp166Zu3brlu//nn3+u4OBgffDBB5KkOnXqaMOGDfroo48UGRlZVDHLhKhz5/T13r36uEMHeTs7mx0HAAAAQBnECHoJsnnzZnXq1ClXW2RkpDZv3mxSotLBMAw9s2qVant56YnQULPjAAAAACijGEEvQeLi4uTn55erzc/PT0lJSUpLS5NzHiO/6enpSk9Pz/k5KSmpyHOWNL8cPqy1Z85o8X33yd7W1uw4AAAAAMooRtBLuQkTJsjd3T3nFhgYaHYkq3I1M1P/XLNG9wYHq2twsNlxAAAAAJRhFOgliL+/v+Lj43O1xcfHy83NLc/Rc0kaO3asEhMTc26nT58ujqglxkc7d+pMcrI+bN/e7CgAAAAAyjhOcS9BIiIitGjRolxty5cvV0RExE23cXR0lKOjY1FHK5Fik5P11pYtGh0WphAvL7PjAAAAACjjGEE3UXJysqKiohQVFSXp92XUoqKidOrUKUm/j34PGzYsp//jjz+uY8eO6YUXXtDBgwf16aefasaMGfrHP/5hRvwS718bNsjRzk7/vsUXHAAAAABQXCjQTbRjxw6FhYUpLCxMkvTss88qLCxM//73vyVJsbGxOcW6JAUHB2vhwoVavny5QkND9cEHH+irr75iibU7sCs+XpNjYvR6y5bydHIyOw4AAAAAyGIYhmF2CBSfpKQkubu7KzExUW5ubmbHMYVhGOowY4biU1K0Z8QI2dnwPRUAAADKHmoD68M16Chz5h09qjWnT2tRv34U5wAAAACsBtUJypSMrCw9v3atugQFsawaAAAAAKvCCDrKlM+jo3X08mX93KuXLBaL2XEAAAAAIAcj6CgzLqWl6dVNm/RIgwZqUKGC2XEAAAAAIBcKdJQZb27ZomtZWXr9nnvMjgIAAAAAN6BAR5lwOCFBn+zerZdatJBfuXJmxwEAAACAG1Cgo0x4cd06VSxXTs80bmx2FAAAAADIE5PEodRbe/q0Zh8+rKndu8vZ3t7sOAAAAACQJ0bQUaplG4aeXbNGzStW1ODatc2OAwAAAAA3xQg6SrUp+/drV3y8Ng4ZwrJqAAAAAKwaI+gotVKvXdNL69drQK1aahkQYHYcAAAAALglCnSUWh/v3Klzqama0KaN2VEAAAAA4LYo0FEqnUtJ0dvbtmlUWJiqe3iYHQcAAAAAbosCHaXSa5s3y8Zi0cstWpgdBQAAAADyhQIdpc6hS5f0RXS0/tW8ubydnc2OAwAAAAD5QoGOUmfMunWq7Oqqpxo3NjsKAAAAAOQby6yhVFl/5ozmHDmiH7t3l5MdhzcAAACAkoMRdJQahmHon2vWqImfnwbXrm12HAAAAAAoEIYYUWrMOHRI2+LitHrgQNlYLGbHAQAAAIACYQQdpUJ6ZqbGrl+vntWrq12VKmbHAQAAAIACYwQdpcKkqCidSkrSwn79zI4CAAAAAHeEEXSUeAlXr+rNLVv0SMOGquPtbXYcAAAAALgjFOgo8d7askUZWVl6tWVLs6MAAAAAwB2jQEeJdiopSRN379bz4eHyL1fO7DgAAAAAcMco0FGivbJhg9wdHfVs06ZmRwEAAACAu0KBjhJrz/nz+mH/fo2LiJCrg4PZcQAAAADgrlCgo8Qas26danh66tGGDc2OAgAAAAB3jWXWUCKtPnVKi48f18yePWVva2t2HAAAAAC4a4ygo8TJNgy9sHatmvn7675atcyOAwAAAACFghF0lDizDh3Sjvh4rRk0SBaLxew4AAAAAFAoGEFHiZKRlaWXNmxQ92rV1DYw0Ow4AAAAAFBoGEFHifK/6Ggdu3xZs3v3NjsKAAAAABQqCnRYvZTETKUkZSo1M1P/Wx2jxwMby++qq1ISM1XOnUMYAAAAQOlAdQOrF7M5UduXJkiSHlNL6Yw0Y8sZhUd6qnlXb5PTAQAAAEDh4Bp0mCYlMVNbl1xUSmLmLfvVj3BXq+Fu+mXfcsWs2CabayfV62++qh/hftf7BgAAAABrQYEO06QkZWr70gSlJN26iLaxzdan98+Sy4oLOrv/mBZ/tllv958qG9vsu943AAAAAFgLTnGH6RLiM255/8JJWxV76JJkSIZhSJJOH7ig6W9uVvdRze9onwAAAABgbSjQTTZp0iS99957iouLU2hoqCZOnKhmzZrl2Xfy5MkaOXJkrjZHR0ddvXq1OKIWmeU/nrvl/TErzubZvnXhWaWknymKSAAAAABQ7CjQTfTTTz/p2Wef1eeff67mzZvr448/VmRkpA4dOiRfX988t3Fzc9OhQ4dyfrZYLMUVt8h0HuorTz+Hm95fzvGsftl/7Ib25t0D1H1U5Ty3SYjPuG3hDwAAAADWhALdRB9++KEeffTRnFHxzz//XAsXLtQ333yjMWPG5LmNxWKRv79/ccYscp5+DvINdLrp/YNfjtD2BQd0+sCFnLbAOj4a/HKEnMvfvLAHAAAAgJKESeJMkpGRoZ07d6pTp045bTY2NurUqZM2b9580+2Sk5NVtWpVBQYGqnfv3tq3b98tHyc9PV1JSUm5btainJudwiM9Vc7t1t8TZWfZaMys+9XtiQgF1K2mbk9EaMys+5WddfPDN7/7BgAAAABrQYFukgsXLigrK0t+fn652v38/BQXF5fnNiEhIfrmm280d+5cTZkyRdnZ2WrZsqXOnLn5ddgTJkyQu7t7zi0wMLBQn8fdKOdup+ZdvVXO/dZFdMzmRM374pyy7auqfqdmyravqnlfnFPM5sS73jcAAAAAWAuqlxIkIiJCEREROT+3bNlSderU0RdffKE33ngjz23Gjh2rZ599NufnpKQkqyrS86N+hLuC65W7oZ3RcQAAAAClCRWOSXx8fGRra6v4+Phc7fHx8fm+xtze3l5hYWE6cuTITfs4OjrK0dHxrrKarZy7HSPhAAAAAEo9TnE3iYODg5o0aaKVK1fmtGVnZ2vlypW5RslvJSsrS3v37lXFihWLKiYAAAAAoJgwLGmiZ599VsOHD1fTpk3VrFkzffzxx0pJScmZ1X3YsGEKCAjQhAkTJEmvv/66WrRooRo1aujy5ct67733dPLkST3yyCNmPg0AAAAAQCGgQDfRoEGDdP78ef373/9WXFycGjVqpCVLluRMHHfq1CnZ2Pz/SQ4JCQl69NFHFRcXJ09PTzVp0kSbNm1S3bp1zXoKAAAAAIBCYjEMwzA7BIpPUlKS3N3dlZiYKDc3N7PjAAAAADAJtYH14Rp0AAAAAACsAAU6AAAAAABWgAIdAAAAAAArQIEOAAAAAIAVoEAHAAAAAMAKUKADAAAAAGAFKNABAAAAALACFOgAAAAAAFgBCnQAAAAAAKyAndkBULwMw5AkJSUlmZwEAAAAgJmu1wTXawSYjwK9jLly5YokKTAw0OQkAAAAAKzBlStX5O7ubnYMSLIYfF1SpmRnZ+u3336Tq6urLBaL2XGsSlJSkgIDA3X69Gm5ubmZHQdWjGMF+cWxgvzgOEF+cawgPwpynBiGoStXrqhSpUqyseHqZ2vACHoZY2Njo8qVK5sdw6q5ubnxjx7yhWMF+cWxgvzgOEF+cawgP/J7nDBybl34mgQAAAAAACtAgQ4AAAAAgBWgQAf+4OjoqHHjxsnR0dHsKLByHCvIL44V5AfHCfKLYwX5wXFSsjFJHAAAAAAAVoARdAAAAAAArAAFOgAAAAAAVoACHQAAAAAAK0CBDgAAAACAFaBAR5l26dIlDR06VG5ubvLw8NDDDz+s5OTkW27Trl07WSyWXLfHH3+8mBKjuEyaNElBQUFycnJS8+bNtW3btlv2nzlzpmrXri0nJyc1aNBAixYtKqakMFtBjpXJkyff8PfDycmpGNPCDOvWrVPPnj1VqVIlWSwWzZkz57bbrFmzRo0bN5ajo6Nq1KihyZMnF3lOmKugx8maNWtu+HtisVgUFxdXPIFhmgkTJig8PFyurq7y9fVVnz59dOjQodtux2eVkoECHWXa0KFDtW/fPi1fvlwLFizQunXr9Nhjj912u0cffVSxsbE5t3fffbcY0qK4/PTTT3r22Wc1btw47dq1S6GhoYqMjNS5c+fy7L9p0yYNGTJEDz/8sHbv3q0+ffqoT58+iomJKebkKG4FPVYkyc3NLdffj5MnTxZjYpghJSVFoaGhmjRpUr76Hz9+XN27d1f79u0VFRWlZ555Ro888oiWLl1axElhpoIeJ9cdOnQo198UX1/fIkoIa7F27VqNGjVKW7Zs0fLly3Xt2jV16dJFKSkpN92GzyolB8usocw6cOCA6tatq+3bt6tp06aSpCVLlujee+/VmTNnVKlSpTy3a9eunRo1aqSPP/64GNOiODVv3lzh4eH65JNPJEnZ2dkKDAzUU089pTFjxtzQf9CgQUpJSdGCBQty2lq0aKFGjRrp888/L7bcKH4FPVYmT56sZ555RpcvXy7mpLAWFotFs2fPVp8+fW7a58UXX9TChQtzfXAePHiwLl++rCVLlhRDSpgtP8fJmjVr1L59eyUkJMjDw6PYssH6nD9/Xr6+vlq7dq3atGmTZx8+q5QcjKCjzNq8ebM8PDxyinNJ6tSpk2xsbLR169Zbbvvjjz/Kx8dH9evX19ixY5WamlrUcVFMMjIytHPnTnXq1CmnzcbGRp06ddLmzZvz3Gbz5s25+ktSZGTkTfujdLiTY0WSkpOTVbVqVQUGBqp3797at29fccRFCcLfFBREo0aNVLFiRXXu3FkbN240Ow5MkJiYKEny8vK6aR/+rpQcdmYHAMwSFxd3w2lgdnZ28vLyuuX1W/fff7+qVq2qSpUqac+ePXrxxRd16NAh/fLLL0UdGcXgwoULysrKkp+fX652Pz8/HTx4MM9t4uLi8uzPdYCl250cKyEhIfrmm2/UsGFDJSYm6v3331fLli21b98+Va5cuThiowS42d+UpKQkpaWlydnZ2aRksCYVK1bU559/rqZNmyo9PV1fffWV2rVrp61bt6px48Zmx0Mxyc7O1jPPPKN77rlH9evXv2k/PquUHBToKHXGjBmjd95555Z9Dhw4cMf7//M16g0aNFDFihXVsWNHHT16VNWrV7/j/QIo/SIiIhQREZHzc8uWLVWnTh198cUXeuONN0xMBqCkCQkJUUhISM7PLVu21NGjR/XRRx/phx9+MDEZitOoUaMUExOjDRs2mB0FhYQCHaXOc889pxEjRtyyT7Vq1eTv73/DRE6ZmZm6dOmS/P398/14zZs3lyQdOXKEAr0U8PHxka2treLj43O1x8fH3/S48Pf3L1B/lA53cqz8lb29vcLCwnTkyJGiiIgS6mZ/U9zc3Bg9xy01a9aMQq0MGT16dM4kx7c7C4vPKiUH16Cj1KlQoYJq1659y5uDg4MiIiJ0+fJl7dy5M2fbVatWKTs7O6fozo+oqChJv59qhpLPwcFBTZo00cqVK3PasrOztXLlylwjn38WERGRq78kLV++/Kb9UTrcybHyV1lZWdq7dy9/P5ALf1Nwp6Kiovh7UgYYhqHRo0dr9uzZWrVqlYKDg2+7DX9XShADKMO6du1qhIWFGVu3bjU2bNhg1KxZ0xgyZEjO/WfOnDFCQkKMrVu3GoZhGEeOHDFef/11Y8eOHcbx48eNuXPnGtWqVTPatGlj1lNAEZg+fbrh6OhoTJ482di/f7/x2GOPGR4eHkZcXJxhGIbx4IMPGmPGjMnpv3HjRsPOzs54//33jQMHDhjjxo0z7O3tjb1795r1FFBMCnqsvPbaa8bSpUuNo0ePGjt37jQGDx5sODk5Gfv27TPrKaAYXLlyxdi9e7exe/duQ5Lx4YcfGrt37zZOnjxpGIZhjBkzxnjwwQdz+h87dsxwcXExnn/+eePAgQPGpEmTDFtbW2PJkiVmPQUUg4IeJx999JExZ84c4/Dhw8bevXuNp59+2rCxsTFWrFhh1lNAMXniiScMd3d3Y82aNUZsbGzOLTU1NacPn1VKLgp0lGkXL140hgwZYpQvX95wc3MzRo4caVy5ciXn/uPHjxuSjNWrVxuGYRinTp0y2rRpY3h5eRmOjo5GjRo1jOeff95ITEw06RmgqEycONGoUqWK4eDgYDRr1szYsmVLzn1t27Y1hg8fnqv/jBkzjFq1ahkODg5GvXr1jIULFxZzYpilIMfKM888k9PXz8/PuPfee41du3aZkBrFafXq1YakG27Xj43hw4cbbdu2vWGbRo0aGQ4ODka1atWMb7/9tthzo3gV9Dh55513jOrVqxtOTk6Gl5eX0a5dO2PVqlXmhEexyus4kZTr7wSfVUou1kEHAAAAAMAKcA06AAAAAABWgAIdAAAAAAArQIEOAAAAAIAVoEAHAAAAAMAKUKADAAAAAGAFKNABAAAAALACFOgAAAAAAFgBCnQAAAAAAKwABToAAAAAAFaAAh0AgFKsXbt2slgsslgsioqKuqt9jRgxImdfc+bMKZR8AADg/1GgAwBQyj366KOKjY1V/fr172o///nPfxQbG1tIqQAAwF/ZmR0AAAAULRcXF/n7+9/1ftzd3eXu7l4IiQAAQF4YQQcAoASaNm2anJ2dc41ojxw5Ug0bNlRiYuJttz9x4oQsFot+/vlntWnTRs7OzgoPD9epU6e0fv16tWjRQi4uLurYsaMuX75chM8EAABcR4EOAEAJNHjwYNWqVUtvvfWWJGncuHFasWKFFi9enK9R7ujoaEnSZ599prfeekubNm1SfHy8HnjgAb399tv65JNPtHr1akVHR+vbb78t0ucCAAB+xynuAACUQBaLRePHj1f//v3l7++viRMnav369QoICMjX9lFRUfLy8tJPP/0kb29vSVLbtm21YcMG7du3Ty4uLpKk8PBwxcXFFdnzAAAA/48RdAAASqgePXqobt26ev311zV79mzVq1cv39tGR0erb9++OcW5JJ06dUqDBg3KKc6vtwUHBxdqbgAAkDcKdAAASqglS5bo4MGDysrKkp+fX4G2jYqKUvPmzXO1RUdHq0WLFjk/X716VYcOHVJoaGih5AUAALdGgQ4AQAm0a9cuDRw4UF9//bU6duyoV155Jd/bJiUl6cSJEwoLC8tpO378uBITE3O17d27V4ZhqEGDBoWaHQAA5I1r0AEAKGFOnDih7t2766WXXtKQIUNUrVo1RUREaNeuXWrcuPFtt4+OjpatrW2uddGvX5NetWrVXG3Vq1dX+fLli+R5AACA3BhBBwCgBLl06ZK6du2q3r17a8yYMZKk5s2bq1u3bnrppZfytY/o6GiFhITIyckpV9ufR8+vt3F6OwAAxcdiGIZhdggAAFA02rVrp0aNGunjjz8utH1aLBbNnj1bffr0KbR9AgAARtABACj1Pv30U5UvX1579+69q/08/vjjnO4OAEARYgQdAIBS7OzZs0pLS5MkValSRQ4ODne8r3PnzikpKUmSVLFiRZUrV65QMgIAgN9RoAMAAAAAYAU4xR0AAAAAACtAgQ4AAAAAgBWgQAcAAAAAwApQoAMAAAAAYAUo0AEAAAAAsAIU6AAAAAAAWAEKdADA/7VfxwIAAAAAg/ytp7GjLAIAYEDQAQAAYEDQAQAAYCAjPL54bPKKFgAAAABJRU5ErkJggg==' width=1000.0/>
</div>





<div style="display: inline-block;">
    <div class="jupyter-widgets widget-label" style="text-align: center;">
        Figure
    </div>
    <img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA+gAAAH0CAYAAACuKActAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguMywgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/H5lhTAAAACXBIWXMAAA9hAAAPYQGoP6dpAAA/p0lEQVR4nO3deZiXZb0/8PcMq9sMR7YBxD3ZRFGQxcwlMFxKSU00OyqRXpp6VPxZoqZlx8g6lpUL2aLHY6ZZ6lEzToqadiQ1EBQUKg8IYgMiMeOSiDPf3x9dTk2OiMjM9wFfr+t6Lq+5v/f93J97fJx6f5+tolQqlQIAAACUVWW5CwAAAAAEdAAAACgEAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdACg1bzyyiuprKzMt771rQ/U3ACwPgR0AD6wrr/++lRUVDRt7du3T58+fXLiiSdm6dKlrTbvI488ki9/+ctZtWpVq81RFHPnzk2pVMqgQYM+UHMDwPpoX+4CAKDcLrnkkuywww55/fXX87vf/S7XX399fvvb32bu3Lnp3LnzBp/vkUceyVe+8pWceOKJ6dKlywbff5E89dRTSZKBAwd+oOYGgPUhoAPwgXfwwQdn2LBhSZLPfe5z6datWy677LLceeedOfroo8tcXdt4/fXXW+XLiKeeeipVVVXp27fvBt93kecGgPXhEncA+Ccf+chHkiTPPvtss/alS5fms5/9bHr27JlOnTpl0KBB+fGPf9ysz8svv5yzzjor22+/fTp16pQePXrkwAMPzKxZs5IkX/7yl3PuuecmSXbYYYemy+sXLVqUJHniiSdy8MEHp6qqKltuuWVGjx6d3/3ud2+r8d3mWZsDDzwwe++9dx5++OHst99+2WyzzXLmmWe+59/TunjqqacyYMCAzJo1KwcffHC22mqr9OnTJ9/5zndaZb6izA0A68MZdAD4J2+F5X/5l39palu2bFlGjhyZioqKnH766enevXt+9atfZeLEiamvr89ZZ52VJDnllFPy85//PKeffnoGDhyYl156Kb/97W/zzDPPZM8998wRRxyRP/zhD/npT3+ab3/72+nWrVuSpHv37pk3b14+8pGPpKqqKl/4whfSoUOHfP/738/++++f3/zmNxkxYkRTPe82z9o8+eST6dKlS8aNG5eTTjopn/70p7Pzzjs367NmzZrU1dWt0+9r6623TmVly9/5P/XUU+nZs2c+/vGPZ8KECRk3blx+8IMf5Oyzz85HP/rRDB48eJ3mWB/lnBsA1ksJAD6grrvuulKS0n333Vd68cUXS0uWLCn9/Oc/L3Xv3r3UqVOn0pIlS5r6Tpw4sdSrV6/SihUrmu3jmGOOKVVXV5dee+21UqlUKlVXV5dOO+20tc77zW9+s5SktHDhwmbt48aNK3Xs2LH07LPPNrW98MILpa222qq07777Nuu7LvO0ZNmyZaUkpS233LL0zDPPvGO/Bx54oJRknbZ/Xsc/1p6k1K1bt9LixYub2p9++ulSktJ//ud/vuf611U55waA9eUMOgAfeGPGjGn28/bbb58bb7wx22yzTZKkVCrlF7/4RY4++uiUSqWsWLGiqe/YsWNz8803Z9asWfnwhz+cLl265NFHH80LL7yQ3r17r3MNDQ0N+fWvf51x48Zlxx13bGrv1atXPv3pT+cHP/hB6uvrU1VVlSTrPc+TTz6ZJDn//PPTv3//d+y3++675957712nfdbU1Kx1rksuuaTZfeAdOnRIknTs2LHFcY2NjXnjjTfWae5OnTqloqJig80NAOUkoAPwgXfVVVdll112SV1dXX784x/noYceSqdOnZo+f/HFF7Nq1apce+21ufbaa1vcx/Lly5Mk3/jGN3LCCSekb9++GTp0aA455JAcf/zxzUJ3S1588cW89tpr6dev39s+GzBgQBobG7NkyZKmV4at7zxvPdl8/Pjxa+33L//yL2/74uK9emuuT37yk83a58+fnyQtrjVJHnrooRxwwAHrNMczzzzT4hcN6zs3AJSTgA7AB97w4cObnuI+bty47LPPPvn0pz+dBQsWZMstt0xjY2OS5DOf+UxOOOGEFvex2267JUmOPvrofOQjH8ntt9+eX//61/nmN7+Zyy67LLfddlsOPvjgDVbz+s7z5JNPplevXu8a5N94442sXLlynWrp3r172rVr97b2p556Kn369HnbGfY5c+akffv27/j6s/79++e6665bp7l79erVYvv6zg0A5SSgA8A/aNeuXaZMmZIDDjggV155Zc4777x07949W221VRoaGtbprHKvXr3y+c9/Pp///OezfPny7Lnnnrn00kubgnNLl2R37949m2++eRYsWPC2z+bPn5/Kysq3vS7s3eZpyZNPPpndd9/9XdfwyCOPrPNZ7IULF2b77bd/W/tTTz3V9MXFP9ewyy67NLtK4R/V1NTkxBNPXKe538n6zg0A5SSgA8A/2X///TN8+PBcccUVOeuss9K5c+cceeSRuemmmzJ37tzsuuuuzfq/+OKL6d69exoaGvLKK6+kurq66bMePXqkd+/eWb16dVPbFltskSRZtWpVU1u7du3ysY99LP/93/+dRYsWNQXeZcuW5aabbso+++zTdP/5us7zzxoaGvL000/nwAMPfNffwfu9B72hoSHPPPNMxo4d+7bP5syZkz322GOd9r0+yjk3ALwfAjoAtODcc8/Npz71qVx//fU55ZRT8vWvfz0PPPBARowYkZNOOikDBw7MypUrM2vWrNx3331ZuXJlXn755WyzzTY56qijsvvuu2fLLbfMfffdl8cffzyXX355076HDh2aJLngggtyzDHHpEOHDvnEJz6Rf//3f8+9996bffbZJ5///OfTvn37fP/738/q1avzjW98o2n8us7zz/74xz/m9ddfX6cz6O/3HvS35vrns9h//etf86c//ekdbxXYEMo5NwC8HwI6ALTgiCOOyE477ZT/+I//yEknnZSePXvmscceyyWXXJLbbrstV199dbp27ZpBgwblsssuS5Jsvvnm+fznP59f//rXue2229LY2Jidd945V199dU499dSmfe+111756le/mqlTp2batGlpbGzMwoULM2jQoDz88MOZPHlypkyZksbGxowYMSI33nhjs3egr+s8/+ytB6e1dOn3hvZOc82dOzcNDQ2tWkM55waA96OiVCqVyl0EAAAAfNBVlrsAAAAAQEAHAACAQhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAvAe9A+YxsbGvPDCC9lqq61SUVFR7nIAAIAyKZVKefnll9O7d+9UVjp3WwQC+gfMCy+8kL59+5a7DAAAoCCWLFmSbbbZptxlEAH9A2errbZK8rf/CKuqqspcDQAAUC719fXp27dvU0ag/AT0D5i3LmuvqqoS0AEAALe+FogbDQAAAKAABHQAAAAoAAEdAAAACsA96AAAQGE1NDRkzZo15S5jo9ShQ4e0a9eu3GXwHgjoAABA4ZRKpdTW1mbVqlXlLmWj1qVLl9TU1HgQ3EZCQAcAAArnrXDeo0ePbL755gLme1QqlfLaa69l+fLlSZJevXqVuSLWhYAOAAAUSkNDQ1M479q1a7nL2WhtttlmSZLly5enR48eLnffCHhIHAAAUChv3XO++eabl7mSjd9bv0P38W8cBHQAAKCQXNb+/vkdblwEdAAAACgAAR0AAAAKQEAHAACAAhDQAdjgGhoay10CAJTVSy+9lB49emTRokWtNscxxxyTyy+/vNX2T9sT0AHYYJ5fsCKnDromh7e/NKcOuibPL1hR7pIAoCwuvfTSHH744dl+++1bbY4LL7wwl156aerq6lptDtqWgN6Krrrqqmy//fbp3LlzRowYkccee2yt/W+99db0798/nTt3zuDBg3PPPfe8rc8zzzyTww47LNXV1dliiy2y1157ZfHixa21BID35NIjbs3SBS8lSZYueCmXHnFrmSsCgLb32muv5Uc/+lEmTpzYanO8+eab2XXXXbPTTjvlxhtvbLV5aFsCeiu55ZZbMmnSpFx88cWZNWtWdt9994wdOzbLly9vsf8jjzySY489NhMnTswTTzyRcePGZdy4cZk7d25Tn2effTb77LNP+vfvnwcffDBPPvlkvvSlL6Vz585ttSyAd9TQ0JglT69IY0MpSdLYUMqSp1e43B2AD5x77rknnTp1ysiRI5vafvrTn2azzTbLn//856a2CRMmZLfddnvXM+CLFi1KRUVFfvazn+UjH/lIOnXqlDvvvDNJ8olPfCI333xz6yyENldRKpVK5S5iUzRixIjstddeufLKK5MkjY2N6du3b84444ycd955b+s/fvz4vPrqq7n77rub2kaOHJkhQ4Zk6tSpSf52j0mHDh3yX//1X+tdV319faqrq1NXV5eqqqr13g9AS04ddE2WLngpjQ2lVLarSJ9+XXPNvFPLXRYAG5nXX389CxcuzA477LDBTkY1NDSmXbu2OT955pln5g9/+EN+9atfNbWVSqUMGTIk++67b773ve/l4osvzo9//OP87ne/S58+fda6v//+7//OuHHjMmzYsHzta1/LDjvskO7du6e6ujrTpk3L4Ycfnvr6+nTq1OltY9f2u5QNiscZ9FbwxhtvZObMmRkzZkxTW2VlZcaMGZMZM2a0OGbGjBnN+ifJ2LFjm/o3Njbml7/8ZXbZZZeMHTs2PXr0yIgRI3LHHXestZbVq1envr6+2QbQWi647VPp069rkqRPv6654LZPlbkiAD7oyvF8lOeeey69e/du1lZRUZFLL700P/jBD3LppZfme9/7XqZNm/au4TxJZs+enS222CK33nprDjzwwOy8886prq5OkvTu3TtvvPFGamtrW2UttC0BvRWsWLEiDQ0N6dmzZ7P2nj17vuN/OLW1tWvtv3z58rzyyiv5+te/noMOOii//vWv88lPfjJHHHFEfvOb37xjLVOmTEl1dXXT1rdv3/e5OoB3tk2/brlm3qn57zcvyDXzTs02/bqVuyQAPuDK8XyUv/71ry2e+f/4xz+egQMH5pJLLsntt9+eQYMGrdP+5syZk8MOO6zFB85tttlmSf523zsbPwF9I9HY+Ld7OA8//PCcffbZGTJkSM4777x8/OMfb7oEviWTJ09OXV1d07ZkyZK2Khn4AGurSwgBYG3K9XyUbt265S9/+cvb2qdNm5b58+e3eDJvbWbPnp3999+/xc9WrlyZJOnevft61Uqx+H9QraBbt25p165dli1b1qx92bJlqampaXFMTU3NWvt369Yt7du3z8CBA5v1GTBgwFqf4t6pU6dUVVU12wAA4IOgXbvK9B3YLZXtKpIkle0q0ndgt1b/InmPPfbI008/3axt1qxZOfroo/OjH/0oo0ePzpe+9KV12ld9fX0WLVqUPfbYo8XP586dm2222SbdurlqbVMgoLeCjh07ZujQoZk+fXpTW2NjY6ZPn55Ro0a1OGbUqFHN+ifJvffe29S/Y8eO2WuvvbJgwYJmff7whz9ku+2228ArAACATUM5no8yduzYzJs3r+ks+qJFi3LooYfm/PPPz7HHHptLLrkkv/jFLzJr1qx33decOXPSrl27DB48uMXPH3744XzsYx/boPVTPu3LXcCmatKkSTnhhBMybNiwDB8+PFdccUVeffXVTJgwIUly/PHHp0+fPpkyZUqSvz3pcb/99svll1+eQw89NDfffHN+//vf59prr23a57nnnpvx48dn3333zQEHHJBp06blrrvuyoMPPliOJQIAQOG99XyUtnyK++DBg7PnnnvmZz/7WT71qU/loIMOyuGHH970NqcRI0bk4IMPzvnnn59p06YlSa6//vpMmDAh//ySrTlz5qRfv34t3tP++uuv54477mjaBxs/Ab2VjB8/Pi+++GIuuuii1NbWZsiQIZk2bVrTvSaLFy9OZeXf/0Dsvffeuemmm3LhhRfm/PPPz4c+9KHccccd2XXXXZv6fPKTn8zUqVMzZcqU/Nu//Vv69euXX/ziF9lnn33afH0AALAxaevno1x00UU599xzc9JJJ2X+/Plv+/yXv/xls58XLlyY/fbb7239Tj/99Jx++uktznHddddl+PDhzd63zsbNe9A/YLzrEACAomuN96CXwxVXXJEjjzxynd6kNHz48Fx55ZUZPnz4Ou//hz/8YT7ykY+kX79+79jHe9A3Ls6gAwAAtIKzzjprnfs+9thj73n/n/vc597zGIrNQ+IAAACgAAR0AAAAKAABHQAAAApAQAcAAArJ86zfP7/DjYuADgAAFEqHDh2SJK+99lqZK9n4vfU7fOt3SrF5ijsAAFAo7dq1S5cuXbJ8+fIkyeabb56KiooyV7VxKZVKee2117J8+fJ06dIl7dq1K3dJrAMBHQAAKJyampokaQrprJ8uXbo0/S4pPgEdAAAonIqKivTq1Ss9evTImjVryl3ORqlDhw7OnG9kBHQAAKCw2rVrJ2TygeEhcQAAAFAAAjoAAAAUgIAOAAAABSCgAwAAQAEI6AAAAFAAAjoAAAAUgIAOAAAABSCgAwAAQAEI6AAAAFAAAjoAAAAUgIAOAAAABSCgAwAAQAEI6AAAAFAAAjoAAAAUgIAOAAAABSCgAwAAQAEI6AAAAFAAAjoAAAAUgIAOAAAABSCgAwAAQAEI6AAAAFAAAjoAAAAUgIAOAAAABSCgAwAAQAEI6AAAAFAAAjoAAAAUgIAOAAAABSCgAwAAQAEI6AAAAFAAAjoAAAAUgIAOAAAABSCgAwAAQAEI6AAAAFAAAjoAAAAUgIAOAAAABSCgAwAAQAEI6K3sqquuyvbbb5/OnTtnxIgReeyxx9ba/9Zbb03//v3TuXPnDB48OPfcc8879j3llFNSUVGRK664YgNXDQAAQFsT0FvRLbfckkmTJuXiiy/OrFmzsvvuu2fs2LFZvnx5i/0feeSRHHvssZk4cWKeeOKJjBs3LuPGjcvcuXPf1vf222/P7373u/Tu3bu1lwEAAEAbENBb0be+9a2cdNJJmTBhQgYOHJipU6dm8803z49//OMW+3/nO9/JQQcdlHPPPTcDBgzIV7/61ey555658sorm/VbunRpzjjjjPzkJz9Jhw4d2mIpAAAAtDIBvZW88cYbmTlzZsaMGdPUVllZmTFjxmTGjBktjpkxY0az/kkyduzYZv0bGxvzr//6rzn33HMzaNCg1ikeAACANte+3AVsqlasWJGGhob07NmzWXvPnj0zf/78FsfU1ta22L+2trbp58suuyzt27fPv/3bv61THatXr87q1aubfq6vr1/XJQAAANCGnEHfiMycOTPf+c53cv3116eiomKdxkyZMiXV1dVNW9++fVu5SgAAANaHgN5KunXrlnbt2mXZsmXN2pctW5aampoWx9TU1Ky1/8MPP5zly5dn2223Tfv27dO+ffs899xzOeecc7L99tu3uM/Jkyenrq6uaVuyZMn7XxwAAAAbnIDeSjp27JihQ4dm+vTpTW2NjY2ZPn16Ro0a1eKYUaNGNeufJPfee29T/3/913/Nk08+mdmzZzdtvXv3zrnnnpv/+Z//aXGfnTp1SlVVVbMNAACA4nEPeiuaNGlSTjjhhAwbNizDhw/PFVdckVdffTUTJkxIkhx//PHp06dPpkyZkiQ588wzs99+++Xyyy/PoYcemptvvjm///3vc+211yZJunbtmq5duzabo0OHDqmpqUm/fv3adnEAAABsUAJ6Kxo/fnxefPHFXHTRRamtrc2QIUMybdq0pgfBLV68OJWVf7+IYe+9985NN92UCy+8MOeff34+9KEP5Y477siuu+5ariUAAADQRipKpVKp3EXQdurr61NdXZ26ujqXuwMAwAeYbFA87kEHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAEdAAAACgAAR0AAAAKQEAHAACAAhDQAQAAoAAE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AAAAoA1ssgF97ty5ufPOO3PDDTfkwQcfzF/+8pc8++yzufbaa/PhD3+4TWq45ZZbMmnSpFx88cWZNWtWdt9994wdOzbLly9vsf8jjzySY489NhMnTswTTzyRcePGZdy4cZk7d25Tn2984xv57ne/m6lTp+bRRx/NFltskbFjx+b1119vkzUBAADQOipKpVKp3EW0hv322y9TpkzJ3nvvXbYaRowYkb322itXXnllkqSxsTF9+/bNGWeckfPOO+9t/cePH59XX301d999d1PbyJEjM2TIkEydOjWlUim9e/fOOeeck//3//5fkqSuri49e/bM9ddfn2OOOeZda6qvr091dXXq6upSVVW1gVYKAABsbGSD4tlkz6CfeeaZ+fKXv5xVq1aVZf433ngjM2fOzJgxY5raKisrM2bMmMyYMaPFMTNmzGjWP0nGjh3b1H/hwoWpra1t1qe6ujojRox4x30CAACwcdhkHxJ31FFHJUk+9KEP5ZOf/GRGjBiRPfbYI7vuums6duzY6vOvWLEiDQ0N6dmzZ7P2nj17Zv78+S2Oqa2tbbF/bW1t0+dvtb1Tn3+2evXqZk+yr6+vf28LAQAAoE1ssgF94cKFmTNnTmbPnp05c+bka1/7WhYtWpT27dunX79+efLJJ8tdYpuYMmVKvvKVr5S7DAAAAN7FJhvQt9tuu2y33XY57LDDmtpefvnlzJ49u03Cebdu3dKuXbssW7asWfuyZctSU1PT4piampq19n/rn8uWLUuvXr2a9RkyZEiL+5w8eXImTZrU9HN9fb1XzQEAABTQJnsPeku22mqrfOQjH8lpp53W6nN17NgxQ4cOzfTp05vaGhsbM3369IwaNarFMaNGjWrWP0nuvffepv477LBDampqmvWpr6/Po48++o777NSpU6qqqpptAAAAFM8mFdCffPLJNDY2rnP/efPm5c0332y1eiZNmpQf/OAH+c///M8888wzOfXUU/Pqq69mwoQJSZLjjz8+kydPbup/5plnZtq0abn88sszf/78fPnLX87vf//7nH766UmSioqKnHXWWfn3f//33HnnnXnqqady/PHHp3fv3hk3blyrrQMAAIDWt0ld4r7HHnuktrY23bt3X6f+o0aNyuzZs7Pjjju2Sj3jx4/Piy++mIsuuii1tbUZMmRIpk2b1vSQt8WLF6ey8u/fkey999656aabcuGFF+b888/Phz70odxxxx3Zddddm/p84QtfyKuvvpqTTz45q1atyj777JNp06alc+fOrbIGAAAA2sYm9R70ysrKnHzyydl8883Xqf/VV1+dp59+utUCehF51yEAAJDIBkW0SZ1B33fffbNgwYJ17j9q1KhsttlmrVgRAAAArJtNKqA/+OCD5S4BAAAA1ssm9ZC4tzQ0NOSOO+7Iyy+/XO5SAAAAYJ1skgG9Xbt2OfbYY/Piiy+WuxQAAABYJ5tkQE+SvfbaKwsXLix3GQAAALBONtmAfsYZZ+T888/PkiVLyl0KAAAAvKtN6iFx/2j8+PFJkkGDBuWwww7L/vvvnz322CODBw9Ox44dy1wdAAAANLfJBvSFCxdmzpw5mT17dubMmZMpU6Zk0aJFad++ffr165cnn3yy3CUCAABAk002oG+33XbZbrvtcthhhzW1vfzyy5k9e7ZwDgAAQOFUlEqlUrmLoO3U19enuro6dXV1qaqqKnc5AABAmcgGxbPJPiQOAAAANiYCOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOmXV0NBY7hIAAAAKQUCnLJ5fsCKnDromh7e/NKcOuibPL1hR7pIAAADKSkCnLC494tYsXfBSkmTpgpdy6RG3lrkiAACA8hLQaXMNDY1Z8vSKNDaUkiSNDaUseXqFy90BAIAPNAG9FaxcuTLHHXdcqqqq0qVLl0ycODGvvPLKWse8/vrrOe2009K1a9dsueWWOfLII7Ns2bKmz+fMmZNjjz02ffv2zWabbZYBAwbkO9/5TmsvpVW0a1eZvgO7pbJdRZKksl1F+g7slnbtHI4AAMAHl0TUCo477rjMmzcv9957b+6+++489NBDOfnkk9c65uyzz85dd92VW2+9Nb/5zW/ywgsv5Igjjmj6fObMmenRo0duvPHGzJs3LxdccEEmT56cK6+8srWX0youuO1T6dOva5KkT7+uueC2T5W5IgAAgPKqKJVKpXIXsSl55plnMnDgwDz++OMZNmxYkmTatGk55JBD8vzzz6d3795vG1NXV5fu3bvnpptuylFHHZUkmT9/fgYMGJAZM2Zk5MiRLc512mmn5Zlnnsn999+/zvXV19enuro6dXV1qaqqWo8VblgNDY3OnAMAQBkULRvgDPoGN2PGjHTp0qUpnCfJmDFjUllZmUcffbTFMTNnzsyaNWsyZsyYprb+/ftn2223zYwZM95xrrq6umy99dZrrWf16tWpr69vthWJcA4AAPA30tEGVltbmx49ejRra9++fbbeeuvU1ta+45iOHTumS5cuzdp79uz5jmMeeeSR3HLLLe966fyUKVNSXV3dtPXt23fdFwMAAECbEdDX0XnnnZeKioq1bvPnz2+TWubOnZvDDz88F198cT72sY+tte/kyZNTV1fXtC1ZsqRNagQAAOC9aV/uAjYW55xzTk488cS19tlxxx1TU1OT5cuXN2t/8803s3LlytTU1LQ4rqamJm+88UZWrVrV7Cz6smXL3jbm6aefzujRo3PyySfnwgsvfNe6O3XqlE6dOr1rPwAAAMpLQF9H3bt3T/fu3d+136hRo7Jq1arMnDkzQ4cOTZLcf//9aWxszIgRI1ocM3To0HTo0CHTp0/PkUcemSRZsGBBFi9enFGjRjX1mzdvXj760Y/mhBNOyKWXXroBVgUAAEBReIp7Kzj44IOzbNmyTJ06NWvWrMmECRMybNiw3HTTTUmSpUuXZvTo0bnhhhsyfPjwJMmpp56ae+65J9dff32qqqpyxhlnJPnbvebJ3y5r/+hHP5qxY8fmm9/8ZtNc7dq1W6cvDt7iSY0AAEAiGxSRM+it4Cc/+UlOP/30jB49OpWVlTnyyCPz3e9+t+nzNWvWZMGCBXnttdea2r797W839V29enXGjh2bq6++uunzn//853nxxRdz44035sYbb2xq32677bJo0aI2WRcAAACtxxn0DxjfkgEAAIlsUESe4g4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjorWDlypU57rjjUlVVlS5dumTixIl55ZVX1jrm9ddfz2mnnZauXbtmyy23zJFHHplly5a12Pell17KNttsk4qKiqxataoVVgAAAEBbE9BbwXHHHZd58+bl3nvvzd13352HHnooJ5988lrHnH322bnrrrty66235je/+U1eeOGFHHHEES32nThxYnbbbbfWKB0AAIAyqSiVSqVyF7EpeeaZZzJw4MA8/vjjGTZsWJJk2rRpOeSQQ/L888+nd+/ebxtTV1eX7t2756abbspRRx2VJJk/f34GDBiQGTNmZOTIkU19r7nmmtxyyy256KKLMnr06PzlL39Jly5d1rm++vr6VFdXp66uLlVVVe9vsQAAwEZLNigeZ9A3sBkzZqRLly5N4TxJxowZk8rKyjz66KMtjpk5c2bWrFmTMWPGNLX1798/2267bWbMmNHU9vTTT+eSSy7JDTfckMpK/+oAAAA2Je3LXcCmpra2Nj169GjW1r59+2y99dapra19xzEdO3Z825nwnj17No1ZvXp1jj322Hzzm9/Mtttum//7v/9bp3pWr16d1atXN/1cX1//HlYDAABAW3Eadh2dd955qaioWOs2f/78Vpt/8uTJGTBgQD7zmc+8p3FTpkxJdXV109a3b99WqhAAAID3wxn0dXTOOefkxBNPXGufHXfcMTU1NVm+fHmz9jfffDMrV65MTU1Ni+NqamryxhtvZNWqVc3Ooi9btqxpzP3335+nnnoqP//5z5Mkbz06oFu3brngggvyla98pcV9T548OZMmTWr6ub6+XkgHAAAoIAF9HXXv3j3du3d/136jRo3KqlWrMnPmzAwdOjTJ38J1Y2NjRowY0eKYoUOHpkOHDpk+fXqOPPLIJMmCBQuyePHijBo1Kknyi1/8In/961+bxjz++OP57Gc/m4cffjg77bTTO9bTqVOndOrUaZ3XCQAAQHkI6BvYgAEDctBBB+Wkk07K1KlTs2bNmpx++uk55phjmp7gvnTp0owePTo33HBDhg8fnurq6kycODGTJk3K1ltvnaqqqpxxxhkZNWpU0xPc/zmEr1ixomm+9/IUdwAAAIpJQG8FP/nJT3L66adn9OjRqayszJFHHpnvfve7TZ+vWbMmCxYsyGuvvdbU9u1vf7up7+rVqzN27NhcffXV5SgfAACAMvAe9A8Y7zoEAAAS2aCIPMUdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAEdAAAACkBABwAAgAIQ0AEAAKAABPRWsHLlyhx33HGpqqpKly5dMnHixLzyyitrHfP666/ntNNOS9euXbPlllvmyCOPzLJly97W7/rrr89uu+2Wzp07p0ePHjnttNNaaxkAAAC0IQG9FRx33HGZN29e7r333tx999156KGHcvLJJ691zNlnn5277rort956a37zm9/khRdeyBFHHNGsz7e+9a1ccMEFOe+88zJv3rzcd999GTt2bGsuBQAAgDZSUSqVSuUuYlPyzDPPZODAgXn88cczbNiwJMm0adNyyCGH5Pnnn0/v3r3fNqauri7du3fPTTfdlKOOOipJMn/+/AwYMCAzZszIyJEj85e//CV9+vTJXXfdldGjR693ffX19amurk5dXV2qqqrWez8AAMDGTTYoHmfQN7AZM2akS5cuTeE8ScaMGZPKyso8+uijLY6ZOXNm1qxZkzFjxjS19e/fP9tuu21mzJiRJLn33nvT2NiYpUuXZsCAAdlmm21y9NFHZ8mSJWutZ/Xq1amvr2+2AQDF0NDQWO4SACgQAX0Dq62tTY8ePZq1tW/fPltvvXVqa2vfcUzHjh3TpUuXZu09e/ZsGvN///d/aWxszNe+9rVcccUV+fnPf56VK1fmwAMPzBtvvPGO9UyZMiXV1dVNW9++fd/fAgGA9+35BSty6qBrcnj7S3PqoGvy/IIV5S4JgAIQ0NfReeedl4qKirVu8+fPb7X5Gxsbs2bNmnz3u9/N2LFjM3LkyPz0pz/NH//4xzzwwAPvOG7y5Mmpq6tr2t7tjDsA0PouPeLWLF3wUpJk6YKXcukRt5a5IgCKoH25C9hYnHPOOTnxxBPX2mfHHXdMTU1Nli9f3qz9zTffzMqVK1NTU9PiuJqamrzxxhtZtWpVs7Poy5YtaxrTq1evJMnAgQObPu/evXu6deuWxYsXv2NNnTp1SqdOndZaNwDQdhoaGrPk6b+fMW9sKGXJ0yvS0NCYdu2cOwH4IBPQ11H37t3TvXv3d+03atSorFq1KjNnzszQoUOTJPfff38aGxszYsSIFscMHTo0HTp0yPTp03PkkUcmSRYsWJDFixdn1KhRSZIPf/jDTe3bbLNNkr+9zm3FihXZbrvt3vf6AIC20a5dZfoO7JalC15KY0Mple0q0qdfV+EcAJe4b2gDBgzIQQcdlJNOOimPPfZY/vd//zenn356jjnmmKYnuC9dujT9+/fPY489liSprq7OxIkTM2nSpDzwwAOZOXNmJkyYkFGjRmXkyJFJkl122SWHH354zjzzzDzyyCOZO3duTjjhhPTv3z8HHHBA2dYLALx3F9z2qfTp1zVJ0qdf11xw26fKXBEAReAMeiv4yU9+ktNPPz2jR49OZWVljjzyyHz3u99t+nzNmjVZsGBBXnvttaa2b3/72019V69enbFjx+bqq69utt8bbrghZ599dg499NBUVlZmv/32y7Rp09KhQ4c2WxsA8P5t069brpl3qsvaAWjGe9A/YLzrEAAASGSDIvKVLQAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAbQvdwG0rVKplCSpr68vcyUAAEA5vZUJ3soIlJ+A/gHz8ssvJ0n69u1b5koAAIAiePnll1NdXV3uMkhSUfJ1yQdKY2NjXnjhhWy11VapqKgodzltor6+Pn379s2SJUtSVVVV7nLYiDh2WF+OHd4Pxw/ry7HDe1UqlfLyyy+nd+/eqax093MROIP+AVNZWZltttmm3GWURVVVlf+xYr04dlhfjh3eD8cP68uxw3vhzHmx+JoEAAAACkBABwAAgAIQ0NnkderUKRdffHE6depU7lLYyDh2WF+OHd4Pxw/ry7EDGz8PiQMAAIACcAYdAAAACkBABwAAgAIQ0AEAAKAABHQAAAAoAAGdTdLKlStz3HHHpaqqKl26dMnEiRPzyiuvrHXM/vvvn4qKimbbKaec0kYVUy5XXXVVtt9++3Tu3DkjRozIY489ttb+t956a/r375/OnTtn8ODBueeee9qoUormvRw7119//dv+vnTu3LkNq6UoHnrooXziE59I7969U1FRkTvuuONdxzz44IPZc88906lTp+y88865/vrrW71Oiue9HjsPPvjg2/7uVFRUpLa2tm0KBtaLgM4m6bjjjsu8efNy77335u67785DDz2Uk08++V3HnXTSSfnzn//ctH3jG99og2opl1tuuSWTJk3KxRdfnFmzZmX33XfP2LFjs3z58hb7P/LIIzn22GMzceLEPPHEExk3blzGjRuXuXPntnHllNt7PXaSpKqqqtnfl+eee64NK6YoXn311ey+++656qqr1qn/woULc+ihh+aAAw7I7Nmzc9ZZZ+Vzn/tc/ud//qeVK6Vo3uux85YFCxY0+9vTo0ePVqoQ2BC8Zo1NzjPPPJOBAwfm8ccfz7Bhw5Ik06ZNyyGHHJLnn38+vXv3bnHc/vvvnyFDhuSKK65ow2oppxEjRmSvvfbKlVdemSRpbGxM3759c8YZZ+S88857W//x48fn1Vdfzd13393UNnLkyAwZMiRTp05ts7opv/d67Fx//fU566yzsmrVqjaulCKrqKjI7bffnnHjxr1jny9+8Yv55S9/2eyLwGOOOSarVq3KtGnT2qBKimhdjp0HH3wwBxxwQP7yl7+kS5cubVYb8P44g84mZ8aMGenSpUtTOE+SMWPGpLKyMo8++uhax/7kJz9Jt27dsuuuu2by5Ml57bXXWrtcyuSNN97IzJkzM2bMmKa2ysrKjBkzJjNmzGhxzIwZM5r1T5KxY8e+Y382Tetz7CTJK6+8ku222y59+/bN4Ycfnnnz5rVFuWzk/N3h/RoyZEh69eqVAw88MP/7v/9b7nKAd9G+3AXAhlZbW/u2y7fat2+frbfeeq33XX3605/Odtttl969e+fJJ5/MF7/4xSxYsCC33XZba5dMGaxYsSINDQ3p2bNns/aePXtm/vz5LY6pra1tsb/7+T5Y1ufY6devX3784x9nt912S11dXf7jP/4je++9d+bNm5dtttmmLcpmI/VOf3fq6+vz17/+NZtttlmZKqPoevXqlalTp2bYsGFZvXp1fvjDH2b//ffPo48+mj333LPc5QHvQEBno3HeeeflsssuW2ufZ555Zr33/4/3qA8ePDi9evXK6NGj8+yzz2annXZa7/0CjBo1KqNGjWr6ee+9986AAQPy/e9/P1/96lfLWBmwqerXr1/69evX9PPee++dZ599Nt/+9rfzX//1X2WsDFgbAZ2NxjnnnJMTTzxxrX123HHH1NTUvO1BTW+++WZWrlyZmpqadZ5vxIgRSZI//elPAvomqFu3bmnXrl2WLVvWrH3ZsmXveJzU1NS8p/5smtbn2PlnHTp0yB577JE//elPrVEim5B3+rtTVVXl7Dnv2fDhw/Pb3/623GUAa+EedDYa3bt3T//+/de6dezYMaNGjcqqVasyc+bMprH3339/Ghsbm0L3upg9e3aSv10ixqanY8eOGTp0aKZPn97U1tjYmOnTpzc70/mPRo0a1ax/ktx7773v2J9N0/ocO/+soaEhTz31lL8vvCt/d9iQZs+e7e8OFJwz6GxyBgwYkIMOOignnXRSpk6dmjVr1uT000/PMccc0/QE96VLl2b06NG54YYbMnz48Dz77LO56aabcsghh6Rr16558sknc/bZZ2fffffNbrvtVuYV0VomTZqUE044IcOGDcvw4cNzxRVX5NVXX82ECROSJMcff3z69OmTKVOmJEnOPPPM7Lfffrn88stz6KGH5uabb87vf//7XHvtteVcBmXwXo+dSy65JCNHjszOO++cVatW5Zvf/Gaee+65fO5znyvnMiiDV155pdmVEwsXLszs2bOz9dZbZ9ttt83kyZOzdOnS3HDDDUmSU045JVdeeWW+8IUv5LOf/Wzuv//+/OxnP8svf/nLci2BMnmvx84VV1yRHXbYIYMGDcrrr7+eH/7wh7n//vvz61//ulxLANZFCTZBL730UunYY48tbbnllqWqqqrShAkTSi+//HLT5wsXLiwlKT3wwAOlUqlUWrx4cWnfffctbb311qVOnTqVdt5559K5555bqqurK9MKaCvf+973Sttuu22pY8eOpeHDh5d+97vfNX223377lU444YRm/X/2s5+Vdtlll1LHjh1LgwYNKv3yl79s44opivdy7Jx11llNfXv27Fk65JBDSrNmzSpD1ZTbAw88UErytu2t4+WEE04o7bfffm8bM2TIkFLHjh1LO+64Y+m6665r87opv/d67Fx22WWlnXbaqdS5c+fS1ltvXdp///1L999/f3mKB9aZ96ADAABAAbgHHQAAAApAQAcAAIACENABAACgAAR0AAAAKAABHQAAAApAQAcAAIACENABAACgAAR0AAAAKAABHQAAAApAQAeATdj++++fioqKVFRUZPbs2e9rXyeeeGLTvu64444NUh8A8HcCOgBs4k466aT8+c9/zq677vq+9vOd73wnf/7znzdQVQDAP2tf7gIAgNa1+eabp6am5n3vp7q6OtXV1RugIgCgJc6gA8BG6Kc//Wk222yzZme0J0yYkN122y11dXXvOn7RokWpqKjIL37xi+y7777ZbLPNstdee2Xx4sV5+OGHM3LkyGy++eYZPXp0Vq1a1YorAQDeIqADwEbomGOOyS677JKvfe1rSZKLL7449913X371q1+t01nuOXPmJEmuueaafO1rX8sjjzySZcuW5TOf+Uy+/vWv58orr8wDDzyQOXPm5LrrrmvVtQAAf+MSdwDYCFVUVOTSSy/NUUcdlZqamnzve9/Lww8/nD59+qzT+NmzZ2frrbfOLbfckq5duyZJ9ttvv/z2t7/NvHnzsvnmmydJ9tprr9TW1rbaOgCAv3MGHQA2Uh//+MczcODAXHLJJbn99tszaNCgdR47Z86cfPKTn2wK50myePHijB8/vimcv9W2ww47bNC6AYCWCegAsJGaNm1a5s+fn4aGhvTs2fM9jZ09e3ZGjBjRrG3OnDkZOXJk08+vv/56FixYkN13332D1AsArJ2ADgAboVmzZuXoo4/Oj370o4wePTpf+tKX1nlsfX19Fi1alD322KOpbeHChamrq2vW9tRTT6VUKmXw4MEbtHYAoGXuQQeAjcyiRYty6KGH5vzzz8+xxx6bHXfcMaNGjcqsWbOy5557vuv4OXPmpF27ds3ei/7WPenbbbdds7addtopW265ZausAwBozhl0ANiIrFy5MgcddFAOP/zwnHfeeUmSESNG5OCDD87555+/TvuYM2dO+vXrl86dOzdr+8ez52+1ubwdANpORalUKpW7CACgdey///4ZMmRIrrjiig22z4qKitx+++0ZN27cBtsnAOAMOgBs8q6++upsueWWeeqpp97Xfk455RSXuwNAK3IGHQA2YUuXLs1f//rXJMm2226bjh07rve+li9fnvr6+iRJr169ssUWW2yQGgGAvxHQAQAAoABc4g4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAFIKADAABAAQjoAAAAUAACOgAAABSAgA4AAAAF8P8BjbdYJGXwxr4AAAAASUVORK5CYII=' width=1000.0/>
</div>



# Gráficos

Si la función no es de tipo `objects.funcFit`, es necesario indicar cuál es la variable independiente de la función y luego usar el método `plot`. \
Los argumentos de `plot` son:
* `ran`: Una tupla que indica el intervalo del gráfico
* `pts`: Entero que indique la cantidad de puntos a calcular
* `ref`: Identificacion para la figura que retorna, por defecto es la ID del `objects.func`
* Parámetros adicionales de personalización


```python
g.x=a
fig = g.plot((1,5))
```



<div style="display: inline-block;">
    <div class="jupyter-widgets widget-label" style="text-align: center;">
        Figure
    </div>
    <img src='data:image/png;base64,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' width=1000.0/>
</div>



# Pasco

Se pueden cargar archivos `.csv` exportados de PASCO Capstone y almacenarse en una variable de tipo `objects.pasco`.


```python
psc = pasco('examples/pscdata.csv')
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Intensidad de campo magnético (G) Serie Nº 3</th>
      <th>Intensidad de campo magnético (G) Serie Nº 4</th>
      <th>Intensidad de campo magnético (G) Serie Nº 5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-3.587876</td>
      <td>-3.774260</td>
      <td>-3.759922</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-3.734832</td>
      <td>-3.774260</td>
      <td>-3.648809</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-3.501853</td>
      <td>-3.774260</td>
      <td>-3.695405</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-3.555618</td>
      <td>-3.770675</td>
      <td>-3.756338</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-3.702574</td>
      <td>-3.770675</td>
      <td>-3.702574</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>721</th>
      <td>-3.774260</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>722</th>
      <td>-3.774260</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>723</th>
      <td>-3.774260</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>724</th>
      <td>-3.774260</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>725</th>
      <td>-3.774260</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>726 rows × 3 columns</p>
</div>


Si se quiere acceder a una serie (columna), se puede llamar la variable con una tupla indicando el sensor (si es que hay mas de uno) comenzando por `0` y el número de serie que indica la tabla. Otra forma es indicando el íncice absoluto de la columna comenzando por `0`.\
Este método tiene los siguientes argumentos:
* `ran`: tupla o lista indicando comienzo y fin del rango de filas deseado (EN UNIDADES DE TIEMPO, NO EN CANTIDAD DE FILAS)
* `plot`: Booleano para graficar el conjunto de puntos indicado


```python
B_1 = psc((0,4), ran=(1,10), plot=True)
```

    No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
    



<div style="display: inline-block;">
    <div class="jupyter-widgets widget-label" style="text-align: center;">
        Figure
    </div>
    <img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA+gAAAH0CAYAAACuKActAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguMywgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/H5lhTAAAACXBIWXMAAA9hAAAPYQGoP6dpAADMSUlEQVR4nOyde7wUdf3/X7N79twFUQ6CckTBuGiSaaVgioSAhiIZX1JLRLG+lpmaqZiWYQZ596t20TpqKJSIeCtTNLz8CvBCoGlCgCIGIioInnPg7GXm98fZzzgzO/eZ3f3s8no+Hueh7MzOzuzMfmben9f79X4rmqZpIIQQQgghhBBCSFlJlHsHCCGEEEIIIYQQwgCdEEIIIYQQQgiRAgbohBBCCCGEEEKIBDBAJ4QQQgghhBBCJIABOiGEEEIIIYQQIgEM0AkhhBBCCCGEEAlggE4IIYQQQgghhEgAA3RCCCGEEEIIIUQCGKATQgghhBBCCCESwACdEEIIIYQQQgiRAAbohBBCCCGEEEKIBDBAJ4QQQgghhBBCJIABOiGEEEIIIYQQIgEM0AkhhBBCCCGEEAlggE4IIYQQQgghhEgAA3RCCCGEEEIIIUQCGKATQgghhBBCCCESwACdEEIIIYQQQgiRAAbohBBCCCGEEEKIBDBAJ4QQQgghhBBCJIABOiGEEEIIIYQQIgEM0AkhhBBCCCGEEAlggE4IIYQQQgghhEgAA3RCCCGEEEIIIUQCGKATQgghhBBCCCESwACdEEIIIYQQQgiRAAbohBBCCCGEEEKIBDBAJ4QQQgghhBBCJIABOiGEEEIIIYQQIgEM0AkhhBBCCCGEEAlggE4IIYQQQgghhEgAA3RCCCGEEEIIIUQCGKATQgghhBBCCCESwACdEEIIIYQQQgiRAAbohBBCCCGEEEKIBDBAJ4QQQgghhBBCJIABOiGEEEKkY86cObjjjjvKvRuEEEJISWGATgghVYKiKPjZz37mud7PfvYzKIoS62cfcMABmDZtWqj3rl+/Hoqi4N577411n0jl8thjj+G8887D4Ycf7vs9xbiu/XL99ddj6NChUFU19Db+/e9/o6amBq+//nqMexYfxx13HI477rhy7wYhhFQ9DNAJIbst9957LxRFwSuvvBL4vZ2dnfjZz36G5557Lv4dI2Q3Zv369Zg+fTrmzp2LkSNHmpbJ+LvbsWMHrrvuOlx++eVIJMyPVV1dXbj99tvx5S9/Gb169UJtbS323XdfTJw4EX/84x+Ry+X0dQ8++GBMmDABP/3pT31/9r/+9S9MnjwZAwYMQH19Pfbbbz+MHTsWt99+e2zHVyymTZsGRVEwfPhwaJpWsFxRFHz/+9/X/53NZvHTn/4UX/ziFzFy5Eicfvrp+PDDDwN95t///ncoigJFUQK/lxBCSgUDdEIICUFnZydmzpwpVaCwc+dOXHXVVeXeDUIisXLlStx555342te+VrDM7Xd31VVXYefOnSXYQzN33303stksTj/9dNPrH3zwAY4++mj84Ac/QHNzM6666irceeeduOCCC9DR0YEzzjgDs2bNMr3nvPPOw8MPP4x169Z5fu6SJUvwhS98Aa+++iq+/e1v44477sC5556LRCKB//u//4v1GAFg0aJFWLRoUezb/de//oWFCxd6rnfjjTfiz3/+M5577jksWbIEe++9N84880zfn6OqKi644AI0NTVF2V1CCCk6NeXeAUIIIfFQX19f7l0gJDKTJk0K9b6amhrU1JT+seaee+7BxIkTC35/Z555JlasWIGHHnoIp556qmnZFVdcgVdeeQWrV682vX788cejV69e+MMf/oBrrrnG9XN/8YtfoGfPnnj55Zex5557mpZt2bIl/AFZ6OzsRGNjI2pra2PbpqChoQGtra245pprcOqpp7paFO6++25cdtlleoD9wx/+EIMGDcJ7772Hfv36eX7WXXfdhXfffRfnnntuUSYwCCEkLqigE0KIgWnTpqG5uRkbN27EpEmT0NzcjJaWFvzoRz/S01HXr1+PlpYWAMDMmTP1lEmj/3vVqlWYPHky9tprL9TX1+MLX/gCHnvsMdNniRT7f/zjH/jhD3+IlpYWNDU14Wtf+xo++OAD07qvvPIKxo8fj969e6OhoQEHHnggzjnnHNM6dh70v//97/jiF7+I+vp6DBo0CHfeeaftcd9zzz34yle+gj59+qCurg4HH3wwfvOb3xSsp2karr32WvTv3x+NjY0YPXo03njjDV/fLQB8/PHHmDZtGnr27Ik999wTZ511Fj7++GPbdf18h06oqor/+7//w6GHHor6+nq0tLTghBNOMNkZ/B7zAQccgJNOOgnPPfccvvCFL6ChoQGHHnqoruIuXLhQ/5wjjjgCK1asML1fXFNvvfUWxo8fj6amJuy777645pprClJ7Ozo6cMkll6C1tRV1dXUYMmQIbrzxRtsUYCvHHXccPvvZz+K1117DqFGj0NjYiIMOOggLFiwAADz//PM48sgj0dDQgCFDhuCZZ54xvf+dd97B9773PQwZMgQNDQ3Ye++98T//8z9Yv359wWeJz2hoaED//v1x7bXX4p577oGiKKb1xXf397//HV/60pdQX1+PgQMHYs6cOQXb/Pjjj3HRRRfpx37QQQfhuuuu033dXr87Jw/6/fffjy996UtobGxEr169cOyxxxYowb/+9a9xyCGHoK6uDvvuuy/OP/98x+vSyNtvv43XXnsNxx9/vOn1pUuX4qmnnsJ3vvOdguBc8IUvfAHf/OY3Ta+lUikcd9xxePTRRz0/e926dTjkkEMKgnMA6NOnT8Fr999/P4444gg0NDRgr732wmmnnYZ3333XtI64hpYvX45jjz0WjY2N+PGPf6wvs3rQu7q6cPXVV+Oggw5CXV0dWltbcdlll6Grq8tz/wEgkUjgqquuwmuvvYaHH37Ydd3//ve/aG1t1f+93377AUDBMdixdetWXHXVVbjmmmtsvy9CCJEJBuiEEGIhl8th/Pjx2HvvvXHjjTdi1KhRuOmmm3DXXXcBAFpaWvRA7mtf+xruu+8+3HffffqD+BtvvIGjjjoKb775JmbMmIGbbroJTU1NmDRpku1D6AUXXIBXX30VV199Nb773e/i8ccfN3kvt2zZgnHjxmH9+vWYMWMGbr/9dnzzm9/EsmXLXI/jX//6F8aNG4ctW7bgZz/7Gc4++2xcffXVtvvwm9/8BgMGDMCPf/xj3HTTTWhtbcX3vvc9/OpXvzKt99Of/hQ/+clP8LnPfQ433HADBg4ciHHjxqGjo8Pze9U0Daeccgruu+8+fOtb38K1116L//73vzjrrLMK1g36HVqZPn26Huxdd911mDFjBurr603fmd9jBoC1a9fijDPOwMknn4zZs2dj27ZtOPnkkzF37lxcfPHF+Na3voWZM2di3bp1mDJlSkGxsFwuhxNOOAH77LMPrr/+ehxxxBG4+uqrcfXVV5u+n4kTJ+KWW27BCSecgJtvvhlDhgzBpZdeih/+8IeexwwA27Ztw0knnYQjjzwS119/Perq6nDaaafhgQcewGmnnYavfvWr+OUvf4mOjg5MnjwZn3zyif7el19+GUuWLMFpp52G2267Deeddx7+9re/4bjjjkNnZ6e+3saNG/WJmSuuuAIXX3wx5s6d66hKrl27FpMnT8bYsWNx0003oVevXpg2bZppYqezsxOjRo3C/fffj6lTp+K2227D0UcfjSuuuEI/dq/fnR0zZ87EmWeeiVQqhWuuuQYzZ85Ea2srFi9erK/zs5/9DOeffz723Xdf3HTTTfj617+OO++8E+PGjUMmk3H9vpcsWQIABcXsHn/8cQDAt771Ldf323HEEUfg9ddfx44dO1zXGzBgAJYvX+6rqNwvfvELTJ06FZ/5zGdw880346KLLsLf/vY3HHvssQUTER999BFOPPFEHHbYYbj11lsxevRo222qqoqJEyfixhtvxMknn4zbb78dkyZNwi233IJvfOMbvo/3jDPOwGc+8xnbCSsj++23HzZt2qT/e+PGjQCA/v37e37GT37yE/Tt2xf/+7//63u/CCGkbGiEELKbcs8992gAtJdffll/7ayzztIAaNdcc41p3c9//vPaEUccof/7gw8+0ABoV199dcF2x4wZox166KHarl279NdUVdVGjhypfeYznyn4/OOPP15TVVV//eKLL9aSyaT28ccfa5qmaQ8//HDBftph3Z9JkyZp9fX12jvvvKO/9u9//1tLJpOadfjv7Ows2N748eO1gQMH6v/esmWLVltbq02YMMG0vz/+8Y81ANpZZ53lun+PPPKIBkC7/vrr9dey2ax2zDHHaAC0e+65R3/d73dox+LFizUA2g9+8IOCZcb99nPMmqZpAwYM0ABoS5Ys0V976qmnNABaQ0OD6fu98847NQDas88+q78mrqkLLrjAtB8TJkzQamtrtQ8++EDTtE+/n2uvvdb0+ZMnT9YURdHWrl3retyjRo3SAGjz5s3TX1u1apUGQEskEtqyZcsK9t/4ndt9H0uXLtUAaHPmzNFfu+CCCzRFUbQVK1bor3300UfaXnvtpQHQ3n77bf118d298MIL+mtbtmzR6urqtEsuuUR/7ec//7nW1NSk/ec//zF9/owZM7RkMqlt2LBB0zT3393VV19tuq7XrFmjJRIJ7Wtf+5qWy+VM64rrQFzT48aNM61zxx13aAC0u+++u+BzjFx11VUaAO2TTz4xvf61r31NA6D/hgU7d+7UPvjgA/1v27ZtBducN2+eBkB78cUXXT970aJFWjKZ1JLJpDZixAjtsssu05566iktnU6b1lu/fr2WTCa1X/ziF6bX//Wvf2k1NTWm18U19Nvf/rbg80aNGqWNGjVK//d9992nJRIJ7f/9v/9nWu+3v/2tBkD7xz/+4br/Z511ltbU1KRpmqb94Q9/0ABoCxcu1JcD0M4//3z939dee632hS98Qb9Ov/e972ljx451/QxN07RXX31VSyaT2lNPPaVp2qfXifjdEUKIbFBBJ4QQG8477zzTv4855hi89dZbnu/bunUrFi9ejClTpuCTTz7Bhx9+iA8//BAfffQRxo8fjzVr1ujKj+A73/mOKTX3mGOOQS6XwzvvvAMAekrmn//8Z09FT5DL5fDUU09h0qRJ2H///fXXhw0bhvHjxxes39DQoP//9u3b8eGHH2LUqFF46623sH37dgDAM888g3Q6jQsuuMC0vxdddJGvfXriiSdQU1OD7373u/pryWQSF1xwgWm9MN+hkYceegiKopjUaYFxv/0cs+Dggw/GiBEj9H8feeSRAICvfOUrpu9XvG53rRizIkSF6nQ6raeaP/HEE0gmk/jBD35get8ll1wCTdPw17/+1fGYBc3NzTjttNP0fw8ZMgR77rknhg0bpu+b034av49MJoOPPvoIBx10EPbcc0/885//1Jc9+eSTGDFiBA477DD9tb322qsgXVtw8MEH45hjjtH/3dLSgiFDhpg++8EHH8QxxxyDXr166ef7ww8/xPHHH49cLocXXnjB89itPPLII1BVFT/96U8LqquL60Bc0xdddJFpnW9/+9vo0aMH/vKXv7h+xkcffYSamho0NzebXhfqt/X13/72t2hpadH/vvzlLxdss1evXgDgWWV87NixWLp0KSZOnIhXX30V119/PcaPH4/99tvPZAVZuHAhVFXFlClTTN9t37598ZnPfAbPPvusabt1dXU4++yzXT8b6D5nw4YNw9ChQ03b/cpXvgIABdt145vf/Kanin7ZZZdh3LhxOPbYYzFy5Eh8+OGHuP/++z23/YMf/AAnnngixo0b53t/CCGknLBIHCGEWBCeZSO9evXCtm3bPN+7du1aaJqGn/zkJ/jJT35iu86WLVt0/yQAU4AnPguA/nmjRo3C17/+dcycORO33HILjjvuOEyaNAlnnHEG6urqbD/jgw8+wM6dO/GZz3ymYNmQIUPwxBNPmF77xz/+gauvvhpLly41pTMD3cFrz5499QkD6zZbWlr0fXbjnXfeQb9+/QqCliFDhpj+HeY7NLJu3Trsu+++2GuvvVz3x88xC6znSCwzemKNr1uvlUQigYEDB5peGzx4MADonu133nkH++67L/bYYw/TesOGDdOXe9G/f/8CH3bPnj197efOnTsxe/Zs3HPPPdi4caMpUDJOWLzzzjumyQrBQQcdZLtP1u8OKPw9rVmzBq+99lrB704QpujZunXrkEgkcPDBBzuuI75T6zVYW1uLgQMH+vrO7RDnsL293XQdff3rX8dnP/tZAN0TL8Y2awLxvfvp6f7FL34RCxcuRDqdxquvvoqHH34Yt9xyCyZPnoyVK1fi4IMPxpo1a6Bpmu1YAHT73o3st99+vgrCrVmzBm+++WYs5yyZTOKqq67CWWedhUceecS2gn8qlcIvfvEL/OIXv/C93QceeABLliyRtrc8IYTYwQCdEEIsJJPJ0O8V3uMf/ehHtko1UBjIOH2e8UF9wYIFWLZsGR5//HE89dRTOOecc3DTTTdh2bJlBQFvUNatW4cxY8Zg6NChuPnmm9Ha2ora2lo88cQTuOWWWwr81MUmzHcYlKDH7HSOvM5dqYmynxdccAHuueceXHTRRRgxYgR69uwJRVFw2mmnRboG/Hy2qqoYO3YsLrvsMtt1xWSGbOy9997IZrP45JNPTBMrQ4cOBQC8/vrrOProo/XXW1tb9ckSkS1gRUxc9O7d2/d+1NbW4otf/CK++MUvYvDgwTj77LPx4IMP4uqrr4aqqlAUBX/9619tz4V1/DBmUrihqioOPfRQ3HzzzbbLrZNCXnzzm9/Ez3/+c1xzzTW2lfx/+ctf4sknnyx43a3V5aWXXor/+Z//QW1trT4RJjz37777LtLpNPbdd99A+0kIIcWGATohhITASd0SKmkqlSqo7ByVo446CkcddRR+8YtfYN68efjmN7+JP/3pTzj33HML1m1paUFDQwPWrFlTsMza2unxxx9HV1cXHnvsMZPaaU1RHTBgAIBu5cyoBn/wwQe+sgsGDBiAv/3tb2hvbzcFBdb9ifodDho0CE899RS2bt3qqKL7Pea4UFUVb731linQ/M9//gOgu9I50P39PPPMMwXB3qpVq/TlxWTBggU466yzcNNNN+mv7dq1q6CI2IABA7B27dqC99u95pdBgwahvb3d83z7UZWN21RVFf/+979N6fhGxHe6evVq0zWdTqfx9ttve+6PCMTffvttDB8+XH/9pJNOwi9/+UvMnTvXFKD74e2330YikQg9KfGFL3wBAPDee+8B6P4eNE3DgQceGOtEx6BBg/Dqq69izJgxgc6LE0JFnzZtmm0V+xkzZmDGjBmBtvnuu+9i3rx5mDdvXsGyww8/HJ/73OewcuXKsLtMCCFFgR50QggJQWNjIwAUBC99+vTBcccdhzvvvFN/QDZibZ/mh23bthUosiLgcGpnlEwmMX78eDzyyCPYsGGD/vqbb76Jp556qmBdAAUpzffcc49pveOPPx6pVAq33367ad1bb73V13F89atfRTabNbUyy+VyuP32203rRf0Ov/71r0PTNMycObNgmdhvv8ccJ3fccYdpP+644w6kUimMGTMGQPf3k8vlTOsBwC233AJFUXDiiScWbd+A7u/Eep3dfvvtBWnY48ePx9KlS02BzdatWzF37tzQnz1lyhS9NZmVjz/+GNlsFoDz786OSZMmIZFI4JprrinIABDHefzxx6O2tha33Xab6djb2tqwfft2TJgwwfUzRKq/sX0fABx99NEYO3Ys7rrrLseWaU5ZFsuXL8chhxxiSo2349lnn7XdhrCviLT9U089FclkEjNnzixYX9M0fPTRR66f48SUKVOwceNG/O53vytYtnPnTl+dHax861vfwkEHHWT72w3Dww8/XPAnKszPmTMHt9xySyyfQwghcUIFnRBCQtDQ0ICDDz4YDzzwAAYPHoy99toLn/3sZ/HZz34Wv/rVr/DlL38Zhx56KL797W9j4MCBeP/997F06VL897//xauvvhros/7whz/g17/+Nb72ta9h0KBB+OSTT/C73/0OPXr0wFe/+lXH982cORNPPvkkjjnmGHzve99DNpvF7bffjkMOOQSvvfaavt64ceNQW1uLk08+Gf/7v/+L9vZ2/O53v0OfPn1MAbLoBz979mycdNJJ+OpXv4oVK1bgr3/9q6903JNPPhlHH300ZsyYgfXr1+Pggw/GwoULCwqyAYj0HY4ePRpnnnkmbrvtNqxZswYnnHACVFXF//t//w+jR4/G97//fd/HHBf19fV48skncdZZZ+HII4/EX//6V/zlL3/Bj3/8Y93De/LJJ2P06NG48sorsX79enzuc5/DokWL8Oijj+Kiiy7CoEGDYt8vIyeddBLuu+8+9OzZEwcffDCWLl2KZ555Bnvvvbdpvcsuuwz3338/xo4diwsuuABNTU34/e9/j/333x9bt24NpaZeeumleOyxx3DSSSdh2rRpOOKII9DR0YF//etfWLBgAdavX4/evXu7/u6sHHTQQbjyyivx85//HMcccwxOPfVU1NXV4eWXX8a+++6L2bNno6WlBVdccQVmzpyJE044ARMnTsTq1avx61//Gl/84hc926QNHDgQn/3sZ/HMM8/gnHPOMS27//77ccIJJ2DSpEk48cQTcfzxx6NXr17YvHkznnnmGbzwwgsFky6ZTAbPP/88vve973l+ZxdccAE6Ozvxta99DUOHDkU6ncaSJUvwwAMP4IADDtALvQ0aNAjXXnstrrjiCqxfvx6TJk3CHnvsgbfffhsPP/wwvvOd7+BHP/qR5+dZOfPMMzF//nycd955ePbZZ3H00Ucjl8th1apVmD9/Pp566ildzfdLMpnElVde6atInR/sUuXFxNKJJ54YyEZACCElo1Tl4gkhRDac2qyJ1j9GrC2cNE3TlixZoh1xxBFabW1tQeundevWaVOnTtX69u2rpVIpbb/99tNOOukkbcGCBa6fr2ma9uyzz5padf3zn//UTj/9dG3//ffX6urqtD59+mgnnXSS9sorr5jeZ90HTdO0559/Xt/HgQMHar/97W9tj+Wxxx7Thg8frtXX12sHHHCAdt1112l33313QdusXC6nzZw5U+vXr5/W0NCgHXfccdrrr7+uDRgwwLPNmqZ1t+M688wztR49emg9e/bUzjzzTG3FihUFLb/8fodOZLNZ7YYbbtCGDh2q1dbWai0tLdqJJ56oLV++PPAxDxgwQJswYULBZ8DSBkrTNO3tt9/WAGg33HCD/pq4ptatW6eNGzdOa2xs1PbZZx/t6quvLmj/9cknn2gXX3yxtu+++2qpVEr7zGc+o91www2m9nBOjBo1SjvkkEMKXve7/9u2bdPOPvtsrXfv3lpzc7M2fvx4bdWqVbbndsWKFdoxxxyj1dXVaf3799dmz56t3XbbbRoAbfPmzZ6fbW3ZJY79iiuu0A466CCttrZW6927tzZy5EjtxhtvNLUOc/rd2V3XmqZpd999t/b5z39eq6ur03r16qWNGjVKe/rpp03r3HHHHdrQoUO1VCql7bPPPtp3v/td2xZodtx8881ac3OzbZu6nTt3arfeeqs2YsQIrUePHlpNTY3Wt29f7aSTTtLmzp2rZbNZ0/p//etfNQDamjVrPD/3r3/9q3bOOedoQ4cO1Zqbm7Xa2lrtoIMO0i644ALt/fffL1j/oYce0r785S9rTU1NWlNTkzZ06FDt/PPP11avXq2v43QNiWXWc5ZOp7XrrrtOO+SQQ/Tv94gjjtBmzpypbd++3XX/ncbaTCajDRo0yPb3FQdss0YIkR1F08pUyYYQQgjZDZg2bRoWLFiA9vb2cu9KUbnoootw5513or29PVKhxUpj+/btGDhwIK6//npMnz490rYmTZoERVHw8MMPx7R3hBBCKg160AkhhBASiJ07d5r+/dFHH+G+++7Dl7/85d0qOAe6W9ZddtlluOGGGyJVu3/zzTfx5z//GT//+c9j3DtCCCGVBhV0QgghpIhUo4J+2GGH4bjjjsOwYcPw/vvvo62tDZs2bcLf/vY3HHvsseXePUIIIaRiYZE4QgghhATiq1/9KhYsWIC77roLiqLg8MMPR1tbG4NzQgghJCJU0AkhhBBCCCGEEAmgB50QQgghhBBCCJEABuiEEEIIIYQQQogE0IO+m6GqKjZt2oQ99tgDiqKUe3cIIYQQQgghZULTNHzyySfYd999kUhQu5UBBui7GZs2bUJra2u5d4MQQgghhBAiCe+++y769+9f7t0gYIC+27HHHnsA6P4R9ujRo8x7QwghhBBCCCkXO3bsQGtrqx4jkPLDAH03Q6S19+jRgwE6IYQQQgghhNZXiaDRgBBCCCGEEEIIkQAG6IQQQgghhBBCiAQwQCeEEEIIIYQQQiSAHnRCCCGEEEIIqVByuRwymYztslQqhWQyWeI9IlFggE4IIYQQQgghFYamadi8eTM+/vhj1/X23HNP9O3bl4XgKgQG6IQQQgghhBBSYYjgvE+fPmhsbCwIwDVNQ2dnJ7Zs2QIA6NevXzl2kwSEATohhBBCCCGEVBC5XE4Pzvfee2/H9RoaGgAAW7ZsQZ8+fZjuXgGwSBwhhBBCCCGEVBDCc97Y2Oi5rljHyadO5IIBOiGEEEIIIYRUIH585fSeVxYM0AkhhBBCCCGEEAlggE4IIYQQQgghhEgAA3RCCCGEEEIIIUQCGKCHYOLEidh///1RX1+Pfv364cwzz8SmTZsc11+/fj0URbH9e/DBB03r3nvvvRg+fDjq6+vRp08fnH/++ablr732Go455hjU19ejtbUV119/fVGOkRBCCCGEECI3mqbFsg6RBwboIRg9ejTmz5+P1atX46GHHsK6deswefJkx/VbW1vx3nvvmf5mzpyJ5uZmnHjiifp6N998M6688krMmDEDb7zxBp555hmMHz9eX75jxw6MGzcOAwYMwPLly3HDDTfgZz/7Ge66666iHi8hVj7s7Cz3LhBCCCGkgvl41y5kcrly70bFkkqlAACdPp7JxDriPURuFI1TKpF57LHHMGnSJHR1dfm+8D//+c/j8MMPR1tbGwBg27Zt2G+//fD4449jzJgxtu/5zW9+gyuvvBKbN29GbW0tAGDGjBl45JFHsGrVKl+fu2PHDvTs2RPbt29Hjx49fL2HECP/fP99HDl3Ljaddx5afLT2IIQQQgixcsg99+C7n/scvn/44eXelYrlvffe03uhNzY2FlRr1zQNnZ2d2LJlC/bcc0/069evYBuMDeSjptw7UOls3boVc+fOxciRI30H58uXL8fKlSvxq1/9Sn/t6aefhqqq2LhxI4YNG4ZPPvkEI0eOxE033YTW1lYAwNKlS3HsscfqwTkAjB8/Htdddx22bduGXr16FXxWV1cXurq69H/v2LEj7KESAgDY0tmJrKpie1cXA3RCCCGEhOKDzk58sHNnuXejounbty8AYMuWLa7r7bnnnvq6RH6Y4h6Syy+/HE1NTdh7772xYcMGPProo77f29bWhmHDhmHkyJH6a2+99RZUVcWsWbNw6623YsGCBdi6dSvGjh2LdDoNANi8eTP22Wcf07bEvzdv3mz7WbNnz0bPnj31PxHsExKWdD4dLauqZd4TQgghhFQqOU3js0REFEVBv379MHjwYBx44IG2f4MHD0a/fv3YC72CYICeZ8aMGY6F3MSfMY380ksvxYoVK7Bo0SIkk0lMnTrVVwGGnTt3Yt68eZg+fbrpdVVVkclkcNttt2H8+PE46qij8Mc//hFr1qzBs88+G/q4rrjiCmzfvl3/e/fdd0NvixCAATohhBBCosMAPT6SySTq6+tt/5LJZLl3jwSEKe55LrnkEkybNs11nYEDB+r/37t3b/Tu3RuDBw/GsGHD0NraimXLlmHEiBGu21iwYAE6OzsxdepU0+vCE3LwwQfrr7W0tKB3797YsGEDgO40lvfff9/0PvFv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' width=1000.0/>
</div>




```python
B_2 = psc(2, ran=(1,10))
```

Ahora se pueden hacer todos los calculos de esta lista de valores utilizando `objects.var`.


```python
B_1, B_2 = var('B_1', B_1, 'G'), var('B_2', B_2, 'G')
```


$\displaystyle B_{1} = (-3.7727 \pm 0.0002) \, G$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad B_{1 \, 95\%}=(-3.7727 \pm 0.0004) \, G$



$\displaystyle B_{2} = (-3.62 \pm 0.01) \, G$



$\displaystyle \text{Intervalo de confianza de 95\,\%\,:}\quad B_{2 \, 95\%}=(-3.62 \pm 0.02) \, G$


# Pruebas de hipótesis con t de Student

Las pruebas de hipótesis se realizan con la función `stats.t_test`. El procedimiento es automático para pruebas entre una variable de tipo `objects.var` y un parámetro de tipo `objects.param` o para dos variables.\
En este último caso analiza si las varianzas son homogéneas a través de la prueba con distribución F.


```python
stats.t_test(B_1, B_2)
```


$\displaystyle \text{Se analiza si las varianzas son homogéneas con un nivel de significancia }\, \alpha = 0.1$



$\displaystyle \text{Hipótesis nula }\, H_0: s_{B1} = s_{B2} \quad \text{Hipótesis alternativa }\, H_a: s_{B1} \neq s_{B2}$



$\displaystyle f = \frac{s_{B1}^{2}}{s_{B2}^{2}} = 0.0004645627787879033$



$\displaystyle \text{Región de rechazo: }\, RR = \{f \geq F_{0.05,179,179} \, o \, f \leq F_{0.95,179,179} \}$



$\displaystyle RR = \{f \geq 1.280 \, o \, f \leq 0.782 \}$



$\displaystyle f \in RR \quad \text{Se rechaza la Hipótesis nula, } \, s_{B1} \neq s_{B2} \, \text{ con un nivel de significancia }\, \alpha = 0.1$



$\displaystyle \text{Se procede a la comparación para varianzas no homogéneas con un nivel de significancia }\, \alpha = 0.05$



$\displaystyle t = \frac{\overline{B_{1}} - \overline{B_{2}}}{\sqrt{\frac{s_{B2}^{2}}{n_{B2}} + \frac{s_{B1}^{2}}{n_{B1}}}}=-14.829738370715608$



$\displaystyle \nu=\frac{\left(\frac{s_{B2}^{2}}{n_{B2}} + \frac{s_{B1}^{2}}{n_{B1}}\right)^{2}}{\frac{s_{B2}^{4}}{\nu_{B2} n_{B2}^{2}} + \frac{s_{B1}^{4}}{\nu_{B1} n_{B1}^{2}}}= 179.16631343891257\approx 179.0$



$\displaystyle \text{Región de rechazo: }\, RR = \{\lvert t \rvert \geq t_{0.025,179.0}\}$



$\displaystyle RR = \{\lvert t \rvert \geq 1.973\}$



$\displaystyle t \in RR \quad \text{Se rechaza la Hipótesis nula, } \, B_{1} \neq B_{2} \, \text{ con un nivel de significancia }\, \alpha = 0.05$

