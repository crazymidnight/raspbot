from bs4 import BeautifulSoup
import requests

WINDOW_TEXT = 'В это время окно'

def get_html(group):

    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
          }
    url = f'http://rasp.tpu.ru/view.php?for={group}&aslist=0'  # url для второй страницы
    r = requests.get(url, headers=headers)

    return r.text


def scrape_today(group):

    rasp = get_html(group=group)

    soup = BeautifulSoup(rasp, "html.parser")
    # print(soup.body.prettify())
    # print(soup.body.find)
    table = soup.body.find('table', {'class': 'c-table schedule'})

    subjects = table.findAll('div', {'class': 'subject'})
    times = table.findAll('div', {'class': 'lesson-type'})
    rooms = table.findAll('div', {'class': 'room'})
    teachers = table.findAll('div', {'class': 'group-teacher'})
    current_day = table.findAll('td', {'class': 'current-day'})

    today_subjects = []

    for i in current_day:

        if len(i.text) < 3:
            today_subjects.append(WINDOW_TEXT)

        else:
            today_subjects.append(i.text)

    return today_subjects
