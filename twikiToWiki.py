#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from flask import Flask, render_template, request
from flask.ext.wtf import Form
from wtforms import SubmitField
from wtforms.fields import StringField
from wtforms.widgets import TextArea


app = Flask(__name__)
app.secret_key = 'you-will-never-guess'

# List of rules to convert twiki lines to mediawiki, many/most
# borrowed from TWiki::Plugins::EditSyntaxPlugin.
# See http://twiki.org/cgi-bin/view/Plugins/MediawikiEditSyntaxRegex
rules = (

    #
    # Wiki Tags
    #

    (r'''^%TOC%''', r''),  # Remove Table of contents
    (r'''^%STARTINCLUDE%''', r''),
    (r'''^%STOPINCLUDE%''', r''),
    (r'''^%SEARCH{[^}]*}%''', r''), # Remove SEARCH macro
    (r'''^%META.*''', r''),  # Remove meta tags
    (r'''</div>''', r''),  # Remove div tags
    (r'''<div(?: [^>]*)?>''', r''),  # Remove div tags
    (r'''\!([A-Z]{1}\w+?[A-Z]{1})''', r"""\1"""),  # remove ! from Twiki words.

    # Formatting
    (r'''(^|[\s\(])\*([^ ].*?[^ ])\*([\s\)\.\,\:\;\!\?]|$)''', r"""\1'''\2'''\3"""), # bold
    (r'''(^|[\s\(])\_\_([^ ].*?[^ ])\_\_([\s\)\.\,\:\;\!\?]|$)''', r"""\1''<b>\2</b>''\3"""),  # italic bold
    (r'''(^|[\s\(])\_([^ ].*?[^ ])\_([\s\)\.\,\:\;\!\?]|$)''', r"""\1''\2''\3"""), # italic
    (r'''(^|[\s\(])==([^ ].*?[^ ])==([\s\)\.\,\:\;\!\?]|$)''', r"""\1'''<tt>\2</tt>'''\3""" ),  # monospaced bold
    (r'''(^|[\s\(])=([^ ].*?[^ ])=([\s\)\.\,\:\;\!\?]|$)''', r"""\1<tt>\2</tt>\3""" ),  # monospaced
    (r'''(^|[\n\r])---\+\+\+\+\+\+([^\n\r]*)''', r"""\1======\2 ======"""),  # H6
    (r'''(^|[\n\r])---\+\+\+\+\+([^\n\r]*)''', r"""\1=====\2 ====="""),  # H5
    (r'''(^|[\n\r])---\+\+\+\+([^\n\r]*)''', r"""\1====\2 ===="""),  # H4
    (r'''(^|[\n\r])---\+\+\+([^\n\r]*)''', r"""\1===\2 ==="""),  # H3
    (r'''(^|[\n\r])---\+\+([^\n\r]*)''', r"""\1==\2 =="""),  # H2
    (r'''(^|[\n\r])----\+\+([^\n\r]*)''', r"""\1==\2 =="""),  # H2 (slightly misformed variant)
    (r'''(^|[\n\r])---\+[!]*([^\n\r]*)''', r"""\1=\2 ="""),  # H1
    # Links
    (r'''\[\[(https?:.*?)]\[(.*?)]]''', r"""[\1 \2]"""),  # external link [[http:...][label]]
    (r'''\[\[((?!http).*?)]\[(.*?)]]''', r"""[[\1 | \2]]"""),  # internal link [[http:...][label]]
    # Bullets
    (r'''(^|[\n\r])[ ]{3}\* ''', r"""\1* """),  # level 1 bullet
    (r'''(^|[\n\r])[\t]{1}\* ''', r"""\1* """),  # level 1 bullet: Handle single tabs (from twiki .txt files)
    (r'''(^|[\n\r])[ ]{6}\* ''', r"""\1** """),  # level 2 bullet
    (r'''(^|[\n\r])[\t]{2}\* ''', r"""\1** """),  # level 1 bullet: Handle double tabs
    (r'''(^|[\n\r])[ ]{9}\* ''', r"""\1*** """),  # level 3 bullet
    (r'''(^|[\n\r])[\t]{3}\* ''', r"""\1*** """),  # level 3 bullet: Handle tabbed version
    (r'''(^|[\n\r])[ ]{12}\* ''', r"""\1**** """),  # level 4 bullet
    (r'''(^|[\n\r])[ ]{15}\* ''', r"""\1***** """),  # level 5 bullet
    (r'''(^|[\n\r])[ ]{18}\* ''', r"""\1****** """),  # level 6 bullet
    (r'''(^|[\n\r])[ ]{21}\* ''', r"""\1******* """),  # level 7 bullet
    (r'''(^|[\n\r])[ ]{24}\* ''', r"""\1******** """),  # level 8 bullet
    (r'''(^|[\n\r])[ ]{27}\* ''', r"""\1********* """),  # level 9 bullet
    (r'''(^|[\n\r])[ ]{30}\* ''', r"""\1********** """),  # level 10 bullet
    # Numbering
    (r'''(^|[\n\r])[ ]{3}[0-9]\.? ''', r"""\1# """),  # level 1 bullet
    (r'''(^|[\n\r])[\t]{1}[0-9]\.? ''', r"""\1# """),  # level 1 bullet: handle 1 tab
    (r'''(^|[\n\r])[ ]{6}[0-9]\.? ''', r"""\1## """),  # level 2 bullet
    (r'''(^|[\n\r])[\t]{2}[0-9]\.? ''', r"""\1## """),  # level 2 bullet: handle 2 tabs
    (r'''(^|[\n\r])[ ]{9}[0-9]\.? ''', r"""\1### """),  # level 3 bullet
    (r'''(^|[\n\r])[\t]{3}[0-9]\.? ''', r"""\1### """),  # level 3 bullet: handle 3 tabs
    (r'''(^|[\n\r])[ ]{12}[0-9]\.? ''', r"""\1#### """),  # level 4 bullet
    (r'''(^|[\n\r])[ ]{15}[0-9]\.? ''', r"""\1##### """),  # level 5 bullet
    (r'''(^|[\n\r])[ ]{18}[0-9]\.? ''', r"""\1###### """),  # level 6 bullet
    (r'''(^|[\n\r])[ ]{21}[0-9]\.? ''', r"""\1####### """),  # level 7 bullet
    (r'''(^|[\n\r])[ ]{24}[0-9]\.? ''', r"""\1######## """),  # level 8 bullet
    (r'''(^|[\n\r])[ ]{27}[0-9]\.? ''', r"""\1######### """),  # level 9 bullet
    (r'''(^|[\n\r])[ ]{30}[0-9]\.? ''', r"""\1########## """),  # level 10 bullet
    (r'''(^|[\n\r])[ ]{3}\$ ([^:]*)''', r"""\1; \2 """), # $ definition: term
    (r'''^[\s]+''', r''),
)

