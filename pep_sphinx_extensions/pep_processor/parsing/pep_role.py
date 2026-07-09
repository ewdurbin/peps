from docutils import nodes
from sphinx import roles
from sphinx.errors import NoUri
from sphinx.util.nodes import make_refnode


class PEPRole(roles.ReferenceRole):
    """Override the :pep: role"""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        # Get PEP URI from role text.
        pep_str, _, fragment = self.target.partition("#")
        try:
            pep_num = int(pep_str)
        except ValueError:
            msg = self.inliner.reporter.error(f'invalid PEP number {self.target}', line=self.lineno)
            prb = self.inliner.problematic(self.rawtext, self.rawtext, msg)
            return [prb], [msg]
        if self.has_explicit_title:
            title = self.title
        else:
            title = f"PEP {pep_num}"

        try:
            reference = make_refnode(
                self.env.app.builder,
                self.env.docname,
                f"pep-{pep_num:04}",
                fragment or None,
                nodes.Text(title),
            )
        except NoUri:
            return [nodes.inline("", title, classes=["pep"])], []

        reference["classes"].append("pep")
        reference["_title_tuple"] = (pep_num, fragment)
        return [reference], []
