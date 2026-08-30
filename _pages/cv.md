---
layout: archive
title: "Curriculum Vitae"
permalink: /cv/
lang: en
alt_lang_url: /fr/cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

[Download my CV (PDF, in French)]({{ base_path }}/files/CV-Jules-Piral-FR.pdf)

Education
======
* **M.A. in Political Science**, Université Laval, Québec — Sept. 2026 – May 2028 (expected)
  * Supervisors: Alexandre Gajevic Sayegh and Yannick Dufresne
* **B.A. in Political Science**, Université Laval, Québec — Sept. 2023 – May 2026
  * GPA: 4.23/4.33 · *Profil distinction* · *Profil international*
  * Faculty of Social Sciences Honour Roll (2025–2026)
  * Dean's Honourable Mention, Faculty of Social Sciences (2024–2025)
* **Certificate in Political Studies**, Sciences Po Lyon, France — Jan. 2025 – May 2025
  * Grade: A (highest ECTS grade)

Research experience
======
* **Datagotchi Chatbot** — Research assistant, CLESSN, Université Laval (July 2026 – present)
  * Outreach and science communication for the tool.
* **Vitrine Démocratique** — Research assistant, CAPP, Université Laval (June 2026 – present)
  * Automated text analysis; development of data refiners.
* **IEADB** — Research assistant, CIRGoM, Université Laval (Jan. 2026 – Sept. 2026)
  * Documentary research, web scraping, and data cleaning in R.
* **Populism and climate change** — Research assistant, OREV, Université Laval (Nov. 2025 – present)
  * Snowball literature review.
* **Mouvement Entreprises Vertes Québec** — Research assistant, Institut EDS, Université Laval (June 2025 – Nov. 2025)
  * Systematic literature review using Covidence.

Teaching experience
======
{% for post in site.teaching reversed %}{% if post.lang == 'en' %}
* **{{ post.title }}** — Teaching assistant, {{ post.venue }} ({{ post.date_display }}){% endif %}{% endfor %}

Publications and working papers
======
{% for post in site.publications reversed %}{% if post.lang == 'en' %}
* {{ post.citation }}{% endif %}{% endfor %}

Talks and workshops
======
{% for post in site.talks reversed %}{% if post.lang == 'en' %}
* "{{ post.title }}" — {{ post.talk_type }}, {{ post.venue }}, {{ post.date_display }}. (Facilitator.){% endif %}{% endfor %}

Grants, fellowships and awards
======
* **Canada Graduate Scholarship – Master's (CGS M)**, $27,000 — Social Sciences and Humanities Research Council of Canada (SSHRC), 2026–2027
* **Faculty of Social Sciences Honour Roll** — Université Laval, awarded by Dean Aurélie Campana, 2025–2026
* **Dean's Honourable Mention, Faculty of Social Sciences** — Université Laval, awarded by Dean Aurélie Campana, 2024–2025
* **Mobility scholarship**, $4,500 — Université Laval, Winter 2025
* **Honor List** — CEGEP Champlain St. Lawrence, Winter 2023

Research affiliations
======
* **CAPP** — Centre d'analyse des politiques publiques
* **CLESSN** — Chaire de leadership en enseignement des sciences sociales numériques
* **CÉCD** — Centre pour l'étude de la citoyenneté démocratique
* **OREV** — Observatoire de recherche en économie verte
* **CIRGoM** — Centre interdisciplinaire de recherche sur la gouvernance mondiale
* **Institut EDS** — Institut en environnement, développement et société

Languages
======
* **French** — native
* **English** — fluent (college studies completed in English, CEGEP Champlain St. Lawrence)

Technical skills
======
* **Statistical computing:** R (data cleaning, web scraping, automated text analysis)
* **Tools:** Git / GitHub, LaTeX, Quarto / R Markdown, Zotero, Covidence

Service and involvement
======
* Delegate, 15th edition of the *Jeux de la science politique* (JDSP), academic case competition, Université Laval (2025–2026)
* Representative, *Prix littéraire des collégien.ne.s*, CEGEP Champlain St. Lawrence (2023)
* President, Félix-Leclerc (2017–2018) and Jacques-Rousseau (2018–2019) student bodies, École secondaire De Rochebelle

Additional training
======
* **Causal analysis and experimentation** (A+) — École interdisciplinaire outils et méthodes (EIOM), Université Laval, Aug.–Sept. 2025

References
======
* **Alexandre Gajevic Sayegh**, Associate Professor, Department of Political Science, Université Laval — [alexandre.gajevic@pol.ulaval.ca](mailto:alexandre.gajevic@pol.ulaval.ca)
* **Yannick Dufresne**, Full Professor, Department of Political Science, Université Laval — [yannick.dufresne@pol.ulaval.ca](mailto:yannick.dufresne@pol.ulaval.ca)
