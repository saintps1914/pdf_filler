from typing import Dict, List, Optional
import fitz
from pathlib import Path
import random
from faker import Faker
from datetime import datetime
from dateutil import parser

fake = Faker()

random_data = {
    "first_name": fake.first_name(),
    "last_name": fake.last_name(),
    "dob": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
    "ssn": f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}",
    "phone": fake.phone_number(),
    "email": fake.email(),
    "address": fake.street_address().replace("\n", " "),
    "city": fake.city(),
    "state": fake.state(),
    "zip_code": fake.zipcode(),
    "company_name": fake.company(),
    "company_address": fake.street_address().replace("\n", " "),
    "company_city": fake.city(),
    "company_state": fake.state(),
    "company_zip": fake.zipcode(),
    "ein": f"{random.randint(100000000, 999999999)}",
    "date_of_incorporation": fake.date_this_century().isoformat(),
}


name_pdf_template_map = {
    "csf": "CFS.pdf",
    "amur": "Amur.pdf",
    "brobas": "Brobas.pdf",
    "keystone": "Keystone.pdf",
    "translease": "Translease.pdf",
    "aladdin": "Aladdin.pdf",
    "priority": "Priority.pdf",
    "mitsu": "Mitsu.pdf",
    "crossroads": "Crossroads.pdf",
    "darla": "Darla.pdf",
    "cefi": "Cefi.pdf",
    "huntington": "Huntington.pdf",
    "peter_brakner": "PeterBrakner.pdf",
    "blue_bridge": "BlueBridge.pdf",
    "quality_equipment": "QualityEquipment.pdf",
    "george_finance": "GeorgeFinance.pdf",
    "gandr": "GandR.pdf",
    "fast_lane": "Fast Lane Leasing Credit Application.pdf",
    "tk_pmb": "Credit Application_TK-PMB.pdf",
}

