varaus_list = []


def get_last_id():
    if varaus_list:
        last_varaus = varaus_list[-1]
    else:
        return 1
    return last_varaus.id + 1

class Varaus:

    def __init__(self, tila, paiva, aika, henkiloita, kuka, sahkoposti):
        self.id = get_last_id()
        self.tila = tila
        self.paiva = paiva
        self.aika = aika
        self.henkiloita = henkiloita
        self.kuka = kuka
        self.sahkoposti = sahkoposti
        self.is_publish = True

    @property
    def data(self):
        return{
            "id": self.id,
            "tila": self.tila,
            "päivä": self.paiva,
            "aika": self.aika,
            "henkilöitä": self.henkiloita,
            "kuka": self.kuka,
            "sähköposti": self.sahkoposti
        }