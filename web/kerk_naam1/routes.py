from flask import Blueprint, request, make_response, url_for
from common.SongEditorPro7Generic import get_text_block_names, gen_pro_data, convert_to_rtf_unicodes
from common.protobuf import presentation_pb2
import common.parse_rtf
import json
from web.kerk_naam1 import checkbox
from web.kerk_naam1 import button
label_string = None

site_prefix = "/".join(__name__.split(".")[:-1]) # /web/kerk_naam1
url_prefix = site_prefix.split("/")[-1] # kerk_naam1

app = Blueprint(site_prefix, __name__, url_prefix="/"+url_prefix)


# Hit the file system only once, then store in memory
def get_label_string():
    global label_string
    if label_string is None:
        with open(site_prefix + "/GroupNames.txt", "r") as group_names:
            labels = group_names.read().split("\n")
            num_labels_per_line = 9
            label_string = "<table><tr>"
            for index, label in enumerate(labels):
                if index == num_labels_per_line:
                    label_string += "</tr>\n<tr>"
                label_string += f"<td>&nbsp;&nbsp;&nbsp;&nbsp;{label}</td>"
            label_string += "</tr></table>"
    return label_string


class MemoryFile(object):
    def __init__(self):
        self.data = b""

    def write(self, stuff):
        self.data += stuff.encode()


def strip_song_name(song_name):
    s = r"ÇüéâäàåçêëèïîìÄÅÉôöòûùÿÖÜøØ×ƒáíóúñÑÁÂÀ¥ãÃÐÊËÈıÍÎÏÌÓßÔÒõÕµÚÛÙýÝ§¹³²"
    r = r"CueaaaaceeeiiiAAEooouuyOU00xfaiounNAAAYaADEEE1IIIIOSOOoOuUUUyYS132"

    converted = ""
    for character in song_name:
        for _s, _r in zip(s, r):
            if character == _s:
                character = _r
        if character not in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz-_ "):
            character = " "
        converted += character
    # remove multiple spaces
    while "  " in converted:
        converted = converted.replace("  ", " ")
    song_name = converted.strip()
    return song_name


def json_download(request):
    form_data = request.form
    text_block_names = get_text_block_names(subdir=site_prefix)
    song_text = {}
    for text_block_name in text_block_names:
        a_song_text = form_data[text_block_name].replace("\r", "")
        song_text[text_block_name] = (a_song_text+"\n").split("\n")
    mem_file = MemoryFile()
    json.dump(song_text, mem_file)
    response = make_response(mem_file.data)
    response.headers.set('Content-Type', 'binary/json')
    song_file_name = strip_song_name(form_data["SongName"])
    response.headers.set('Content-Disposition', 'attachment', filename=f'{song_file_name}.json')
    return response


def song_download(request):
    form_data = request.form
    # print([form_data])
    text_block_names = get_text_block_names(subdir=site_prefix)
    song_text = {}
    for text_block_name in text_block_names:
        a_song_text = form_data[text_block_name].replace("\r", "")
        if 'punctuation' in form_data:
            tmp_songtext = a_song_text.split("\n")
            for i in range(len(tmp_songtext)):
                tmp_songtext[i] = tmp_songtext[i].rstrip(" .,;")
            a_song_text = "\n".join(tmp_songtext)
        if "brackets_"+text_block_name in form_data:
            a_song_text = ["("+regel+")" for regel in a_song_text.split("\n")]
            a_song_text = "\n".join(a_song_text)
        song_text[text_block_name] = (a_song_text+"\n").split("\n")
    line_count = int(form_data["NumLines"])

    try:
        if 'groupLabelCheck' in form_data:
            song_binary = gen_pro_data(text_block_names, song_text, line_count, subdir=site_prefix, check_labels=True, max_line_length=int(form_data["NumChars"]))
        else:
            song_binary = gen_pro_data(text_block_names, song_text, line_count, subdir=site_prefix, check_labels=False, max_line_length=int(form_data["NumChars"]))
    except Exception as error_message:
        return f"""<html><head>
        <link rel="stylesheet" href="/static/kerk_naam1/style.css">
        </head>
        <body  style="background-color:#DFE3D3 ;">
        <b><H0 >Multi Language Song Editor</H0></br></br><label>{error_message}</label></br></br><button  class="buttonBlue" onclick="history.back()">Go Back</button></body></html>"""

    response = make_response(song_binary)
    response.headers.set('Content-Type', 'binary/pro')
    song_file_name = strip_song_name(form_data["SongName"])
    response.headers.set('Content-Disposition', 'attachment', filename=f'{song_file_name}.pro')
    return response


