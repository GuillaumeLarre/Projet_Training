class Serie:
    def __init__(self, poids, reps):
        if poids <= 0 or reps <= 0:
            raise ValueError("valeur incorrecte")
        self.poids = poids
        self.reps = reps

    @property
    def volume(self):
        return round((self.poids * self.reps), 1)
    
    def __str__(self):
        return f"{self.poids:.1f} kg x {self.reps}"
    
    def to_dict(self):
        return {"poids": self.poids, "reps": self.reps}
    
    @classmethod
    def from_dict(cls, donnees):
        return cls(donnees["poids"], donnees["reps"])