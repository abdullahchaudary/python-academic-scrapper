from pathlib import Path
from tkinter import *
from tkinter import ttk
import tkinter as tk
from bs4 import BeautifulSoup
import requests, lxml, os, json, csv, time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
RESULTS_PATH = OUTPUT_PATH / Path("./results")


headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

proxies = {
  'http': os.getenv('HTTP_PROXY')
}
data_gs = []
data_ma = []
# search_keyword = ' '

def getResults(keyword):
    global search_keyword
    search_keyword = keyword
    ua = UserAgent()
    userAgent = ua.random
    opts = webdriver.ChromeOptions()
    opts.add_argument('--ignore-certificate-errors')
    # opts.add_argument('--incognito')
    # opts.add_argument('--headless')
    # opts.headless =False
    search_keyword = keyword
    opts2 = webdriver.ChromeOptions()
    opts2.add_argument('--ignore-certificate-errors')
    opts2.add_argument(f'user-agent={userAgent}')
    opts2.add_argument('--incognito')
    opts2.add_argument('--headless')
    # opts2.headless =False
    # driver =webdriver.Chrome(ChromeDriverManager().install()
    # s  = HTMLSession()
    driver_ma = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    driver_gs = webdriver.Chrome(ChromeDriverManager().install(), options=opts2)
    url_gs = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + keyword +'&oq='
    url_ma = 'https://academic.microsoft.com/search?q=' + keyword
    # html_gs = requests.get(url_gs, headers=headers, proxies=proxies).text
    driver_gs.get(url_gs)
    driver_ma.get(url_ma)
    time.sleep(10)
    html_gs = driver_gs.page_source
    html_ma = driver_ma.page_source
    # file1 = open("myfile.txt","w",encoding='utf-8')
    # file1.write(html_gs)
    # file1.close()

    soup_gs = BeautifulSoup(html_gs, 'lxml')
    soup_ma = BeautifulSoup(html_ma, 'lxml')
    data_gs.clear()
    data_ma.clear()
    
    # for pdf_link in soup_gs.select('.gs_or_ggsm a'):
    #     pdf_file_link = pdf_link['href']
    #     print(pdf_file_link)

    for result in soup_gs.select('.gs_ri'):
        title = result.select_one('.gs_rt').text
        title_link = result.select_one('.gs_rt a')['href']
        publication_info = result.select_one('.gs_a').text
        snippet = result.select_one('.gs_rs').text
        cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
        related_articles = result.select_one('a:nth-child(4)')['href']
        data_gs.append({
            'title': title,
            'title_link': title_link,
            'publication_info': publication_info,
            'snippet': snippet,
            'cited_by': f'https://scholar.google.com{cited_by}',
            'related_articles': f'https://scholar.google.com{related_articles}',
            # 'all_article_versions': f'https://scholar.google.com{all_article_versions}',
            'data_source': 'Google Scholar'
        })

    for res in soup_ma.select('.primary_paper'):
        if res.select_one('.title span'):
            title = res.select_one('.title span').text
        else:
            title = ' '

        if res.select_one('.title'):
            title_link = res.select_one('.title')['href']
        else:
            title_link = ' '

        if res.select_one('.publication .year'):
            publication_year = res.select_one('.publication .year').text
        else:
            publication_year = ' '

        if res.select_one('.publication .name'):
            publication_name = res.select_one('.publication .name').text
        else:
            publication_name = ' '

        publication_info = publication_year + ' ' + publication_name 
        
        if res.select_one('.publication'):
            publication_link = res.select_one('.publication')['href']
        else:
            publication_link = ' '

        if res.select_one('.ma-expandable-text .text .au-target'):
            snippet = res.select_one('.ma-expandable-text .text .au-target').text
        else:
            snippet = ' '

        if res.select_one('.citations .citation a span'):
            citations = res.select_one('.citations .citation a span').text
        else: 
            citations = ' '

        if res.select_one('.citations .citation a'):
            cited_by = res.select_one('.citations .citation a')['href']
        else: 
            cited_by = ' '

        if res.select_one('.authors'):
            authors = res.select_one('.authors').text
        else:
            authors = ' '

        if res.select_one('.institutions'):
            institutions = res.select_one('.institutions').text
        else:
            institutions = ' '

        if res.select_one('.paper-actions .download'):
            download_link = res.select_one('.paper-actions ma-call-to-action.download')['data-appinsights-download-link']
        else:
            download_link = ' '

        data_ma.append({
            'title': title,
            'title_link': f'https://academic.microsoft.com/{title_link}',
            'publication_info': publication_info,
            'publication_link': f'https://academic.microsoft.com/{publication_link}',
            'snippet': snippet,
            'citations': citations,
            'cited_by': f'https://academic.microsoft.com{cited_by}',
            'authors': authors,
            'institutions': institutions,
            'download_link': download_link,
            # 'related_articles': f'https://scholar.google.com{related_articles}',
            # 'all_article_versions': f'https://scholar.google.com{all_article_versions}',
            'data_source': 'Microsoft Academic'
        })

    try:
        all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
    except:
        all_article_versions = None

    showResults(data_gs, data_ma)
    # print(json.dumps(data_gs, indent = 2, ensure_ascii = False))



