#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import datetime
from pathlib import Path

# -- Project information -----------------------------------------------------
this_year = datetime.datetime.today().year
if this_year == 2022:
    copyright_year = 2022
else:
    copyright_year = f"2022 - {this_year}"
project = "idemenv"
copyright = f"{copyright_year}, nicholasmhughes"
author = "nicholasmhughes"

# Strip version info from ../../idemenv/version.py
with open(Path(Path(__file__).parent.parent, "idemenv", "version.py")) as version_file:
    content = version_file.readlines()
    for file_line in content:
        if "version =" in file_line:
            version = file_line.split(" ")[2].replace('"', "")
            break

# Variables to pass into the docs from sitevars.rst for rst substitution
with open("sitevars.rst") as site_vars_file:
    site_vars = site_vars_file.read().splitlines()

rst_prolog = """
{}
""".format(
    "\n".join(site_vars[:])
)

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = "3.5.3"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    # "sphinxcontrib.spelling",
]
# Render TODO directives, set to FALSE before publishing
# This is incredibly helpful, when set to True, to know what is yet to be
# completed in documentation.
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".vscode",
    ".venv",
    ".git",
    ".gitlab-ci",
    ".gitignore",
    "sitevars.rst",
]

autosummary_generate = True

# ----- Napolean Config ------------------------------------------------------
# For using Google-style docstrings in Python code as a standard, which is
# highly recommended. This improves tooling by expecting a standard way of
# using docstrings in your project.
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# ----- Intersphinx Config ---------------------------------------------------
# This extension can generate automatic links to the documentation of objects
# in other projects, such as the official Python or POP docs.
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pytest": ("https://pytest.readthedocs.io/en/stable", None),
    "pop": ("https://pop.readthedocs.io/en/latest/", None),
}

# ----- Autodoc Config -------------------------------------------------------
# This extension can import the modules you are documenting, and pull in
# documentation from docstrings in a semi-automatic way. This is powerful!
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_default_options = {"member-order": "bysource"}

# ----- Autosummary Config ---------------------------------------------------
# This extension generates function/method/attribute summary lists, similar to
# those output e.g. by Epydoc and other API doc generation tools. This is
# especially useful when your docstrings are long and detailed, and putting
# each one of them on a separate page makes them easier to read.
# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
autosummary_generate = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"
html_title = f"{project} Documentation"
html_show_sourcelink = True  # False on private repos; True on public repos

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# For example, official Salt Project docs use images from the salt-branding-guide
# https://gitlab.com/saltstack/open/salt-branding-guide/
#
# Example for >=4.0.0 of Sphinx (support for favicon via URL)
# html_logo = "https://gitlab.com/saltstack/open/salt-branding-guide/-/raw/master/logos/SaltProject_altlogo_teal.png?inline=true"
# Example for <4.0.0 of Sphinx, if added into _static/img/ and html_static_path is valid
# html_logo = "_static/img/SaltProject_altlogo_teal.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large. Favicons can be up to at least 228x228. PNG
# format is supported as well, not just .ico'
# For example, official Salt Project docs use images from the salt-branding-guide
# https://gitlab.com/saltstack/open/salt-branding-guide/
#
# Example for >=4.0.0 of Sphinx (support for favicon via URL)
# html_favicon = "https://gitlab.com/saltstack/open/salt-branding-guide/-/raw/master/logos/SaltProject_Logomark_teal.png?inline=true"
# Example for <4.0.0 of Sphinx, if added into _static/img/ and html_static_path is valid
# html_favicon = "_static/img/SaltProject_Logomark_teal.png"

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "idemenvdoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "idemenv.tex",
        "idemenv Documentation",
        "nicholasmhughes",
        "manual",
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        "idemenv",
        "idemenv Documentation",
        [author],
        1,
    )
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "idemenv",
        "idemenv Documentation",
        author,
        "idemenv",
        "One line description of project.",
        "Miscellaneous",
    ),
]


# -- Extension configuration -------------------------------------------------
