"""
Sistema de referências estilo BibTeX para CustomSlide (manim-slides).

Uso:
    # 1) uma vez, ex. no topo de custom_slide.py:
    from components.references import ReferenceMixin, load_bib
    load_bib("assets/refs.bib")          # ou register_ref("chave", author=..., ...)

    # 2) CustomSlide herda do mixin:
    class CustomSlide(ReferenceMixin, Slide): ...

    # 3) em cada slide:
    c = self.cite(texto, "landau1937")           # label [n] ou (Autor, ano)
    self.play(FadeIn(c))
    ...
    foot = self.slide_references()               # só as citadas NESTE slide
    self.add(foot)
"""

import re

from manim import DOWN, UP, RIGHT, DL, VGroup, Text

# --------------------------------------------------------------------------
# Registro global (carregado uma vez; vale para qualquer slide/processo)
# --------------------------------------------------------------------------
REFS = {}  # chave -> dict(author, title, year, journal, doi)
_ORDER = []  # ordem de registro => numeração determinística


def register_ref(key, author, title, year, journal=None, doi=None):
    if key not in REFS:
        _ORDER.append(key)
    REFS[key] = dict(author=author, title=title, year=year, journal=journal, doi=doi)


def _parse_bib(text):
    """Parser mínimo de .bib: @tipo{chave, campo = {valor}, ...}"""
    entries = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        key, start = m.group(2), m.end()
        depth, i = 1, start
        while i < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        body = text[start : i - 1]
        fields = {}
        for f in re.finditer(r"(\w+)\s*=\s*", body):
            j = f.end()
            if j >= len(body):
                continue
            if body[j] == "{":
                d, k = 1, j + 1
                while k < len(body) and d:
                    d += {"{": 1, "}": -1}.get(body[k], 0)
                    k += 1
                val = body[j + 1 : k - 1]
            elif body[j] == '"':
                k = body.index('"', j + 1)
                val = body[j + 1 : k]
            else:
                val = re.match(r"[^,\s]+", body[j:]).group(0)
            fields[f.group(1).lower()] = re.sub(r"[{}]", "", val).strip()
        entries[key] = fields
    return entries


def load_bib(path):
    with open(path, encoding="utf-8") as fh:
        entries = _parse_bib(fh.read())
    for key, f in entries.items():
        register_ref(
            key,
            author=f.get("author", ""),
            title=f.get("title", ""),
            year=f.get("year", ""),
            journal=f.get("journal"),
            doi=f.get("doi"),
        )


def _short_author(author):
    """'Landau, L. D. and Lifshitz, E. M.' -> 'Landau & Lifshitz'"""
    names = [a.strip().split(",")[0].strip() for a in author.split(" and ")]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} & {names[1]}"
    return f"{names[0]} et al."


def _last_leaf(mob):
    """Último glifo/forma do objeto (fim do texto da última linha)."""
    while mob.submobjects:
        mob = mob.submobjects[-1]
    return mob


# --------------------------------------------------------------------------
# Mixin
# --------------------------------------------------------------------------
class ReferenceMixin:
    # "number" -> [3]   |   "author-year" -> (Landau, 1937)
    CITE_STYLE = "number"

    def _slide_keys(self):
        if not hasattr(self, "_slide_ref_keys"):
            self._slide_ref_keys = []  # por instância = por slide
        return self._slide_ref_keys

    def register_ref(self, key, author, title, year, journal=None, doi=None):
        """Atalho para o register_ref do módulo: self.register_ref(...)"""
        register_ref(key, author, title, year, journal, doi)

    def ref_label(self, key):
        r = REFS[key]
        if self.CITE_STYLE == "author-year":
            return f"({_short_author(r['author'])}, {r['year']})"
        return f"[{_ORDER.index(key) + 1}]"

    def cited_keys(self):
        """Chaves citadas (via cite) NESTE slide, em ordem."""
        return list(self._slide_keys())

    def _cite_text(self, keys):
        if self.CITE_STYLE == "author-year":
            parts = [
                f"{_short_author(REFS[k]['author'])}, {REFS[k]['year']}" for k in keys
            ]
            return "(" + "; ".join(parts) + ")"
        return "[" + ", ".join(str(_ORDER.index(k) + 1) for k in keys) + "]"

    def cite(self, obj, *keys, buff=0.1, dy=0.0, **inline):
        """Label de citação logo após o ÚLTIMO caractere de `obj`, em texto normal.

        Uma ou várias chaves no mesmo label:
            self.cite(caption, "landau1937")                -> [1]
            self.cite(caption, "landau1937", "binder1981")  -> [1, 2]
        Para criar a referência na hora (uma só chave): author=, title=, year=, ...
        `dy` ajusta a altura (ex.: dy=0.05); `buff` o espaço horizontal.
        """
        if not keys:
            raise ValueError("cite() precisa de pelo menos uma chave")
        if inline:
            if len(keys) != 1:
                raise ValueError("Dados inline só valem para uma chave")
            if keys[0] not in REFS:
                register_ref(keys[0], **inline)
        for k in keys:
            if k not in REFS:
                raise KeyError(f"Referência '{k}' não encontrada")
            if k not in self._slide_keys():
                self._slide_keys().append(k)

        label = Text(
            self._cite_text(keys),
            font_size=self.FONT_SIZE_CITATION,
            color=self.get_color("title"),
        )
        label.next_to(_last_leaf(obj), RIGHT, buff=buff)
        label.ref_keys = list(keys)
        return label

    def _format_ref(self, key, full):
        r = REFS[key]
        head = f"{self.ref_label(key)} "
        if not full:
            return f"{head}{_short_author(r['author'])} ({r['year']})."
        txt = f"{head}{r['author']} ({r['year']}). {r['title']}"
        if r.get("journal"):
            txt += f", {r['journal']}"
        return txt + "."

    def build_reference_list(self, keys, full=False, font_size=None):
        group = VGroup(
            *[
                Text(
                    self._format_ref(k, full),
                    font="Latin Modern Mono",
                    font_size=font_size or self.FONT_SIZE_FOOTNOTE,
                    color=self.get_color("divider"),
                )
                for k in keys
            ]
        )
        return group.arrange(DOWN, aligned_edge=-RIGHT, buff=0.1)

    def slide_references(self, extra=(), full=False, keys=None):
        """Rodapé com as refs citadas neste slide (+ `extra` manuais).
        Com `keys=[...]` mostra exatamente essas, ignorando o rastreio."""
        if keys is None:
            keys = list(self._slide_keys())
            keys += [k for k in extra if k not in keys]
        footer = self.build_reference_list(keys, full=full)
        return footer.to_edge(DL, buff=0.1)