def rtf_download(request):
    form_data = request.form
    text_block_names = get_text_block_names(subdir=site_prefix)

    rtf_data_start = b'{\\rtf1\\ansi\\ansicpg1252\\cocoartf2759\n\\cocoatextscaling0\\cocoaplatform0{\\fonttbl\\f0\\fnil\\fcharset0 HelveticaNeue;\\f1\\fnil\\fcharset0 LucidaGrande;}\n' \
                     b'{\\colortbl;\\red255\\green0\\blue0;\\red0\\green255\\blue0;\\red0\\green0\\blue255;\\red0\\green255\\blue255;\\red255\\green0\\blue255;\\red255\\green255\\blue0;\\red125\\green125\\blue125;}\n' \
                     b'{\\*\\expandedcolortbl;;\\csgray\\c100000;}\n'
    color_number = 0
    rtf_data_line = b'\\deftab1680\n\\pard\\pardeftab1680\\pardirnatural\\qc\\partightenfactor0\n\n\\f0\\fs18\\cf{color_number}\\f1\\uc1 '
    rtf_document = rtf_data_start

    for text_block_name in text_block_names:
        color_number += 1
        rtf_document += rtf_data_line.replace(b"{color_number}", str(color_number).encode())
        rtf_document += b"\\par\\par " + text_block_name.encode() + b"\\par\\par "
        a_song_text = form_data[text_block_name].replace("\r", "")
        a_song_text = a_song_text.replace("\n", "\\par ")
        a_song_text = convert_to_rtf_unicodes(a_song_text) + "\\par"
        rtf_document += a_song_text.encode()
    rtf_document += b"}"

    response = make_response(rtf_document)
    response.headers.set('Content-Type', 'binary/rtf')
    song_file_name = strip_song_name(form_data["SongName"])
    response.headers.set('Content-Disposition', 'attachment', filename=f'{song_file_name}.rtf')
    return response


def load_song_pro(pro_data):
    presentation_obj = presentation_pb2.Presentation()
    presentation_obj.ParseFromString(pro_data.read())

    slide_list = dict()
    song_text_slides = []

    # read all slides in dictionary named by their uuid.
    for presentation_que in presentation_obj.cues:
        one_slide = dict()
        for action in presentation_que.actions:
            for element in action.slide.presentation.base_slide.elements:
                rtf_data = element.element.text.rtf_data
                rtf_data =rtf_data.replace(b"\\\n", b"\\par ")
                text = common.parse_rtf.rtf_to_txt(rtf_data.decode())
                text = text.replace("\n\n", "\n")
                text = text.rstrip("\n")
                lines = text.split("\n")
                lines = [line.strip("()") for line in lines]  # remove brackets ()
                one_slide[element.element.name] = lines
        slide_list[presentation_que.uuid.string] = one_slide

    # get the order for the slides form the cue group
    for cue_group in presentation_obj.cue_groups:
        for cue_identifier in cue_group.cue_identifiers:
            slide_list[cue_identifier.string]["group_label"] = cue_group.group.name
            song_text_slides.append(slide_list[cue_identifier.string])

    song_text_dict = dict()
    # convert song text dict to three times long text
    text_block_names = get_text_block_names("web/kerk_naam1")
    for text_block_name in text_block_names:
        song_text_dict[text_block_name] = []

    prev_group_label = "empty_label"
    for text_block_name in text_block_names:
        for song_text_slide in song_text_slides:
            if text_block_name in song_text_slide:
                if song_text_slide[text_block_name] != ['']:
                    if "group_label" in song_text_slide:
                        if song_text_slide["group_label"] != prev_group_label:
                            song_text_dict[text_block_name].append(song_text_slide["group_label"])
                    song_text_dict[text_block_name].extend(song_text_slide[text_block_name])
                    song_text_dict[text_block_name].append("")
            prev_group_label = song_text_slide["group_label"]
    return song_text_dict


