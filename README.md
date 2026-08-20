# 💡 TalkToData — Plateforme Multi-Agents d'Intelligence Décisionnelle Entreprise

**TalkToData** est une plateforme décisionnelle multi-agents déployée sur **Google Cloud Platform (GCP)**. Elle transforme les données d'entreprise et les bases officielles d'Open Data en **décisions stratégiques, financières et opérationnelles à fort ROI**, directement accessibles en langage naturel via **Vertex AI Data Agents**.

Chaque agent est un **Copilote Métier Spécialisé** qui répond aux vraies questions des dirigeants (DG, DAF, DRH, Directeur des Opérations, Directeur Risques) en interrogeant directement des bases BigQuery relationnelles, des tables d'objets GCS (PDF, images satellites) et le Knowledge Catalog Dataplex.

---

## 🎯 La Valeur Métier des 11 Agents Spécialisés

---

### 1. 🏥 **Sully** — *Copilote Emploi Public, RH & URSSAF*
* **Problématique** : Les pénuries de compétences techniques menacent la réindustrialisation (ex: usines de batteries en Hauts-de-France) et la vacance prolongée de postes hospitaliers (> 6 mois) génère des surcoûts financiers majeurs.
* **Valeur Ajoutée & ROI** :
  - **Réduction des coûts de vacance** : Identification des postes vacants à fort impact financier (ex: Hôpital national de paris à 380-650 €/jour de perte) pour déclencher des plans de recrutement d'urgence.
  - **Péréquation des aides à l'embauche** : Mobilisation ciblée des subventions publiques (POEI, AFPR, CPF) à coût zéro pour l'employeur.
  - **Rapprochement candidat sur-mesure** : Analyse des freins à l'emploi (garde d'enfants, mobilité) et accès direct aux CVs PDF d'origine sur Cloud Storage via les tables d'objets natives BigQuery.
* **3 Questions Métier Clés** :
  1. *« Quels sont les 10 métiers qui comptabilisent le plus grand nombre de recrutements difficiles BMO 2025 en Île-de-France ? »*
  2. *« Pour l'Hôpital national de paris, présente ses offres non pourvues depuis +6 mois et leur impact financier (Vacancy Cost) quotidien. »*
  3. *« Présente-moi le profil synthétique d'Anna (ID: FT-99720068), ses compétences et le lien vers son CV PDF d'origine. »*

---

### 2. 🏦 **CreditAdvisor** — *Copilote Risque Crédit & Finance B2B*
* **Problématique** : La hausse des taux d'intérêt et les chocs sectoriels augmentent le risque de faillites PME/ETI et compliquent l'arbitrage entre maîtrise du risque d'impayés et développement commercial.
* **Valeur Ajoutée & ROI** :
  - **Détection préventive du risque de défaillance** : Identification des entreprises à risque de liquidation judiciaire d'ici 6 mois pour ajuster les exigences de garanties.
  - **Optimisation de la marge d'intérêt (RAROC)** : Calcul du rendement ajusté du risque et modélisation du provisionnement comptable IFRS 9 (ECL Staging 1, 2, 3).
  - **Ciblage d'upsell B2B** : Identification des PME résilientes (Score FIBEN ≥ 75) éligibles à des lignes de trésorerie confirmées.
* **3 Questions Métier Clés** :
  1. *« Quelle est la répartition des encours de crédit par classe de risque IFRS 9 et par secteur d'activité ? »*
  2. *« Quels sont les 10 clients professionnels qui génèrent le plus d'encours et leur taux d'intérêt moyen ? »*
  3. *« Quel est le montant global des provisions IFRS 9 (ECL) et des encours par région administrative ? »*

---

### 3. 📡 **NetArch** — *Copilote Architecture Réseau Télécom & Abonnés ARCEP*
* **Problématique** : La saturation des antennes 5G, les pannes d'équipements sous SLA et l'attrition des abonnés B2B pénalisent le chiffre d'affaires des opérateurs.
* **Valeur Ajoutée & ROI** :
  - **Suivi de l'ARPU & Rétention B2B** : Analyse du chiffre d'affaires mensuel récurrent par type de forfait (5G Pro, Fibre 2Gbps) pour cibler les campagnes d'upsell 5G Max.
  - **Maintenance prédictive des pylônes** : Détection IoT des antennes à risque de panne sous 7 jours (température CPU, batterie) pour isoler le composant à remplacer.
  - **Supervision QoS & SLA** : Réduction du temps moyen de rétablissement (MTTR) et minimisation des pénalités contractuelles B2B.
