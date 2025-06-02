---
marp: true
theme: default
class: lead
paginate: true
math: mathjax
title:  Formación de Equipos Multiples
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
## Multiple Team Formation Problem
Ignacio Martínez

---

## Introducción al Problema

- Asignar individuos a proyectos considerando:  
  - Requerimientos mínimos de habilidades  
  - Afinidades sociales entre individuos  
  - Prioridades de proyectos

- Objetivo: maximizar la eficiencia social y técnica en la formación de equipos.

---


## Contexto y Simplificaciones

- **Contexto Real**:
  - Diversidad de habilidades y disponibilidad.
  - Interacciones sociales (positivas, negativas, neutras) evolucionan.
  - Proyectos independientes con requerimientos mínimos.

- **Suposiciones del Modelo**:
  - Cada persona tiene una única habilidad principal.
  - Asignación parcial a varios proyectos.
  - Afinidad social entre individuos es estática.

---

- **Simplificaciones**:
  - No se consideran múltiples habilidades por persona.
  - Sin restricciones económicas ni dependencias entre proyectos.
  - La matriz de afinidad social se mantiene fija.

- **Importancia de los Proyectos**:
  - Cada proyecto tiene un peso que refleja su prioridad o relevancia.

---

## Definición Formal del Problema (MTFP)

### Conjuntos

- **$\mathcal{H} = \{1, \ldots, h\}$**: Conjunto de individuos disponibles para asignar a proyectos.

- **$\mathcal{P} = \{1, \ldots, p\}$**: Conjunto de proyectos que requieren equipos.

- **$\mathcal{K} = \{1, \ldots, k\}$**: Conjunto de habilidades disponibles.

- **$Q_a \subseteq \mathcal{H}$**: Subconjunto de individuos que poseen la habilidad $a \in \mathcal{K}$.

---

## Parámetros del Modelo

- **Afinidad social ($s_{ij}$)**: 
  - Valor que indica la relación entre individuos $i$ y $j$:
    - **1**: Colaboración positiva.
    - **0**: Relación neutral o sin interacción.
    - **-1**: Conflicto o afinidad negativa.
  - Este parámetro es fundamental para maximizar la afinidad social en los equipos.


---

- **Requerimientos ($r_{al}$)**: 
  - Representa el número mínimo de personas con habilidad $a$ requerido para el proyecto $l$. 
  - Se expresa como un número entero positivo ($\mathbb{Z}^+$) y asegura que haya suficiente personal especializado para cumplir con las necesidades del proyecto.

- **Peso de proyecto ($w_l$)**: 
  - Valor que refleja la prioridad relativa de cada proyecto, donde $w_l \in [0,1]$ y $\sum w_l = 1$.
  - Este peso es crucial para orientar la asignación de recursos hacia proyectos más estratégicos o urgentes.

---

## Variables y Función Objetivo

- **Variables de decisión ($x_{il}$)**: 
  - Representa la fracción del tiempo que el individuo $i$ está asignado al proyecto $l$, donde $x_{il} \in [0,1]$.
  - Permite modelar la asignación fraccionaria de recursos, reflejando la disponibilidad y el compromiso de cada individuo.

- **Función objetivo**:
$$
\max E = \sum_{l \in \mathcal{P}} w_l \cdot \frac{1}{2}\left(1 + \frac{\sum_{i \neq j} s_{ij} x_{il} x_{jl}}{\left(\sum_{a} r_{al}\right)^2}\right)
$$
  - Esta función busca maximizar la eficiencia ponderada de todos los proyectos, considerando tanto la cohesión social como el tamaño del equipo.

---

## Explicaciones

- **Normalización por $\left(\sum_{a} r_{al}\right)^2$**: 
  - Asegura que la eficiencia sea comparable entre proyectos de diferentes escalas, penalizando sobreasignaciones y promoviendo equipos balanceados.

- **Imposibilidad de $e_l = 100\%$**: 
  - Es imposible alcanzar 100% debido a la penalización por sobreasignación y la estructura del modelo.

- **Interpretación de $e_l$**:
  - **$e_l > 100\%$**: Indica sobreasignación con alta sinergia.
  - **$e_l < 50\%$**: Refleja conflictos o baja cohesión en el equipo.

