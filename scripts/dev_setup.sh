#!/bin/zsh

# exit if any command fails
set -e

echo "Initializing development environment"

function prompt_confirmation {
  message="$1"
  while true; do
    echo "${message} \nEnter Y to continue or N to exit. "
    read yn
    case "$yn" in
      [Yy]* ) break;;
      [Nn]* ) echo "Exiting"; exit 1;;
      * ) echo "Please answer yes or no.";;
    esac
  done
}

# install pyenv if necessary
if ! pyenv --version > /dev/null 2>&1; then
  prompt_confirmation "pyenv not found. pyenv will now be installed using Homebrew."
  echo "Installing pyenv..."
  brew install pyenv
else
  echo "$(pyenv --version) found"
fi

# init pyenv in shell
export PYENV_ROOT="${PYENV_ROOT:-$HOME/.pyenv}"
eval "$(pyenv init -)"

# install required python version
echo "Installing python version: $(pyenv version)"
pyenv install --skip-existing

# Install poetry if required
if ! poetry --version > /dev/null 2>&1; then
  prompt_confirmation "poetry not found. poetry will now be installed."
  curl -sSL# https://install.python-poetry.org | python - --version 1.4.2
  echo "Installed poetry version: $(poetry --version)"
  echo "Edit your ~/.zshrc to permanently add $HOME/.local/bin to your PATH"
  export PATH="$HOME/.local/bin:$PATH"
else
  echo "Poetry version found: $(poetry --version)"
fi

# make sure to use the python version set by pyenv
# this is more explicit than expecting virtualenvs.prefer-active-python=true to be set
poetry env use "$(pyenv prefix)/bin/python"

# Create virtualenv and install dependencies
echo "Installing with poetry..."
poetry install
