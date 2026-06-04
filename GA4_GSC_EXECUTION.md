# SETUP GA4 + GSC - Exécution Rapide (15 min)

## 🎯 Objectif
- Créer GA4 pour blog.smarttv.one
- Créer Google Search Console
- Lier les deux
- Email: **theyemoo@gmail.com**

---

## ⚡ ÉTAPE 1: Google Analytics 4 (5 min)

### Via Browser:
```
URL: https://analytics.google.com
Email: theyemoo@gmail.com
```

### Actions:
1. **Admin** (⚙️ en bas)
2. **+ Create Property**
3. **Property name:** `smarttv-blog-astro`
4. **Timezone:** Europe/Berlin
5. **Next** → **Create Web Stream**
6. **Website URL:** `https://blog.smarttv.one`
7. **Stream name:** `blog-smarttv-one`
8. **Create stream**

### ⭐ RÉSULTAT:
- **Measurement ID** = `G-XXXXXXXXXX`
- **Copier et sauvegarder** cette valeur!

---

## ⚡ ÉTAPE 2: Google Search Console (3 min)

### Via Browser:
```
URL: https://search.google.com/search-console
Email: theyemoo@gmail.com
```

### Actions:
1. **+ Create property**
2. **URL Prefix:** `https://blog.smarttv.one`
3. **Continue**
4. **Recommended verification:** HTML Meta Tag
5. **Copier le code:**
   ```html
   <meta name="google-site-verification" content="xxxxxxxxxxxxx">
   ```
6. **Copier JUSTE le contenu** = `xxxxxxxxxxxxx`

### ⭐ RÉSULTAT:
- **Verification code** = `xxxxxxxxxxxxx`
- **Copier et sauvegarder** cette valeur!

---

## ⚡ ÉTAPE 3: Ajouter à Vercel (3 min)

### Via Browser:
```
URL: https://vercel.com/ehtyessir-bit/smarttv-blog-astro
```

### Actions:
1. **Settings** (onglet)
2. **Environment Variables**
3. **+ Add another**

### Variable 1:
```
Name:  PUBLIC_GA_ID
Value: G-XXXXXXXXXX    ← De l'étape 1
Environments: Production, Preview, Development
```
**Save**

### Variable 2:
```
Name:  PUBLIC_GSC_VERIFICATION
Value: xxxxxxxxxxxxx    ← De l'étape 2
Environments: Production, Preview, Development
```
**Save**

### ⭐ RÉSULTAT:
- Vercel **redéploie automatiquement**
- blog.smarttv.one maintenant a GA4 tracking!

---

## ⚡ ÉTAPE 4: Vérifier GSC (48h)

### Via Browser:
```
URL: https://search.google.com/search-console
Email: theyemoo@gmail.com
```

### Actions:
1. Sélectionner `blog.smarttv.one`
2. **Verification** → **Verified** ✅
3. (Peut prendre 24-48h)

---

## ⚡ ÉTAPE 5: Lier GA4 + GSC (2 min)

### Via Browser:
```
URL: https://analytics.google.com
Email: theyemoo@gmail.com
```

### Actions:
1. **Admin** → **Property** 
2. **Google Search Console linking**
3. **Link Search Console**
4. Sélectionner: `blog.smarttv.one`
5. **Link**

### ⭐ RÉSULTAT:
- GA4 + GSC **unified dashboard**
- Données de recherche intégrées
- Clicks, impressions, CTR visibles

---

## ✅ VÉRIFICATION FINALE

### Check 1: GA4 Fonctionne?
```
1. Visiter: https://blog.smarttv.one
2. F12 → Console
3. Chercher: "gtag"
4. ✅ Pas d'erreur = OK
```

### Check 2: Analytics Dashboard?
```
1. Aller à: https://analytics.google.com
2. Sélectionner: smarttv-blog-astro
3. Aller à: Realtime
4. ✅ Voir visitors = OK
```

### Check 3: GSC Verified?
```
1. Aller à: https://search.google.com/search-console
2. Sélectionner: blog.smarttv.one
3. Status: "Verified" ✅
```

---

## 📊 Timeline Complet

| Étape | Durée | Quand |
|-------|-------|-------|
| GA4 création | 5 min | Immédiat |
| GSC création | 3 min | Immédiat |
| Ajouter à Vercel | 3 min | Immédiat |
| Redéploiement | 1 min | Immédiat |
| Premier data GA4 | ~5 min | 5-10 min |
| Dashboard complet | ~1h | 1-2 heures |
| GSC verification | 24-48h | 1-2 jours |
| Full integration | 48h | 2 jours |

---

## 🎯 Résumé Final

```
✅ GA4 Property créée: smarttv-blog-astro
✅ Measurement ID obtenu: G-XXXXXXXXXX
✅ GSC Property créée: blog.smarttv.one
✅ Verification code obtenu: xxxxxxxxxxxxx
✅ Variables ajoutées à Vercel
✅ Vercel redéployé
✅ blog.smarttv.one suivi par GA4
✅ blog.smarttv.one indexé par GSC
✅ GA4 + GSC liés
✅ Dashboard analytics active
```

---

## 💬 Support

- **Email:** theyemoo@gmail.com
- **Blog:** https://blog.smarttv.one
- **Analytics:** https://analytics.google.com
- **Search Console:** https://search.google.com/search-console
- **Vercel:** https://vercel.com/ehtyessir-bit/smarttv-blog-astro
