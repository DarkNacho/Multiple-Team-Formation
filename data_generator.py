from onefile import DataGenerator

sizes = [(10, 2, 2), (20, 5, 4), (30, 5, 4), (50, 10, 8), (100, 10, 8)]

for n_people, n_projects, n_skills in sizes:
    skills = [f"Habilidad_{i+1}" for i in range(n_skills)]
    data = DataGenerator.generate_random_instance(
        num_people=n_people,
        num_projects=n_projects,
        skills=skills,
        time_fractions=[0.0, 0.5, 1.0],
        positive_prob=0.3,
        seed=42 + n_people + n_projects + n_skills,
    )
    fname = (
        f"test_cases/escalabilidad/escala_{n_people}p_{n_projects}pr_{n_skills}sk.json"
    )
    DataGenerator.save_to_json(data, fname)
