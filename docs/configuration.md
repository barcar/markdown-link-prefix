# Configuration

All prefixes come from **`prefixes_file`** (YAML) and/or **`prefixes`** (config). Nothing is hard-coded. If the file is missing or empty and no config is given, no prefixes are defined. Prefix names are **case-insensitive**: keys are normalized to lowercase, so `YouTube` and `youtube` in config or in links are equivalent.

## Option reference

| Option | Default | Description |
|--------|--------|--------------|
| `prefixes` | `{}` | Dict of prefix name → URL template with `{id}`. Merged on top of prefixes loaded from prefixes_file; same key overrides. |
| `prefixes_file` | `""` | Path to a YAML file (relative to `project_root`) defining prefix → URL template. If missing or empty, no prefixes are loaded from file. Requires PyYAML. |
| `project_root` | `"."` | Project root for resolving `prefixes_file`. |

## Controlling prefixes without editing code

You never need to edit Python code to add or change prefixes. Use one or both of:

### 1. Tool config (MkDocs, Zensical)

In your site config, set `prefixes` and/or `prefixes_file`. When you want a change, edit the config file and rebuild.

**Zensical** (`zensical.toml`):

```toml
[project.markdown_extensions.link_prefix]
prefixes_file = "docs/link_prefixes.yaml"
# optional overrides or extras:
# prefixes = { snkb = "https://mycompany.service-now.com/kb_view.do?sysparm_article={id}" }
```

**MkDocs** (`mkdocs.yml`):

```yaml
markdown_extensions:
  - link_prefix:
      prefixes_file: docs/link_prefixes.yaml
      # optional:
      # prefixes:
      #   snkb: "https://mycompany.service-now.com/kb_view.do?sysparm_article={id}"
```

### 2. External YAML file (`prefixes_file`)

Put prefix definitions in a YAML file and point the extension at it. Anyone can edit that file to add or change prefixes.

Example `docs/link_prefixes.yaml`:

```yaml
youtube: "https://www.youtube.com/watch?v={id}"
snkb: "https://mycompany.service-now.com/kb_view.do?sysparm_article={id}"
snci: "https://mycompany.service-now.com/sp?id=sc_cat_item&sys_id={id}"
jira: "https://mycompany.atlassian.net/browse/{id}"
confluence: "https://wiki.mycompany.com/display/{id}"
```

Then in Zensical or MkDocs:

```toml
[project.markdown_extensions.link_prefix]
prefixes_file = "docs/link_prefixes.yaml"
project_root = "."
```

Merge order: load from **prefixes_file** (if set and file exists), then apply **prefixes** (config). Config overrides or adds to what was loaded from the file.

## URL template format

- Use `{id}` in the URL where the link ID should go.
- The “id” is the part after `prefix:` in the link, e.g. `dQw4w9WgXcQ` in `youtube:dQw4w9WgXcQ`, or `KB0012345` in `snkb:KB0012345`.

Examples:

| Prefix | Template | Example link | Result |
|--------|-----------|--------------|--------|
| youtube | `https://www.youtube.com/watch?v={id}` | `[Watch](youtube:abc123)` | `https://www.youtube.com/watch?v=abc123` |
| snkb | `https://instance.service-now.com/kb_view.do?sysparm_article={id}` | `[KB](snkb:KB999)` | Knowledge Article |
| snci | `https://instance.service-now.com/sp?id=sc_cat_item&sys_id={id}` | `[Item](snci:abc123)` | Catalog Item |
| jira | `https://jira.example.com/browse/{id}` | `[Ticket](jira:PROJ-42)` | `https://jira.example.com/browse/PROJ-42` |

## Defining prefixes in the YAML file

The repo's `docs/link_prefixes.yaml` is an example: it defines `youtube`, `snkb` (Knowledge Articles), `snci` (Catalog Items), and `jira`. Copy or adapt it for your site and set `prefixes_file` to its path. Override any entry (e.g. your ServiceNow instance) in the same file or via the `prefixes` config option.

## PyYAML for `prefixes_file`

Loading from a file requires PyYAML. Install it with:

```bash
pip install "markdown-link-prefix[yaml]"
# or
pip install pyyaml
```

If `prefixes_file` is set and PyYAML is not installed, the extension raises a clear error telling you to install it.
