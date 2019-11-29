# Words were sought corresponding to 146 basic meanings using a regionally
# adapted Swadesh-type list. Malay loanwords were excluded (112 instances of
# borrowing from 55 distinct Malay source words); chance resemblances were
# excluded where they could be identified. The database contained 984 distinct
# Aslian cognate sets. The cognate candidates were identified according to
# explicit criteria, devised according to language-family specific knowledge of
# general patterns of language change in the Aslian family. The primary
# criterion is place of articulation of onset and coda for the final syllable; a
# fuller account of these principles and their exceptions is given in Dunn et
# al. (2011: 300).



def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_languages(cldf_dataset):
    f = [f for f in cldf_dataset["LanguageTable"] if f["ID"] == "Tenen_Paborn"]
    assert len(f) == 1
    assert f[0]["Name"] == "Tenen Paborn"
    assert f[0]["Glottocode"] == "tong1308"
    assert f[0]["ISO639P3code"] == "tnz"


def test_parameters(cldf_dataset):
    assert len([f for f in cldf_dataset["ParameterTable"]]) == 146


def test_forms(cldf_dataset):
    # check one specific form to make sure columns, values are correct.
    # Semaq_Beri_Berua	jlaŋ	3	ci	0	ʔipəʔ	3	balɑʔ	2	ɲsəc; ʔay (game)	0
    f = [f for f in cldf_dataset["FormTable"] if f["Value"] == "ɲsəc; ʔay (game)"]
    assert len(f) == 2
    assert f[0]["Language_ID"] == "Semaq_Beri_Berua"
    assert f[1]["Language_ID"] == "Semaq_Beri_Berua"

    assert f[0]["Parameter_ID"] == "65_meat"
    assert f[1]["Parameter_ID"] == "65_meat"

    assert f[0]["Form"] in ("ɲsəc", "ʔay")
    assert f[1]["Form"] in ("ɲsəc", "ʔay")


def test_cognates(cldf_dataset):
    allcogs = set(c['Cognateset_ID'] for c in cldf_dataset['CognateTable'])
    # we get 980 cognate sets not 984 as they say in the paper. 
    assert len(allcogs) == 980


def test_who_cognates(cldf_dataset):
    # test all entries for `who`. This contains a nice mix of things that are overridden
    # in the import script, some languages with no cognates, and some cognates that are
    # "A, B".
    cogs = [
        c for c in cldf_dataset['CognateTable'] if c['Cognateset_ID'].startswith('139_who_')
    ]
    # Jahai_Banun    makɛn    0
    # Jahai_Rual    makɛn    0
    # Menriq_Lah    makɛn    0
    # Menriq_Rual    makɛn    0
    # Batek_Teh_Lebir    nakɛn    0
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_0']) == 5
    
    # Batek_Teh_Taku    ʔalɘw    1
    # Batek_Teq    batɛk ləw    1
    # Batek_Deq_Terengganu    ʔoləw     1
    # Batek_Deq_Koh    ʔoʔ lɘw    1
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_1']) == 4
    
    # Ceq_Wong    biʔ ʔay    2
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_2']) == 1

    # Semnam_Bal    diːʔ    3
    # Semnam_Malau    diːʔ    3
    # Semelai    kadeh    3
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_3']) == 3

    # Temiar_Kelantan    cɔːʔ    4
    # Temiar_Perak    cɔ:ʔ    4
    # Maniq    kuʔ cɔʔ    8, 4   # Note this should be in 4 and 8
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_4']) == 3

    # Jah_Hut    ɲah    5
    # Mon    ɲɛ̤h ko̤h rao    5, 8   # Note this should be in 5 and 8
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_5']) == 2

    # Mah_Meri    humaʔ    6
    # Kammu    mə    6
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_6']) == 2

    # Semai_Ringlet    boːʔ    7
    # Semai_Kampar    bɔːʔ    7
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_7']) == 2

    # Maniq    kuʔ cɔʔ    8, 4   # Note this should be in 4 and 8
    # Mon    ɲɛ̤h ko̤h rao    5, 8   # Note this should be in 5 and 8
    # Kensiw_Perak    tom mniʔ    8
    # Kensiw_Kedah    tom mniʔ    8
    # Kintaq    tom mniʔ    8
    # Semaq_Beri_Berua    ʔiŋkɔʔ    8
    # Semaq_Beri_Jaboy    ʔŋkɔʔ    8
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_8']) == 7

    # Ten'en_Palian    ʔeʔ klɨɲ    9
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_9']) == 1

    # Khmer_Surin    ʔaraː    10
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_10']) == 1

    # Khmer_Siem_Reap    nonaː    11
    assert len([c for c in cogs if c['Cognateset_ID'] == '139_who_11']) == 1

    # Ten'en_Paborn
    # Lanoh_Kertei
    assert len([c for c in cogs if c['ID'].startswith("Tenen_Paborn")]) == 0
    assert len([c for c in cogs if c['ID'].startswith("Lanoh_Kertei")]) == 0



def test_sources(cldf_dataset):
    assert len(cldf_dataset.sources) == 1
