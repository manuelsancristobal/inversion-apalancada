"""Deploy de assets al repositorio Jekyll."""

from __future__ import annotations

import logging
import shutil

from inversion_apalancada.config import (
    CHARTS_DIR,
    DATA_JSON_DIR,
    JEKYLL_CHARTS_DIR,
    JEKYLL_CSS_DIR,
    JEKYLL_DATA_DIR,
    JEKYLL_JS_DIR,
    JEKYLL_PAGE,
    JEKYLL_PROJECT_MD,
    JEKYLL_PROJECTS_DIR,
    JEKYLL_REPO,
    VIZ_DIR,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def deploy() -> None:
    """Copia assets y markdown al repositorio Jekyll."""
    if JEKYLL_REPO is None:
        logger.error("Variable de entorno 'JEKYLL_REPO' no definida.")
        return

    logger.info(f"Usando repo Jekyll en: {JEKYLL_REPO}")

    # Copiar JSON de datos
    if DATA_JSON_DIR.exists():
        JEKYLL_DATA_DIR.mkdir(parents=True, exist_ok=True)
        count = 0
        for f in DATA_JSON_DIR.glob("*.json"):
            shutil.copy2(f, JEKYLL_DATA_DIR / f.name)
            count += 1
        logger.info(f"Copiados {count} archivos de datos → {JEKYLL_DATA_DIR}")

    # Copiar PNGs
    if CHARTS_DIR.exists():
        JEKYLL_CHARTS_DIR.mkdir(parents=True, exist_ok=True)
        count = 0
        for f in CHARTS_DIR.glob("*.png"):
            shutil.copy2(f, JEKYLL_CHARTS_DIR / f.name)
            count += 1
        logger.info(f"Copiados {count} gráficos → {JEKYLL_CHARTS_DIR}")

    # Copiar CSS
    css_src = VIZ_DIR / "assets" / "css" / "inversion.css"
    if css_src.exists():
        JEKYLL_CSS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(css_src, JEKYLL_CSS_DIR / css_src.name)
        logger.info(f"Copiado CSS → {JEKYLL_CSS_DIR}")

    # Copiar JS
    js_src = VIZ_DIR / "assets" / "js" / "inversion-apalancada.js"
    if js_src.exists():
        JEKYLL_JS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(js_src, JEKYLL_JS_DIR / js_src.name)
        logger.info(f"Copiado JS → {JEKYLL_JS_DIR}")

    # Copiar HTML
    html_src = VIZ_DIR / "index.html"
    if html_src.exists():
        JEKYLL_PAGE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(html_src, JEKYLL_PAGE)
        logger.info(f"Copiado viz.html → {JEKYLL_PAGE}")

    # Copiar markdown del proyecto
    if JEKYLL_PROJECT_MD.exists():
        JEKYLL_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(JEKYLL_PROJECT_MD, JEKYLL_PROJECTS_DIR / JEKYLL_PROJECT_MD.name)
        logger.info(f"Copiado proyecto .md → {JEKYLL_PROJECTS_DIR}")

    logger.info("Deploy completado. Recuerda hacer git push en el repo Jekyll.")


if __name__ == "__main__":
    deploy()
