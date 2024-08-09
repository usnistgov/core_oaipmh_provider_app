from django.test import SimpleTestCase

from xml_utils.xsd_tree.xsd_tree import XSDTree


class TestOaiPmhSuite(SimpleTestCase):
    """Test OaiPmh Suite"""

    def check_tag_exist(self, text, check_tag):
        """check_tag_exist

        Args:
            text:
            check_tag:

        Returns:
        """
        tag_found = False
        for tag in XSDTree.iterfind(
            text, ".//{http://www.openarchives.org/OAI/2.0/}" + check_tag
        ):
            tag_found = True
        self.assertTrue(tag_found)

    def check_tag_error_code(self, text, error):
        """check_tag_exist

        Args:
            text:
            error:

        Returns:
        """
        self.check_tag_exist(text, "error")
        for tag in XSDTree.iterfind(
            text, ".//{http://www.openarchives.org/OAI/2.0/}error"
        ):
            self.assertEqual(tag.attrib["code"], error)

    def check_tag_count(self, text, check_tag, number):
        """check_tag_exist

        Args:
            text:
            check_tag:
            number:

        Returns:
        """
        count = 0
        for tag in XSDTree.iterfind(
            text, ".//{http://www.openarchives.org/OAI/2.0/}" + check_tag
        ):
            count += 1
        self.assertEqual(number, count)
