from xml.etree                       import ElementTree
from xml.etree.ElementTree           import Element
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Data_Feeds__Parser(Type_Safe):
    channel         : Element = None
    root            : Element = None
    xml_content     : str     = None

    def get_element_text(self, element: Element, tag: str, default: str = ""):    # Helper method to safely get text from an XML element
        elem = element.find(tag)
        return elem.text if elem is not None else default

    def setup(self, xml_content: str):                                            # Store and parse the XML content
        if xml_content:
            self.xml_content = xml_content
            self.root        = ElementTree.fromstring(xml_content)
            self.channel     = self.root.find('channel')
        return self