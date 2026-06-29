from stats.stats import lister_exercices_differents_par_groupe, un_rm_estime_par_exercice, record_par_exercice, volume_total_exercice_realise

def test_lister_exercices_differents_par_groupe():
    seances = [
        {
            "date": "2026-06-24",
            "duree": 90,
            "exercices_realises": [
                {"id_exercice": "DC01", "nom": "Développé couché", "groupe_musculaire": "pectoraux", "muscles_cibles": ["pec"], "type_materiel": "barre", "series": []},
                {"id_exercice": "SQ01", "nom": "Squat", "groupe_musculaire": "jambes", "muscles_cibles": ["quadriceps"], "type_materiel": "barre", "series": []},
            ]
        },
        {
            "date": "2026-06-25",
            "duree": 90,
            "exercices_realises": [
                {"id_exercice": "DC01", "nom": "Développé couché", "groupe_musculaire": "pectoraux", "muscles_cibles": ["pec"], "type_materiel": "barre", "series": []},
            ]
        },
    ]
    
    resultat = lister_exercices_differents_par_groupe(seances)
    assert resultat == {
        "pectoraux": ["Développé couché"],
        "jambes": ["Squat"],
    }

def test_calcul_du_1rm_est_juste():
    seance = [
        {
            "date": "2026-06-24",
            "duree": 90,
            "exercices_realises": [
                {"id_exercice": "DC01", "nom": "Développé couché", "groupe_musculaire": "pectoraux", "muscles_cibles": ["pec"], "type_materiel": "barre", "series": [
                    {"numero_serie": 1, "poids": 90, "reps": 15, "est_echauffement": 0},
                    {"numero_serie": 2, "poids": 110, "reps": 4, "est_echauffement": 0},
                    {"numero_serie": 3, "poids": 90, "reps": 15, "est_echauffement": 1}
                ]}
            ]
        }
    ]
    resultat = un_rm_estime_par_exercice(seance)
    assert resultat == {"Développé couché": 135.0}


def test_record_par_exercice_donne_le_bon_resultat():
    seance = [
        {
            "date": "2026-06-24",
            "duree": 90,
            "exercices_realises": [
                {"id_exercice": "DC01", "nom": "Développé couché", "groupe_musculaire": "pectoraux", "muscles_cibles": ["pec"], "type_materiel": "barre", "series": [
                    {"numero_serie": 1, "poids": 90, "reps": 15, "est_echauffement": 0},
                    {"numero_serie": 2, "poids": 110, "reps": 4, "est_echauffement": 0},
                    {"numero_serie": 3, "poids": 300, "reps": 15, "est_echauffement": 1}
                ]}
            ]
        }
    ]
    resultat = record_par_exercice("DC01", seance)
    assert resultat == 110

def test_volume_total_exercice_realise_prend_en_compte_halteres():
    resultat1 = volume_total_exercice_realise({"id_exercice": "DC01", "nom": "Développé couché", "groupe_musculaire": "pectoraux", "muscles_cibles": ["pec"], "type_materiel": "barre", "series": [
                    {"numero_serie": 1, "poids": 90, "reps": 15, "est_echauffement": 0},
                    {"numero_serie": 2, "poids": 110, "reps": 4, "est_echauffement": 0},
                    {"numero_serie": 3, "poids": 300, "reps": 15, "est_echauffement": 1}
                ]})
    resultat2 = volume_total_exercice_realise({"id_exercice": "DI01", "nom": "Développé incliné haltère", "groupe_musculaire": "pectoraux", "muscles_cibles": ["pec"], "type_materiel": "haltères", "series": [
                    {"numero_serie": 1, "poids": 90, "reps": 15, "est_echauffement": 0},
                    {"numero_serie": 2, "poids": 110, "reps": 4, "est_echauffement": 0},
                    {"numero_serie": 3, "poids": 300, "reps": 15, "est_echauffement": 1}
                ]})
    assert resultat1 == 1790
    assert resultat2 == 3580