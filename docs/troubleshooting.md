# Troubleshooting

## Changelog page 404 when building docs locally

The Changelog page is generated from the root `CHANGELOG.md` only in CI (when deploying to GitHub Pages). When you run `zensical serve` or `zensical build` locally, `docs/changelog.md` does not exist, so the Changelog link may 404 or show an error. This is expected. The published docs at GitHub Pages include the changelog.

## Prefixed links are not expanded

- **Check that the extension is enabled.** In Zensical or MkDocs, ensure `link_prefix` is in your `markdown_extensions` list (and that the package is installed: `pip install markdown-link-prefix`).
- **Check that prefixes are defined.** All prefixes come from `prefixes_file` (YAML) and/or the `prefixes` config option. If `prefixes_file` is not set or the file is missing or empty, and `prefixes` is empty, no prefixes are defined—prefixed links are left unchanged.
- **Check the prefix name.** The link must use a prefix that exists in your config or YAML file (e.g. `youtube:VIDEO_ID`, `snkb:KB123`). Prefix names are case-insensitive.

## "prefixes_file requires PyYAML" error

Loading prefixes from a YAML file requires PyYAML. Install it with:

```bash
pip install "markdown-link-prefix[yaml]"
# or
pip install pyyaml
```

If you prefer not to use a file, define all prefixes in the `prefixes` config option instead (no PyYAML needed).
