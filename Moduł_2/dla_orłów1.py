exam_points = {
  "Mariusz":30,
  "Mateusz":55,
  "Marta":76,
  "Roman":30,
  "Arleta":59,
  "Adrian": 96,
  "Monika":91,
  "Andrzej":22,
  "Krzysztof":83,
  "Krystyna":93,
  "Piotr":44,
  "Dawid":10,
  "Agnieszka":15
}

failed_students = []  # Nie zdali egzaminu. Są to wszyscy uczniowie z oceną niedostateczny. 
top_students = []  # Zdali egzamin śpiewająco! Są to wszyscy uczniowie z oceną 'bardzo dobry'.
best_student = ("",0)   # Nauczyciel chciałby też znać imię najlepszego ucznia oraz liczbę punktów,
                        # jaką uzyskał podczas egzaminu. Zapisz tę informację w postaci krotki,
                        # której pierwszą wartością będzie imię ucznia, a drugą wartością będzie liczba punktów.

# Skala ocen
# 0 - 45 niedostateczny 46 - 60 dopuszczający 61 - 75 dostateczny 76 - 90 dobry 91 - 100 bardzo dobry

top_score = max(exam_points.values())
for student, points in exam_points.items():
    if points <= 45:
        failed_students.append(student)
    elif points >= 91:
        top_students.append(student)

    # TO NADPISUJE JEŻELI JEST WIĘCEJ O TEJ SAMEJ MAX. LICZBIE PUNKTÓW
    if points == top_score:
        best_student = (student, points)

# TO PODAJE WSZYSTKICH O TEJ SAMEJ MAX. LICZBIE PUNKTÓW
exam_points["Krystyna"] = 96
best_students = [(student, points) for student, points in exam_points.items() if points == top_score]

print(f"{failed_students=}")
print(f"{top_students=}")
print(f"{best_student=}")
print(f"{best_students=}")