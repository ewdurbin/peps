from types import SimpleNamespace

import pytest
from docutils import nodes
from docutils.core import publish_doctree
from docutils.parsers.rst import roles

from pep_sphinx_extensions.pep_processor.html.pep_html_builder import (
    DirectoryBuilder,
    FileBuilder,
)
from pep_sphinx_extensions.pep_processor.parsing.pep_role import PEPRole


@pytest.mark.parametrize(
    ("builder_class", "target", "expected"),
    [
        (FileBuilder, "621", "../pep-0621.html"),
        (DirectoryBuilder, "621", "../../pep-0621/"),
        (DirectoryBuilder, "621#license", "../../pep-0621/#license"),
        (DirectoryBuilder, "639", "../"),
    ],
    ids=["html", "dirhtml", "fragment", "parent-pep"],
)
def test_nested_pep_reference(
    monkeypatch: pytest.MonkeyPatch,
    builder_class: type[FileBuilder],
    target: str,
    expected: str,
) -> None:
    monkeypatch.setitem(roles._roles, "pep", PEPRole())
    docname = "pep-0639/appendix-rejected-ideas"
    builder = object.__new__(builder_class)
    env = SimpleNamespace(
        app=SimpleNamespace(builder=builder),
        docname=docname,
        temp_data={"docname": docname},
    )

    doctree = publish_doctree(
        f":pep:`{target}`",
        source_path="peps/pep-0639/appendix-rejected-ideas.rst",
        settings_overrides={
            "builder": builder.name,
            "env": env,
        },
    )

    reference = next(doctree.findall(nodes.reference))
    assert reference["refuri"] == expected