def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("1440x1024")
window.configure(bg = "#FFFFFF")
window.title('Python Academic Web Scrapper')

scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1024,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1440.0,
    447.0,
    fill="#0EB7FF",
    outline="")

canvas.create_text(
    337.0,
    81.0,
    anchor="nw",
    text="Academic Web Scrapper",
    fill="#FFFFFF",
    font=("Roboto", 64 * -1),
    width=766.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png")
)
entry_bg_1 = canvas.create_image(
    720.0,
    254.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=435.0,
    y=215.0,
    width=570.0,
    height=76.0
)

canvas.create_text(
    434.0,
    243.0,
    anchor="nw",
    text="Search..",
    fill="#000",
    font=("Roboto", 30 * -1),
    width=210.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: getResults(entry_1.get()),
    relief="flat"
)
button_1.place(
    x=602.0,
    y=331.0,
    width=237.0,
    height=50.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: saveCSV(),
    relief="flat"
)

Lb1 = Listbox(window, height=26, width=150, bg='#F0F0F0',
                activestyle = 'dotbox', 
                font = "Helvetica",
                fg = "#767676",
                borderwidth=0,
                highlightthickness=0)
Lb1.pack(side=tk.BOTTOM)

def showResults(data_gs, data_ma):
    canvas.create_text(
        644.0,
        474.0,
        anchor="nw",
        text="Results",
        fill="#9E9E9E",
        font=("Roboto", 36 * -1),
        width=153.0
    )
    button_2.place(
        x=1180.0,
        y=463.0,
        width=204.0,
        height=56.0
    )
    Lb1.delete(0,tk.END)

    i = 0
    for gs in data_gs:
        Lb1.insert(i+1, "  ")
        Lb1.insert(i+2, "  ")
        Lb1.insert(i+3, "Title:               " + gs['title'])
        Lb1.insert(i+4, "Title Link:          " + gs['title_link'])
        Lb1.insert(i+5, "Publication Info:    " + gs['publication_info'])
        Lb1.insert(i+6, "Snippet:             " + gs['snippet'])
        Lb1.insert(i+7, "Cited By:            " + gs['cited_by'])
        Lb1.insert(i+8, "Related Articles:    " + gs['related_articles'])
        Lb1.insert(i+9, "Source:              " + gs['data_source'])
    
    for ma in data_ma:
        Lb1.insert(i+1, "  ")
        Lb1.insert(i+2, "  ")
        Lb1.insert(i+3, "Title:                     " + ma['title'])
        Lb1.insert(i+4, "Title Link:                " + ma['title_link'])
        Lb1.insert(i+5, "Publication Info:          " + ma['publication_info'])
        Lb1.insert(i+6, "Publication Link:          " + ma['publication_link'])
        Lb1.insert(i+7, "Snippet:                   " + ma['snippet'])
        Lb1.insert(i+8, "Citations:                 " + ma['citations'])
        Lb1.insert(i+9, "Cited By:                  " + ma['cited_by'])
        Lb1.insert(i+10, "Authors:                  " + ma['authors'])
        Lb1.insert(i+11, "Institutions:             " + ma['institutions'])
        Lb1.insert(i+12, "Download Link:            " + ma['download_link'])
        Lb1.insert(i+13, "Source:                   " + ma['data_source'])

def saveCSV():
    timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = 'results/' + timestr + '_' + search_keyword + '_data.csv'
    try:
        with open(filename, 'w', newline = '\n', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter = ',')
            writer.writerow(["Academic Data Web Scraper"])
            writer.writerow(' ')
            writer.writerow(' ')
            writer.writerow(["Google Scholar Data"])
            writer.writerow(["Title", "Title Link", "Publication Info", "Snippet", "Cited By", "Related Articles", "Data Source"])

            for d1 in data_gs:
                writer.writerow(' ')
                writer.writerow([d1['title'], d1['title_link'], d1['publication_info'], d1['snippet'], d1['cited_by'], d1['related_articles'], d1['data_source']])

            writer.writerow(' ')
            writer.writerow(' ')
            writer.writerow(["Microsoft Academic Data"])
            writer.writerow(["Title", "Title Link", "Publication Info", "Publication Link", "Snippet", "Citations", "Cited By", "Authors", "Institutions", "Download Link", "Data Source"])
            
            for d2 in data_ma:
                writer.writerow(' ')
                writer.writerow([d2['title'], d2['title_link'], d2['publication_info'], d2['publication_link'], d2['snippet'], d2['citations'], d2['cited_by'], d2['authors'], d2['institutions'], d2['download_link'], d2['data_source']])

            messaage = 'Data has been saved successfully in \n' + filename

    except BaseException as e:
        print('BaseException:', filename)
    else:
        popupmsg(messaage)
        print('Data has been loaded successfully !')


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Data Saved!")
    label = ttk.Label(popup, text=msg, font=("Roboto", 24 * -1))
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

window.resizable(False, False)
window.mainloop()

