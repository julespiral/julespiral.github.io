# julespiral.github.io

Site académique personnel de Jules Piral, publié sur GitHub Pages à
<https://julespiral.github.io>.

Construit avec [Jekyll](https://jekyllrb.com/) à partir du thème
[Academic Pages](https://github.com/academicpages/academicpages.github.io)
(lui-même dérivé de Minimal Mistakes).

---

## Comment le site est organisé

Le site est **bilingue**. L'anglais vit à la racine, le français sous `/fr/` :

| Anglais             | Français                  |
|---------------------|---------------------------|
| `/`                 | `/fr/`                    |
| `/research/`        | `/fr/recherche/`          |
| `/publications/`    | `/fr/publications/`       |
| `/talks/`           | `/fr/communications/`     |
| `/teaching/`        | `/fr/enseignement/`       |
| `/cv/`              | `/fr/cv/`                 |

Trois mécanismes rendent ça possible :

1. **`lang:`** — chaque page et chaque entrée déclare `lang: en` ou `lang: fr`
   dans son en-tête YAML (le bloc entre `---` en haut du fichier). Les pages de
   liste ne montrent que les entrées de leur langue.
2. **`alt_lang_url:`** — pointe vers la même page dans l'autre langue. C'est ce
   qui fait apparaître le bouton **EN/FR** dans le menu. Si tu l'omets, le
   bouton disparaît sur cette page.
3. **`_data/navigation.yml`** — contient deux menus : `main` (anglais) et `fr`.

## Où se trouve quoi

| Je veux modifier…                | Fichier(s)                                        |
|----------------------------------|---------------------------------------------------|
| Mon nom, ma bio, mes liens       | `_config.yml` (section `author:`)                 |
| La page d'accueil                | `_pages/about.md` · `_pages/fr-about.md`          |
| La page Recherche                | `_pages/research.md` · `_pages/fr-research.md`    |
| Le CV                            | `_pages/cv.md` · `_pages/fr-cv.md`                |
| Le menu du haut                  | `_data/navigation.yml`                            |
| Un article                       | un fichier dans `_publications/`                  |
| Une communication                | un fichier dans `_talks/`                         |
| Un cours                         | un fichier dans `_teaching/`                      |
| Ma photo                         | `images/profile.png`                              |
| Le PDF du CV                     | `files/CV-Jules-Piral-FR.pdf`                     |

**Important :** chaque entrée existe en deux exemplaires, un par langue. Quand
tu ajoutes un article ou un cours, copie une entrée existante dans les deux
langues et ajuste `lang`, `permalink` et `alt_lang_url`.

## Ajouter une publication

Crée deux fichiers dans `_publications/`, nommés `AAAA-MM-JJ-titre-court.md`.
Copie le contenu d'une entrée existante comme modèle. Les champs utiles :

- `category:` — `articles`, `workingpapers` ou `chapters` (définis dans
  `_config.yml` sous `publication_category`, avec leur titre FR).
- `status:` — pour un manuscrit sans revue (« Manuscript in preparation »).
  S'affiche à la place de « Published in … ».
- `venue:` — la revue, une fois l'article publié. Remplace alors `status`.
- `paperurl:`, `slidesurl:`, `bibtexurl:` — génèrent automatiquement des
  boutons de téléchargement. Dépose les fichiers dans `files/`.
- `excerpt:` — le résumé d'une ligne affiché dans la liste.

## Le style LaTeX

Le site utilise un thème maison qui le fait ressembler à un article LaTeX. Il
s'active par une seule ligne dans `_config.yml` :

```yaml
site_theme               : "latex"
```

Remets `"default"` (ou `"air"`, `"mint"`…) et tu retrouves l'apparence
d'origine du template — rien d'autre à changer.

Trois fichiers portent ce thème :

| Fichier                          | Rôle                                          |
|----------------------------------|-----------------------------------------------|
| `_sass/theme/_latex_light.scss`  | polices et couleurs, version claire           |
| `_sass/theme/_latex_dark.scss`   | les mêmes, version sombre                     |
| `_sass/layout/_latex.scss`       | la mise en page (justification, numérotation…)|

**Attention :** les deux fichiers de thème définissent tous les deux les
polices, et le sombre est importé après le clair. Si tu changes de police,
change-la dans les *deux*, sinon tu obtiendras un résultat incohérent.

### La police

**Latin Modern**, celle qu'utilise LaTeX par défaut. Les fichiers sont dans
`assets/fonts/` plutôt que chargés depuis un CDN : le site reste autonome et
aucune requête n'est envoyée à un tiers quand quelqu'un visite la page. La
licence est rappelée dans `assets/fonts/README.md`.

### La numérotation des sections

Les titres `##` d'une page sont numérotés 1, 2, 3 et les `###` en 1.1, 1.2,
comme `\section` et `\subsection`. C'est fait avec des compteurs CSS, donc
la numérotation se met à jour toute seule quand tu ajoutes ou déplaces une
section.

Elle ne touche que les titres qui sont des enfants *directs* du contenu —
c'est pourquoi les titres d'articles sur `/publications/` ne sont pas
numérotés, alors que les intitulés de catégorie le sont.

Pour désactiver la numérotation sur une page, ajoute dans son en-tête YAML :

```yaml
unnumbered: true
```

### Les retraits de paragraphe

Comme dans LaTeX, un paragraphe qui en suit un autre commence par un retrait
au lieu d'être séparé par une ligne blanche. Si tu préfères l'inverse, mets
`$paragraph-indent` à `false` dans les **deux** fichiers de thème.

### Les titres de section dans le Markdown

Écris-les avec `##` et `###`, pas avec les soulignements `======` du template
d'origine : ceux-ci produisent des `<h1>`, ce qui donne plusieurs titres de
premier niveau par page (mauvais pour l'accessibilité et le référencement) et
casse la numérotation.

## Prévisualiser en local

Le site se compile dans Docker, donc rien à installer côté Ruby.

```bash
# Depuis ce dossier, une seule fois (ou après un changement au Gemfile) :
docker compose build

# Puis, à chaque session de travail :
docker compose up
```

Le site est alors sur <http://localhost:4000>. Il se recompile tout seul quand
tu enregistres un fichier — **sauf `_config.yml`**, qui exige de redémarrer
(`Ctrl-C` puis `docker compose up`).

Pour arrêter : `Ctrl-C`.

## Publier

```bash
git add -A
git commit -m "Décris ton changement"
git push
```

GitHub Pages recompile et met le site en ligne en une minute environ. En cas
d'erreur de compilation, elle apparaît dans l'onglet **Actions** du dépôt
GitHub.

## Récupérer les mises à jour du thème

Le dépôt d'origine est configuré comme second remote :

```bash
git fetch upstream
git merge upstream/master   # attends-toi à devoir résoudre des conflits
```

À faire seulement si tu as une raison précise — les fichiers de mise en page
(`_layouts/`, `_includes/`) ont été modifiés pour le bilinguisme et sont les
plus susceptibles d'entrer en conflit.

## Licence

Le thème Academic Pages est sous licence MIT (voir `LICENSE`). Le contenu du
site (textes, CV, articles) reste la propriété de son auteur.
