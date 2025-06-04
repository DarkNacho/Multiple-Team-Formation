| #   | Caso de Prueba (Archivo JSON)            | Personas (N) | Proyectos (M) | Habilidades (K) | Fracciones Tiempo (TF) | Espacio Búsqueda (TF<sup>N\*M</sup>) | Brute Force: Eficiencia Global | Brute Force: Tiempo (s) | Brute Force: Soluciones Válidas | Pyomo (Bonmin): Eficiencia Global | Pyomo (Bonmin): Tiempo (s) | ¿Coinciden Eficiencia? | Detalle Coincidencia                                               |
| --- | ---------------------------------------- | ------------ | ------------- | --------------- | ---------------------- | ------------------------------------ | ------------------------------ | ----------------------- | ------------------------------- | --------------------------------- | -------------------------- | ---------------------- | ------------------------------------------------------------------ |
| 1   | [`minimal.json`](./minimal.json)         | 2            | 1             | 2               | 3                      | 9                                    | 75.00%                         | 0.00                    | 1                               | 75.00%                            | 0.09                       | Sí                     | Eficiencia y Asignación Idénticas                                  |
| 2   | [`manual.json`](./manual.json)           | 3            | 2             | 2               | 3                      | 729                                  | 85.00%                         | 0.01                    | 3                               | 85.00%                            | 0.09                       | Sí                     | Misma Eficiencia, Distinta Asignación (Múltiples Óptimos Globales) |
| 3   | [`medium_case.json`](./medium_case.json) | 4            | 3             | 3               | 3                      | 531,441                              | 84.86%                         | 3.05                    | 4                               | 84.86%                            | 0.09                       | Sí                     | Eficiencia y Asignación Idénticas                                  |
| 4   | [`complex.json`](./complex.json)         | 5            | 3             | 3               | 3                      | 14,348,907                           | 84.86%                         | 76.02                   | 16                              | 84.86%                            | 0.11                       | Sí                     | Eficiencia y Asignación Idénticas                                  |
| 5   | [`complex2.json`](./complex2.json)       | 6            | 3             | 3               | 3                      | 387,420,489                          | 76.39%                         | 2698.17                 | 64                              | 76.39%                            | 0.11                       | Sí                     | Misma Eficiencia, Distinta Asignación (Múltiples Óptimos Globales) |
| 6   | [`complex3.json`](./complex3.json)       | 6            | 3             | 3               | 3                      | 387,420,489                          | 77.78%                         | 2334.29                 | 64                              | 77.78%                            | 0.12                       | Sí                     | Misma Eficiencia, Distinta Asignación (Múltiples Óptimos Globales) |


---

### **Test Case 1: [`minimal.json`](./minimal.json)**


**Instance Details (from Brute Force Log):**
*   Personas: 2, Proyectos: 1, Fracciones de Tiempo: 3
*   Habilidades disponibles: \['S1', 'S2']
*   Habilidades de las personas: Persona 0: S1, Persona 1: S2
*   Proyecto 0 (peso 1.00) requerimientos: {'S1': 0.5, 'S2': 0.5}
*   Matriz de Afinidad:
    ```
         00  01
    00   1   0
    01   0   1
    ```
*   Fracciones de Tiempo: \[0.0, 0.5, 1.0]

**Resultados de la Fuerza Bruta:**
*   Eficiencia Global Óptima: **0.7500**
*   Total combinaciones verificadas: 9
*   Asignaciones válidas encontradas: 1
*   Tiempo de ejecución: 0.00 segundos
*   **Proyecto 1 (Peso: 100.00%)**
    *   Requerimientos: S1: 0.5, S2: 0.5
    *   Equipo Asignado: Persona 0 (S1): 0.50, Persona 1 (S2): 0.50
    *   Suministro total: S1: 0.50, S2: 0.50
    *   Eficiencia del Proyecto (e\_1): 0.7500 (Numerador: 0.50, Denominador T\_j^2: 1.00, T\_j: 1.00)

