"""
Link Prefix extension: preprocessor that expands prefix:id links to full URLs.
"""

import re
from pathlib import Path

from markdown import Extension
from markdown.preprocessors import Preprocessor

try:
    import yaml
except ImportError:
    yaml = None


def _load_prefixes_file(path: str, project_root: str = ".") -> dict:
    """Load prefix -> URL template from a YAML file. Returns dict or empty dict on error.
    Prefix keys are normalized to lowercase. Path must resolve under project_root.
    """
    if not yaml:
        raise RuntimeError(
            "prefixes_file requires PyYAML. Install with: pip install pyyaml"
        )
    root = Path(project_root or ".").resolve()
    p = (root / path) if not Path(path).is_absolute() else Path(path)
    try:
        resolved = p.resolve()
        resolved.relative_to(root)
    except (ValueError, OSError):
        return {}
    if not resolved.exists():
        return {}
    try:
        with open(resolved, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k).lower(): str(v) for k, v in data.items() if v}


def _escape_url(url: str) -> str:
    """Escape URL for use in markdown link destination (minimal safe encoding)."""
    # Markdown allows most characters in URLs; encode spaces and characters
    # that could break the link syntax
    return url.replace(" ", "%20")


class LinkPrefixPreprocessor(Preprocessor):
    """Rewrites ](prefix:id) and ](prefix:id "title") to ](full_url) before parsing."""

    def __init__(self, md, prefixes):
        super().__init__(md)
        self.prefixes = dict(prefixes or {})
        if not self.prefixes:
            self._re = None
        else:
            # Build regex that matches any configured prefix
            names = "|".join(re.escape(k) for k in sorted(self.prefixes.keys(), key=len, reverse=True))
            # Match: ](prefix:id) or ](prefix:id "title") or ](prefix:id 'title')
            self._re = re.compile(
                r"\]\s*\(\s*(" + names + r"):([^\)\s\"']+)(\s+(\"[^\"]*\"|'[^']*'))?\s*\)",
                re.IGNORECASE,
            )

    def _repl(self, m):
        prefix = m.group(1).lower()
        id_part = m.group(2).strip()
        optional_title = (m.group(3) or "").strip()
        if prefix not in self.prefixes:
            return m.group(0)
        template = self.prefixes[prefix]
        try:
            expanded = template.format(id=id_part)
        except KeyError:
            expanded = template.replace("{id}", id_part)
        expanded = _escape_url(expanded)
        return "]({}{})".format(expanded, " " + optional_title if optional_title else "")

    def run(self, lines):
        if self._re is None:
            return lines
        text = "\n".join(lines)
        text = self._re.sub(self._repl, text)
        return text.split("\n")


class LinkPrefixExtension(Extension):
    """Python-Markdown extension: expand prefix:id links to full URLs."""

    def __init__(self, **kwargs):
        self.config = {
            "prefixes": [
                {},
                "Dict of prefix_name -> URL template with {id} placeholder. "
                "Example: {'youtube': 'https://www.youtube.com/watch?v={id}'}. "
                "Merged with prefixes from prefixes_file (config overrides file).",
            ],
            "prefixes_file": [
                "",
                "Path to a YAML file (relative to project_root) defining prefix -> URL template. "
                "Edit this file to add or change prefixes without touching code or tool config.",
            ],
            "project_root": [
                ".",
                "Project root for resolving prefixes_file path.",
            ],
        }
        super().__init__(**kwargs)

    def get_prefixes(self):
        """Load prefixes from prefixes_file (if set and present), then merge config prefixes on top.
        All prefix keys are normalized to lowercase (links are matched case-insensitively).
        """
        base = {}
        path = (self.getConfig("prefixes_file") or "").strip()
        if path:
            root = self.getConfig("project_root") or "."
            from_file = _load_prefixes_file(path, root)
            base.update(from_file)
        custom = self.getConfig("prefixes") or {}
        base.update({str(k).lower(): str(v) for k, v in custom.items() if v})
        return base

    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(
            LinkPrefixPreprocessor(md, self.get_prefixes()),
            "link_prefix",
            priority=25,  # run early, before standard link parsing
        )


def make_extension(**kwargs):
    return LinkPrefixExtension(**kwargs)
