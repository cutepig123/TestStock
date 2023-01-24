import os

# fc-list :lang=zh
# https://blog.kelu.org/tech/2022/03/09/pandoc-md-to-pdf-with-chinese-charator.html
'''
/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc: Noto Serif CJK SC:style=Bold
/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc: Noto Serif CJK TC:style=Bold
/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc: Noto Serif CJK JP:style=Bold
/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc: Noto Serif CJK KR:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans CJK JP:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans CJK HK:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans CJK KR:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans CJK SC:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans CJK TC:style=Regular
/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc: Noto Serif CJK SC:style=Regular
/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc: Noto Serif CJK TC:style=Regular
/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc: Noto Serif CJK JP:style=Regular
/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc: Noto Serif CJK KR:style=Regular
/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf: Droid Sans Fallback:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans Mono CJK TC:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans Mono CJK SC:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans Mono CJK KR:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans Mono CJK HK:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans Mono CJK JP:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans Mono CJK SC:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans Mono CJK TC:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans Mono CJK HK:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans Mono CJK KR:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc: Noto Sans Mono CJK JP:style=Regular
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans CJK JP:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans CJK KR:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans CJK HK:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans CJK TC:style=Bold
/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc: Noto Sans CJK SC:style=Bold

 pandoc --pdf-engine=xelatex -V CJKmainfont="Noto Serif CJK SC" 1.md -o 1.pdf
'''

def MarkdownToPdf(MDFILE):
    
    # Work but not support chinese
    #command = f'/home/cutepig/.local/bin/mdpdf {MDFILE} -o {MDFILE}.pdf'
    
    # Good
    command = f'pandoc --pdf-engine=xelatex -V CJKmainfont="Noto Serif CJK SC"  {MDFILE} -o {MDFILE}.pdf'
    
    #command = f'/home/cutepig/.local/bin/md2pdf {MDFILE} {MDFILE}.pdf'
    
    print(command)
    os.system(command)
    

class MarkdownRowFormat:
    def __init__(self):
        pass

    def title(self, titles:list):
        l1 = '|' + '|'.join(titles) + '|\n'
        l2 = '|' + '|'.join(['----' for _ in titles])+ '|\n'
        return '\n' + l1 + l2

    def data_row(self, data:list):
        l1 = '|' + '|'.join(data) + '|\n'
        return l1
    
class MyPrinter:
    def __init__(self, MyWrite):
        self.is_head_printed = False
        self.row_formater = MarkdownRowFormat()
        self.MyWrite = MyWrite

    def print(self, d, **kwargs):
        all_data = {**d, **kwargs}
        if not self.is_head_printed:
            titles = [str(k) for k in all_data.keys()]
            self.MyWrite(self.row_formater.title(titles))
            
            self.is_head_printed = True

        values = [str(k) for k in all_data.values()]
        self.MyWrite(self.row_formater.data_row(values))
            