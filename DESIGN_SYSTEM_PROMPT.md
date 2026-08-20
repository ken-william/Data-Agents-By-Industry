# Master Specification & Prompt System - Talk to Data (3D Google Luminous Wave Canvas System)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée selon le design system **3D Google Luminous Wave** avec rendu Canvas 3D immersif aux 4 couleurs Google.

---

# 🌊 1. Les Principes du 3D Google Luminous Wave

### A. Rendu 3D Canvas Plein Écran
- **Perspective 3D & Projection Mathématique** : Rendu d'un ruban et d'un maillage de vagues 3D ondulantes (`Math.sin`, `Math.cos`, projection avec `fov / (fov + z)`).
- **Les 4 Couleurs Claires Google** :
  * **Bleu Google** : `#4285F4`
  * **Rouge Google** : `#EA4335`
  * **Jaune Google** : `#FBBC05`
  * **Vert Google** : `#34A853`
- **Surface Cloturée & Lumineuse** : Fond clair lumineux (`#F8FAFC` / `#FFFFFF`) réhaussé des vagues 3D fluides.

---

# 🔮 2. Interactions Parallaxe GSAP & Scrollytelling

- **Parallaxe Souris 3D** : Le tilt et l'inclinaison de la vague 3D s'adaptent doucement au curseur de la souris via `gsap.to()`.
- **Modulation au Scroll** : Le défilement de la page (`scrollFraction`) fait onduler et amplifier l'amplitude des vagues 3D en 60FPS.

---

# 🔊 3. Purification Vocale Live (`sanitizeForSpeech`)

Toute réponse orale est filtrée par `sanitizeForSpeech()` pour exclure le code SQL, les objets JSON et la syntaxe Markdown, afin d'offrir une conversation naturelle en français.

---

# 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu me codes l'application web double écran "Talk to Data" avec l'animation arrière-plan 3D Google Wave Canvas.

CONSIGNES STRICTES :
1. ANIMATION 3D WAVE CANVAS : Maillage de vagues 3D ondulantes aux 4 couleurs claires Google (#4285F4, #EA4335, #FBBC05, #34A853).
2. PARALLAXE SOURIS GSAP : Inclinaison fluide du canvas 3D avec GSAP.
3. FOND LUMINEUX CLAIR : Fond blanc/bleu céleste dépoli.
```
