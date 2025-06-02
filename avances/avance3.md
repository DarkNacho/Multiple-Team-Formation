---
marp: true
theme: default
class: lead
paginate: true
math: mathjax
title:  Formación de Equipos Multiples (MINLP)
author: Ignacio Martínez
style: |
  .header {
    position: absolute;
    top: 10px;
    right: 10px;
    height: 60px;
  }
  section {
    background-image: url('utalca.png');
    background-position: top right;
    background-repeat: no-repeat;
    background-size: 400px;
    padding-top: 30px;
  }
---

# Formación de Equipos Multiples (MTFP) con Sociometría
## Modelo MINLP para Asignación Discreta
Ignacio Martínez

---

## Introducción al Problema

- Asignar individuos a proyectos considerando:  
  - Requerimientos mínimos de habilidades  
  - Afinidades sociales entre individuos  
  - Prioridades de proyectos

- Objetivo: maximizar la eficiencia social y técnica en la formación de equipos.
- **Novedad**: Modelo evolucionó a Programación No Lineal Entera Mixta (MINLP) para asignaciones de tiempo discretas.

---

## Contexto y Simplificaciones

- **Contexto Real**:
  - Diversidad de habilidades y disponibilidad.
  - Interacciones sociales (positivas, negativas, neutras) evolucionan.
  - Proyectos independientes con requerimientos mínimos.

- **Suposiciones del Modelo**:
  - Cada persona tiene una única habilidad principal.
  - **Asignación parcial a varios proyectos en fracciones discretas (e.g., 0%, 50%, 100%).**
  - Afinidad social entre individuos es estática.

---

- **Simplificaciones**:
  - No se consideran múltiples habilidades por persona.
  - Sin restricciones económicas ni dependencias entre proyectos.
  - La matriz de afinidad social se mantiene fija.

- **Importancia de los Proyectos**:
  - Cada proyecto tiene un peso que refleja su prioridad o relevancia.

---

## Definición Formal del Problema (MTFP - MINLP)

### Conjuntos

- **$\mathcal{H} = \{1, \ldots, h\}$**: Conjunto de individuos disponibles.
- **$\mathcal{P} = \{1, \ldots, p\}$**: Conjunto de proyectos que requieren equipos.
- **$\mathcal{K} = \{1, \ldots, k\}$**: Conjunto de habilidades disponibles.
- **$Q_a \subseteq \mathcal{H}$**: Subconjunto de individuos que poseen la habilidad $a \in \mathcal{K}$.
- **$\mathcal{D}$**: Conjunto de fracciones de tiempo discretas permitidas para la asignación (e.g., $\{0.0, 0.5, 1.0\}$).


---

## Parámetros del Modelo

- **Afinidad social ($s_{ij}$)**: 
  - Valor que indica la relación entre individuos $i$ y $j$:
    - **1**: Colaboración positiva.
    - **0**: Relación neutral o sin interacción.
    - **-1**: Conflicto o afinidad negativa.

- **Requerimientos ($r_{al}$)**: 
  - Cantidad mínima de dedicación (en personas equivalentes a tiempo completo) con habilidad $a$ requerida para el proyecto $l$. $r_{al} \in \mathbb{R}_{\ge 0}$.

- **Peso de proyecto ($w_l$)**: 
  - Valor que refleja la prioridad relativa de cada proyecto, $w_l \in [0,1]$ y $\sum_{l \in \mathcal{P}} w_l = 1$.
---

## Variables de Decisión

  
  - $x_{il}$: Fracción del tiempo del individuo $i$ asignada al proyecto $l$. 

  - $y_{ild} \in \{0,1\}$: Variable binaria. Es 1 si al individuo $i$ se le asigna la fracción de tiempo $d \in \mathcal{D}$ para el proyecto $l$, y 0 en caso contrario.



---

## Función objetivo

Maximizar la eficiencia global ponderada $E$.
$$
\max E = \sum_{l \in \mathcal{P}} w_l \cdot e_l
$$


Donde la eficiencia del proyecto $l$, $e_l$, es:
$$
e_l = \frac{1}{2}\left(1 + \frac{\sum_{i \in \mathcal{H}}\sum_{j \in \mathcal{H}} s_{ij} x_{il} x_{jl}}{\left(\sum_{a \in \mathcal{K}} r_{al}\right)^2}\right)
$$


---
## Explicaciones de la Métrica $e_l$