coordinates = {
    "csf": {
        0: {  # Company Information
            "company_name": (150, 168),
            "company_address": (150, 190),
            "phone": [(150, 212), (150, 352)],
            "email": [(150, 234), (410, 352)],
            "company_city": (340, 190),
            "company_state": (460, 190),
            "company_zip": (524, 190),
            "date_of_incorporation": (460, 212),
            "ein": (460, 234),
            # Officer Information
            "name": (150, 283),
            "address": (150, 305),
            "dob": (150, 330),
            "title": (340, 283),
            "ownership": (525, 283),
            "city": (340, 305),
            "state": (460, 305),
            "zip_code": (524, 305),
            "ssn": (340, 330),
            # Signatures
            "applicant_1_date": (490, 743),
        }
    },
    "amur": {
        0: {  # Company Information
            "company_name": (45, 152),
            "company_address": (45, 180),
            "company_city": (230, 180),
            "state": [(355, 180), (400, 357)],
            "county": (400, 180),
            "company_zip": (500, 180),
            "phone": [(45, 206), (45, 385)],
            "date_of_incorporation": (400, 210),
            "ein": (400, 235),
            # Personal Information
            "name": (45, 330),
            "ownership": (320, 330),
            "title": (400, 330),
            "address": (45, 357),
            "city": (230, 357),
            "zip_code": (500, 357),
            "email": (400, 385),
            "ssn": (45, 412),
            # Footer
            "applicant_1_name": (300, 735),
            "applicant_1_date": (470, 735),
            "officer_1_signature": (45, 735),
        }
    },
    "brobas": {
        0: {  # Company Information
            "company_name": (75, 129),
            "ein": (350, 129),
            "company_address": (75, 149),
            "company_city": (440, 149),
            "company_state": (600, 149),
            "company_zip": (680, 149),
            "phone": [(75, 169), (614, 244)],
            "email": (430, 169),
            # Officer Information
            "name": (75, 223),
            "address": (75, 244),
            "city": (320, 244),
            "state": (490, 244),
            "zip_code": (560, 244),
            "ssn": (500, 223),
            "dob": (700, 244),
            "ownership": (705, 223),
            "title": (307, 223),
            "years_in_business": (430, 190),
            # Footer
            "applicant_1_name": (110, 425),
            "applicant_1_date": (650, 425),
        }
    },
    "keystone": {
        0: {  # Company Information
            "company_name": (110, 175),
            "company_address": (110, 208),
            "company_city_state_zip": (110, 225),
            "bus_phone": (105, 271),
            "date_of_incorporation": (120, 367),
            "ein": (120, 383),
            "email": (110, 303),
            "contact": (110, 317),
            "title": [(220, 317), (430, 573)],
            "phone": [(220, 335), (500, 590)],
            # Owner Information
            "name": (102, 573),
            "ssn": (325, 573),
            "ownership": (545, 573),
            "person_address": (102, 590),
            # Footer
            "applicant_1_name": (290, 732),
            "applicant_1_date": (510, 732),
        }
    },
    "translease": {
        0: {  # Company Information
            "company_name": (225, 116),
            "company_address": (110, 158),
            "company_city": (218, 158),
            "company_state": (285, 158),
            "company_zip": (321, 158),
            "country": (495, 158),
            "phone": [(110, 200), (107, 430)],
            "email": (247, 200),
            "date_of_incorporation": (500, 116),
            # Owner Information
            "name": (107, 376),
            "ssn": (195, 391),
            "person_address": (107, 410),
            "dob": (107, 391),
            "ownership": (107, 443),
            # Signatures
            "applicant_1_name": (60, 750),
            "applicant_1_date": (256, 750),
        }
    },
    "aladdin": {
        0: {  # Company Information
            "company_name": (110, 96),
            "company_address": (50, 132),
            "company_city": (315, 132),
            "company_state": (450, 132),
            "company_zip": (520, 132),
            "ein": (315, 158),
            "phone": [(180, 158), (315, 446)],
            "email": (335, 390),
            "date_of_incorporation": (50, 185),
            # Owner Information
            "name": (70, 387),
            "ssn": (180, 446),
            "address": (50, 420),
            "city": (315, 420),
            "state": (450, 420),
            "zip_code": (520, 420),
            "dob": (50, 446),
            # Signatures
            "applicant_1_name": (100, 757),
            "applicant_1_date": (245, 732),
        }
    },
    "priority": {
        0: {  # Company Information
            "company_name": (130, 100),
            "company_address": (90, 120),
            "company_city_state_zip": (360, 120),
            "ein": (490, 175),
            "name": [(145, 260), (100, 155)],
            "phone": [(110, 175), (480, 277)],
            "email": (360, 155),
            "date_of_incorporation": (130, 140),
            # Owner Information
            "ssn": (485, 260),
            "person_address": (100, 277),
            "dob": (365, 295),
            "ownership": (345, 260),
            # Signatures
            "applicant_1_name": (360, 730),
            "applicant_1_date": (500, 735),
        }
    },
    "mitsu": {
        0: {  # Company Information
            "company_name": (165, 137),
            "company_address": (100, 152),
            "company_city": (55, 165),
            "company_state": (180, 165),
            "company_zip": (250, 165),
            "ein": (220, 190),
            "phone": [(60, 175), (225, 315)],
            "email": [(360, 185), (415, 315)],
            "date_of_incorporation": (105, 186),
            "title": (345, 330),
            # Owner Information
            "name": (180, 290),
            "ssn": (450, 290),
            "address": (40, 305),
            "city": (200, 305),
            "state": (285, 305),
            "zip_code": (340, 305),
            "dob": (335, 315),
            "ownership": (100, 330),
            # Signatures
            "applicant_1_name": (100, 745),
            "applicant_1_date": (300, 745),
        }
    },
    "crossroads": {
        0: {
            # Company Information
            "company_name": (105, 70),
            "company_address": (115, 87),
            "company_city": (90, 105),
            "company_state": [(260, 105), (265, 157)],
            "company_zip": (345, 105),
            "ein": (435, 70),
            "phone": [(480, 87), (480, 105), (345, 255)],
            "title": (260, 123),
            "email": [(345, 240), (348, 123)],
            "ssn": [(70, 140), (130, 255)],
            "years_in_business": (260, 140),
            "date_of_incorporation": [(130, 157)],
            "title": [(255, 150)],
            # Owner Information
            "name": [(105, 123), (90, 240)],
            "dob": (250, 240),
            "ownership": (270, 255),
            "person_address": (95, 272),
            # Signatures
            "applicant_1_name": (110, 745),
            "applicant_1_date": (510, 745),
        }
    },
    "darla": {
        0: {
            # Company Information
            "company_name": (50, 610),
            "company_address": (50, 675),
            "company_city": (315, 675),
            "company_state": (470, 675),
            "company_zip": (520, 675),
            "ein": (470, 610),
            # Owner Information
            "first_name": (50, 440),
            "last_name": (350, 440),
            "address": (50, 470),
            "city": (315, 470),
            "state": (460, 470),
            "zip_code": (520, 470),
            "phone": (450, 540),
            "email": (200, 540),
            "date_of_incorporation": (50, 645),
            "title": (255, 610),
            "dob": (50, 505),
            "ownership": (410, 610),
        },
        1: {
            "ssn": (50, 705),
            # Signatures
            "applicant_1_name": (50, 740),
            "applicant_1_date": (430, 740),
        },
    },
    "cefi": {
        0: {
            # Company Information
            "company_name": (80, 152),
            "company_address": (80, 205),
            "company_city": (75, 240),
            "company_state": (155, 240),
            "company_zip": (228, 240),
            "ein": (313, 170),
            # Owner Information
            "name": [(315, 223), (80, 320)],
            "address": (80, 352),
            "city": (315, 352),
            "state": None,
            "zip_code": (420, 352),
            "phone": [(315, 257), (315, 152), (525, 320)],
            "email": (315, 273),
            "date_of_incorporation": (311, 205),
            "title": [(315, 240), (315, 320)],
            "dob": (315, 337),
            "ownership": (255, 337),
            "ssn": (420, 320),
            # Signatures
            "applicant_1_name": (280, 660),
            "applicant_1_date": (480, 660),
        },
    },
    "huntington": {
        0: {
            # Company Information
            "company_name": (205, 170),
            "company_address": (118, 195),
            "company_city_state_zip": (130, 218),
            "ein": (80, 288),
            # Owner Information
            "name": (65, 467),
            "address": (103, 490),
            "person_city_state_zip": (405, 490),
            "phone": [(430, 218), (357, 514)],
            "email": None,
            "date_of_incorporation": (395, 250),
            "title": None,
            "dob": (375, 537),
            "ownership": None,
            "ssn": (110, 537),
        },
    },
    "peter_brakner": {
        0: {
            # Company Information
            "company_name": (150, 84),
            "years_in_business": (307, 84),
            "ein": (340, 84),
            "company_state_year": (392, 84),
            "company_address": [(143, 136), (143, 154)],
            "company_city": [(235, 136), (235, 154)],
            "company_state": [(295, 136), (295, 154)],
            "company_zip": [(350, 136), (350, 154)],
            # Owner Information
            "name": (150, 102),
            "ownership": (305, 102),
            "ssn": (340, 102),
            "dob": (405, 102),
            "phone": [(150, 172), (230, 172)],
            "email": (270, 207),
            # Signatures
            "applicant_1_name": (350, 655),
            "applicant_1_date": (350, 709),
        },
    },
    "blue_bridge": {
        0: {
            # Company Information
            "company_name": (120, 232),
            "company_address": (120, 253),
            "company_city": (75, 274),
            "company_state": (230, 274),
            "company_zip": (400, 274),
            "date_of_incorporation": (120, 316),
            "ein": (410, 316),
            "phone": [(75, 295), (85, 463)],
            "email": [(410, 295), (270, 463)],
            # Owner Information
            "name": (85, 400),
            "ssn": (400, 400),
            "address": (75, 421),
            "city": (65, 442),
            "state": (270, 442),
            "zip_code": (410, 442),
            # "ownership": (490, 484),
        },
        1: {
            # Signatures
            "applicant_1_name": (35, 130),
            "applicant_1_date": (100, 155),
        },
    },
    "quality_equipment": {
        0: {
            # Company Information
            "company_name": (155, 195),
            "company_address": (160, 225),
            "company_city": (100, 242),
            "company_state": (295, 242),
            "company_zip": (460, 242),
            "date_of_incorporation": (160, 259),
            "ein": (420, 259),
            "email": (150, 276),
            "phone": [(460, 276), (415, 343), (420, 480)],
            # Owner Information
            "first_name": (135, 311),
            "last_name": (390, 311),
            "dob": (145, 327),
            # "ownership": None,
            "ssn": (190, 343),
            "address": (150, 360),
            "city": (100, 378),
            "state": (295, 378),
            "zip_code": (460, 378),
        },
        1: {
            # Signatures
            "applicant_1_name": (320, 567),
            "applicant_1_date": (470, 567),
        },
    },
    "george_finance": {
        0: {
            "company_name": (130, 207),
            "company_address": (90, 227),
            "phone": [(130, 247), (120, 372)],
            "email": [(120, 267), (340, 372)],
            "company_city": (290, 227),
            "company_state": (445, 227),
            "company_zip": (515, 227),
            "date_of_incorporation": (380, 247),
            "ein": (310, 267),
            # Officer Information
            "name": (85, 312),
            "address": (85, 332),
            "dob": (75, 352),
            "title": (290, 312),
            # "ownership": (525, 283),
            "city": (290, 332),
            "state": (435, 332),
            "zip_code": (515, 332),
            "ssn": (290, 352),
            # Signatures
            "applicant_1_name": (130, 788),
            "applicant_1_date": (470, 788),
        }
    },
    "gandr": {
        0: {  # Company Information
            "company_name": (150, 225),
            "company_address": (110, 247),
            "phone": [(150, 270), (150, 410)],
            "email": [(150, 295), (400, 410)],
            "company_city": (340, 247),
            "company_state": (460, 247),
            "company_zip": (524, 247),
            "date_of_incorporation": (460, 270),
            "ein": (360, 295),
            # Officer Information
            "name": (110, 340),
            "address": (110, 363),
            "dob": (110, 385),
            "title": (340, 340),
            "ownership": (525, 340),
            "city": (340, 363),
            "state": (460, 363),
            "zip_code": (524, 363),
            "ssn": (340, 385),
            # Signatures
            "applicant_1_name": (170, 800),
            "applicant_1_date": (480, 800),
        }
    },
}

