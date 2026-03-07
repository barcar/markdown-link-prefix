# Usage

## Link syntax

- `[link text](prefix:id)` — expands to a normal link using the URL template for `prefix`.
- `[link text](prefix:id "optional title")` — same, with an optional title attribute.

The ID is everything after `prefix:` until a space, quote, or closing parenthesis. So you can use YouTube-style IDs, KB numbers, Jira keys (e.g. `PROJ-123`), etc.

## Zensical

1. Add the extension and optional options in `zensical.toml`:

```toml
[project.markdown_extensions.link_prefix]
prefixes_file = "docs/link_prefixes.yaml"
project_root = "."
```

2. Optionally create `docs/link_prefixes.yaml` (or another path) with your prefix → URL mappings.

3. Run `zensical serve` or `zensical build`. Prefixed links in your docs will be expanded.

## MkDocs

1. Add the extension in `mkdocs.yml`:

```yaml
markdown_extensions:
  - link_prefix:
      prefixes_file: docs/link_prefixes.yaml
      # or inline:
      # prefixes:
      #   snkb: "https://mycompany.service-now.com/kb_view.do?sysparm_article={id}"
```

2. Install the package: `pip install markdown-link-prefix`. For file-based config, also install PyYAML or `pip install markdown-link-prefix[yaml]`.

3. Run `mkdocs serve` or `mkdocs build`.

## Plain Python

```python
import markdown
from markdown_link_prefix import LinkPrefixExtension

# Using prefixes from a YAML file
# Prefixes must be configured (file or config); with no config, nothing is expanded
md = markdown.Markdown(extensions=[LinkPrefixExtension(prefixes={"youtube": "https://www.youtube.com/watch?v={id}"})])
html = md.convert("[Watch](youtube:dQw4w9WgXcQ)")

# With custom prefixes
md = markdown.Markdown(extensions=[
    LinkPrefixExtension(prefixes={
        "jira": "https://jira.example.com/browse/{id}",
    })
])
html = md.convert("[Ticket](jira:PROJ-42)")

# With prefixes from a YAML file (requires PyYAML)
md = markdown.Markdown(extensions=[
    LinkPrefixExtension(
        prefixes_file="link_prefixes.yaml",
        project_root="/path/to/project",
    )
])
html = md.convert("[KB](snkb:KB0012345)")
```

## Building the docs locally

From the repo root:

```bash
pip install -e ".[docs]"
zensical serve
```

Open the URL shown (e.g. http://127.0.0.1:8000). The docs use the link_prefix extension and a sample `link_prefixes.yaml` so you can see prefixed links in action. (The Changelog page may 404 locally—it is generated from root `CHANGELOG.md` in CI only.)
