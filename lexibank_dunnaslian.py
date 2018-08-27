# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.path import Path
from pylexibank.dataset import Metadata
from pylexibank.dataset import Dataset as BaseDataset
from clldutils.misc import slug, nfilter


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'dunnaslian'

    def cmd_download(self, **kw):
        return

    def cmd_install(self, **kw):
        source = self.raw.read_bib()[0]
        with self.cldf as ds:
            ds.add_sources(source)
            ds.add_languages(id_factory=lambda l: slug(l['ID']))
            ds.add_concepts(id_factory=lambda c: slug(c.label))
            header = []
            for line in self.raw.read_tsv("Aslian_wordlists_Master_full+Maniq.tsv"):
                row = [e.strip() for e in line]
                if row[0] == "WORD":
                    header = row[1:]
                elif row[0]:
                    lang = row.pop(0)
                    for i in range(0, 10, 2):
                        concept = header[i]
                        lexeme = row[i].strip()
                        cog = row[i + 1]
                        if lexeme and lexeme not in ['––', '--', '-']:
                            cogid = slug(concept + '-' + cog)
                            for lex in ds.add_lexemes(
                                Language_ID=slug(lang),
                                Parameter_ID=slug(concept),
                                Value=lexeme,
                                Source=source.id
                            ):
                                ds.add_cognate(
                                    lexeme=lex,
                                    Cognateset_ID=cogid,
                                    Source=['DunnKruspeBurenhult2013'])

