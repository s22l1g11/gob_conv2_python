#gob conv
import subprocess
import os
import time
directory=input('In welchem Verzeichnis liegt das OpenBook? (Bitte die Anfuehrungsstriche nicht vergessen.)\n')
print 'system laeuft an!\n',
#mod.css wird erstellt
print 'mod.css wird erstellt!\n',
directoryModFile=directory+'/mod.css'
modTest = open(directoryModFile, 'w+')
modTest.write('body {visibility:hidden;background:none;width:100%;padding:0;margin:0;}\n')
modTest.write('table, tr, td{padding:0;margin:0; width:auto;}\n')
modTest.write('div.main, .box {visibility:visible;margin:0;padding:0;width:100%;}\n')
modTest.write('.box {border:none; margin-top:-100; padding-bottom:50px;}\n')
modTest.write('dd {display:none;}\n')
modTest.close()
#gob_conv2.sh wird erstellt
print 'gob_conv2.sh wird erstellt\n',
directoryGobConvSH = directory+'/gob_conv2.sh'
gobConvSh = open (directoryGobConvSH, 'w+')
contentVar = '#!/bin/sh\n'
contentVar += 'cat ./common/galileo_open.css > ./user.css\n'
contentVar += 'cat ./mod.css >> ./user.css\n'
contentVar += 'HTMS="`ls *.html`"\n'
contentVar += 'for FILE in ${HTMS};\n'
contentVar += 'do\n'
contentVar += '	if [ "$FILE" != "stichwort.html" ]; then\n'
		# werfe die kommentare raus (alles zwischen <br><hr><a  und </form> )
contentVar += '		sed \'/<br><hr><a /,/<\/form>/ d\' ./$FILE > ./clean\n'
		# werfe head und erste tabelle raus
contentVar += '		sed \'/<html>/,/<\/table>/ d\' ./clean > ./cleaner\n'
		#fuege minimale kopfzeilen ein
contentVar += '		echo "<html><head><title></title></head><body>" > ./clean\n'
contentVar += '		cat ./cleaner >> ./clean\n'
		#saeubere die ausgabe ohne etwas auszugeben
contentVar += '		tidy -m ./clean 2>/dev/null\n'
		#haenge es der alle beinhaltenden datei an
contentVar += '		cat ./clean >> ./alle.htm\n'
contentVar += '	fi\n'
contentVar += 'done\n'
#saeubere ausgabe ohne etwas auszugeben
contentVar += 'tidy -m ./alle.htm 2>/dev/null\n'
#loesche den anfang der datei
contentVar += 'sed \'/<!DOC/,/<\/head>/ d\' ./alle.htm > ./clean\n'
#fuege minimale kopfzeilen ein
contentVar += 'echo "<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">\n<html>\n<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"user.css\">\n</head>" > ./alle.htm\n'
#fuege restinhalt ein
contentVar += 'cat clean >> ./alle.htm\n'
# umwandeln von htm zu pdf
contentVar += 'wkhtmltopdf -n -s A4 -d 200 ./alle.htm ./openbook.pdf\n'
#aufraeumen -.-
contentVar += 'rm ./clean\n'
contentVar += 'rm ./cleaner\n'
contentVar += 'rm ./alle.htm\n'
contentVar += 'rm ./user.css\n'
gobConvSh.write(contentVar)
gobConvSh.close()
#erstelle ein script zum ausfuehren von gob_conv2.sh, sowie zum anschlieszenden aufraeumen
print 'execution script wird erstellt\n',
directoryExecutionSH = directory+'/exe.sh'
exeSh = open (directoryExecutionSH, 'w+')
contentVar = '#!/bin/sh\n'
contentVar += 'chmod a+x '+directoryGobConvSH+'\n'
contentVar += 'cd '+directory+'\n'
contentVar += './gob_conv2.sh\n'
contentVar += 'rm ./gob_conv2.sh\n'
contentVar += 'rm ./mod.css\n'
exeSh.write(contentVar)
exeSh.close()
exeSH = directoryExecutionSH
#ermoegliche die benutzung von exe.sh
subprocess.call(['chmod', 'a+x', directoryExecutionSH])
print 'Kurzes warten vor dem naechsten Schritt!\n',
#time.sleep(5)
print 'execution script wird nun ausgefuehrt\n',
subprocess.call([exeSH], shell=True,)
print 'pdf sollte nun erstellt worden sein!\n',
#loeschen von exe.sh
#subprocess.call(['rm', exeSh])
print 'vorgang ist abgeschlossen\n',
