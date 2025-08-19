# sphinxcontrib-jupyter
A Sphinx extension for converting reStructuredText (RST) documents into executable Jupyter notebooks. This extension provides two main builders: `jupyter` (for notebooks) and `jupyterpdf` (for PDF generation via notebooks).

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Install Dependencies
- Install Python dependencies: `pip install sphinx nbconvert nbformat dask distributed nbdime jupyter_client sphinxcontrib-bibtex sphinx-rtd-theme`
- Install the extension in development mode: `pip install -e .`
- **NOTE**: Installation takes about 30-60 seconds depending on network speed

### Build and Test Commands
- Build Jupyter notebooks: `make jupyter` -- takes 5 seconds. NEVER CANCEL. Set timeout to 60+ seconds.
- Run full test suite: `make test` -- takes 5 seconds. NEVER CANCEL. Set timeout to 60+ seconds.
- Run no-inline exercises test: `make no-inline-test` -- takes 4 seconds. NEVER CANCEL. Set timeout to 60+ seconds.
- Build documentation: `cd docs && make html` -- takes 1 second. NEVER CANCEL. Set timeout to 60+ seconds.
- Build PDF (requires LaTeX): `make pdf` -- takes 2 seconds but fails without xelatex. NEVER CANCEL. Set timeout to 60+ seconds.

### Working Directory Structure
All build commands should be run from the `tests/` directory unless otherwise specified:
- `cd /home/runner/work/sphinxcontrib-jupyter/sphinxcontrib-jupyter/tests`

## Validation

### Always Test Your Changes
- Run `make jupyter` to build notebooks and verify no errors
- Run `make test` to validate against expected outputs (some cell ID diffs are expected)
- ALWAYS manually inspect generated notebooks in `tests/base/_build/jupyter/` after making changes
- Test files are in JSON format - validate they parse correctly with: `python -m json.tool filename.ipynb`
- Check that notebooks contain expected markdown and code cells

### Manual Validation Scenarios
After making changes, ALWAYS execute this validation sequence:
1. `cd tests && make clean && make jupyter`
2. Verify notebooks generated in `base/_build/jupyter/`
3. Open and inspect `simple_notebook.ipynb` to ensure proper cell structure
4. Run `python -c "import json; print('Valid JSON' if json.load(open('base/_build/jupyter/simple_notebook.ipynb')) else 'Invalid')"` to validate JSON format
5. Check that code blocks are properly converted to code cells and text to markdown cells

### Build Validation Requirements
- Core functionality works WITHOUT LaTeX - do not attempt to install texlive unless specifically needed
- Test failures due to cell ID differences or nbformat_minor version differences are EXPECTED and acceptable
- Language configuration warnings are EXPECTED and can be ignored
- Missing `_static` directory warnings are EXPECTED in some test configs

## Common Tasks

### Debugging Build Issues
- Missing dependencies: Install with `pip install [package_name]`
- Missing themes: `pip install sphinx-rtd-theme` for documentation builds
- Missing bibtex: `pip install sphinxcontrib-bibtex` for PDF tests
- Permission errors: Use `pip install --user` or `pip install -e .` for development

### Configuration Files
- Main config: `tests/base/conf.py` - contains sphinxcontrib.jupyter settings
- PDF config: `tests/pdf/conf.py` - includes bibtex and PDF-specific settings  
- Documentation config: `docs/conf.py` - standard Sphinx configuration

### Key Project Files
Always check these files when investigating issues:
- `setup.py` - package dependencies and metadata
- `sphinxcontrib/jupyter/builders/jupyter.py` - main builder implementation
- `tests/Makefile` - build targets and commands
- `tests/base/index.rst` - test document structure
- `tests/check_diffs.py` - test validation script

### Repository Structure
```
├── .github/                 # GitHub configuration
├── docs/                    # Documentation source
├── sphinxcontrib/          # Main package code
│   └── jupyter/            # Extension implementation
│       ├── builders/       # Sphinx builders
│       ├── directive/      # Custom directives  
│       ├── transform/      # Document transformations
│       └── writers/        # Output writers
├── tests/                  # Test cases and builds
│   ├── base/              # Main test documents
│   ├── pdf/               # PDF-specific tests
│   ├── no_inline_exercises/ # Alternative test configs
│   └── Makefile           # Build commands
├── setup.py               # Package configuration
└── README.rst             # Project documentation
```

## Critical Timing Information
- **NEVER CANCEL builds**: All builds complete within 5 seconds under normal conditions
- Set timeouts to minimum 60 seconds for any build command to account for system variance
- Test suite may show "FAIL" messages for expected differences - this is normal behavior
- PDF builds will fail at LaTeX step without xelatex but successfully generate notebooks

## Expected Build Outputs
- Jupyter builder creates `.ipynb` files in `tests/base/_build/jupyter/`
- Each RST file becomes a corresponding notebook with proper cell structure
- Markdown content becomes markdown cells, code-block directives become code cells
- Dependencies (like images) are copied to the build directory

## Environment Notes
- Works with Python 3.7+ and modern Sphinx versions
- No special system dependencies required for core functionality
- LaTeX is optional and only needed for actual PDF generation
- All core development can be done without LaTeX installation

## Troubleshooting
- If `make test` shows many failures, check if they are only cell ID or format version differences
- Missing static files warnings are expected in test configurations
- Language configuration warnings are cosmetic and can be ignored
- Build errors related to missing xelatex are expected unless LaTeX is installed