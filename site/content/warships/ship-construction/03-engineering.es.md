+++
title = "Ingeniería"
description = "Paso 3 al Paso 5 de la construcción de Starship."
weight = 30
+++
## Paso 3: Planta de energía

El corazón de cualquier barco es su central eléctrica. Se necesitan grandes cantidades de energía para impulsar una nave a través del espacio, energizar su armamento y defensas y suministrar calor y gravedad. Una nave bajo Armas de energía puede tener docenas de armas mortales, pero no tener capacidad para llevarlas a la pelea o emplearlas todas una vez que esté allí.

La planta de energía del barco suministra uno de los tres productos básicos que querrás conservar en Rastrear mientras construyes tu barco: energía. (Los dos productos del Otros son puntos de casco y dinero, en caso de que lo hayas olvidado). Muchos sistemas requieren una cantidad específica de energía para funcionar, por lo que querrás asegurarte de saber si tu nave tiene suficientes puntos de energía para que todo lo que consideras importante funcione al mismo tiempo.

Las plantas de energía se clasifican según la cantidad de puntos de energía que producen PER punto de durabilidad. Por ejemplo, si estás construyendo un caza de durabilidad 10, podrías decidir instalar un reactor masivo de durabilidad 3. Esto genera 7,5 puntos de energía para el barco (redondeando a 8) y cuesta 600.000.

Algunas centrales eléctricas no se pueden miniaturizar más allá de cierto punto y no están disponibles para instalaciones mínimas. Esto se expresa como un tamaño mínimo para la central eléctrica. Algunas centrales eléctricas también pueden tener un tamaño máximo, lo que indica que la tecnología simplemente no es adecuada para aplicaciones extremadamente grandes. Sin embargo, puedes sortear la limitación de tamaño máximo instalando varias plantas de energía pequeñas: la energía de todas las fuentes cuenta para el total del barco.

Como eres el diseñador, puedes decidir si los múltiples puntos de durabilidad gastados en tu planta de energía forman una gran planta de energía o varias plantas de energía pequeñas esparcidas por el barco. La ventaja de varias plantas pequeñas es que tu nave es algo más resistente a los daños: es difícil eliminar toda tu potencia de un solo disparo. Sin embargo, es más caro construir un barco de esta manera.

Por ejemplo, un reactor de gran masa capaz de generar 10 puntos de potencia requiere 4 puntos de durabilidad (cada punto de durabilidad proporciona 2,5 puntos de potencia). Esta instalación cuesta 100.000 por el reactor, más 100.000 por cada uno de los cuatro puntos de durabilidad asociados con el reactor, un total de 500.000. Si comprara esto como cuatro reactores de masa de una durabilidad, pagaría el costo base multiplicado por cuatro, más el costo de durabilidad nuevamente, para un total de 800.000. Tenga en cuenta que algunos sistemas de energía son difíciles de ampliar y tienen un punto de durabilidad PER de costo relativamente alto, mientras que los sistemas Otros se pueden ampliar fácilmente y tienen un punto de durabilidad PER de bajo costo.

### Tabla 5-3: Centrales eléctricas

| Planta de energía | Tecnología | Pow | Costo base | Costo/casco pt. | Tamaño mínimo | ¿Combustible? | Costo del combustible | Eficiencia de combustible |
|---|---|---|---|---|---|---|---|---|
| Célula solar | S | 1.5 | $500 mil | $200 mil | 4 | No | - | - |
| Generador de fisión | - | 1.5 | 1 millón de dólares | $100 mil | 4 | No | - | - |
| Generador de fusión | F | 2.0 | 1 millón de dólares | $200 mil | 2 | Sí | $1 mil | 200 |
| Célula de fusión gravitacional | GRAMO | 2.5 | 2 millones de dólares | $200 mil | 4 | Sí | $1 mil | 300 |
| Tanque de combustible | - | - | $50 mil | $10 mil | - | - | - | - |
| Colisionador taquiónico | Q | 2.5 | 1 millón de dólares | $100 mil | 2 | No | - | - |
| Reactor de antimateria | Un | 3.0 | 4 millones de dólares | $400 mil | 3 | No | - | - |
| Reactor de masa | D | 3.5 | 2 millones de dólares | $250 mil | 2 | No | - | - |
| Reactor de masa dinámico | D | 4.0 | 3 millones de dólares | $200 mil | 1 | No | - | - |
| Convertidor de Materia | M, X | 4.5 | 4 millones de dólares | $200 mil | 2 | No | - | - |
| Célula cuántica | Q | 5.0 | 5 millones de dólares | $400 mil | 3 | No | - | - |
| Generador de singularidad | GRAMO | 6.0 | 10 millones de dólares | $500 mil | 20 | No | - | - |

**Tech**: La tecnología Rastrear necesaria para producir este sistema de energía.
**Pow**: La cantidad de energía producida por una central eléctrica de 1 punto de casco. Las fracciones se redondean normalmente, por lo que un reactor de antimateria de 2 puntos de casco (3,0 puntos de casco PER producidos con energía) produce 6 puntos de potencia.
**Costo base**: El costo de cada planta de energía instalada por separado.
**Costo/Punto de casco**: El costo de cada punto de casco de la planta de energía, acumulativo con el costo de cada nueva planta.
**Tamaño mínimo**: La central eléctrica más pequeña posible, en puntos de casco.
**Tamaño máximo**: La central eléctrica más grande posible, en puntos de casco.
**Combustible**: Si el sistema de energía requiere o no tanque de combustible adicional.
**Costo de combustible**: El costo del punto de casco PER del combustible comprado.
**Eficiencia**: El número de días de energía que puede generar 1 punto de combustible del casco. Por ejemplo, un punto de combustible en el casco proporciona 200 días de energía para un generador de fusión de 1 punto de casco, o 20 días de energía para un generador de fusión de 10 puntos de casco.

