import glob
import json
import os
import re
import sys

HEADING1 = "\n# "
HEADING2 = "\n## "
LINK_RE = re.compile("(\\[)([^\\[]*)(\\])(\\()([^\\)]*)(\\))")

def main(target_dir):

    # Iterate over files
    local_dir = os.path.dirname(__file__)
    for fname in glob.glob(os.path.join(local_dir, "*.md")):

        if "readme.md" == fname:
            continue

        # Output as a dictionary
        language_dict = dict()

        fp = os.path.join(local_dir, fname)
        # Load file
        with open(fp) as f:
            contents = "\n" + f.read(-1)

        pages = contents.split(HEADING1)

        assert "" == pages[0], "first page should be empty: %s, %s" % (fname, pages[0])
        
        for page in pages[1:]:

            page_sections = page.split(HEADING2)

            page_title = page_sections[0].strip()

            page_dict = dict()

            for page_section in page_sections[1:]:

                section_title_ending = page_section.find("\n")
                section_title = page_section[:section_title_ending]

                section_content = page_section[section_title_ending:].strip()

                assert section_title not in page_dict, "Duplicated heading: %s" % section_title

                # Verify no tags in the content
                assert "<" not in section_content
                assert ">" not in section_content

                # Convert links to a tags with regular expressions
                last_span = 0
                section_content_array = []
                for m in LINK_RE.finditer(section_content):
                    span = m.span()
                    section_content_array.append(section_content[last_span:span[0]])
                    section_content_array.append('<a href="%s">%s</a>' % (m.group(5), m.group(2)))
                    last_span = span[1]

                section_content_array.append(section_content[last_span:])
                new_content = "".join(section_content_array).strip()

                # Convert new lines to paragraphs
                if "\n\n" in new_content:
                    new_content = "<p>" + new_content.replace("\n\n", "</p><p>") + "</p>"
                new_content = new_content.replace("\n", " ")
                page_dict[section_title] = new_content
            language_dict[page_title] = page_dict

        # Save to disk
        target_fp = fname.replace(local_dir, target_dir).replace("//", "/").replace(".md", ".json")
        with open(target_fp, "w+") as f:
            json.dump(language_dict, f, indent=2, separators=(",", ":"))
        print("Wrote to %s" % target_fp)
        
        
if "__main__" == __name__:
    target_dir = sys.argv[1]
    main(target_dir)
