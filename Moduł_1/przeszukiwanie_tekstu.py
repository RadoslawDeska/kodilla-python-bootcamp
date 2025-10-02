text = """– Czemu tak ciągle gadasz o kobietach, Stan?
– Bo chcę zostać kobietą. Chcę być kobietą. Chce żebyście od dziś mówili na mnie „Loretta”. To moje niezbywalne prawo jako mężczyzny.
– Ale dlaczego chcesz zostać Lorettą, Stan?
– Bo chcę mieć dzieci.
– Dzieci?
– Każdy mężczyzna ma prawo mieć dzieci, jeśli chce.
– Przecież ty nie możesz mieć dzieci!
– Nie prześladuj mnie!
– Nie prześladuję cię, Stan! Nie masz macicy! Gdzie będziesz trzymał swojego embriona? W pudełku?
– Mam pomysł! Przyjmijmy, że Stan nie może póki co mieć dzieci, gdyż nie ma macicy, co nie jest niczyją winą, nawet Rzymian, ale musimy przyznać, że ma prawo do dzieci!
– Świetnie, Judith! Będziemy walczyć z ciemiężycielami…
– Przepraszam.
– A po co?
– Co po co?
– Po co walczyć o jego prawo do posiadania dzieci…
– To symbol naszej beznadziejnej walki z najeźdźcą.
– Symbol jego beznadziejnej walki z rzeczywistością."""

number_of_a = text.count('a')
number_of_e = text.count('e')
number_of_i = text.count('i')
number_of_o = text.count('o')
number_of_u = text.count('u')
number_of_y = text.count('y')

print(f"Liczba małych 'a': {number_of_a}, małych i dużych: {text.lower().count('a')}")
print(f"Liczba małych 'e': {number_of_e}, małych i dużych: {text.lower().count('e')}")
print(f"Liczba małych 'i': {number_of_i}, małych i dużych: {text.lower().count('i')}")
print(f"Liczba małych 'o': {number_of_o}, małych i dużych: {text.lower().count('o')}")
print(f"Liczba małych 'u': {number_of_u}, małych i dużych: {text.lower().count('u')}")
print(f"Liczba małych 'y': {number_of_y}, małych i dużych: {text.lower().count('y')}")