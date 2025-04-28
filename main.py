# main.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

# Importation des fonctions depuis le fichier séparé
try:
    import cee_function as cf
except ImportError:
    st.error("ERREUR : Le fichier 'cee_functions.py' est introuvable...")
    st.stop()

# --- Configuration et Styles CSS ---
st.set_page_config( page_title="Calculateur MaPrimeRénov' Ampleur", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")
# --- Styles CSS (Copiez/Collez les styles CSS ici) ---
st.markdown("""<style>
    /* Styles généraux */
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; }
    .main-title { text-align: center; font-size: 2.6rem; color: #1E3A8A; margin-bottom: 0.5rem; font-weight: 800; letter-spacing: -1px; }
    .sub-header { text-align: center; font-size: 1.3rem; color: #3B82F6; margin-bottom: 2rem; font-weight: 300; }
    .section-title { color: #1E3A8A; font-size: 1.6rem; border-bottom: 3px solid #60A5FA; padding-bottom: 0.6rem; margin: 1.8rem 0 1.2rem 0; font-weight: 700; }
    .info-box { background-color: #EFF6FF; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 6px solid #3B82F6; box-shadow: 0 3px 10px rgba(0,0,0,0.05); color: #374151; line-height: 1.6; }
    .result-container { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #D1D5DB; }
    /* Cards */
    .card { background-color: white; padding: 1.8rem; border-radius: 10px; box-shadow: 0 4px 12px -1px rgba(0, 0, 0, 0.08), 0 2px 8px -1px rgba(0, 0, 0, 0.04); margin-bottom: 1.8rem; border: 1px solid #E5E7EB; }
    .card-header { font-size: 1.2rem; font-weight: 700; color: #111827; margin-bottom: 1.2rem; padding-bottom: 0.6rem; border-bottom: 1px solid #E5E7EB;}
    /* Alertes */
    .success-box { background-color: #ECFDF5; color: #065F46; padding: 1rem; border-radius: 6px; margin: 0.8rem 0; border-left: 5px solid #10B981; font-weight: 500;}
    .warning-box { background-color: #FFFBEB; color: #92400E; padding: 1rem; border-radius: 6px; margin: 0.8rem 0; border-left: 5px solid #F59E0B; font-weight: 500;}
    .error-box { background-color: #FEF2F2; color: #991B1B; padding: 1rem; border-radius: 6px; margin: 0.8rem 0; border-left: 5px solid #EF4444; font-weight: 500;}
    .info-alert-box { background-color: #EFF6FF; color: #1E40AF; padding: 1rem; border-radius: 6px; margin: 0.8rem 0; border-left: 5px solid #3B82F6; font-weight: 500;}
    /* Métriques */
    div[data-testid="stMetric"] { background-color: #FFFFFF; border: 1px solid #E5E7EB; padding: 1rem 1.2rem; border-radius: 8px; margin-bottom: 1rem; border-left: 6px solid #60A5FA; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    div[data-testid="stMetric"] label p { font-weight: 600; color: #4B5563; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.3rem;}
    div[data-testid="stMetric"] div div { font-size: 1.8em; font-weight: 700; color: #1F2937; line-height: 1.2;}
    div[data-testid="stMetric"]:nth-of-type(1) { border-left-color: #10B981; } /* Aide MPR */
    div[data-testid="stMetric"]:nth-of-type(1) div div { color: #047857; }
    div[data-testid="stMetric"]:nth-of-type(3) { border-left-color: #10B981; } /* Aide Totale */
    div[data-testid="stMetric"]:nth-of-type(3) div div { color: #047857; }
    div[data-testid="stMetric"]:nth-of-type(4) { border-left-color: #EF4444; } /* Reste à charge */
    div[data-testid="stMetric"]:nth-of-type(4) div div { color: #B91C1C; }
    /* Classes Énergétiques */
    .classe-a { background-color: #16A34A; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-b { background-color: #84CC16; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-c { background-color: #FACC15; color: #422006; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-d { background-color: #F97316; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-e { background-color: #EA580C; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-f { background-color: #DC2626; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    .classe-g { background-color: #BE123C; color: white; padding: 3px 9px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 0.9em;}
    /* Footer */
    .footer-section { text-align: center; color: #6B7280; font-size: 0.85rem; margin-top: 3rem; padding: 1.5rem; border-top: 1px solid #E5E7EB; background-color: #F9FAFB; }
    /* Autres */
    .stButton>button { border-radius: 8px; padding: 0.7rem 1.8rem; font-weight: 600; font-size: 1.05rem; border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
    .stButton>button:disabled { background-color: #E5E7EB !important; color: #9CA3AF !important; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; padding-bottom: 0.8rem;}
    .stTabs [data-baseweb="tab-list"] { border-bottom-color: #D1D5DB !important; margin-bottom: 1.5rem;}
    div[data-testid="stExpander"] details { border: 1px solid #D1D5DB; border-radius: 8px; box-shadow: none; margin-bottom: 1rem; }
    div[data-testid="stExpander"] summary { font-weight: 600; color: #1E3A8A; padding: 0.8rem 1rem;}
    div[data-testid="stExpander"] summary:hover { background-color: #F3F4F6;}
    /* Masquer les flèches +/- du number input */
    /* div[data-baseweb="input"] > div:nth-child(2) { display: none; } */ /* Optionnel: peut masquer les boutons up/down */
</style>""", unsafe_allow_html=True)

# --- Fonctions Helper UI ---
def afficher_alerte(message, type_alerte="info"):
    icon_map = {"success": "✅", "warning": "⚠️", "error": "❌", "info": "ℹ️"}
    st.markdown(f'<div class="{type_alerte}-box">{icon_map.get(type_alerte, "ℹ️")} {message}</div>', unsafe_allow_html=True)

def formatter_classe(classe):
    return f'<span class="classe-{classe.lower()}">{classe}</span>'

def creer_graphique_financement(aide_mpr, reste_charge, ttc, aide_mar=0):
    labels=['Aide MPR', 'Aide MAR', 'Reste à charge']; values=[aide_mpr, aide_mar, reste_charge]
    valid_indices = [i for i, v in enumerate(values) if v > 0]; labels = [labels[i] for i in valid_indices]; values = [values[i] for i in valid_indices]
    colors_map = {'Aide MPR': '#10B981', 'Aide MAR': '#3B82F6', 'Reste à charge': '#EF4444'}; colors = [colors_map.get(l, '#9CA3AF') for l in labels]
    if not values: return go.Figure()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.45, marker=dict(colors=colors, line=dict(color='#ffffff', width=1.5)), textinfo='percent', hoverinfo='label+value+percent', insidetextorientation='radial', pull=[0.04]*len(labels), sort=False)])
    fig.update_traces(textfont_size=13, textposition='outside')
    fig.update_layout(title={'text': "Répartition du Financement", 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font_size': 18, 'font_color': '#111827'}, height=360, margin=dict(l=10, r=10, t=60, b=10), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font_size=11))
    fig.add_annotation(text=f"<b>Total:<br>{ttc:,.0f} €</b>", align='center', showarrow=False, font=dict(size=16, color="#1F2937"), x=0.5, y=0.5)
    return fig

# -------------------- Interface Streamlit Principale --------------------

# En-tête et profil
col_h1, col_h2 = st.columns([3, 1])
with col_h1: st.markdown("<h1 class='main-title'>✨ Simulateur MaPrimeRénov' Ampleur TEST✨</h1>", unsafe_allow_html=True); st.markdown("<p class='sub-header'>Estimez vos aides pour une rénovation énergétique performante</p>", unsafe_allow_html=True)
with col_h2: st.markdown("<div class='profile-section' style='margin-top:1rem;'><img src='https://st3.depositphotos.com/1026550/15275/i/450/depositphotos_152750910-stock-photo-environment-conservation-concept.jpg' class='profile-image' alt='Profil'><div class='profile-text'><strong>Sadou BARRY</strong><br>Passionné par l’Éco-Rénovation & la Transition Énergétique<br><a href='https://www.linkedin.com/in/sadou-barry-881868164/' target='_blank'>Contactez-moi sur LinkedIn</a></div></div>", unsafe_allow_html=True)

# Onglets principaux
tab1, tab2, tab3 = st.tabs(["📊 **Calculateur**", "ℹ️ **Infos Utiles**", "❓ **FAQ**"])

with tab1:
    st.markdown("<h2 class='section-title'>1. Renseignez votre projet</h2>", unsafe_allow_html=True)

    # --- Inputs ---
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1: # Ménage
            st.markdown("<h6>👤 Ménage <span style='color:red;'>*</span></h6>", unsafe_allow_html=True)
            code_postal = st.text_input("Code postal", max_chars=5, key="cp_input", help="Code postal du logement (5 chiffres)")
            personnes = st.number_input("Personnes foyer", min_value=1, value=2, step=1, key="pers_input", help="Nombre de personnes composant le foyer fiscal")
            revenu_fiscal = st.number_input("Revenu fiscal réf. (€)", min_value=0.0, value=30000.0, step=100.0, format="%.0f", key="rev_input", help="Votre revenu fiscal de référence (avis d'imposition N-1)")
        with col2: # Projet
            st.markdown("<h6>🛠️ Projet <span style='color:red;'>*</span></h6>", unsafe_allow_html=True)
            cout_travaux_ht = st.number_input("Coût travaux HT (€)", min_value=1.0, value=50000.0, step=100.0, format="%.0f", key="ht_input", help="Coût total HT des travaux éligibles (doit être > 0)")
            cout_travaux_ttc_defaut = round(cout_travaux_ht * 1.055, 0) if cout_travaux_ht > 0 else 0.0
            cout_travaux_ttc = st.number_input("Coût travaux TTC (€)", min_value=1.0, value=cout_travaux_ttc_defaut, step=100.0, format="%.0f", key="ttc_input", help="Coût total TTC (vérifiez la TVA applicable, souvent 5.5%)")
            inclure_mar = st.checkbox("Inclure aide Accompagnateur", value=True, key="mar_input", help="Inclure l'aide pour Mon Accompagnateur Rénov' (obligatoire)")
            habitat_indigne = st.checkbox("Cas d'habitat indigne", value=False, key="indigne_input", help="Cocher si traitement d'habitat indigne inclus (plafond MAR à 4000€)")
        with col3: # Performance
            st.markdown("<h6>⚡ Performance <span style='color:red;'>*</span></h6>", unsafe_allow_html=True)
            classe_actuelle = st.selectbox("Classe actuelle", cf.CLASSES_ORDRE, index=cf.CLASSES_ORDRE.index('G'), key="cl_act_input", help="Classe DPE avant travaux")
            classe_apres = st.selectbox("Classe visée", cf.CLASSES_ORDRE, index=cf.CLASSES_ORDRE.index('B'), key="cl_apr_input", help="Classe DPE visée après travaux")
            # --- INPUT RADIO DU GAIN SUPPRIMÉ ---
            renovation_deux_etapes = st.checkbox("Rénovation en 2 étapes", value=False, key="deux_etapes_input", help="Si le projet est réalisé sur 5 ans (concerne G, F, E initialement)")

    st.caption("<span style='color:red;'>*</span> Champs obligatoires pour le calcul.")
    st.markdown("---")

    # --- Zone de Validation et Bouton ---
    validation_placeholder = st.container() # Pour les messages
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1.5, 1]) # Centrer le bouton

    # Variables pour stocker l'état de la validation
    calcul_possible = True
    gain_reel = 0
    sortie_passoire_atteinte = False
    messages_validation = []

    # 1. Validation Inputs de base
    region = cf.verifier_region(code_postal)
    if region is None: calcul_possible = False; messages_validation.append(("warning", "Code postal invalide."))
    if not isinstance(personnes, int) or personnes < 1: calcul_possible = False; messages_validation.append(("warning", "Nombre de personnes invalide."))
    if not isinstance(revenu_fiscal, (int, float)) or revenu_fiscal < 0: calcul_possible = False; messages_validation.append(("warning", "Revenu fiscal invalide."))
    if not isinstance(cout_travaux_ht, (int, float)) or cout_travaux_ht <= 0: calcul_possible = False; messages_validation.append(("warning", "Coût HT invalide."))
    if not isinstance(cout_travaux_ttc, (int, float)) or cout_travaux_ttc <= 0: calcul_possible = False; messages_validation.append(("warning", "Coût TTC invalide."))
    elif cout_travaux_ttc < cout_travaux_ht: calcul_possible = False; messages_validation.append(("warning", "Coût TTC < Coût HT."))

    # 2. Validation Performance Logique et Planchers (si inputs OK)
    if calcul_possible:
        perf_ok, gain_reel, msg_perf = cf.valider_performance(classe_actuelle, classe_apres)
        if not perf_ok:
            calcul_possible = False # La logique prime
            messages_validation.append(("error", msg_perf))
        else:
            # Afficher le gain réel calculé (informatif)
            validation_placeholder.info(f"Gain réel calculé : {gain_reel} classes ({classe_actuelle} → {classe_apres}).")
            # Vérifier bonus
            est_passoire = classe_actuelle in ["F", "G"]
            index_apres = cf.CLASSES_ORDRE_INV.get(classe_apres, -1)
            sortie_passoire_atteinte = est_passoire and index_apres != -1 and index_apres >= cf.CLASSES_ORDRE_INV["D"] # Correction >= D
            if sortie_passoire_atteinte: messages_validation.append(("success", "Bonus Sortie de Passoire (+10%) applicable."))
            elif est_passoire: messages_validation.append(("info", "Pas de Bonus Sortie de Passoire (arrivée < D)."))
            # Info 2 étapes
            if renovation_deux_etapes and classe_actuelle not in ["G", "F", "E"]: messages_validation.append(("info", "Info: Rénovation en 2 étapes concerne surtout G/F/E."))

    # Afficher les messages de validation dans le placeholder
    with validation_placeholder.container():
        for type_msg, msg in messages_validation:
            afficher_alerte(msg, type_msg)
        if not calcul_possible and not messages_validation:
             afficher_alerte("Veuillez vérifier vos saisies.", "warning")

    with col_btn2:
        calcul_btn = st.button("🚀 Lancer l'estimation", use_container_width=True, disabled=not calcul_possible, type="primary")

    # --- Affichage des Résultats ---
    if calcul_btn and calcul_possible: # Vérifier si le calcul est possible
        categorie, categorie_display, region, seuils_perso = cf.determiner_categorie(code_postal, personnes, revenu_fiscal)

        if categorie is None:
            afficher_alerte(categorie_display, "error")
        else:
            region_nom = "Île-de-France" if region == "idf" else "Hors Île-de-France"

            # Calculer l'aide en utilisant le gain RÉEL calculé
            resultats = cf.calculer_aide_maprimereno(
                categorie=categorie,
                gain_reel=gain_reel, # Utilise le gain calculé !
                cout_travaux_ht=cout_travaux_ht,
                cout_travaux_ttc=cout_travaux_ttc,
                est_passoire_energetique=sortie_passoire_atteinte
            )

            if resultats is None:
                 # Cette erreur signifie que gain_reel < 2, ce qui devrait déjà désactiver le bouton
                 afficher_alerte("Erreur : Gain de performance insuffisant (< 2 classes).", "error")
            else:
                aide_mar_effective = 0.0
                aide_mar_base = resultats.get('aide_mar_base', 0.0)
                if inclure_mar:
                    taux_mar_dec = resultats["taux_mar"] / 100
                    plafond_mar_actuel = cf.PLAFOND_MAR_HABITAT_INDIGNE if habitat_indigne else cf.PLAFOND_MAR
                    aide_mar_effective = round(min(plafond_mar_actuel * taux_mar_dec, plafond_mar_actuel), 2)
                    base_limit = cf.PLAFOND_MAR_HABITAT_INDIGNE if habitat_indigne else aide_mar_base
                    aide_mar_effective = min(aide_mar_effective, base_limit)

                aide_finale_mpr = resultats['aide_finale']
                aide_totale_estimee = round(aide_finale_mpr + aide_mar_effective, 2)
                reste_a_charge_estime = resultats['reste_a_charge']

                st.markdown("<h2 class='section-title'>📊 Résultats de votre estimation</h2>", unsafe_allow_html=True)
                res_col1, res_col2 = st.columns([1, 1])

                with res_col1:
                     st.markdown("<h6>💰 Montants Estimés</h6>", unsafe_allow_html=True)
                     st.metric(label="Aide MaPrimeRénov'", value=f"{aide_finale_mpr:,.0f} €")
                     if inclure_mar: st.metric(label="Aide Accompagnement (MAR)", value=f"{aide_mar_effective:,.0f} €")
                     st.metric(label="Aide Totale (MPR + MAR)", value=f"{aide_totale_estimee:,.0f} €")
                     st.metric(label="Reste à Charge (Travaux MPR)", value=f"{reste_a_charge_estime:,.0f} €")

                     classe_act_fmt = formatter_classe(classe_actuelle); classe_apr_fmt = formatter_classe(classe_apres)
                     bonus_msg_res = " (+ Bonus Passoire)" if resultats['bonus_applique'] else ""
                     ecret_msg_res = " (Écrêtement appliqué)" if resultats['ecretement_applique'] else ""

                     st.markdown(f"""
                     <div class='info-alert-box' style='margin-top: 15px;'>
                     <strong>Contexte :</strong><br>
                     - Profil: {categorie_display} ({region_nom})<br>
                     - Performance: {classe_act_fmt} → {classe_apr_fmt} (Gain: <span class="highlight">{gain_reel}</span> cl.){bonus_msg_res}<br>
                     - Coût TTC: {cout_travaux_ttc:,.0f} €{ecret_msg_res}
                     </div>""", unsafe_allow_html=True)

                with res_col2:
                    st.markdown("<h6>📊 Répartition du Financement</h6>", unsafe_allow_html=True)
                    fig = creer_graphique_financement(aide_finale_mpr, reste_a_charge_estime, cout_travaux_ttc, aide_mar_effective)
                    if fig: st.plotly_chart(fig, use_container_width=True)
                    else: st.warning("Impossible de générer le graphique.")

                with st.expander("🔍 Voir les détails du calcul"):
                     detail_col1, detail_col2 = st.columns(2)
                     with detail_col1:
                         st.markdown("<h6>Calcul Aide MPR</h6>", unsafe_allow_html=True)
                         st.markdown(f"- Catégorie : {categorie_display.split(' aux ')[1]}")
                         st.markdown(f"- **Gain réel utilisé : {gain_reel} classes**") # Utilise gain_reel
                         st.markdown(f"- Plafond HT applicable: {resultats['plafond_travaux']:,.0f} €")
                         st.markdown(f"- Taux base : {resultats['taux_base']:.0f}%")
                         st.markdown(f"- Bonus passoire : {'Oui (+10%)' if resultats['bonus_applique'] else 'Non'}")
                         st.markdown(f"- Taux appliqué : {resultats['taux_avec_bonus']:.0f}%")
                         st.markdown(f"- Coût éligible HT : {resultats['cout_eligible_ht']:,.2f} €")
                         st.markdown(f"- Aide avant écrêtement : {resultats['aide_base']:,.2f} €")
                         st.markdown(f"- Taux écrêtement : {resultats['taux_ecretement']:.0f}% TTC")
                         st.markdown(f"- Aide max. après écrêt. : {resultats['montant_max_aide']:,.2f} €")
                         st.markdown(f"- **Aide finale MPR : {aide_finale_mpr:,.2f} €**")
                         if inclure_mar:
                             plafond_mar_actuel = cf.PLAFOND_MAR_HABITAT_INDIGNE if habitat_indigne else cf.PLAFOND_MAR
                             st.markdown("<h6>Calcul Aide MAR</h6>", unsafe_allow_html=True)
                             st.markdown(f"- Taux prise en charge : {resultats['taux_mar']:.0f}%")
                             st.markdown(f"- Plafond prestation : {plafond_mar_actuel:,} €")
                             st.markdown(f"- **Aide MAR : {aide_mar_effective:,.2f} €**")
                     with detail_col2:
                         st.markdown("<h6>Votre Catégorie de Revenus</h6>", unsafe_allow_html=True)
                         st.markdown(f"Région : {region_nom}, Foyer : {personnes} personne(s)")
                         if seuils_perso and len(seuils_perso) == 3:
                             seuils_formatted = [f"≤ {s:,.0f} €" for s in seuils_perso] + [f"> {seuils_perso[2]:,.0f} €"]
                             data_seuils = {"Catégorie": ["Très modestes", "Modestes", "Intermédiaires", "Supérieurs"],"Plafond Revenus 2025": seuils_formatted}
                             df_seuils = pd.DataFrame(data_seuils)
                             st.table(df_seuils)
                         else: st.warning("Impossible d'afficher le tableau des seuils.")


