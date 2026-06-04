# Google Analytics 4 + Google Search Console Setup Guide

## 📊 Étape 1: Créer une propriété Google Analytics 4

### Via Google Analytics (analytics.google.com)

1. **Se connecter** avec theyemoo@gmail.com à https://analytics.google.com
2. **Cliquer** sur **Admin** (⚙️ en bas à gauche)
3. **Propriété** → **+ Créer une propriété**
   - Nom: `smarttv-blog-astro`
   - Type de compte: Standard
   - Fuseau horaire: Europe/Berlin
4. **Ajouter un flux Web**
   - URL: `https://blog.smarttv.one`
   - Nom du flux: `blog-smarttv-one`
5. **Copier le MEASUREMENT ID** (format: `G-XXXXXXXXXX`)

### ⚡ Résultat attendu:
```
G-XXXXXXXXXX (ex: G-3ABC1DEFGH)
```

---

## 🔗 Étape 2: Ajouter GA4 à blog.smarttv.one

### A. Ajouter la variable .env

```bash
# Dans astro-blog-smarttv/.env
PUBLIC_GA_ID=G-XXXXXXXXXX
```

### B. Redéployer sur Vercel

```bash
cd astro-blog-smarttv
git add -A
git commit -m "setup: add Google Analytics 4 tracking"
git push
```

✅ **Vercel redéploiera automatiquement avec GA4**

---

## 🔍 Étape 3: Configurer Google Search Console

### 1. Accéder à Google Search Console
- URL: https://search.google.com/search-console

### 2. Ajouter la propriété
- **Propriété URL**: `https://blog.smarttv.one`
- **Méthode de vérification**: 
  - Sélectionner **Enregistrement DNS** ou **Métabalise HTML**
  
#### Option A: Métabalise HTML (recommandé)
1. Copier le code de vérification: 
   ```html
   <meta name="google-site-verification" content="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx">
   ```
2. Ajouter au fichier `.env`:
   ```
   PUBLIC_GSC_VERIFICATION=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
3. Ajouter au `src/layouts/BlogPost.astro`:
   ```astro
   <meta name="google-site-verification" content={import.meta.env.PUBLIC_GSC_VERIFICATION}/>
   ```

#### Option B: Enregistrement DNS
1. Copier l'enregistrement TXT: `google-site-verification=xxxxx`
2. Ajouter au DNS de ton domaine (smarttv.one)

### 3. Vérifier la propriété
- Cliquer **Vérifier** après avoir ajouté la métabalise ou l'enregistrement DNS
- ✅ La vérification peut prendre 24-48h

---

## 📈 Étape 4: Lier GA4 et Google Search Console

### Via Google Analytics
1. **Aller à**: Admin → Propriété → **Google Search Console** (lien)
2. **Cliquer** sur **Lier les données de Search Console**
3. **Sélectionner** ta propriété Google Search Console `blog.smarttv.one`
4. **Sauvegarder**

---

## ✅ Vérification Finale

### Check 1: Vérifier GA4 fonctionne
1. Visiter https://blog.smarttv.one
2. **Ouvrir Developer Tools** (F12)
3. **Onglet Console** → Vérifier qu'il n'y a **pas d'erreur** GA4
4. Attendre **24h**, puis vérifier dans **Google Analytics** → **Rapports** → **Temps réel**

### Check 2: Vérifier Google Search Console
1. Aller à https://search.google.com/search-console
2. Sélectionner `blog.smarttv.one`
3. Attendre **48h** pour voir les données d'indexation

---

## 🎯 Résumé des Actions

| Étape | Action | Status |
|-------|--------|--------|
| 1 | Créer GA4 dans analytics.google.com | ⏳ À faire |
| 2 | Copier `G-XXXXXXXXXX` | ⏳ À faire |
| 3 | Ajouter à `.env` `PUBLIC_GA_ID` | ⏳ À faire |
| 4 | Git push pour redéployer | ⏳ À faire |
| 5 | Ajouter blog.smarttv.one à GSC | ⏳ À faire |
| 6 | Vérifier la propriété GSC | ⏳ À faire |
| 7 | Lier GA4 + GSC | ⏳ À faire |

---

## 📞 Support

**Email**: theyemoo@gmail.com

**Domaines**:
- Blog: https://blog.smarttv.one
- Main: https://smarttv.one

**Repository**: https://github.com/ehtyessir-bit/smarttv-blog-astro
