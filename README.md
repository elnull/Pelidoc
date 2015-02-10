# Pandoc Generator (Pelidoc)

A Pelican plugin to use Pandoc software.

Pandoc is a powerful tool to transform text from different formats (e.g. ReST,
Markdown) to others. It is really helpful to generate PDF or EPUB. It also can easily replace the "official" PDF plugin.

This plugin provides a powerful interface to handle document generation through
Pandoc.

Markdown parsing is done in MultiMarkdown to be able to parse metadata information easily.

## Installation

You need to have [Pandoc](http://johnmacfarlane.net/pandoc/) (!) and [pypandoc](https://github.com/bebraw/pypandoc), a Python module wrapper for Pandoc, installed on your system. You can install pypandoc with `pip`:

```bash
$ pip install pypandoc
```

Then, put the plugin directory in your plugin directory. For instance, create a `./plugins` directory in your Pelican project and add these lines in your `pelicanconf.py` file:

```python
PLUGIN_PATHS = ['plugins']
PLUGINS = ['Pelidoc']
```

Obviously, you'll have to adapt instructions if you already have installed some plugins.

To use this plugin then, you'll need to set a `PANDOC_OUTPUTS` configuration variable. It is a dictionary where the keys are the output formats and the
values are the corresponding destination directories. For instance:

```python
PANDOC_OUTPUTS = {
    'pdf': 'pdfs',
    'epub': 'epubs',
}
```

Note you'll have to modify your theme template to support download of files. Here is a snippet to download files (PDF or EPUB) of a specific article. You can put it in the `templates/article_infos.html` file (or similar) of your theme:

```jinja
{% if 'pdf' in PANDOC_OUTPUTS or 'epub' in PANDOC_OUTPUTS %}
    <div class="entry-download">
        {% if 'pdf' in PANDOC_OUTPUTS %}
            <a href="{{ SITEURL }}/{{ PANDOC_OUTPUTS['pdf'] }}/{{ article.slug }}.pdf">Download as PDF</a><br />
        {% endif %}
        {% if 'epub' in PANDOC_OUTPUTS %}
            <a href="{{ SITEURL }}/{{ PANDOC_OUTPUTS['epub'] }}/{{ article.slug }}.epub">Download as EPUB</a>
        {% endif %}
    </div>
{% endif %}
```

## How-to contribute

- Fork the [project Git repository](https://github.com/marienfressinaud/Pelidoc) ;
- Please open a ticket [on the bug tracker](https://github.com/marienfressinaud/Pelidoc/issues) so we can discuss about your bug / feature ;
- Create a dedicated branch for your fix (`git checkout -b` is your friend) ;
- Commit your work, push your branch upstream (`git push --set-upstream origin your_branch_name`) and do a [pull request](https://github.com/marienfressinaud/Pelidoc/compare).

Note there's a bunch of TODOs in the source code that you may fix.

## Credits

- [Pelican](http://getpelican.com) by [Alexis Métaireau](http://blog.notmyidea.org/) ;
- [Pelican plugins](https://github.com/getpelican/pelican-plugins) for the code basis (especially PDF plugin!)
- [pypandoc](https://github.com/bebraw/pypandoc) by [Juho Vepsäläinen](http://www.nixtu.info/) ;
- [Pandoc Reader](https://github.com/liob/pandoc_reader), another Pandoc plugin for Pelican but a bit less powerful, by [Hinrich B. Winther](https://github.com/liob).
- And, obviously, [Pandoc](http://johnmacfarlane.net/pandoc/) by [John MacFarlane](http://johnmacfarlane.net).
