import glob
import json
import os
import re
import sys

from googletrans import Translator


HEADING1 = "\n# "
HEADING2 = "\n## "
NEWLINE = "\n"
LINK_RE = re.compile("(\\[)([^\\[]*)(\\])(\\()([^\\)]*)(\\))")

DEBUG = False

AUTHORITATIVE_SOURCE = "en-gb.md"

def translate(text, language):
    t = Translator()
    if DEBUG:
        print(language)
    obj = t.translate(text, src='en', dest=language)
    if DEBUG:
        print(obj)
    return obj.text;

def translate_content(language):

    languageBigram = language[:2]

    # Iterate over files
    local_dir = os.path.dirname(__file__)
    fp = os.path.join(local_dir, AUTHORITATIVE_SOURCE)

    # Load file
    with open(fp) as f:
        contents = "\n" + f.read(-1)

    output = []

    pages = contents.split(HEADING1)

    assert "" == pages[0], "first page should be empty"
    
    for page in pages[1:]:

        page_sections = page.split(HEADING2)

        output.append(HEADING1 + page_sections[0])

        for page_section in page_sections[1:]:

            section_title_ending = page_section.find("\n")
            section_title = page_section[:section_title_ending]

            section_content = page_section[section_title_ending:]

            # eat up the leading and trailing newlines, which the translator gobbles up

            leading_newlines = ""
            trailing_newlines = ""
            while section_content.startswith(NEWLINE):
                leading_newlines += NEWLINE
                section_content = section_content[1:]
            while section_content.endswith(NEWLINE):
                trailing_newlines += NEWLINE
                section_content = section_content[:-1]

            translated = ""

            # Convert links to a tags with regular expressions
            last_span = 0
            section_content_array = []
            for m in LINK_RE.finditer(section_content):
                span = m.span()
                translated += translate(section_content[last_span:span[0]], languageBigram)
                translated += "[%s](%s)" % (translate(m.group(2), languageBigram), m.group(5))
                last_span = span[1]

            rest = section_content[last_span:]
            if DEBUG:
                print(rest)
            temp = translate(rest, languageBigram)
            if DEBUG: 
                print(temp)
            translated += temp

            output.append(HEADING2 + section_title + leading_newlines + translated + trailing_newlines)
            


    # Save to disk
    target = os.path.join(local_dir, language + ".md")
    with open(target, "w+") as f:
        f.write("".join(output))
    print("Translated to %s" % language)
        
if "__main__" == __name__:
    assert False "deal with gobbling of spaces around sentences"
    #translate_content("pt-pt")
    #translate_content("fr-fr")
    translate_content("de-de")
    translate_content("es-es")