### Depósitos de combustible y repostaje

En niveles de progreso más altos, la mayoría de las centrales eléctricas requieren reabastecimiento de combustible sólo en intervalos poco frecuentes. Su combustible es inagotable o sólo necesita ser reemplazado cuando se revisa todo el barco. Sin embargo, muchas centrales eléctricas PL 6 requieren un tanque de combustible además de los sistemas de energía propiamente dichos.

La cantidad de combustible que lleva un barco depende de usted, pero la consideración más importante aquí es Resistencia. En palabras de Otros, ¿cuánto tiempo puede funcionar la central eléctrica con un tanque de combustible? Esto se mide por los días de energía totales del tanque de combustible. Si un tanque de combustible tiene capacidad para 100 días de energía, puede operar una planta de energía que genera 1 punto de energía por 100 días, 2 puntos de energía por 50 días, 20 puntos de energía por 5 días, y así sucesivamente. Si su diseño requiere 10 puntos de energía para hacer funcionar sus sistemas principales, es una idea muy Bueno comprar varios tanques de combustible (o uno grande) para que su barco funcione durante al menos un par de semanas sin repostar.

### Sistemas de energía

Con la posible excepción de la celda cuántica, un sistema de generación de energía no crea energía. En cambio, transforma la energía de un tipo a otro, más utilizable. La caldera de un barco de vapor transforma la energía almacenada en los enlaces químicos de su fueloil en energía térmica, que luego se transforma en energía cinética a través de una turbina. De manera similar, un generador de fisión o fusión convierte la energía de los enlaces atómicos en energía térmica que luego se transforma en electricidad, o en alguna forma de energía fácil de utilizar.

La mayoría de estos sistemas de energía en realidad transportan combustible de un tipo u otro, incluso si no se requiere un tanque de combustible. Un generador de fisión no necesita miles de galones de agua, pero sí una cierta cantidad de uranio o plutonio que se consume con el tiempo. La duración de una planta típica y sus costos de reabastecimiento de combustible se abordan en la descripción de cada sistema de energía.

**Célula solar (PL 6)**
La célula solar convierte la energía luminosa y térmica de una estrella cercana en energía a bordo de un barco a través de grandes bancos de células fotovoltaicas e intercambiadores de calor altamente eficientes. A 1 UA (150 millones de kilómetros) de una estrella de tipo Sol, la capacidad de generación de energía de la célula solar aumenta en un 50 por ciento; de manera similar, a una distancia de más de 5 AU de una estrella de tipo Sol, la capacidad de generación de energía de la célula solar cae en un 50 por ciento. Por ejemplo, un crucero equipado con 40 puntos de durabilidad de células solares normalmente genera 40 puntos de energía; esto aumenta a 60 puntos de potencia en la parte interior de un sistema estelar y cae a 20 puntos de potencia en la parte exterior de un sistema estelar. Tenga en cuenta que las estrellas particularmente brillantes (clase O, B o A) amplían el rango de alta eficiencia y caída de energía a 2 AU y 10 AU, mientras que las estrellas muy pequeñas (clase K y M) cambian estas cifras a 0,5 AU y 2 AU.

**Generador de fisión (PL 6)**
También conocida como central atómica o nuclear, el generador de fisión extrae energía de una reacción en cadena controlada de uranio o plutonio. Los generadores de fisión requieren un blindaje pesado, por lo que las instalaciones pequeñas son muy difíciles. Sin embargo, la tecnología es fácil de aplicar a grandes instalaciones.
Las barras de combustible de un generador de fisión duran aproximadamente de dos a cuatro años y luego deben ser reemplazadas con un coste de 50.000 PER punto de casco de la central eléctrica.

**Generador de fusión (PL 6)**
Un generador de fusión aprovecha el poder de la fusión nuclear para crear energía a bordo. Un dispositivo de contención “embotella” la reacción en campos magnéticos, ya que el núcleo del generador arde a temperaturas tan altas como la superficie de una estrella. Afortunadamente, la mayoría de los generadores de fusión están diseñados para funcionar a prueba de fallos en caso de daños.
El generador de fusión utiliza hidrógeno como combustible, pero al igual que el reactor de fusión en frío, éste suele almacenarse en forma de agua.

**Célula Grav-Fusion (PL 6)**
Basada en un dispositivo fraal, la celda de gravedad-fusión emplea campos de gravedad artificiales para contener y mejorar el rendimiento de una reacción de fusión. Por lo demás, es similar al generador de fusión.

**Reactor de Antimateria (PL 7)**
El reactor de antimateria aniquila partículas de antimateria para crear grandes cantidades de energía. Al igual que el generador de fusión, requiere algunos procedimientos de contención muy cuidadosos, y una parte importante de la producción del generador debe dedicarse a mantener los campos magnéticos que aíslan su fuente de combustible de su entorno. No se requiere tanque de combustible: la antimateria y su dispositivo de contención están incluidos en el costo de durabilidad y el precio del reactor.
El reactor de antimateria requiere un reabastecimiento de combustible aproximadamente una vez entre tres y cinco años, aunque funcionar con una configuración de energía mínima (nada más que soporte vital) podría extender este tiempo a diez o quince años entre cada repostaje. La antimateria es cara; Repostar el reactor cuesta la mitad de lo que se gastaba en la central eléctrica en el momento de su construcción.

