import tempfile, unittest, zipfile
from pathlib import Path
from main import build_epub, render_markdown
class EpubTests(unittest.TestCase):
    def test_heading_navigation(self):
        body,toc=render_markdown("# Hello\n\n## Details\n")
        self.assertEqual(len(toc),2)
        self.assertIn('id="hello"',body)
    def test_epub_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"book.epub"
            result=build_epub("# Hello\n\nText",out,"Title","Author")
            with zipfile.ZipFile(out) as z:
                self.assertEqual(z.namelist()[0],"mimetype")
                self.assertEqual(z.read("mimetype"),b"application/epub+zip")
                self.assertIn("OEBPS/content.opf",z.namelist())
            self.assertEqual(result["toc_entries"],1)
if __name__=="__main__": unittest.main()
