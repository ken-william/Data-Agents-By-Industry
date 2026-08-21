# Master Specification & Prompt System - Talk to Data (Bright Luminous Ice-Blue Theme - NO BLACK)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée pour bannir tout fond noir ou sombre et garantir un arrière-plan clair, lumineux et céleste.

---

# 🎨 1. Palette & Arrière-plan Lumineux (NO BLACK / NO DARK)

| Élément UI | Spécification Visuelle |
| :--- | :--- |
| **Fond Global** | Dégradé lumineux céleste bleu ciel / blanc argenté (`radial-gradient(circle at 50% 35%, #E0F2FE 0%, #DBEAFE 45%, #EFF6FF 80%, #FFFFFF 100%)`). |
| **Navbar** | Verre dépoli clair `bg-white/80 border-b border-slate-200/80 backdrop-blur-xl text-slate-900`. |
| **Cartes d'Agents Sectoriels** | Cartes blanc pur `#FFFFFF` avec bordures fines `border-slate-200` et ombres adoucies. |
| **Carte Sélectionnée** | Bleu Google `#0B57D0` intense avec texte blanc pur `#FFFFFF`. |
| **Bouton d'Action** | Bouton bleu Google `#0B57D0` avec flèche `→`. |

```css
html, body {
  background: radial-gradient(circle at 50% 35%, #E0F2FE 0%, #DBEAFE 45%, #EFF6FF 80%, #FFFFFF 100%) !important;
  color: #0F172A;
  font-family: "Google Sans Flex", "Google Sans", "Inter", sans-serif;
  min-height: 100dvh;
}
```

---

# 📋 2. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" avec un thème clair lumineux bleu céleste (SANS AUCUN NOIR).

CONSIGNES STRICTES :
1. AUCUN FOND SOMBRE NI NOIR : background radial-gradient(circle at 50% 35%, #E0F2FE 0%, #DBEAFE 45%, #EFF6FF 80%, #FFFFFF 100%).
2. CARTES BLANCHES PUR : bg-white avec bordures border-slate-200.
3. BOUTONS BLEU GOOGLE : bg-[#0B57D0] pour l'agent actif et le bouton de lancement.
```
