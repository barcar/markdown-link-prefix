"""Tests for the Markdown Link Prefix extension."""

from unittest.mock import patch

import pytest
import markdown
from markdown_link_prefix import LinkPrefixExtension, make_extension
from markdown_link_prefix import extension as ext_module

# Prefixes used in tests when config is needed (no built-ins; all from file or config)
EXAMPLE_PREFIXES = {
    "youtube": "https://www.youtube.com/watch?v={id}",
    "snkb": "https://instance.service-now.com/kb_view.do?sysparm_article={id}",
    "snci": "https://instance.service-now.com/sp?id=sc_cat_item&sys_id={id}",
}


def _md(prefixes=None):
    if prefixes is not None:
        return markdown.Markdown(extensions=[LinkPrefixExtension(prefixes=prefixes)])
    return markdown.Markdown(extensions=[LinkPrefixExtension()])


def test_no_prefixes_when_no_config():
    """With no prefixes_file and no prefixes config, prefixed links are left unchanged."""
    md = _md()
    text = "[Watch](youtube:dQw4w9WgXcQ)"
    html = md.convert(text)
    assert 'href="youtube:dQw4w9WgXcQ"' in html


def test_youtube_from_config():
    md = _md(prefixes=EXAMPLE_PREFIXES)
    text = "[Watch](youtube:dQw4w9WgXcQ)"
    html = md.convert(text)
    assert 'href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"' in html
    assert "Watch" in html


def test_snkb_from_config():
    md = _md(prefixes=EXAMPLE_PREFIXES)
    text = "[KB article](snkb:KB0012345)"
    html = md.convert(text)
    assert 'href="https://instance.service-now.com/kb_view.do?sysparm_article=KB0012345"' in html


def test_snci_from_config():
    md = _md(prefixes=EXAMPLE_PREFIXES)
    text = "[Catalog item](snci:abc123def456)"
    html = md.convert(text)
    assert "instance.service-now.com" in html and "sc_cat_item" in html and "sys_id=abc123def456" in html


def test_link_with_title():
    md = _md(prefixes=EXAMPLE_PREFIXES)
    text = '[Watch](youtube:dQw4w9WgXcQ "Optional title")'
    html = md.convert(text)
    assert 'href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"' in html
    assert 'title="Optional title"' in html


def test_custom_prefix():
    md = _md(prefixes={"jira": "https://jira.example.com/browse/{id}"})
    text = "[Ticket](jira:PROJ-42)"
    html = md.convert(text)
    assert 'href="https://jira.example.com/browse/PROJ-42"' in html


def test_override_from_file():
    md = _md(prefixes={"snkb": "https://mycompany.service-now.com/kb_view.do?sysparm_article={id}"})
    text = "[KB](snkb:KB999)"
    html = md.convert(text)
    assert "mycompany.service-now.com" in html
    assert "KB999" in html


def test_unknown_prefix_unchanged():
    md = _md(prefixes=EXAMPLE_PREFIXES)
    text = "[Link](unknown:something)"
    html = md.convert(text)
    assert "unknown:something" in html


def test_prefix_key_case_insensitive():
    """Config keys are normalized to lowercase; links match case-insensitively."""
    md = _md(prefixes={"YouTube": "https://www.youtube.com/watch?v={id}"})
    text = "[Watch](youtube:abc)"
    html = md.convert(text)
    assert 'href="https://www.youtube.com/watch?v=abc"' in html


def test_normal_url_unchanged():
    md = _md()
    text = "[Google](https://google.com)"
    html = md.convert(text)
    assert 'href="https://google.com"' in html


def test_id_with_dash():
    md = _md(prefixes=EXAMPLE_PREFIXES)
    text = "[Video](youtube:abc-def_123)"
    html = md.convert(text)
    assert "abc-def_123" in html


