import scraper

resp = scraper.check_scraper()

if resp:
    print("The scraper works for you")
else:
    print("Sorry but the scraper doesnt work for you")