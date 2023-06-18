import random
import string
import json
from datetime import datetime, timedelta

def generate_fake_user():
    fake_user = {
        "_id": generate_id(),
        "type": "individual",
        "businessUnit": "BLFR",
        "logins": {
            "email": generate_email()
        },
        "phoneNumbers": generate_phone_numbers(),
        "emails": [
            {
                "email": generate_email(),
                "default": True
            }
        ],
        "gender": random.choice(["man", "woman"]),
        "firstName": generate_name(),
        "lastName": generate_name(),
        "birthdate": generate_birthdate(),
        "favouriteStores": generate_favourite_stores(),
        "addresses": generate_addresses(),
        "consents": generate_consents(),
        "createdDate": generate_date(),
        "updatedDate": generate_date(),
        "updatedBy": generate_id(),
        "source": generate_source(),
        "version": random.randint(1, 10)
    }
    return fake_user

def generate_source():
    return random.choice(["WEB", "MAGASIN", "MOBILE", "SUPPORT", "MARKETPLACE"]),

def generate_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_email():
    username = ''.join(random.choices(string.ascii_lowercase, k=4))
    domain = ''.join(random.choices(string.ascii_lowercase, k=4))
    return f"{username}@{domain}.com"

def generate_phone_numbers():
    phone_numbers = []
    default_number = {
        "number": generate_phone_number(),
        "default": True
    }
    phone_numbers.append(default_number)
    
    for _ in range(random.randint(1, 3)):
        phone_number = {
            "number": generate_phone_number(),
            "default": False
        }
        phone_numbers.append(phone_number)
    
    return phone_numbers

def generate_phone_number():
    return "+336" + ''.join(random.choices(string.digits, k=8))

def generate_name():
    name_length = random.randint(4, 10)
    return ''.join(random.choices(string.ascii_letters, k=name_length))

def generate_birthdate():
    start_date = datetime.strptime('1900-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2005-01-01', '%Y-%m-%d')
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime('%Y-%m-%d')

def generate_favourite_stores():
    stores = []
    for _ in range(random.randint(1, 3)):
        store = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        stores.append(store)
    return stores

def generate_addresses():
    addresses = []
    for address_id in range(2):
        address = {
            "type": random.choice(["BILLING", "SHIPPING"]),
            "id": random.randint(0, 1),
            "title": "Maison",
            "default": True,
            "addressLine1": generate_street_address(),
            "addressLine2": generate_apartment(),
            "addressLine3": generate_residence(),
            "addressLine4": generate_building(),
            "postalCode": generate_postal_code(),
            "city": generate_city(),
            "country": "FRA",
            "recipientPhoneNumber": generate_phone_number()
        }
        addresses.append(address)
    return addresses

def generate_street_address():
    street_types = ["Rue", "Avenue", "Boulevard", "Impasse", "Place", "Allée"]
    street_name = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 10)))
    street_type = random.choice(street_types)
    street_number = random.randint(1, 500)
    return f"{street_number} {street_type} {street_name}"

def generate_apartment():
    apartment_number = random.randint(1, 50)
    return f"Appt {apartment_number}"

def generate_residence():
    residence_name = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 10)))
    return f"Résidence {residence_name}"

def generate_building():
    building_number = random.randint(1, 10)
    building_name = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 10)))
    return f"{building_number} {building_name}"

def generate_postal_code():
    return ''.join(random.choices(string.digits, k=5))

def generate_city():
    cities = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"]
    return random.choice(cities)

def generate_consents():
    consents = []
    consent_types = ["opt-in", "opt-out"]
    consent_granted = [True, False]
    consent_names = ["MAIL", "SMS", "NEWSLETTER", "SURVEY", "CONTACT_REFUSED"]
    for consent_name in consent_names:
        consent = {
            "type": consent_name,
            "consent-type": random.choice(consent_types),
            "granted": random.choice(consent_granted)
        }
        consents.append(consent)
    return consents

def generate_date():
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.now()
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    return random_date.strftime('%Y-%m-%dT%H:%M:%SZ')

num_documents = 100000
fake_user_documents = []

for _ in range(num_documents):
    fake_user = generate_fake_user()
    with open("fake_user_documents.json", "a") as myfile:
        myfile.write(json.dump(fake_user))