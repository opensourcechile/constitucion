# Historial de cambios de la Constitución

En este blog se documentan las leyes que han modificado la Constitución.
Está construido con [Jekyll](https://jekyllrb.com/), y extrae información sobre la Constitución desde [opensourcechile/constitucion_chile](https://github.com/opensourcechile/constitucion_chile)


## Extracción de información

El archivo ubicado en `scripts/repo_data_to_posts.py`:

 - Extrae info del repo, previamente clonado en `data/constitucion_chile`
 - Va commit por commit (ley por ley) extrayendo metadata
 - Compara con commit anterior y crea un diff (línea por línea)
 - Genera archivo markdown en formato apot para Jekyll


## TODO

 - Anchor links para cada artículo
 - Índice
 - Ordenar y documentar script
 - Estilizar diff
