.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+

*******************************************************************************
                                Contemplations
*******************************************************************************

``Contemplations`` is Eric McDonald's engineering and science-oriented blog. It
is powered by `Nikola <https://getnikola.com/>`_ and published with GitHub
Pages at `emcd.github.io <https://emcd.github.io/>`_.

The repository also contains project infrastructure for local validation and,
eventually, small helper programs under the ``emcdblog`` Python package. The
blog itself remains the primary artifact.


Repository Layout
===============================================================================

``posts/``
  Blog posts. Historical posts are currently written in reStructuredText.

``pages/``
  Nikola pages which are not part of the dated weblog.

``listings/``
  Source listings included by posts and pages through Nikola directives or
  shortcodes.

``themes/mine/``
  Custom Nikola theme assets and templates.

``utilities/``
  Helper scripts and the custom Pygments lexer for the experimental language
  examples.

``sources/emcdblog/``
  Python helper package reserved for local automation around the blog.

``documentation/``
  Project-maintenance documentation built with Sphinx.


Local Environment
===============================================================================

Install `uv <https://github.com/astral-sh/uv/blob/main/README.md>`_ and
`Hatch <https://hatch.pypa.io/latest/>`_. Then use the managed development
environment:

::

    hatch --env develop run blog-build

Hatch will create the environment and install the Python dependencies declared
in ``pyproject.toml``, including Nikola and its template-engine dependencies.


Blog Commands
===============================================================================

Build the static site:

::

    hatch --env develop run blog-build

Check the generated site:

::

    hatch --env develop run blog-check

Preview the site locally with automatic rebuilds:

::

    hatch --env develop run blog-preview

Publish manually to GitHub Pages:

::

    hatch --env develop run blog-publish

Publishing uses Nikola's GitHub deployment support. The source branch is
``source`` and the generated GitHub Pages branch is ``master``.


Writing Workflow
===============================================================================

For new posts, prefer Markdown unless the content needs reStructuredText-only
features. The Nikola configuration already accepts both ``.rst`` and ``.md``
files for posts and pages.

Before publishing:

1. Build the blog with ``blog-build``.
2. Review the local preview with ``blog-preview``.
3. Run ``blog-check``.
4. Commit the source changes on ``source``.
5. Publish with ``blog-publish``.

Historical reStructuredText posts can remain as they are. If they are converted
to Markdown later, pay close attention to Nikola ``listing`` inclusions, line
ranges, list tables, and custom CSS classes such as ``pros`` and ``cons``.


Development Validation
===============================================================================

Run Python and documentation validation through Hatch:

::

    hatch --env develop run linters
    hatch --env develop run testers
    hatch --env develop run docsgen

The broad validation command is:

::

    hatch --env develop run make-all


Project Links
===============================================================================

* Site: `https://emcd.github.io/ <https://emcd.github.io/>`_
* Source: `emcd/emcd.github.io <https://github.com/emcd/emcd.github.io>`_
* Issues: `GitHub issues
  <https://github.com/emcd/emcd.github.io/issues>`_
