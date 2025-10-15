shopping_list = {
    "Piekarnia": ["chleb", "bułki", "pączek"],
    "Warzywniak": ["marchew", "seler", "rukola"],
}

cnt = 0

print("Lista zakupów:")
for store in shopping_list:
    print(f"Idę do {store} i kupuję tam: {shopping_list[store]}.")
    cnt += len(shopping_list[store])
print(f"W sumie kupuję {cnt} produktów.")

# print("\nInne formatowanie:")
# for store, prod in shopping_list.items():
#     print(f"Idę do {store} i kupuję tam:", end=" ")
#     for item in prod:
#         print(f"{item}", end=", " if item != prod[-1] else ".\n")