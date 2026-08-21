# Master Specification & Prompt System - Talk to Data (Google Blue Luminous Gradient & Glass Navbar)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée selon le design system **Google Blue Luminous Gradient** avec navbar en verre dépoli translucide et puces des 11 agents sectoriels.

---

# 🎨 1. Palette Chromatique & Fond Céleste (NO BLACK)

| Étape | Code Hexadécimal | Rôle dans l'UI |
| :--- | :--- | :--- |
| **Bleu Google Clair (Départ)** | `#79A7F7` | Haut du dégradé de fond. |
| **Bleu Google (Milieu)** | `#4285F4` | Cœur du dégradé. |
| **Bleu Foncé (Fin)** | `#1A56DB` | Bas du dégradé. |
| **Navbar Verre Translucide** | `rgba(255, 255, 255, 0.35)` | Flou dépoli éthéré `backdrop-filter: blur(24px)`. |
| **Puces d'Agents Sectoriels** | `#FFFFFF` / `rgba(255, 255, 255, 0.95)` | Capsules blanches dépolies avec les 11 noms d'agents sectoriels. |

```css
.google-blue-gradient-bg {
  background: linear-gradient(135deg, #79A7F7 0%, #4285F4 50%, #1A56DB 100%) !important;
  min-height: 100vh;
}
```

---

# 🔮 2. Navbar en Verre Translucide (`.glass-navbar`)

```css
.glass-navbar {
  background: rgba(255, 255, 255, 0.35);
  border-bottom: 1px solid rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}
```

---

# 💊 3. Puces d'Agents Sectoriels (11 Copilotes Métiers)

Puces de taille généreuse avec icônes métier et noms d'agents réels (*RH & Emploi Public*, *Risque Crédit & Finance*, *Télécoms & Réseau 5G*, *Spatial & Satellite*, *Transports & SNCF*, *Santé Publique*, *CPG & Grande Distribution*, *Sport, Stades & VIP*, *Énergie & Bornes IRVE*, *Agriculture & Bilan Carbone*, *Box-Office & Cinéma*).

---

# 📋 4. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" selon le style Google Blue Luminous Gradient.

CONSIGNES STRICTES :
1. FOND BLEU GOOGLE DEGRADÉ : linear-gradient(135deg, #79A7F7 0%, #4285F4 50%, #1A56DB 100%) sans aucun fond noir.
2. NAVBAR VERRE TRANSLUCIDE : Header en verre dépoli transparent (bg-white/35, backdrop-blur-2xl).
3. BARRE DE RECHERCHE CAPSULE : Barre de recherche épurée avec bouton d'envoi rond bleu.
4. PUCES DES 11 AGENTS SECTORIELS : Puces blanches avec les noms des 11 copilotes métiers BigQuery.
```
