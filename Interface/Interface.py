from models.Serie import Serie
from models.Exercice import Exercice
from models.Seance import Seance
from models.ExerciceRealise import ExerciceRealise
from models.CarnetEntrainement import CarnetEntrainement

from fonctions_utiles.fonctions import verifier_date, demander_entier_positif

from constantes.constantes import GROUPES_MUSCULAIRES, MUSCLES_CIBLES,MATERIELS

from stats.stats import volume_total_par_groupe_musculaire_seance

import logging
logger = logging.getLogger(__name__)

##############################################################
# Les fonctions répondant aux menus #
def lister_catalogue(carnet: CarnetEntrainement) -> None:
    if not carnet.exercices:
        print("Catalogue vide")
        return
    print(f"=== CATALOGUE DES EXERCICES ===\n")
    for exercice in carnet.exercices.values():
        print(f"[{exercice.id_exercice}] {exercice.nom} - {exercice.groupe_musculaire} : {exercice.muscle_cible} ({exercice.type_materiel})")

def saisir_exercice(carnet: CarnetEntrainement) -> None:
    print(f"--- Ajout d'un exercice au catalogue ---\n")
    while True:
        id_exercice = input("Saisis un ID d'exercice (ex: 001): ").strip().upper()
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
        if muscle in liste_muscles_cibles:
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
 
def saisir_seance(carnet: CarnetEntrainement) -> None:
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
        saisir_series(exercice_realise)
        if exercice_realise.nb_series > 0:
            seance.ajouter_exercice(exercice_realise)
    if seance.nb_exercices > 0:
        carnet.ajouter_seance(seance)
        print(seance)
        logger.info(f"Nouvelle séance saisie par l'utilisateur: {seance.date}")
        print("\n=== Volume par groupe musculaire ===")
        for groupe, volume in volume_total_par_groupe_musculaire_seance(seance).items():
            print(f"  {groupe:15s} : {volume:.1f}")
    else:
        print("Séance annulée car aucun exercice valide n'a été saisi")
    
def afficher_records(carnet: CarnetEntrainement) -> None:
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

def supprimer_seances(carnet: CarnetEntrainement) -> None:
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