# --- Onglets Information et FAQ (inchangés) ---
with tab2: # Informations
    st.markdown("<h2 class='section-title'>ℹ️ Informations utiles</h2>", unsafe_allow_html=True)
    info_tab1, info_tab2, info_tab3, info_tab4 = st.tabs([ "Taux & Plafonds", "Rénovation en 2 étapes", "Accompagnement", "Conditions Clés" ])
    with info_tab1:
        st.markdown("<h5>Taux de financement 2025 (% du HT plafonné)</h5>", unsafe_allow_html=True); html_table_taux = """<table class="styled-table"><thead><tr><th>Catégorie</th><th>Gain 2 cl.</th><th>Gain 3 cl.</th><th>Gain 4+ cl.</th><th>Bonus Passoire</th><th>Écrêtement (% TTC)</th></tr></thead><tbody><tr><td>Très modestes</td><td>80%</td><td>80%</td><td>80%</td><td>+10%</td><td>100%</td></tr><tr><td>Modestes</td><td>60%</td><td>60%</td><td>60%</td><td>+10%</td><td>80%*</td></tr><tr><td>Intermédiaires</td><td>45%</td><td>50%</td><td>50%</td><td>+10%</td><td>80%</td></tr><tr><td>Supérieurs</td><td>10%</td><td>15%</td><td>20%</td><td>+10%</td><td>50%</td></tr></tbody></table><p style="font-size: 0.85rem; margin-top: 0.5rem;">*Taux écrêtement Modestes susceptible de passer à 90% (attente décret).</p>"""; st.markdown(html_table_taux, unsafe_allow_html=True)
        st.markdown("<h5>Plafonds de travaux HT</h5>", unsafe_allow_html=True); plafonds_html = """<table class="styled-table"><thead><tr><th>Gain énergétique</th><th>Plafond HT</th></tr></thead><tbody><tr><td>Gain de 2 classes</td><td>40 000 €</td></tr><tr><td>Gain de 3 classes</td><td>55 000 €</td></tr><tr><td>Gain de 4 classes ou plus</td><td>70 000 €</td></tr></tbody></table>"""; st.markdown(plafonds_html, unsafe_allow_html=True)
        st.markdown("<h6>Bonus Sortie de Passoire (+10%)</h6>", unsafe_allow_html=True); st.markdown("Si logement initial F/G ET final D, C, B ou A.")
    with info_tab2:
        st.markdown("<h5>La rénovation en deux étapes</h5>", unsafe_allow_html=True); st.markdown("- Possible sur 5 ans max. pour départs G, F, E.\n- **Objectif final minimum après 2ème étape :** Classe **C** (si départ G/F) ou **B** (si départ E).\n- Calcul aide 2ème étape basé sur gain total et dépenses cumulées.\n- Pas de bonus passoire sur la 2ème étape.")
        try: st.image("https://user-images.githubusercontent.com/118736018/299179280-6229d60b-0c2d-4233-b2cd-a1a1b2bfa534.png", caption="Schéma indicatif de la rénovation en deux étapes")
        except Exception: st.warning("Impossible d'afficher le schéma.")
    with info_tab3:
        st.markdown("<h5>Mon Accompagnateur Rénov' (MAR)</h5>", unsafe_allow_html=True); st.markdown("- **Obligatoire** pour MPR Ampleur.\n- **Prise en charge (plafond 2000€):** 100% (Très Modestes), 80% (Modestes), 40% (Intermédiaires), 20% (Supérieurs).\n- **Plafond MAR à 4000€** si traitement habitat indigne.")
    with info_tab4:
        st.markdown("<h5>Conditions Clés pour MPR Ampleur</h5>", unsafe_allow_html=True); st.markdown("- **Gain minimum réel :** 2 classes énergétiques.\n- **Classe finale minimum réelle :** C (si départ G/F), B (si départ E) (condition réglementaire).\n- **Gestes obligatoires :** Au moins 2 gestes d'isolation thermique.\n- **Accompagnement :** Recours à MAR obligatoire.\n- **Entreprises :** Qualifiées RGE.")
        afficher_alerte("Ce simulateur est indicatif. Contactez un conseiller France Rénov' ou un MAR agréé.", "info")

