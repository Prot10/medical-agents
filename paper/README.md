# NeuroAgent paper (Nature Machine Intelligence, Article)

| Folder | Content |
|---|---|
| `manuscript/` | LaTeX source. `main.tex` plus one file per section in `sections/`; `references.bib` |
| `figures/` | Figures made in HTML/CSS (`python3 build.py` → `figN.pdf`, `figN.png`; `--static` exports for Figma) |
| `template/` | Springer Nature LaTeX template v3.1 (December 2024) as downloaded, with its user manual |

## Build

```bash
cd paper/manuscript && tectonic main.tex
```

For now `main.tex` is a plan, not the manuscript: no section text yet. The abstract page holds the
narrative and what the paper must prove (claims C1–C5, the evidence for each, and what would refute
it). The overview page holds positioning, word budget, display items and risks. Every section then
gives, in the same order: role in the narrative, what goes there, structure and length, artefacts
and why they are needed, and status. Prose replaces these blocks section by section.

## NMI limits (checked 26 Oct 2026)

Main text ≤ 3,500 words (without abstract, Methods, references, legends) · abstract ≤ 150 words,
no references · ≤ 6 display items · ~50 references · ≤ 10 Extended Data items · Results and Methods
with subheadings, introduction and Discussion without · initial submission in any format (PDF),
final in LaTeX with standard packages and numbered references pasted from the `.bbl`.

## References

`references.bib` merges `docs/research/*.bib` (26 Oct 2026). `sn-nature.bst` fails on
`@inproceedings` ("You can't pop an empty literal stack"), so conference papers are written as
`@article` with the proceedings in `journal`, which matches Nature's style ("Proc. ICLR"). Entries
marked TODO in a `note` need their details checked.
