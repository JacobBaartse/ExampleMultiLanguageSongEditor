import re

debug_print = False


def rtf_to_txt(rtf: str) -> str:
    """
    Convert RTF to plain text using regex
    """
    pattern = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)
    # Control words which specify a "destionation".
    destinations = frozenset((
        'aftncn', 'aftnsep', 'aftnsepc', 'annotation', 'atnauthor', 'atndate', 'atnicn', 'atnid',
        'atnparent', 'atnref', 'atntime', 'atrfend', 'atrfstart', 'author', 'background',
        'bkmkend', 'bkmkstart', 'blipuid', 'buptim', 'category', 'colorschememapping',
        'colortbl', 'comment', 'company', 'creatim', 'datafield', 'datastore', 'defchp', 'defpap',
        'do', 'doccomm', 'docvar', 'dptxbxtext', 'ebcend', 'ebcstart', 'factoidname', 'falt',
        'fchars', 'ffdeftext', 'ffentrymcr', 'ffexitmcr', 'ffformat', 'ffhelptext', 'ffl',
        'ffname', 'ffstattext', 'field', 'file', 'filetbl', 'fldinst', 'fldrslt', 'fldtype',
        'fname', 'fontemb', 'fontfile', 'fonttbl', 'footer', 'footerf', 'footerl',
        'footerr', 'footnote', 'formfield', 'ftncn', 'ftnsep', 'ftnsepc', 'g', 'generator',
        'gridtbl', 'header', 'headerf', 'headerl', 'headerr', 'hl', 'hlfr', 'hlinkbase',
        'hlloc', 'hlsrc', 'hsv', 'htmltag', 'info', 'keycode', 'keywords', 'latentstyles',
        'lchars', 'levelnumbers', 'leveltext', 'lfolevel', 'linkval', 'list', 'listlevel',
        'listname', 'listoverride', 'listoverridetable', 'listpicture', 'liststylename',
        'listtable', 'listtext', 'lsdlockedexcept', 'macc', 'maccPr', 'mailmerge', 'maln',
        'malnScr', 'manager', 'margPr', 'mbar', 'mbarPr', 'mbaseJc', 'mbegChr', 'mborderBox',
        'mborderBoxPr', 'mbox', 'mboxPr', 'mchr', 'mcount', 'mctrlPr', 'md', 'mdeg', 'mdegHide',
        'mden', 'mdiff', 'mdPr', 'me', 'mendChr', 'meqArr', 'meqArrPr', 'mf', 'mfName', 'mfPr',
        'mfunc', 'mfuncPr', 'mgroupChr', 'mgroupChrPr', 'mgrow', 'mhideBot', 'mhideLeft',
        'mhideRight', 'mhideTop', 'mhtmltag', 'mlim', 'mlimloc', 'mlimlow', 'mlimlowPr',
        'mlimupp', 'mlimuppPr', 'mm', 'mmaddfieldname', 'mmath', 'mmathPict', 'mmathPr',
        'mmaxdist', 'mmc', 'mmcJc', 'mmconnectstr', 'mmconnectstrdata', 'mmcPr', 'mmcs',
        'mmdatasource', 'mmheadersource', 'mmmailsubject', 'mmodso', 'mmodsofilter',
        'mmodsofldmpdata', 'mmodsomappedname', 'mmodsoname', 'mmodsorecipdata', 'mmodsosort',
        'mmodsosrc', 'mmodsotable', 'mmodsoudl', 'mmodsoudldata', 'mmodsouniquetag',
        'mmPr', 'mmquery', 'mmr', 'mnary', 'mnaryPr', 'mnoBreak', 'mnum', 'mobjDist', 'moMath',
        'moMathPara', 'moMathParaPr', 'mopEmu', 'mphant', 'mphantPr', 'mplcHide', 'mpos',
        'mr', 'mrad', 'mradPr', 'mrPr', 'msepChr', 'mshow', 'mshp', 'msPre', 'msPrePr', 'msSub',
        'msSubPr', 'msSubSup', 'msSubSupPr', 'msSup', 'msSupPr', 'mstrikeBLTR', 'mstrikeH',
        'mstrikeTLBR', 'mstrikeV', 'msub', 'msubHide', 'msup', 'msupHide', 'mtransp', 'mtype',
        'mvertJc', 'mvfmf', 'mvfml', 'mvtof', 'mvtol', 'mzeroAsc', 'mzeroDesc', 'mzeroWid',
        'nesttableprops', 'nextfile', 'nonesttables', 'objalias', 'objclass', 'objdata',
        'object', 'objname', 'objsect', 'objtime', 'oldcprops', 'oldpprops', 'oldsprops',
        'oldtprops', 'oleclsid', 'operator', 'panose', 'password', 'passwordhash', 'pgp',
        'pgptbl', 'picprop', 'pict', 'pn', 'pnseclvl', 'pntext', 'pntxta', 'pntxtb', 'printim',
        'private', 'propname', 'protend', 'protstart', 'protusertbl', 'pxe', 'result',
        'revtbl', 'revtim', 'rsidtbl', 'rxe', 'shp', 'shpgrp', 'shpinst',
        'shppict', 'shprslt', 'shptxt', 'sn', 'sp', 'staticval', 'stylesheet', 'subject', 'sv',
        'svb', 'tc', 'template', 'themedata', 'title', 'txe', 'ud', 'upr', 'userprops',
        'wgrffmtfilter', 'windowcaption', 'writereservation', 'writereservhash', 'xe', 'xform',
        'xmlattrname', 'xmlattrvalue', 'xmlclose', 'xmlname', 'xmlnstbl',
        'xmlopen',
    ))
    # Translation of some special characters.
    specialchars = {
        'par': '\n',
        'sect': '\n\n',
        'page': '\n\n',
        'line': '\n',
        'tab': '\t',
        'emdash': u'\u2014',
        'endash': u'\u2013',
        'emspace': u'\u2003',
        'enspace': u'\u2002',
        'qmspace': u'\u2005',
        'bullet': u'\u2022',
        'lquote': u'\u2018',
        'rquote': u'\u2019',
        'ldblquote': u'\201C',
        'rdblquote': u'\u201D',
    }
    fcharset_to_codepage = {
        '178': '1256',  # arabic
        '134':  'gb2312',  # chinese  # todo gather multiple /'xx all to a bytestring
    }
    # private unicode range U+E000–U+F8FF
    hex_string_indicator = "\uF722"
    code_page_indicator = "\uF723"

    stack = []
    ignorable = False           # Whether this group (and all inside it) are "ignorable".
    ucskip = 1                  # Number of ASCII characters to skip after a unicode character.
    curskip = 0                 # Number of ASCII characters left to skip
    out = []                    # Output buffer.
    font_table = False
    cur_font_nr = 0
    codepage_list = dict()
    global_codepage = "1252"
    for match in pattern.finditer(rtf):
        word, arg, l_hex, char, brace, tchar = match.groups()
        if debug_print:
            print(word, arg, l_hex, char, brace, tchar)
        if word == "f":
            cur_font_nr = arg
        if word == "ansicpg":
            global_codepage = arg
        if word == "fonttbl":
            font_table = True
        if font_table:
            if brace == '}':
                font_table = False
        if font_table:
            if word == "f":
                codepage_list[cur_font_nr] = global_codepage
            if word == "fcharset":
                if arg != '0':
                    codepage_list[cur_font_nr] = fcharset_to_codepage[arg]
        if brace:
            curskip = 0
            if brace == '{':
                # Push state
                stack.append((ucskip, ignorable))
            elif brace == '}':
                # Pop state
                ucskip, ignorable = stack.pop()
        elif char:  # \x (not a letter)
            curskip = 0
            if char == '~':
                if not ignorable:
                    out.append(u'\xA0')
            elif char in '{}\\':
                if not ignorable:
                    out.append(char)
            elif char == '*':
                ignorable = True
        elif word:  # \foo
            curskip = 0
            if word in destinations:
                ignorable = True
            elif ignorable:
                pass
            elif word in specialchars:
                out.append(specialchars[word])
            elif word == 'uc':
                ucskip = int(arg)
            elif word == 'u':
                c = int(arg)
                if c < 0:
                    c += 0x10000
                if c > 127:
                    out.append(chr(c))
                else:
                    out.append(chr(c))
                curskip = ucskip
        elif l_hex:  # \'xx
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                # c = int(l_hex, 16)
                # if c > 127:
                out.append(code_page_indicator + codepage_list[cur_font_nr] + hex_string_indicator + l_hex)
                # out.append(l_hex)
                # else:
                #     out.append(chr(c))
        elif tchar:
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                out.append(tchar)
    #walk through the output combine hex values, and decode them at once (required for chinese characters) depending on the code page.
    decoded_out = []
    hex_string = ""
    prev_code_page = "None"
    for a_string in out:
        if a_string.startswith(code_page_indicator+prev_code_page):
            prev_code_page, cur_hex_string = a_string[1:].split(hex_string_indicator)
            hex_string += cur_hex_string
        else:
            if hex_string:
                decoded_out.append(bytes.fromhex(hex_string).decode(prev_code_page))
            if a_string.startswith(code_page_indicator):
                prev_code_page, hex_string = a_string[1:].split(hex_string_indicator)
            else:
                decoded_out.append(a_string)
                hex_string = ""
                prev_code_page = "None"
    if hex_string:
        decoded_out.append(bytes.fromhex(hex_string).decode(prev_code_page))
    retval = ''.join(decoded_out)
    print(retval)
    return retval