def translate_twiki_to_wiki(line):
    """Converts a line from TWiki to Mediawiki syntaxes"""
    for r in rules:
        search, replace = r
        line = re.sub(search, replace, line)
    return line

def  convert_twiki_to_wikimedia(text):
    """Converts a text from TWiki syntax to Mediawiki's"""

    converted = ''
    converting_table = False
    for line in text.splitlines():
        # Handle Table Endings
        if converting_table:
            if re.match(r'''^[^\|]''', line):
                converted += "|}\n\n"
                converting_table = False

        # Handle Tables
        if re.match(r'''\|''', line):
            if not converting_table:
                converted += '{| cellpadding="5" cellspacing="0" border="1"' + "\n"
                converting_table = True

            # start new row
            converted += "|-\n"

            arAnswer = re.sub(r'''\|$''', r"", line)  # remove end pipe.

            text = '||'.join(map(translate_twiki_to_wiki, re.split(r'\|', arAnswer[1:])))
            converted += '|' + text + "\n"

        # Handle blank lines..
        elif re.match(r'^$', line):
            converted += line + "\n"

        # Handle anything else...
        else:
            text = translate_twiki_to_wiki(line)
            converted += text + "\n"

    # Get rid of the Categories header
    converted = re.sub(r'''----\n<b>Categories for.*</b>''', r'', converted)
    return converted

class ConvertToWikiForm(Form):
    input = StringField(u'Text', widget=TextArea())
    submit = SubmitField("Send")

@app.route('/', methods=['GET', 'POST'])
def form():
    convert_to_wiki_form = ConvertToWikiForm()
    if request.method == 'POST':
        input_text = request.form['twikiInput']
        wikimedia_text = convert_twiki_to_wikimedia(input_text)
        return render_template('index.html', form=convert_to_wiki_form, input=input_text, output=wikimedia_text)
    elif request.method == 'GET':
        return render_template('index.html', form=convert_to_wiki_form, output="Default output")

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')