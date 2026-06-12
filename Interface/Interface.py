from Models.Serie import Serie
from Models.Exercice import Exercice
from Models.Seance import Seance
from Models.ExerciceRealise import ExerciceRealise

from Fonctions_utiles.fonctions import verifier_date, demander_entier_positif

from Constantes.Constantes import GROUPES_MUSCULAIRES, MUSCLES_CIBLES,MATERIELS

from Stats.Stats import volume_total_par_groupe_musculaire_seance

def lister_catalogue(carnet):
    if not carnet.exercices:
        print("Catalogue vide")
        return
    print(f"=== CATALOGUE DES EXERCICES ===\n")
    for exercice in carnet.exercices.values():
        print(f"[{exercice.id_exercice}] {exercice.nom} - {exercice.groupe_musculaire} : {exercice.muscle_cible} ({exercice.type_materiel})")

def saisir_exercice(carnet):
    print(f"--- Ajout d'un exercice au catalogue ---\n")
    while True:
        id_exercice = input("Saisis un ID d'exercice (ex: 001): ").strip().lower()
        if not id_exercice:
            print("L'ID ne peut pas être vide ")
            continue
        if id_exercice in carnet.exercices:
            print(f"ID déjà prise par : {carnet.exercices[id_exercice].nom}")
            continue
        break
    while True:
        nom = input("Nom de l'exercice : ").strip()
        if not nom:
            print("Le nom ne peut pas être vide")
            continue
        nom_deja_utilise = False
        for exercice in carnet.exercices.values():
            if nom.title() == exercice.nom.title():
                nom_deja_utilise = True
                print(f"Nom déjà utilisé par : {exercice.nom}")
                break
        if nom_deja_utilise:
            continue
        break
    while True:
        groupe_musculaire = input(f"Groupe musculaire ({', '.join(GROUPES_MUSCULAIRES)}) : ").strip().lower()
        if groupe_musculaire in GROUPES_MUSCULAIRES:
            break
        print("Groupe invalide")
    liste_muscles_cibles = []
    while True:
        muscle = input(f"Muscle ciblé ({', '.join(MUSCLES_CIBLES)}) ou 'fin' : ").strip().lower()
        if muscle == "fin":
            if liste_muscles_cibles:
                break
            print("Tu dois saisir au moins un muscle ciblé")
            continue
        if muscle not in MUSCLES_CIBLES:
            print("Saisis un muscle ciblé valide")
            continue
        if muscle in MUSCLES_CIBLES:
            print("muscle déjà présent")
            continue
        liste_muscles_cibles.append(muscle)
    while True:
        type_materiel = input(f"Type de matériel ({', '.join(MATERIELS)}) : ").strip().lower()
        if type_materiel in MATERIELS:
            break
        print("Matériel invalide") 
    exercice = Exercice(id_exercice, nom, groupe_musculaire, liste_muscles_cibles, type_materiel)
    carnet.ajouter_exercice(exercice)
    print(f"Exercice ajouté : [{id_exercice}] {nom}")



 
def saisir_seance(carnet):
    while True:
        date = input("Saisie une date : ")
        if verifier_date(date):
            break
        else:
            print("Saisie une date valide")
    while True:
        duree_saisie = input("Saisie une durée : ")
        try:
            if int(duree_saisie) > 0:
                duree = int(duree_saisie)
                break
            else:
                print("Saisie une durée valide")
        except ValueError:
            print("Saisie une valeur numérique")
            continue
    seance = Seance(date, duree)
    while True:
        lister_catalogue(carnet)
        if not carnet.exercices:
            print("Tu dois ajouter au moins un exercice au catalogue avant de saisir une séance")
            return
        id_exercice = input("Saisie l'id de l'exercice : ").strip().lower()
        if id_exercice == "fin":
            break
        if id_exercice not in carnet.exercices:
            print("Exercice inconnu")
            continue
        exercice = carnet.exercices[id_exercice]
        exercice_realise = ExerciceRealise(exercice)
        while True:
            poids = input("Poids utilisé : ")
            if poids.strip().lower() == "fin":
                break
            try:
                if float(poids) > 0:
                    poids_utilise = float(poids)
                else:
                    print("Saisie un poids valide")
                    continue
            except ValueError:
                print("Saisie un poids valide")
                continue
            reps_effectuees = demander_entier_positif("Reps effectuées : ")
            serie = Serie(poids_utilise, reps_effectuees)
            exercice_realise.ajouter_serie(serie)
        if exercice_realise.nb_series > 0:
            seance.ajouter_exercice(exercice_realise)
    if seance.nb_exercices > 0:
        carnet.ajouter_seance(seance)
        print(seance)
        print("\n=== Volume par groupe musculaire ===")
        for groupe, volume in volume_total_par_groupe_musculaire_seance(seance).items():
            print(f"  {groupe:15s} : {volume:.1f}")
    else:
        print("Séance annulée car aucun exercice valide n'a été saisi")
    
def afficher_records(carnet):
    id_exercices = carnet.liste_exercices_pratiques()
    if not id_exercices:
        print("Aucun exercice enregistré.")
        return
    else:
        print("Records par exercice :")
        for id_ex in id_exercices:
            exercice = carnet.exercices[id_ex]
            record = carnet.record_par_exercice(id_ex)
            print(f"{exercice.nom} :")
            print(f"    {record:.1f} kg")

def supprimer_seances(carnet):
    print("⚠️ Attention la suppression est définitive")
    while True:
        saisie = input("Confirmez-vous la suppression de toutes les séances ?")
        if saisie.strip().lower() == "non":
            print("Suppression annulée")
            break
        elif saisie.strip().lower() == "oui":
            print("Toutes les séances ont été supprimées")
            carnet.seances.clear()
            carnet.sauvegarder("carnet.json")
            break
        else:
            print("Réponse invalide, tape 'oui' ou 'non' ")
    

def afficher_menu():
    print(f"=== CARNET D'ENTRAÎNEMENT ===")
    print(f"1. Ajouter une séance")
    print(f"2. Voir l'historique")
    print(f"3. Voir le catalogue d'exercice")
    print(f"4. Ajouter un exercice au catalogue")
    print(f"5. Récap semaine")
    print(f"6. Évolution des charges")
    print(f"7. Exercices pratiqués par groupe")
    print(f"8. Mes records et 1RM")
    print(f"9. Supprimer les séances")
    print(f"0. Quitter")