**Reactor de masa (PL 7)**
La tecnología de la materia oscura supone que la materia oscura no bariónica puede tener propiedades desconocidas para la ciencia del siglo XX. En concreto, la materia oscura puede sufrir un proceso de desintegración similar a la desintegración radiactiva en el que se libera energía mediante la transformación de la materia oscura en “materia normal”. El reactor de masa aprovecha esta fantástica energía. Al igual que el reactor de antimateria, el reactor de masa no requiere tanque de combustible; La materia oscura y su dispositivo de contención ya están incluidos.
El reactor de masa requiere reabastecimiento de combustible aproximadamente una vez cada seis meses, con un costo equivalente a 5.000 PER punto de casco de la central eléctrica.

**Colisionador taquiónico (PL 7)**
Los taquiones son partículas que se mueven más rápido que la velocidad de la luz. El colisionador taquiónico frena estas partículas y aprovecha su energía. Si bien el colisionador es costoso y no proporciona tanta potencia como los sistemas de energía Otros en este nivel de progreso, tiene una ventaja significativa: no requiere ningún combustible.

**Reactor de masa dinámica (PL 8)**
Básicamente un refinamiento del reactor de masa PL 7, el reactor de masa dinámico acelera el proceso de desintegración, liberando más energía que su predecesor. También es una instalación más pequeña y segura.
El reactor de masa dinámica requiere un repostaje cada seis meses, con un coste equivalente a 10.000 PER de casco de la central. Por ejemplo, repostar un reactor de masa dinámica de 30 puntos de durabilidad cuesta 300.000.

**Convertidor de Materia (PL 8)**
Este dispositivo produce energía mediante la conversión total de la materia. Literalmente cualquier cosa puede usarse como combustible. Si bien el convertidor de materia es caro, produce una inmensa cantidad de energía y no requiere una fuente importante de combustible.

**Célula cuántica (PL 8)**
Aprovechando el Santo Grial de las fuentes de energía (la fluctuación cuántica o energía de punto cero observada en el vacío), la célula cuántica produce una enorme cantidad de energía sin ninguna fuente de combustible.

> **Consejo de diseño: potencia**
> Suponiendo que esté utilizando un sistema de energía promedio (digamos, un reactor de masa), probablemente desee dedicar entre el 10 y el 15 por ciento de los puntos del casco de su barco a su planta de energía. (Los tanques de combustible funcionarían entre un 5 y un 10 por ciento más, si fuera necesario). Esto debería brindarle muchos puntos de energía para todos sus motores, armas y defensas. Tener un barco con poca potencia es una verdadera molestia, ya que tendrás que decidir qué sistemas deben ser Armas de energía durante cada ronda de Combate. Proporcionar a un barco más potencia de la que necesita es más seguro, ya que puedes dañar la planta de energía y no perder la capacidad de luchar eficazmente, pero puedes desperdiciar espacio en el casco y dinero que podría gastarse mejor en otra parte.

**Generador de singularidad (PL 9)**
El generador de singularidades es un dispositivo increíblemente poderoso que aprovecha el poder de un pequeño agujero negro. No es tanto un generador como una batería de gran capacidad, pero la energía contenida en un pequeño agujero negro es asombrosa.
Con el paso de los años, la singularidad se reducirá a medida que se “evapore” o pierda energía; el generador de singularidad debe ser reabastecido mediante la creación de un nuevo agujero negro. Un generador singularidad dura de 10 a 15 años antes de que sea necesario repostar. Repostar combustible cuesta una cantidad de dinero equivalente a la mitad del coste de la central eléctrica en el momento de su construcción.

## Paso 4: motores

Sin motores, un barco no puede ir a ninguna parte. Muchos barcos pequeños confían en su movilidad y maniobrabilidad como primera (y a veces única) línea de defensa contra el fuego enemigo. Los sistemas de motor consumen puntos de energía creados por la central eléctrica del barco y los convierten en aceleración. Al igual que el blindaje, los sistemas de motores son proporcionales al tamaño del barco y requieren la dedicación de un cierto porcentaje de los puntos del casco del barco para alcanzar los puntos de interrupción de efectividad designados.

### Requisitos de combustible del motor

Varios tipos de motores requieren algún tipo de tanque de combustible, más allá de los requisitos de combustible para la central eléctrica del barco. Cada punto de combustible del casco contiene una cierta cantidad de días de empuje para un motor de 1 punto del casco; Esta es la cantidad de días que el motor podría funcionar continuamente con 1 punto de combustible en el casco. Los motores con 2, 3 o más puntos de casco quemarán combustible dos, tres, etc., veces más rápido que la cifra indicada. La cifra de consumo de combustible supone un empuje máximo más o menos continuo. Naturalmente, un barco que pasa tres semanas a la deriva sin encender sus motores no consume combustible alguno.

### Tabla 5-4: Motores

