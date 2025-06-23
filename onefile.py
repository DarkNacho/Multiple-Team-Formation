"""
Solución del Multiple Team Formation Problem (MTFP)
Basado en: Gutiérrez et al. (2016).
"""

import time
from typing import List, Dict, Literal, Optional
from pydantic import BaseModel, Field
import numpy as np
import pyomo.environ as pyo
from pyomo.opt import SolverResults

import json
import random


# =============================================
# 1. Modelado de Datos (Sección 3.1 del Paper)
# =============================================
class Person(BaseModel):
    """Representa una persona con una única habilidad.

    Atributos:
        skill (str): Habilidad de la persona (debe existir en InstanceData.skills)
    """

    skills: List[str]


class Project(BaseModel):
    """Representa un proyecto con requerimientos y prioridad.

    Atributos:
        requirements (Dict[str, float]): Requerimientos por habilidad {skill: cantidad}
        weight (float): Peso del proyecto (entre 0 y 1, suma total debe ser 1)
    """

    requirements: Dict[str, float]
    weight: float = Field(ge=0, le=1)


class InstanceData(BaseModel):
    """Contiene todos los datos de una instancia del problema MTFP.

    Atributos:
        people (List[Person]): Lista de personas disponibles
        projects (List[Project]): Lista de proyectos
        skills (List[str]): Lista única de habilidades
        sociometric (np.ndarray): Matriz NxN de afinidad (S_ij ∈ {-1, 0, +1})
        time_fractions (List[float]): Fracciones de tiempo permitidas (conjunto D)
    """

    people: List[Person]
    projects: List[Project]
    skills: List[str]
    sociometric: np.ndarray
    time_fractions: List[float]

    class Config:
        arbitrary_types_allowed = True  # Permite usar np.ndarray


