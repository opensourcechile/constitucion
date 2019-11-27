# Constitución abierta

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

Es importante seguir nuestro [código de conducta](CODE_OF_CONDUCT.md)

## Cosas pendientes

Ver la sección de [Issues](https://github.com/opensourcechile/constitucion/issues)

## Extracción de información

El archivo ubicado en `scripts/repo_data_to_posts.py`:

 - Extrae info del repo, previamente clonado en `data/constitucion_chile`
 - Va commit por commit (ley por ley) extrayendo metadata
 - Compara con commit anterior y crea un diff (línea por línea)
 - Genera archivo markdown en formato apto para Jekyll

## Estructura del proyecto

- Carpetas `_includes/`, `_layouts/`: Son default de Jekyll, y contienen los templates html para las distintas secciones
- Carpeta `_posts/`: Contienen los archivos markdown con la metadata y los contenidos de cada ley. Lamentablemente no se le puede cambiar el nombre
- `_sass/`: Contienen los archivos scss que le dan estilo al sitio.
- `assets/`: Contiene archivos estáticos como css, imágenes, íconos, etc.
- `data/`: No está trackeada, pero el script busca ahí el repo de la constitución por defecto. Ver script para más detalles
- `scripts/`: Contiene scripts para extraer información y convertirla a los formatos apropiados
- `glosario.md`, `index.md`, `timeline.html`: Corresponden a las distintas secciones del sitio.

## Como correr localmente

1 - Instala (ruby)[https://www.ruby-lang.org/es/documentation/installation/]

2 - Instala Jekyll (Instrucciones (en inglés) para [Windows](https://jekyllrb.com/docs/installation/windows/), [Mac](https://jekyllrb.com/docs/installation/macos/))

3 - Clona este repositorio. [Más info aquí](https://help.github.com/es/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

4 - En la línea de comandos:

```bash
cd constitucion ## Muévete al directorio del repo
bundle install ## Instala las dependencias
```

5 - Finalmente, ejecuta `bundle exec jekyll serve`

6 - En el navegador (Chrome, por ejemplo) ve a la URL `http://localhost:4000/`

Ahora deberías ver los contenidos actuales del blog en tu navegador.
