from faker import Faker
fake = Faker('pl_PL')

class BaseContact:
    def __init__(self, fname, lname, phone, email):
        self.fname = fname
        self.lname = lname
        self.phone = phone
        self.email = email.lower()

    def __str__(self):
        return f"{self.fullname}, {self.phone}, {self.email}"
    
    @property
    def fullname(self):
        return f"{self.fname} {self.lname}"
    
    @property
    def label_length(self):
        return len(self.fullname)
    
    def contact(self):
        print(f"Wybieram numer {self.phone} i dzwonię do {self.fullname}")


class BusinessContact(BaseContact):
    def __init__(self, firm, position, workphone, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.firm = firm
        self.position = position
        self.phone = workphone
    
    def __str__(self):
        return f"{super().fullname}, {self.phone}, {self.firm}, {self.position}"


class ContactList(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.args = args
    
    def __repr__(self):
        reprs = (arg.__repr__() for arg in self.args)
        return f"ContactList{reprs}"

def _create_contacts(contact_class, quantity):
    if contact_class not in [BaseContact, BusinessContact]:
        raise ValueError("contact_class must be BaseContact or BusinessContact")
    for _ in range(quantity):
        fname = fake.first_name()
        lname = fake.last_name()
        phone = fake.phone_number()
        email = fake.email()
        if contact_class is BaseContact:
            yield BaseContact(fname, lname, phone, email)
        else:
            firm = fake.company()
            position = fake.job()
            workphone = fake.phone_number()
            yield BusinessContact(firm, position, workphone, fname, lname, phone, email)

def create_contacts(contact_class, quantity):
    return ContactList(_create_contacts(contact_class, quantity))

contacts = create_contacts(BusinessContact, 5)
print(contacts)

# RANDOM DATA
p1 = "Augustyn,Czerwinski,+48891524857,AugustynCzerwinski@einrot.com,Mages,Horticultural specialty farmer,+48935059320"
p2 = "Wawrzyniec,Symanski,+48534271296,WawrzyniecSymanski@jourrapide.com,Soul Sounds Unlimited,Wire installer,+48800262133"
p3 = "Kazimiera,Chmielewska,+48849183440,KazimieraChmielewska@fleckens.hu,Just For Feet,Tour escort,+48226534360"
p4 = "Anka,Sobczak,+48928746173,AnkaSobczak@cuvox.de,Sports Unlimited,Conservator,+48291927517"
p5 = "Iwona,Dudek,+48979124700,IwonaDudek@jourrapide.com,Argus Tapes & Records,Holistic nurse,+48941956594"

people = [data.split(",") for data in [p1, p2, p3, p4, p5]]
base_cards = [BaseContact(*person[:4]) for person in people]
business_cards = [BusinessContact(*person[4:], *person[:4]) for person in people]

if __name__ == "__main__":
    base_cards[0].contact()
    print(base_cards[0])
    business_cards[0].contact()
    print(business_cards[0])