- **Normalización por $\left(\sum_{a \in \mathcal{K}} r_{al}\right)^2$**: 
  - Permite comparar la cohesión social entre proyectos de diferentes tamaños (total de requerimientos).
  - Penaliza la dispersión de esfuerzos si el denominador es grande.
  

---

- **Interpretación de $e_l$ (eficiencia del proyecto)**:
  - $e_l \approx 1$ (o $100\%$): Cohesión social positiva ideal (todas las interacciones $s_{ij}$ son positivas y maximizadas).
  - $e_l > 0.5$ (o $>50\%$): Predominan afinidades positivas.
  - $e_l = 0.5$ (o $50\%$): Cohesión neutra (afinidades se cancelan o son cero).
  - $e_l < 0.5$ (o $<50\%$): Predominan afinidades negativas, indicando conflictos.
  - $e_l \approx 0$ (o $0\%$): Conflicto social máximo (todas las interacciones $s_{ij}$ son negativas y maximizadas).

---

## Restricciones del Modelo

1.  **Capacidad individual**:  
    $$ \sum_{l \in \mathcal{P}} x_{il} \leq 1 \quad \forall i \in \mathcal{H} $$  

El tiempo total asignado de un individuo no excede su disponibilidad total

2.  **Requerimientos de habilidad por proyecto**:  
    $$ \sum_{i \in Q_a} x_{il} \geq r_{al} \quad \forall a \in \mathcal{K}, \forall l \in \mathcal{P} $$  

Se cumple el mínimo de dedicación requerida por habilidad en cada proyecto

---

3.  **Asignación de fracción de tiempo única**:
    $$ \sum_{d \in \mathcal{D}} y_{ild} = 1 \quad \forall i \in \mathcal{H}, \forall l \in \mathcal{P} $$

Para cada individuo y proyecto, se selecciona exactamente una fracción de tiempo $d$ del conjunto $\mathcal{D}$

4.  **Definición de $x_{il}$ a partir de $y_{ild}$**:
    $$ x_{il} = \sum_{d \in \mathcal{D}} d \cdot y_{ild} \quad \forall i \in \mathcal{H}, \forall l \in \mathcal{P} $$

Vincula la variable de asignación fraccionaria $x_{il}$ con la decisión binaria $y_{ild}$

---

## Consideraciones

- **Requerimientos ($r_{al}$)**: Pueden ser fraccionarios (e.g., se necesitan 1.5 personas con habilidad Backend).

- **Asignaciones ($x_{il}$)**: 
  - El modelo ahora asigna $x_{il}$ tomando valores de un conjunto discreto $\mathcal{D}$ (e.g., $\{0, 0.5, 1.0\}$) mediante las variables binarias $y_{ild}$.
  - La suma de estas asignaciones discretas $\sum_{i \in Q_a} x_{il}$ debe cumplir con el requerimiento $r_{al}$.
  - Interpretación: Carga o tiempo asignado en fracciones de dedicación predefinidas y realistas.

- **Impacto**: La introducción de $y_{ild}$ y $\mathcal{D}$ transforma el problema en un **Modelo de Programación No Lineal Entera Mixta (MINLP)**, lo que aumenta el realismo de las asignaciones pero también la complejidad.

---

## Métrica de Eficiencia por Proyecto ($e_l$)

$$
e_l = \frac{1}{2}\left(1 + \frac{\sum_{i \in \mathcal{H}}\sum_{j \in \mathcal{H}} s_{ij} x_{il} x_{jl}}{\left(\sum_{a \in \mathcal{K}} r_{al}\right)^2}\right)
$$
(Se puede multiplicar por $100\%$ para visualización porcentual)

| Valor ($e_l \times 100\%$) | Significado General                             |
| -------------------------- | ----------------------------------------------- |
| $\approx 100\%$            | Cohesión social positiva ideal                  |
| $> 50\%$                   | Predominio de afinidades positivas              |
| $= 50\%$                   | Cohesión social neutra / Balanceada             |
| $< 50\%$                   | Predominio de afinidades negativas / Conflictos |
| $\approx 0\%$              | Conflicto social máximo                         |

---

## Implementación Técnica

- Modelado con **Pyomo** (Python).
- Optimización con **Bonmin** (solver para MINLP).
  - Bonmin es adecuado para problemas de optimización no lineal entera mixta.
- Generadores de datos para instancias controladas y pruebas.
- El cambio a fracciones de tiempo discretas ($x_{il} \in \mathcal{D}$) es la razón principal para usar un solver MINLP.

---

## Resultados Iniciales y Pruebas Fundamentales

