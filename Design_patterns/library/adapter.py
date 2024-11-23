import json
import xml.etree.ElementTree as ET

class BookDataAdapter:
    def __init__(self, format):
        self.format = format

    def parse(self, data):
        if self.format == "JSON":
            return json.loads(data)
        elif self.format == "XML":
            root = ET.fromstring(data)
            return [{"title": book.find("title").text, "author": book.find("author").text} for book in root]
        elif self.format == "CSV":
            return [dict(zip(["title", "author"], line.split(","))) for line in data.splitlines()]
        else:
            raise ValueError("Unsupported format")