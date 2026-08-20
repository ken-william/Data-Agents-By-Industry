# Master Specification & Prompt System - Talk to Data (Google Fluid Blue)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** pour l'événement **BigData Paris 2026**.

---

## 🎨 1. Le Design System "Google Fluid Blue" (Inspiré de Gemini)

Ce design system abandonne le noir brut au profit d'un environnement sombre à base de bleu marine profond, enrichi par des gradients lumineux inspirés de **Gemini Live**.

### Palette Chromatique (Gradients & Surfaces)

| Élément UI | Propriété / Classe Tailwind | Rendu Visuel / Description |
| :--- | :--- | :--- |
| **Fond Global (Canvas)** | `bg-gradient-to-br from-[#020617] via-[#070F2B] to-[#0A192F]` | Bleu nuit/marine extrêmement profond, offrant un aspect mat et haut de gamme. |
| **Bento Cards (Surfaces)** | `bg-[#0B132B]/60 border border-slate-800/80 backdrop-blur-md` | Cartes semi-transparentes avec un léger flou d'arrière-plan. |
| **Liseré Actif / Focus** | `border-sky-500/40 shadow-[0_0_15px_rgba(14,165,233,0.15)]` | Remplacement des gros halos par une lueur fine et chirurgicale de couleur cyan/bleu. |
| **Gradient Gemini (Accent)** | `from-[#38BDF8] via-[#3B82F6] to-[#6366F1]` | Dégradé fluide signature (Sky Blue ➔ Royal Blue ➔ Indigo). |
| **Texte Principal** | `text-slate-100` | Blanc cassé doux pour éviter la fatigue oculaire du blanc pur. |
| **Texte Secondaire** | `text-slate-400` | Gris bleuté pour toutes les descriptions et informations secondaires. |

### Typographie & Formes

| Propriété | Règle Métrique | Justification B2B |
| :--- | :--- | :--- |
| **Police Titres** | `Google Sans` / `Inter` (Font-Weight: 600) | Modernité, clarté et lisibilité parfaite à distance sur grand écran. |
| **Coins (Cards/Bento)** | `rounded-2xl` (16px) | Forme adoucie mais professionnelle. Fini l'aspect "jouet" des coins à 32px. |
| **Coins (Boutons/Chips)** | `rounded-lg` (8px) | Structure rigoureuse pour les éléments d'action et les filtres. |

---

## 🖥️ 2. Architecture Double Écran (Dual-Screen Setup)

Pour une démonstration fluide, les rôles sont strictement répartis entre l'écran public de présentation et le terminal de l'utilisateur.

```text
+------------------------------------------------------------------------------------------------+
|                                     DUAL-SCREEN ARCHITECTURE                                   |
+------------------------------------------------------------------------------------------------+
|  ÉCRAN A : LE GRAND ÉCRAN (SHOWCASE)           |  ÉCRAN B : LE PC CONTRÔLEUR (TACTILE)         |
|  - Orbe Gemini Géant et Fluide (Centre)         |  - Grille des 11 Agents (Format Compact)     |
|  - Visualisation des Données (70% Largeur)     |  - Smart Challenge Chips (Défis instantanés)  |
|  - Requête SQL en Direct (Flip Card Discret)   |  - Console Vocale (Push-to-Talk) / Entrée     |
|  - Statuts & Indicateurs Clés Métiers          |  - Toggle Sécurité & Mode Démo                |
+------------------------------------------------------------------------------------------------+
```

### Spécifications comparatives des deux écrans

| Caractéristique | ÉCRAN A : Le Grand Écran (Showcase / Public) | ÉCRAN B : Le PC / Tablette (Contrôleur) |
| :--- | :--- | :--- |
| **Cible** | Le public du salon, les spectateurs. | Le présentateur ou le client manipulant la démo. |
| **Priorité Visuelle** | L'**Orbe Gemini Live** et les **Résultats de données** (Graphiques et tableaux épurés). | La **sélection rapide d'agents** et la **saisie de questions**. |
| **Composant Phare** | `DynamicDataCanvas` : Rendu Markdown ultra-pro avec animations d'apparition des lignes. | `AgentSwitcherGrid` + `SmartChips` : Boutons compacts réactifs au clic/tactile. |
| **Affichage Technique** | `SQLFlipCard` qui se retourne élégamment lors de l'exécution pour montrer la requête BigQuery. | Console de logs simplifiée indiquant l'état de la connexion au Data Agent Kit. |
| **Taille Textes** | Titres en `text-4xl` ou `text-5xl` pour une lecture à 3 mètres. | Textes compacts en `text-sm` et `text-xs` pour optimiser l'espace. |

---

## 🔮 3. L'Orbe Gemini Live : Le "Cœur" de l'Interface

L'avatar vocal est un **orbe fluide vectoriel (Canvas/SVG)** calqué sur l'expérience mobile de **Gemini Live**, avec des vagues organiques oscillantes.

```text
  [Idle State]             [Listening State]           [Thinking State]           [Speaking State]
    Soft Glow             Active Soundwaves           Spinning Gradients            Pulse Wave
     (Bleu)                 (Bleu/Indigo)               (Gemini Gradient)           (Cyan/Turquoise)
```

