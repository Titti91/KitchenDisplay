# KitchenDisplay

## Einleitung
Selbst gekochtes Essen schmeckt nicht nur besser, sondern ist oft auch gesünder und verzichtet auf Zusatzstoffe. Doch wo kommen die ganzen Rezepte her? Wenn man was Neues ausprobieren will, ist meist ChefK**€# die erste Anlaufstelle. Doch ein Tablet in der Küche ist mit dreckigen Händen oft keine gute Idee. Auch sind solche Webseiten oft voll mit Werbung, was für die Finanzierung legitim ist, beim tatsächlichen Nachkochen der Rezepte kann das ständige Scrollen jedoch schnell nervig werden. Deshalb hab ich mir ein Display gebaut, was dem Komfort von online Rezepten, das angenehme leseverhalten von Papier und eine Hands free Experience* kombiniert. 
*Sprachsteuerung ist im ersten Prototyp noch nicht enthalten. 

## Funktionen
* Rezept anzeigen
* Foto anzeigen

## Rezept abrufen
1.	Verknüpfe die App mit deinem Display (siehe Einrichtung der App)
2.	Geh mit deinem Handy oder Tablet auf die online Rezepte Seite deines Vertrauens. 
3.	Suche dir ein Rezept raus, was du gerne nachkochen möchtest.
4.	Wähle in deinem Browser die Funktion „Teilen mit“ aus.
5.	Wähle nun die Kochbuch App aus.
6.	Das Rezept ist nun auf deinem Display sichtbar.

## Aktuell unterstützte Plattformen
*	ChefK**€#
*	Weitere folgen

## Hardware
*	Display: 7.5inch HD e-Paper E-Ink Display HAT for Raspberry Pi, 880×528, Black / White, SPI (https://www.waveshare.com/product/7.5inch-hd-e-paper-hat.htm)
*	Controller: Raspberry Pi Zero W (https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
*	Bilderrahmen: RIBBA Rahmen, schwarz13x18 cm (https://www.ikea.com/de/de/p/ribba-rahmen-schwarz-50378448/)

## Einrichtung
1.	Raspberry Pi einrichten. Es wird keine GUI benötigt, ich verwende Raspberry Pi OS Lite. 
Der Pi lässt sich auch über SSH einrichten. (https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)
2.	Display an den Pi anschließen und einrichten. Dazu der Anleitung von Waveshare folgen. (https://www.waveshare.com/wiki/7.5inch_HD_e-Paper_HAT#Hardware_connection)
3.	Zielordner für das Projekt auf dem Pi anlegen bsp. home/pi/KichenDisplay
4.	Den „lib“ Ordner aus der Wavehare Installation hineinkopieren
5.	Neben dem „lib“ Ordner einen „pic“ und einen „src“ Ordner erstellen. Folgende Struktur entsteht:
```
|-KichenDisplay
|---lib
|-----waveshare_edp
|---pic
|---src
```
6.	In den „src“ Ordner wechseln
a.	`git clone https://github.com/Titti91/KitchenDisplay.git` 
7.	Für die Verwendung von Bildern müssen diese in den Ordner „pic“ als Bitmap abgelegt werden. Namensgebung: „`screensaver<1-9>.bmp`" bei anderer Verwendung muss die Funktion „`drawScreensaver`“ in der Datei „`Display.py`“ angepasst werden. 
8.	Das Projekt verwendet eine andere Schriftart, als die im Standard enthaltene Schriftart. Die Schriftart „Arial“ muss als ttf Datei in den „pic“ Ordner gelegt werden. Die arial.ttf Datei findet sich unter Windows in den Schriftarteinstellungen und kann kopiert werden (C:windows\fonts\arial.ttf). 
9.	Abhängigkeiten installieren
    * `pip3 install beautifulsoup4`
    * `pip3 install requests`
10.	CronTab für das automatische starten des Servers anlegen:
    *	In der Konsole auf dem Pi: `crontab -e` aufrufen
    *	Folgende Zeile an die eigenen Bedürfnisse und Gegebenheiten anpassen, einfügen und speichern
    *	`@reboot /usr/bin/python3 /home/pi/KitchenDisplay/src/Server.py >> ~/cron.log 2>&1`
11.	Den Server starten 
    *	Ins verzeichnis scr wecheln 
    *	`python3 Server.py`

## Bildermodus
Das Display kann beliebige Bilder anzeigen. Dazu muss das Bild schwarz weiß sein und als Bitmat in einer Auflösung von 880×528 im Ordner „pic“ abgelegt werden. 
Die Bilder müssen den Namen „`screensaver<1-9>`" Haben. 
Bei Verwendung der Funktion wird per Zufall eins der Bilder angezeigt. Anpassungen an der Namensgebung oder der Zufallsfunktion sind in der Funktion „`drawScreensaver`“ in der Datei „Display.py“ anzupassen. 

## API
Die Kommunikation zwischen Eingabegerät (App) und Display erfolgt über eine REST API. Somit lassen sich auch andere Geräte für die Steuerung verwenden. 
Endpunkte:
*	Neues Rezept laden
    *	`/new/recipe` (post)
    *	Body: `{"url" : "https://url_zum_Rezept.html"}`
*	Rezept blättern
    *	`/recipe/page` (post)
    *	Body: `{"direction": "++"}` // ++ für vorwärts; -- für rückwärts
*	Zutaten blättern
    *	`/ingredient/page` (post)
    *	Body: `{"direction": "++"}` // ++ für vorwärts; -- für rückwärts
*	Bilder anzeigen
    *	`/screensaver` (post)

## Nützliche Links:
*	Waveshare Wiki: https://www.waveshare.com/wiki/7.5inch_HD_e-Paper_HAT 
*	Raspberri Pi Headless setup: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md 
*	Fotobearbeitungssoftware: https://www.photopea.com/ 

