# -*- coding: utf-8 -*-
"""A Pelican plugin to use Pandoc software.

Pandoc is a powerful tool to transform text from different formats (e.g. ReST,
Markdown) to others. It is really helpful to generate PDF or EPUB.

This plugin provides a powerful interface to handle document generation through
Pandoc.

Here is the list of configuration variables.

PANDOC_OUTPUTS          a dict where the keys are the output formats and the
                        values are the destination directories. Note if
                        to_format is set at "pdf", the "to"-argument is set at
                        latex" for Pandoc which does not support "-t pdf"
                        argument.
PANDOC_EXPORT_ARTICLES  True (default) if you want to export articles, False
                        else.
PANDOC_EXPORT_PAGES     True (default) if you want to export pages, False else.

Important note: this plugin requires Pandoc and pypandoc to be installed on
your system to work!

"""

from __future__ import unicode_literals

import os
import logging

from pelican import signals
from pelican.generators import Generator

# TODO: it could be great to not depend on an external module for such a basic
# work.
import pypandoc


logger = logging.getLogger(__name__)


class PandocGenerator(Generator):
    """The Pandoc generator.

    It takes the list of articles / pages and generates files according to
    PANDOC_OUTPUTS configuration variable.

    """

    def guess_format(self, content):
        """Return the format used by a given content.

        Since Pelican only supports reStructuredText and MarkDown files, this
        method returns just "md" or "rst".

        It is based on the file extension.

        TODO: it could be great if Pelican could support this method itself.

        :param content: the content (article or page)
        :type content: pelican.contents.Content
        :return: the article type (rst or md)
        :rtype: str
        :raises: KeyError if the file extension is not supported

        """
        formats = {
            '.rst': 'rst',
            '.md': 'md',
            '.markdown': 'md',
            '.mkd': 'md',
            '.mdown': 'md',
        }

        file_name, file_extension = os.path.splitext(content.source_path)

        return formats[file_extension]

    def generate_files(self, content):
        """Generates the list of files for a given content.

        :param content: the content to generate.
        :type content: pelican.contents.Content

        """
        try:
            from_format = self.guess_format(content)
        except KeyError:
            # The content format is not supported.
            return

        list_outputs = self.settings.get('PANDOC_OUTPUTS', {})
        for to_format, output_dir in list_outputs.items():
            output_dir = os.path.join(self.output_path, output_dir)

            # Create the output directory if it does not exist yet.
            # TODO: this big-block is quite ugly, please move it elsewhere.
            if not os.path.isdir(output_dir):
                try:
                    os.mkdir(output_dir)
                except OSError:
                    logger.error(
                        "Couldn't create the {format} output folder in {dir}".format(
                            format=to_format,
                            dir=output_dir
                        )
                    )

            filename = "{id_file}.{extension}".format(
                id_file=content.slug,
                extension=to_format
            )
            filepath = os.path.join(output_dir, filename)

            if to_format == 'pdf':
                # Pandoc don't take "pdf" as an output value.
                # Use latex instead.
                to_format = 'latex'

            if from_format == 'md':
                # Use the same format as Pelican (paticularly for metadata!)
                from_format = 'markdown_mmd'

            # Here is the magic!
            # TODO: support extra_args extending (it could be useful to use
            # specific Pandoc template).
            pypandoc.convert(
                source=content.source_path,
                to=to_format,
                format=from_format,
                extra_args=(
                    '--smart',
                    '--standalone',
                    '-o', filepath,
                )
            )

            logger.info("[ok] writing {filepath}".format(
                filepath=filepath
            ))

    def generate_output(self, writer=None):
        """Generate files for each articles and pages.

        If PANDOC_EXPORT_ARTICLES is False, articles are not generated.
        If PANDOC_EXPORT_PAGES is False, pages are not generated.

        We don't use the writer passed as argument since we write our own
        files ((c) PDF plugin :)).

        """
        contents_to_export = []
        if self.settings.get('PANDOC_EXPORT_ARTICLES', True):
            contents_to_export += self.context['articles']

        if self.settings.get('PANDOC_EXPORT_PAGES', True):
            contents_to_export += self.context['pages']

        for content_to_export in contents_to_export:
            self.generate_files(content_to_export)


def get_generators(generators):
    return PandocGenerator


def register():
    """Register our Pandoc class to the Pelican generators."""
    signals.get_generators.connect(get_generators)
