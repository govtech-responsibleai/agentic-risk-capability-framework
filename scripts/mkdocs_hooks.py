"""MkDocs hook: generate the register's site files at build time.

The YAML in arc-risk-register/ is the only committed form of the register. On
every build (and every `mkdocs serve` reload) this hook validates it and adds
the generated JSON and Crosswalks page to the site in memory, so nothing
generated is committed and the site cannot serve a stale copy. An invalid
register fails the build.
"""

import logging
import sys
from pathlib import Path

from mkdocs.exceptions import PluginError
from mkdocs.structure.files import File

sys.path.insert(0, str(Path(__file__).parent))
import build_risk_register  # noqa: E402

log = logging.getLogger('mkdocs.hooks.register')


def on_files(files, config):
    try:
        generated, warnings = build_risk_register.generate()
    except build_risk_register.RegisterInvalid as e:
        raise PluginError(str(e))
    for w in warnings:
        log.info('register: %s', w)
    for src_uri, content in generated.items():
        stale = files.get_file_from_path(src_uri)  # e.g. a copy left in docs/ by an older checkout
        if stale is not None:
            files.remove(stale)
        files.append(File.generated(config, src_uri, content=content))
    return files