def modifier_seance(carnet: CarnetEntrainement) -> None:
    seance_trouvee = None
    while True:
        date_seance = input("Saisie une date : ")
        if verifier_date(date_seance):
            break
        else:
            print("Saisie une date valide")
    for seance in carnet.seances:
        if seance.date == date_seance:
            seance_trouvee = seance
            break
    if seance_trouvee is None:
        print("Aucune séance enregistrée à cette date")
        return
    while True:
        afficher_sous_menu()
        saisie_choix = input("Choisis une option :")
        if not saisie_choix.isdigit():
            print("Saisis un chiffre")
            continue
        if saisie_choix == "1":
            while True:
                saisie_nouvelle_date = input("Entre la nouvelle date ")
                if verifier_date(saisie_nouvelle_date):
                    date_deja_utilisee = False
                    for seance in carnet.seances:
                        if seance is not seance_trouvee and seance.date == saisie_nouvelle_date:
                            date_deja_utilisee = True
                            break
                    if date_deja_utilisee:
                        print("Date de séance déjà enregistrée ")
                    else:
                        seance_trouvee.date = saisie_nouvelle_date
                        print("Date modifiée ")
                        carnet.sauvegarder("carnet.json")
                        break
                else:
                    print("Entre une date valide ")

        elif saisie_choix == "2":
            saisie_duree = demander_entier_positif("Saisie la nouvelle durée ")
            seance_trouvee.duree = saisie_duree
            print("Durée modifiée")
            carnet.sauvegarder("carnet.json")

        elif saisie_choix == "3":
            lister_catalogue(carnet)
            id_exercice = input("Saisie l'id de l'exercice : ").strip().upper()
            if id_exercice not in carnet.exercices:
                print("Exercice inconnu")
                continue
            exercice = carnet.exercices[id_exercice]
            exercice_realise = ExerciceRealise(exercice)
            saisir_series(exercice_realise)
            if len (exercice_realise.series) > 0:
                seance_trouvee.ajouter_exercice(exercice_realise)
                print("Exercice ajouté ")
                carnet.sauvegarder("carnet.json")
            else:
                print("Exercice annulé, aucune série saisie ")

        elif saisie_choix == "4":
            exercice_trouve = choisir_exercice_realise_dans_seance(seance_trouvee, carnet)
            if exercice_trouve is None:
                continue
            print("⚠️ Attention la suppression est définitive")
            while True:
                saisie = input("Confirmez-vous la suppression de l'exercice (o/n) ?")
                if saisie.strip().lower() in ("non", "n"):
                    print("Suppression annulée")
                    break
                elif saisie.strip().lower() in ("oui", "o"):
                    print("L'exercice a été supprimé")
                    seance_trouvee.exercices_realises.remove(exercice_trouve)
                    carnet.sauvegarder("carnet.json")
                    break
                else:
                    print("Réponse invalide, tape 'oui' ou 'non'")

        elif saisie_choix == "5":
            exercice_realise_trouve = choisir_exercice_realise_dans_seance(seance_trouvee, carnet)
            if exercice_realise_trouve is None:
                continue
            index_serie = choisir_index_serie(exercice_realise_trouve)
            if index_serie is None:
                continue
            serie_a_modifier = exercice_realise_trouve.series[index_serie]
            afficher_sous_menu_modification_serie()
            while True:
                saisie = input("Saisie une option ")
                if saisie in ("1", "2", "3", "0"):
                    break
                else:
                    print("Option invalide ")
            if saisie == "1":
                while True:
                    try:
                        saisie_poids = input("Saisie un poids pour la série ")
                        if float(saisie_poids) > 0:
                            nouveau_poids = float(saisie_poids)
                            break
                    except ValueError:
                        print("Poids invalide ")
                        continue
                serie_a_modifier.poids = nouveau_poids
                carnet.sauvegarder("carnet.json")
                print("Poids modifié ")
            elif saisie == "2":
                nouvelles_reps = demander_entier_positif("Reps effectuées : ")
                serie_a_modifier.reps = nouvelles_reps
                carnet.sauvegarder("carnet.json")
                print("Nouvelles répétitions enregistrées ")
            elif saisie == "3":
                while True:
                    demande_echauffement = input("S'agit il d'une série d'échauffement ? (o/n)")
                    if demande_echauffement.strip().lower() in ("o", "oui"):
                        echauffement = True
                        break
                    elif demande_echauffement.strip().lower() in ("n", "non"):
                        echauffement = False
                        break
                    else:
                        print("Entre une valeur valide (o/n)")
                serie_a_modifier.est_echauffement = echauffement
                carnet.sauvegarder("carnet.json")
                print("Echauffement modifié ")
            elif saisie == "0":
                continue
 
        elif saisie_choix == "6":
            exercice_realise_trouve = choisir_exercice_realise_dans_seance(seance_trouvee, carnet)
            if exercice_realise_trouve is None:
                continue
            nb_avant = len(exercice_realise_trouve.series)
            saisir_series(exercice_realise_trouve)
            nb_apres = len(exercice_realise_trouve.series)
            nb_ajoutees = nb_apres - nb_avant
            if nb_ajoutees > 0:
                carnet.sauvegarder("carnet.json")
                print(f"{nb_ajoutees} série(s) ajoutée(s)")
            else:
                print("Aucune série ajoutée")
        elif saisie_choix == "7":
            exercice_realise_trouve = choisir_exercice_realise_dans_seance(seance_trouvee, carnet)
            if exercice_realise_trouve is None:
                continue
            index_serie = choisir_index_serie(exercice_realise_trouve)
            if index_serie is None:
                continue
            print("⚠️ Attention la suppression est définitive")
            while True:
                saisie = input("Confirmez-vous la suppression de la série (o/n) ?")
                if saisie.strip().lower() in ("non", "n"):
                    print("Suppression annulée")
                    break
                elif saisie.strip().lower() in ("oui", "o"):
                    del exercice_realise_trouve.series[index_serie]
                    carnet.sauvegarder("carnet.json")
                    print("Série supprimée")
                    break
                else: 
                    print("Réponse invalide, tape 'oui' ou 'non'")

        elif saisie_choix == "8":
           print("⚠️ Attention la suppression est définitive")
           while True:
                saisie = input("Confirmez-vous la suppression de la séance (o/n) ?")
                if saisie.strip().lower() in ("non", "n"):
                    print("Suppression annulée")
                    break
                elif saisie.strip().lower() in ("oui", "o"):
                    carnet.seances.remove(seance_trouvee)
                    carnet.sauvegarder("carnet.json")
                    print("La séance a été supprimée")
                    return
                else: 
                    print("Réponse invalide, tape 'oui' ou 'non'")
        elif saisie_choix == "0":
            break
        else:
            print("Choix invalide")