# =============================================
# 2. Generación de Datos (Sección 5.1 del Paper)
# =============================================
class DataGenerator:
    """Genera instancias del MTFP con datos aleatorios o predefinidos."""

    @staticmethod
    def generate_random_instance(
        num_people: int = 10,
        num_projects: int = 2,
        skills: List[str] = ["Backend", "Frontend"],
        time_fractions: List[float] = [0.0, 0.5, 1.0],
        positive_prob: float = 0.3,
        seed: int = 42,
    ) -> InstanceData:
        """Genera una instancia aleatoria del MTFP."""
        random.seed(seed)
        np.random.seed(seed)

        people = DataGenerator._generate_people(num_people, skills)
        projects = DataGenerator._generate_projects(
            num_projects, skills, people, time_fractions
        )
        sociometric = DataGenerator._generate_sociometric_matrix(
            num_people, positive_prob
        )

        # --- NUEVO: chequeo de viabilidad ---
        max_time = max(time_fractions)
        for skill in skills:
            cap = sum(1 for p in people if skill in p.skills) * max_time
            req = sum(pr.requirements.get(skill, 0.0) for pr in projects)
            if req > cap + 1e-6:
                print(
                    f"WARNING: Requerimiento total de '{skill}' ({req}) excede capacidad ({cap})"
                )

        return InstanceData(
            people=people,
            projects=projects,
            skills=skills,
            sociometric=sociometric,
            time_fractions=time_fractions,
        )

    @staticmethod
    def _generate_people(num_people: int, skills: List[str]) -> List[Person]:
        """Genera una lista de personas con una o más habilidades aleatorias."""
        people = []
        for _ in range(num_people):
            # Asignar un número aleatorio de habilidades (e.g., de 1 a 3)
            num_skills_to_assign = random.randint(1, min(3, len(skills)))
            person_skills = random.sample(skills, num_skills_to_assign)
            people.append(Person(skills=person_skills))
        return people

    @staticmethod
    def _generate_projects(
        num_projects: int,
        skills: List[str],
        people: List[Person],
        time_fractions: List[float],
    ) -> List[Project]:
        """Genera proyectos viables y realistas: solo incluye habilidades requeridas (valor > 0) en los requerimientos."""
        max_time = max(time_fractions)
        min_fraction = min([f for f in time_fractions if f > 0], default=1.0)
        skill_capacity = {
            skill: sum(1 for p in people if skill in p.skills) * max_time
            for skill in skills
        }

        reqs_per_project = []
        for j in range(num_projects):
            reqs = {}
            # Elegir al menos una habilidad requerida por proyecto
            possible_skills = [
                skill for skill in skills if skill_capacity[skill] >= min_fraction
            ]
            n_required = (
                random.randint(1, len(possible_skills)) if possible_skills else 0
            )
            required_skills = (
                set(random.sample(possible_skills, n_required))
                if n_required > 0
                else set()
            )
            for skill in required_skills:
                cap = skill_capacity[skill]
                max_units = int(cap // min_fraction)
                if max_units > 0:
                    units = random.randint(1, max_units)
                    req = round(units * min_fraction, 6)
                    if req > 0:
                        reqs[skill] = req
            reqs_per_project.append(reqs)

        # Ajusta para que la suma total de requerimientos por habilidad no exceda la capacidad
        for skill in skills:
            cap = skill_capacity[skill]
            total_req = sum(reqs.get(skill, 0.0) for reqs in reqs_per_project)
            while total_req > cap:
                # Quita una fracción mínima a un proyecto aleatorio que tenga ese skill > min_fraction
                candidates = [
                    j
                    for j in range(num_projects)
                    if reqs_per_project[j].get(skill, 0.0) >= min_fraction * 2
                ]
                if not candidates:
                    break
                j = random.choice(candidates)
                reqs_per_project[j][skill] -= min_fraction
                reqs_per_project[j][skill] = round(reqs_per_project[j][skill], 6)
                if reqs_per_project[j][skill] <= 0:
                    del reqs_per_project[j][skill]
                total_req = sum(reqs.get(skill, 0.0) for reqs in reqs_per_project)

        # Asigna pesos aleatorios y normaliza
        raw_projects = []
        total_weight = 0.0
        for j in range(num_projects):
            weight = random.uniform(0.5, 2.0)
            raw_projects.append((reqs_per_project[j], weight))
            total_weight += weight

        return [
            Project(requirements=reqs, weight=weight / total_weight)
            for reqs, weight in raw_projects
        ]

    @staticmethod
    def _generate_sociometric_matrix(
        num_people: int, positive_prob: float
    ) -> np.ndarray:
        """Genera una matriz de afinidad no simétrica."""
        sociometric = np.eye(num_people)  # Diagonal = +1 (auto-afinidad)
        rng = np.random.default_rng()

        for i in range(num_people):
            for j in range(num_people):
                if i != j:
                    sociometric[i][j] = rng.choice(
                        [-1, 0, 1], p=[1 - positive_prob - 0.2, 0.2, positive_prob]
                    )

        return sociometric

    @staticmethod
    def save_to_json(data: InstanceData, filename: str):
        """Guarda una instancia en formato JSON."""
        with open(filename, "w") as f:
            json.dump(
                {
                    "people": [p.dict() for p in data.people],
                    "projects": [pr.dict() for pr in data.projects],
                    "skills": data.skills,
                    "sociometric": data.sociometric.tolist(),
                    "time_fractions": data.time_fractions,
                },
                f,
                indent=2,
            )

    @staticmethod
    def load_from_json(filename: str) -> InstanceData:
        """Carga una instancia desde archivo JSON."""
        with open(filename, "r") as f:
            data = json.load(f)
        data["sociometric"] = np.array(data["sociometric"])
        return InstanceData(**data)

    @staticmethod
    def pretty_print_instance(data: InstanceData):
        """Imprime los datos de la instancia de forma legible."""
        print("\n" + "=" * 50)
        print(" DATOS DE LA INSTANCIA ".center(50, "="))
        print("=" * 50)

        DataGenerator._print_people(data.people)
        DataGenerator._print_projects(data.projects)
        DataGenerator._print_skills(data.skills)
        DataGenerator._print_sociometric_matrix(data.sociometric)
        DataGenerator._print_time_fractions(data.time_fractions)

        print("\n" + "=" * 50)

    @staticmethod
    def _print_people(people: List[Person]):
        """Imprime la lista de personas."""
        print("\nPERSONAS:")
        for i, person in enumerate(people):
            print(f"  Persona {i + 1}: Habilidades = {', '.join(person.skills)}")

    @staticmethod
    def _print_projects(projects: List[Project]):
        """Imprime la lista de proyectos."""
        print("\nPROYECTOS:")
        for j, project in enumerate(projects):
            print(f"  Proyecto {j + 1}:")
            print(f"    - Peso: {project.weight:.2%}")
            print(f"    - Requerimientos:")
            for skill, req in project.requirements.items():
                print(f"      -> {skill}: {req}")

    @staticmethod
    def _print_skills(skills: List[str]):
        """Imprime la lista de habilidades."""
        print("\nHABILIDADES:")
        print(f"  {', '.join(skills)}")

    @staticmethod
    def _print_sociometric_matrix(sociometric: np.ndarray):
        """Imprime la matriz de afinidad."""
        print("\nMATRIZ DE AFINIDAD:")
        for i, row in enumerate(sociometric):
            if i == 0:
                header = "     " + "  ".join([f"{j:02}" for j in range(len(row))])
                print(header)
            print(f"{i:02}  " + "  ".join([f"{int(val):2}" for val in row]))

    @staticmethod
    def _print_time_fractions(time_fractions: List[float]):
        """Imprime las fracciones de tiempo permitidas."""
        print("\nFRACCIONES DE TIEMPO PERMITIDAS:")
        print(f"  {', '.join(map(str, time_fractions))}")


# =============================================
# 3. Modelo de Optimización (Sección 3.3 del Paper)
# =============================================
class MTFP_Optimizer:
    """Implementa el modelo matemático del MTFP usando Pyomo."""

    def __init__(self, data: InstanceData):
        """
        Inicializa el modelo con los datos de entrada.

        Parámetros:
            data (InstanceData): Datos del problema a resolver
        """
        self.data = data
        self.Q = self._build_skill_groups()  # Q_k = {i ∈ H | skill(i) = k}
        self.model = self._build_model()

    def _build_skill_groups(self) -> Dict[str, List[int]]:
        """Construye el conjunto Q_k
        Personas con habilidad k.
        """
        return {
            k: [i for i, p in enumerate(self.data.people) if k in p.skills]
            for k in self.data.skills
        }

    def _build_model(self) -> pyo.ConcreteModel:
        """Construye el modelo de optimización"""
        model = pyo.ConcreteModel()

        # -------------------------------------
        # Conjuntos
        # -------------------------------------
        # P: Personas (índices)
        model.P = pyo.Set(initialize=range(len(self.data.people)))

        # J: Proyectos (índices)
        model.J = pyo.Set(initialize=range(len(self.data.projects)))

        # K: Habilidades
        model.K = pyo.Set(initialize=self.data.skills)

        # Q_k: Personas con habilidad k
        model.Q = pyo.Set(model.K, initialize=lambda m, k: self.Q[k])

        # F: Fracciones de tiempo permitidas
        # (en este caso, se usa como un conjunto de índices para las fracciones)
        model.F = pyo.Set(initialize=range(len(self.data.time_fractions)))

        # -------------------------------------
        # Parámetro
        # -------------------------------------
        # R_{k,j}: Requerimientos por habilidad
        model.R = pyo.Param(
            model.J,
            model.K,
            initialize=lambda m, j, k: self.data.projects[j].requirements.get(k, 0.0),
        )

        # S_{i,j}: Matriz de afinidad (no simétrica)
        model.S = pyo.Param(
            model.P, model.P, initialize=lambda m, i, j: self.data.sociometric[i][j]
        )

        # w_j: Pesos de los proyectos
        model.w = pyo.Param(
            model.J, initialize=lambda m, j: self.data.projects[j].weight
        )

        # Parámetro para mapear índices de F a valores de fracción de tiempo
        model.tf_map = pyo.Param(
            model.F, initialize=lambda m, f_idx: self.data.time_fractions[f_idx]
        )

        # Parámetro que indica si la persona i tiene la habilidad k
        model.HasSkill = pyo.Param(
            model.P,
            model.K,
            initialize=lambda m, i, k: 1 if k in self.data.people[i].skills else 0,
        )

        # -------------------------------------
        # Variables de Decisión
        # -------------------------------------
        # x_{i,j,k}: Fracción de tiempo de la persona i en el proyecto j usando la habilidad k
        model.x = pyo.Var(
            model.P,
            model.J,
            model.K,
            domain=pyo.NonNegativeReals,
        )

        # x_total_{i,j}: Fracción de tiempo TOTAL de la persona i en el proyecto j
        model.x_total = pyo.Var(
            model.P,
            model.J,
            domain=pyo.NonNegativeReals,
        )

        # y_choice_{i,j,f}: Variable binaria que es 1 si la fracción f se elige para x_total_{i,j}
        model.y_choice = pyo.Var(model.P, model.J, model.F, domain=pyo.Binary)

        # -------------------------------------
        # Restricciones
        # -------------------------------------
        @model.Constraint(model.P)
        def total_time(m, i):
            """Restricción (2): ∑_{j∈J} x_total_{i,j} ≤ 1 ∀i∈P
            Las personas pueden ocupar un máximo de todo su tiempo en los proyectos (No mayor a 1 -> 100%).
            """
            return sum(m.x_total[i, j] for j in m.J) <= 1

        @model.Constraint(model.J, model.K)
        def skill_requirement(m, j, k):
            """Restricción (3): ∑_{i∈P} x_{i,j,k} = R_{k,j} ∀j∈J, ∀k∈K
            Las personas con habilidad k deben cumplir los requerimientos del proyecto j.
            La restricción HasSkill_rule se encarga de que solo aporten personas con esa habilidad.
            """
            return sum(m.x[i, j, k] for i in m.P) == m.R[j, k]

        # Restricción para asegurar que una persona solo puede ser asignada con una habilidad que posee
        @model.Constraint(model.P, model.J, model.K)
        def HasSkill_rule(m, i, j, k):
            # La dedicación máxima es 1, por lo que esto funciona como una restricción Big-M
            return m.x[i, j, k] <= m.HasSkill[i, k]

        # Restricción para enlazar la variable de tiempo total con la de tiempo por habilidad
        @model.Constraint(model.P, model.J)
        def link_x_total_rule(m, i, j):
            return m.x_total[i, j] == sum(m.x[i, j, k] for k in m.K)

        # Restricción para asegurar que se elija exactamente una fracción de tiempo para cada x_total_{i,j}
        @model.Constraint(model.P, model.J)
        def force_one_fraction_rule(m, i, j):
            return sum(m.y_choice[i, j, f_idx] for f_idx in m.F) == 1

        # Restricción para definir x_total_{i,j} basado en la y_choice seleccionada
        @model.Constraint(model.P, model.J)
        def define_x_from_choice_rule(m, i, j):
            return m.x_total[i, j] == sum(
                m.tf_map[f_idx] * m.y_choice[i, j, f_idx] for f_idx in m.F
            )

        # -------------------------------------
        # Función Objetivo
        # -------------------------------------
        def objective_rule(m):
            """Objetivo: Maximizar E = ∑_{j∈J} w_j * e_j"""
            total_efficiency = 0.0
            for j in m.J:
                # Numerador: ∑_{i,h∈P} S_{i,h}*x_total_{i,j}*x_total_{h,j}
                numerator = sum(
                    m.S[i1, i2] * m.x_total[i1, j] * m.x_total[i2, j]
                    for i1 in m.P
                    for i2 in m.P
                )

                # Denominador: (∑_{k∈K} R_{k,j})²
                T = sum(m.R[j, k] for k in m.K)
                denominator = T**2
                ej = (1 + numerator / denominator) / 2 if denominator != 0 else 0.0

                total_efficiency += m.w[j] * ej
            return total_efficiency

        model.obj = pyo.Objective(rule=objective_rule, sense=pyo.maximize)

        return model

    def solve(
        self, solver: Literal["ipopt", "bonmin", "couenne", "scip"], tee: bool = True
    ) -> SolverResults:
        """Resuelve el modelo usando el solver especificado.

        Parámetros:
            solver (str): Nombre del solver (ej: 'glpk', 'ipopt')
            tee (bool): Mostrar output del solver

        Retorna:
            pyo.SolverResults: Resultados de la optimización
        """
        solver = pyo.SolverFactory(solver)
        return solver.solve(self.model, tee=tee)

    def pretty_print(self, time_elapsed: Optional[float] = None):
        """Muestra los resultados en formato legible con detalles de cálculo."""

        DataGenerator.pretty_print_instance(self.data)
        print("\n" + "=" * 50)
        print(" RESULTADOS DE LA OPTIMIZACIÓN ".center(50, "="))
        print("=" * 50)

        total_efficiency = 0.0

        for j in self.model.J:
            project = self.data.projects[j]
            ej, numerator, denominator = self._project_efficiency(j)
            weighted_ej = pyo.value(self.model.w[j] * ej)
            total_efficiency += weighted_ej

            print(f"\n{'='*50}")
            print(f" PROYECTO {j+1} ".center(50, "="))
            print(f" - Peso: {project.weight:.2%}")
            print(f" - Requerimientos:")
            for skill, req in project.requirements.items():
                print(f"   -> {skill}: {req}")

            print(f"\n - Equipo asignado:")
            team = [
                i for i in self.model.P if pyo.value(self.model.x_total[i, j]) > 0.001
            ]
            for i in team:
                alloc = pyo.value(self.model.x_total[i, j])
                person_skills = ", ".join(self.data.people[i].skills)
                print(
                    f"   -> Persona {i} ({person_skills}): {alloc:.1%} de tiempo total."
                )
                # Detalle de tiempo por habilidad
                for k in self.model.K:
                    skill_alloc = pyo.value(self.model.x[i, j, k])
                    if skill_alloc > 0.001:
                        print(f"      - {k}: {skill_alloc:.1%}")

            print(f"\n - Cálculo de Eficiencia (e_{j+1}):")
            print(f"   • Suma de afinidades: {numerator:.2f}")
            print(f"   • Total requerimientos: {denominator:.2f}")
            # print(f"   • Denominador: ({denominator:.2f})² = {denominator**2:.2f}")
            print(f"   • Denominador: T^2 = {denominator:.2f}")
            print(
                f"   • e_{j+1} = (1 + {numerator:.2f}/{denominator:.2f})/2 = {ej:.2%}"
            )
            # print(
            #    f"   • e_{j+1} = (1 + {numerator:.2f}/{denominator**2:.2f})/2 = {ej:.2%}"
            # )
            print(f"   • Contribución Global: {weighted_ej:.2%}")

        print(f"\n{' EFICIENCIA GLOBAL TOTAL: ':=^50}")
        print(f"{total_efficiency:.2%}".center(50))
        if time_elapsed is not None:
            print(f"\nTiempo de ejecución: {time_elapsed:.2f} segundos")

    def pretty_print_infeasible(
        self, results=None, time_elapsed: Optional[float] = None
    ):
        """Imprime un mensaje detallado cuando el modelo es inviable."""
        DataGenerator.pretty_print_instance(self.data)
        print("\n" + "=" * 50)
        print(" RESULTADO: MODELO INVIABLE ".center(50, "="))
        print("=" * 50)
        print("No se encontró solución óptima: el problema es inviable (infeasible).")
        print(
            "Esto significa que no existe ninguna asignación posible que cumpla todas las restricciones dadas las personas, habilidades y requerimientos."
        )
        if results is not None and hasattr(results, "solver"):
            print(f"\nEstado del solver: {results.solver.termination_condition}")
            if hasattr(results.solver, "message") and results.solver.message:
                print(f"Mensaje del solver: {results.solver.message}")
        if time_elapsed is not None:
            print(f"\nTiempo de ejecución: {time_elapsed:.2f} segundos")
        print("=" * 50)

    def _project_efficiency(self, j: int) -> tuple:
        """Calcula la eficiencia de un proyecto (e_j)."""
        # Convertir el generador en una suma evaluada
        numerator = sum(
            pyo.value(
                self.model.S[i1, i2]
                * self.model.x_total[i1, j]
                * self.model.x_total[i2, j]
            )
            for i1 in self.model.P
            for i2 in self.model.P
        )
        # denominator = sum(pyo.value(self.model.R[j, k]) for k in self.model.K)
        T = sum(pyo.value(self.model.R[j, k]) for k in self.model.K)
        denominator = T**2

        ej = (1 + numerator / denominator) / 2 if denominator != 0 else 0.0
        # ej = (1 + numerator / denominator**2) / 2 if denominator != 0 else 0.0
        # ej = 0.5 * (1 + numerator / denominator**2) if denominator != 0 else 0.0
        return ej, numerator, denominator


if __name__ == "__main__":

    dataGen = DataGenerator()

    data = dataGen.generate_random_instance(
        num_people=20,  # Reducido para pruebas iniciales con el modelo más complejo
        num_projects=3,
        skills=[
            "Backend",
            "Frontend",
            "DevOps",
            "QA",
            "UX/UI",
        ],
        time_fractions=[0.0, 0.5, 1.0],
        positive_prob=0.3,
        seed=42,
    )

    start_time = time.time()
    optimizer = MTFP_Optimizer(data)
    results = optimizer.solve(solver="bonmin", tee=False)
    elapsed = time.time() - start_time
    if results.solver.termination_condition == pyo.TerminationCondition.optimal:
        optimizer.pretty_print(time_elapsed=elapsed)
    else:
        optimizer.pretty_print_infeasible(results=results, time_elapsed=elapsed)
