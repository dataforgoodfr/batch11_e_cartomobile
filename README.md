# Data For Good - Batch 11 - E-cartomobile

This project aims at encouraging and planning electric mobility in French territories by developing a Streamlit dashboard leveraging Open-Data for decision makers.

## Index
- [I want to contribute! Where do I start?](#contrib)
- [Development](#wrench-development)
  - [File Structure](#file_folder-file-structure)
  - [Setting up the environment](#nut_and_bolt-setting-up-the-environment)


##  :wrench: Development

### :file_folder: Repo structure

```
-.github/workflows --------------------- ochestrate GH actions jobs
- e_cartomobile ------------------------ all methods needed to serve the dashboard
        content ------------------------ documentation
        data_analytics ----------------- methods and figures for final dashboard
        data_extracts ------------------ raw data extracts
        data_transform ----------------- methods related to process raw and aggregated data
        utils --------------------------
        tests -------------------------- unit tests
- notebooks ---------------------------- R&D notebooks
- pages -------------------------------- the different pages making the dashboard
app.py --------------------------------- run dashboard
```


### :nut_and_bolt: Setting up the environment
Doing the following step will enable your local environement to be aligned with the one of any other collaborator.

First install pyenv:

<table>
<tr>
<td> OS </td> <td> Command </td>
</tr>

<tr>
<td> MacOS </td>
<td>

```bash
cd -
brew install pyenv # pyenv itself
brew install pyenv-virtualenv # integration with Python virtualenvsec
```
</td>
</tr>

<tr>
<td> Ubuntu </td>
<td>

```bash
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

curl https://pyenv.run | bash
```
</td>
</tr>

<tr>
<td> Windows </td>
<td>
An installation using miniconda is generally simpler than a pyenv one on Windows.
</td>
</tr>
</table>

Make the shell pyenv aware:

<table>
<tr>
<td> OS </td> <td> Command </td>
</tr>

<tr>
<td> MacOS </td>
<td>

```bash
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

</td>
</tr>

<tr>
<td> Ubuntu </td>
<td>

```bash
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
</td>
</tr>

<tr>
<td> Windows </td>
<td>

:fr: Dans Propriétés systèmes > Paramètres système avancés >  Variables d'environnement...
Choisissez la variable "Path" > Modifier... et ajoutez le chemin de votre installation python, où se trouve le python.exe. (par défaut, C:\Users\username\AppData\Roaming\Python\Scripts\ )

:uk: In System Properties > Advanced >  Environment Variables...
Choose the variable "Path" > Edit... et add the path to your python's installation, where is located the pyhton.exe (by default, this should be at C:\Users\username\AppData\Roaming\Python\Scripts\ )

In the console, you can now try :
```bash
poetry --version
```

</td>
</tr>
</table>


Let's install a python version (for windows, this step has been done with miniconda):
```bash
pyenv install 3.9.16 # this will take time
```

**Supported python versions for this project:** ">=3.8.1,<3.9.7 || >3.9.7,<3.10"

Check if it works properly, this command:
```bash
pyenv versions
```
should return:
```bash
  system
  3.9.16
```


Then you are ready to create a virtual environment. Go in the project folder, and run:
```bash
  pyenv virtualenv 3.9.16 batch11_e_cartomobile
  pyenv local batch11_e_cartomobile
```
A nice tutorial to know more about pyenv: [pyenv tuto](https://realpython.com/intro-to-pyenv/).

You now need a tool to manage dependencies. Let's use poetry: [Poetry documentation](https://python-poetry.org/docs/)
On windows, if not already installed, you will need a VS installation.

Link : https://wiki.python.org/moin/WindowsCompilers#Microsoft_Visual_C.2B-.2B-_14.x_with_Visual_Studio_2022_.28x86.2C_x64.2C_ARM.2C_ARM64.29

```bash
pip install poetry
poetry update
```
The virtual environment will be installed in .venv folder.

When you need to install a new dependency that is not in the pyproject.toml (use a new package, e.g. nltk), run 
```bash
poetry add ntlk
```

After commiting to the repo, other team members will be able to use the exact same environment you are using. Please be sure that you do not break the CI or other important stuff when merging your PR to the main branch.

**All Pull requests should be validated by 1 member before being merged.** See below for more details on pull requests review.

**Disclaimer: The virtual environment and CI are not perfect and need collaboration to be stable.** Please comment any surprising things you see. Also, your PR may be bloked due to Black, Flake8 or isort. Pre-commit hooks are here to help and apply some fixes to your code when you commit stuff to follow PEP8 standards. But you may have other surprises with a CI failing. Please take the time to analyze errors in "Actions" on Github and try to fix them. Try not to ignore too many errors. We will tweak flake8 and other libs parameters iteratively to have the best experience.

### A few details about pre-commit

The pre-commit library is installed in the virtual environment. It runs isort on your files (check if your imports are well sorted), then black (formatter following PEP8 standards) and eventually runs flake8 to check if everything is good. This suite runs automatically when you do a git commit. You can also run this pipeline with the following command:

```
pre-commit run --all-files
```

If you want more details, here is a small tutorial on pre-commit : [tuto](https://rohitgupta.xyz/blog/keeping-python-code-clean-with-pre-commit-hooks-black-flake8-and-isort/)

### Run the dashboard

Run:
```
make run_streamlit
```

Or full commands:
```bash
poetry run streamlit run app.py
```
On Windows, you may need instead of above solutions:
```bash
poetry run python -m streamlit run app.py
```
Depending on your installation process and version, "python" can also be "python3" or "py".

### Fix linting & unit tests

Before committing, make sure that the line of codes you wrote are conform to PEP8 standard by running:
```bash
poetry run black e_cartomobile --check
poetry run flake8 e_cartomobile
poetry run isort e_cartomobile
```

You can also test your code using pytest:
```bash
poetry run pytest e_cartomobile/tests
```

Please try to develop unit tests for your code. See [this tuto](https://realpython.com/pytest-python-testing/).

### Use the virtual environment in VS Code notebooks or Jupyter notebooks

**TO BE VALIDATED, like all README.** Please edit/comment if anything is wrong.

You can select the virtual environment created in VSCode to run the notebooks (in python evironments, .venv should be available). If you prefer to run your notebooks with Jupyter in the browser:
```
poetry run jupyter notebook
```
Then, open your notebook, you should be inside your virtual environment. If something is weird, trop running ```poetry install``` and relaunch ```poetry run jupyter notebook```.


### Code Review Guidelines

1. Look for anti-patterns that the linter and CI/CD do not already pick up on, for example too many magic strings or typos in column names that are only evaluated at runtime.

2. Be detail oriented. Consider off-by-one indexing errors, spelling mistakes in docstrings, and other easy-to-miss errors.

3. Evaluate if the unit tests cover most major corner cases.

4. Consider readability. If a section of code is difficult to understand ask for it to be refactored or better commented.

## Data used

**TODO:** Details on data set used after convergence
