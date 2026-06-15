class Exercice:
    def __init__(self, id_exercice: str, nom: str, groupe_musculaire: str, muscle_cible: list[str], type_materiel: str) -> None:
        self.id_exercice = id_exercice
        self.nom = nom
        self.groupe_musculaire = groupe_musculaire
        self.muscle_cible = muscle_cible
        self.type_materiel = type_materiel

    def to_dict(self) -> dict:
        return {"id_exercice": self.id_exercice, "nom": self.nom, "groupe_musculaire": self.groupe_musculaire, "muscle_cible": self.muscle_cible, "type_materiel": self.type_materiel}

    @classmethod
    def from_dict(cls, donnees: dict) -> "Exercice":
        return cls(donnees["id_exercice"], donnees["nom"], donnees["groupe_musculaire"], donnees["muscle_cible"], donnees["type_materiel"])

    def __str__(self) -> str:
        return self.nom