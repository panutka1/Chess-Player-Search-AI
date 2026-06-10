import fitz

def read_pdf(path):
    doc = fitz.open(path)
    all_pages = []
    i = 1
    for page in doc:
        text = page.get_text()
        i+=1
        all_pages.append(text)
    return "\n".join(all_pages)
        
path = "players_info.pdf"
readed_pdf = read_pdf(path)
#print((readed_pdf)[0])