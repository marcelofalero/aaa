+++
title = "Armamento"
weight = 2
toc = true
+++

{{< quick-nav >}}

## Reglas de Combate de Armamento

### Modificadores de ataque de armamento a distancia
Cuando un personaje usa cualquier arma a distancia, ya sea primitiva o moderna, se deben considerar varios factores para determinar el dado de situación de la tirada de habilidad:
- El dado de situación base del arma (+4 para la habilidad amplia o +0 para la especialidad).
- El modificador de distancia del arma (véase la **TABLA P22: MODIFICADORES DE DISTANCIA POR TIPO DE ARMA** abajo).
- Cualquier modificador por la resistencia de Destreza del objetivo (bonificación de –1 paso para DES 11–12, –2 pasos para DES 13–14, –3 pasos para DES 15–16, –4 pasos para DES 17–18 y –5 pasos para DES 19 o más).

#### TABLA: MODIFICADORES COMUNES DE ATAQUE A DISTANCIA
| Condición | Modificador | Tipos de Arma | Nota |
| :--- | :--- | :--- | :--- |
| **Alcance Cero** (0–1m) | **-3 pasos** | Pistola, Subfusil, Escopeta | El arma debe ser lo suficientemente corta para un forcejeo. |
| **A bocajarro** (1–4m) | **-1 paso** | Todas | Véase beneficios de rango de especialidad para mejoras. |
| **En lucha cuerpo a cuerpo** | **+1 paso** | Todas | Cancelado por el entrenamiento de la habilidad de **Combate cuerpo a cuerpo**. |
| **En movimiento** | **+1 paso** | Todas | Para disparar mientras se corre o se mueve rápido. |
| **Cambiar cargador** | **+2 pasos** | Todas | Para cambiar el cargador y disparar en la misma fase. |

#### TABLA P22: MODIFICADORES DE DISTANCIA POR TIPO DE ARMA
| Arma | Corta | Media | Larga |
| :--- | :--- | :--- | :--- |
| Subfusil | -1 paso | +1 paso | +2 pasos |
| Pistola | -1 paso | +1 paso | +2 pasos |
| Fusil | -1 paso | Nada | +1 paso |

### Modos de ataque de armamento automático
Los subfusiles, fusiles de asalto y algunas armas pesadas proporcionan a un personaje hasta tres opciones de ataque por fase de acción:

- **Disparar:** Un solo ataque a un solo objetivo. (Control estándar + dado de situación).
- **Ráfaga:** Una lluvia de munición dirigida a un solo objetivo. El personaje recibe una **bonificación de –1 paso** a su tirada de habilidad. En caso de fallo crítico, el arma se encasquilla y requiere una prueba de Ciencia técnica—reparación para desatascarla.
- **Fuego automático:** Una ráfaga de munición barrida sobre un área amplia. Se pueden ver afectados hasta tres objetivos diferentes a menos de 6 metros entre sí.
  - Para resolver el fuego automático, el jugador tira un dado de control y tres dados de situación a la vez.
  - Los resultados se leen del dado de control, modificados por los dados de situación individuales: **+1 paso** para el primer objetivo, **+2 pasos** para el segundo y **+3 pasos** para el tercero.


## Armamento cuerpo a cuerpo

{{< json-table "weapons" "melee" >}}

## Armamento a distancia

{{< json-table "weapons" "ranged" >}}

## Armamento pesado

Cada armamento pesado tiene un conjunto de cifras de alcance. Los modificadores de los dados de situación para el alcance, como se muestra a continuación en la **TABLA P21: MODIFICADORES DE ALCANCE DE ARMAMENTO PESADO**, pueden aplicarse cuando se usa un cierto tipo de armamento pesado contra un objetivo o una ubicación que se encuentre dentro de una categoría de alcance particular. Además, la precisión de un armamento de fuego indirecto depende del alcance entre el tirador y la ubicación del objetivo, así como del tipo de éxito logrado, como se muestra en la [**TABLA P20: PRECISIÓN POR ALCANCE**]({{< relref "skills/athletics/_index.es.md#accuracy-by-range" >}}). Algunos armamentos pesados de fuego directo (así como algunos rifles y todas las metralletas) son [**armamentos automáticos**]({{< relref "skills/modern-ranged-weapons/_index.es.md#automatic-weapon-attack-modes" >}}) capaces de disparar múltiples rondas de munición en cada ataque.

#### TABLA P21: MODIFICADORES DE ALCANCE DE ARMAMENTO PESADO
| Alcance | Directo | Indirecto |
| :--- | :--- | :--- |
| **Corto** | -1 paso | +2 pasos |
| **Medio** | Ninguno | -2 pasos |
| **Largo** | +1 paso | Ninguno |

{{< json-table "weapons" "heavy" >}}

## Munición

{{< json-table "weapons" "ammunition" "platform" "payload" "cost" >}}

## Accesorios

{{< json-table "weapons" "accessories" "platform" "mass" "cost" >}}
