"""
extension_script.py
====================

Extension-Script fuer den best-of-generator
(https://github.com/best-of-lists/best-of-generator), gedacht fuer
z. B. ein "awesome-obsidian"-Repository.

Der best-of-generator laedt die in der `configuration.extension_script`
konfigurierte Datei ueber `importlib`, BEVOR die Projekt-Daten
gesammelt und das Markdown generiert wird (siehe
`best_of.generator.load_extension_script`). Das Script wird dabei
einfach als Python-Modul ausgefuehrt -- es gibt keinen speziellen
Hook/Callback, den man implementieren muss. Stattdessen "patcht" man
die gewuenschten Funktionen des Generators direkt im Modul-Namespace
(daher auch der Changelog-Eintrag "extend the best-of generation
through patching").

Dieses Script patcht `best_of.generators.markdown_list.generate_project_body`
(Signatur: `generate_project_body(project, configuration, labels) -> str`),
also genau die Funktion, die den aufklappbaren "<details>"-Inhalt eines
Projekts erzeugt (dort, wo z. B. bei mkdocs/catalog der "Add to
mkdocs.yml"-Hinweis steht).

Neue, optionale Projekteigenschaften in der `projects.yaml`
-------------------------------------------------------------

image: <URL>
    Eine Vorschaugrafik/Screenshot der Website bzw. des Plugins,
    genau wie im MkDocs-Catalog-Beispiel. Wird oben im aufklappbaren
    Bereich rechts ausgerichtet eingebunden (<img ... align="right">),
    optional als Link umschlossen.

image_link: <URL>   (optional)
    Ziel-URL, wenn man auf das Bild klickt. Falls nicht gesetzt, wird
    automatisch `homepage`, sonst `docs_url`, sonst `github_url` des
    Projekts verwendet.

obsidian_plugin: <plugin-id>  ODER  [<plugin-id>, ...]
    Die Plugin-ID aus dem Obsidian Community-Plugin-Verzeichnis
    (identisch mit dem "id"-Feld in der manifest.json des Plugins
    bzw. in obsidianmd/obsidian-releases/community-plugins.json).
    Daraus werden automatisch erzeugt:
      - Link zur offiziellen Plugin-Seite:
            https://obsidian.md/plugins?id=<plugin-id>
      - Direkter obsidian://-Link, der das Plugin in einer laufenden
        Obsidian-Installation sofort oeffnet/zur Installation anbietet:
            obsidian://show-plugin?id=<plugin-id>

obsidian_theme: <Theme-Name>  ODER  [<Theme-Name>, ...]
    Der exakte Anzeigename des Themes, wie er im "name"-Feld von
    obsidianmd/obsidian-releases/community-css-themes.json steht
    (z. B. "Minimal", "AnuPpuccin", "Things"). Daraus werden erzeugt:
      - Link zur Community-Theme-Seite (best-effort Slug aus dem
        Namen, siehe Hinweis unten):
            https://community.obsidian.md/themes/<slug>
      - Direkter obsidian://-Link, der das Theme in einer laufenden
        Obsidian-Installation sofort installiert/aktiviert:
            obsidian://show-theme?name=<Theme-Name>
    Hinweis: Themes werden von Obsidian ueber ihren `name` (nicht
    ueber eine feste `id` wie bei Plugins) identifiziert. Der
    Seiten-Link wird deshalb per einfachem Slugify aus dem Namen
    erzeugt (kleingeschrieben, Leer-/Sonderzeichen zu Bindestrichen)
    und passt in den meisten Faellen (z. B. "Minimal" ->
    ".../themes/minimal"), muss aber nicht immer exakt mit der
    offiziellen URL uebereinstimmen. Falls noetig, kann die Seite
    ueber `obsidian_theme_page` (gleiche Reihenfolge wie
    `obsidian_theme`, falls das eine Liste ist) explizit gesetzt
    werden. Der obsidian://show-theme-Link ist davon unabhaengig und
    funktioniert zuverlaessig, da er direkt den `name` verwendet.

Beispiele in der projects.yaml
-------------------------------

    configuration:
      extension_script: "extension_script.py"

    projects:
      - name: "Dataview"
        github_id: "blacksmithgu/obsidian-dataview"
        obsidian_plugin: "dataview"
        image: "https://raw.githubusercontent.com/blacksmithgu/obsidian-dataview/master/images/preview.png"
        category: data

      - name: "Minimal"
        github_id: "kepano/obsidian-minimal"
        obsidian_theme: "Minimal"
        image: "https://raw.githubusercontent.com/kepano/obsidian-minimal/master/images/dark-simple.png"
        category: themes

      - name: "Buisson"
        github_id: "buisson-theme/buisson-obsidian"
        obsidian_theme: "Buisson"
        obsidian_theme_page: "https://community.obsidian.md/themes/buisson"
        category: themes
"""

import logging
import re
from urllib.parse import quote

log = logging.getLogger(__name__)


OBSIDIAN_PLUGIN_PAGE_URL = "https://obsidian.md/plugins?id={plugin_id}"
OBSIDIAN_PLUGIN_INSTALL_URI = "obsidian://show-plugin?id={plugin_id}"