# if __name__ == "__main__":
#
#     rtf_data = b"{\\rtf1\\ansi\\ansicpg1252\\cocoartf2822\n\\cocoatextscaling0\\cocoaplatform0" \
#                b"{\\fonttbl\\f0\\fnil\\fcharset178 GeezaPro-Bold;\\f1\\fnil\\fcharset0 CMGSans-SemiBold;}\n" \
#                b"{\\colortbl;\\red255\\green255\\blue255;\\red253\\green213\\blue63;}\n" \
#                b"{\\*\\expandedcolortbl;;\\cssrgb\\c99719\\c85967\\c31075;}\n" \
#                b"\\deftab1680\n\\pard\\pardeftab1680\\pardirnatural\\qc\\partightenfactor0\n\n" \
#                b"\\f0\\b\\fs54 \\cf2 \\'e5\\'e1\\'e1\\'e6\\uc0\\u1740 \\'c7\\'a1\n" \
#                b"\\f1  \n" \
#                b"\\f0 \\'e5\\'e1\\'e1\\'e6\\uc0\\u1740 \\'c7\\'a1\n\\f1  \n\\f0 \\'e5\\'e1\\'e1\\'e6\\uc0\\u1740 \\'c7\\'a1\n\\f1 \\par \n\\f0 \\'e5\\'e1\\'e1\\'e6\\uc0\\u1740 \\'c7\\'a1\n\\f1  \n\\f0 \\'e5\\'e1\\'e1\\'e6\\uc0\\u1740 \\'c7\\'a1\n\\f1  \n\\f0 \\'e5\\'e1\\'e1\\'e6\\uc0\\u1740 \\'c7}"
#     print(rtf_to_txt(rtf_data.decode()))
#
#
#
#     o_0017_chinees = b"{\\rtf1\\ansi\\ansicpg1252\\cocoartf1671\n{\\fonttbl\\f0\\fnil\\fcharset0 CMGSans-Regular;\\f1\\fswiss\\fcharset0 ArialMT;\\f2\\fnil\\fcharset134 PingFangSC-Semibold;\n\\f3\\fnil\\fcharset0 CMGSans-MediumItalic;\\f4\\fnil\\fcharset0 LucidaGrande-Bold;}\n{\\colortbl;\\red255\\green255\\blue255;\\red0\\green190\\blue255;}\n{\\*\\expandedcolortbl;;\\csgenericrgb\\c0\\c74510\\c100000;}\n\\deftab720\n\\pard\\pardeftab720\\slleading120\\partightenfactor0\n\n\\f0\\b\\fs132 \\cf1 Chinees:\n\\f1\\b0\\fs148 \\cf0 \\par \n\\f2\\b\\fs132 \\cf1 \\'ce\\'d2\\'b0\\'ae\\'c4\\'e3\\'a3\\'ac\\'d2\\'ae\\'f6\\'d5\n\\f1\\b0\\fs148 \\cf0 \\par \\pard\\pardeftab720\\slleading120\\partightenfactor0\n\n\\f3\\i\\fs132 \\cf2   W\n\\f4\\i0\\b \\uc0\\u466 \n\\f3\\i\\b0  \\'e0i n\n\\f4\\i0\\b \\uc0\\u464 \n\\f3\\i\\b0 , y\\uc0\\u275 s\\u363 \n\\f1\\i0\\fs148 \\cf0 \\par \\pard\\pardeftab720\\slleading120\\partightenfactor0\n\n\\f2\\b\\fs132 \\cf1 \\'ce\\'d2\\'b0\\'ae\\'c4\\'e3\\'a3\\'ac\\'d2\\'ae\\'f6\\'d5\n\\f1\\b0\\fs148 \\cf0 \\par \\pard\\pardeftab720\\slleading120\\partightenfactor0\n\n\\f3\\i\\fs132 \\cf2   W\n\\f4\\i0\\b \\uc0\\u466 \n\\f3\\i\\b0  \\'e0i n\n\\f4\\i0\\b \\uc0\\u464 \n\\f3\\i\\b0 , y\\uc0\\u275 s\\u363 \n\\f1\\i0\\fs148 \\cf0 \\par \\pard\\pardeftab720\\slleading120\\partightenfactor0\n\n\\f2\\b\\fs132 \\cf1 \\'ce\\'d2\\'b0\\'ae\\'c4\\'e3\\'a3\\'ac\\'d2\\'ae\\'f6\\'d5\n\\f1\\b0\\fs148 \\cf0 \\par \\pard\\pardeftab720\\slleading120\\partightenfactor0\n\n\\f3\\i\\fs132 \\cf2   W\n\\f4\\i0\\b \\uc0\\u466 \n\\f3\\i\\b0  \\'e0i n\n\\f4\\i0\\b \\uc0\\u464 \n\\f3\\i\\b0 , y\\uc0\\u275 s\\u363 \n\\f1\\i0\\fs148 \\cf0 \\par \\pard\\pardeftab720\\slleading120\\partightenfactor0\n\n\\f2\\b\\fs132 \\cf1 \\'d2\\'ae\\'f6\\'d5\\'a3\\'ac\\'ce\\'d2\\'b0\\'ae\\'c4\\'e3\n\\f1\\b0\\fs148 \\cf0 \\par \\pard\\pardeftab720\\slleading120\\partightenfactor0\n\n\\f3\\i\\fs132 \\cf2   y\\uc0\\u275 s\\u363 , w\n\\f4\\i0\\b \\uc0\\u466 \n\\f3\\i\\b0  \\'e0i n\n\\f4\\i0\\b \\uc0\\u464 \n\\f1\\b0\\fs148 \\cf0 \\par }"
#
#     print(rtf_to_txt(o_0017_chinees.decode()))