| Motor | Tecnología | Pow | Tamaño mínimo | Costo Básico. | Costo/Casco | Aceleración @ 5% | @ 10% | @ 15% | @ 20% | @ 30% | @ 40% | @ 50% | Ef. | Costo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Propulsor planetario | - | 1.0 | 1 | $200 mil | $50 mil | 0,1* | 0,25* | 0,5* | 1* | - | - | - | 10 | $10 mil |
| Vela de fotones | - | - | 5 | $500 mil | $50 mil | -- | 0,02* | 0,05* | 0,1* | 0,15* | 0,2* | 0,25* | - | - |
| Antorcha de fusión | - | 0,33 | 3 | $500 mil | $100 mil | 0,5* | 1* | 1,5* | 2* | 3* | 4* | 5* | 200 | $1 mil |
| Motor de iones | S | 0,5 | 2 | $800 mil | $200 mil | -- | 0,5* | 1* | 1,5* | 2* | 3* | 4* | 400 | $5 mil |
| Impulso de partículas | - | 0,75 | 4 | $500 mil | $300 mil | 0,5 | 1.0 | 1.5 | 2 | 2.5 | 3 | 4 | - | - |
| Motor de inducción | GRAMO | 1.0 | 2 | 1 millón de dólares | $500 mil | 1 | 2 | 3 | 4 | 5 | 6 | 8 | - | - |
| Motor de flujo inercial | X | 1.0 | 1 | 2 millones de dólares | $500 mil | 2 | 3 | 4 | 5 | 6 | 8 | 10 | - | - |
| Redirector gravitacional | GRAMO | 0,67 | 3 | 3 millones de dólares | 1 millón de dólares | 2 | 4 | 6 | 8 | 10 | 12 | 16 | - | - |
| Compresor espacial | T | 2.0 | 4 | 1,5 millones de dólares | $200 mil | 3 | 6 | 9 | 12 | 15 | 18 | 20 | - | - |

**Tecnología**: El tipo de tecnología necesaria para construir un motor de este tipo.
**Potencia**: La cantidad de puntos de energía requeridos por cada punto del casco asignado a este motor. Por ejemplo, una antorcha de fusión de 30 puntos de casco requiere 10 puntos de alimentación para funcionar.
**Tamaño mínimo**: El número más pequeño de puntos de casco que se pueden asignar a este sistema.
**Costo base**: El costo de la instalación de un motor de este tipo.
**Costo/Casco**: El costo PER del punto de casco asignado a este motor; acumulable con el costo base.
**Clasificación de aceleración en...**: La aceleración del barco para una instalación que comprende entre el 5 y el 50 % de su casco total. Por ejemplo, un barco de 100 puntos de casco con 20 puntos de casco de motor de inducción posee una aceleración de 4.
**Eff.**: La eficiencia de combustible del motor. Un único punto de casco dedicado al combustible impulsa un motor de un solo punto de casco durante tantos días de funcionamiento continuo.
**Costo**: El costo PER punto de casco dedicado al combustible para este tipo de motor.

### Descripciones del sistema del motor

No todos los motores son iguales. Los motores de baja tecnología pueden necesitar horas, días o semanas de aceleración continua para alcanzar una velocidad que un motor de alta tecnología puede igualar en cuestión de dos o tres fases. Cuando seleccionas un sistema de motor para tu nave estelar, registra la clasificación de aceleración del motor en la hoja de registro de tu nave y asigna los motores a una o más ubicaciones de impacto. Consulte la última parte del capítulo para obtener más información.

**Vela de fotones (PL 6)**
Este dispositivo es una estructura de lámina inmensa pero increíblemente frágil de sólo unas pocas moléculas de espesor. Utiliza la ligera presión de una estrella cercana o una estación de accionamiento láser como fuerza motriz. Sus tasas de aceleración caen en un 50% si la nave está a más de 5 AU de distancia de la estrella del sistema. La vela puede naufragar con el menor daño, pero cada barco equipado con una vela de fotones lleva al menos tres repuestos. Desafortunadamente, se necesitan horas para guardar o desplegar una vela.

| Control de tripulación | Crítico. Fracaso | Fracaso | Ordinario | Bueno | Asombroso |
|---|---|---|---|---|---|
| Implementación | d4+1 días | 3d4 horas | 2d4 horas | 1d4 horas | 1 hora |

En Combate, cualquier impacto de arma destruye una vela de fotones desplegada e impide que el velero realice maniobras hasta que se pueda volver a desplegar la vela. El velero continuará su último rumbo y mantendrá su velocidad anterior hasta que vuelva a navegar. Dado que los barcos Armas de energía exclusivamente con velas no pueden cambiar de rumbo fácilmente, supongamos que todos los barcos de vela son de maniobrabilidad de Clase I. Es una idea de Bueno que un velero lleve un sistema de propulsión secundario, como un pequeño motor de iones o un cohete, para maniobras de emergencia y navegación contra el sol. Las velas de fotones son completamente inútiles en la atmósfera; de hecho, la entrada atmosférica las destruye instantáneamente. La mayoría de los veleros llevan un pequeño sistema de propulsión de respaldo para realizar maniobras precisas.

**Propulsor planetario (PL 6)**
Varios sistemas de motores PL 6 son inútiles o peligrosos en cualquier tipo de atmósfera. El propulsor planetario es un sistema de motor de respaldo diseñado específicamente para usarse cuando los motores principales de la nave deben apagarse para realizar un aterrizaje planetario. Las variedades más comunes son el scramjet, el cohete químico o el perfil aerodinámico Armas de energía. La forma exacta no importa. El propulsor planetario requiere combustible o energía, pero no ambos. Puedes optar por instalar un tanque de combustible estándar o asegurarte de que la nave tenga suficiente energía disponible para hacer funcionar un propulsor planetario cuando sea necesario.

