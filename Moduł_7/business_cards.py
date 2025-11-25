from faker import Faker
fake = Faker('pl_PL')

class BaseContact:
    def __init__(self, fname, lname, phone, email):
        self.fname = fname
        self.lname = lname
        self.phone = phone
        self.email = email.lower()

    def __str__(self):
        """Display base contact information."""
        return f"{self.fullname}, {self.phone}, {self.email}"
    
    def __repr__(self):
        """Display detailed contact information."""
        return f"{self.fullname}, {self.phone}, {self.email}{self.additional_info}"
    
    @property
    def fullname(self):
        return f"{self.fname} {self.lname}"
    
    @property
    def label_length(self):
        return len(self.fullname)
    
    @property
    def contactphone(self):
        return self.phone
    
    @property
    def additional_info(self):
        return ""
    
    def contact(self):
        print(f"Wybieram numer {self.contactphone} i dzwonię do {self.fullname}")


class BusinessContact(BaseContact):
    def __init__(self, firm, position, workphone, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.firm = firm
        self.position = position
        self.workphone = workphone
    
    def __str__(self):
        """Display business contact information."""
        return f"{super().fullname}, {self.workphone}, {self.firm}, {self.position}"

    @property
    def contactphone(self):
        return self.workphone
    
    @property
    def additional_info(self):
        return f", Work phone: {self.workphone}, Company: {self.firm}, Position: {self.position}"

class ContactList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

def create_contacts(contact_class, quantity) -> ContactList[BaseContact | BusinessContact]:
    return ContactList(_create_contacts(contact_class, quantity))

pcards = create_contacts(BaseContact, 5)
bcards = create_contacts(BusinessContact, 5)

if __name__ == "__main__":
    print(pcards[0].__repr__())
    pcards[0].contact()
    print(bcards[0].__repr__())
    bcards[0].contact()