### Les 4 États de l'Orbe Fluidique

| État | Comportement de l'Orbe | Palette de Couleurs |
| :--- | :--- | :--- |
| **Idle (Attente)** | Pulsation lente et circulaire (effet de respiration). | `#3B82F6` (Bleu Royal) avec opacité à 40%. |
| **Listening (Écoute)** | L'orbe se transforme en ondes de fréquences vocales (Soundwaves) réactives au volume du micro. | `#38BDF8` (Cyan) fusionnant vers le `#6366F1` (Indigo). |
| **Thinking (Réflexion SQL)** | Rotation fluide et continue d'un anneau de gradient double (symbole de la génération BigQuery). | Gradient complet Gemini : Rose, Violet, Indigo, Bleu. |
| **Speaking (Parole / Synthèse)** | Ondulations douces et concentriques s'étendant vers l'extérieur au rythme de la voix (TTS). | `#22C55E` (Émeraude) à `#0EA5E9` (Sky Blue). |

---

## 🛠️ 4. La Grille des 11 Agents (Design Épuré)

Chaque agent est affiché sous forme d'une carte Bento sobre avec des **icônes monochromes raffinées** et de subtils badges gris-bleutés.

| Agent ID | Icône | Couleur Thématique (Subtile) | Positionnement Métier (B2B) |
| :--- | :--- | :--- | :--- |
| **sully** | `UserCheck` | `text-blue-400` | RH & Vacance des Postes Publics |
| **credit_advisor** | `TrendingUp` | `text-sky-400` | Risque Crédit & Provisionnement IFRS 9 |
| **net_arch** | `Cpu` | `text-indigo-400` | Télécoms & Maintenance IoT 5G |
| **earth_intel** | `Globe` | `text-teal-400` | Satellite, Télédétection & Déforestation |
| **transit_navigator** | `Navigation` | `text-cyan-400` | Logistique & Transports Publics |
| **pulse_checker** | `Activity` | `text-emerald-400` | Santé Publique & Gestion des Urgences |
| **shelf_optimizer** | `Package` | `text-blue-300` | CPG Retail & Optimisation des Stocks |
| **arena_manager** | `Award` | `text-indigo-300` | Sport & Performance Énergétique |
| **helios** | `Zap` | `text-amber-400` | Bornes Électriques & Réseau Intelligent |
| **ceres** | `Leaf` | `text-green-400` | Bilans ACV & Agroécologie |
| **cine_analyst** | `Film` | `text-violet-400` | Analyse du Box-Office & ROI Cinéma |

---

## 📋 5. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur Full-Stack Google Cloud et un Designer UX/UI d'exception.
Ta mission est de coder l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents.

CONSIGNES STRICTES DE STYLE & STRUCTURE ("Google Fluid Blue") :

1. ARCHITECTURE D'ÉCRAN DOUBLE :
   - Écran A (Grand Écran / Présentation) : Épuré, immersif. Met en valeur l'Orbe Gemini (centre) et le Canvas des Résultats (70% de la largeur). Intègre le composant SQLFlipCard qui se retourne pour afficher la requête BigQuery native avec coloration syntaxique SQL.
   - Écran B (PC / Contrôleur) : Dense et ergonomique. Affiche la grille des 11 agents en cartes compactes, un panneau de Push-to-Talk pour la voix, et les Smart Challenge Chips sous forme de boutons d'action rapide.

2. PALETTE & THÉMATIQUE GEMINI :
   - Fond global : Dégradé bleu marine mat profond `bg-gradient-to-br from-[#020617] via-[#070F2B] to-[#0A192F]`. Fini le noir absolu ou les halos fluorescents.
   - Surfaces Bento : `bg-[#0B132B]/60` avec des bordures très fines et élégantes `border-slate-800/80` et un effet de flou backdrop-blur-md.
   - Accents : Utilise exclusivement un gradient fluide Gemini de bleu royal à indigo pour les actions clés (`from-sky-400 via-blue-500 to-indigo-500`).

3. ORBE GEMINI LIVE VECTOREL :
   - Coder l'avatar vocal sous forme de composant SVG dynamique simulant l'orbe de Gemini Live.
   - Implémenter 4 états animés : 
     * Idle : Pulsation bleue douce circulaire.
     * Listening : Ondes de fréquences réactives au micro (cyan/indigo).
     * Thinking : Rotation d'un anneau de gradient Gemini multicolore.
     * Speaking : Ondulations concentriques fluides vertes/bleues coordonnées avec la synthèse vocale.

4. ICÔNES ET COMPACITÉ :
   - Utilise des icônes unicolores et sobres.
   - Masque par défaut les données techniques lourdes (comme le nom complet du Dataset BigQuery) et affiche-les uniquement au survol dans un petit badge de métadonnées discret (`text-slate-500 text-[11px]`).

5. RÉSILIENCE :
   - Si l'appel API à l'agent échoue (ex: 404/500), affiche une notification d'erreur élégante et propose un mode dégradé gracieux (Visualisation d'exemples hors-ligne).
```
