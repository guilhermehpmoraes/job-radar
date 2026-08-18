"""Mantém os testes isolados das configurações pessoais do arquivo .env."""

import os


os.environ["PYTHON_DOTENV_DISABLED"] = "1"