##############################################################
# Les fonctions de refactorisation #
def saisir_series(exercice_realise: ExerciceRealise) -> None:
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
            while True:
                demande_echauffement = input("S'agit il d'une série d'échauffement ? (o/n)")
                if demande_echauffement.strip().lower() in ("o", "oui"):
                    echauffement = True
                    break
                elif demande_echauffement.strip().lower() in ("n", "non"):
                    echauffement = False
                    break
                else:
                    print("Entre une valeur valide (o/n)")
            serie = Serie(poids_utilise, reps_effectuees, echauffement)
            exercice_realise.ajouter_serie(serie)
    
def choisir_exercice_realise_dans_seance(seance: Seance, carnet: CarnetEntrainement) -> ExerciceRealise | None:
    exercice_realise_trouve = None
    while True:
        saisie_id = input("Saisie un id exercice valide ou 'stop' ").strip().upper()
        if saisie_id.lower() == "stop":
            print("Modification annulée ")
            return None
        elif saisie_id not in carnet.exercices:
            print("Exercice inconnu ")
            continue
        else:
            exercice_choisi = carnet.exercices[saisie_id]
        for exercice_seance in seance.exercices_realises:
            if exercice_seance.exercice == exercice_choisi:
                exercice_realise_trouve = exercice_seance
                break
        if exercice_realise_trouve is None:
            print("Cet exercice n'est pas enregistré dans cette séance ")
            continue
        else:
            print("Exercice trouvé dans la séance ")
            return exercice_realise_trouve
        
def choisir_index_serie(exercice_realise: ExerciceRealise) -> int | None:
    if len(exercice_realise.series) == 0:
        print("Aucune série enregistrée sur cet exercice ")
        return None
    for position, serie in enumerate(exercice_realise.series, start=1):
        print(f"{position}. {serie.poids} kg x {serie.reps}")
    while True:
        saisie_num_serie = input("Saisie le numéro de la série ")
        if not saisie_num_serie.isdigit():
            print("Saisie invalide, entre un numéro ")
            continue
        index_serie = int(saisie_num_serie) - 1
        if 0 <= index_serie < len(exercice_realise.series):
            print("Numéro de série valide ")
            return index_serie
        else:
            print("Numéro de série invalide ")


    
##############################################################  
# Les fonctions pour l'affichage de menu #
def afficher_menu() -> None:
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
    print(f"10. Modifier/supprimer une séance")
    print(f"0. Quitter")


def afficher_sous_menu() -> None:
    print(f"1. Modifier la date")
    print(f"2. Modifier la durée")
    print(f"3. Ajouter un exercice")
    print(f"4. Supprimer un exercice de la séance")
    print(f"5. Modifier une série")
    print(f"6. Ajouter une série à un exercice")
    print(f"7. Supprimer une série d'un exercice")
    print(f"8. Supprimer la séance entière")
    print(f"0. Retour au menu principal")

def afficher_sous_menu_modification_serie() -> None:
    print(f"1. Modifier le poids")
    print(f"2. Modifier les reps")
    print(f"3. Modifier le statut échauffement")
    print(f"0. Retour")