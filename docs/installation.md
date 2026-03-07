# Installation

## Prerequisites

- **Python** ≥ 3.8
- **Python-Markdown** ≥ 3.4

For loading prefixes from a YAML file (`prefixes_file`), you also need **PyYAML** ≥ 6.0 (optional):

```bash
pip install "markdown-link-prefix[yaml]"
```

## Standard installation

```bash
pip install markdown-link-prefix
```

This installs the extension and `markdown`. You must configure prefixes (via `prefixes` or `prefixes_file`); with no config, no prefixes are defined. For `prefixes_file` you need PyYAML.

## Enabling the extension

Register the extension with Python-Markdown. How you do that depends on your environment.

### By name (recommended)

**Zensical** (`zensical.toml`):

```toml
[project.markdown_extensions.link_prefix]
# optional: prefixes = { ... }, prefixes_file = "docs/link_prefixes.yaml"
```

**MkDocs** (`mkdocs.yml`):

```yaml
markdown_extensions:
  - link_prefix
  # or with options:
  # - link_prefix:
  #     prefixes_file: docs/link_prefixes.yaml
  #     prefixes:
  #       jira: "https://mycompany.atlassian.net/browse/{id}"
```

**Python**:

```python
import markdown

html = markdown.markdown(
    source,
    extensions=["link_prefix"]
)
```

### By class (with options)

For full control over options:

```python
import markdown
from markdown_link_prefix import LinkPrefixExtension

md = markdown.Markdown(extensions=[
    LinkPrefixExtension(
        prefixes={
            "youtube": "https://www.youtube.com/watch?v={id}",
            "snkb": "https://mycompany.service-now.com/kb_view.do?sysparm_article={id}",
            "snci": "https://mycompany.service-now.com/sp?id=sc_cat_item&sys_id={id}",
        },
        # or load from file:
        # prefixes_file="link_prefixes.yaml",
        # project_root=".",
    )
])
html = md.convert(source)
```

## Check that it works

1. Create a Markdown file:

   ```markdown
   [Test link](youtube:dQw4w9WgXcQ)
   ```

2. Convert it with the extension enabled (e.g. `zensical serve`, or the Python snippet above).

3. In the output HTML, the link should point to `https://www.youtube.com/watch?v=dQw4w9WgXcQ`.

If the link still shows `youtube:dQw4w9WgXcQ` or is not a link, the extension is not in the Markdown pipeline—check that it’s listed in your tool’s `markdown_extensions` (or equivalent).
