import pywikibot, csv
import stanza

site = pywikibot.Site(code='en', fam='wiktionary')
site.login()

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')

tones_to_letters = {
    'MS': 'H',
    'MH': 'I',
    'ML': 'J',
    'HL': 'B',
    'HS': 'D',
    'LS': 'M',
    'LH': 'G',
    'LM': 'F',
    'H': 'E',
    'M': 'C',
    'L': 'A'
}

tones_to_numbers = {
    'LS': '40',
    'LH': '42',
    'LM': '3',
    'MS': '20',
    'MH': '32',
    'ML': '24',
    'HS': '10',
    'HL': '14',
    'H': '1',
    'M': '2',
    'L': '4'
}

edits = 0
with open('new corpus.csv', 'r') as fin:
    reader = csv.reader(fin)
    header = ['CPL', 'PROG', 'HAB', 'POT']
    cur = {}
    for i, data in enumerate(reader):
        if i < 3: continue
        print(data)
        if data[0]:
            if data[0][0] == '[':
                # class and headword
                cur['class'] = data[0][1:-1]
                cur['word'] = data[1]

                # altforms (using stupid find-replace)
                cur['altnums'] = cur['word']
                for key, val in tones_to_numbers.items():
                    cur['altnums'] = cur['altnums'].replace(key, val)
                cur['altletters'] = cur['word']
                for key, val in tones_to_letters.items():
                    cur['altletters'] = cur['altletters'].replace(key, val)

                # other pertinent information
                cur['gloss'] = data[2]
                words = nlp(cur['gloss']).sentences[0].words
                cur['gloss'] = ' '.join([f'[[{word.lemma}|{word.text}]]' for word in words])
                print(cur['gloss'])
                # cur['transitivity'] = ''
                # if 'iv' in data[3]: cur['transitivity'] += 'i'
                # if 'tv' in data[3]: cur['transitivity'] += 't'
                cur['paradigm'] = []
                for cell in data[4:8]:
                    cur['paradigm'].extend([word.strip() for word in cell.split('\n')])

                page = pywikibot.Page(site, cur['word'])
                if '==San Juan Quiahije Chatino==' in page.text:

                    match_text = f"""===References===
* {{{{R:ctp-san:Cruz, et al. 2020}}}}"""
                    pos = page.text.find(match_text)
                    entry = f"""===Verb===
{{{{ctp-san-verb|{cur['word']}|class={cur['class']}}}}}

# {cur['gloss']}

====Conjugation====
{{{{ctp-san-conj|class={cur['class']}|{'|'.join(cur['paradigm'])}}}}}

"""
                    if entry not in page.text:
                        page.text = page.text[:pos] + entry + page.text[pos:]
                        page.save('San Juan Quiahije Chatino verb with inflection from file--existing lang section')
                    edits += 1
                else:
                    entry = f"""
==San Juan Quiahije Chatino==

===Alternative forms===
* {{{{alter|ctp-san|{cur['altnums']}||numeral tones}}}}
* {{{{alter|ctp-san|{cur['altletters']}||alphabetic tones}}}}

===Verb===
{{{{ctp-san-verb|{cur['word']}|class={cur['class']}}}}}

# {cur['gloss']}

====Conjugation====
{{{{ctp-san-conj|class={cur['class']}|{'|'.join(cur['paradigm'])}}}}}

===References===
* {{{{R:ctp-san:Cruz, et al. 2020}}}}
                """
                    if entry not in page.text:
                        page.text = page.text[:pos] + entry + page.text[pos:]
                        page.save('San Juan Quije Chatino verb with inflection from file')
                    edits += 1
                print(edits)

