# Master Specification & Prompt System - Talk to Data (Google Luminous Aurora Light & Vibrant Theme)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée pour garantir un design **100% VIF, CLAIR ET LUMINEUX** (aucun fond noir ou sombre).

---

# 🎨 1. Les 4 Thèmes Visuels Célestes et Vifs (BRIGHT ONLY)

| Identifiant | Nom du Thème | Fond Lumineux (`--aurora-bg`) | Palette Vibrante |
| :--- | :--- | :--- | :--- |
| **`cloud-next`** *(Défaut)* | **Google Cloud Next** | Blanc Céleste `#F8FAFC` | Bleu `#4285F4`, Rouge `#EA4335`, Jaune `#FBBC05`, Vert `#34A853`. |
| **`gemini-aurora`** | **Gemini AI Official** | Bleu Glacé `#F0F9FF` | Cyan `#38BDF8`, Violet `#818CF8`, Magenta `#C084FC`, Rose `#EC4899`. |
| **`tech-sunset`** | **Techmakers Sunset** | Ambre Chaud `#FFF7ED` | Magenta `#E11D48`, Orange `#F97316`, Or `#F59E0B`, Violet `#7C3AED`. |
| **`eco-system`** | **Workspace Harmony** | Menthe Claire `#F0FDF4` | Émeraude `#10B981`, Menthe `#34D399`, Teal `#14B8A6`, Cyan `#06B6D4`. |

```css
:root[data-theme="cloud-next"] {
  --aurora-1: #4285F4;
  --aurora-2: #EA4335;
  --aurora-3: #FBBC05;
  --aurora-4: #34A853;
  --aurora-bg: #F8FAFC;
}
```

---

# 🔮 2. Aurore Lumineuse Vivante & Contrastes Élevés

- **Fond "Luminous Aurora"** : Animation CSS fluide de 4 nébuleuses organiques vifs en fusion sous un filtre `blur(100px)` sur fond clair céleste `#F8FAFC`.
- **Bento Cards Blanc Pur (`bg-white/95`)** : Cartes blanches avec ombres adoucies `0 10px 30px rgba(0, 0, 0, 0.05)` et texte noir-ardoise `#0F172A` ultra-net.

---

# 📋 3. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" selon le thème Google Luminous Aurora 100% CLAIR ET VIF.

CONSIGNES STRICTES :
1. FOND CLAIR ET VIF : Arrière-plan animé céleste #F8FAFC avec aurores vibrantes (Bleu #4285F4, Rouge #EA4335, Jaune #FBBC05, Vert #34A853). AUCUN FOND SOMBRES OU NOIR (#050b24 BANNIS).
2. CARTES BLANCHES PUR : bg-white/95 avec texte sombre #0F172A pour une lisibilité parfaite.
3. 4 THÈMES CLAIRS VIFS : Cloud Next, Gemini Aurora, Tech Sunset, Eco-System.
```