form_field_map = {
    "fast_lane": {
        "Business Name": "company_name",
        "Business Address": "company_address",
        "Bus City": "company_city",
        "Bus State": "company_state",
        "Bus Zip": "company_zip",
        "Bus Telephone": "phone",
        "Email": "email",
        "Federal ID": "ein",
        "Bus Years": "years_in_business",
        "Name 1": "name",
        "DOB 1": "dob",
        "Own 1": "ownership",
        "SSN 1": "ssn",
        "Phone 1": "phone",
        "Cell 1": "phone",
        "Address 1": "address",
        "City 1": "city",
        "State 1": "state",
        "Zip 1": "zip_code",
        "Date 1": "applicant_1_date",
    },
    "tk_pmb": {
        "BUSINESS NAME": "company_name",
        "Year Started": "year_started",
        "Office": "phone",
        "Contact": "name",
        "Email": "email",
        "Mailing Address": "company_address",
        "City": "company_city",
        "State": "company_state",
        "ZIP": "company_zip",
        "Tax ID": "ein",
        "BUSINESS OWNER 1": "name",
        "Soc Sec": "ssn",
        "Date Of Birth": "dob",
        "Address": "address",
        "City_2": "city",
        "State_2": "state",
        "ZIP_2": "zip_code",
        "Years Exp": "years_in_business",
        "Ownership": "ownership",
        "Business Owner": "name",
        "Date": "applicant_1_date",
    },
}

