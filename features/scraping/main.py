from extractor import GFG, TTP ,JTP
from scraper import ArticleParser


GFG_prefix = ''
GFG_src = "https://www.geeksforgeeks.org/operating-systems/"

TTP_prefix = "https://www.tutorialspoint.com/"
TTP_src = "https://www.tutorialspoint.com/operating_system/index.htm"

JTP_prefix = "https://www.javatpoint.com/"
JTP_src = "https://www.javatpoint.com/os-tutorial"

links = []


links.extend(GFG(GFG_src, GFG_prefix).scrape())
links.extend(TTP(TTP_src, TTP_prefix).scrape())
links.extend(JTP(JTP_src, JTP_prefix).scrape())


ap = ArticleParser(urls= links, filename='os_comp.txt')

ap.buildTextFile()