def test_prefixes_file(tmp_path):
    """Prefixes loaded from YAML file when prefixes_file and project_root are set."""
    try:
        import yaml
    except ImportError:
        pytest.skip("PyYAML required for prefixes_file")
    config_file = tmp_path / "link_prefixes.yaml"
    config_file.write_text(
        "jira: \"https://jira.example.com/browse/{id}\"\n"
        "wiki: \"https://wiki.example.com/page/{id}\"\n",
        encoding="utf-8",
    )
    md = markdown.Markdown(
        extensions=[
            LinkPrefixExtension(
                prefixes_file="link_prefixes.yaml",
                project_root=str(tmp_path),
            )
        ]
    )
    html = md.convert("[Ticket](jira:PROJ-1) and [Doc](wiki:123)")
    assert "https://jira.example.com/browse/PROJ-1" in html
    assert "https://wiki.example.com/page/123" in html


def test_prefixes_file_path_traversal_returns_empty(tmp_path):
    """When path resolves outside project_root, load returns empty (no path traversal)."""
    try:
        import yaml
    except ImportError:
        pytest.skip("PyYAML required")
    (tmp_path / "project").mkdir()
    (tmp_path / "other.yaml").write_text("x: \"https://x.com/{id}\"", encoding="utf-8")
    from markdown_link_prefix.extension import _load_prefixes_file
    result = _load_prefixes_file("../other.yaml", str(tmp_path / "project"))
    assert result == {}


def test_prefixes_file_missing(tmp_path):
    """When prefixes_file path does not exist, no prefixes loaded from file; config still used."""
    md = markdown.Markdown(
        extensions=[
            LinkPrefixExtension(
                prefixes_file="nonexistent.yaml",
                project_root=str(tmp_path),
                prefixes={"jira": "https://jira.example.com/browse/{id}"},
            )
        ]
    )
    html = md.convert("[Ticket](jira:PROJ-1)")
    assert "https://jira.example.com/browse/PROJ-1" in html


def test_prefixes_file_invalid_yaml_returns_empty(tmp_path):
    """When YAML file is invalid, load returns empty (exception caught)."""
    (tmp_path / "bad.yaml").write_text("not: valid: yaml: [", encoding="utf-8")
    from markdown_link_prefix.extension import _load_prefixes_file
    result = _load_prefixes_file("bad.yaml", str(tmp_path))
    assert result == {}


def test_prefixes_file_not_dict(tmp_path):
    """When YAML file content is not a dict, load returns empty and config is used."""
    config_file = tmp_path / "link_prefixes.yaml"
    config_file.write_text("[\"list\", \"not\", \"dict\"]", encoding="utf-8")
    md = markdown.Markdown(
        extensions=[
            LinkPrefixExtension(
                prefixes_file="link_prefixes.yaml",
                project_root=str(tmp_path),
                prefixes={"x": "https://example.com/{id}"},
            )
        ]
    )
    html = md.convert("[Link](x:123)")
    assert "https://example.com/123" in html


def test_template_keyerror_fallback():
    """Template with extra placeholder triggers KeyError; fallback replace({id}) is used."""
    # Template has {id} and {name}; we only pass id= so .format() raises KeyError; fallback replace
    md = _md(prefixes={"multi": "https://example.com/{id}/{name}"})
    html = md.convert("[Link](multi:XYZ)")
    assert "https://example.com/XYZ/{name}" in html


def test_escape_url_space_in_template():
    """URL with space in template is escaped via _escape_url."""
    md = _md(prefixes={"space": "https://example.com/foo bar/{id}"})
    html = md.convert("[Link](space:xyz)")
    assert "foo%20bar" in html


def test_prefixes_file_requires_pyyaml(tmp_path):
    """When prefixes_file is set and PyYAML is not available, RuntimeError is raised."""
    (tmp_path / "link_prefixes.yaml").write_text("x: \"https://x.com/{id}\"", encoding="utf-8")
    with patch.object(ext_module, "yaml", None):
        with pytest.raises(RuntimeError, match="prefixes_file requires PyYAML"):
            markdown.Markdown(
                extensions=[
                    LinkPrefixExtension(
                        prefixes_file="link_prefixes.yaml",
                        project_root=str(tmp_path),
                    )
                ]
            )


def test_make_extension():
    """make_extension() returns a LinkPrefixExtension instance."""
    ext = make_extension(prefixes={"a": "https://a.com/{id}"})
    assert isinstance(ext, LinkPrefixExtension)
    md = markdown.Markdown(extensions=[ext])
    html = md.convert("[Link](a:123)")
    assert "https://a.com/123" in html