* **3 Questions Métier Clés** :
  1. *« Quel est l'ARPU (Revenu Moyen par Utilisateur) et le chiffre d'affaires mensuel généré par catégorie de forfaits B2B vs B2C ? »*
  2. *« Identifie les 10 antennes 5G qui enregistrent le plus fort volume de trafic de données (en Go) et leur score de qualité d'expérience. »*
  3. *« Quels sont les équipements réseau ayant subi le plus grand nombre d'incidents techniques ce trimestre et leur délai de rétablissement MTTR ? »*

---

### 4. 🛰️ **EarthIntel** — *Copilote Imagerie Satellitaire & Risques Géospatiaux*
* **Problématique** : L'exposition aux risques climatiques (inondations, sécheresse, incendies) et les exigences réglementaires de durabilité (CSRD Zéro Déforestation) nécessitent une vérification visuelle incontestable.
* **Valeur Ajoutée & ROI** :
  - **Évaluation des risques du portefeuille d'actifs** : Croisement des localisations géographiques d'actifs avec l'imagerie spatiale ESA Sentinel-2 (10m).
  - **Prévention du stress hydrique agricole (NDVI)** : Télédétection de la santé chlorophyllienne des cultures pour anticiper les pertes de récoltes.
  - **Conformité CSRD & Élagage Réseau** : Preuve visuelle de non-déforestation pour la retail et détection de la surcroissance végétale sous les lignes haute tension.
* **3 Questions Métier Clés** :
  1. *« Quels sont les départements agricoles affichant la plus forte baisse de l'indice NDVI sur les derniers clichés Sentinel-2 ? »*
  2. *« Liste tous les actifs immobiliers et industriels de notre portefeuille situés dans des zones à fort score d'exposition aux inondations ou feux de forêt. »*
  3. *« Évalue le risque d'inondation et d'incendie sur notre portefeuille d'actifs immobiliers assurés en PACA et affiche le cliché satellite Sentinel-2 de confirmation. »*

---

### 5. 🚆 **TransitNavigator** — *Copilote Transports Publics & Régularité SNCF*
* **Problématique** : Les retards ferroviaires entraînent des pénalités financières et une baisse de satisfaction usagers, tandis que les wagons de 1ère classe souffrent parfois d'un sous-remplissage.
* **Valeur Ajoutée & ROI** :
  - **Diagnostic des causes de retard** : Isolation des retards imputables aux pannes d'infrastructures (voies, signalisation) vs matériel roulant pour arbitrer les investissements.
  - **Yield Management & Optimisation tarifaire** : Ajustement dynamique des billets 1ère classe pour augmenter le panier moyen de +12 %.
  - **Gestion des flux usagers & Objets trouvés** : Analyse de la fréquentation des 3 021 gares de France et amélioration du taux de restitution des objets oubliés.
* **3 Questions Métier Clés** :
  1. *« Quels sont les 5 axes ferroviaires qui enregistrent le plus fort taux de retards de trains et quelle en est la cause principale ? »*
  2. *« Quelles sont les 10 gares de voyageurs enregistrant la plus forte fréquentation annuelle et leur nombre de voyageurs ? »*
  3. *« Quel est le nombre total d'objets trouvés déclarés en gare par type d'objet et quel est le taux de restitution aux usagers ? »*

---

