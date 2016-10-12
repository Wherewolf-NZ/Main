from bs4 import BeautifulSoup

class SpiderUtils:

    _scriptName = "Unnamed"

    #def SpiderUtils(self, scriptName=None):
    #    # constructor, set vars for each spider here
    #    self._scriptName = scriptName


    def log(self, message):
        # print message, also put file logging in here
        print(message)

    def do_match_for_soup(self, className):

        def do_match(tag):
            classes = tag.get('class', [])
            outTags = []
            for c in classes:
                if c.find(className) > -1:
                    outTags.append(c)
            return outTags
        return do_match


    def match_class(self, soup, className):
        return soup.find_all(self.do_match_for_soup(className))



    def escapeSpecialHtmlChars(text):

        text = text.strip()
        text = text.replace("Ã©", 'e')
        text = text.replace("Â", "")
        text = text.replace("&#8211;", "-")
        text = text.replace("&#8220;", "'")
        text = text.replace("&#8221;", "'")
        text = text.replace("&nbsp;", "")
        text = text.replace("&#039;", "'")
        text = text.replace("&amp;", "&")
        text = text.replace("â", "'")
        text = text.replace("â", "'")
        text = text.replace("â", "'")
        text = text.replace("&rsquo;", "'")
        text = text.replace("&rsaquo;", "-")
        text = text.replace("&#8217;", "'")
        text = text.replace("&#39;", "'")
        text = text.replace("&#039;", "'")
        text = text.replace("&quot;", "'")
        text = text.replace("&rdquo;", "'")
        text = text.replace("&amp;", "&")
        text = text.replace("&nbsp;", "")

        return text



