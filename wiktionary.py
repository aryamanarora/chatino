import pywikibot, csv

site = pywikibot.Site(code='en', fam='wiktionary')
site.login()

with open('data.csv', 'r') as fin:
    reader = csv.reader(fin)
    header = ['CPL', 'PROG', 'HAB', 'POT']
    cur = {}
    for i, data in enumerate(reader):
        print(data)
        if i < 4: continue
        if data[2] == 'CPL': continue
        if data[0]:
            if data[0][0] == '[':
                cur['class'] = data[0][1]
                cur['word'] = data[1]
                cur['gloss'] = data[2]
                cur['transitivity'] = ''
                if 'iv' in data[3]: cur['transitivity'] += 'i'
                if 'tv' in data[3]: cur['transitivity'] += 't'
                cur['paradigm'] = []
        elif cur and data[1]:
            cur['paradigm'].extend(data[2:6])
        if data[1] == '3;PL':
            entry = f"""==Western Highland Chatino==

===Verb===
{{{{ctp-verb|{cur['word']}|class={cur['class']}|t={cur['transitivity']}}}}}

# {cur['gloss']}

====Conjugation====
{{{{ctp-conj|class={cur['class']}|{'|'.join(cur['paradigm'])}}}}}

===References===
* {{{{R:ctp:Cruz, et al. 2020}}}}
            """

            page = pywikibot.Page(site, 'User:AryamanA/' + cur['word'])
            page.text = entry
            page.save('Western Highland Chatino verb with inflection from file')

