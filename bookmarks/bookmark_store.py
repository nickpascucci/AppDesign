"""Storage for user bookmarks."""

__author__ = "Nick Pascucci (npascut1@gmail.com)"

# We could try to parse the HTML, but that would take much more time and effort.
import re
import bookmark

URL_RE = r'http(s{0,1})://.*?(?=")'
# Matches anything preceding a </a> tag. Results need to be pruned.
NAME_RE = r'.*(?=</(A|a)>)'
# Matches just the date string.
DATE_RE = r'(?<=(ADD_DATE|add_date)=")[0-9]*'

NETSCAPE_BKMK_RE = (r'<(DT|dt)><(A|a) (HREF|href)="%(URL_RE)s" '
                    r'(ADD_DATE|add_date)=.*>'
                    r'.*</(A|a)></(DT|dt)>') % locals()

URL_MATCHER = re.compile(URL_RE)
NAME_MATCHER = re.compile(NAME_RE)
DATE_MATCHER = re.compile(DATE_RE)

NETSCAPE_MATCHER = re.compile(NETSCAPE_BKMK_RE)

HEADER = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>"""

class BookmarkStore(dict):
    """Storage for user bookmarks."""
    
    def import_from_string(self, html_string):
        """Import bookmarks from an HTML string.

        @param html_string: A set of bookmarks as an HTML string.
        """
        matches = _get_bookmarks(html_string)
        for bookmark_string in matches:
            url = URL_MATCHER.search(bookmark_string).group()
            name = NAME_MATCHER.search(bookmark_string).group()
            name = name.split(">")[-1]  # Make up for regex deficiencies.
            date = DATE_MATCHER.search(bookmark_string).group().replace('"', '')
            if url and name and date:
                bkmk = bookmark.Bookmark(name, url, date)
                self[name] = bkmk

    def import_from_file(self, html_file):
        """Import bookmarks from an HTML file."""
        for line in html_file:
            self.import_from_string(line)

    def export_to_file(self, html_file):
        """Export bookmarks to an HTML file."""
        outfile = open(html_file, "w")
        outfile.write(self.export_to_string())
        outfile.close()

    def export_to_string(self):
        """Export bookmarks to an HTML string."""
        elements = [HEADER, "\n<DL>\n"]
        for bkmk in self.itervalues():
            elements.append("    <DT>")
            elements.append(bkmk.to_link())
            elements.append("</DT>\n")
        elements.append("</DL>")
        html = "".join(elements)
        return html

def _get_bookmarks(html_string):
    """Get a list of bookmark strings from an HTML string.

    @param html_string: A string of HTML-formatted bookmarks.
    @return: A list of all the matching strings.
    """
    matches = [m.group(0) for m in NETSCAPE_MATCHER.finditer(html_string)]
    return matches

if __name__ == "__main__":
    print NETSCAPE_BKMK_RE
