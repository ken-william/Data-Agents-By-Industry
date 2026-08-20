# Master Specification & Prompt System - Talk to Data (Google Fluid Blue Dual Screen)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** pour les événements B2B (BigData Paris 2026, Google Cloud Next).

---

# 🎨 1. Le Design System "Google Fluid Blue" (CSS Variables)

```css
:root {
  /* Palette Chromatique - Google Fluid Blue */
  --bg-gradient: radial-gradient(circle at 50% 30%, #070f2b 0%, #020617 70%, #000000 100%);
  --bento-bg: rgba(15, 23, 42, 0.45);
  --bento-border: rgba(51, 65, 85, 0.5);
  --bento-border-active: rgba(56, 189, 248, 0.55);
  --gemini-gradient: linear-gradient(135deg, #38bdf8 0%, #3b82f6 50%, #6366f1 100%);
  
  /* Typographie Premium */
  --font-family-google: "Google Sans Flex", "Google Sans", "Inter", sans-serif;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-dark: #0f172a;

  /* Formes et Animations */
  --radius-card: 16px;
  --radius-pill: 9999px;
  --glow-active: 0 0 25px rgba(56, 189, 248, 0.15);
}
```

---

# 🖥️ 2. Architecture Double Écran (Dual-Screen Setup)

```text
+------------------------------------------------------------------------------------------------+
|                                     DUAL-SCREEN ARCHITECTURE                                   |
+------------------------------------------------------------------------------------------------+
|  ÉCRAN A : LE GRAND ÉCRAN (SHOWCASE / PUBLIC)      |  ÉCRAN B : LE PC CONTRÔLEUR (TACTILE)         |
|  - Orbe Gemini Live & Vagues Wave-1/2/3 (Centre)   |  - Grille Bento des 11 Agents Sectoriels      |
|  - Visualisation des Données (70% Largeur)         |  - Barre de Saisie Hybride Fixe (Bas d'écran)  |
|  - SQLFlipCard Recto/Verso (Looker vs Neon SQL)    |  - Push-to-Talk Mic + Smart Chips anti-bruit   |
|  - KPI Scores & Graphiques Épurés                  |  - Console de Log & Switcher Écran A/B        |
+------------------------------------------------------------------------------------------------+
```

### Spécifications comparatives des deux écrans

| Caractéristique | ÉCRAN A : Le Grand Écran (Showcase / Public) | ÉCRAN B : Le PC / Tablette (Contrôleur) |
| :--- | :--- | :--- |
| **Cible** | Le public du salon, les spectateurs. | Le présentateur ou le client manipulant la démo. |
| **Priorité Visuelle** | L'**Orbe Gemini Live** et le **Data Canvas (70%)**. | La **sélection d'agents** et le **dock de saisie anti-bruit**. |
| **Composant Phare** | `DynamicDataCanvas` + `SQLFlipCard` (Looker KPI Recto / SQL Verso). | `AgentGrid` + `InputDockFixed` avec Smart Chips. |
| **Affichage Technique** | Carte 3D se retournant pour montrer la requête BigQuery native. | Console de contrôle et statut de connexion BigQuery. |

---

# 🔮 3. L'Orbe Gemini Live (Physics Waves)

L'avatar vocal est un orbe tridimensionnel animé avec des vagues concentriques d'ondes physiques (`wave wave-1`, `wave-2`, `wave-3`).

### Les 4 États de l'Orbe Fluidique

| État | Comportement de l'Orbe | Animation & Intention |
| :--- | :--- | :--- |
| **Idle (Attente)** | Respiration circulaire douce (`gemini-orbe-live idle`). | Attente de connexion ou de question. |
| **Listening (Écoute)** | Ondes pulsées concentriques et réactives (`listening`). | Capture audio du microphone (STT). |
| **Thinking (Réflexion SQL)** | Rotation rapide d'un anneau de gradient Gemini (`thinking`). | Analyse Conversational Analytics & BigQuery. |
| **Speaking (Parole / Synthèse)** | Ondulations douces au rythme de la voix (`speaking`). | Restitution sonore Text-to-Speech (TTS). |

---

# 🛠️ 4. La Grille des 11 Agents Sectoriels

| Agent ID | Icône Material / Lucide | Intitulé Métier | Positionnement B2B |
| :--- | :--- | :--- | :--- |
| **sully** | `user_check` / `UserCheck` | Emploi Public & RH | Audit vacance des postes & CV PDF GCS |
| **credit_advisor** | `trending_up` / `TrendingUp` | Risque Crédit & Finance B2B | Scoring faillite PME & IFRS 9 |
| **net_arch** | `cpu` / `Cpu` | Télécoms & IoT 5G | ARPU abonnés & Maintenance pylônes |
| **earth_intel** | `globe` / `Globe` | Spatial & Imagerie Satellite | Télédétection NDVI & Déforestation CSRD |
| **transit_navigator** | `navigation` / `Navigation` | Transports & SNCF | Yield Management & Retards gares |
| **pulse_checker** | `activity` / `Activity` | Santé Publique & Urgences | Plan Blanc & Ruptures stock médicaments |
| **shelf_optimizer** | `package` / `Package` | CPG Retail & Merchandising | Éradication Shelf-Out & Bundles Frais |
| **arena_manager** | `award` / `Award` | Sport & Stades RES | Remplissage loges VIP & Audit énergie |
| **helios** | `zap` / `Zap` | Énergie & Bornes IRVE | Supervision 10k bornes & Effacement |
| **ceres** | `leaf` / `Leaf` | Agriculture & Agroécologie | Rendements & Label Bas-Carbone ADEME |
| **cine_analyst** | `film` / `Film` | Cinéma & Box-Office CNC | ROI Box-Office & Formats IMAX/4DX |

---

# 📋 5. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur Full-Stack Google Cloud et un Designer UX/UI d'exception.
Ta mission est de coder l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents.

CONSIGNES STRICTES DE STYLE & STRUCTURE ("Google Fluid Blue") :

1. PALETTE CHROMATIQUE & VARIABLES CSS :
   - Fond global : radial-gradient(circle at 50% 30%, #070f2b 0%, #020617 70%, #000000 100%).
   - Surfaces Bento : rgba(15, 23, 42, 0.45) avec bordures rgba(51, 65, 85, 0.5) et backdrop-filter blur(12px).
   - Accents : linear-gradient(135deg, #38bdf8 0%, #3b82f6 50%, #6366f1 100%).

2. ARCHITECTURE D'ÉCRAN DOUBLE :
   - Écran A (Showcase / Public) : Orbe Gemini Live géant avec vagues wave-1/2/3, Data Canvas 70% largeur avec graphiques style Looker et carte 3D SQLFlipCard (Recto KPI / Verso SQL néon).
   - Écran B (Contrôleur Tactile) : Grille compacte des 11 agents sectoriels, barre de saisie hybride fixe en bas d'écran avec bouton Push-to-Talk et Smart Chips d'exemples.

3. RÉSILIENCE & NIVEAU DE BRUIT :
   - Si l'environnement est bruyant, l'application bascule silencieusement sur le clavier virtuel avec le message d'aide "Environnement bruyant ? Saisissez votre question ici !".
```