**Resultados de la Optimización (Pyomo - Bonmin):**
*   Eficiencia Global Total: **75.00%**
*   Tiempo de ejecución: 0.09 segundos
*   **Proyecto 1 (Peso: 100.00%)**
    *   Requerimientos: S1: 0.5, S2: 0.5
    *   Equipo asignado: Persona 0 (S1): 50.0%, Persona 1 (S2): 50.0%
    *   Cálculo de Eficiencia (e\_1):
        *   Suma de afinidades: 0.50
        *   Total requerimientos (T\_j^2): 1.00
        *   e\_1 = (1 + 0.50/1.00)/2 = 75.00%
        *   Contribución Global: 75.00%

---

### **Test Case 2: [`manual.json`](./manual.json)**

**Instance Details (from Brute Force Log):**
*   Personas: 3, Proyectos: 2, Fracciones de Tiempo: 3
*   Habilidades disponibles: \['S1', 'S2']
*   Habilidades de las personas: Persona 0: S1, Persona 1: S1, Persona 2: S2
*   Proyecto 0 (peso 0.60) requerimientos: {'S1': 1.0, 'S2': 1.0}
*   Proyecto 1 (peso 0.40) requerimientos: {'S1': 1.0}
*   Matriz de Afinidad:
    ```
         00  01  02
    00   1   1   0
    01   1   1   0
    02   0   0   1
    ```
*   Fracciones de Tiempo: \[0.0, 0.5, 1.0]

**Resultados de la Fuerza Bruta:**
*   Eficiencia Global Óptima: **0.8500**
*   Total combinaciones verificadas: 729
*   Asignaciones válidas encontradas: 3
*   Tiempo de ejecución: 0.01 segundos
*   **Proyecto 1 (Peso: 60.00%)**
    *   Requerimientos: S1: 1.0, S2: 1.0
    *   Equipo Asignado: Persona 1 (S1): 1.00, Persona 2 (S2): 1.00
    *   Suministro total: S1: 1.00, S2: 1.00
    *   Eficiencia del Proyecto (e\_1): 0.7500 (Numerador: 2.00, Denominador T\_j^2: 4.00, T\_j: 2.00)
*   **Proyecto 2 (Peso: 40.00%)**
    *   Requerimientos: S1: 1.0
    *   Equipo Asignado: Persona 0 (S1): 1.00
    *   Suministro total: S1: 1.00
    *   Eficiencia del Proyecto (e\_2): 1.0000 (Numerador: 1.00, Denominador T\_j^2: 1.00, T\_j: 1.00)

**Resultados de la Optimización (Pyomo - Bonmin):**
*   Eficiencia Global Total: **85.00%**
*   Tiempo de ejecución: 0.09 segundos
*   **Proyecto 1 (Peso: 60.00%)**
    *   Requerimientos: S1: 1.0, S2: 1.0
    *   Equipo asignado: Persona 0 (S1): 50.0%, Persona 1 (S1): 50.0%, Persona 2 (S2): 100.0%
    *   Cálculo de Eficiencia (e\_1):
        *   Suma de afinidades: 2.00
        *   Total requerimientos (T\_j^2): 4.00
        *   e\_1 = (1 + 2.00/4.00)/2 = 75.00%
        *   Contribución Global: 45.00%
*   **Proyecto 2 (Peso: 40.00%)**
    *   Requerimientos: S1: 1.0
    *   Equipo asignado: Persona 0 (S1): 50.0%, Persona 1 (S1): 50.0%
    *   Cálculo de Eficiencia (e\_2):
        *   Suma de afinidades: 1.00
        *   Total requerimientos (T\_j^2): 1.00
        *   e\_2 = (1 + 1.00/1.00)/2 = 100.00%
        *   Contribución Global: 40.00%

---

### **Test Case 3: [`medium_case.json`](./medium_case.json)**


**Instance Details (from Brute Force Log):**
*   Personas: 4, Proyectos: 3, Fracciones de Tiempo: 3
*   Habilidades disponibles: \['A', 'B', 'C']
*   Habilidades de las personas: Persona 0: A, Persona 1: A, Persona 2: B, Persona 3: C
*   Proyecto 0 (peso 0.40) requerimientos: {'A': 1.0, 'B': 0.5}
*   Proyecto 1 (peso 0.35) requerimientos: {'B': 0.5, 'C': 0.5}
*   Proyecto 2 (peso 0.25) requerimientos: {'A': 0.5, 'C': 0.5}
*   Matriz de Afinidad:
    ```
         00  01  02  03
    00   1   1  -1   0
    01   1   1   0   0
    02  -1   0   1   1
    03   0   0   1   1
    ```