### 6. 🏥 **PulseChecker** — *Copilote Santé & Gestion Hospitalière*
* **Problématique** : La saturation des urgences, l'absentéisme soignant et les ruptures de stock de médicaments critiques (antibiotiques, insuline) mettent en péril la continuité des soins.
* **Valeur Ajoutée & ROI** :
  - **Régulation des urgences & Plans Blancs** : Détection en temps réel des établissements sous tension extrême (>110 % d'occupation).
  - **Sécurisation des approvisionnements pharmacie** : Alerte précoce sur les molécules vitaux affichant moins de 5 jours d'autonomie en stock.
  - **Optimisation des blocs opératoires** : Augmentation du taux d'occupation des salles de chirurgie par spécialité et réduction des heures supplémentaires.
* **3 Questions Métier Clés** :
  1. *« Quel est le taux d'occupation et d'utilisation moyen des blocs opératoires par spécialité chirurgicale ? »*
  2. *« Quels sont les produits pharmaceutiques et médicaments vitaux dont le niveau de stock actuel est critique (< 5 jours d'autonomie) ? »*
  3. *« Quels départements en désert médical RPPS représentent les meilleures opportunités pour implanter une nouvelle clinique privée avec les plus forts projets d'EBITDA sur 5 ans ? »*

---

### 7. 🛒 **ShelfOptimizer** — *Copilote Merchandising & Supply Chain Retail*
* **Problématique** : Les ruptures visuelles en rayon (Shelf-Out) et la casse sur les produits frais génèrent des pertes de chiffre d'affaires et de marge brute irrécupérables.
* **Valeur Ajoutée & ROI** :
  - **Éradication des Shelf-Out** : Audit de conformité des planogrammes et détection des trous en linéaire pour réapprovisionner les rayons prioritaires.
  - **Réduction de la gâche rayon Frais** : Prédiction à 14 jours de la péremption pour appliquer des stickers anti-gaspillage automatiques.
  - **Upsell & Cross-Merchandising MDD** : Recommandation de bundles associant Marques Nationales et Marques de Distributeur à forte marge.
* **3 Questions Métier Clés** :
  1. *« Quels sont les rayons (Épicerie, Frais, Boissons) qui comptabilisent le plus grand nombre de références et leur taux moyen de rupture visuelle ? »*
  2. *« Quelles sont les références produits qui connaissent les plus forts taux de rupture visuelle (Shelf Out) en linéaire magasin ? »*
  3. *« Quelles sont les meilleures associations de produits (Marques Nationales vs MDD) qui génèrent la plus forte hausse de ticket moyen ? »*

---

### 8. 🏟️ **ArenaManager** — *Copilote Événementiel, Stades & Arenas*
* **Problématique** : Le sous-remplissage des enceintes sportives, la lenteur d'accès aux portillons et le gaspillage énergétique des gymnases municipaux pèsent sur les bilans financiers.
* **Valeur Ajoutée & ROI** :
  - **Maximisation des recettes billetterie & VIP** : Optimisation du taux de remplissage des loges d'hospitalité prestige lors des matchs et concerts.
  - **Augmentation du panier catering & buvettes** : Analyse du chiffre d'affaires restauration et merchandising par spectateur.
  - **Audit énergétique RES** : Détection des complexes sportifs vétustes affichant une surconsommation kWh/m² et une sous-occupation < 30 %.
* **3 Questions Métier Clés** :
  1. *« Quel est le taux de remplissage moyen et le chiffre d'affaires billetterie réalisé par catégorie d'événement (Concerts, Matchs, Spectacles) ? »*
  2. *« Quel est le chiffre d'affaires moyen généré par les buvettes et points de restauration rapide par spectateur lors des événements ? »*
  3. *« Quels complexes sportifs affichent la plus forte consommation énergétique annuelle (en MWh) et leur état de vétusté ? »*

---

### 9. ☀️ **Helios** — *Copilote Énergie & Bornes IRVE Enedis*
* **Problématique** : L'explosion du parc de véhicules électriques crée des risques de saturation des transformateurs de quartier lors des pics de recharge.
* **Valeur Ajoutée & ROI** :
  - **Supervision du réseau d'IRVE (10 000 bornes)** : Suivi de la puissance nominale (kW), des connecteurs (Combo CCS) et du taux d'utilisation par opérateur.
  - **Prévention de la saturation des transformateurs** : Télémesures 30 min du taux de charge des postes HTA/BT pour déclencher des renforcements ciblés.
  - **Intégration EnR & Flexibilité B2B** : Maximisation de l'injection solaire/éolienne et valorisation des effacements de consommation des industriels.
* **3 Questions Métier Clés** :
  1. *« Quelle a été la production électrique totale raccordée (en kW) par filière d'énergie renouvelable (Solaire, Éolien, Hydraulique) ? »*
  2. *« Quels sont les principaux opérateurs de bornes de recharge IRVE et la puissance moyenne installée par région ? »*
  3. *« Quels transformateurs de quartier enregistrent le plus fort taux de charge et leur niveau de risque de saturation ? »*

---

### 10. 🌾 **Ceres** — *Copilote Transition Agroécologique & Exploitations*
* **Problématique** : Les alés météorologiques menacent les récoltes et la pression ESG des investisseurs exige une preuve mesurable de décarbonation agricole.
* **Valeur Ajoutée & ROI** :
  - **Pilotage des rendements à l'hectare** : Analyse des volumes récoltés (Blé, Maïs, Colza) par région et suivi des sondes IoT d'humidité des sols.
  - **Valorisation du Label Bas-Carbone** : Certification des tonnes de CO2e séquestrées par les exploitations HVE/Bio pour revendre le grain à prime.
  - **Reporting ESG certifié investisseurs** : Consolidation de l'empreinte carbone ADEME Agribalyse 3.1 sur l'ensemble de la chaîne coopérative.
* **3 Questions Métier Clés** :
  1. *« Quel est le rendement moyen constaté en tonnes par hectare pour les principales cultures par région agricole ? »*
  2. *« Quelle est l'humidité moyenne des sols et la pluviométrie mesurée par nos capteurs IoT par station météo ? »*
  3. *« Quel est le chiffre d'affaires annuel et le nombre d'adhérents des coopératives agricoles par région ? »*

---

### 🎬 11. **CineAnalyst** — *Copilote Cinéma, Box-Office & Exploitation*
* **Problématique** : Les arbitrages de programmation des films en salles doivent concilier potentiel au box-office, budget engagé et durée de maintien à l'affiche.
* **Valeur Ajoutée & ROI** :
  - **Analyse du ROI des productions** : Évaluation du ratio recettes au box-office / budget de production par film et distributeur.
  - **Optimisation des tarifs par format** : Comparatif de la fréquentation des salles immersives (IMAX, 4DX, Dolby) et valorisation du surcoût billet.
  - **Distribution régionale & Art et Essai** : Ciblage des circuits de multiplexes et salles indépendantes selon la démographie locale.
* **3 Questions Métier Clés** :
  1. *« Quels sont les 5 films sortis cette année qui affichent le meilleur ratio de rentabilité (recettes au box-office vs budget de production) ? »*
  2. *« Quelle est la moyenne de fréquentation et le taux d'occupation des fauteuils par séance selon le format de projection (IMAX, 4DX, Standard) ? »*
  3. *« Quels sont les films sortis cette année enregistrant le plus grand nombre total d'entrées cumulées au box-office ? »*

---

## 🛠️ Architecture Technique GCP

La plateforme s'appuie sur une stack Google Cloud d'entreprise automatisée :
- **Vertex AI Data Agents** (`geminidataanalytics.googleapis.com`) : Moteur de raisonnement naturel et de génération de requêtes analytiques sécurisées.
- **BigQuery** : Data Warehouse hébergeant les 11 datasets sectoriels interconnectés.
- **BigQuery Object Tables (GCS)** : Stockage et requêtage direct des fichiers non structurés (PDFs de CVs candidats, images satellites PNG).
- **Dataplex Knowledge Catalog** : Gouvernance centralisée des métadonnées, glossaires métiers et règles de qualité des données.

---

## 🚀 Installation & Déploiement

### Prérequis
- Python 3.10+
- Google Cloud SDK (`gcloud`) configuré avec les accès administrateur sur le projet cible.

```bash
# 1. Cloner le dépôt
git clone https://github.com/ken-william/Data-Agents-By-Industry.git
cd Data-Agents-By-Industry

# 2. Configurer votre projet GCP
export GOOGLE_CLOUD_PROJECT="votre-projet-gcp"

# 3. Authentification Google Cloud
gcloud auth login
gcloud auth application-default login

# 4. Installer l'environnement Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 5. Déployer l'intégralité des datasets et des 11 agents en 1 commande
python deploy_all_agents.py
```