**Antorcha de fusión (PL 6)**
Este motor es básicamente un reactor de fusión al que le falta una pared de la botella magnética; El escape es plasma increíblemente caliente. La antorcha de fusión está destinada a trabajos únicamente en el espacio; su corriente de escape escoriaría cualquier cosa sobre la que aterrizara e incineraría todo lo que se encontrara a unos cientos de metros de la zona cero. Muchas naves equipadas con cohetes de fusión llevan propulsores planetarios para trabajos atmosféricos o permanecen permanentemente en el espacio, utilizando lanzaderas para llegar a la superficie de un planeta. Su combustible es hidrógeno, fusionado en la cámara de reacción y expulsado en forma de plasma candente.

**Motor de iones (PL 6)**
El motor de iones utiliza energía para descomponer las moléculas de un material combustible para crear iones y luego los expulsa por medio de un impulsor magnético. No proporciona el potencial de empuje de la antorcha de fusión, pero consume mucho más combustible y su escape no es tan peligroso. Los motores de iones no funcionan en ningún tipo de atmósfera, por lo que la mayoría de las naves con este tipo de central eléctrica también llevan un propulsor planetario.

**Motor de impulso de partículas (PL 7)**
Esta es simplemente una versión mejorada del motor de iones PL 6. El impulso de partículas utiliza campos magnéticos para producir un flujo constante de partículas de alta energía y vectorizarlas para impulsarlas. A diferencia del motor de iones, el motor de impulso de partículas no requiere tanque de combustible. Su reacción es tan eficiente que la muy pequeña cantidad de materia presente en el espacio interplanetario o interestelar puede recolectarse a través de campos magnéticos débiles y convertirse en un medio de empuje.
El motor de impulso de partículas es capaz de entrar en la atmósfera. Causa algunos daños a cualquier superficie cercana a sus puertos de escape, pero no es mucho peor que un jetwash moderno.

> **Consejo de diseño: motores**
> Un motor que ocupe entre el 10 y el 20 por ciento de su casco es bastante razonable. Será casi imposible diseñar algo más que eso, a menos que estés construyendo un mensajero rápido especial con armamento y comodidades mínimos para la tripulación.

**Motor de inducción (PL 7)**
Sin duda, el mejor motor disponible en este o en cualquier nivel de progreso anterior, el motor de inducción utiliza gravedad artificial para proporcionar un empuje y una maniobrabilidad increíbles. El motor de inducción no requiere combustible y no produce gases de escape; es ideal para trabajos atmosféricos, orbitales o en el espacio profundo.

**Motor de flujo inercial (PL 8)**
Al controlar con precisión el nivel de energía cuántica de cada átomo de la nave simultáneamente, el motor de flujo inercial asume los estados inerciales necesarios para producir movimiento en cualquier dirección. En efecto, el piloto elige de un instante a otro qué vector poseerá a continuación la nave, y el motor de flujo inercial lo hace posible. Este motor no requiere combustible y es seguro para trabajos atmosféricos.

**Redirector Gravítico (PL 8)**
Un refinamiento del motor de inducción, el redirector gravítico cambia la gravedad ambiental en las proximidades de la nave para producir una fuerza motriz. Es más potente y más eficiente que el motor de inducción.

**Compresor espacial (PL 9)**
Uno de los motores más avanzados disponibles, el compresor espacial rodea la nave en un campo que "pliega" o "arruga" la estructura del espacio en la dirección que el piloto desea viajar. Esto da como resultado una serie continua de microsaltos en los que la nave entra y sale de la realidad, teletransportándose miles de veces por segundo. Dado que la nave no tiene velocidad intrínseca (está estacionaria mientras se teletransporta), el compresor espacial puede detenerse o cambiar instantáneamente la dirección y el vector de empuje sin realizar ninguna maniobra. Sin embargo, el motor aún necesita aumentar la velocidad cíclica para aumentar la frecuencia de sus microsaltos, por lo que acelera normalmente.
El compresor espacial requiere mucha potencia, pero nada de combustible. Es seguro para vuelos atmosféricos.

## Paso 5: unidad FTL

El término "FTL" significa más rápido que la luz. El propulsor FTL de una nave es el sistema de motor que le permite salir del universo einsteiniano y viajar a velocidades que facilitan los viajes interestelares. Con un motor FTL, un barco puede convertir un viaje de muchos años a velocidades inferiores a la de la luz en un viaje de meses, semanas, días o incluso horas. Obviamente, no todos los barcos necesitan estar equipados con un motor FTL. De hecho, el coste de la mayoría de los sistemas FTL significa que sólo se construirán con ellos las naves que necesiten capacidad FTL, incluso cuando la tecnología avance hasta el punto del comercio interestelar común.
Los barcos sin motor FTL aún pueden disfrutar de acceso a viajes FTL; Es posible que un barco grande con propulsión FTL remolque o transporte un barco subluz. Consulte “Instalaciones varias” para obtener información sobre las abrazaderas de acoplamiento.

