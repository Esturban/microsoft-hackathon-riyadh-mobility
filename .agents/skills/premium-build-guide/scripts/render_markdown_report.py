#!/usr/bin/env python3
"""Render a Markdown report to DOCX/PDF with reliable Word page breaks."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


PAGEBREAK_LUA = """\
function RawBlock(el)
  if el.format == 'tex' and el.text:match('\\\\newpage') then
    return pandoc.RawBlock('openxml', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
  end
end
"""


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"required tool not found on PATH: {name}")
    return path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--docx", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--reference-doc", type=Path)
    parser.add_argument("--pages-dir", type=Path)
    args = parser.parse_args()

    require_tool("pandoc")
    require_tool("soffice")

    args.docx.parent.mkdir(parents=True, exist_ok=True)
    args.pdf.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        lua = tmpdir / "pagebreak.lua"
        lua.write_text(PAGEBREAK_LUA)
        tmp_docx = tmpdir / args.docx.name
        pandoc_cmd = [
            "pandoc",
            str(args.markdown),
            "--resource-path=.",
            "--from",
            "markdown+raw_tex",
            "--to",
            "docx",
            f"--lua-filter={lua}",
            "-o",
            str(tmp_docx),
        ]
        if args.reference_doc:
            pandoc_cmd.insert(-2, f"--reference-doc={args.reference_doc}")
        run(pandoc_cmd)
        shutil.copy2(tmp_docx, args.docx)

        pdf_dir = tmpdir / "pdf"
        pdf_dir.mkdir()
        run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(pdf_dir), str(args.docx)])
        rendered_pdf = pdf_dir / f"{args.docx.stem}.pdf"
        shutil.copy2(rendered_pdf, args.pdf)

    if args.pages_dir:
        require_tool("pdftoppm")
        if args.pages_dir.exists():
            shutil.rmtree(args.pages_dir)
        args.pages_dir.mkdir(parents=True)
        run(["pdftoppm", "-png", "-r", "144", str(args.pdf), str(args.pages_dir / "page")])


if __name__ == "__main__":
    main()
