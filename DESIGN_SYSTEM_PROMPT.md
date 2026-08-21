# Master Specification & Prompt System - Talk to Data (Editorial Bento Grid & High-End Minimalist Style)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée selon le design system **Editorial Bento Grid** d'après la référence visuelle (`media_1787309819040.png`).

---

# 🎨 1. Design System & Palette Chromatique

| Élément UI | Classe Tailwind / Style | Spécification Visuelle |
| :--- | :--- | :--- |
| **Fond Global** | `bg-[#F4F6F9]` | Fond épuré gris-glacé ultra-doux et lumineux. |
| **Cartes Bento Principales** | `bg-white rounded-3xl p-8 border border-slate-200/80 shadow-sm` | Cartes blanches aux coins généreux `rounded-3xl` (24px - 32px), bordures fines et ombres subtiles. |
| **Bouton d'Action Noir Contrasté** | `bg-slate-950 hover:bg-slate-800 text-white rounded-full px-6 py-3 font-semibold` | Bouton capsule noir intense avec flèche `→` pour les actions principales. |
| **Accordéons / Cartes Grises** | `bg-slate-100/90 rounded-2xl p-4 border border-slate-200/60 flex justify-between` | Tiroirs/cartes gris clairs avec icônes de bascule `+` et `-`. |
| **Puces d'Agents (Chips)** | `bg-white border border-slate-200/80 rounded-full px-4 py-2 text-xs font-semibold shadow-xs` | Capsules blanches arrondies `rounded-full` s'adaptant automatiquement à la taille du texte. |

---

# 📐 2. Layout Bento Grid (Structure Double Colonne)

- **Colonne Gauche (Headline & Chips)** :
  * Sur-titre avec puce bleue : `• Copilotes Métiers`
  * Titre Éditorial Géant : *"Explore our 11 sector AI copilots."*
  * Puces d'Agents Sectoriels : Capsules d'agents avec icônes métiers.
  * Tiroirs d'Accordéon : Cartes grises pliables (`Connexions BigQuery +`, `Packs Décisionnels -`).
- **Colonne Droite (Carte Feature & Poster Visualizer)** :
  * Sur-titre : `BIGDATA — 2026`
  * Texte descriptif : *"Smart features designed to move with your enterprise data — fast, flexible, and built for everyday action."*
  * Poster Visuel Néo-Brutaliste : Grand visuel aux couleurs vibrantes Google avec badge flottant (`Précision 86%`, `Boost`).
  * Bouton d'Action Noir : `Commencer l'Analyse →`.

---

# 📋 3. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" selon le style Editorial Bento Grid (media_1787309819040.png).

CONSIGNES STRICTES :
1. LAYOUT BENTO GRID : Structure à 2 colonnes avec cartes blanches rounded-3xl sur fond #F4F6F9.
2. BOUTONS NOIRS INTENSES : Boutons d'action capsules noirs avec flèches →.
3. ACCORDÉONS GRIS ENCAPSULÉS : Tiroirs gris clair avec icônes + et -.
4. PUCES D'AGENTS SECTORIELS : Capsules blanches adaptées à la taille du texte.
```