*   Fracciones de Tiempo: \[0.0, 0.5, 1.0]

**Resultados de la Fuerza Bruta:**
*   Eficiencia Global Óptima: **0.8486**
*   Total combinaciones verificadas: 531441
*   Asignaciones válidas encontradas: 4
*   Tiempo de ejecución: 3.05 segundos
*   **Proyecto 1 (Peso: 40.00%)**
    *   Requerimientos: A: 1.0, B: 0.5
    *   Equipo Asignado: Persona 1 (A): 1.00, Persona 2 (B): 0.50
    *   Suministro total: A: 1.00, B: 0.50
    *   Eficiencia del Proyecto (e\_1): 0.7778 (Numerador: 1.25, Denominador T\_j^2: 2.25, T\_j: 1.50)
*   **Proyecto 2 (Peso: 35.00%)**
    *   Requerimientos: B: 0.5, C: 0.5
    *   Equipo Asignado: Persona 2 (B): 0.50, Persona 3 (C): 0.50
    *   Suministro total: B: 0.50, C: 0.50
    *   Eficiencia del Proyecto (e\_2): 1.0000 (Numerador: 1.00, Denominador T\_j^2: 1.00, T\_j: 1.00)
*   **Proyecto 3 (Peso: 25.00%)**
    *   Requerimientos: A: 0.5, C: 0.5
    *   Equipo Asignado: Persona 0 (A): 0.50, Persona 3 (C): 0.50
    *   Suministro total: A: 0.50, C: 0.50
    *   Eficiencia del Proyecto (e\_3): 0.7500 (Numerador: 0.50, Denominador T\_j^2: 1.00, T\_j: 1.00)

**Resultados de la Optimización (Pyomo - Bonmin):**
*   Eficiencia Global Total: **84.86%**
*   Tiempo de ejecución: 0.09 segundos
*   **Proyecto 1 (Peso: 40.00%)**
    *   Requerimientos: A: 1.0, B: 0.5
    *   Equipo asignado: Persona 1 (A): 100.0%, Persona 2 (B): 50.0%
    *   Cálculo de Eficiencia (e\_1):
        *   Suma de afinidades: 1.25
        *   Total requerimientos (T\_j^2): 2.25
        *   e\_1 = (1 + 1.25/2.25)/2 = 77.78%
        *   Contribución Global: 31.11%
*   **Proyecto 2 (Peso: 35.00%)**
    *   Requerimientos: B: 0.5, C: 0.5
    *   Equipo asignado: Persona 2 (B): 50.0%, Persona 3 (C): 50.0%
    *   Cálculo de Eficiencia (e\_2):
        *   Suma de afinidades: 1.00
        *   Total requerimientos (T\_j^2): 1.00
        *   e\_2 = (1 + 1.00/1.00)/2 = 100.00%
        *   Contribución Global: 35.00%
*   **Proyecto 3 (Peso: 25.00%)**
    *   Requerimientos: A: 0.5, C: 0.5
    *   Equipo asignado: Persona 0 (A): 50.0%, Persona 3 (C): 50.0%
    *   Cálculo de Eficiencia (e\_3):
        *   Suma de afinidades: 0.50
        *   Total requerimientos (T\_j^2): 1.00
        *   e\_3 = (1 + 0.50/1.00)/2 = 75.00%
        *   Contribución Global: 18.75%

---

### **Test Case 4: [`complex.json`](./complex.json)**

**Instance Details (from Brute Force Log):**
*   Personas: 5, Proyectos: 3, Fracciones de Tiempo: 3
*   Habilidades disponibles: \['X', 'Y', 'Z']
*   Habilidades de las personas: Persona 0: X, Persona 1: X, Persona 2: Y, Persona 3: Y, Persona 4: Z
*   Proyecto 0 (peso 0.40) requerimientos: {'X': 1.0, 'Y': 0.5}
*   Proyecto 1 (peso 0.35) requerimientos: {'Y': 1.0, 'Z': 0.5}
*   Proyecto 2 (peso 0.25) requerimientos: {'X': 0.5, 'Z': 0.5}
*   Matriz de Afinidad:
    ```
         00  01  02  03  04
    00   1   1  -1   0   0
    01   1   1   0   0  -1
    02  -1   0   1   1   0
    03   0   0   1   1   1
    04   0  -1   0   1   1
    ```
