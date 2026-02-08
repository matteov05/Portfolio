# Portfolio BUT R&T ROM - Guide de Démarrage

## 📁 Arborescence du Projet

```
Portfolio-site/
├── index.html                    # Page principale
├── styles/
│   └── main.css                 # CSS global (design system complet)
├── js/
│   ├── components.js            # Composants réutilisables
│   └── app.js                   # Routage et gestion navigation
├── data/
│   └── competences.json         # Données des 5 compétences
├── pages/                       # (Dossier préparé pour futures pages)
├── assets/
│   └── icons/                   # Dossier pour les icônes (SVG optionnels)
└── README.md                    # Ce fichier
```

## 🚀 Lancer le site en local

### Méthode 1: Avec Python (Simple)
```bash
cd /Users/matteovargiu/Desktop/Portfolio-site
python3 -m http.server 8000
```
Puis ouvrir: **http://localhost:8000**

### Méthode 2: Avec Node.js (si installé)
```bash
npm install -g http-server
http-server .
```

### Méthode 3: Directement dans VS Code
- Installer l'extension **Live Server** (par Ritwick Dey)
- Clic droit sur `index.html` → "Open with Live Server"

## 📋 Structure des données

Le fichier `data/competences.json` contient:
```json
{
  "competences": [
    {
      "id": 1,
      "slug": "administrer-reseaux-internet",
      "title": "Administrer les réseaux et l'Internet",
      "description": "Votre description...",
      "keywords": ["DNS", "DHCP", "BGP", ...],
      "icon": "network",
      "sae": [],
      "alternance": { "description": "..." },
      "apprentissages_critiques": {
        "but1": [],
        "but2": [],
        "but3": []
      },
      "preuves": {
        "rapports": [],
        "github": [],
        "autres": []
      }
    },
    ...
  ]
}
```

## 🎨 Personnalisation

### Couleurs
Modifiez les variables CSS dans `styles/main.css`:
```css
:root {
  --color-primary: #7c3aed;        /* Violet */
  --color-secondary: #000000;      /* Noir */
  --color-bg: #ffffff;             /* Blanc */
  ...
}
```

### Polices
Changez `--font-primary` pour utiliser votre police préférée.

### Icônes
Les icônes sont générées en SVG inline dans `js/components.js`. Modifiez la fonction `Component.createIcon()` pour ajouter les vôtres.

## 📝 Format du contenu à ajouter

### Pour la description (BUT1, BUT2, BUT3 dans AC):
- Format simple: Une ligne par AC
- JSON: Tableau d'objets

Exemple AC:
```json
"apprentissages_critiques": {
  "but1": [
    "AC 1.1 - Installer et configurer un OS",
    "AC 1.2 - Sécuriser une infrastructure"
  ],
  "but2": ["..."],
  "but3": ["..."]
}
```

### Pour les SAE:
Structure complète à ajouter (page détail):
```json
"sae": [
  {
    "id": 1,
    "title": "SAE 1.3 - Supervision réseau",
    "year": "BUT1",
    "description": "Création d'un outil de monitoring",
    "objectives": ["...", "..."],
    "realisations": "...",
    "competences": ["..."],
    "ac_mobilises": ["AC 1.1", "AC 1.2"],
    "technos": ["Docker", "Prometheus", "Grafana"],
    "lien_detail": "#sae-1-3"
  }
]
```

## 🌐 Déploiement sur GitHub Pages

### 1. Créer un repo GitHub
```bash
git init
git add .
git commit -m "Initial commit: Portfolio skeleton"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/portfolio.git
git push -u origin main
```

### 2. Activer GitHub Pages
- Aller sur: Settings → Pages
- Source: Branch `main` / folder `root`
- Custom domain: (optionnel)
- Sauvegarder

### 3. Votre site est en ligne!
🎉 Accédez-le via: `https://YOUR_USERNAME.github.io/portfolio`

## 💡 Conseils d'utilisation

1. **Remplir progressivement**: Les PLACEHOLDER facilitent le suivi
2. **Valider localement**: Testez avant chaque push
3. **Versionner**: Commitez régulièrement
4. **Structure claire**: Gardez les données JSON bien organisées
5. **Ajouter des preuves**: Liens GitHub, rapports PDF, etc.

## 📱 Responsivité

Le design s'adapte automatiquement sur:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## ✅ Checklist avant le premier envoi

- [ ] `index.html` testé localement
- [ ] `data/competences.json` bien structuré
- [ ] CSS chargé correctement
- [ ] Navigation fonctionne (hash routing)
- [ ] Accordéons AC fonctionnels
- [ ] Menu mobile responsive
- [ ] Footer affiche bien
- [ ] Repo Git créé et pushé

## 🔧 Troubleshooting

### Les styles ne chargent pas
- Vérifier le chemin: `./styles/main.css` (point obligatoire)
- Recharger (Ctrl+Shift+R ou Cmd+Shift+R sur Mac)

### La navigation ne marche pas
- Vérifier que `js/app.js` et `js/components.js` sont chargés
- Ouvrir la console (F12) pour voir les erreurs

### Les données ne s'affichent pas
- Vérifier le chemin `./data/competences.json`
- S'assurer que le JSON est valide: https://jsonlint.com/

## 📧 Support & Prochaines étapes

Une fois ce squelette validé, on remplira page par page:
1. Présentation d'accueil
2. CV Français
3. CV Anglais
4. Compétence 1 + SAE détails
5. etc.

À toi! 🚀
