from Apartment import Apartment
from DTO.DTO import DTO


class ApartmentDTO(DTO):
    def __init__(self, apartment: Apartment):
        self.apartment_number = apartment.apartment_number

    def to_json(self):
        return {
            'apartment_number': self.apartment_number,
        }
