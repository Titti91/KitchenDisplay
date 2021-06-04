#!/usr/bin/python
# -*- coding:utf-8 -*-
import random
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_HD
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
import textwrap
from Recipe import Recipe


class DescriptionPages:
    def __init__(self):
        self.pages = list()

class IngredientPages:
    def __init__(self):
        self.pages = list()

class Display:

    def __init__(self):
        self.myRecipe = Recipe()
        self.descriptionPages = DescriptionPages()
        self.ingredientPages = IngredientPages()
        self.currentIngredientPage = 0
        self.currentDescriptionPage = 0

    def initDisplay(self, recipe):
        self.myRecipe = recipe
        self.descriptionPages.pages = list()
        self.ingredientPages.pages = list()
        self.currentDescriptionPage = 0
        self.currentIngredientPage= 0

        # Generate the ingredients pages
        # Display the ingredients umbrechen bei 7 | 22
        self.ingredientPages = IngredientPages()
        ingredientPage = list()
        inLineCount = 1
        tempIngredient = list()
        for ing in self.myRecipe.ingredients:
            temp2Ingredient = list()
            tempLIng = self.wrapTextRight(ing[0], 7)
            tempRIng = self.wrapTextRight(ing[1], 22)
            inLineCount += max(len(tempLIng), len(tempRIng))
            temp2Ingredient.append(tempLIng)
            temp2Ingredient.append(tempRIng)
            if (inLineCount <= 14):  # number of displayed lines per page
                ingredientPage.append(temp2Ingredient)
            else:
                self.ingredientPages.pages.append(ingredientPage)
                ingredientPage = list()
                inLineCount = 1
                ingredientPage.append(temp2Ingredient)
        self.ingredientPages.pages.append(ingredientPage)

        # Generate description pages
        # Display Description 57
        temp = self.myRecipe.recipeInstructions
        self.descriptionPages = DescriptionPages()

        numberOfLines = len(self.myRecipe.recipeInstructions) - 1;

        descriptionPage = list()
        lineCount = 0;
        for r in temp:
            temp2 = self.wrapTextRight(r, 60)
            for t in temp2:
                if (lineCount <= 20):
                    descriptionPage.append(t)
                    # print(descriptionPage)
                else:
                    self.descriptionPages.pages.append(descriptionPage)
                    descriptionPage = list()
                    lineCount = 0
                    descriptionPage.append(t)
                lineCount += 1
            descriptionPage.append(" ")
            lineCount += 1
        self.descriptionPages.pages.append(descriptionPage)

        self.updateDisplay()


    # def updateDisplay(self, recipe = "", myIngredientsPage = 0, myDescriptionPage = 0):
    def updateDisplay(self):
        # self.myRecipe = recipe
        logging.basicConfig(level=logging.DEBUG)

        try:
            #logging.info("epd7in5_HD Demo")

            epd = epd7in5_HD.EPD()
            logging.info("init and Clear")
            epd.init()
            #epd.Clear()        #try to avoid clearing the display every time

            fontTitle = ImageFont.truetype(os.path.join(fontdir, 'arial.ttf'), 35)
            fontTitleTwoLines = ImageFont.truetype(os.path.join(fontdir, 'arial.ttf'), 30)
            fontTimes = ImageFont.truetype(os.path.join(fontdir, 'arial.ttf'), 14)
            fontIngredients = ImageFont.truetype(os.path.join(fontdir, 'arial.ttf'), 23)
            fontDescription = ImageFont.truetype(os.path.join(fontdir, 'arial.ttf'), 18)


            #Create Canvas
            #
            Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)

            # create square for ingredients
            boxStartX = 10
            boxEndX = (epd.width/2) - 100
            boxStartY = 80
            boxEndY = epd.height-10
            boxMiddleX = (boxEndX / 2) + boxStartX
            draw.rectangle((boxStartX, boxStartY, boxEndX, boxEndY), outline=0)

            # Display Title 34
            titleLines = self.wrapTextRight(self.myRecipe.name, 34)
            if len(titleLines) == 1:
                draw.text((boxEndX - 50, 20),
                          self.myRecipe.name,
                          font=fontTitle, fill=0)
            else:
                line = 0
                for l in titleLines:
                    draw.text((boxEndX - 50, 10 + (line * 30)),
                              l,
                              font=fontTitleTwoLines, fill=0)
                    line += 1


            # Display the times
            timesString = " \n".join(self.myRecipe.time)
            draw.text((10, 10), timesString, font=fontTimes, fill=0)

            #print(ingredientPages.pages)
            ### pages ready, now draw the pages

            #zutaten = [["500g", "Nudeln"], ["1000g", "Gyrosfleic"], ["2", "Paprikaschote(n)"]]
            lines = 1

            # currentIngredientPage = self.ingredientPages.pages[myIngredientsPage]
            currentIngredientPage = self.ingredientPages.pages[self.currentIngredientPage]
            ingLines = 0
            if (self.currentIngredientPage > 0):
                ingLines = 1


            w, h = draw.textsize("Zutaten", font=fontIngredients)
            draw.text((((boxEndX - w)/2) + 10, boxStartY  + (ingLines * 30)),
                      "Zutaten",
                      font=fontIngredients, fill=0)
            ingLines += 1

            for ingr in currentIngredientPage:
                currentNumberLines = max(len(ingr[0]),len(ingr[1]))
                for i in range(len(ingr[0])):
                    w, h = draw.textsize(ingr[0][i], font=fontIngredients)
                    draw.text(((boxStartX + 90) - w, boxStartY + ((ingLines + i) * 30)),
                              ingr[0][i],
                              font=fontIngredients, fill=0)
                for j in range(len(ingr[1])):
                    draw.text(((boxStartX + 100), boxStartY + ((ingLines + j) * 30)),
                              ingr[1][j],
                              font=fontIngredients, fill=0)
                ingLines += currentNumberLines

            #draw indication for more ingredients

            if (self.currentIngredientPage == 0 and len(self.ingredientPages.pages) > 1):
                #draw more arrow at the bottom
                #draw.rectangle((boxStartX + 5, boxEndY - 15, boxEndX - 5, boxEndY - 5), fill=0)
                #draw.polygon((boxStartX + 140, boxEndY - 15, boxEndX - 140, boxEndY - 15, (boxEndX / 2) + (boxStartX -3), boxEndY - 3 ), fill=0) old
                draw.polygon((boxMiddleX - 15, boxEndY - 15, boxMiddleX + 15, boxEndY - 15, boxMiddleX, boxEndY - 3 ), fill=0)

            if (self.currentIngredientPage > 0 and self.currentIngredientPage < len(self.ingredientPages.pages)-1):
                draw.polygon(
                    (boxMiddleX - 15, boxStartY + 15, boxMiddleX + 15, boxStartY + 15, boxMiddleX, boxStartY + 3),
                    fill=0)

                draw.polygon((boxMiddleX - 15, boxEndY - 15, boxMiddleX + 15, boxEndY - 15, boxMiddleX, boxEndY - 3 ), fill=0)

            if(self.currentIngredientPage > 0 and self.currentIngredientPage == len(self.ingredientPages.pages)-1):
                draw.polygon(
                    (boxMiddleX - 15, boxStartY + 15, boxMiddleX + 15, boxStartY + 15, boxMiddleX, boxStartY + 3),
                    fill=0)


            #draw description pages
            # currentPage = self.descriptionPages.pages[myDescriptionPage]
            currentPage = self.descriptionPages.pages[self.currentDescriptionPage]
            mylines = 0;
            for p in currentPage:
                draw.text((boxEndX + 20, boxStartY + (20 * mylines)),
                          p, font=fontDescription, fill=0)
                mylines += 1;


            #Draw page number

            draw.text((epd.width -50, epd.height - 20),
                      str(self.currentDescriptionPage + 1) + " / " + str(len(self.descriptionPages.pages)), font=fontDescription, fill=0)


            epd.display(epd.getbuffer(Himage))
            #time.sleep(5)


            #logging.info("Clear...")
            #epd.init()
            #epd.Clear()

            logging.info("Goto Sleep...")
            epd.sleep()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd7in5_HD.epdconfig.module_exit()
            exit()



    def wrapText(self, text, length):
        wrapper = textwrap.TextWrapper(width=length)
        wrappedText = wrapper.wrap(text=text)
        wrappedText = " \n".join(wrappedText)
        return wrappedText

    def wrapTextRight(self, text, length):
        wrapper = textwrap.TextWrapper(width=length)
        wrappedText = wrapper.wrap(text=text)
        return wrappedText

    def drawScreensaver(self):

        try:

            epd = epd7in5_HD.EPD()
            logging.info("init and Clear")
            epd.init()
            oldRandValue = -1
            randValue = random.randrange(1, 12)  #inclusive, exclusive
            while randValue == oldRandValue :
                randValue = random.randrange(1, 12)  # inclusive, exclusive
            oldRandValue = randValue

            Himage = Image.open(os.path.join(picdir, 'screensaver' + str(randValue) + '.bmp'))
            epd.display(epd.getbuffer(Himage))
            logging.info("Goto Sleep...")
            epd.sleep()


        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd7in5_HD.epdconfig.module_exit()
            exit()