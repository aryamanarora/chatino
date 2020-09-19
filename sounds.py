import pywikibot, re

site = pywikibot.Site(code='en', fam='wiktionary')
site.login()

pattern = re.compile(r'''==San Juan Quiahije Chatino==

===Alternative forms===
.*
.*

''')

with open('uploads.txt', 'r') as file:
    count = 0
    for line in file:
        name = line.strip('\n')
        pagename = re.split('-|—', name)[1]
        page = pywikibot.Page(site, pagename)
        if page.exists():
            match = pattern.search(page.text)
            if match:
                count += 1
                page.text = page.text[:match.span()[1]] + f'''===Pronunciation===
* {{{{audio|ctp-san|{name}|Audio (San Juan Quiahije)}}}}

''' + page.text[match.span()[1]:]
                page.save("Add San Juan Quiahije Chatino pronunciation")
            else:
                print(name)
        else:
            print(name)
        print(count)