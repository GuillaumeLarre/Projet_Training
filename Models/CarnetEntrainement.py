import json
from Models import Exercice, Seance


class CarnetEntrainement:
    def __init__(self):
        self.seances = []
        self.exercices = {}

    def ajouter_exercice(self, exercice):
        self.exercices[exercice.id_exercice] = exercice

    def ajouter_seance(self, seance):
        self.seances.append(seance)

    @property
    def nb_seances(self):
        return len(self.seances)

    @property
    def volume_total_global(self):
        return sum(s.volume_total for s in self.seances)
    
    def record_par_exercice(self, id_exercice):
        poids_record = 0
        for seance in self.seances:
            for exercice_realise in seance.exercices_realises:
                if exercice_realise.exercice.id_exercice == id_exercice:
                    for serie in exercice_realise.series:
                        if serie.poids > poids_record:
                            poids_record = serie.poids
        return poids_record
        
    def liste_exercices_pratiques(self):
        id_exercice_pratiques = set()
        for seance in self.seances:
            for exercice_realise in seance.exercices_realises:
                id_exercice_pratiques.add(exercice_realise.exercice.id_exercice)
        return list(id_exercice_pratiques)
    
    def afficher_historique(self):
            if len(self.seances) == 0:
                print("Aucune séance enregistrée")
            for seance in self.seances:
                print(seance)
                for exercice in seance.exercices_realises:
                    print(exercice)

    def to_dict(self):
        return {"seances": [s.to_dict() for s in self.seances], "exercices": [e.to_dict() for e in self.exercices.values()]}

    @classmethod
    def from_dict(cls, donnees):
        carnet = cls()
        for exercice_dict in donnees["exercices"]:
            exercice = Exercice.from_dict(exercice_dict)
            carnet.ajouter_exercice(exercice)
        for s_dict in donnees["seances"]:
            seance = Seance.from_dict(s_dict, carnet.exercices)
            carnet.ajouter_seance(seance)

        return carnet
    
    def sauvegarder(self, chemin):
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def charger(cls, chemin):
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)
            return cls.from_dict(donnees)
        except FileNotFoundError:
            return cls()