coordinates["fast_lane"] = {"__widgets__": form_field_map["fast_lane"]}
coordinates["tk_pmb"] = {"__widgets__": form_field_map["tk_pmb"]}


def convert_date(date: str, format: str) -> str:
    parsed_date = parser.parse(date)
    return parsed_date.strftime(format)

def normalize_data(data: Dict) -> Dict:
    data = dict(data)
    parsed_dob = convert_date(data.get("dob", ""), "%m-%d-%Y")
    data["dob"] = parsed_dob

    if "name" not in data:
        data["name"] = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
    if "company_city_state_zip" not in data:
        data["company_city_state_zip"] = (
            f"{data.get('company_city', '-')} / {data.get('company_state', '-')} / {data.get('company_zip', '-')}"
        )
    if "person_address" not in data:
        data["person_address"] = (
            f"{data.get('address', '-')} / {data.get('city', '-')} / {data.get('state', '-')} / {data.get('zip_code', '-')}"
        )
    if "person_city_state_zip" not in data:
        data["person_city_state_zip"] = (
            f"{data.get('city', '-')} / {data.get('state', '-')} / {data.get('zip_code', '-')}"
        )
    if "applicant_1_name" not in data:
        data["applicant_1_name"] = data.get("name", "")
    if "applicant_1_date" not in data:
        data["applicant_1_date"] = datetime.now().date().strftime("%m-%d-%Y")
    if "years_in_business" not in data:
        parsed_date = parser.parse(data.get("date_of_incorporation", ""))
        today = datetime.today()
        delta = today - parsed_date
        years = int(delta.days / 365.25)
        data["date_of_incorporation"] = parsed_date.strftime("%m-%d-%Y")
        data["years_in_business"] = str(years)
    if "company_state_year" not in data:
        data["company_state_year"] = (
            f"{data.get('company_state', '-')} / {data.get('date_of_incorporation', '-')}"
        )
    if "ownership" not in data:
        data["ownership"] = "100"
    if "year_started" not in data:
        try:
            parsed_date = parser.parse(data.get("date_of_incorporation", ""))
            data["year_started"] = parsed_date.strftime("%Y")
        except Exception:
            data["year_started"] = ""

    return data

