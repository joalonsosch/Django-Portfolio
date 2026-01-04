# Pregunta técnica Python

## Definiciones

Un portafolio de inversión está compuesto por una combinación de N activos. En cada instante de tiempo $t$ el monto en dólares para el activo viene dado por la variable $x_{i,t}$ y por tanto el valor total del portafolio en tiempo $t$ $(V_{t})$ es equivalente a:

$$V_{t}=\sum_{i=1}^{N}x_{i,t}$$

El precio de cada activo en el tiempo viene dado por $p_{i,t}$ y la cantidad de cada activo en el tiempo viene dado por $c_{i,t}$ de forma tal que se cumple que:

$$x_{i,t}=p_{i,t}*c_{i,t}$$

A su vez se conoce como weight $(w_{i,t})$ de cada activo al % que representa este sobre el portafolio total. En otras palabras se cumple que:

$$w_{i,t}=\frac{x_{i,t}}{V_{t}}=\frac{p_{i,t}*c_{i,t}}{V_{t}}$$

Considere un portafolio que tiene su inicio en $t=0$ con valor inicial $V_{0}$. La cantidad invertida por activo $(c_{i,0})$ se puede calcular usando las definiciones anteriores lo que da como resultado:

$$C_{i,0}=\frac{w_{i,0}*V_{0}}{P_{i,0}}$$

En el siguiente archivo:

datos.xlsx 62.7KB

Se encuentran dos sets de datos separados por hoja:

* **Weights:** valores para $w_{i,0}$ de dos portafolios (1 y 2 en las columnas C y D respectivamente) donde el tiempo $t=0$ equivale al $15/2/22$ e $i=1,...,17$ corresponde a cada uno de los 17 activos invertibles
* **Precios:** valores para $P_{i,t}$ donde cada columna corresponde a cada uno de los 17 activos y cada fila corresponde al tiempo $t=15/2/22,...,16/2/23$

## Preguntas

1. Cree un proyecto en Django que permita modelar la definición anterior. Esto es, activos, portafolios, precios, cantidades, weights, montos y cualquier otro elemento que estime conveniente. Considere que el proyecto debe permitir responder las siguientes preguntas

2. Genere una función tipo ETL que permita leer y cargar los datos del archivo datos.xlsx a la base de datos correspondiente al proyecto django mencionado en el punto anterior

3. Considere que tanto el portafolio 1 como el portafolio 2 tienen un valor inicial al 15/02/22 $(V_{0})$ de \$1,000,000,000. Calcule las cantidades iniciales $(C_{i,0})$ para cada uno de los 17 activos en cada uno de los 2 portafolios.

4. A partir del $15/02/22$ los valores de las cantidades se mantienen invariantes, $c_{i,t}=c_{i,0}$ y por tanto los valores de $x_{i,t}$; $w_{i,t}$ y $V_{t}$ evolucionan debido a la variación en el tiempo de los precios $p_{i,t}$ y las definiciones explicitadas en el inicio del documento. Genere endpoints tipo API rest que reciban los parametros fecha_inicio y fecha_fin y entregue los valores entre esas fechas para $w_{i,t}$ y $V_{t}$. Se espera uso del ORM de django para obtener los datos necesarios para los cálculos

5. Bonus 1: Genere un view que utilice la API anterior donde se pueda comparar de manera gráfica la evolución en el tiempo de las variables $w_{i,t}$ y $V_{t}$ Para $w_{i,t}$ se recomienda un grafico tipo "stacked area" y para $V_{t}$ gráficos de linea.

6. Bonus 2: Considere ahora la creación de un metodo que permita procesar compra ventas de activos. La anterior debe permitir procesar que el día 15/05/2022 se realiza una operación de compra y venta, donde se venden \$200,000,000 del activo EEUU y se compran \$200.000.000 de Europa en el portafolio 1. Calcule el nuevo historial de $c_{i,t}$; $x_{i,t}$; $w_{i,t}$ y $V_{t}$.

7. Bonus: Estructurar el proyecto de Django siguiendo la siguiente guía de estilos que está en el archivo .md correspondiente.