**Salto de conducción (PL 6)**
El motor de salto se basa en un tipo de tecnología bastante Raro: la tecnología de transmisión de materia. Requiere una enorme cantidad de energía, hasta el punto de que el motor de salto en sí es un colosal dispositivo de fusión que obtiene la energía para su salto aniquilando cantidades masivas de combustible de hidrógeno en un solo salto. Por lo tanto, el motor de salto sólo requiere el 5 por ciento de los puntos del casco del barco, pero debe construirse con un tanque de combustible que pueda representar entre otro 5 y 50 por ciento del casco del barco. También se requiere una pequeña cantidad de energía a bordo (1 punto de energía PER en el casco dedicado a la maquinaria impulsora del salto) para controlar la maquinaria y dirigir el salto.
La distancia a la que un motor de salto puede teletransportarse en un salto depende de cuánta masa de la nave (es decir, los puntos del casco) se aniquila durante el salto. Por ejemplo, un barco de salto de 200 puntos de casco podría tener tanques de combustible con una capacidad de 60 puntos de combustible, es decir, el 30 por ciento del casco del barco. Podría eliminar 10 puntos de combustible del casco (5 por ciento del casco) para un salto de 1 año luz, o podría eliminar los 60 puntos de combustible para un salto de 6 años luz.
Dado que la mayoría de los barcos de salto utilizan la mayor parte o todo el combustible disponible en un salto, necesitan saltar a un punto en el que puedan repostar sus tanques. Obviamente, un sistema civilizado tendrá capacidad de abastecimiento de combustible, pero si no se puede comprar combustible, el barco de salto debe improvisar. El hidrógeno puede extraerse de los gigantes gaseosos, separarse del agua o extraerse en forma de hielo. Suponiendo que se dispone de una fuente adecuada de hidrógeno, se puede suponer que un barco necesita 1 día completo de abastecimiento de combustible. PER Se recolectan 10 puntos del casco. Consulte “Instalaciones varias”.
El motor de salto puede ejecutar un salto en cualquier momento que tenga suficiente combustible para hacerlo. Se necesitan 1d4 horas para hacer funcionar el motor y trazar el siguiente punto de salto, por lo que suele haber un pequeño retraso entre los saltos incluso si hay combustible disponible de inmediato.

**Pantalla de agujero de gusano (PL 6)**
En teoría, es posible que un objeto como una nave pase a través de un agujero de gusano (un túnel en el espacio producido por un evento espectacular como la creación de un agujero negro) y emerja a decenas, cientos o miles de años luz de su ubicación anterior. Sin embargo, el simple hecho de pasar a través de un agujero de gusano desencadena su colapso, lo que dificulta su uso como medio de viaje interestelar. La pantalla del agujero de gusano enmascara la masa de la nave estelar del agujero de gusano, manteniendo así el conducto abierto el tiempo suficiente para que la nave pase de un extremo al Otros. También protege al barco de las condiciones extremas en las proximidades del agujero de gusano.
La pantalla del agujero de gusano sólo permite el tránsito a lo largo de un agujero de gusano natural, lo que significa que un barco no puede elegir su destino; tiene que ir a donde lo lleve el agujero de gusano. (En algunas campañas, las redes de agujeros de gusano artificiales preexistentes pueden permitir llegar a un gran número de estrellas de esta manera). El dispositivo de pantalla requiere el 5 por ciento de los puntos del casco de la nave y 2 puntos de energía PER del casco dedicados al sistema. Un barco de 800 puntos de casco debe gastar 40 puntos de casco en la pantalla y un total de 80 puntos de energía para energizar el dispositivo. Entrar en un agujero de gusano es, en el mejor de los casos, una propuesta arriesgada, por lo que se necesitan 2d4 horas para realizar los cálculos de rumbo y las maniobras necesarias para iniciar el tránsito por un agujero de gusano una vez que la nave se encuentra en las proximidades del siguiente agujero de gusano por el que pretende saltar.

**Activador de puerta (PL 7)**
Este dispositivo simplemente controla un dispositivo de puerta de algún tipo, que funciona como un enorme teletransportador a otra puerta en otro lugar. No requiere mucha energía en comparación con los variadores Otros FTL porque la mayor parte del trabajo lo realiza la propia puerta. El activador de puerta requiere el 1 por ciento de los puntos de casco del barco (1 punto de casco PER 100 puntos de casco del barco) y 2 puntos de energía PER puntos de casco asignados al sistema. El barco que transita por la puerta llega automáticamente a la terminal Otros y no puede saltar a un lugar donde no existe ninguna puerta. La duración del tránsito puede ser instantánea o durar varias horas; Depende de la campaña del GM. Un dispositivo de puerta normalmente requiere algún tiempo de ciclo para acumular las increíbles energías necesarias para lanzar una nave a través de distancias interestelares. Nuevamente, esto depende del DJ, pero un período de 2d4 horas como tiempo mínimo de ciclo es razonable.

**Hiperimpulsor (PL 7)**
Este sistema de propulsión lanza la nave a una dimensión o realidad alternativa en la que el límite de velocidad de la luz no tiene sentido. Al igual que con el impulso de salto, es necesario calcular un destino antes de ingresar al hiperespacio. Esto requiere 1d4 (x) 10 minutos, o una prueba de habilidad Navegación (prueba de habilidad compleja de 4 Éxitos sin penalización, prueba de 10 minutos PER). Una vez que la nave realiza un salto hiperespacial, no puede cambiar de rumbo. Puede salir del hiperespacio en cualquier momento simplemente desconectando el hiperimpulsor, y puede haber dispositivos o fenómenos naturales que impidan los viajes al hiperespacio e impidan cualquier nave que pase por las proximidades.