*   Fracciones de Tiempo: \[0.0, 0.5, 1.0]

**Resultados de la Fuerza Bruta:**
*   Eficiencia Global Óptima: **0.8486**
*   Total combinaciones verificadas: 14348907
*   Asignaciones válidas encontradas: 16
*   Tiempo de ejecución: 76.02 segundos
*   **Proyecto 1 (Peso: 40.00%)**
    *   Requerimientos: X: 1.0, Y: 0.5
    *   Equipo Asignado: Persona 1 (X): 1.00, Persona 2 (Y): 0.50
    *   Suministro total: X: 1.00, Y: 0.50
    *   Eficiencia del Proyecto (e\_1): 0.7778 (Numerador: 1.25, Denominador T\_j^2: 2.25, T\_j: 1.50)
*   **Proyecto 2 (Peso: 35.00%)**
    *   Requerimientos: Y: 1.0, Z: 0.5
    *   Equipo Asignado: Persona 3 (Y): 1.00, Persona 4 (Z): 0.50
    *   Suministro total: Y: 1.00, Z: 0.50
    *   Eficiencia del Proyecto (e\_2): 1.0000 (Numerador: 2.25, Denominador T\_j^2: 2.25, T\_j: 1.50)
*   **Proyecto 3 (Peso: 25.00%)**
    *   Requerimientos: X: 0.5, Z: 0.5
    *   Equipo Asignado: Persona 0 (X): 0.50, Persona 4 (Z): 0.50
    *   Suministro total: X: 0.50, Z: 0.50
    *   Eficiencia del Proyecto (e\_3): 0.7500 (Numerador: 0.50, Denominador T\_j^2: 1.00, T\_j: 1.00)

**Resultados de la Optimización (Pyomo - Bonmin):**
*   Eficiencia Global Total: **84.86%**
*   Tiempo de ejecución: 0.11 segundos
*   **Proyecto 1 (Peso: 40.00%)**
    *   Requerimientos: X: 1.0, Y: 0.5
    *   Equipo asignado: Persona 1 (X): 100.0%, Persona 2 (Y): 50.0%
    *   Cálculo de Eficiencia (e\_1):
        *   Suma de afinidades: 1.25
        *   Total requerimientos (T\_j^2): 2.25
        *   e\_1 = (1 + 1.25/2.25)/2 = 77.78%
        *   Contribución Global: 31.11%
*   **Proyecto 2 (Peso: 35.00%)**
    *   Requerimientos: Y: 1.0, Z: 0.5
    *   Equipo asignado: Persona 3 (Y): 100.0%, Persona 4 (Z): 50.0%
    *   Cálculo de Eficiencia (e\_2):
        *   Suma de afinidades: 2.25
        *   Total requerimientos (T\_j^2): 2.25
        *   e\_2 = (1 + 2.25/2.25)/2 = 100.00%
        *   Contribución Global: 35.00%
*   **Proyecto 3 (Peso: 25.00%)**
    *   Requerimientos: X: 0.5, Z: 0.5
    *   Equipo asignado: Persona 0 (X): 50.0%, Persona 4 (Z): 50.0%
    *   Cálculo de Eficiencia (e\_3):
        *   Suma de afinidades: 0.50
        *   Total requerimientos (T\_j^2): 1.00
        *   e\_3 = (1 + 0.50/1.00)/2 = 75.00%
        *   Contribución Global: 18.75%

---

### **Test Case 5: [`complex2.json`](./complex2.json)**

**Instance Details (from Brute Force Log):**
*   Personas: 6, Proyectos: 3, Fracciones de Tiempo: 3
*   Habilidades disponibles: \['A', 'B', 'C']
*   Habilidades de las personas: Persona 0: A, Persona 1: A, Persona 2: B, Persona 3: B, Persona 4: C, Persona 5: C
*   Proyecto 0 (peso 0.50) requerimientos: {'A': 1.0, 'B': 0.5}
*   Proyecto 1 (peso 0.30) requerimientos: {'B': 1.0, 'C': 1.0}
*   Proyecto 2 (peso 0.20) requerimientos: {'A': 0.5, 'C': 0.5}
*   Matriz de Afinidad:

    ```
         00  01  02  03  04  05
    00   1   1  -1   0   0   0
    01   1   1   0   0  -1   0
    02  -1   0   1   1   0   0
    03   0   0   1   1   0   0
    04   0  -1   0   0   1   1
    05   0   0   0   0   1   1
    ```