---

## Restricciones del Modelo

1. Capacidad:  
$$
\sum_l x_{il} \leq 1 \quad \forall i \in \mathcal{H}
$$  
(individuos no pueden asignarse más del 100% de su tiempo)

2. Requerimientos:  
$$
\sum_{i \in Q_a} x_{il} \geq r_{al} \quad \forall a \in \mathcal{K}, l \in \mathcal{P}
$$  

---

## Requerimientos: Enteros vs Fraccionales

- **Diseño original:** $r_{al}$ son enteros, ej. 2 personas Backend.  

- **En la práctica:**  
  - Modelo asigna $x_{il} \in [0,1]$, permitiendo fracciones de personas.  
  - Esto implica que la suma de fracciones puede cumplir el requisito mínimo.  
  - Interpretación: carga o tiempo asignado, no individuos enteros estrictos.  

- **Importante:** Esta reinterpretación fue inesperada pero válida para el modelo y mejora flexibilidad.

---

## Métrica de Eficiencia por Proyecto

$$
e_l = \frac{1}{2}\left(1 + \frac{\sum_{i,j} s_{ij} x_{il} x_{jl}}{\left(\sum_a r_{al}\right)^2}\right) \times 100\%
$$

| Valor | Significado                         |
| ----- | ----------------------------------- |
| 100%  | Equipo ideal (No factible)          |
| >100% | Sobreasignación con eficiencia alta |
| <50%  | Conflictos y baja cohesión          |

---

## Implementación Técnica

- Modelado con Pyomo (Python)  
- Optimización con IPOPT (solver no lineal)  
- Generadores de datos para instancias controladas y pruebas

---

## Resultados

- Se evaluó el modelo en casos de prueba de distintos tamaños y complejidad:
  - Casos pequeños (validación): eficiencia global alta, asignaciones balanceadas.
  - Casos medianos y grandes: eficiencia disminuye levemente, pero se mantienen tiempos de cómputo bajos (< 2 s).
- Ejemplo de resultados:
  - Eficiencia global varía entre 54% y 87% en escenarios realistas.
  - En casos de sobreasignación, la métrica puede superar el 100% (ej: 216%).
- El modelo es robusto ante requerimientos fraccionarios y distribuciones desiguales de habilidades.

---


| Caso | Pers. | Proy. | Req. Totales | Efic. Global | Tiempo (s) | Observaciones         |
| ---- | ----- | ----- | ------------ | ------------ | ---------- | --------------------- |
| 1    | 4     | 2     | 4            | 87.5%        | 2.38       | Asignación balanceada |
| 2    | 6     | 1     | 3            | 216.67%      | 0.08       | Sobreasignación       |
| 3    | 4     | 1     | 2            | 37.5%        | 0.08       | Afinidad negativa     |
| 4    | 5     | 2     | 6            | 89.72%       | 0.09       | Variación en pesos    |
| 5    | 10    | 2     | 16           | 63.13%       | 0.09       | Incremental pequeño   |
| 6    | 20    | 3     | 36           | 81.60%       | 0.12       | Incremental mediano   |
| 7    | 30    | 4     | 64           | 76.39%       | 0.54       | Incremental grande    |
| 8    | 40    | 3     | 48           | 70.37%       | 0.20       | Incremental mayor     |
| 9    | 50    | 3     | 48           | 65.17%       | 0.39       | Incremental extremo   |
| G1   | 100   | 10    | 160          | 58.20%       | 18.37      | Caso grande           |
| G2   | 200   | 20    | 320          | 54.10%       | 767.11     | Caso muy grande       |


---

## Conclusión

- El modelo mantiene tiempos de solución bajos incluso en instancias grandes.
- La métrica penaliza sobreasignación y premia cohesión social.
- Valores >100% reflejan equipos sobredimensionados, no errores.
- Soporta requerimientos fraccionarios (media jornada, etc.).
- Permite priorizar proyectos mediante pesos.
- No considera múltiples habilidades por persona ni restricciones económicas.
- La afinidad social es estática y no evoluciona.
- Útil para planificación flexible y rápida de equipos multidisciplinarios en organizaciones.
