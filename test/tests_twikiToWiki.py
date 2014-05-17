from twikiToWiki import translate_twiki_to_wiki, convert_twiki_to_wikimedia
import unittest
import StringIO

class TestTranslationRules(unittest.TestCase):

    def test_TOC_removal(self):
        wiki = translate_twiki_to_wiki('%TOC%')
        self.assertEqual(wikimedia, '')
    def test_STARTINCLUDE_removal(self):
        wikimedia = translate_twiki_to_wiki('%STARTINCLUDE%')
        self.assertEqual(wikimedia, '')
    def test_STOPINCLUDE_removal(self):
        wikimedia = translate_twiki_to_wiki('%STOPINCLUDE%')
        self.assertEqual(wikimedia, '')
    def test_TOC_removal(self):
        wikimedia = translate_twiki_to_wiki('%TOC%')
        self.assertEqual(wikimedia, '')
    def test_META_removal(self):
        wikimedia = translate_twiki_to_wiki('%META foo%')
        self.assertEqual(wikimedia, '')
    def test_div_removal(self):
        wikimedia = translate_twiki_to_wiki('<div>foo</div>')
        self.assertEqual(wikimedia, 'foo')
    def test_noautolink_removal(self):
        wikimedia = translate_twiki_to_wiki('<noautolink>foo</noautolink>')
        self.assertEqual(wikimedia, 'foo')

    def test_bold(self):
        wikimedia = translate_twiki_to_wiki('foo *bold* string')
        self.assertEqual(wikimedia,"foo '''bold''' string")
    def test_partial_bold(self):
        wikimedia = translate_twiki_to_wiki('*foo* bar *baz*')
        self.assertEqual(wikimedia,"'''foo''' bar '''baz'''")
    def test_full_bold(self):
        wikimedia = translate_twiki_to_wiki('*foo bar*')
        self.assertEqual(wikimedia,"'''foo bar'''")

    def test_italic_bold(self):
        wikimedia = translate_twiki_to_wiki('foo __bold italic__ bar')
        self.assertEqual(wikimedia,"foo ''<b>bold italic</b>'' bar")
    def test_italic(self):
        wikimedia = translate_twiki_to_wiki('foo _italic_ bar')
        self.assertEqual(wikimedia,"foo ''italic'' bar")

    def test_monospaced_bold(self):
        wikimedia = translate_twiki_to_wiki('foo ==monospaced bold== bar')
        self.assertEqual(wikimedia,"foo '''<tt>monospaced bold</tt>''' bar")
    def test_monospaced(self):
        wikimedia = translate_twiki_to_wiki('foo =monospaced= bar')
        self.assertEqual(wikimedia,"foo <tt>monospaced</tt> bar")

    def test_h6(self):
        wikimedia = translate_twiki_to_wiki('---++++++ foo')
        self.assertEqual(wikimedia,"====== foo ======")
    def test_h5(self):
        wikimedia = translate_twiki_to_wiki('---+++++ foo')
        self.assertEqual(wikimedia,"===== foo =====")
    def test_h4(self):
        wikimedia = translate_twiki_to_wiki('---++++ foo')
        self.assertEqual(wikimedia,"==== foo ====")
    def test_h3(self):
        wikimedia = translate_twiki_to_wiki('---+++ foo')
        self.assertEqual(wikimedia,"=== foo ===")
    def test_h2(self):
        wikimedia = translate_twiki_to_wiki('---++ foo')
        self.assertEqual(wikimedia,"== foo ==")
    def test_h2_malformed(self):
        wikimedia = translate_twiki_to_wiki('----++ foo (misformed)')
        self.assertEqual(wikimedia,"== foo (misformed) ==")
    def test_h1(self):
        wikimedia = translate_twiki_to_wiki('---+ foo')
        self.assertEqual(wikimedia,"= foo =")
    def test_h1_notoc(self):
        wikimedia = translate_twiki_to_wiki('---+!! foo')
        self.assertEqual(wikimedia,"= foo =")

    def test_link_external(self):
        wikimedia = translate_twiki_to_wiki('link: [[http://foo.bar/][external link]]')
        self.assertEqual(wikimedia,'link: [http://foo.bar/ external link]')
    def test_link_external_camel_case_in_desc(self):
        wikimedia = translate_twiki_to_wiki('link: [[http://foo.bar/][CamelCase external link]]')
        self.assertEqual(wikimedia,'link: [http://foo.bar/ CamelCase external link]')
    def test_link_internal_explicit(self):
        wikimedia = translate_twiki_to_wiki('[[Foo]]')
        self.assertEqual(wikimedia, '[[Foo]]')
    def test_link_internal_explicit_anchor(self):
        wikimedia = translate_twiki_to_wiki('[[Foo#Bar]]')
        self.assertEqual(wikimedia, '[[Foo#Bar]]')
    def test_link_internal_explicit_aliased(self):
        wikimedia = translate_twiki_to_wiki('[[foo][foo bar]]')
        self.assertEqual(wikimedia, '[[foo | foo bar]]')
    def test_link_external_html(self):
        wikimedia = translate_twiki_to_wiki('link: <a target="_blank" href="https://www.foo.com">bar</a>')
        self.assertEqual(wikimedia,'link: [https://www.foo.com bar]')

    def test_bullet1(self):
        wikimedia = translate_twiki_to_wiki('   * foo')
        self.assertEqual(wikimedia,'* foo')
    def test_bullet1_tab(self):
        wikimedia = translate_twiki_to_wiki("\t* foo")
        self.assertEqual(wikimedia,'* foo')
    def test_bullet2(self):
        wikimedia = translate_twiki_to_wiki('      * foo')
        self.assertEqual(wikimedia,'** foo')
    def test_bullet1_tab(self):
        wikimedia = translate_twiki_to_wiki("\t\t* foo")
        self.assertEqual(wikimedia,'** foo')
    def test_bullet3(self):
        wikimedia = translate_twiki_to_wiki('         * foo')
        self.assertEqual(wikimedia,'*** foo')
    def test_bullet3_tab(self):
        wikimedia = translate_twiki_to_wiki("\t\t\t* foo")
        self.assertEqual(wikimedia,'*** foo')
    def test_bullet4(self):
        wikimedia = translate_twiki_to_wiki('            * foo')
        self.assertEqual(wikimedia,'**** foo')
    def test_bullet5(self):
        wikimedia = translate_twiki_to_wiki('               * foo')
        self.assertEqual(wikimedia,'***** foo')
    def test_bullet6(self):
        wikimedia = translate_twiki_to_wiki('                  * foo')
        self.assertEqual(wikimedia,'****** foo')
    def test_bullet7(self):
        wikimedia = translate_twiki_to_wiki('                     * foo')
        self.assertEqual(wikimedia,'******* foo')
    def test_bullet8(self):
        wikimedia = translate_twiki_to_wiki('                        * foo')
        self.assertEqual(wikimedia,'******** foo')
    def test_bullet9(self):
        wikimedia = translate_twiki_to_wiki('                           * foo')
        self.assertEqual(wikimedia,'********* foo')
    def test_bullet10(self):
        wikimedia = translate_twiki_to_wiki('                              * foo')
        self.assertEqual(wikimedia,'********** foo')

    def test_numbered1(self):
        wikimedia = translate_twiki_to_wiki('   1. foo')
        self.assertEqual(wikimedia,'# foo')
    def test_numbered1_tab(self):
        wikimedia = translate_twiki_to_wiki("\t1. foo")
        self.assertEqual(wikimedia,'# foo')
    def test_numbered2(self):
        wikimedia = translate_twiki_to_wiki('      1. foo')
        self.assertEqual(wikimedia,'## foo')
    def test_numbered2_tab(self):
        wikimedia = translate_twiki_to_wiki("\t\t1 foo")
        self.assertEqual(wikimedia,'## foo')
    def test_numbered3(self):
        wikimedia = translate_twiki_to_wiki('         1. foo')
        self.assertEqual(wikimedia,'### foo')
    def test_numbered3_tab(self):
        wikimedia = translate_twiki_to_wiki("\t\t\t1 foo")
        self.assertEqual(wikimedia,'### foo')
    def test_numbered4(self):
        wikimedia = translate_twiki_to_wiki('            1. foo')
        self.assertEqual(wikimedia,'#### foo')
    def test_numbered5(self):
        wikimedia = translate_twiki_to_wiki('               1. foo')
        self.assertEqual(wikimedia,'##### foo')
    def test_numbered6(self):
        wikimedia = translate_twiki_to_wiki('                  1. foo')
        self.assertEqual(wikimedia,'###### foo')
    def test_numbered7(self):
        wikimedia = translate_twiki_to_wiki('                     1. foo')
        self.assertEqual(wikimedia,'####### foo')
    def test_numbered8(self):
        wikimedia = translate_twiki_to_wiki('                        1. foo')
        self.assertEqual(wikimedia,'######## foo')
    def test_numbered9(self):
        wikimedia = translate_twiki_to_wiki('                           1. foo')
        self.assertEqual(wikimedia,'######### foo')
    def test_numbered10(self):
        wikimedia = translate_twiki_to_wiki('                              1. foo')
        self.assertEqual(wikimedia,'########## foo')

    def test_verbatim_pre(self):
        wikimedia = translate_twiki_to_wiki('<verbatim>foo</verbatim>')
        self.assertEqual(wikimedia,'<pre>foo</pre>')

    def test_definition_term(self):
        wikimedia = translate_twiki_to_wiki('   $ foo: bar')
        self.assertEqual(wikimedia,'; foo : bar')

    def test_spaces_removal(self):
        wikimedia = translate_twiki_to_wiki('    foo')
        self.assertEqual(wikimedia,'foo')

    def test_upper_case_text(self):
        tw = 'FOO bar BAZ'
        wikimedia = translate_twiki_to_wiki(tw)
        self.assertEqual(wikimedia, tw)

    def test_table(self):
        wikimedia = translate_twiki_to_wiki("""
| *L1* | *C* | *R* |
| A2 |  B2  |  C2 |
| A3 |  B3  |  C3 |""")
        self.assertEqual(wikimedia,"| '''L1''' | '''C* | *R''' |\n| A2 |  B2  |  C2 |\n| A3 |  B3  |  C3 |")

    def test_nowikiword(self):
        wikimedia = translate_twiki_to_wiki('''foo !bar''')
        self.assertEqual(wikimedia, 'foo bar')

    def test_searchmacro(self):
        wikimedia = translate_twiki_to_wiki('''%SEARCH{".*" web="%INCLUDINGWEB%" regex="on" nosearch="on" nototal="on" order="modified" limit="20" reverse="on"  format="| [[$topic][$topic(25, ...)]] | $wikiusername  | $date |" }%''')
        self.assertEqual(wikimedia, '')

    def test_camelcaseemail(self):
        tw = 'foo.bar@baz.com email'
        wikimedia = translate_twiki_to_wiki(tw)
        self.assertEqual(wikimedia, tw)

if __name__ == '__main__':
    unittest.main()