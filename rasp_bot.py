from scrapper import scrapper


group = '8е41'

today = scrapper.scrape_today(group=group)

for i in today:
    print(i)