*   Fracciones de Tiempo: \[0.0, 0.5, 1.0]

**Resultados de la Fuerza Bruta:**
*   Eficiencia Global Óptima: **0.7639**
*   Total combinaciones verificadas: 387420489
*   Asignaciones válidas encontradas: 64
*   Tiempo de ejecución: 2698.17 segundos
*   **Proyecto 1 (Peso: 50.00%)**
    *   Requerimientos: A: 1.0, B: 0.5
    *   Equipo Asignado: Persona 1 (A): 1.00, Persona 3 (B): 0.50
    *   Suministro total: A: 1.00, B: 0.50
    *   Eficiencia del Proyecto (e\_1): 0.7778 (Numerador: 1.25, Denominador T\_j^2: 2.25, T\_j: 1.50)
*   **Proyecto 2 (Peso: 30.00%)**
    *   Requerimientos: B: 1.0, C: 1.0
    *   Equipo Asignado: Persona 2 (B): 0.50, Persona 3 (B): 0.50, Persona 5 (C): 1.00
    *   Suministro total: B: 1.00, C: 1.00
    *   Eficiencia del Proyecto (e\_2): 0.7500 (Numerador: 2.00, Denominador T\_j^2: 4.00, T\_j: 2.00)
*   **Proyecto 3 (Peso: 20.00%)**
    *   Requerimientos: A: 0.5, C: 0.5
    *   Equipo Asignado: Persona 0 (A): 0.50, Persona 4 (C): 0.50
    *   Suministro total: A: 0.50, C: 0.50
    *   Eficiencia del Proyecto (e\_3): 0.7500 (Numerador: 0.50, Denominador T\_j^2: 1.00, T\_j: 1.00)

**Resultados de la Optimización (Pyomo - Bonmin):**
*   Eficiencia Global Total: **76.39%**
*   Tiempo de ejecución: 0.11 segundos
*   **Proyecto 1 (Peso: 50.00%)**
    *   Requerimientos: A: 1.0, B: 0.5
    *   Equipo asignado: Persona 0 (A): 50.0%, Persona 1 (A): 50.0%, Persona 3 (B): 50.0%
    *   Cálculo de Eficiencia (e\_1):
        *   Suma de afinidades: 1.25
        *   Total requerimientos (T\_j^2): 2.25
        *   e\_1 = (1 + 1.25/2.25)/2 = 77.78%
        *   Contribución Global: 38.89%
*   **Proyecto 2 (Peso: 30.00%)**
    *   Requerimientos: B: 1.0, C: 1.0
    *   Equipo asignado: Persona 2 (B): 50.0%, Persona 3 (B): 50.0%, Persona 4 (C): 50.0%, Persona 5 (C): 50.0%
    *   Cálculo de Eficiencia (e\_2):
        *   Suma de afinidades: 2.00
        *   Total requerimientos (T\_j^2): 4.00
        *   e\_2 = (1 + 2.00/4.00)/2 = 75.00%
        *   Contribución Global: 22.50%
*   **Proyecto 3 (Peso: 20.00%)**
    *   Requerimientos: A: 0.5, C: 0.5
    *   Equipo asignado: Persona 0 (A): 50.0%, Persona 5 (C): 50.0%
    *   Cálculo de Eficiencia (e\_3):
        *   Suma de afinidades: 0.50
        *   Total requerimientos (T\_j^2): 1.00
        *   e\_3 = (1 + 0.50/1.00)/2 = 75.00%
        *   Contribución Global: 15.00%

---

### **Test Case 6: [`complex3.json`](./complex3.json)**

