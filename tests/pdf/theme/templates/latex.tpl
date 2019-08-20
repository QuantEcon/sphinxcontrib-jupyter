((*- extends 'article.tplx' -*))

% See http://blog.juliusschulz.de/blog/ultimate-ipython-notebook#templates
% for some useful tips

%===============================================================================
% Document class
%===============================================================================

((* block docclass *))
\documentclass[11pt, twoside, a4paper]{article}
((* endblock docclass *))

%===============================================================================
% Packages
%===============================================================================

((* block packages *))
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage[breakable]{tcolorbox}
% We will generate all images so they have a width \maxwidth. This means
% that they will get their normal width if they fit onto the page, but
% are scaled down if they would overflow the margins.
\makeatletter
\def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth
\else\Gin@nat@width\fi}
\makeatother
\let\Oldincludegraphics\includegraphics
% Set max figure width to be 80% of text width, for now hardcoded.
\renewcommand{\includegraphics}[1]{\Oldincludegraphics[width=.8\maxwidth]{#1}}
% Ensure that by default, figures have no caption (until we provide a
% proper Figure object with a Caption API and a way to capture that
% in the conversion process - todo).
\usepackage{caption}
\DeclareCaptionLabelFormat{nolabel}{}
\captionsetup{labelformat=nolabel}

\usepackage{adjustbox} % Used to constrain images to a maximum size
\usepackage{xcolor} % Allow colors to be defined
\usepackage{enumerate} % Needed for markdown enumerations to work
\usepackage{geometry} % Used to adjust the document margins
\usepackage{amsmath} % Equations
\usepackage{amssymb} % Equations
\usepackage{textcomp} % defines textquotesingle
% Hack from http://tex.stackexchange.com/a/47451/13684:
\AtBeginDocument{%
    \def\PYZsq{\textquotesingle}% Upright quotes in Pygmentized code
}
\usepackage{upquote} % Upright quotes for verbatim code
\usepackage{eurosym} % defines \euro
\usepackage[mathletters]{ucs} % Extended unicode (utf-8) support
\usepackage[utf8x]{inputenc} % Allow utf-8 characters in the tex document
\usepackage{fancyvrb} % verbatim replacement that allows latex
\usepackage{grffile} % extends the file name processing of package graphics
                     % to support a larger range
% The hyperref package gives us a pdf with properly built
% internal navigation ('pdf bookmarks' for the table of contents,
% internal cross-reference links, web links for URLs, etc.)
\usepackage{hyperref}
\usepackage{booktabs}  % table support for pandoc > 1.12.2
\usepackage[inline]{enumitem} % IRkernel/repr support (it uses the enumerate* environment)
\usepackage[normalem]{ulem} % ulem is needed to support strikethroughs (\sout)
                            % normalem makes italics be italics, not underlines
\usepackage{braket}
((* endblock packages *))

%===============================================================================
% Title Page
%===============================================================================

((* block title -*))
((*- endblock title *))
((* block author -*))
((* endblock author *))

((* block maketitle *))

((*- if nb.metadata.get("latex_metadata", {}).get("title", ""): -*))
\title{((( nb.metadata["latex_metadata"]["title"] )))}
((*- else -*))
\title{((( resources.metadata.name | ascii_only | escape_latex )))}
((*- endif *))

((*- if nb.metadata.get("latex_metadata", {}).get("author", ""): -*))
\author{((( nb.metadata["latex_metadata"]["author"] )))}
((*- else -*))
\author{Michael Goerz}
((*- endif *))

((*- if nb.metadata.get("latex_metadata", {}).get("affiliation", ""): -*))
\affiliation{((( nb.metadata["latex_metadata"]["affiliation"] )))}
((*- endif *))

\date{\today}
\maketitle

((* endblock maketitle *))


%===============================================================================
% Input
%===============================================================================

% Input cells can be hidden using the "Hide input" and "Hide input all"
% nbextensions (which set the hide_input metadata flags)

((* block input scoped *))
((*- if cell.metadata.hide_input or nb.metadata.hide_input: -*))
((*- else -*))
   ((( custom_add_prompt(cell.source | wrap_text(88) | highlight_code(strip_verbatim=True), cell, 'In ', 'incolor') )))
((*- endif *))
((* endblock input *))


%===============================================================================
% Output
%===============================================================================

((* block output_group -*))
((*- if cell.metadata.hide_output: -*))
((*- else -*))
    ((( super() )))
((*- endif -*))
((* endblock output_group *))

% Display stream ouput with coloring
((* block stream *))
    \begin{Verbatim}[commandchars=\\\{\}]
((( output.text | wrap_text(86) | escape_latex | ansi2latex )))
    \end{Verbatim}
((* endblock stream *))

%==============================================================================
% Define macro custom_add_prompt() (derived from add_prompt() macro in style_ipython.tplx)
%==============================================================================

((* macro custom_add_prompt(text, cell, prompt, prompt_color) -*))
    ((*- if cell.execution_count is defined -*))
    ((*- set execution_count = "" ~ (cell.execution_count | replace(None, " ")) -*))
    ((*- else -*))
    ((*- set execution_count = " " -*))
    ((*- endif -*))
    ((*- set indention =  " " * (execution_count | length + 7) -*))
\begin{Verbatim}[commandchars=\\\{\}]
((( text | add_prompts(first='{\color{' ~ prompt_color ~ '}' ~ prompt ~ '[{\\color{' ~ prompt_color ~ '}' ~ execution_count ~ '}]:} ', cont=indention) )))
\end{Verbatim}
((*- endmacro *))

%==============================================================================
% Bibliography
%==============================================================================

% Insert citations in markdown as e.g.
%    <cite data-cite="DevoretS2013">[DevoretS2013]</cite>
% requires file references.bib in current directory (or the file set as "bib" in the latex_metadata)

((* block bibliography *))
\bibliography{((( nb.metadata.get("latex_metadata", {}).get("bib", "references") )))}
((* endblock bibliography *))