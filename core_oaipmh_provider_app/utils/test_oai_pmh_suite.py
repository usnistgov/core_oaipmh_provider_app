from django.test import override_settings, SimpleTestCase
import os
from xml_utils.xsd_tree.xsd_tree import XSDTree


@override_settings(
    SECRET_KEY='<secret_key>',
    ALLOWED_HOSTS=['testserver'],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join((os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))))
                    , 'templates')
            ],
        },
    ]
)
class TestOaiPmhSuite(SimpleTestCase):
    def check_tag_exist(self, text, check_tag):
        tag_found = False
        for tag in XSDTree.iterfind(text, './/{http://www.openarchives.org/OAI/2.0/}' + check_tag):
            tag_found = True
        self.assertTrue(tag_found)

    def check_tag_error_code(self, text, error):
        self.check_tag_exist(text, 'error')
        for tag in XSDTree.iterfind(text, './/{http://www.openarchives.org/OAI/2.0/}error'):
            self.assertEqual(tag.attrib['code'], error)

    def check_tag_count(self, text, checkTag, number):
        count = 0
        for tag in XSDTree.iterfind(text, './/{http://www.openarchives.org/OAI/2.0/}' + checkTag):
            count += 1
        self.assertEquals(number, count)