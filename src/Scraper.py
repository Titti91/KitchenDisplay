#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import requests
import re
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from Recipe import Recipe
#Scraper

##Recipe object


class Scraper:
    def __init__(self):
        self.myRecipe = Recipe()

    #def scrapeRewe(url):
        #session = HTMLSession()
        #resp = session.get("https://www.rewe.de/rezepte/ostertorte-moehrenbeet/")
        #resp.html.render()
        #html = BeautifulSoup(resp.html.html, "lxml")
        #title = html.find('h1').text
        #print(title)
        #headers = {
        #    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        # ua = UserAgent()
        # hdr = {'User-Agent': ua.random,
        #       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        #       'Accept-Encoding': 'none',
        #       'Accept-Language': 'en-US,en;q=0.8',
        #       'Connection': 'keep-alive'}

        #driver = webdriver.Firefox()
        #driver.get(url)
        #recource = driver.page_source
        # response = requests.get(url, headers=hdr)
        #html = BeautifulSoup(recource, 'html.parser')
        #title = html.find('h1').text
        #print(title)
        #myRecipe.name = title
        #times_html = html.find('small', class_="ds-recipe-meta rds-recipe-meta")
        #ingredients_html = html.find_all('table', class_="ingredients")
        #recipe = html.select_one('article:has(>h2:-soup-contains("Zubereitung")) > .ds-box').text.lstrip().splitlines()
        #recipe = list(filter(lambda a: a != '', recipe))
        #myRecipe.recipeInstructions = recipe

    def scrapeChefkoch(self, url):

        ua = UserAgent()
        hdr = {'User-Agent': ua.random,
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}
        # GET-Request ausführen
        response = requests.get(url, headers=hdr)

        # BeautifulSoup HTML-Dokument aus dem Quelltext parsen
        html = BeautifulSoup(response.text, 'html.parser')

        # Alle relevanten Abschnitte aus dem HTML-Dokument extrahieren
        ingredients_html = html.find_all('table', class_="ingredients")
        #definition_html = html.find_all('article', class_="ds-box")
        times_html = html.find('small', class_="ds-recipe-meta rds-recipe-meta")
        title = html.find('h1').text
        self.myRecipe.name = title
        #print(title)

        # Die Zutatenpaare in einer Liste sammeln
        tempIngredients = list()
        for ingredient in ingredients_html:
            listentry = list()
            menge = ingredient.find_all('td', class_='td-left')
            zutat = ingredient.find_all('td', class_='td-right')
            for i in range(len(menge)):
                listentry = [" ".join(menge[i].text.split()), " ".join(zutat[i].text.split())]
                #print(listentry)
                tempIngredients.append(listentry)
                #print(myRecipe.ingredients)
        self.myRecipe.ingredients = tempIngredients
        # Die zubereitungszeiten sammeln
        times = times_html.text.splitlines()
        clean_times = list()
        for time in times:
            time = re.sub('[^A-Za-z0-9]+', ' ', time).lstrip()
            clean_times.append(time)
        clean_times = list(filter(lambda a: a != "", clean_times))
        self.myRecipe.time = clean_times
        #print(clean_times)
        # Die Zubereitung holen mit css selector  splitlines()
        recipe = html.select_one('article:has(>h2:-soup-contains("Zubereitung")) > .ds-box').text.lstrip().splitlines()
        recipe = list(filter(lambda a: a != '', recipe))
        self.myRecipe.recipeInstructions = recipe
        #print(recipe)
        return self.myRecipe

    def scrapeWeb(self, url):
        if "chefkoch" in url:
            return self.scrapeChefkoch(url)
        #if "lidl" in url:
            #scrapeRewe(url)