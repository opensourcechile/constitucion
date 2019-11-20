# Historial de cambios de la Constitución

En este blog se documentan las leyes que han modificado la Constitución.
Está construido con [Jekyll](https://jekyllrb.com/), y extrae información sobre la Constitución desde [opensourcechile/constitucion_chile](https://github.com/opensourcechile/constitucion_chile)

Los usuarios pueden leer la Constitución de Chile, ver los detalles
de las distintas leyes que lo han modificado y compartir links directos
a las versiones de los artículos que les interesan.

## Cómo colaborar

Estamos centrando la discusión sobre este sitio en su [repositorio en Github](https://github.com/opensourcechile/constitucion).

1. ¿Tienes ideas sobre cosas que podemos mejorar del sitio? ¿Has encontrado
errores? Por favor crea un [nuevo Issue](https://github.com/opensourcechile/constitucion/issues/new) describiendo tu sugerencia
de forma lo más detallada posible. Idealmente incluye pantallazos,
dibujos, etc.

2. ¿Eres programador, o te gustaría serlo? Anímate y crea un Pull Request
con alguna mejora para el sitio. Puedes usar tus propias ideas, tomar ideas 
de la sección de Issues, o avanzar con alguna de las cosas en la lista de pendientes.

## Extracción de información

El archivo ubicado en `scripts/repo_data_to_posts.py`:

 - Extrae info del repo, previamente clonado en `data/constitucion_chile`
 - Va commit por commit (ley por ley) extrayendo metadata
 - Compara con commit anterior y crea un diff (línea por línea)
 - Genera archivo markdown en formato apot para Jekyll


## Cosas pendientes

Ver la sección de [Issues](https://github.com/opensourcechile/constitucion/issues)
