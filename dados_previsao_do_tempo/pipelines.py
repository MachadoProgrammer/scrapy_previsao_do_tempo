# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
from dados_previsao_do_tempo.settings import XLSX_PATH

CAMPOS = ['dia_atual', 'temperatura_maxima_e_minima', 'condicao_atual']
class DadosXLSXPrevisaoDoTempoPipeline:
    planilha = None
    sheet = None

    def open_spider(self, spider):
        self.planilha = openpyxl.Workbook() 
        self.sheet = self.planilha.active
        self.sheet.append(CAMPOS) 



    def process_item(self, item, spider):
        adpater = ItemAdapter(item)
        self.sheet.append([adpater.get('dia_atual'), adpater.get('temperatura_maxima_e_minima'), adpater.get('condicao_atual')])
        
        return item
    
    def close_spider(self, spider):
        self.planilha.save(XLSX_PATH)
        self.planilha.close()