Se han realizado pruebas iniciales para validar el comportamiento del modelo MINLP bajo diferentes condiciones controladas. Estas pruebas utilizaron un escenario base consistente (4 personas, 2 proyectos, requerimientos definidos) y se enfocaron en dos aspectos principales:


---

<br><br>

Se evaluó el modelo con el conjunto de fracciones de tiempo $\mathcal{D} = \{0.0, 1.0\}$.

*   Variaciones en la matriz de afinidad social:
    *   **Ideal:** Todas las afinidades positivas ($s_{ij}=1$). Resultó en una eficiencia global del 100%. 
    *   **Negativa:** Todas las afinidades negativas ($s_{ij}=-1$). Resultó en una eficiencia global del 0%. 
    *   **Neutra:** Todas las afinidades neutras ($s_{ij}=0$). Resultó en una eficiencia global del 50%. 
    *   **Alterna:** Mezcla de afinidades positivas y negativas. Resultó en una eficiencia global del 50%. 
*   Estos resultados confirman que el modelo responde 

---

**Impacto de la Granularidad de las Fracciones de Tiempo (con Afinidad Ideal):**

*   Manteniendo una matriz de afinidad ideal ($s_{ij}=1$ para todos).
    *   Se probaron diferentes conjuntos $\mathcal{D}$:
        *   $\mathcal{D} = \{0.0, 0.5, 1.0\}$: Eficiencia global del 100%.
        *   $\mathcal{D} = \{0.0, 0.25, 0.5, 0.75, 1.0\}$: Eficiencia global del 100%. 
*   Esto sugiere que, en condiciones sociales ideales, el modelo puede aprovechar eficazmente una mayor granularidad en las asignaciones de tiempo sin pérdida de eficiencia.

---

| Caso de Prueba        | Fracciones de Tiempo | Asignaciones Proyecto 1    | Asignaciones Proyecto 2    |
| :-------------------- | :------------------- | :------------------------- | :------------------------- |
| **Afinidad Ideal**    | $\{0.0, 1.0\}$       | P0 (B): 100%, P3 (F): 100% | P1 (B): 100%, P2 (F): 100% |
| **Afinidad Negativa** | $\{0.0, 1.0\}$       | P1 (B): 100%, P2 (F): 100% | P0 (B): 100%, P3 (F): 100% |
| **Afinidad Neutra**   | $\{0.0, 1.0\}$       | P1 (B): 100%, P3 (F): 100% | P0 (B): 100%, P2 (F): 100% |

---

| Caso de Prueba           | Fracciones de Tiempo            | Asignaciones Proyecto 1                        | Asignaciones Proyecto 2                        |
| :----------------------- | :------------------------------ | :--------------------------------------------- | :--------------------------------------------- |
| **Afinidad Alterna**     | $\{0.0, 1.0\}$                  | P0 (B): 100%, P3 (F): 100%                     | P1 (B): 100%, P2 (F): 100%                     |
| **Ideal Fraccionario 1** | $\{0.0, 0.5, 1.0\}$             | P0(B):50%, P1(B):50% <br> P2(F):50%, P3(F):50% | P0(B):50%, P1(B):50% <br> P2(F):50%, P3(F):50% |
| **Ideal Fraccionario 2** | $\{0.0, 0.25, 0.5, 0.75, 1.0\}$ | P0(B):50%, P1(B):50% <br> P2(F):50%, P3(F):50% | P0(B):50%, P1(B):50% <br> P2(F):50%, P3(F):50% |


---
## Conclusión 

- El modelo ha evolucionado a un **MINLP** para permitir asignaciones de tiempo más realistas (fracciones discretas).
- La métrica de eficiencia $e_l$ sigue buscando un balance entre cohesión social y cumplimiento de requerimientos.
- El uso del solver Bonmin es crucial para abordar la naturaleza MINLP.
- El modelo sigue siendo una herramienta útil para la planificación inicial de equipos.

---

## Posibles Trabajo Futuro

- **Múltiples Habilidades por Individuo**:
  - Permitir que cada persona $i \in \mathcal{H}$ pueda poseer un conjunto de habilidades $\mathcal{K}_i \subseteq \mathcal{K}$.
  - Modificar la restricción de requerimientos para considerar esto.

- **Relajación del Modelo para Infactibilidad**:
  - Investigar técnicas para obtener soluciones "cercanas" cuando el modelo es infactible.
  - Por ejemplo, permitir violaciones suaves de ciertas restricciones con penalizaciones en la función objetivo.
    - Permitir que un proyecto no sea completado en requerimientos de habilidad.