**Instance Details (from Brute Force Log):**
*   Personas: 6, Proyectos: 3, Fracciones de Tiempo: 3
*   Habilidades disponibles: \['S1', 'S2', 'S3']
*   Habilidades de las personas: Persona 0: S1, Persona 1: S1, Persona 2: S2, Persona 3: S2, Persona 4: S3, Persona 5: S3
*   Proyecto 0 (peso 0.40) requerimientos: {'S1': 1.0, 'S2': 0.5}
*   Proyecto 1 (peso 0.35) requerimientos: {'S2': 1.0, 'S3': 0.5}
*   Proyecto 2 (peso 0.25) requerimientos: {'S1': 0.5, 'S3': 1.0}
*   Matriz de Afinidad:
    ```
         00  01  02  03  04  05
    00   1   1  -1   0   0   0
    01   1   1   0   0  -1   0
    02  -1   0   1   1   0   0
    03   0   0   1   1   0  -1
    04   0  -1   0   0   1   1
    05   0   0   0  -1   1   1
    ```
*   Fracciones de Tiempo: \[0.0, 0.5, 1.0]

**Resultados de la Fuerza Bruta:**
*   Eficiencia Global Óptima: **0.7778**
*   Total combinaciones verificadas: 387420489
*   Asignaciones válidas encontradas: 64
*   Tiempo de ejecución: 2334.29 segundos
*   **Proyecto 1 (Peso: 40.00%)**
    *   Requerimientos: S1: 1.0, S2: 0.5
    *   Equipo Asignado: Persona 1 (S1): 1.00, Persona 3 (S2): 0.50
    *   Suministro total: S1: 1.00, S2: 0.50
    *   Eficiencia del Proyecto (e\_1): 0.7778 (Numerador: 1.25, Denominador T\_j^2: 2.25, T\_j: 1.50)
*   **Proyecto 2 (Peso: 35.00%)**
    *   Requerimientos: S2: 1.0, S3: 0.5
    *   Equipo Asignado: Persona 2 (S2): 0.50, Persona 3 (S2): 0.50, Persona 4 (S3): 0.50
    *   Suministro total: S2: 1.00, S3: 0.50
    *   Eficiencia del Proyecto (e\_2): 0.7778 (Numerador: 1.25, Denominador T\_j^2: 2.25, T\_j: 1.50)
*   **Proyecto 3 (Peso: 25.00%)**
    *   Requerimientos: S1: 0.5, S3: 1.0
    *   Equipo Asignado: Persona 0 (S1): 0.50, Persona 5 (S3): 1.00
    *   Suministro total: S1: 0.50, S3: 1.00
    *   Eficiencia del Proyecto (e\_3): 0.7778 (Numerador: 1.25, Denominador T\_j^2: 2.25, T\_j: 1.50)

**Resultados de la Optimización (Pyomo - Bonmin):**
*   Eficiencia Global Total: **77.78%**
*   Tiempo de ejecución: 0.12 segundos
*   **Proyecto 1 (Peso: 40.00%)**
    *   Requerimientos: S1: 1.0, S2: 0.5
    *   Equipo asignado: Persona 0 (S1): 50.0%, Persona 1 (S1): 50.0%, Persona 3 (S2): 50.0%
    *   Cálculo de Eficiencia (e\_1):
        *   Suma de afinidades: 1.25
        *   Total requerimientos (T\_j^2): 2.25
        *   e\_1 = (1 + 1.25/2.25)/2 = 77.78%
        *   Contribución Global: 31.11%
*   **Proyecto 2 (Peso: 35.00%)**
    *   Requerimientos: S2: 1.0, S3: 0.5
    *   Equipo asignado: Persona 2 (S2): 50.0%, Persona 3 (S2): 50.0%, Persona 4 (S3): 50.0%
    *   Cálculo de Eficiencia (e\_2):
        *   Suma de afinidades: 1.25
        *   Total requerimientos (T\_j^2): 2.25
        *   e\_2 = (1 + 1.25/2.25)/2 = 77.78%
        *   Contribución Global: 27.22%
*   **Proyecto 3 (Peso: 25.00%)**
    *   Requerimientos: S1: 0.5, S3: 1.0
    *   Equipo asignado: Persona 0 (S1): 50.0%, Persona 4 (S3): 50.0%, Persona 5 (S3): 50.0%
    *   Cálculo de Eficiencia (e\_3):
        *   Suma de afinidades: 1.25
        *   Total requerimientos (T\_j^2): 2.25
        *   e\_3 = (1 + 1.25/2.25)/2 = 77.78%
        *   Contribución Global: 19.44%

---

