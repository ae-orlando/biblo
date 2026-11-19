from pathlib import Path
import sys
import unittest
from playwright.sync_api import expect
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'90-tools'))
from test_support import TARGET
from browser_support import browser_page


class HTMLTests(unittest.TestCase):
    def test_semantics_labels_and_keyboard_entry(self):
        with browser_page(TARGET) as page:
            self.assertEqual(page.locator('html').get_attribute('lang'),'en')
            self.assertEqual(page.get_by_role('main').count(),1)
            self.assertEqual(page.get_by_role('heading',level=1).count(),1)
            self.assertTrue(page.title().strip())
            ids=page.locator('[id]').evaluate_all('(elements)=>elements.map(element=>element.id)')
            self.assertEqual(len(ids),len(set(ids)))
            for label in ['Full name','Email','Track','Morning','Evening','I agree to the training terms']:
                self.assertEqual(page.get_by_label(label,exact=True).count(),1,label)
            self.assertEqual(page.locator('fieldset legend').count(),1)
            self.assertEqual(page.locator('table caption').count(),1)
            self.assertGreaterEqual(page.locator('th[scope]').count(),2)
            self.assertGreaterEqual(page.locator('img').count(),1)
            for image in page.locator('img').all(): self.assertIsNotNone(image.get_attribute('alt'))
            page.keyboard.press('Tab')
            self.assertEqual(page.locator(':focus').get_attribute('href'),'#main')

    def test_native_validation_and_actual_local_post(self):
        with browser_page(TARGET) as page:
            initial=page.url
            button=page.get_by_role('button',name='Register',exact=True)
            button.click()
            self.assertEqual(page.url,initial)
            page.get_by_label('Full name',exact=True).fill('Learner')
            email=page.get_by_label('Email',exact=True); email.fill('not-an-email')
            self.assertTrue(email.evaluate('(element)=>element.validity.typeMismatch'))
            email.fill('learner@example.test')
            page.get_by_label('Track',exact=True).select_option('python')
            page.get_by_label('Morning',exact=True).check()
            button.click()
            self.assertEqual(page.url,initial,'required terms must prevent a premature submission')
            page.get_by_label('I agree to the training terms',exact=True).check()
            button.click()
            expect(page.get_by_role('heading',name='Training preview',exact=True)).to_be_visible()
            text=page.locator('pre').inner_text()
            for value in ['name: Learner','email: learner@example.test','track: python','session: morning','terms: agreed']:
                self.assertIn(value,text)


if __name__=='__main__': unittest.main()