with tab3: # FAQ
    st.markdown("<h2 class='section-title'>❓ Questions fréquentes</h2>", unsafe_allow_html=True)
    faq_col1, faq_col2 = st.columns(2)
    with faq_col1:
        with st.expander("MPR Ampleur, c'est quoi ?"): st.markdown("L'aide pour les rénovations globales avec ≥ 2 classes de gain et accompagnement obligatoire.")
        with st.expander("Comment est calculé le gain ?"): st.markdown("Différence entre classe avant et après travaux (ex: F -> C = 3 classes). L'aide dépend du gain *réel* calculé.")
        with st.expander("Qui est Mon Accompagnateur Rénov' ?"): st.markdown("Professionnel agréé obligatoire qui aide de l'audit au suivi des travaux.")
    with faq_col2:
        with st.expander("L'écrêtement, c'est quoi ?"): st.markdown("Plafond de l'aide basé sur un % du coût TTC des travaux (variable selon les revenus).")
        with st.expander("Cumul possible avec d'autres aides ?"): st.markdown("Oui avec Éco-PTZ, aides locales, TVA 5.5%. Non cumulable avec les CEE classiques ou MPR par geste.")
        with st.expander("Rénovation en 2 étapes ?"): st.markdown("Pour G/F/E sur 5 ans max. Atteindre C (si G/F) ou B (si E) minimum à la fin. Voir MAR pour détails.")


# Pied de page
st.markdown("""
---
<div class="footer-section">
    <p>Barèmes et règles 2025 (selon infos disponibles Mars 2025). Calculateur indicatif non contractuel.</p>
    <p>Infos officielles : <a href="https://france-renov.gouv.fr" target="_blank">france-renov.gouv.fr</a> | 0 808 800 700 (service gratuit + prix appel).</p>
    <p>© 2025 - Conçu avec ❤️ par Sadou BARRY</p>
</div>
""", unsafe_allow_html=True)