### Tabla 5-5: Unidades FTL

| Motor | Tecnología | Pow | Tamaño mínimo | Costo Básico. | Costo/Casco | Aceleración @ 5% | @ 10% | @ 15% | @ 20% | @ 30% | @ 40% | @ 50% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Unidad de salto | T | 1 | 5 | 4 millones de dólares | 1 millón de dólares | - | var | - | - | - | - | - |
| Combustible gastado | - | - | - | - | $10 mil | 1 año | 2 años | 3 años | 4 años | 6 años | 8 años | 10 años |
| Pantalla de agujero de gusano | METRO | 2 | 1 | 1 millón de dólares | $200 mil | ** | - | - | - | - | - | - |
| Activador de puerta | T | 2 | 1 | $500 mil | $100 mil | ** | - | - | - | - | - | - |
| Hiperimpulsor | X | 3 | 4 | 5 millones de dólares | 2 millones de dólares | 1/día | 2/día | 3/día | 4/día | 5/día | 6/día | 7/día |
| Motor estelar | GRAMO | ! | 3 | 2 millones de dólares | 1 millón de dólares | var | - | - | - | - | - | - |
| Onda impulsora | GRAMO | ! | 2 | 3 millones de dólares | 1,5 millones de dólares | var | - | - | - | - | - | - |
| Unidad plegada espacial | T | 4 | 4 | 8 millones de dólares | 2 millones de dólares | - | prisionero de guerra | - | - | - | - | - |
| Impulso Psicoportivo | P | 1 | 10 | 6 millones de dólares | $200 mil | - | PEP | - | - | - | - | - |
| Impulso trascendente | P | 1 | 4 | 12 millones de dólares | $400 mil | - | PEP/hora | - | - | - | - | - |
| motor de deformación | X | 2 | 2 | 10 millones de dólares | 5 millones de dólares | 1/hora | 2/hora | 4/hora | 8/hora | 16/hora | 32/h | 64/h |

* El motor de salto requiere el 10 por ciento de los puntos del casco del barco. Su clasificación FTL varía según la cantidad de combustible gastado en un salto.
** La pantalla del agujero de gusano ocupa el 5 por ciento de los puntos del casco del barco; el activador de puerta se lleva el 1 por ciento. El rendimiento varía.
! El stardrive y el drivewave requieren una planta de energía con un reactor de masa. El rendimiento varía.
**Tecnología**: La tecnología necesaria para construir este sistema de propulsión.
**Pow**: La cantidad de energía requerida, punto de casco PER dedicado a este sistema.
**Tamaño mínimo**: La instalación de accionamiento más pequeña posible de este tipo, en puntos del casco.
**Costo base**: El costo de una instalación FTL de este tipo.
**Costo/Casco**: El costo del punto de casco PER asignado a esta unidad; acumulable con el costo base.
**Clasificación de aceleración en...**: La velocidad FTL del barco para una instalación que comprende entre el 5 y el 50 % de su casco total. Por ejemplo, una nave de 100 puntos de casco con 20 puntos de casco de hiperimpulsor viaja a 4 años luz PER día de viaje hiperespacial.

La velocidad FTL de un barco depende de qué parte del casco esté dedicada al sistema de hiperimpulsión, con un mínimo del 10 por ciento. Cada punto del casco gastado en el hiperimpulsor requiere 3 puntos de energía para activar el sistema. Por ejemplo, un barco de 300 puntos de casco tiene un hiperimpulsor de 45 puntos de casco, o el 15 por ciento del casco; esto requiere 135 puntos de energía para activarse y proporciona a la nave una velocidad de 2 años luz PER día de viaje en hiperimpulsor. No hay límite para la duración de un salto Otros que la simple pregunta de cuánto tiempo puede permanecer una nave en el hiperespacio sin actualizar sus provisiones. (El DJ puede imponer un límite de hipersalto PER de 1000 años luz a su discreción).

**Impulsión Psicoportiva (PL 7)**
La tecnología de impulso psicoportivo utiliza el poder de la mente para vencer las restricciones del tiempo y el espacio. El impulso psicoportivo funciona de manera muy parecida a un impulso de salto, excepto que en lugar de quemar combustible, quema puntos de energía psiónica (o PEP), como se muestra a continuación:

| Clase | Psi Energía PER LY |
|---|---|
| Pequeño | 3 PEP PER LY |
| Luz | 6 PEP PER LY |
| Medio | 10 PEP PER LY |
| Pesado | 15 PEP PER LY |
| Súper pesado | 25 PEP PER LY |

Múltiples personajes psiónicos pueden contribuir con PEP para aumentar el alcance del salto. Cada salto psicoportivo dura un día completo. Los personajes psiónicos recuperan sus puntos de energía psiónica normalmente después de usarlos en la entrada inicial al Otro Espacio. Calcular las probabilidades y energías del próximo salto requiere que un Personaje psiónico, el navegante, realice una compleja verificación de habilidades contra ESP-navcognition. El navegante requiere 4 Éxitos y puede realizar una prueba de habilidad cada diez minutos para preparar la nave para su próximo salto.
El propulsor psicoportivo requiere el 10 por ciento del casco del barco y utiliza 1 punto de potencia PER del casco dedicado al propulsor.

