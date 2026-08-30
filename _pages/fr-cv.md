---
layout: archive
title: "Curriculum vitæ"
permalink: /fr/cv/
lang: fr
alt_lang_url: /cv/
author_profile: true
---

{% include base_path %}

[Télécharger mon CV (PDF)]({{ base_path }}/files/CV-Jules-Piral-FR.pdf)

## Formation
* **M. A. en science politique**, Université Laval, Québec — sept. 2026 – mai 2028 (prévu)
  * Direction : Alexandre Gajevic Sayegh et Yannick Dufresne
* **B. A. en science politique**, Université Laval, Québec — sept. 2023 – mai 2026
  * Moyenne : 4,23/4,33 · Profil distinction · Profil international
  * Tableau d'honneur de la Faculté des sciences sociales (2025-2026)
  * Mention d'honneur de la Doyenne de la Faculté des sciences sociales (2024-2025)
* **Attestation d'études politiques**, Sciences Po Lyon, France — janv. 2025 – mai 2025
  * Moyenne : A (note maximale en notation ECTS)

## Expérience de recherche
* **Projet Datagotchi Chatbot** — Auxiliaire de recherche, CLESSN, Université Laval (juill. 2026 – en cours)
  * Communication et vulgarisation de l'outil.
* **Projet Vitrine Démocratique** — Auxiliaire de recherche, CAPP, Université Laval (juin 2026 – en cours)
  * Analyse textuelle automatisée ; création de raffineurs.
* **Projet IEADB** — Auxiliaire de recherche, CIRGoM, Université Laval (janv. 2026 – sept. 2026)
  * Recherche documentaire, web scraping et nettoyage de données en R.
* **Populisme et changements climatiques** — Auxiliaire de recherche, OREV, Université Laval (nov. 2025 – en cours)
  * Revue de littérature par *snowballing*.
* **Mouvement Entreprises Vertes Québec** — Auxiliaire de recherche, Institut EDS, Université Laval (juin 2025 – nov. 2025)
  * Revue de littérature systématique à l'aide de Covidence.

## Expérience d'enseignement
{% for post in site.teaching reversed %}{% if post.lang == 'fr' %}
* **{{ post.title }}** — Auxiliaire d'enseignement, {{ post.venue }} ({{ post.date_display }}){% endif %}{% endfor %}

## Publications et documents de travail
{% for post in site.publications reversed %}{% if post.lang == 'fr' %}
* {{ post.citation }}{% endif %}{% endfor %}

## Communications
{% for post in site.talks reversed %}{% if post.lang == 'fr' %}
* «&nbsp;{{ post.title }}&nbsp;» — {{ post.talk_type }}, {{ post.venue }}, {{ post.date_display }}. (Animateur.){% endif %}{% endfor %}

## Bourses, prix et distinctions
* **Bourse d'études supérieures du Canada au niveau de la maîtrise (BESC M)**, 27 000 $ — Conseil de recherches en sciences humaines du Canada (CRSH), 2026-2027
* **Tableau d'honneur de la Faculté des sciences sociales** — Université Laval, décerné par Aurélie Campana, doyenne, 2025-2026
* **Mention d'honneur de la Doyenne de la Faculté des sciences sociales** — Université Laval, décernée par Aurélie Campana, doyenne, 2024-2025
* **Bourse de mobilité**, 4 500 $ — Université Laval, hiver 2025
* **Honor List** — CEGEP Champlain St. Lawrence, hiver 2023

## Affiliations de recherche
* **CAPP** — Centre d'analyse des politiques publiques
* **CLESSN** — Chaire de leadership en enseignement des sciences sociales numériques
* **CÉCD** — Centre pour l'étude de la citoyenneté démocratique
* **OREV** — Observatoire de recherche en économie verte
* **CIRGoM** — Centre interdisciplinaire de recherche sur la gouvernance mondiale
* **Institut EDS** — Institut en environnement, développement et société

## Langues
* **Français** — langue maternelle
* **Anglais** — courant (scolarité collégiale en anglais, CEGEP Champlain St. Lawrence)

## Compétences techniques
* **Calcul statistique :** R (nettoyage de données, web scraping, analyse textuelle automatisée)
* **Outils :** Git / GitHub, LaTeX, Quarto / R Markdown, Zotero, Covidence

## Engagement
* Délégué, 15<sup>e</sup> édition des Jeux de la science politique (JDSP), épreuve Cas académique, Université Laval (2025-2026)
* Représentant, Prix littéraire des collégien.ne.s, CEGEP Champlain St. Lawrence (2023)
* Président, pavillons Félix-Leclerc (2017-2018) et Jacques-Rousseau (2018-2019), École secondaire De Rochebelle

## Formation complémentaire
* **Analyse causale et expérimentation** (A+) — École interdisciplinaire outils et méthodes (EIOM), Université Laval, août-sept. 2025

## Références
* **Alexandre Gajevic Sayegh**, professeur agrégé, Département de science politique, Université Laval — [alexandre.gajevic@pol.ulaval.ca](mailto:alexandre.gajevic@pol.ulaval.ca)
* **Yannick Dufresne**, professeur titulaire, Département de science politique, Université Laval — [yannick.dufresne@pol.ulaval.ca](mailto:yannick.dufresne@pol.ulaval.ca)
