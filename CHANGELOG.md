# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-03-07

### Changed

- Bump for testing PyPI publish workflow.

## [0.1.0] - 2026-03-07

### Added

- **LinkPrefixExtension**: Python-Markdown extension that expands prefixed link shorthand to full URLs.
  - Syntax: `[text](prefix:id)` and `[text](prefix:id "title")`; URL template uses `{id}` placeholder.
  - All prefixes from `prefixes_file` (YAML) and/or `prefixes` config—nothing hard-coded. Missing or empty file with no config means no prefixes.
- Config options: `prefixes`, `prefixes_file`, `project_root`.
- Entry point `link_prefix` under `markdown.extensions` for `extensions=['link_prefix']`.
- Documentation (docs/) with Zensical: installation, configuration, usage, demo, changelog, license.
- GitHub Actions: tests and deploy docs to GitHub Pages on push to `main`; publish to PyPI on release (version from tag).
