import random
from faker import Faker
fake = Faker()


def fake_person():
    gender_id = fake.random_int(min=1, max=2)  # 1=female, 2=male

    if gender_id == 1:
        first = fake.first_name_female()
        last = fake.last_name_female()
    else:
        first = fake.first_name_male()
        last = fake.last_name_male()

    return {
            "first_name": first,
            "last_name": last,
            "birth_date": fake.date_of_birth(minimum_age=20, maximum_age=65).isoformat(),
            "gender_id": gender_id
        }


def fake_employee(person_id: int, jobs: dict) -> dict:
    if not jobs:
        raise ValueError("Jobs dict cannot be empty.")
    return {
            "pay": round(fake.random_number(digits=4) + fake.random.random(), 2),
            "description": fake.job(),
            "position": random.choice(list(jobs.values())),
            "person_id": person_id,
        }