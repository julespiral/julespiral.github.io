#!/bin/sh
# Régénère les images des pages du CV affichées sur la page CV.
# À relancer chaque fois qu'un PDF de static/cv/ change.
set -e
cd "$(dirname "$0")/.."
rm -rf static/cv/pages && mkdir -p static/cv/pages
for pdf in static/cv/*.pdf; do
  name=$(basename "$pdf" .pdf)
  pdftoppm -png -scale-to-x 1400 -scale-to-y -1 "$pdf" "static/cv/pages/$name"
done
ls static/cv/pages
