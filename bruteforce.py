import itertools
import time
from typing import Optional

import numpy as np

from onefile import DataGenerator, InstanceData  # Necesario para la fuerza bruta


# =============================================
# 4. Solución por Fuerza Bruta (Para Validación y Comparación)
# =============================================
class BruteForce_MTFP_Solver:
    """
    Resuelve el MTFP mediante fuerza bruta, explorando todas las asignaciones posibles.
    ADVERTENCIA: Solo factible para instancias MUY pequeñas.
    """

    def __init__(self, data: InstanceData):
        self.data = data
        self.N = len(data.people)
        self.M = len(data.projects)
        self.K_skills = data.skills
        self.tf_values = data.time_fractions
        self.num_tf_values = len(self.tf_values)

        self.Q_k = {
            k: [i for i, p in enumerate(self.data.people) if p.skill == k]
            for k in self.data.skills
        }
        self.R_kj = {
            (j, k): self.data.projects[j].requirements.get(k, 0.0)
            for j in range(self.M)
            for k in self.K_skills
        }
        self.S_ij = self.data.sociometric
        self.w_j = [p.weight for p in self.data.projects]
        self.epsilon = 1e-9  # Para comparaciones de punto flotante

    def _is_assignment_valid(self, current_x_matrix: np.ndarray) -> bool:
        # Restricción (2): Total time per person
        for i in range(self.N):
            if sum(current_x_matrix[i, j] for j in range(self.M)) > 1.0 + self.epsilon:
                return False

        # Restricción (3): Skill requirement per project and skill (must be EQUAL)
        for j in range(self.M):
            for k_skill in self.K_skills:
                required = self.R_kj.get((j, k_skill), 0.0)
                # No need to check if required is 0.0, sum will be 0 and compared to 0.

                supplied = sum(
                    current_x_matrix[p_idx, j] for p_idx in self.Q_k[k_skill]
                )
                # Check for equality within epsilon
                if abs(supplied - required) > self.epsilon:
                    return False
        return True

    def _calculate_objective(self, current_x_matrix: np.ndarray) -> float:
        total_weighted_efficiency = 0.0
        for j in range(self.M):
            numerator = 0.0
            for i1 in range(self.N):
                for i2 in range(self.N):
                    numerator += (
                        self.S_ij[i1, i2]
                        * current_x_matrix[i1, j]
                        * current_x_matrix[i2, j]
                    )

            T_j = sum(self.R_kj.get((j, k_skill), 0.0) for k_skill in self.K_skills)

            # Denominador según la función objetivo del modelo Pyomo: T_j^2
            denominator_val = T_j**2

            e_j = 0.0
            # e_j = (1 + numerator / denominator) / 2 if denominator != 0 else 0.0
            if abs(denominator_val) > self.epsilon:  # Check if T_j^2 is not zero
                e_j = (1.0 + numerator / denominator_val) / 2.0
            # If T_j is 0, denominator_val will be 0, and e_j remains 0.0, which is correct.

            total_weighted_efficiency += self.w_j[j] * e_j
        return total_weighted_efficiency

    def solve(self, max_iterations: int = 1000000):
        """
        Intenta resolver el problema por fuerza bruta.

        Args:
            max_iterations (int): Límite de combinaciones a probar para evitar ejecuciones excesivamente largas.

        Returns:
            tuple: (best_assignment_matrix, best_efficiency, num_valid_assignments, num_total_assignments_checked)
                   Retorna (None, -inf, 0, count) si no se encuentra solución o se excede el límite.
        """
        best_efficiency = -float("inf")
        best_assignment_matrix = None
        num_valid_assignments = 0
        num_total_assignments_checked = 0

        # Iterador sobre los índices de las fracciones de tiempo para cada variable x_ij
        # Hay N*M variables x_ij
        assignment_indices_iter = itertools.product(
            range(self.num_tf_values), repeat=self.N * self.M
        )

        print(
            f"Iniciando Fuerza Bruta. Total de combinaciones teóricas: {self.num_tf_values**(self.N * self.M)}"
        )
        print(f"Se probarán como máximo {max_iterations} combinaciones.")

        current_x_matrix = np.zeros((self.N, self.M))

        for indices_tuple in assignment_indices_iter:
            num_total_assignments_checked += 1
            if num_total_assignments_checked > max_iterations:
                print(
                    f"Fuerza Bruta: Límite de {max_iterations} iteraciones alcanzado."
                )
                break

            # Construir la matriz de asignación actual x_ij
            idx = 0
            for r_person in range(self.N):
                for c_project in range(self.M):
                    current_x_matrix[r_person, c_project] = self.tf_values[
                        indices_tuple[idx]
                    ]
                    idx += 1

            if self._is_assignment_valid(current_x_matrix):
                num_valid_assignments += 1
                current_efficiency = self._calculate_objective(current_x_matrix)
                if current_efficiency > best_efficiency:
                    best_efficiency = current_efficiency
                    best_assignment_matrix = current_x_matrix.copy()

            if (
                num_total_assignments_checked
                % (max_iterations // 10 if max_iterations > 100 else 100)
                == 0
            ):
                print(
                    f"Fuerza Bruta: {num_total_assignments_checked} combinaciones verificadas..."
                )

        if best_assignment_matrix is not None:
            print(
                f"Fuerza Bruta: Solución encontrada con eficiencia {best_efficiency:.4f}"
            )
        elif num_total_assignments_checked <= max_iterations:
            print(
                f"Fuerza Bruta: No se encontró ninguna asignación válida tras {num_total_assignments_checked} combinaciones."
            )

        print(
            f"Fuerza Bruta: Total combinaciones verificadas: {num_total_assignments_checked}"
        )
        print(
            f"Fuerza Bruta: Asignaciones válidas encontradas: {num_valid_assignments}"
        )
        return (
            best_assignment_matrix,
            best_efficiency,
            num_valid_assignments,
            num_total_assignments_checked,
        )

    def pretty_print_solution(
        self, assignment_matrix: Optional[np.ndarray], efficiency: float
    ):
        if assignment_matrix is None:
            print("Fuerza Bruta: No hay solución para mostrar.")
            return

        print("\n" + "=" * 60)
        print(" RESULTADOS DE LA FUERZA BRUTA ".center(60, "="))
        print("=" * 60)
        DataGenerator.pretty_print_instance(self.data)  # Mostrar datos de la instancia
        print("-" * 60)
        print(f"Eficiencia Global Óptima (Fuerza Bruta): {efficiency:.4f}")
        print("-" * 60)

        for j_proj_idx in range(self.M):
            project_data = self.data.projects[j_proj_idx]
            print(f"\nPROYECTO {j_proj_idx + 1} (Peso: {project_data.weight:.2%})")
            print("  Requerimientos:")
            for skill, req_val in project_data.requirements.items():
                print(f"    - {skill}: {req_val}")

            print("  Equipo Asignado y Contribuciones:")
            project_total_alloc_skill = {skill: 0.0 for skill in self.K_skills}
            for i_person_idx in range(self.N):
                alloc = assignment_matrix[i_person_idx, j_proj_idx]
                if alloc > self.epsilon:
                    person_skill = self.data.people[i_person_idx].skill
                    print(f"    - Persona {i_person_idx} ({person_skill}): {alloc:.2f}")
                    project_total_alloc_skill[person_skill] += alloc

            print("  Suministro total por habilidad para este proyecto:")
            for skill, supplied_val in project_total_alloc_skill.items():
                if (
                    project_data.requirements.get(skill, 0.0) > 0
                ):  # Mostrar solo si había requerimiento
                    print(
                        f"    - {skill}: {supplied_val:.2f} (Requerido: {project_data.requirements.get(skill,0.0):.2f})"
                    )

            # Recalcular e_j para este proyecto con la asignación encontrada
            numerator_ej = 0.0
            for i1 in range(self.N):
                for i2 in range(self.N):
                    numerator_ej += (
                        self.S_ij[i1, i2]
                        * assignment_matrix[i1, j_proj_idx]
                        * assignment_matrix[i2, j_proj_idx]
                    )

            T_j = sum(
                self.R_kj.get((j_proj_idx, k_skill), 0.0) for k_skill in self.K_skills
            )
            # Denominador según la función objetivo del modelo Pyomo: T_j^2
            denominator_val_ej = T_j**2
            e_j = 0.0
            if abs(denominator_val_ej) > self.epsilon:  # Check if T_j^2 is not zero
                e_j = (1.0 + numerator_ej / denominator_val_ej) / 2.0

            print(f"  Eficiencia del Proyecto (e_{j_proj_idx + 1}): {e_j:.4f}")
            print(
                f"    (Numerador: {numerator_ej:.2f}, Denominador T_j^2: {denominator_val_ej:.2f}, T_j: {T_j:.2f})"
            )
        print("=" * 60)


if __name__ == "__main__":
    dataGen = DataGenerator()
    data = dataGen.load_from_json("test_cases\complex3.json")
    optimizer = BruteForce_MTFP_Solver(data)

    # Calcular el número total de combinaciones teóricas
    total_theoretical_combinations = optimizer.num_tf_values ** (
        optimizer.N * optimizer.M
    )

    # Establecer max_iterations para que sea igual al total de combinaciones teóricas,
    # asegurando que se explore todo el espacio.
    # El valor anterior (15348907) ya era mayor que 14348907, por lo que no era la causa del problema.
    iterations_to_run = total_theoretical_combinations

    print(f"--- Preparando para ejecutar Fuerza Bruta ---")
    print(
        f"Instancia: Personas={optimizer.N}, Proyectos={optimizer.M}, Fracciones de Tiempo={optimizer.num_tf_values}"
    )
    print(f"Habilidades disponibles en la instancia: {optimizer.data.skills}")
    print(f"Habilidades de las personas (índice: habilidad):")
    for i, p in enumerate(optimizer.data.people):
        print(f"  Persona {i}: {p.skill}")
    for i, project in enumerate(optimizer.data.projects):
        print(
            f"Proyecto {i} (peso {project.weight:.2f}) requerimientos: {project.requirements}"
        )
    print(f"--- Fin detalles de instancia ---")

    start_time = time.time()
    # La función solve ya tiene un print para el total de combinaciones teóricas y el máximo a probar.
    results = optimizer.solve(max_iterations=iterations_to_run)
    elapsed = time.time() - start_time

    if results[0] is not None:
        optimizer.pretty_print_solution(results[0], results[1])
    else:
        print("\nNo se encontró solución óptima por fuerza bruta.")
        print(
            "Esto significa que, para la instancia de datos generada, no existe ninguna"
        )
        print("asignación de personas a proyectos que cumpla TODAS las restricciones.")
        print("Causas posibles:")
        print(
            "  1. La instancia es inherentemente inviable (ej: requerimientos muy altos para las habilidades/personas disponibles con la semilla actual)."
        )
        print(
            "     Prueba con otra semilla o ajusta los parámetros de generación (más skills, menos proyectos/personas para prueba)."
        )
        print(
            "  2. Un error en la lógica de validación (menos probable si el modelo Pyomo sí encuentra soluciones para otras instancias)."
        )
        print(
            f"Se verificaron {results[3]} de {total_theoretical_combinations} combinaciones teóricas."
        )

    print(f"Tiempo de ejecución: {elapsed:.2f} segundos")
