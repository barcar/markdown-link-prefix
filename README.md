# Markdown Link Prefix

[![PyPI version](https://img.shields.io/pypi/v/markdown-link-prefix.svg)](https://pypi.org/project/markdown-link-prefix/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deploy docs to GitHub Pages](https://github.com/barcar/markdown-link-prefix/actions/workflows/pages.yml/badge.svg)](https://github.com/barcar/markdown-link-prefix/actions/workflows/pages.yml)

**Author:** [BarCar](https://github.com/barcar) · **Repository:** [github.com/barcar/markdown-link-prefix](https://github.com/barcar/markdown-link-prefix)

A **Python-Markdown extension** that expands prefixed link shorthand into full URLs. Write `[text](youtube:VIDEO_ID)` or `[KB](snkb:KB123)`; when rendered, they become normal links using URL templates you define in a YAML file or config. All prefixes come from `link_prefixes.yaml` (or `prefixes_file`) and/or the `prefixes` option—nothing is hard-coded. Works with Zensical, MkDocs, or any tool that uses Python-Markdown.

[![BuyMeACoffee](https://raw.githubusercontent.com/barcar/buymeacoffee-badges/main/bmc-donate-white.svg)](https://buymeacoffee.com/barcar)

## Features

- **Prefixed links**: `[text](prefix:id)` → `[text](https://.../id)` via a URL template with `{id}`.
- **All from config or file**: define prefixes in `prefixes_file` (YAML) and/or `prefixes`; if the file is missing or empty and no config is given, no prefixes are defined.
- **Optional link titles**: `[text](prefix:id "title")` is supported.

## Installation

```bash
pip install markdown-link-prefix
```

Requires: `markdown>=3.4`. For loading from a YAML file: `pip install "markdown-link-prefix[yaml]"` (PyYAML).

## Quick example

```python
import markdown
from markdown_link_prefix import LinkPrefixExtension

text = "[Watch](youtube:dQw4w9WgXcQ) and [KB](snkb:KB0012345)"
md = markdown.Markdown(extensions=[
    LinkPrefixExtension(prefixes_file="docs/link_prefixes.yaml", project_root=".")
])
html = md.convert(text)  # links expanded from the YAML templates
```

In Zensical or MkDocs, add `link_prefix` to your Markdown extensions and set `prefixes_file` (and optionally `prefixes`). See the [documentation](https://barcar.github.io/markdown-link-prefix/) for configuration, usage, and examples.

## Documentation

**Online:** [Documentation](https://barcar.github.io/markdown-link-prefix/) (GitHub Pages).

To build the docs locally:

```bash
pip install -e ".[docs]"
zensical serve
```

(The Changelog page may 404 locally—it is generated from root `CHANGELOG.md` in CI only.)

## License

MIT License. See [LICENSE](LICENSE).
