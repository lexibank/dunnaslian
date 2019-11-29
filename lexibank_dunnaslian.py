# coding: utf8
from pathlib import Path
from clldutils.misc import slug
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import FormSpec

DATAFILE = "Aslian_wordlists_Master_full+Maniq.tsv"

# some of the lexemes will be split into multiple lexemes.
# these have been checked to make sure the cognates align correctly
# to the split entries e.g.
# Mah_Meri _child_ has the lexeme "kənɔn; budɛk" and the cognate "1". 
# Set 1 refers to the first item ("kənɔn") not the second ("budɛk") which
# has no cognate, so this is set to None
COGNATE_OVERRIDES = {
    "kənɔn; budɛk": ("1", None),
    "knɔn; knkɔn": ("1", "1"),
    "klkɔʔ/katɔ̃ŋ/cnrɔs": ("0", None, None),
    "ʔawãʔ, ʔawɛ̃ʔ": ("M1", "M1"),
    "lʔos (grease); bcɔʔ (adj)": ("0", "2"),
    "sup/suk": (None, "0"),
    "tʰi/ti": ("M1", "M1"),
    "ʔahuʔ/ʔisɛ̃d": ("2", None),
    "wɔŋ/kɛn": (None, "1"),
    "skɔʔ; lkɔʔ": (None, "0"),
    "tarek nəhɔm; hɔm [hɔbm]": ("M", "1"),
    "blɑc (slippery); saluc (smooth)": ("0", "0"),
    "pay/mɔh": (None, "0"),
    "heʔ; ja": ("1", None),
    "masə, namaʔ": ("5", None),
    "mreʔ; bilaʔ": ("M", "M"),
    "ji; kɑ": ("2", None),
    "ʔɑy; sac": (None, "0"),
    "jələ̤k, jəlaŋ": ("3", "3"),
    "ɲsəc; ʔay (game)": ("0", None),
    "nsət; ʔuʔɔʔ": ("0", None),
    "ddɛs, dkʰɛs": ("7", "7"),
    "briʔ (CW); biʔ (orang)": ("0", None),
    "yeʔ, kəʔeʔ;": (None, "4"),
    "soʔ; haʔũt (smell rotten)": ("0", None),
    "baləy, səbəʔ": ("2", None),
    "nɛtɛŋ, nata̤̤̤̤̤k": ("M", "M"),
}

def is_loan(x):
    """
    Tests for loan words. 
    These are in cognate set M, M1, M2, or A or L etc
    """
    if x.startswith("M"):
        return True
    elif x in ("A", "L", "P", "T"):
        return True
    return False


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'dunnaslian'

    form_spec = FormSpec(
        brackets={"[": "]", "{": "}", "(": ")"},
        separators=";/,",
        missing_data=('––', '--', '-'),
        strip_inside_brackets=True,
    )
    
    def cmd_makecldf(self, args):
        args.writer.add_sources()

        args.writer.add_languages(id_factory = lambda l: l['ID'].replace("'", ""))

        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split('-')[-1]+ '_' + slug(c.english),
            lookup_factory="Name"
        )
        
        # empty lines do not play well with dicts=True, unfortunately so we do 
        # it the hard way
        header = None
        for row in self.raw_dir.read_csv(DATAFILE, delimiter="\t"):
            if row[0] == '':
                continue  # empty lines
            elif row[0] == 'WORD':
                header = row[1:]  # remove column 1 so it synchronises below
            else:
                assert header is not None, "header should not be empty here!"
                # headers look like this:
                #   WORD	animal		back		bad		belly		big	
                # i.e. have an empty column for cognates.
                # data rows look like this:
                #   Ten'en_Palian	ʔay	0	kaʁɔʔ	0	gbaʔ	3	ʔɛc	0	caw	6
                #   Ten'en_Paborn	bsiŋ	6	kaʁɔʔ	0	baʔ	3	ʔec	0	ʔahaw	7
                # 
                # so we grab the languages in the first cell:
                lang = row.pop(0)
                # and then loop over each pair of columns (gloss, cognate) and join.
                for i in range(0, 10, 2):
                    concept = concepts.get(header[i])
                    value = row[i].strip()

                    # get cognacy
                    cogs = COGNATE_OVERRIDES.get(value, [_.strip() for _ in row[i + 1].split(",")])
                    
                    # skip empty forms
                    if len(value) == 0:
                        continue
                    
                    lex = args.writer.add_forms_from_value(
                        Language_ID=lang.replace("'", ""),
                        Parameter_ID=concept,
                        Value=value,
                        Source="DunnKruspeBurenhult2013",
                        Loan=any([is_loan(c) for c in cogs if c])
                    )
                    
                    # handle cognates
                    if len(lex) == 0:
                        continue  # no lexeme, no cognate
                    
                    for i, cog in enumerate(cogs):
                        if cog is None or len(cog) == 0 or is_loan(cog):
                            # ignore empty cognates and loan words
                            continue
                        else:
                            # if we have one lexeme, multiple cognates then add all the
                            # cognates to lexeme[0]. These are:
                            #   wɔŋ ʔəhɔʔ = 9, 2
                            #   kuʔ cɔʔ = 8, 4
                            #   ɲɛ̤h ko̤h rao = 5, 8
                            #   kəbɘʔ ploʔ = 0,1
                            # ... otherwise we should have one cognate
                            # for each lexeme
                            o = lex[i] if len(lex) == cog else lex[0]
                            args.writer.add_cognate(
                                lexeme=o,
                                Cognateset_ID=concept + "_" + cog,
                                Source="DunnKruspeBurenhult2013"
                            )
