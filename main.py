from bs4 import BeautifulSoup
import requests
import random


required_link = "/wiki/Adolf_Hitler"
ignored_prefixes = [
    "/wiki/Main_Page",
    "/wiki/Help:",  # Matches all help pages starting with "Help:"
    "/w/index.php",  # Common link for various special pages
	"/wiki/Special:",  # Matches all special pages
	"/wiki/File:",  # Matches all file pages
	"/wiki/Template:",  # Matches all template pages
	"/wiki/Category:",  # Matches all category pages
	"/wiki/Portal:",  # Matches all portal pages
	"/wiki/Book:",  # Matches all book pages
	"/wiki/Module:",  # Matches all module pages
	"/wiki/Talk:",  # Matches all talk pages
	"/wiki/User:",  # Matches all user pages
	"/wiki/Wikipedia:",  # Matches all Wikipedia pages
]
helping_words = [
	"World_War_II",
	"Holocaust",
	"Germany",
	"Dictator",
	"Dictatorship",
	"Nazi Germany",
	"National Socialism",
	"Europe",
	"History",
]
n = 7


def find_link(page, n, path=None, visited=None):
	if path == None:
		path = page.url
	else:
		path = path + " + " + page.url
	if visited == None:
		visited = set()
	if n == 0:
		print("Hitler not found")
		return
	print(page.url)
	visited.add(page.url)
	soup = BeautifulSoup(page.text, 'html.parser')
	links = soup.find_all('a', href=lambda href: href and href.startswith('/wiki/'))
	links = [link for link in links if not any(link.get('href').startswith(prefix) for prefix in ignored_prefixes)]
	links = [link for link in links if not 'mw-disambig' in link.get('class', [])]

	for link in links:
		if link.get('href') == required_link:
			path = path + " + " + "https://en.wikipedia.org" + required_link
			print("We found the link!\nThe path is: " + path)
			return
	for link in links:
		url = "https://en.wikipedia.org" + link.get('href')
		if url not in visited and any(word in link.get('href') for word in helping_words):
			visited.add(url)
			find_link(requests.get(url), n - 1, path, visited)
			return
	while (links):
		link = random.choice(links)
		url = "https://en.wikipedia.org" + link.get('href')
		if url not in visited:
			visited.add(url)
			find_link(requests.get(url), n - 1, path, visited)
			return
		links.remove(link)

while True:
	user_url = requests.get(input("Enter the name of the page you want to scrape: "))
	find_link(user_url, n)
	if input("Do you want to continue? (y/n) ").lower() != "y":
		break
