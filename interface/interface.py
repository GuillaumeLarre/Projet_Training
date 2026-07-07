from fonctions_utiles.fonctions import verifier_date, demander_entier_positif, sans_accents

from constantes.constantes import GROUPES_MUSCULAIRES, MUSCLES_CIBLES,MATERIELS

from stats.stats import record_par_exercice, liste_exercices_pratiques, volume_total_par_groupe_musculaire_seance

from database.exercices_repository import charger_catalogue, verifier_id_exercice_existe, verifier_nom_exercice_deja_utilise, ajouter_exercice

from database.seances_repository import verifier_date_seance_existe, ajouter_serie, enregistrer_seance_complete, supprimer_toutes_les_seances, lister_seances, charger_seance_complete, modifier_date_seance, modifier_duree_seance, charger_seance_par_date, ajouter_exercice_realise_a_seance, prochain_numero, verifier_exercice_deja_dans_seance, supprimer_exercice_realise, verifier_exercice_realise_existe, lister_exercices_realises_par_seance, lister_series_par_exercice_realise, verifier_serie_existe, modifier_echauffement_serie, modifier_poids_serie, modifier_reps_serie, supprimer_serie, supprimer_seance, charger_toutes_les_seances_completes

import logging
logger = logging.getLogger(__name__)

##############################################################
# Les fonctions répondant aux menus #

def afficher_catalogue(catalogue) -> None:
    print(f"=== CATALOGUE DES EXERCICES ===\n")
    for ligne in sorted(catalogue.values(), key=lambda ligne: sans_accents(ligne['nom'])):
        print(f"[{ligne['id_exercice']}] {ligne['nom']} - {ligne['groupe_musculaire']} : {', '.join(ligne['muscles_cibles'])} ({ligne['type_materiel']})")

def afficher_historique(conn) -> None:
    seances = lister_seances(conn)
    if not seances:
        print("Aucune séance enregistrée")
        return
    print("=== Historique ===\n")
    for seance in seances:
        print(f"[{seance['id_seance']}] {seance['date']} - {seance['duree']} min")
    while True:
        saisie = input("Saisie l'ID de la séance à voir ou 'fin' :").strip().lower()
        if saisie == "fin":
            return
        if not saisie:
            print("Saisie un ID")
            continue
        if not saisie.isdigit():
            print("L'ID doit être composé de chiffres")
            continue
        afficher_seance_detail(conn, int(saisie))
        

def afficher_seance_detail(conn, id_seance) -> None:
    seance_complete = charger_seance_complete(conn, id_seance)
    if seance_complete is None:
        print("Aucune séance trouvée avec cet ID")
        return
    print(f"[{seance_complete['id_seance']}] {seance_complete['date']} - {seance_complete['duree']} min")
    for exercice in seance_complete["exercices_realises"]:
        print(f"{exercice['nom']}")
        for serie in exercice["series"]:
            mention = "(échauffement)" if serie['est_echauffement'] else ""
            print(f"{serie['numero_serie']}. {serie['poids']:.1f} kg - {serie['reps']} fois {mention}")

def lister_catalogue(conn) -> None:
    catalogue = charger_catalogue(conn)
    if not catalogue:
        print("Catalogue vide")
        return
    afficher_catalogue(catalogue)

def saisir_exercice(conn) -> None:
    print(f"--- Ajout d'un exercice au catalogue ---")
    while True:
        id_exercice = input("Saisis un ID d'exercice (ex: 001): ").strip().upper()
        if not id_exercice:
            print("L'ID ne peut pas être vide ")
            continue
        if verifier_id_exercice_existe(conn, id_exercice):
            print(f"ID déjà pris")
            continue
        break
    while True:
        nom = input("Nom de l'exercice : ").strip()
        if not nom:
            print("Le nom ne peut pas être vide")
            continue
        if verifier_nom_exercice_deja_utilise(conn, nom):
            print("Nom déjà utilisé")
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
    ajouter_exercice(conn, id_exercice, nom, groupe_musculaire, type_materiel, liste_muscles_cibles)
    print(f"Exercice ajouté : [{id_exercice}] {nom}")
 
def saisir_seance(conn) -> None:
    catalogue = charger_catalogue(conn)
    if not catalogue:
        print("Catalogue vide")
        return
    while True:
        date = input("Saisie une date : ")
        if verifier_date(date):
            if verifier_date_seance_existe(conn, date):
                print("Une séance existe déjà à cette date")
                continue
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
    liste_exercices_realises = []
    while True:
        afficher_catalogue(catalogue)
        id_exercice = input("Saisie l'id de l'exercice ou 'fin' : ").strip().upper()
        if id_exercice == "FIN":
            break
        if id_exercice not in catalogue:
            print("Exercice inconnu")
            continue
        liste_series = saisir_series()
        if liste_series:
            liste_exercices_realises.append({"id_exercice": id_exercice, "series": liste_series})
    if not liste_exercices_realises:
        print("Séance annulée car aucun exercice valide n'a été saisi")
        return
    dict_seance = {"date": date, "duree": duree, "exercices_realises": liste_exercices_realises}
    id_seance = enregistrer_seance_complete(conn, dict_seance)
    print("Séance enregistrée")
    logger.info(f"Nouvelle séance saisie : {date}")
    print("\n=== Volume par groupe musculaire ===")
    seance = charger_seance_complete(conn, id_seance)
    for groupe, volume in volume_total_par_groupe_musculaire_seance(seance).items():
        print(f"  {groupe:15s} : {volume:.1f}")
    
