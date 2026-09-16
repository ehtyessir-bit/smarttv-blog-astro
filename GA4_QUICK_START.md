# 🚀 QUICK ACTION: Google Analytics 4 + GSC Setup

## Pour: blog.smarttv.one avec email theyemoo@gmail.com

---

## ✅ Ce qui a été fait (automatiquement)

1. ✅ Composant GA4 créé (`src/components/GoogleAnalytics.astro`)
2. ✅ Intégré dans le layout BlogPost.astro
3. ✅ Support GSC métabalise ajouté
4. ✅ Variables d'environnement préparées (.env.example)
5. ✅ Guide de configuration créé (GOOGLE_ANALYTICS_SETUP.md)
6. ✅ Code pushé vers GitHub → Vercel prêt

---

## 🎯 ACTIONS REQUISES (Toi)

### 1. Créer GA4 Property (5 min)

```
URL: https://analytics.google.com
Email: theyemoo@gmail.com
```

**Steps:**
1. Go to Admin → Create Property
2. Name: `smarttv-blog-astro`
3. Add Web Stream for `blog.smarttv.one`
4. **COPY**: Measurement ID (format: `G-XXXXXXXXXX`)

### 2. Ajouter GA4 ID à Vercel (2 min)

**Via dashboard Vercel:**
1. Aller à: https://vercel.com/ehtyessir-bit/smarttv-blog-astro
2. Settings → Environment Variables
3. Ajouter:
   ```
   PUBLIC_GA_ID = G-XXXXXXXXXX
   ```
4. Sauvegarder → Auto-redéploie

**OU via CLI:**
```bash
vercel env add PUBLIC_GA_ID
# Enter: G-XXXXXXXXXX
```

### 3. Vérifier GA4 fonctionne (1 min)

1. Visiter: https://blog.smarttv.one
2. Ouvrir Dev Tools (F12) → Console
3. Chercher `gtag` → pas d'erreur ✅
4. Attendre 24h pour voir données dans Google Analytics

### 4. Configurer Google Search Console (5 min)

```
URL: https://search.google.com/search-console
Email: theyemoo@gmail.com
```

**Steps:**
1. Ajouter propriété: `https://blog.smarttv.one`
2. Choisir vérification par **HTML Meta Tag**
3. Copier: `google-site-verification=xxxxx`
4. **OPTION A: Auto** - Ajouter à Vercel:
   ```
   PUBLIC_GSC_VERIFICATION = xxxxx
   ```
5. **OPTION B: Manuel** - Ajouter au DNS du domaine smarttv.one

### 5. Lier GA4 + GSC (2 min)

Dans Google Analytics:
1. Admin → Property → Google Search Console (link)
2. Click: Link Search Console
3. Sélectionner: `blog.smarttv.one`
4. Sauvegarder

---

## ⏱️ Timeline

| Action | Temps | Status |
|--------|-------|--------|
| GA4 création | 5 min | ⏳ TODO |
| Ajouter GA4 ID à Vercel | 2 min | ⏳ TODO |
| Test GA4 | 1 min | ⏳ TODO |
| GSC setup | 5 min | ⏳ TODO |
| Lier GA4+GSC | 2 min | ⏳ TODO |
| **TOTAL** | **15 min** | ⏳ TODO |

---

## 📊 Résultat Final

**Après 24-48h:**
- ✅ blog.smarttv.one tracked par GA4
- ✅ Analytics data dans Google Analytics Dashboard
- ✅ Search Console affiche l'indexation
- ✅ Données de clics/impressions dans Analytics

---

## 🔗 Ressources

- [Google Analytics Setup](./GOOGLE_ANALYTICS_SETUP.md)
- [Analytics Console](https://analytics.google.com)
- [Search Console](https://search.google.com/search-console)
- [GitHub Repo](https://github.com/ehtyessir-bit/smarttv-blog-astro)

---

## 💬 Support

**Email**: theyemoo@gmail.com
**Repo**: ehtyessir-bit/smarttv-blog-astro
**Blog**: https://blog.smarttv.one
