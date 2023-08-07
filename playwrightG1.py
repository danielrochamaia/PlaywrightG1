from playwright.sync_api import sync_playwright

subject = "Lula"
pageNumber = 1
maximumPages = 2

def getPortalAndTime(info):
        info = info.replace("\n", "").strip().replace("    ","").split("•")
        portal = info[0]
        time = info[1]
        return portal, time

def getContent(className):
    try:
        return element.query_selector(f'.{className}').text_content()
    except Exception:
        return None

with open('dados.txt', 'w') as file:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        while pageNumber <= maximumPages:
            file.write(f"[PÁGINA {pageNumber}]\n\n")
            page.goto(f"https://g1.globo.com/busca/?q={subject}&page={pageNumber}&ajax=1")
            elements = page.query_selector('.results__list').query_selector_all('.widget')

            if elements:
                for element in elements:
                    info = getContent("widget--info__meta--card")
                    title = getContent("widget--info__title")

                    if(info != None):
                        portal, time = getPortalAndTime(info)
                        file.write(f"PORTAL: {portal}\n")
                        file.write(f"DATA: {time}\n")
                    
                    if(title != None):
                        title = title.replace("\n","").replace("  ","")
                        file.write(f"TÍTULO: {title}\n")

                    if(info != None or title != None):
                        file.write(f"LINK: {element.query_selector('a').get_attribute('href')}\n\n")
                
            pageNumber += 1

        browser.close()