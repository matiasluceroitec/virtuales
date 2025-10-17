import os
import sys
from pathlib import Path

def setup_django() -> None:
    """
    Inicializa Django para poder el ORM desde Typer, fuera del manage.py

    - Cuando 'itec' no vamos a estar dentro de Django pero vamos cosas de el
    - Para poder usar los modelos
    """

    ## Vamos a buscar la raiz del proyecto
    repo_root = Path(__file__).resolve().parents[2]
    django_project_dir = repo_root / "itec2025"

    if str(django_project_dir) not in sys.path:
        sys.path.insert(0, str(django_project_dir))

    ## Apuntamos explicitamente al settings de Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itec2025.settings")
    
    import django

    django.setup()