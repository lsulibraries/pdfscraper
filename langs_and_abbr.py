#! /usr/bin/env python

langs_and_abbr = {
    'Vai': 'vai', 'kho\xc3\xafsan': 'khi', 'Palauan': 'pau', 'Official Aramaic (700-300 BCE); Imperial Aramaic (700-300 BCE)': 'arc', 'sino-tib\xc3\xa9taines': 'sit', 'Niuean': 'niu', 'Fanti': 'fat', 'Masai': 'mas', 'Bambara': 'bam', 'Sindhi': 'snd', 'Adyghe; Adygei': 'ady', 'Santali': 'sat', 'Duala': 'dua', 'romanes': 'roa', 'Votic': 'vot', 'Karachay-Balkar': 'krc', 'Tsonga': 'tso', 'Kanuri': 'kau', 'Umbundu': 'umb', 'artificielles': 'art', 'Komi': 'kom', 'Hiligaynon': 'hil', 'Nyamwezi': 'nym', 'Pangasinan': 'pag', ' North; North Ndebele': 'nde', 'philippines': 'phi', 'Pohnpeian': 'pon', 'songhai': 'son', 'Pushto; Pashto': 'pus', 'Yiddish': 'yid', 'Ga': 'gaa', 'Blin; Bilin': 'byn', 'Mossi': 'mos', 'Southern Sami': 'sma', 'Kawi': 'kaw', 'Konkani': 'kok', 'Nauru': 'nau', 'Sasak': 'sas', 'Latin': 'lat', 'Zulu': 'zul', 'Georgian': 'geo', 'Tigrinya': 'tir', 'Tibetan': 'tib', 'Central Khmer': 'khm', 'Ingush': 'inh', 'Dzongkha': 'dzo', 'Guarani': 'grn', 'Sidamo': 'sid', ' Ottoman (1500-1928)': 'ota', 'Kurukh': 'kru', 'Herero': 'her', 'Latvian': 'lav', 'English': 'eng', 'afro-asiatiques': 'afa', 'Tumbuka': 'tum', 'Croatian': 'hrv', 'Chinese': 'chi', 'Swiss German; Alemannic; Alsatian': 'gsw', 'Inuktitut': 'iku', 'Tatar': 'tat', 'Pali': 'pli', 'Yapese': 'yap', 'Arabic': 'ara', 'Venda': 'ven', 'perse': 'peo', 'Erzya': 'myv', 'nilo-sahariennes': 'ssa', ' Middle (1100-1500)': 'enm', 'Oriya': 'ori', ' Southern': 'sot', 'Inupiaq': 'ipk', 'Lojban': 'jbo', 'Hindi': 'hin', 'Ewondo': 'ewo', 'Eastern Frisian': 'frs', 'Tonga (Nyasa)': 'tog', 'Hungarian': 'hun', 'Wolof': 'wol', 'Bosnian': 'bos', 'Vietnamese': 'vie', 'Sinhala; Sinhalese': 'sin', 'Afrihili': 'afh', 'Manchu': 'mnc', 'Russian': 'rus', 'Romany': 'rom', 'Gbaya': 'gba', 'Luo (Kenya and Tanzania)': 'luo', 'Tiv': 'tiv', 'Undetermined': 'und', 'Hiri Motu': 'hmo', 'Basa': 'bas', 'Braj': 'bra', 'iraniennes': 'ira', 'Mirandese': 'mwl', 'German': 'ger', 'Khotanese; Sakan': 'kho', 'indo-europ\xc3\xa9ennes': 'ine', 'Lezghian': 'lez', 'Basque': 'baq', 'chinook': 'chn', 'Dutch; Flemish': 'dut', 'Mandar': 'mdr', 'Sranan Tongo': 'srn', 'nahuatl': 'nah', 'Chechen': 'che', 'Nzima': 'nzi', 'Northern Sami': 'sme', 'Sanskrit': 'san', 'Ekajuk': 'eka', 'Grebo': 'grb', 'tai': 'tai', 'Reserved for local use': 'qaa-qtz', 'Welsh': 'wel', 'yupik': 'ypk', 'Gondi': 'gon', 'Bashkir': 'bak', 'Kamba': 'kam', 'caucasiennes': 'cau', 'Skolt Sami': 'sms', 'sioux': 'sio', 'nord-am\xc3\xa9rindiennes': 'nai', 'batak': 'btk', 'Japanese': 'jpn', 'Kinyarwanda': 'kin', 'sorabes': 'wen', 'Hebrew': 'heb', 'Esperanto': 'epo', 'Telugu': 'tel', 'Uighur; Uyghur': 'uig', 'Chichewa; Chewa; Nyanja': 'nya', 'berb\xc3\xa8res': 'ber', "Gwich'in": 'gwi', 'Bini; Edo': 'bin', 'Tamil': 'tam', "Mi'kmaq; Micmac": 'mic', 'dravidiennes': 'dra', 'Haitian; Haitian Creole': 'hat', 'Kachin; Jingpho': 'kac', 'Spanish; Castilian': 'spa', ' Old (to 900)': 'sga', 'Lamba': 'lam', 's\xc3\xa9mitiques': 'sem', 'Galician': 'glg', 'Upper Sorbian': 'hsb', 'Madurese': 'mad', 'Kimbundu': 'kmb', 'Khasi': 'kha', 'Mandingo': 'man', 'Marshallese': 'mah', 'Kuanyama; Kwanyama': 'kua', 'Marathi': 'mar', 'Slovenian': 'slv', 'Azerbaijani': 'aze', 'Klingon; tlhIngan-Hol': 'tlh', 'Elamite': 'elx', 'indo-aryennes': 'inc', 'Makasar': 'mak', 'Kalmyk; Oirat': 'xal', 'Norwegian': 'nor', 'Ganda': 'lug', 'No linguistic content; Not applicable': 'zxx', 'Lahnda': 'lah', 'Aragonese': 'arg', 'Hittite': 'hit', 'Turkmen': 'tuk', 'Ido': 'ido', 'Sukuma': 'suk', 'Urdu': 'urd', 'Kazakh': 'kaz', 'Bihari languages': 'bih', 'Chipewyan; Dene Suline': 'chp', 'Rarotongan; Cook Islands Maori': 'rar', 'Tokelau': 'tkl', 'Kabyle': 'kab', 'finno-ougriennes': 'fiu', 'Gothic': 'got', 'bantoues': 'bnt', ' Norwegian; Norwegian Bokm\xc3\xa5l': 'nob', 'Tamashek': 'tmh', 'Pedi; Sepedi; Northern Sotho': 'nso', 'Kara-Kalpak': 'kaa', 'Swahili': 'swa', 'Samaritan Aramaic': 'sam', 'Cherokee': 'chr', 'Yao': 'yao', 'iroquoises': 'iro', 'athapascanes': 'ath', 'Magahi': 'mag', 'Pampanga; Kapampangan': 'pam', 'Malagasy': 'mlg', 'Tlingit': 'tli', ' Old (to 1500)': 'pro', 'Maori': 'mao', 'Zhuang; Chuang': 'zha', 'Igbo': 'ibo', 'Ladino': 'lad', 'Kirghiz; Kyrgyz': 'kir', 'germaniques': 'gem', 'Serer': 'srr', 'Phoenician': 'phn', 'Selkup': 'sel', 'Baluchi': 'bal', ' Old (842-ca.1400)': 'fro', 'Rajasthani': 'raj', ' Middle (ca.1400-1600)': 'frm', 'Hausa': 'hau', 'wakashanes': 'wak', 'nig\xc3\xa9ro-kordofaniennes': 'nic', 'Nias': 'nia', 'Kumyk': 'kum', 'Avaric': 'ava', 'Chuukese': 'chk', ' Modern (1453-)': 'gre', 'Romanian; Moldavian; Moldovan': 'rum', 'Maithili': 'mai', 'Aromanian; Arumanian; Macedo-Romanian': 'rup', 'Swati': 'ssw', ' South; South Ndebele': 'nbl', 'algonquines': 'alg', 'Balinese': 'ban', 'Dogri': 'doi', 'Ukrainian': 'ukr', 'Tuvinian': 'tyv', ' Portuguese-based ': 'cpp', 'Multiple languages': 'mul', 'Maltese': 'mlt', 'Sichuan Yi; Nuosu': 'iii', 'Assamese': 'asm', 'Tswana': 'tsn', 'Coptic': 'cop', 'Beja; Bedawiyet': 'bej', 'baltes': 'bat', 'Portuguese': 'por', 'Achinese': 'ace', 'Tereno': 'ter', 'Occitan (post 1500); Proven\xc3\xa7al': 'oci', 'Avestan': 'ave', 'austron\xc3\xa9siennes': 'map', 'slaves': 'sla', 'Minangkabau': 'min', ' French-based ': 'cpf', 'Uncoded languages': 'mis', 'Limburgan; Limburger; Limburgish': 'lim', 'Asturian; Bable; Leonese; Asturleonese': 'ast', 'Panjabi; Punjabi': 'pan', 'Cornish': 'cor', 'Bulgarian': 'bul', 'Moksha': 'mdf', 'couchitiques': 'cus', 'Yoruba': 'yor', 'Arawak': 'arw', 'Nyankole': 'nyn', 'French': 'fre', 'Karelian': 'krl', 'Bengali': 'ben', 'Angika': 'anp', ' English based': 'cpe', 'Zaza; Dimili; Dimli; Kirdki; Kirmanjki; Zazaki': 'zza', ' Old (ca.450-1100)': 'ang', 'Ossetian; Ossetic': 'oss', 'Nepali': 'nep', 'Finnish': 'fin', 'Sundanese': 'sun', 'Albanian': 'alb', 'Irish': 'gle', 'otomi': 'oto', 'Tagalog': 'tgl', 'Serbian': 'srp', 'Italian': 'ita', 'Luiseno': 'lui', 'Chibcha': 'chb', 'Walloon': 'wln', 'Chamorro': 'cha', 'Luba-Lulua': 'lua', 'Amharic': 'amh', 'Inari Sami': 'smn', 'Tajik': 'tgk', 'Rapanui': 'rap', 'Tonga (Tonga Islands)': 'ton', 'Lozi': 'loz', 'Gorontalo': 'gor', 'Chagatai': 'chg', 'Volap\xc3\xbck': 'vol', 'Waray': 'war', 'Gaelic; Scottish Gaelic': 'gla', 'Kutenai': 'kut', 'Fulah': 'ful', 'Buginese': 'bug', 'Cheyenne': 'chy', 'Fon': 'fon', 'Awadhi': 'awa', 'Cree': 'cre', 'Indonesian': 'ind', 'Hawaiian': 'haw', 'Adangme': 'ada', 'Thai': 'tha', 'Afrikaans': 'afr', ' Middle (900-1200)': 'mga', 'Ugaritic': 'uga', 'Uzbek': 'uzb', 'Zenaga': 'zen', 'Burmese': 'bur', 'Divehi; Dhivehi; Maldivian': 'div', 'Aleut': 'ale', 'Egyptian (Ancient)': 'egy', ' Middle (ca.1050-1350)': 'dum', 'Lingala': 'lin', 'Lunda': 'lun', 'Galibi Carib': 'car', 'Friulian': 'fur', 'Nyoro': 'nyo', 'Breton': 'bre', 'papoues': 'paa', 'Turkish': 'tur', 'Kalaallisut; Greenlandic': 'kal', 'Delaware': 'del', 'bamil\xc3\xa9k\xc3\xa9': 'bai', 'karen': 'kar', 'Zapotec': 'zap', 'Chuvash': 'chv', 'Blissymbols; Blissymbolics; Bliss': 'zbl', 'Lithuanian': 'lit', 'Malay': 'may', "N'Ko": 'nqo', 'Zuni': 'zun', 'Iban': 'iba', "am\xc3\xa9rindiennes de L'Am\xc3\xa9rique centrale": 'cai', 'Mapudungun; Mapuche': 'arn', 'Cebuano': 'ceb', 'Armenian': 'arm', 'Mohawk': 'moh', 'Dogrib': 'dgr', 'Standard Moroccan Tamazight': 'zgh', 'Romansh': 'roh', 'Sandawe': 'sad', 'Tok Pisin': 'tpi', 'Javanese': 'jav', 'Kannada': 'kan', 'Persian': 'per', 'Mongolian': 'mon', 'Choctaw': 'cho', 'norv\xc3\xa9gien nynorsk; nynorsk': 'nno', 'Aymara': 'aym', 'Shona': 'sna', 'Western Frisian': 'fry', 'Corsican': 'cos', 'Kpelle': 'kpe', 'Somali': 'som', 'Arapaho': 'arp', 'Judeo-Persian': 'jpr', 'Akan': 'aka', 'Lushai': 'lus', 'Syriac': 'syr', 'Sign Languages': 'sgn', 'Tahitian': 'tah', 'Siksika': 'bla', 'Dargwa': 'dar', 'Sogdian': 'sog', 'Gayo': 'gay', 'norrois': 'non', 'Sango': 'sag', 'Judeo-Arabic': 'jrb', 'Oromo': 'orm', ' bas; saxon': 'nds', 'dayak': 'day', 'Neapolitan': 'nap', 'Bemba': 'bem', 'Quechua': 'que', 'Lower Sorbian': 'dsb', 'Estonian': 'est', 'Fang': 'fan', 'krou': 'kro', 'zand\xc3\xa9': 'znd', 'Dinka': 'din', 'Himachali languages; Western Pahari languages': 'him', 'Fijian': 'fij', 'Iloko': 'ilo', 'Samoan': 'smo', 'maya': 'myn', 'Manx': 'glv', 'Soninke': 'snk', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic': 'chu', 'manobo': 'mno', 'Dyula': 'dyu', 'Kosraean': 'kos', 'Malayalam': 'mal', 'Efik': 'efi', 'mounda': 'mun', 'banda': 'bad', 'Creek': 'mus', 'Mongo': 'lol', 'Lule Sami': 'smj', 'Filipino; Pilipino': 'fil', 'Bislama': 'bis', 'Kongo': 'kon', 'Catalan; Valencian': 'cat', 'apaches': 'apa', 'Acoli': 'ach', 'Timne': 'tem', 'Papiamento': 'pap', 'Marwari': 'mwr', 'Dakota': 'dak', 'chames': 'cmc', 'Bikol': 'bik', 'Swedish': 'swe', 'Ainu': 'ain', 'alta\xc3\xafques': 'tut', ' Ancient (to 1453)': 'grc', 'Mari': 'chm', 'Ewe': 'ewe', 'Faroese': 'fao', 'ijo': 'ijo', 'Danish': 'dan', 'nubiennes': 'nub', 'm\xc3\xb4n-khmer': 'mkh', 'Tetum': 'tet', 'Pahlavi': 'pal', 'Slovak': 'slo', 'Gilbertese': 'gil', 'Tigre': 'tig', ' langues; celtes': 'cel', 'Polish': 'pol', 'Interlingue; Occidental': 'ile', "indiennes d'Am\xc3\xa9rique du Sud": 'sai', 'Bhojpuri': 'bho', 'Tsimshian': 'tsi', 'Nogai': 'nog', 'Yakut': 'sah', 'Sumerian': 'sux', 'Xhosa': 'xho', 'Manipuri': 'mni', 'Buriat': 'bua', 'Kikuyu; Gikuyu': 'kik', 'Hupa': 'hup', 'Interlingua (International Auxiliary Language Association)': 'ina', 'Icelandic': 'ice', 'sames': 'smi', 'Twi': 'twi', 'Luxembourgish; Letzeburgesch': 'ltz', 'Gujarati': 'guj', 'Akkadian': 'akk', 'Kashubian': 'csb', 'Korean': 'kor', 'Shan': 'shn', 'allemand': 'goh', 'Northern Frisian': 'frr', 'Caddo': 'cad', 'Kashmiri': 'kas', 'Haida': 'hai', 'tupi': 'tup', 'salishennes': 'sal', 'Afar': 'aar', 'Udmurt': 'udm', 'Osage': 'osa', 'Sicilian': 'scn', 'Czech': 'cze', 'Creoles and pidgins ': 'crp', 'Kabardian': 'kbd', 'Belarusian': 'bel', 'Macedonian': 'mac', 'australiennes': 'aus', 'Tuvalu': 'tvl', 'Classical Newari; Old Newari; Classical Nepal Bhasa': 'nwc', 'Sardinian': 'srd', 'Lao': 'lao', 'Slave (Athapascan)': 'den', 'Nepal Bhasa; Newari': 'new', 'Mende': 'men', 'Ojibwa': 'oji', 'Kurdish': 'kur', 'Classical Syriac': 'syc', 'Walamo': 'wal', 'Geez': 'gez', 'Luba-Katanga': 'lub', 'Navajo; Navaho': 'nav', 'Crimean Tatar; Crimean Turkish': 'crh', 'Rundi': 'run', 'Abkhazian': 'abk', 'Southern Altai': 'alt', 'Ndonga': 'ndo', 'Hmong; Mong': 'hmn', 'Scots': 'sco', 'Susu': 'sus', 'Washo': 'was', 'pr\xc3\xa2krit': 'pra'
}


def get_langs_and_abbr():
    lowercase_and_unicode_lang_and_abbr = dict()
    for key, value in langs_and_abbr.iteritems():
        lowercase_and_unicode_lang_and_abbr[key.lower().decode('utf-8')] = value.lower().decode('utf-8')
    return lowercase_and_unicode_lang_and_abbr
