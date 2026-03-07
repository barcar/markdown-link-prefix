# Demo: YouTube links

This page shows the link prefix extension in action with **YouTube** examples. The links below use the `youtube:` prefix; when the docs are built, they are expanded to full URLs.

## Watch URL (`youtube:`)

Use the `youtube:` prefix for the standard watch URL format:

- [Introduction to Python](youtube:dQw4w9WgXcQ)
- [Markdown tutorial](youtube:2XkV6IpV2Y0)
- [Git in 15 minutes](youtube:USjZcfj8FX8)

Same link with an optional title:

- [Watch on YouTube](youtube:dQw4w9WgXcQ "Click to open in YouTube")

## In a paragraph

You can embed prefixed links in prose: check out [this classic](youtube:dQw4w9WgXcQ) or [this one](youtube:2XkV6IpV2Y0) for more. The extension rewrites them before Markdown parses the document, so the output is a normal `<a href="...">` link.

## Source vs output

In your Markdown you write:

```markdown
[Watch video](youtube:dQw4w9WgXcQ)
```

After the extension runs, the link destination becomes `https://www.youtube.com/watch?v=dQw4w9WgXcQ`, and the rest of the pipeline sees a standard Markdown link.
