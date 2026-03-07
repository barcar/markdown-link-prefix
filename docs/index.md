# Markdown Link Prefix

**A Python-Markdown extension that expands prefixed link shorthand into full URLs.**

Markdown Link Prefix is a [Python-Markdown](https://python-markdown.github.io/) extension. Write short links like [Watch video](youtube:dQw4w9WgXcQ) or [KB article](snkb:KB0012345); when rendered, they become normal URLs using templates you define in a YAML file or config. All prefixes come from `link_prefixes.yaml` (or `prefixes_file`) and/or the `prefixes` option—nothing is hard-coded. It works with [Zensical](https://zensical.org), MkDocs, or any tool that uses Python-Markdown.

[![PyPI version](https://img.shields.io/pypi/v/markdown-link-prefix.svg)](https://pypi.org/project/markdown-link-prefix/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deploy docs to GitHub Pages](https://github.com/barcar/markdown-link-prefix/actions/workflows/pages.yml/badge.svg)](https://github.com/barcar/markdown-link-prefix/actions/workflows/pages.yml)

**Author:** [BarCar](https://github.com/barcar) · **Repository:** [github.com/barcar/markdown-link-prefix](https://github.com/barcar/markdown-link-prefix)

[![BuyMeACoffee](https://raw.githubusercontent.com/barcar/buymeacoffee-badges/main/bmc-donate-white.svg)](https://buymeacoffee.com/barcar)

## Why use it?

- **Shorter, readable links** in Markdown: `[Watch](youtube:VIDEO_ID)` instead of long URLs.
- **Change URLs in one place**: point all `snkb:` / `snci:` links to your ServiceNow instance by editing your `link_prefixes.yaml` or config—no search-and-replace in content.
- **Easy to add prefixes**: define new ones (Jira, Confluence, internal tools) in config or a file.

## Quick example

In your Markdown:

```markdown
- [Watch video](youtube:dQw4w9WgXcQ)
- [KB article](snkb:KB0012345)
```

With the extension enabled and prefixes defined (in a YAML file or config), those render as normal links. **All prefixes come from your `link_prefixes.yaml` (or `prefixes_file`) and/or the `prefixes` option—nothing is hard-coded.** If the file is missing or empty and no config is given, no prefixes are defined.

## Controlling prefixes without editing code

You can change or add prefixes in two ways—**no code changes**:

1. **Tool config** (MkDocs, Zensical): in `mkdocs.yml` or `zensical.toml`, set the `prefixes` option (or use `prefixes_file`). Edit the config file when you want to add a prefix or change a URL template.

2. **External YAML file**: set `prefixes_file` to a path (e.g. `docs/link_prefixes.yaml`). Edit that file whenever you want to add or change prefixes; the extension loads it at build time. Ideal for sharing one file across projects or non-developers.

See [Configuration](configuration.md) for details and examples.

## Next steps

- [Demo](demo.md) – See YouTube link examples in action
- [Installation](installation.md) – Install and enable the extension
- [Configuration](configuration.md) – Prefixes, `prefixes_file`, and all options
- [Usage](usage.md) – Zensical, MkDocs, and plain Python
- [Troubleshooting](troubleshooting.md) – Changelog 404, links not expanding, PyYAML
