# SecureCAN Documentation Prompt

## Context

You are writing technical documentation for SecureCAN — an offline-first automotive cybersecurity platform. The audience includes developers, hardware engineers, security researchers, investors, and hackathon participants.

## Documentation Principles

1. **Accuracy** — Technical details must match implementation. Document assumptions and limitations.
2. **Completeness** — Every file must be meaningful. No placeholder text or "coming soon".
3. **Clarity** — Engineering language. Avoid generic AI wording. Use precise terminology.
4. **Structure** — Every markdown file must include: Title, Purpose, Scope, Detailed sections, Future TODO section.

## Key Files to Reference

- `PRODUCT_CONSTITUTION.md` — Inviolable product principles
- `docs/SRS.md` — Software requirements specification
- `docs/SYSTEM_ARCHITECTURE.md` — System-level architecture
- `configs/` — Configuration files that must align with documentation

## Documentation Structure

```
SecureCAN/
├── README.md           # Project overview, quick start
├── PRODUCT.md          # Product description, market, features
├── VISION.md           # Vision statement, design north stars
├── PROJECT_CONTEXT.md  # Technical context, constraints
├── PRODUCT_CONSTITUTION.md  # Inviolable principles
├── ROADMAP.md          # Phased milestone plan
├── CHANGELOG.md        # Release history
├── docs/               # Detailed technical documentation
├── configs/            # Configuration files (documented inline)
├── prompts/            # AI development prompts
└── memory/             # Sprint and decision tracking
```

## Writing Guidelines

### Markdown Style

- Use `#` for title, `##` for major sections, `###` for subsections
- Code blocks with language specifiers
- Tables for structured data
- Diagrams using ASCII art or Mermaid (where supported)
- Lists for enumerations
- Bold for emphasis, code ticks for inline code

### Content Checklist

Every document should answer:
- What is this document about? (Purpose)
- What does it cover? (Scope)
- Who is the audience? (Reader)
- What are the key technical details? (Content)
- What is not yet done? (TODOs)

### File Relationships

When referencing another file, use relative paths:
```
See `docs/SOFTWARE_ARCHITECTURE.md` for service layer details.
See `configs/firewall_rules.json` for default rule definitions.
```

### Non-Goals

Documentation should not:
- Include placeholder text
- Contradict other documentation
- Reference features not yet planned in ROADMAP.md
- Use marketing fluff in technical sections

## Common Tasks

### Adding a New Document

1. Create file with .md extension in appropriate directory
2. Add title, purpose, scope sections
3. Write detailed technical content
4. Add TODOs section at the end
5. Update any cross-references in other documents

### Updating Configuration Documentation

1. Update the config JSON file with new fields
2. Update any documentation that references the config fields
3. Ensure examples in documentation match actual config structure

---

**TODOs**

- [ ] Review all documentation for consistency every sprint
- [ ] Create architecture decision record (ADR) process
- [ ] Add API documentation auto-generation from TypeScript interfaces
- [ ] Write deployment runbook for production gateway builds