**Stardrive (PL 7)**
El impulso estelar crea una singularidad controlada y de corta duración que deja a la nave fuera del espacio normal y en el espacio impulsor, una dimensión paralela ligada al universo real. Todas las sumersiones en el espacio motriz duran 121 horas (aproximadamente cinco días). Un motor estelar debe estar acoplado a un reactor de masa; ningún sistema de energía Otros puede energizar un stardrive. Al igual que el hiperimpulsor o el impulsor de salto, una nave Armas de energía con un impulsor estelar debe trazar su salto con cuidado; no puede maniobrar una vez que ingresa al espacio impulsor y nada puede interferir con su progreso hasta que llega a su destino. La distancia base lograda por un stardrive en un solo salto se basa en la clase de nave:

| Clase | Base Lluvia de estrellas |
|---|---|
| Pequeño | 5 Ly |
| Luz | 10 Ly |
| Medio | 20 Ly |
| Pesado | 30 Ly |
| S-pesado | 50 Ly |

El stardrive requiere el 5 por ciento del casco de la nave y 3 puntos de energía PER del casco del sistema; por ejemplo, una nave de 80 puntos de casco requiere un motor estelar de 4 puntos de casco y 12 puntos de energía para hacer caer las estrellas. Es posible aumentar las distancias que se muestran arriba excediendo los requisitos de energía que se encuentran en la TABLA 5-5. Por cada 10 puntos de energía más allá del mínimo asignado al motor estelar, la nave puede caer en estrellas un año luz adicional. Por ejemplo, un acorazado de 1.000 puntos de casco necesita 150 de potencia para su propulsor estelar, pero si se le asignan 300 puntos de potencia, las estrellas caen hasta 45 años luz en lugar de 30 años luz.
El stardrive requiere varios días para recargarse después de un viaje espacial. Normalmente, se necesitan d4+1 días para recargar un motor estelar para la próxima caída de estrellas.

**Onda de conducción (PL 8)**
El generador de ondas motrices es simplemente una mejora del stardrive. Se parece al motor anterior en la mayoría de los detalles, excepto que la duración de la inmersión del espacio de transmisión es de solo 11 horas y el tiempo de recarga de la unidad es de solo d4+1 horas. Dado que circula mucho más rápido, puede cubrir territorio a un ritmo correspondientemente más rápido.

**Unidad Spacefold (PL 8)**
El mecanismo de plegado espacial “pliega el espacio”, haciendo posible que una nave salte decenas o cientos de años luz en un solo instante. El alcance del variador está determinado completamente por la cantidad de energía utilizada para alimentar el sistema, siempre que cumpla con los mínimos especificados en la TABLA 5-5. Por ejemplo, una nave de 200 puntos de casco debe asignar 20 puntos de casco al motor espacial, lo que requiere 120 puntos de energía. Siempre que la nave pueda generar 120 o más puntos de energía, puede realizar un plegado espacial de hasta un punto de energía PER de un año luz asignado al propulsor.
El impulso espacial puede realizar ciclos casi instantáneamente, pero crea tensiones peligrosas en la estructura del espacio; por seguridad, una nave debe viajar 5d20 (x) 10 AU (unidades astronómicas) desde su punto de llegada en el espacio normal antes de que sea seguro volver a utilizar el motor.

**Impulso trascendente (PL 9)**
El sistema de impulso trascendente aprovecha el poder de una persona con talento psiónico y desbloquea energías insondables con la clave de una mente inteligente. La unidad permite viajar a velocidades FTL en el espacio normal sin necesidad de realizar trazados ni cálculos cuidadosos. La velocidad de la nave es una cantidad de años luz PER hora igual a la puntuación de energía psiónica de un único Personaje psiónico que esté volando la nave en un momento dado. Un Personaje psiónico que impulsa el impulso trascendente aunque sea por un momento gasta inmediatamente todos sus puntos de energía psiónica. Puede permanecer “en la silla” hasta ocho horas antes de agotarse. Puede comenzar a recuperar puntos de energía psiónica normalmente después de levantarse de la silla.

Ejemplo: Jaleel es un caminante mental frágil con 18 puntos de energía psiónica. Si toma el timón de una nave equipada con un motor trascendente, la nave viajará a una velocidad de 18 años luz PER hora hasta que Jaleel se quede sin vapor, momento en el que otro Personaje psiónico podría tomar el control. Los grandes barcos de este tipo suelen tener pequeños equipos de pilotos-timoneles que pueden rotar las tareas de pilotaje.
El impulso trascendente requiere el 10 por ciento de los puntos del casco del barco y una modesta cantidad de energía.

**Motor warp (PL 9)**
Al crear un campo warp en el que se suspenden las leyes normales de Física, el motor warp permite el viaje FTL. El campo warp no interfiere con la capacidad de una nave para recopilar información de su entorno, y una nave que viaja con motor warp puede cambiar de rumbo, detenerse o comenzar de nuevo a voluntad, siempre que haya energía disponible para el motor.
Al igual que el hiperimpulsor, la velocidad del motor warp se mide en el número de años luz que puede cruzar PER hora de funcionamiento. Una nave de 100 puntos de casco que dedica 15 puntos de casco a su motor warp ha asignado el 15 por ciento del casco al motor, por lo que puede viajar a una velocidad de 4 años luz PER hora.