# julespiral.github.io

Site académique personnel de Jules Piral, construit avec [Hugo](https://gohugo.io).
Le design est adapté de [buchh.org](https://github.com/JonathanBuchh/buchh.org) (licence MIT, voir `LICENSE`), avec un fond crème.

## Organisation

Le site est bilingue : l'anglais à la racine, le français sous `/fr/`.

| Je veux modifier…        | Fichier(s)                                          |
|--------------------------|-----------------------------------------------------|
| La page d'accueil        | `content/en/_index.md` · `content/fr/_index.md`     |
| La page Recherche        | `content/en/research.md` · `content/fr/research.md` |
| La page Enseignement     | `content/en/teaching.md` · `content/fr/teaching.md` |
| La page CV               | `content/en/cv.md` · `content/fr/cv.md`             |
| Les PDF du CV            | `static/cv/CV-Jules-Piral-EN.pdf` et `-FR.pdf`      |
| Le menu                  | `hugo.toml` (sections `menus.main`)                 |
| Couleurs et typographie  | `layouts/partials/style.html` (variables `--bg`, `--fg`) |

Une page existe en deux exemplaires portant le **même nom de fichier** dans `content/en/` et `content/fr/` : c'est ce qui relie les deux langues et fait apparaître le lien « English / Français » dans le menu. L'adresse française se règle avec `slug:` dans l'en-tête du fichier.

## Mettre le CV à jour

Le CV vit dans `École/A26/lectures/mémoire/09_CV/CV/` (LaTeX). Après l'avoir modifié :

```bash
./build.sh                                   # dans le dossier du CV
cp cv-fr.pdf <site>/static/cv/CV-Jules-Piral-FR.pdf
cp cv-en.pdf <site>/static/cv/CV-Jules-Piral-EN.pdf
```

## Prévisualiser

```bash
hugo server        # puis http://localhost:1313
```

## Publier

Le workflow `.github/workflows/pages.yml` compile le site avec Hugo et le publie sur GitHub Pages à chaque `git push` sur `main`. Dans les réglages du dépôt GitHub, choisir **Settings → Pages → Source : GitHub Actions**.