@app.route("/", methods=["GET", "POST"])
def song_input():
    loaded_dict = {}
    if request.method == "POST":
        if "action" in request.files:
            if request.files["action"]:
                if ".pro" in request.files["action"].filename:
                    # load song data from .pro file
                    pro_data = request.files["action"]
                    loaded_dict = load_song_pro(pro_data)
                    loaded_dict["song_title"] = pro_data.filename.replace(".pro", "")
                elif ".json" in request.files["action"].filename:
                    # load song data from .json file
                    json_data = request.files["action"]
                    loaded_dict = json.load(json_data.stream)
                    loaded_dict["song_title"] = json_data.filename.replace(".json", "")

        if "action" in request.form:
            action = request.form["action"]
            if action == "pro":
                return song_download(request)
            if action == "json":
                return json_download(request)
            if action == "rtf":
                return rtf_download(request)
    title = ""
    brackets = ""
    content = ""

    text_block_names = get_text_block_names(subdir=site_prefix)  # gets the translation languages as in ["Songtext", "Translation 1", "Translation 2]
    for index, language in enumerate(text_block_names):
        if index == 0:
            brackets += f'<td valign=bottom><label>{language}</label></td>\n'  # skip songtext, no brackets needed there
            continue
        brackets += f'<td><label>{language}</label>' \
                    f'{checkbox.html("brackets_"+language, checked="", label=f"place {language} in brackets ()")}' \
                    f'</td>\n'
    
    for language in text_block_names:
        if language in loaded_dict:
            song_text = "\n".join(loaded_dict[language]).rstrip("\n")
            content += f"""<td><textarea style="white-space:pre;" id ="{language}" name="{language}" rows="26" cols="47"  class="linked">{song_text}</textarea></td>\n"""
        else:
            content += f"""<td><textarea style="white-space:pre;" id ="{language}" name="{language}" rows="26" cols="47"  class="linked"></textarea></td>\n"""
    label_string = get_label_string()
    song_title = ""
    if "song_title" in loaded_dict:
        song_title = loaded_dict["song_title"]

    song_table = f"""            <table>
                <tr>{title}</tr>
                <tr>{brackets}</tr>
                <tr>{content}</tr>
            </table>
"""
    group_labels = f"""            <table><tr>
            <td><label>Possible Group labels:</label>
            {checkbox.html(name="groupLabelCheck", checked="checked", label="unique")}
            </td><td><label> {label_string}</label></td>
            </tr></table>"""

    # https://zerodevx.github.io/zero-md/
    markdown = """
                <div style="width:400px; max-height:700px; overflow:auto;">
                    <zero-md src="/static/kerk_naam1/readme_kerk_naam1.md">  
                        <!-- We apply this style template after defaults -->
                          <template data-append>
                            <style>
                              * {
                            margin-left: 20px;
                            margin-right: 20px;
                            text-align: left;
                              }
                            </style>
                          </template>
                    </zero-md>
                </div>"""

    html = f"""<!DOCTYPE html>
        <head>
        <title>kerk_naam1 - Multi Language Song Editor</title>
        <script type="module" src="/static/kerk_naam1/zero-md.js?register"></script>
        <script src="../static/jquery.min.js"></script>
        <script src="../static/main.js"></script>
        <link rel="stylesheet" href="/static/kerk_naam1/style.css">
        </head>
        <body  style="background-color:#DFE3D3 ;">
        <b><H0 >Multi Language Song Editor</H0></b>
        <form action=# method="post"  enctype="multipart/form-data">
        <table>
        <tr>
        <td valign="top">
            <label>Song name:</label>
            <input id="SongName" name="SongName" type="text" value="{song_title}" size="50" required />&nbsp;&nbsp;&nbsp;
            <label>Number of lines per slide:</label>
            <input id="NumLines" name="NumLines" type="number" value="5" min="1" max="10" step="1" required size="2" />&nbsp;&nbsp;&nbsp;
            <label>Number of characters per line:</label>
            <input id="NumChars" name="NumChars" type="number" value="48" min="20" max="60" step="1" required size="2" />
            {checkbox.html(name="punctuation", checked="checked", label="remove punctuation . , ; at the end of the sentence")}
            </br>
            {group_labels}
            </br> 
            {song_table}
            <br/>
            {button.html("buttonBlue", "pro", "Download .pro")}&nbsp
            {button.html("buttonGray", "json", "Download .json")}&nbsp
            {button.html("buttonGray", "rtf", "Download .rtf Textfile")}&nbsp
            <label for="file-upload" class="buttonGray">
                <input type="file" id="file-upload" name="action" value=load_json accept=".json;*.pro" onchange="form.submit()" />
                Import File
            </label>            

            </td>
            <td valign="top" align="left">
            <br/><br/><br/><br/>
            {markdown}
            </td>
            </tr>
            </table>
        </form>
    </body></html>"""
    return html