def afficher_records(conn) -> None:
    seances = charger_toutes_les_seances_completes(conn)
    liste_ids = liste_exercices_pratiques(seances)
    catalogue = charger_catalogue(conn)
    if not liste_ids:
        print("Aucun exercice enregistré.")
        return
    print("Records par exercice :")
    for id_ex in sorted(liste_ids, key=lambda id_ex: sans_accents(catalogue[id_ex]["nom"])):
        nom = catalogue[id_ex]["nom"]
        record = record_par_exercice(id_ex, seances)
        print(f"{nom} :")
        print(f"    {record:.1f} kg")

def supprimer_seances(conn) -> None:
    print("⚠️ Attention la suppression est définitive")
    while True:
        saisie = input("Confirmez-vous la suppression de toutes les séances ?")
        if saisie.strip().lower() == "non":
            print("Suppression annulée")
            break
        elif saisie.strip().lower() == "oui":
            supprimer_toutes_les_seances(conn)
            print("Toutes les séances ont été supprimées")
            break
        else:
            print("Réponse invalide, tape 'oui' ou 'non' ")

def modifier_seance(conn) -> None:
    while True:
        date_seance = input("Saisie une date : ")
        if verifier_date(date_seance):
            seance = charger_seance_par_date(conn, date_seance)
            if seance is None:
                print("Aucune séance effectuée à cette date")
                continue
            break
        else:
            print("Saisie une date valide")
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
                    if verifier_date_seance_existe(conn, saisie_nouvelle_date):
                        print("Date de séance déjà enregistrée ")
                    else:
                        modifier_date_seance(conn, seance['id_seance'], saisie_nouvelle_date)
                        print("Date modifiée ")
                        break
                else:
                    print("Entre une date valide ")

        elif saisie_choix == "2":
            saisie_duree = demander_entier_positif("Saisie la nouvelle durée ")
            modifier_duree_seance(conn, seance["id_seance"], saisie_duree)
            print("Durée modifiée")

        elif saisie_choix == "3":
            lister_catalogue(conn)
            id_exercice = input("Saisie l'id de l'exercice : ").strip().upper()
            if not verifier_id_exercice_existe(conn, id_exercice):
                print("Exercice inconnu")
                continue
            if verifier_exercice_deja_dans_seance(conn, seance["id_seance"], id_exercice):
                print("Exercice déjà dans la séance")
                continue
            liste_series = saisir_series()
            if not liste_series:
                print("Aucune série ajouté, annulation de l'ajout d'exercice")
                continue
            id_exercice_realise = ajouter_exercice_realise_a_seance(conn, seance["id_seance"], id_exercice)
            print("Exercice ajouté ")
            for position, serie in enumerate(liste_series, start=1):
                ajouter_serie(conn, position, serie["poids"], serie["reps"], serie["est_echauffement"], id_exercice_realise)


        elif saisie_choix == "4":
            id_exercice_realise = choisir_exercice_realise_dans_seance(conn, seance["id_seance"])
            if id_exercice_realise is None:
                continue
            print("⚠️ Attention la suppression est définitive")
            while True:
                saisie = input("Confirmez-vous la suppression de l'exercice (o/n) ?")
                if saisie.strip().lower() in ("non", "n"):
                    print("Suppression annulée")
                    break
                elif saisie.strip().lower() in ("oui", "o"):
                    supprimer_exercice_realise(conn, id_exercice_realise)
                    print("L'exercice a été supprimé")
                    break
                else:
                    print("Réponse invalide, tape 'oui' ou 'non'")

        elif saisie_choix == "5":
            id_exercice_realise = choisir_exercice_realise_dans_seance(conn, seance["id_seance"])
            if id_exercice_realise is None:
                continue
            id_serie = choisir_id_serie(conn, id_exercice_realise)
            if id_serie is None:
                continue
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
                modifier_poids_serie(conn, id_serie, nouveau_poids)
                print("Poids modifié ")
                afficher_serie_apres_modification(conn, id_serie, id_exercice_realise)
            elif saisie == "2":
                nouvelles_reps = demander_entier_positif("Reps effectuées : ")
                modifier_reps_serie(conn, id_serie, nouvelles_reps)
                print("Nouvelles répétitions enregistrées ")
                afficher_serie_apres_modification(conn, id_serie, id_exercice_realise)
            elif saisie == "3":
                while True:
                    demande_echauffement = input("S'agit il d'une série d'échauffement ? (o/n)")
                    if demande_echauffement.strip().lower() in ("o", "oui"):
                        nouvel_echauffement = 1
                        break
                    elif demande_echauffement.strip().lower() in ("n", "non"):
                        nouvel_echauffement = 0
                        break
                    else:
                        print("Entre une valeur valide (o/n)")
                modifier_echauffement_serie(conn, id_serie, nouvel_echauffement)
                print("Echauffement modifié ")
                afficher_serie_apres_modification(conn, id_serie, id_exercice_realise)
            elif saisie == "0":
                continue
 
        elif saisie_choix == "6":
            id_exercice_realise = choisir_exercice_realise_dans_seance(conn, seance['id_seance'])
            if id_exercice_realise is None:
                continue
            liste_series = saisir_series()
            if len(liste_series) == 0:
                print("Aucune série ajoutée")
                continue
            for serie in liste_series:
                num_serie = prochain_numero(conn, id_exercice_realise)
                ajouter_serie(conn, num_serie,serie["poids"], serie["reps"], serie["est_echauffement"], id_exercice_realise)
            print(f"{len(liste_series)} série(s) ajoutée(s)")

        elif saisie_choix == "7":
            id_exercice_realise = choisir_exercice_realise_dans_seance(conn, seance["id_seance"])
            if id_exercice_realise is None:
                continue
            id_serie = choisir_id_serie(conn, id_exercice_realise)
            if id_serie is None:
                continue
            print("⚠️ Attention la suppression est définitive")
            while True:
                saisie = input("Confirmez-vous la suppression de la série (o/n) ?")
                if saisie.strip().lower() in ("non", "n"):
                    print("Suppression annulée")
                    break
                elif saisie.strip().lower() in ("oui", "o"):
                    supprimer_serie(conn, id_serie)
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
                    supprimer_seance(conn, seance["id_seance"])
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
def saisir_series() -> list:
    liste_series = []
    while True:
            poids = input("Poids utilisé ou 'fin': ")
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
                    echauffement = 1
                    break
                elif demande_echauffement.strip().lower() in ("n", "non"):
                    echauffement = 0
                    break
                else:
                    print("Entre une valeur valide (o/n)")
            liste_series.append({"poids": poids_utilise, "reps": reps_effectuees, "est_echauffement": echauffement})
    return liste_series
            
    
