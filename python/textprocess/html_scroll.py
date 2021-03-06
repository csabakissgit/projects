import re
from textprocess import xml_substitutions
from textprocess import line_to_dn
from textprocess import txt_output_line
from textprocess import simpletxtdn_line

def html_scroll(filename, apparatus_type):
    chapter = 0
    vsnum = 0
    textflag = False
    appflag = False
    paralflag = False
    anustubh = True
    hemistich = 0
    proseflag = False
    pvarflag = False
    trflag = False
    noteflag = False
    onflag = False
    firstTEXT = True
    note = ''
    pada = '<padaab>'
    collected_tr = ""
    collected_notes = ""
    appforthisline = "" 
    # header
    print('<!DOCTYPE html>\n <html lang="en"><head>\n <meta http-equiv="content-type" content="text/html; charset=UTF-8">\n <meta charset="utf-8">\n <title>Csaba</title>\n <meta name="viewport" content="width=device-width, initial-scale=1.0">\n <link rel="stylesheet" href="style_scroll.css">\n</head>\n<body onload="closeapp();">\n<br/><div class="text" id="sanskrittext">\n<script xmlns="http://www.w3.org/1999/xhtml" src="showhide.js"></script>\n<div class="tooltip-wrap"><TEXT onclick="turnItDevnag()" id="switchbutton">[Click to switch to Devanāgarī]</TEXT></div><div class="tooltip-wrap"><TEXT onclick="showFunction(\'instructions\')" ><RMTEXT> [Click for instructions] </RMTEXT><DNTEXT> [निर्देशः] </DNTEXT></TEXT><div class="tooltip-content" onclick="hideFunction(\'instructions\')" id="instructions"> <APP> • Click inside this box to close it</APP> <APP> • Single click on Sanskrit line to display apparatus </APP><APP> • Click inside apparatus box to close it</APP><APP> • Double click on Sanskrit line to scroll to relevant note in opposite window, if any </APP><APP> • If your browser has problems rendering the Devanāgarī font, change your browser\'s default font (e.g. to \'Noto Sans Devanagari\' on Ubuntu) </APP></div></div><br/><br/>\n<h2>Sanskrit text</h2>\n\n ')
    openfile = open(filename, "r")
    for line in openfile:
        if '<START/>' in line:
            onflag = True
        if '<STOP/>' in line:
            # close text box
            print("</div></div><br/><br/><br/><br/></div>\n")        
            # print translation box
            print('<div class="translation">\n<h2>Translation</h2>')
            print(collected_tr)
            print("\n</div>\n")        
            # print notes box
            print('<div class="notes">\n<h2>Notes</h2>\n')
            print(collected_notes)
            print("\n</div>\n")        
            # print mss box
            print('<div class="msimage">\n<h2>Sources</h2>\n')
            open_mssdata_file = open("/home/csaba/indology/dharma_project/vrsa_edition/vss_mss_data.html", "r")
            for l in open_mssdata_file:
                print(l[:-1], end=" ")        
            print("\n</div>\n</body></html>")        
            quit()
        if onflag == True:
            if '<NOTANUSTUBH/>' in line:
                anustubh = False 
                proseflag = False
                hemistich = 0
            if '<ANUSTUBH/>' in line:
                anustubh = True
                proseflag = False
                #hemistich = 0
            if '<PROSE>' in line:
                proseflag = True
                anustubh = False
            if '</PROSE>' in line:
                proseflag = False
                anustubh = False
            if '<NEWCHAPTER/>' in line:
                chapter += 1
                #if text doesn't start with verse 1
                #vsnum = 72
                vsnum = 0
                print('<!-- chapter', chapter, '-->')
                if firstTEXT == False:
                   print('\n</div>\n</div>\n<br/><br/><br/><NEWCHAPTER/>')
                else:
                   print('<NEWCHAPTER/>')
                firstTEXT = True
            if '<SETVSNUM' in line:
                v01 = re.sub('.*<SETVSNUM="', '', line)
                v01 = re.sub('".*', '', v01)
                vsnum = int(v01) - 1
            # hover trick
            if '<TEXT>' in line and firstTEXT == False:
                 line = re.sub('<TEXT>', '\n</div>\n</div>\n\n<mainwrap>\n<TEXT>', line)
            if '<TEXT>' in line and firstTEXT == True:
                 line = re.sub('<TEXT>', '\n<mainwrap>\n<TEXT>', line) 
                 firstTEXT = False
            # if it is the main text:        
            if '<TEXT>' in line or textflag == True:
                line = re.sub('\\\\-', '', line)
                maintextrm = txt_output_line.txt_output_line(line, textflag)
                maintextrm = re.sub('<MNTR>', '', maintextrm)
                maintextrm = re.sub('</MNTR>', '', maintextrm)
                maintextrm = re.sub('<mainwrap>', '', maintextrm)
                maintextrm = re.sub('</mainwrap>', '', maintextrm)
                maintextrm = re.sub('<div>', '', maintextrm)
                maintextrm = re.sub('</div>', '', maintextrm)
                if proseflag == False:
                    maintextrm = re.sub('\|\|.*', " ॥"+ str(chapter) + ":" + str(vsnum), maintextrm)
                else:
                    maintextrm = re.sub('\|\|', " ॥", maintextrm)
                maintextrm = re.sub('\|', " ।", maintextrm)
                maintextdn = simpletxtdn_line.simpletxtdn_line(maintextrm) 

                textflag = True
                uvacaflag = 0
                if '</TEXT>' in line:
                    textflag = False
                # check if this is the end of a verse
                if '||' in line and proseflag == False:
                    chap_and_vsnum = ("<vsnum>" + str(chapter) + "." + str(vsnum) + "</vsnum>||") 
                else:
                    chap_and_vsnum = "" 
                if '||' in line and anustubh == True and hemistich == 1 and proseflag == False:
                    outputline = re.sub('\|\|', ' ||' + chap_and_vsnum, line)
                    outputline = re.sub('<TEXT>', '<TEXT pada="' + str(chapter) + '.' + str(vsnum) + 'cd" onclick="showFunction(\''  +  str(chapter) + '.' + str(vsnum) + 'cd\')" ondblclick="showNote(\'' + 'note' + str(chapter) + '.' + str(vsnum) + '\')" '  + '><RMTEXT>', outputline)
                    appforthisline = "cd"
                    hemistich = 0
                elif '||' in line and anustubh == False and proseflag == False:
                    outputline = re.sub('\|\|', ' ||' + chap_and_vsnum, line)
                    outputline = "\n" + outputline + "\n" 
                    outputline = re.sub('<TEXT>', '<TEXT pada="' + str(chapter) + '.' + str(vsnum) + 'd" onclick="showFunction(\''  +  str(chapter) + '.' + str(vsnum) + 'd\')" ondblclick="showNote(\'' + 'note' + str(chapter) + '.' + str(vsnum) + '\')" '  + '><RMTEXT>&#160;&#160;&#160;&#160;', outputline)
                    hemistich = 0
                    appforthisline = "d"
                # special danda: it does not increase verse number, e.g. after devy uvāca
                elif '|*' in line:
                    uvacaflag = 1
                    outputline = re.sub('\|\*', ' | ', line)
                    outputline = re.sub('<TEXT>', '<TEXT><RMTEXT><uvaca onclick="showFunction(\''  +  str(chapter) + '.' + str(vsnum) + 'nextuvaca\')">', outputline)
                    outputline = re.sub('</TEXT>', '</uvaca></TEXT>', outputline)
                    hemistich = 0
                    appforthisline = "nextuvaca"
                # with anuṣṭubh, a danda increases verse number if it is the first single danda
                elif '|' in line and hemistich == 0 and anustubh == True and proseflag == False:
                    vsnum += 1
                    #outputline = '\n\n<verse verseno="' + str(chapter) + "." + str(vsnum) + '"/>' + line  
                    outputline = re.sub('<TEXT>', '\n<TEXT pada="' + str(chapter) + '.' + str(vsnum) + 'ab" onclick="showFunction(\''  +  str(chapter) + '.' + str(vsnum) + 'ab\')" ondblclick="showNote(\'' + 'note' + str(chapter) + '.' + str(vsnum) + '\')" '  + '><RMTEXT>', line)
                    appforthisline = "ab"
                    outputline = re.sub('\|', ' |', outputline)
                    # the next single danda not a first single danda
                    hemistich = 1 
                # check if this is a non-anuṣṭubh first line
                elif '|' not in line and hemistich == 0 and anustubh == False:
                    # no indent
                    vsnum += 1
                    #outputline = '\n\n<verse verseno="' + str(chapter) + "." + str(vsnum) + '"/>' + line  
                    outputline = re.sub('<TEXT>', '<TEXT pada="' + str(chapter) + '.' + str(vsnum) + 'a" onclick="showFunction(\''  +  str(chapter) + '.' + str(vsnum) + 'a\')" ondblclick="showNote(\'' + 'note' + str(chapter) + '.' + str(vsnum) + '\')" '  + '><RMTEXT>', line)
                    hemistich = 1
                    appforthisline = "a"
                # check if this is a non-anuṣṭubh third line
                elif '|' not in line and hemistich == 2 and anustubh == False:
                    # no indent
                    outputline = re.sub('<TEXT>', '<TEXT pada="' + str(chapter) + '.' + str(vsnum) + 'c" onclick="showFunction(\''  +  str(chapter) + '.' + str(vsnum) + 'c\')" ondblclick="showNote(\'' + 'note' + str(chapter) + '.' + str(vsnum) + '\')" '  + '><RMTEXT>', line)
                    hemistich = hemistich + 1
                    appforthisline = "c"
                # if this is a first single danda but it is not anuṣṭubh, don't increase verse number    
                elif '|' in line and anustubh == False and proseflag == False:
                    outputline = "\n" + line
                    outputline = re.sub('<TEXT>', '<TEXT pada="' + str(chapter) + '.' + str(vsnum) + 'b" onclick="showFunction(\''  +  str(chapter) + '.' + str(vsnum) + 'b\')" ondblclick="showNote(\'' + 'note' + str(chapter) + '.' + str(vsnum) + '\')" '  + '><RMTEXT>&#160;&#160;&#160;&#160;', outputline)
                    outputline = re.sub('\|', ' |', outputline)
                    hemistich = hemistich + 1 
                    appforthisline = "b"
                elif '||' in line and hemistich == 2 and anustubh == True:
                    outputline = re.sub('\|\|', ' ||' + chap_and_vsnum, line)
                    outputline = re.sub('<TEXT>', '<TEXT pada="' + str(chapter) + '.' + str(vsnum) + 'ef" onclick="showFunction(\''  +  str(chapter) + '.' + str(vsnum) + 'ef\')"'  + '><RMTEXT>', outputline)
                    hemistich = 0 
                    appforthisline = "ef"
                elif '|' in line and hemistich == 1 and anustubh == True:
                    outputline = re.sub('<TEXT>', '<TEXT pada="' + str(chapter) + '.' + str(vsnum) + 'cd onclick="showFunction(\''  +  str(chapter) + '.' + str(vsnum) + 'cd\')" ondblclick="showNote(\'' + 'note' + str(chapter) + '.' + str(vsnum) + '\')" ' + '><RMTEXT>', line)
                    outputline = re.sub('\|', ' |', outputline)
                    hemistich = 2 
                    appforthisline = "cd"
                else:
                    outputline = line 
                v01 = re.sub('{ }', " ", outputline)
                v01 = re.sub('<COLOPHON>', "\n<colophon><RMTEXT> ", v01)
                v01 = re.sub('</COLOPHON>', " </colophon>", v01)
                if '&#160;&#160;&#160;&#160' in v01: 
                    v01 = re.sub('</TEXT>.*', '</RMTEXT><DNTEXT>&#160;&#160;&#160;&#160' + maintextdn + ' </DNTEXT></TEXT>\n<apparatuswrap>', v01)
                else:
                    v01 = re.sub('</TEXT>.*', '</RMTEXT><DNTEXT>' + maintextdn + ' </DNTEXT></TEXT>\n<apparatuswrap>', v01)
                v01 = re.sub('Ó', "oṃ", v01)
                #v01 = re.sub('<uvaca>', '', v01)
                #v01 = re.sub('</uvaca>', '', v01)
                v01 = re.sub('<ja>', ' ', v01)
                v01 = re.sub('</ja>', ' ', v01)
                v01 = re.sub('\\\\-', '', v01)
                v01 = re.sub('<mainwrap>', '<div class="tooltip-wrap">', v01)
                v01 = re.sub('</mainwrap>', '</div>', v01)
                v01 = re.sub('<apparatuswrap>', '<div class="tooltip-content" onclick="hideFunction(\'' + str(chapter) + '.' + str(vsnum) + appforthisline + '\')" id="' + str(chapter) + '.' + str(vsnum) + appforthisline + '">', v01)
                v01 = re.sub('</apparatuswrap>', '</div>', v01)
                print(v01)
                # fill in the dn version
            if '<APP>' in line or appflag == True:
                appflag = True
                if '</APP>' in line:
                    appflag = False
                v01 = re.sub('{ }', " ", line)
                v01 = re.sub('\\\\vo', str(vsnum+uvacaflag), v01)
                v01 = re.sub('\\\\v', str(vsnum+uvacaflag), v01)
                v01 = re.sub('\\\\csa', 'ā', v01)
                v01 = re.sub('\\\\csi', 'i', v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                print(v01)
            if '<PARAL>' in line or paralflag == True:
                paralflag = True
                if '</PARAL>' in line:
                    paralflag = False
                v01 = re.sub('{ }', " ", line)
                v01 = re.sub('<PARAL> *\\\\vo', "<PARAL>" + str(vsnum+uvacaflag), v01)
                v01 = re.sub('<PARAL> *\\\\v', "<PARAL>" + str(vsnum+uvacaflag), v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                print(v01)
            '''
            if '<PVAR>' in line or pvarflag == True:
                pvarflag = True
                if '</PVAR>' in line:
                    pvarflag = False
                v01 = re.sub('{ }', " ", line)
                v01 = re.sub('<PVAR>\\\\vo', "<PVAR>", v01)
                v01 = re.sub('<PVAR>\\\\v', "<PVAR>", v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                print(v01)
            '''    
            if '<TR>' in line or trflag == True:
                trflag = True
                v01 = re.sub('<!-- <TR>', '<trnls>', line)
                v01 = re.sub('</TR> -->', '</trnsl>', v01)
                v01 = xml_substitutions.xml_substitutions(v01)
                if '<TR>' in line:
                    collected_tr = collected_tr + "<br/></br>" + "|" + "<vsnum>" + str(chapter) + "." + str(vsnum) + "</vsnum>" + "| "
                if '</TR>' in line:
                    trflag = False
                    collected_tr = collected_tr  + v01
                else:
                    collected_tr = collected_tr + v01
            if '<NOTE>' in line or noteflag == True:
                noteflag = True
                v01 = xml_substitutions.xml_substitutions(line)
                if '<NOTE>' in line:
                    collected_notes = collected_notes + "<br/></br>" + "|" + '<vsnum id="note' + str(chapter) + "." + str(vsnum) + '">' + str(chapter) + "." + str(vsnum) + "</vsnum>" + "| "
                if '</NOTE>' in line:
                    noteflag = False
                    collected_notes = collected_notes  + v01
                else:
                    collected_notes = collected_notes + v01
            '''    
            if '<NOTE>' in line or noteflag == True:
                noteflag = True
                note = note + line
                if '</NOTE>' in line:
                    noteflag = False
                    note = xml_substitutions.xml_substitutions(note)
                    print(note)
                    note = '' 
            '''
            if '<SUBCHAPTER>' in line or '<CHAPTER>' in line or '<TITLE>' in line:
                v01 = re.sub('{ }', " ", line)
                if firstTEXT == False:
                   print('\n</div>\n</div>')
                print(v01)
                firstTEXT = True
    openfile.close()

