# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.path import Path
from pylexibank.dataset import Metadata
from pylexibank.dataset import Dataset as BaseDataset
from clldutils.misc import slug, nfilter


class Dataset(BaseDataset):
    dir = Path(__file__).parent

    def cmd_download(self, **kw):
        return

    def cmd_install(self, **kw):
        cmap = {c.english: c.concepticon_id for c in self.conceptlist.concepts.values()}
        source = self.raw.read_bib()[0]
        languages = {l['NAME']: l for l in self.languages}

        with self.cldf as ds:
            ds.add_sources(source)
            header = []
            for line in self.raw.read_tsv("Aslian_wordlists_Master_full+Maniq.tsv"):
                row = [e.strip() for e in line]
                if row[0] == "WORD":
                    header = row[1:]
                    for concept in nfilter(header):
                        ds.add_concept(
                            ID=cmap[concept], Name=concept, Concepticon_ID=cmap[concept])
                elif row[0]:
                    lang = row.pop(0)
                    ds.add_language(
                        Glottocode=languages[lang]['GLOTTOCODE'],
                        Name=languages[lang]['DIALECT'],
                        ISO639P3code=languages[lang]['ISO'],
                        ID=slug(lang))
                    for i in range(0, 10, 2):
                        concept = header[i]
                        lexeme = row[i].strip()
                        cog = row[i + 1]
                        if lexeme and lexeme not in ['––', '--', '-']:
                            cogid = slug(concept + '-' + cog)
                            for lex in ds.add_lexemes(
                                Language_ID=slug(lang),
                                Parameter_ID=cmap[concept],
                                Value=lexeme,
                                Source=source.id
                            ):
                                ds.add_cognate(
                                    lexeme=lex,
                                    Cognateset_ID=cogid,
                                    Source=['DunnKruspeBurenhult2013'])