def choisir_exercice_realise_dans_seance(conn, id_seance) -> int | None:
    liste_exercices_realises = lister_exercices_realises_par_seance(conn, id_seance)
    if not liste_exercices_realises:
        print("Aucun exercice réalisé dans cette séance")
        return None
    ids_valides = {exo["id_exercice_realise"] for exo in liste_exercices_realises}
    for exo_realise in liste_exercices_realises:
        print(f"[{exo_realise['id_exercice_realise']}] {exo_realise['nom']}")
    while True:
        saisie_id = input("Saisie un id exercice valide ou 'stop' ").strip().upper()
        if saisie_id.lower() == "stop":
            print("Modification annulée ")
            return None
        if not saisie_id.isdigit():
            print("L'ID doit être un nombre")
            continue
        id_choisi = int(saisie_id)
        if id_choisi not in ids_valides:
            print("Cet ID n'est pas dans la séance")
            continue
        return id_choisi
        
def choisir_id_serie(conn, id_exercice_realise) -> int | None:
    liste_series_exercice_realise = lister_series_par_exercice_realise(conn, id_exercice_realise)
    if len(liste_series_exercice_realise) == 0:
        print("Aucune série enregistrée sur cet exercice ")
        return None
    ids_valides = {serie['id_serie'] for serie in liste_series_exercice_realise}
    for serie in liste_series_exercice_realise:
        print(f"[{serie['id_serie']}] {serie['poids']} kg x {serie['reps']}")
    while True:
        saisie_id_serie = input("Saisie l'ID de la série ")
        if not saisie_id_serie.isdigit():
            print("Saisie invalide, entre un numéro ")
            continue
        if int(saisie_id_serie) in ids_valides:
            print("Numéro de série valide ")
            return int(saisie_id_serie)
        else:
            print("Numéro de série invalide ")

def afficher_serie_apres_modification(conn, id_serie, id_exercice_realise) -> None:
    series = lister_series_par_exercice_realise(conn, id_exercice_realise)
    for serie in series:
        if serie["id_serie"] == id_serie:
            echauffement = " (échauffement)" if serie["est_echauffement"] else ""
            print(f"Série {serie['numero_serie']} : {serie['poids']} kg x {serie['reps']}{echauffement}")
            return

    
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