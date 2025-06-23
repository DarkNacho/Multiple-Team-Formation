Plan detallado para la sección de "Resultados y Discusión":

**Pseudocódigo del plan de pruebas:**

1. **Validación de Correctitud (Pequeñas Instancias)**
- Generar instancias pequeñas (2-6 personas, 1-2 proyectos, 2 habilidades).
- Resolver con el modelo MINLP y comparar el resultado con la solución de fuerza bruta.
- Verificar que la eficiencia global y las asignaciones coincidan o sean muy cercanas.
- Documentar casos donde la solución óptima es alcanzada.

2. **Pruebas de Escalabilidad**
- Generar instancias crecientes en tamaño:
- 10, 20, 30, 50, 100 personas.
- 2, 5, 10 proyectos.
- 2, 4, 8 habilidades.
- Medir tiempo de resolución y eficiencia global obtenida.
- Registrar si el solver alcanza optimalidad o se detiene por tiempo.

3. **Impacto de la Discretización de Fracciones de Tiempo**
- Comparar resultados usando diferentes conjuntos de fracciones permitidas (e.g., {0,1}, {0,0.5,1}, {0,0.25,0.5,0.75,1}).
- Analizar cómo afecta la calidad de la solución y el tiempo de cómputo.

4. **Robustez ante Afinidades Negativas**
- Generar instancias con alta proporción de afinidades negativas.
- Observar si el modelo evita asignar personas con conflictos a los mismos equipos.
- Medir el impacto en la eficiencia global.

5. **Sensibilidad a la Prioridad de Proyectos**
- Crear instancias donde un proyecto tenga peso mucho mayor.
- Verificar si el modelo prioriza la cohesión en ese proyecto.

6. **Casos Inviables**
- Forzar instancias donde los requerimientos superan la capacidad.
- Confirmar que el modelo detecta inviabilidad y reporta correctamente.

7. **Comparación con la Solución de Fuerza Bruta**
- Para instancias pequeñas, comparar la eficiencia y asignaciones.
- Documentar diferencias y justificar posibles discrepancias.

8. **Tabla de Resultados**
- Para cada experimento, registrar:
- Tamaño de la instancia (personas, proyectos, habilidades)
- Fracciones permitidas
- Tiempo de resolución
- Eficiencia global obtenida
- Estado del solver (óptimo, factible, inviable)
- Gap (si aplica)
- Observaciones relevantes

**Resumen del plan para la sección:**
- Validar correctitud y optimalidad en instancias pequeñas.
- Evaluar escalabilidad y tiempos de cómputo.
- Analizar el efecto de la discretización de fracciones.
- Medir robustez ante afinidades negativas y prioridades.
- Probar detección de inviabilidad.
- Comparar con fuerza bruta donde sea posible.
- Presentar resultados en una tabla clara para discusión.