def fill_pdf_form_fields(
    template_path: Path,
    save_file_path: Path,
    data: Dict,
    field_map: Dict[str, str],
) -> None:
    pdf_document = fitz.open(template_path)
    data = normalize_data(data)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        for widget in page.widgets() or []:
            field_name = widget.field_name
            data_key = field_map.get(field_name)
            if not data_key:
                continue
            value = data.get(data_key, "")
            if value is None:
                value = ""
            widget.field_value = str(value)
            widget.update()

    pdf_document.save(save_file_path)

def fill_pdf_by_coordinates(
    template_path: Path,
    save_file_path: Path,
    data: Dict,
    coordinates: Dict,
    font_size: int = 12,
) -> None:
    if coordinates is None:
        raise ValueError("Coordinates are required for non-form PDFs.")

    if "__widgets__" in coordinates:
        field_map = coordinates["__widgets__"]
        return fill_pdf_form_fields(template_path, save_file_path, data, field_map)

    pdf_document = fitz.open(template_path)
    data = normalize_data(data)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        page_coordinates = coordinates.get(page_num, None)
        if not page_coordinates:
            break

        for key, value in data.items():
            field_coordinates = page_coordinates.get(key, None)
            if not field_coordinates:
                continue

            if isinstance(field_coordinates, list):
                for fc in field_coordinates:
                    page.insert_text(fc, value.strip(), fontsize=font_size)
            else:
                page.insert_text(field_coordinates, value.strip(), fontsize=font_size)

    pdf_document.save(save_file_path)


if __name__ == "__main__":
    fill_pdf_by_coordinates(
        Path(__file__).resolve().parent.parent
        / "applications"
        / name_pdf_template_map["crossroads"],
        Path("Crossroads.pdf"),
        random_data,
        coordinates["crossroads"],
        font_size=8,
    )
