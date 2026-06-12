from Fonctions_utiles.fonctions import accord
from Models.ExerciceRealise import ExerciceRealise

class Seance:
    def __init__(self, date, duree):
        if duree <= 0:
            raise ValueError("Durée invalide")
        self.date = date
        self.duree = duree
        self.exercices_realises = []

    def ajouter_exercice(self, exercice_realise):
        self.exercices_realises.append(exercice_realise)

    @property
    def volume_total(self):
        return sum(e.volume_total for e in self.exercices_realises)
    
    @property
    def nb_exercices(self):
        return len(self.exercices_realises)
    
    def __str__(self):
        return f"Séance du {self.date} - Durée : {self.duree} min - {self.nb_exercices} {accord(self.nb_exercices, 'exercice', 'exercices')}, volume total : {self.volume_total:.1f} kg"

    def to_dict(self):
        return {"date": self.date, "duree": self.duree, "exercices": [e.to_dict() for e in self.exercices_realises]}

    @classmethod
    def from_dict(cls, donnees, catalogue_exercices):
        seance = cls(donnees["date"], donnees["duree"])
        for e_dict in donnees["exercices"]:
            exercice_realise = ExerciceRealise.from_dict(e_dict, catalogue_exercices)
            seance.ajouter_exercice(exercice_realise)
        return seance