OBSIDIAN_THEME_PAGE_URL = "https://community.obsidian.md/themes/{slug}"
OBSIDIAN_THEME_INSTALL_URI = "obsidian://show-theme?name={name}"


def _as_list(value):
    """Erlaubt sowohl einen einzelnen String als auch eine Liste von
    Strings fuer ein Feld (analog zu mkdocs_plugin/mkdocs_theme in
    anderen best-of-Listen)."""
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value if v]
    return [str(value)]


def _slugify(name: str) -> str:
    """Best-effort Slug fuer die community.obsidian.md-Theme-Seite."""
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def _generate_image_md(project) -> str:
    """Erzeugt den rechtsbuendigen Vorschaubild-Block, analog zum
    MkDocs-Material-Beispiel im MkDocs-Catalog."""
    image_url = project.get("image")
    if not image_url:
        return ""

    link_target = (
        project.get("image_link")
        or project.get("homepage")
        or project.get("docs_url")
        or project.get("github_url")
    )

    if link_target:
        return (
            f'<a href="{link_target}">\n'
            f'<img src="{image_url}" width="400" align="right">\n'
            f"</a>\n"
        )
    # Ohne bekanntes Link-Ziel wird das Bild ohne Verlinkung eingebunden
    return f'<img src="{image_url}" width="400" align="right">\n'


def _generate_obsidian_plugin_md(project) -> str:
    """Erzeugt eine Zeile mit Link zur Plugin-Seite und einem direkten
    obsidian://-Installationslink. Format und Icon (🔌) sind bewusst an
    den Stil des restlichen best-of-Outputs angelehnt (Icon-Praefix,
    " · " als Trenner, sprechende Link-Texte statt roher IDs)."""
    plugin_ids = _as_list(project.get("obsidian_plugin"))
    if not plugin_ids:
        return ""

    multiple = len(plugin_ids) > 1
    lines = []
    for plugin_id in plugin_ids:
        page_url = OBSIDIAN_PLUGIN_PAGE_URL.format(plugin_id=plugin_id)
        install_uri = OBSIDIAN_PLUGIN_INSTALL_URI.format(plugin_id=plugin_id)
        page_label = f"Plugin page ({plugin_id})" if multiple else "Plugin page"
        lines.append(
            f"- [{page_label}]({page_url}) (📲 [Open in Obsidian]({install_uri}))\n"
        )
    return "".join(lines)


def _generate_obsidian_theme_md(project) -> str:
    """Erzeugt eine Zeile mit Link zur Theme-Seite und einem direkten
    obsidian://-Installationslink. Gleicher Stil wie
    `_generate_obsidian_plugin_md`, nur mit dem Theme-Icon (🎨)."""
    theme_names = _as_list(project.get("obsidian_theme"))
    if not theme_names:
        return ""

    # Optionaler manueller Override der Seiten-URL, falls der
    # automatisch erzeugte Slug nicht zur echten URL passt. Gleiche
    # Reihenfolge wie `obsidian_theme`, falls dort eine Liste steht.
    override_pages = _as_list(project.get("obsidian_theme_page"))

    multiple = len(theme_names) > 1
    lines = []
    for index, theme_name in enumerate(theme_names):
        if index < len(override_pages):
            page_url = override_pages[index]
        else:
            page_url = OBSIDIAN_THEME_PAGE_URL.format(slug=_slugify(theme_name))
        install_uri = OBSIDIAN_THEME_INSTALL_URI.format(name=quote(theme_name))
        page_label = f"Theme page ({theme_name})" if multiple else "Theme page"
        lines.append(
            f"- [{page_label}]({page_url}) (📲 [Open in Obsidian]({install_uri}))\n"
        )
    return "".join(lines)


def _patch_markdown_list():
    try:
        from best_of.generators import markdown_list
    except ImportError as ex:
        log.warning(
            "best_of.generators.markdown_list konnte nicht importiert werden "
            "- extension_script wird uebersprungen.",
            exc_info=ex,
        )
        return

    # Verhindert doppeltes Patchen, falls das Script mehrfach geladen wird
    if getattr(markdown_list, "_obsidian_extension_applied", False):
        return

    original_generate_project_body = markdown_list.generate_project_body

    def generate_project_body_with_obsidian(project, configuration, labels) -> str:
        body_md = original_generate_project_body(project, configuration, labels)
        image_md = _generate_image_md(project)
        obsidian_md = _generate_obsidian_plugin_md(project) + _generate_obsidian_theme_md(project)
        # Bild kommt an den Anfang (wie im MkDocs-Catalog-Beispiel),
        # Plugin-/Theme-Hinweise werden als zusaetzliche Bullet-Points
        # ans Ende der bestehenden Liste angehaengt.
        return image_md + body_md + obsidian_md

    markdown_list.generate_project_body = generate_project_body_with_obsidian
    markdown_list._obsidian_extension_applied = True
    log.info(
        "extension_script.py geladen: 'image', 'obsidian_plugin' und "
        "'obsidian_theme' Projekteigenschaften sind jetzt aktiv."
    )


_patch_markdown_list()
