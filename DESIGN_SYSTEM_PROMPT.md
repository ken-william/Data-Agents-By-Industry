# Master Specification & Prompt System - Talk to Data (Google Light Workspace - NotebookLM Style)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** inspirée de l'interface officielle **Google NotebookLM** et **Gemini Enterprise**.

---

## 🎨 1. Le Design System "Google Light Workspace" (NotebookLM Style)

Ce système repose sur des surfaces blanches, des ombres ultra-douces, des couleurs pastel pour thématiser les agents, et une typographie très aérée.

### Palette Chromatique & Textures

| Élément UI | Propriété / Classe Tailwind | Rendu Visuel / Description |
| :--- | :--- | :--- |
| **Fond d'Écran Principal** | `bg-[#F8F9FA]` / `bg-slate-50` | Blanc cassé Google officiel, extrêmement propre et reposant. |
| **Gradients de Fond (Ambient)** | `bg-gradient-to-tr from-[#EEF2F6] via-[#F1F5F9] to-[#E0E7FF]/30` | Dégradés bleus et lavande très subtils et dilués pour donner de la profondeur. |
| **Cartes Bento & Éléments** | `bg-white border border-slate-100 shadow-[0_2px_12px_rgba(0,0,0,0.03)]` | Blanc pur, se détachant doucement du fond avec une ombre presque invisible. |
| **Boutons & Actions Clés** | `bg-blue-600 hover:bg-blue-700 text-white` | Bleu Google standard pour les interactions principales. |
| **Texte Principal** | `text-[#1F1F1F]` / `text-slate-900` | Noir doux (anthracite) pour une lisibilité parfaite sans agressivité. |
| **Texte Secondaire** | `text-[#5F6368]` / `text-slate-500` | Gris neutre pour les descriptions, tags et métadonnées. |

### Typographie & Formes

| Élément | Règle Métrique | Look & Feel |
| :--- | :--- | :--- |
| **Typographie** | `Google Sans` (Titres) / `Roboto` (Corps) | Identité Google forte, lisible et épurée. |
| **Coins (Cartes Carousel)** | `rounded-2xl` (16px) | Coins élégamment arrondis sans tomber dans l'effet "bulle". |
| **Coins (Conteneurs & Dock)** | `rounded-3xl` (24px) | Courbes plus amples pour le dock de chat et les grands panneaux. |

---

## 🖥️ 2. L'Architecture Double Écran Réalignée

L'expérience se sépare toujours en deux écrans, mais adopte le style "Document & Carnet de Notes" épuré.

```text
+-------------------------------------------------------------------------------------------------+
|                                 DUAL-SCREEN WORKSPACE STRUCTURE                                 |
+-------------------------------------------------------------------------------------------------+
|  ÉCRAN A : LE GRAND ÉCRAN (SHOWCASE / PUBLIC)      |  ÉCRAN B : LE PC CONTRÔLEUR (PRÉSENTATEUR) |
|  - Orbe Gemini Translucide (Flottant discret)      |  - Carousel Horizontal Compact des Agents  |
|  - Zone de Document Active (Rendu clean type PDF)   |  - Zone de Chat et Smart Prompt Chips      |
|  - Données et Graphiques Minimalistes              |  - Bouton "Settings" (Roue crantée)        |
|  - État de synchronisation discret                 |  - Sélecteur de scénario d'utilisation     |
+-------------------------------------------------------------------------------------------------+
```

---

## 📦 3. Reconstruction des Composants Clés

### A. Le Carousel de "Scènes" (Agents Sectoriels) - Style NotebookLM
Les agents s'affichent sous forme de **petits carnets de notes alignés horizontalement** avec un défilement fluide.
- **Structure des Cartes :** Hauteur limitée (`h-36`), bordure pastel supérieure, icône monochrome, titre (`text-sm font-semibold`), description (`text-xs text-slate-500`) et badge source.
- **Flèches & Modal Galerie :** Flèches au survol + bouton **"Afficher tout"** (`Grid` icon) ouvrant un catalogue complet.

### B. Le Canvas de Résultats & SQL Inspector
- Rendu type **page de document épurée** avec lignes séparatrices gris clair.
- SQL Inspector relégué dans un onglet discret en accordéon *"Détails techniques : Requête générée par Vertex AI"*.

### C. Le Dock d'Entrée & L'Orbe Gemini Live (Version Light)
- Orbe translucide en verre dépoli (`bg-white/40 backdrop-blur-md border-white/60`) avec vagues en dégradé bleu ciel et violet pastel.
- Dock arrondi (`rounded-3xl`) inspiré de Gemini Enterprise.

### D. Le Panneau "Settings" (Roue Crantée)
Tiroir latéral (Drawer) pour ajuster les thèmes visuels, le Text-to-Speech et l'état Dataplex.

---

## 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur Full-Stack Google Cloud et un Designer UX/UI d'exception, spécialisé dans les interfaces B2B haut de gamme (style Google Workspace / NotebookLM).
Ta mission est de reconstruire l'application "Talk to Data" avec une esthétique "Light & Minimalist" moderne, propre, et fluide.

CONSIGNES STRICTES DE DESIGN (Tailwind CSS) :

1. THÈME GLOBAL ("On sort du sombre") :
   - Fond de l'application : Gris/blanc ultra-pro `bg-[#F8F9FA]` agrémenté de légers dégradés de bleus et de lavande subtils en arrière-plan (`from-[#EEF2F6] to-[#E0E7FF]/30`).
   - Surfaces et Cartes (Bento) : Blanc pur `bg-white` avec une bordure fine et discrète `border-slate-100` et une ombre douce `shadow-[0_2px_12px_rgba(0,0,0,0.03)]`.
   - Boutons et puces actives : Bleu Google standard `bg-blue-600 hover:bg-blue-700 text-white`.
   - Coins : `rounded-2xl` (16px) pour les cartes et `rounded-3xl` (24px) pour les conteneurs majeurs et le dock de chat.

2. LE CAROUSEL DE SCÈNES (Format NotebookLM) :
   - Crée un défilement horizontal fluide des 11 agents sectoriels.
   - Les cartes doivent être compactes (hauteur limitée, max `h-36`).
   - Chaque carte affiche une icône monochrome discrète, un liseré pastel thématique selon son secteur, un titre en `text-sm font-semibold`, et une description en `text-xs text-slate-500`.
   - Ajoute des flèches de navigation gauche/droite discrètes au survol et un bouton "Afficher tout" qui ouvre une vue galerie complète.

3. LE MODULE LIVE & L'ORBE GEMINI LIGHT :
   - L'Orbe Gemini adopte un style "Glassmorphism" : une sphère translucide `bg-white/30 backdrop-blur-md` avec de légères vagues ondulantes en dégradé bleu ciel et violet pastel, coordonnées avec l'activité vocale (écoute, réflexion, parole).
   - Supprime tout bouton "Connecter à BigQuery" ou badge de connexion jaune/fluo. Remplace-le par un indicateur d'état passif et minimaliste : un point vert discret `• Connecté` à côté de la source de données.
   - Le Canvas de Résultats ressemble à un document PDF/Rapport imprimé épuré, avec des tableaux aux bordures grises ultra-fines.

4. PAGE SETTINGS :
   - Intègre un bouton "Paramètres" (roue crantée) ouvrant un tiroir latéral (Drawer) ou une modal pour configurer le look and feel : changement de pack de couleurs, vitesse d'oscillation de l'orbe, activation du Text-to-Speech et sélection des agents à afficher.
```
