from pathlib import Path
import re
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'90-tools'))
from test_support import TARGET
from browser_support import browser_page


def luminance(color):
    values=[float(value) for value in re.findall(r'[\d.]+',color)]
    if len(values)>3 and values[3]!=1: raise AssertionError('Use opaque exercise colors; this check does not model compositing')
    channels=[value/255 for value in values[:3]]
    linear=[value/12.92 if value<=0.04045 else ((value+0.055)/1.055)**2.4 for value in channels]
    return sum(value*weight for value,weight in zip(linear,[0.2126,0.7152,0.0722]))


class CSSTests(unittest.TestCase):
    def test_responsive_geometry_and_content_changes(self):
        for width,columns in [(360,1),(768,2),(1200,3)]:
            with self.subTest(width=width),browser_page(TARGET,width=width) as page:
                cards=page.locator('.card').all(); self.assertEqual(len(cards),6)
                boxes=[card.bounding_box() for card in cards]
                first_row=sum(abs(box['y']-boxes[0]['y'])<2 for box in boxes)
                self.assertEqual(first_row,columns)
                self.assertGreaterEqual(boxes[0]['x'],16)
                if columns>1: self.assertGreaterEqual(boxes[1]['x']-boxes[0]['x']-boxes[0]['width'],12)
                geometry=page.locator('.page').bounding_box()
                self.assertLessEqual(geometry['width'],1120)
                self.assertLessEqual(abs(geometry['x']-(width-geometry['x']-geometry['width'])),2)
                page.locator('.card h2').first.evaluate('(element)=>element.textContent="longunbrokentoken".repeat(20)')
                if width==360: page.locator('html').evaluate('(element)=>element.style.fontSize="200%"')
                self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth-window.innerWidth'),1)

    def test_controls_focus_and_two_opaque_contrast_pairs(self):
        with browser_page(TARGET) as page:
            button=page.get_by_role('button',name='Search',exact=True)
            self.assertGreaterEqual(button.bounding_box()['height'],44)
            page.keyboard.press('Tab'); page.keyboard.press('Tab')
            self.assertEqual(page.locator(':focus').inner_text(),'Search')
            outline=button.evaluate('(element)=>({style:getComputedStyle(element).outlineStyle,width:parseFloat(getComputedStyle(element).outlineWidth)})')
            self.assertNotEqual(outline['style'],'none'); self.assertGreaterEqual(outline['width'],2)
            for selector in ['body','button']:
                colors=page.locator(selector).evaluate('(element)=>({text:getComputedStyle(element).color,background:getComputedStyle(element).backgroundColor})')
                first,second=sorted([luminance(colors['text']),luminance(colors['background'])])
                self.assertGreaterEqual((second+0.05)/(first+0.05),4.5)


if __name__=='__main__': unittest.main()
