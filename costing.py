import tkinter as tk
from tkinter import ttk
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import os
import platform

class FinishedGood:
    def __init__(self, name, raw_materials, packing_materials, labor_cost, retail_price, standard_unit_per_batch):
        self.name = name
        self.raw_materials = raw_materials
        self.packing_materials = packing_materials
        self.labor_cost = labor_cost
        self.retail_price = retail_price
        self.standard_unit_per_batch = standard_unit_per_batch
        self.total_raw_material_cost = sum(item['Amount'] for item in raw_materials)
        self.total_packing_material_cost = sum(item['Amount'] for item in packing_materials)
    
    def calculate_costs(self):
        raw_material_cost_per_unit = self.total_raw_material_cost / self.standard_unit_per_batch
        packing_material_cost_per_unit = self.total_packing_material_cost / self.standard_unit_per_batch
        total_prime_cost_per_unit = raw_material_cost_per_unit + packing_material_cost_per_unit + self.labor_cost
        gross_margin_per_unit = self.retail_price - total_prime_cost_per_unit
        return raw_material_cost_per_unit,packing_material_cost_per_unit, total_prime_cost_per_unit, gross_margin_per_unit

# Sample data for finished goods
finished_goods_data = [
    {
        'name': 'Kiwi Shoepolish - Black - Summer 90ml',
        'raw_materials': [
            {'Name': 'Paraffin 60/62', 'Consumption': 28.0, 'Rate': 699.00, 'Amount': 28 * 699.00},
            {'Name': 'Carnauba F.Grey', 'Consumption': 8.80, 'Rate': 2494.00, 'Amount': 8.8 * 2494.00},
            {'Name': 'LICOWAX "O"', 'Consumption': 8.80, 'Rate': 4117.00, 'Amount': 8.80 * 4117.00},
            {'Name': 'LICOWAX "S"', 'Consumption': 0.75, 'Rate': 4028.00, 'Amount': 0.75 * 4028.00},
            {'Name': 'Multy Wax ML-445', 'Consumption': 1.70, 'Rate': 1154.00, 'Amount': 1.7 * 1154.00},
            {'Name': 'Nitrobenzene', 'Consumption': 1.20, 'Rate': 1250.00, 'Amount': 1.2 * 1250.00},
            {'Name': 'Dye Fluid Black', 'Consumption': 5.07, 'Rate': 4162.46, 'Amount': 5.07 * 4162.46},
            {'Name': 'White Spirit', 'Consumption': 105.71, 'Rate': 212.29, 'Amount': 105.71 * 212.29},
            {'Name': 'Turpentine Oil', 'Consumption': 12.9, 'Rate': 1410.00, 'Amount': 12.9 * 1410.00},
        ],
        'packing_materials': [
            {'Name': 'BODY SHOE POLISH 90ML', 'Consumption': 2592, 'Rate': 25.25, 'Amount': 2592 * 25.25},
            {'Name': 'LIDS SHOE POLISH 90ML BLACK', 'Consumption': 2592, 'Rate': 25.24, 'Amount': 2592 * 25.24},
            {'Name': 'ALUMINUM FOIL SHOE POLISH 90ML', 'Consumption': 2592, 'Rate': 3.05, 'Amount': 2592 * 3.05},
            {'Name': 'CARTON 1 DZ SHOE POLISH 90ML BLACK', 'Consumption': 216, 'Rate': 34.87, 'Amount': 216 * 34.87},
            {'Name': 'CARTON 1 GRS MASTER SHOE POLISH 90ML', 'Consumption': 18, 'Rate': 121.23, 'Amount': 18 * 121.23},
            {'Name': 'TAPE ROLL', 'Consumption': 1, 'Rate': 125.00, 'Amount': 1 * 125.00},
            {'Name': 'ROUGH PAPER 90ML', 'Consumption': 864, 'Rate': 0.33, 'Amount': 864 * 0.33},
        ],
        'labor_cost': 3.55,
        'retail_price': 635.59,
        'standard_unit_per_batch': 2592
    },
    {
        'name': 'Kiwi Shoepolish - Dark Tan - Summer 90ml',
        'raw_materials': [
            {'Name': 'Paraffin 60/62', 'Consumption': 28.00, 'Rate': 699.00, 'Amount': 28 * 699.00},
            {'Name': 'Carnauba F.Grey', 'Consumption': 8.20, 'Rate': 2494.00, 'Amount': 8.20 * 2494.00},
            {'Name': 'LICOWAX "O"', 'Consumption': 8.20, 'Rate': 4117.00, 'Amount': 8.20 * 4117.00},
            {'Name': 'LICOWAX "S"', 'Consumption': 1.70, 'Rate': 4028.00, 'Amount': 1.70 * 4028.00},
            {'Name': 'Multy Wax ML-445', 'Consumption': 1.70, 'Rate': 1154.00, 'Amount': 1.70 * 1154.00},
            {'Name': 'Nitrobenzene', 'Consumption': 1.20, 'Rate': 1250.00, 'Amount': 1.2 * 1250.00},
            {'Name': 'Dye Fluid Dark Tan', 'Consumption': 2.00, 'Rate': 1801.51, 'Amount': 2.00 * 1801.51},
            {'Name': 'White Spirit', 'Consumption': 105.71, 'Rate': 212.29, 'Amount': 105.71 * 212.29},
            {'Name': 'Turpentine Oil', 'Consumption': 12.90, 'Rate': 1410.00, 'Amount': 12.90 * 1410.00},
        ],
        'packing_materials': [
            {'Name': 'BODY SHOE POLISH 90ML', 'Consumption': 2448, 'Rate': 25.25, 'Amount': 2448 * 25.25},
            {'Name': 'LIDS SHOE POLISH 90ML BLACK', 'Consumption': 2448, 'Rate': 25.25, 'Amount': 2448 * 25.24},
            {'Name': 'ALUMINUM FOIL SHOE POLISH 90ML', 'Consumption': 2448, 'Rate': 3.05, 'Amount': 2448 * 3.05},
            {'Name': 'CARTON 1 DZ SHOE POLISH 90ML BLACK', 'Consumption': 204, 'Rate': 34.87, 'Amount': 204 * 34.87},
            {'Name': 'CARTON 1 GRS MASTER SHOE POLISH 90ML', 'Consumption': 17, 'Rate': 121.23, 'Amount': 17 * 121.23},
            {'Name': 'TAPE ROLL', 'Consumption': 1, 'Rate': 125.00, 'Amount': 1 * 125.00},
            {'Name': 'ROUGH PAPER 90ML', 'Consumption': 816, 'Rate': 0.33, 'Amount': 816 * 0.33},
        ],
        'labor_cost': 3.55,
        'retail_price': 635.59,
        'standard_unit_per_batch': 2448,
    },
    {
        'name': 'Kiwi Shoepolish - Black - Summer 45ml',
        'raw_materials': [
            {'Name': 'Paraffin 60/62', 'Consumption': 28.00, 'Rate': 699.00, 'Amount': 28 * 699.00},
            {'Name': 'Carnauba F.Grey', 'Consumption': 8.80, 'Rate': 2494.00, 'Amount': 8.8 * 2494.00},
            {'Name': 'LICOWAX "O"', 'Consumption': 8.80, 'Rate': 4117.00, 'Amount': 8.80 * 4117.00},
            {'Name': 'LICOWAX "S"', 'Consumption': 0.75, 'Rate': 4028.00, 'Amount': 0.75 * 4028.00},
            {'Name': 'Multy Wax ML-445', 'Consumption': 1.70, 'Rate': 1154.00, 'Amount': 1.7 * 1154.00},
            {'Name': 'Nitrobenzene', 'Consumption': 1.20, 'Rate': 1250.00, 'Amount': 1.2 * 1250.00},
            {'Name': 'Dye Fluid Black', 'Consumption': 5.07, 'Rate': 4162.46, 'Amount': 5.07 * 4162.46},
            {'Name': 'White Spirit', 'Consumption': 105.71, 'Rate': 212.29, 'Amount': 105.71 * 212.29},
            {'Name': 'Turpentine Oil', 'Consumption': 12.9, 'Rate': 1410.00, 'Amount': 12.9 * 1410.00},
        ],
        'packing_materials': [
            {'Name': 'BODY SHOE POLISH 45ML', 'Consumption': 4949, 'Rate': 13.71, 'Amount': 4949 * 13.71},
            {'Name': 'LIDS SHOE POLISH 45ML BLACK', 'Consumption': 4949, 'Rate': 11.78, 'Amount': 4949 * 11.78},
            {'Name': 'ALUMINUM FOIL SHOE POLISH 90ML', 'Consumption': 4949, 'Rate': 2.21, 'Amount': 4949 * 2.21},
            {'Name': 'CARTON 2 DZ SHOE POLISH 45ML BLACK', 'Consumption': 207, 'Rate': 35.00, 'Amount': 207 * 35.00},
            {'Name': 'CARTON 2 GRS MASTER SHOE POLISH 45ML', 'Consumption': 18, 'Rate': 155.41, 'Amount': 18 * 155.41},
            {'Name': 'TAPE ROLL', 'Consumption': 1, 'Rate': 125.00, 'Amount': 1 * 125.00},
            {'Name': 'ROUGH PAPER 45ML', 'Consumption': 828, 'Rate': 0.33, 'Amount': 828 * 0.33},
        ],
        'labor_cost': 1.83,
        'retail_price': 377.12,
        'standard_unit_per_batch': 4949,
    },
    {
        'name': 'Kiwi Shoepolish - Dark Tan - Summer 45ml',
        'raw_materials': [
            {'Name': 'Paraffin 60/62', 'Consumption': 28.00, 'Rate': 699.00, 'Amount': 28 * 699.00},
            {'Name': 'Carnauba F.Grey', 'Consumption': 8.20, 'Rate': 2494.00, 'Amount': 8.20 * 2494.00},
            {'Name': 'LICOWAX "O"', 'Consumption': 8.20, 'Rate': 4117.00, 'Amount': 8.20 * 4117.00},
            {'Name': 'LICOWAX "S"', 'Consumption': 1.70, 'Rate': 4028.00, 'Amount': 1.70 * 4028.00},
            {'Name': 'Multy Wax ML-445', 'Consumption': 1.70, 'Rate': 1154.00, 'Amount': 1.70 * 1154.00},
            {'Name': 'Nitrobenzene', 'Consumption': 1.20, 'Rate': 1250.00, 'Amount': 1.2 * 1250.00},
            {'Name': 'Dye Fluid Dark Tan', 'Consumption': 2.00, 'Rate': 1801.51, 'Amount': 2.00 * 1801.51},
            {'Name': 'White Spirit', 'Consumption': 105.71, 'Rate': 212.29, 'Amount': 105.71 * 212.29},
            {'Name': 'Turpentine Oil', 'Consumption': 12.90, 'Rate': 1410.00, 'Amount': 12.90 * 1410.00},
        ],
        'packing_materials': [
            {'Name': 'BODY SHOE POLISH 45ML', 'Consumption': 4854, 'Rate': 13.71, 'Amount': 4854 * 13.71},
            {'Name': 'LIDS SHOE POLISH 45ML D/Tan', 'Consumption': 4854, 'Rate': 11.78, 'Amount': 4854 * 11.78},
            {'Name': 'ALUMINUM FOIL SHOE POLISH 45ML', 'Consumption': 4854, 'Rate': 2.21, 'Amount': 4854 * 2.21},
            {'Name': 'CARTON 2 DZ SHOE POLISH 45ML BLACK', 'Consumption': 203, 'Rate': 35.00, 'Amount': 203 * 35},
            {'Name': 'CARTON 2 GRS MASTER SHOE POLISH 45ML', 'Consumption': 17, 'Rate': 155.41, 'Amount': 17 * 155.41},
            {'Name': 'TAPE ROLL', 'Consumption': 1, 'Rate': 125.00, 'Amount': 1 * 125.00},
            {'Name': 'ROUGH PAPER 45ML', 'Consumption': 812, 'Rate': 0.33, 'Amount': 812 * 0.33},
        ],
        'labor_cost': 1.83,
        'retail_price': 377.12,
        'standard_unit_per_batch': 4949,
    },    
    {
        'name': 'Kiwi Shoepolish - Black - Summer 20ml',
        'raw_materials': [
            {'Name': 'Paraffin 60/62', 'Consumption': 42.00, 'Rate': 699.00, 'Amount': 42 * 699.00},
            {'Name': 'Carnauba F.Grey', 'Consumption': 13.20, 'Rate': 2494.00, 'Amount': 13.20 * 2494.00},
            {'Name': 'LICOWAX "O"', 'Consumption': 13.20, 'Rate': 4117.00, 'Amount': 13.20 * 4117.00},
            {'Name': 'LICOWAX "S"', 'Consumption': 1.13, 'Rate': 4028.00, 'Amount': 1.13 * 4028.00},
            {'Name': 'Multy Wax ML-445', 'Consumption': 2.55, 'Rate': 1154.00, 'Amount': 2.55 * 1154.00},
            {'Name': 'Nitrobenzene', 'Consumption': 1.80, 'Rate': 1250.00, 'Amount': 1.80 * 1250.00},
            {'Name': 'Dye Fluid Black', 'Consumption': 7.61, 'Rate': 4162.46, 'Amount': 7.61 * 4162.46},
            {'Name': 'White Spirit', 'Consumption': 158.56, 'Rate': 212.29, 'Amount': 158.56 * 212.29},
            {'Name': 'Turpentine Oil', 'Consumption': 19.35, 'Rate': 1410.00, 'Amount': 19.35 * 1410.00},
        ],
        'packing_materials': [
            {'Name': 'BODY SHOE POLISH 20ML', 'Consumption': 19008, 'Rate': 8.98, 'Amount': 19008 * 8.98},
            {'Name': 'LIDS SHOE POLISH 20ML BLACK', 'Consumption': 19008, 'Rate': 7.10, 'Amount': 19008 * 7.10},
            {'Name': 'ALUMINUM FOIL SHOE POLISH 20ML', 'Consumption': 19008, 'Rate': 1.14, 'Amount': 19008 * 1.14},
            {'Name': 'CARTON 3 DZ SHOE POLISH 20ML BLACK', 'Consumption': 528, 'Rate': 22.17, 'Amount': 528 * 22.17},
            {'Name': 'CARTON 2 GRS MASTER SHOE POLISH 20ML', 'Consumption': 66, 'Rate': 76.00, 'Amount': 66 * 76.00},
            {'Name': 'TAPE ROLL', 'Consumption': 3, 'Rate': 125.00, 'Amount': 2 * 125.00},
            {'Name': 'ROUGH PAPER 20ML', 'Consumption': 3168, 'Rate': 0.33, 'Amount': 3168 * 0.33},
        ],
        'labor_cost': 1.45,
        'retail_price': 194.92,
        'standard_unit_per_batch': 19008,
    },
    {
        'name': 'Kiwi Shoepolish - Dark Tan - Summer 20ml',
        'raw_materials': [
            {'Name': 'Paraffin 60/62', 'Consumption': 42.00, 'Rate': 699.00, 'Amount': 42 * 699.00},
            {'Name': 'Carnauba F.Grey', 'Consumption': 12.30, 'Rate': 2494.00, 'Amount': 12.30 * 2494.00},
            {'Name': 'LICOWAX "O"', 'Consumption': 12.30, 'Rate': 4117.00, 'Amount': 12.30 * 4117.00},
            {'Name': 'LICOWAX "S"', 'Consumption': 1.13, 'Rate': 4028.00, 'Amount': 1.13 * 4028.00},
            {'Name': 'Multy Wax ML-445', 'Consumption': 2.55, 'Rate': 1154.00, 'Amount': 2.55 * 1154.00},
            {'Name': 'Nitrobenzene', 'Consumption': 1.80, 'Rate': 1250.00, 'Amount': 1.80 * 1250.00},
            {'Name': 'Dye Fluid Dark Tan', 'Consumption': 3.00, 'Rate': 1801.51, 'Amount': 3.00 * 1801.51},
            {'Name': 'White Spirit', 'Consumption': 158.56, 'Rate': 212.29, 'Amount': 158.56 * 212.29},
            {'Name': 'Turpentine Oil', 'Consumption': 19.35, 'Rate': 1410.00, 'Amount': 19.35 * 1410.00},
        ],
        'packing_materials': [
            {'Name': 'BODY SHOE POLISH 20ML', 'Consumption': 18638, 'Rate': 8.98, 'Amount': 18638 * 8.98},
            {'Name': 'LIDS SHOE POLISH 20ML BLACK', 'Consumption': 18638, 'Rate': 7.10, 'Amount': 18638 * 7.10},
            {'Name': 'ALUMINUM FOIL SHOE POLISH 20ML', 'Consumption': 18638, 'Rate': 1.14, 'Amount': 18638 * 1.14},
            {'Name': 'CARTON 3 DZ SHOE POLISH 20ML BLACK', 'Consumption': 518, 'Rate': 22.17, 'Amount': 528 * 22.17},
            {'Name': 'CARTON 2 GRS MASTER SHOE POLISH 20ML', 'Consumption': 65, 'Rate': 76.00, 'Amount': 65 * 76.00},
            {'Name': 'TAPE ROLL', 'Consumption': 3, 'Rate': 125.00, 'Amount': 3 * 125.00},
            {'Name': 'ROUGH PAPER 20ML', 'Consumption': 3108, 'Rate': 0.33, 'Amount': 3108 * 0.33},
        ],
        'labor_cost': 1.45,
        'retail_price': 194.92,
        'standard_unit_per_batch': 18638,
    },

    {
        'name': 'Revive All 250ml  - Regular',
        'raw_materials': [
            {'Name': 'Silicone Emuslsion', 'Consumption': 200.00, 'Rate': 947.00, 'Amount': 200 * 947.00},
            {'Name': 'De-ionized Water', 'Consumption': 458.43, 'Rate': 2.25, 'Amount': 458.43 * 2.25},
            {'Name': 'Formoline', 'Consumption': 1.47, 'Rate': 220.00, 'Amount': 1.47 * 220.00},
            {'Name': 'Fragrance White Safe Guard', 'Consumption': 3.40, 'Rate': 4049.58, 'Amount': 3.40 * 4049.58},
            {'Name': 'Vinkocide CMIF', 'Consumption': 1.47, 'Rate': 805.00, 'Amount': 1.47 * 805.00},
           
        ],
        'packing_materials': [
            {'Name': 'Bottle / Cap  Revive All', 'Consumption': 2772, 'Rate': 21.00, 'Amount': 2772 * 21.00},
            {'Name': 'Spray Pump Revive all', 'Consumption': 2772, 'Rate': 40.99, 'Amount': 2772 * 40.99},
            {'Name': 'Label Revive All Regular', 'Consumption': 2772, 'Rate': 1.64, 'Amount': 2772 * 1.64},
            {'Name': 'CARTON 3 DZ Revive All', 'Consumption': 77, 'Rate': 131.14, 'Amount': 77 * 131.14},
            {'Name': 'Plastic Shrink Pack Revive All', 'Consumption': 2772, 'Rate': 1.40, 'Amount': 2772 * 1.40},
            {'Name': 'TAPE ROLL', 'Consumption': 1, 'Rate': 125.00, 'Amount': 1 * 125.00},
            {'Name': 'Glue S-10 Malcom', 'Consumption': 1, 'Rate': 680.00, 'Amount': 1 * 680.00},
        ],
        'labor_cost': 4.07,
        'retail_price': 593.22,
        'standard_unit_per_batch': 2772,
    },
    {
        'name': 'Revive All 250ml  - Auto',
        'raw_materials': [
            {'Name': 'Silicone Emuslsion', 'Consumption': 200.00, 'Rate': 947.00, 'Amount': 200 * 947.00},
            {'Name': 'De-ionized Water', 'Consumption': 458.43, 'Rate': 2.25, 'Amount': 458.43 * 2.25},
            {'Name': 'Formoline', 'Consumption': 1.47, 'Rate': 220.00, 'Amount': 1.47 * 220.00},
            {'Name': 'Fragrance White Safe Guard', 'Consumption': 3.40, 'Rate': 4049.58, 'Amount': 3.40 * 4049.58},
            {'Name': 'Vinkocide CMIF', 'Consumption': 1.47, 'Rate': 805.00, 'Amount': 1.47 * 805.00},
           
        ],
        'packing_materials': [
            {'Name': 'Bottle / Cap  Revive All', 'Consumption': 2772, 'Rate': 21.00, 'Amount': 2772 * 21.00},
            {'Name': 'Spray Pump Revive all', 'Consumption': 2772, 'Rate': 40.99, 'Amount': 2772 * 40.99},
            {'Name': 'Label Revive All Regular', 'Consumption': 2772, 'Rate': 1.64, 'Amount': 2772 * 1.64},
            {'Name': 'CARTON 3 DZ Revive All', 'Consumption': 77, 'Rate': 131.14, 'Amount': 77 * 131.14},
            {'Name': 'Plastic Shrink Pack Revive All', 'Consumption': 2772, 'Rate': 1.40, 'Amount': 2772 * 1.40},
            {'Name': 'TAPE ROLL', 'Consumption': 2, 'Rate': 125.00, 'Amount': 2 * 125.00},
            {'Name': 'Glue S-10 Malcom', 'Consumption': 1, 'Rate': 680.00, 'Amount': 1 * 680.00},
        ],
        'labor_cost': 4.07,
        'retail_price': 593.22,
        'standard_unit_per_batch': 2772,
    },
    {
        'name': 'Revive All 250ml  - Computer',
        'raw_materials': [
            {'Name': 'Silicone Emuslsion', 'Consumption': 200.00, 'Rate': 947.00, 'Amount': 200 * 947.00},
            {'Name': 'De-ionized Water', 'Consumption': 458.43, 'Rate': 2.25, 'Amount': 458.43 * 2.25},
            {'Name': 'Formoline', 'Consumption': 1.47, 'Rate': 220.00, 'Amount': 1.47 * 220.00},
            {'Name': 'Fragrance White Safe Guard', 'Consumption': 3.40, 'Rate': 4049.58, 'Amount': 3.40 * 4049.58},
            {'Name': 'Vinkocide CMIF', 'Consumption': 1.47, 'Rate': 805.00, 'Amount': 1.47 * 805.00},
           
        ],
        'packing_materials': [
            {'Name': 'Bottle / Cap  Revive All', 'Consumption': 2772, 'Rate': 21.00, 'Amount': 2772 * 21.00},
            {'Name': 'Spray Pump Revive all', 'Consumption': 2772, 'Rate': 40.99, 'Amount': 2772 * 40.99},
            {'Name': 'Label Revive All Regular', 'Consumption': 2772, 'Rate': 1.64, 'Amount': 2772 * 1.64},
            {'Name': 'CARTON 3 DZ Revive All', 'Consumption': 77, 'Rate': 131.14, 'Amount': 77 * 131.14},
            {'Name': 'Plastic Shrink Pack Revive All', 'Consumption': 2772, 'Rate': 1.40, 'Amount': 2772 * 1.40},
            {'Name': 'TAPE ROLL', 'Consumption': 2, 'Rate': 125.00, 'Amount': 2 * 125.00},
            {'Name': 'Glue S-10 Malcom', 'Consumption': 1, 'Rate': 680.00, 'Amount': 1 * 680.00},
        ],
        'labor_cost': 4.07,
        'retail_price': 593.22,
        'standard_unit_per_batch': 2772,
    },
    {
        'name': 'Glint Glass Cleaner 500ml - Regular',
        'raw_materials': [
            {'Name': 'Isopropyle Alcohol', 'Consumption': 176.77, 'Rate': 735.00, 'Amount': 176.77 * 735.00},
            {'Name': 'Cellosolve Solvent', 'Consumption': 43.69, 'Rate': 560, 'Amount': 43.69 * 560.00},
            {'Name': 'Silwet', 'Consumption': 3.20, 'Rate': 9788.00, 'Amount': 3.20 * 9788.00},
            {'Name': 'Tergitol NP-9', 'Consumption': 3.40, 'Rate': 4049.58, 'Amount': 3.40 * 4049.58},
            {'Name': 'Solar Torquise Blue', 'Consumption': 0.07, 'Rate': 13800, 'Amount': 0.07 * 13800.00},
            {'Name': 'Fragrance Sunlight', 'Consumption': 1.25, 'Rate': 7713.75, 'Amount': 1.25 * 7713.75},
            {'Name': 'De-Ionized Water', 'Consumption': 1774, 'Rate': 2.25, 'Amount': 1774 * 2.25},
        ],
        'packing_materials': [
            {'Name': 'Bottle Glint Glass Cleaner', 'Consumption': 4248, 'Rate': 28.00, 'Amount': 4248 * 28.00},
            {'Name': 'Hand Trigger Glint Spray', 'Consumption': 4248, 'Rate': 47.16, 'Amount': 4248 * 47.16},
            {'Name': 'Sticker Glint 500ml Front', 'Consumption': 4248, 'Rate': 2.16, 'Amount': 4248 * 2.16},
            {'Name': 'Sticker Glint 500ml Back', 'Consumption': 4248, 'Rate': 2.17, 'Amount': 4248 * 2.17},
            {'Name': 'Carton 2 Dozen Glint 500ml', 'Consumption': 177.00, 'Rate': 193.44, 'Amount': 177 * 193.44},
            {'Name': 'TAPE ROLL', 'Consumption': 2, 'Rate': 125.00, 'Amount': 2 * 125.00},
        ],        
        'labor_cost': 4.14,
        'retail_price': 593.22,
        'standard_unit_per_batch': 4248,
    },
    {
        'name': 'Glint Glass Cleaner 500ml - Lavender',
        'raw_materials': [
            {'Name': 'De-Ionized Water', 'Consumption': 963.81, 'Rate': 2.25, 'Amount': 963.81 * 2.25},
            {'Name': 'Novathix L-10', 'Consumption': 3.50, 'Rate': 3000, 'Amount': 3.50 * 3000.00},
            {'Name': 'Iso Propyle Alchol', 'Consumption': 20.00, 'Rate': 735.00, 'Amount': 20.00 * 735.00},
            {'Name': 'Cellosolve Solvent', 'Consumption': 10.00, 'Rate': 560.00, 'Amount': 10.00 * 560.00},
            {'Name': 'Caustic Soda Flakes', 'Consumption': 0.18, 'Rate': 186.50, 'Amount': 0.18 * 186.50},
            {'Name': 'Sulphonic Acid', 'Consumption': 0.50, 'Rate': 510, 'Amount': 0.50 * 510.00},
            {'Name': 'Genaminox LA Clariant', 'Consumption': 0.50, 'Rate': 1148.00, 'Amount': 0.50 * 1148},
            {'Name': 'Soft Lavender WS 375715', 'Consumption': 1.00, 'Rate': 6509.00, 'Amount': 1.00 * 6509},
            {'Name': 'Sanoline Dye', 'Consumption': .01, 'Rate': 24657.10, 'Amount': 0.01 * 24657},
            {'Name': 'Vinkocide', 'Consumption': 0.50, 'Rate': 805.00, 'Amount': 0.50 * 805.00},

        ],
        'packing_materials': [
            {'Name': 'Bottle Glint Glass Cleaner', 'Consumption': 2122, 'Rate': 28.00, 'Amount': 2122 * 28.00},
            {'Name': 'Hand Trigger Glint Spray', 'Consumption': 2122, 'Rate': 47.16, 'Amount': 2122 * 47.16},
            {'Name': 'Sticker Glint Lavender 500ml Front', 'Consumption': 2122, 'Rate': 2.10, 'Amount': 2122 * 2.10},
            {'Name': 'Sticker Glint Lavender 500ml Back', 'Consumption': 2122, 'Rate': 2.11, 'Amount': 2122 * 2.11},
            {'Name': 'Carton 2 Dozen Glint 500ml', 'Consumption': 88, 'Rate': 193.44, 'Amount': 88 * 193.44},
            {'Name': 'TAPE ROLL', 'Consumption': 1, 'Rate': 125.00, 'Amount': 1 * 125.00},
        ],        
        'labor_cost': 4.14,
        'retail_price': 593.22,
        'standard_unit_per_batch': 2122,
    },

    
    # Add more finished goods here
]

# Create FinishedGood objects
finished_goods = [FinishedGood(**fg) for fg in finished_goods_data]

# GUI setup
def show_gross_margin():
    selected_good_name = finished_good_combobox.get()

    for good in finished_goods:
        if good.name == selected_good_name:
            raw_cost,pack_cost, prime_cost, margin = good.calculate_costs()

            # Clear existing rows
            for i in tree.get_children():
                tree.delete(i)

            # Insert raw material costs
            for item in good.raw_materials:
                tree.insert("", "end", values=(item['Name'], f"{item['Consumption']:.2f}", f"{item['Rate']:.2f}", f"{item['Amount']:.2f}"))
            
            tree.insert("", "end", values=("Total Raw Material Cost", "", "", f"{good.total_raw_material_cost:.2f}"))

            # Configure Treeview Tag for Raw Material Cost
            tree.tag_configure('black', foreground='black')
            for item in tree.get_children():
                if tree.item(item, 'values')[0] == "Total Raw Material Cost":
                    tree.item(item, tags=('black',))
                    break

            tree.insert("", "end", values=("", "", "", ""))

            # Insert packing material costs
            for item in good.packing_materials:
                tree.insert("", "end", values=(item['Name'], f"{item['Consumption']:.2f}", f"{item['Rate']:.2f}", f"{item['Amount']:.2f}"))
            tree.insert("", "end", values=("Total Packing Material Cost", "", "", f"{good.total_packing_material_cost:.2f}"))
            
            # Configure Treeview Tag for Packing Material Cost
            tree.tag_configure('black', foreground='black', background='white')
            for item in tree.get_children():
                if tree.item(item, 'values')[0] == "Total Packing Material Cost":
                    tree.item(item, tags=('black',))
                    break

            tree.insert("", "end", values=("", "", "", ""))

            tree.insert("", "end", values=("                                                       S U M M A R Y", "", "", ""))
            tree.insert("", "end", values=("                                                       -----------------------", "", "", ""))

            tree.insert("", "end", values=("", "", "", ""))


            tree.insert("", "end", values=("Standard Production Unit Per Batch", "", "", f"{good.standard_unit_per_batch:.2f}"))
            tree.insert("", "end", values=("Raw Material Cost Per Unit", "", "", f"{raw_cost:.2f}"))
            tree.insert("", "end", values=("Packing Material Cost Per Unit", "", "", f"{pack_cost:.2f}"))
            tree.insert("", "end", values=("Labor Cost Per Unit", "", "", f"{good.labor_cost:.2f}"))
            tree.insert("", "end", values=("Prime Cost Per Unit", "", "", f"{prime_cost:.2f}"))
            tree.insert("", "end", values=("Retail Price Per Unit", "", "", f"{good.retail_price:.2f}"))
            tree.insert("", "end", values=("Gross Margin Per Unit", "", "", f"{margin:.2f}"))
            GRP = (margin / good.retail_price) * 100
            tree.insert("", "end", values=("Gross Margin %", "", "", f"{GRP:.2f}%"))

            heading_label.config(text=selected_good_name,background="#CD5C5C")
            break
def export_to_pdf():
    try:
        print("Export to PDF function called")  # Debug print

        # Create a canvas object
        pdf_file = "Finished_Good_Cost_Report.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=A4)
        elements = []

        selected_good_name = finished_good_combobox.get()
        print(f"COST SHEET <br> {selected_good_name}<br>")  # Debug print

        for good in finished_goods:
            if good.name == selected_good_name:
                raw_cost, pack_cost, prime_cost, margin = good.calculate_costs()

                styles = getSampleStyleSheet()
                title3 = Paragraph(f"PERIDOT PRODUCTS PVT LTD", styles['Title'])
                title = Paragraph(f" {selected_good_name}", styles['Title'])
                title2 = Paragraph(f"COST SHEET", styles['Title'])
                elements.append(title3)
                elements.append(title)
                elements.append(title2)

                # Raw Materials Table
                raw_materials_data = [["Name", "Consumption", "Rate", "Amount In Rs."]]
                for item in good.raw_materials:
                    raw_materials_data.append([item['Name'], f"{item['Consumption']:.2f}", f"{item['Rate']:.2f}", f"{item['Amount']:.2f}"])
                raw_materials_data.append(["Total Raw Material Cost", "", "", f"{good.total_raw_material_cost:.2f}"])

                raw_materials_table = Table(raw_materials_data, colWidths=[200, 100, 100, 100])
                raw_materials_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(raw_materials_table)

                elements.append(Paragraph("<br/>", styles['Normal']))  # Add space between tables

                # Packing Materials Table
                packing_materials_data = [["Name", "Consumption", "Rate", "Amount In Rs."]]
                for item in good.packing_materials:
                    packing_materials_data.append([item['Name'], f"{item['Consumption']:.2f}", f"{item['Rate']:.2f}", f"{item['Amount']:.2f}"])
                packing_materials_data.append(["Total Packing Material Cost", "", "", f"{good.total_packing_material_cost:.2f}"])

                packing_materials_table = Table(packing_materials_data, colWidths=[200, 100, 100, 100])
                packing_materials_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(packing_materials_table)

                elements.append(Paragraph("<br/>", styles['Normal']))  # Add space between tables

                # Summary Table
                summary_data = [
                    ["Description", "Value In Rs."],
                    ["Standard Production Unit Per Batch (Rs.)", f"{good.standard_unit_per_batch:.2f}"],
                    ["Raw Material Cost Per Unit", f"{raw_cost:.2f}"],
                    ["Packing Material Cost Per Unit", f"{pack_cost:.2f}"],
                    ["Labor Cost Per Unit", f"{good.labor_cost:.2f}"],
                    ["Prime Cost Per Unit", f"{prime_cost:.2f}"],
                    ["Retail Price Per Unit", f"{good.retail_price:.2f}"],
                    ["Gross Margin Per Unit", f"{margin:.2f}"],
                    ["Gross Margin %", f"{(margin / good.retail_price) * 100:.2f}%"]
                ]

                styles = getSampleStyleSheet()
                title_s = Paragraph(f"SUMMARY", styles['Title'])

                summary_table = Table(summary_data, colWidths=[300, 200])
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Center align for header row
                    ('ALIGN', (0, 1), (0, -1), 'LEFT'),    # Left align for Description column
                    ('ALIGN', (1, 1), (1, -1), 'RIGHT'),    # Left align for Value column
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))

                elements.append(title_s)
                elements.append(summary_table)

                break

        doc.build(elements)
        print(f"PDF created: {pdf_file}")  # Debug print

        if os.name == 'nt':  # for Windows
            os.startfile(pdf_file)
        elif os.name == 'posix':  # for macOS or Linux
            subprocess.call(('open', pdf_file) if platform.system() == 'Darwin' else ('xdg-open', pdf_file))
    except Exception as e:
        print(f"Error during PDF creation: {e}")  # Debug print



app = tk.Tk()
app.title("Gross Margin Calculator")
app.geometry('640x1000+250+10')
app.configure(bg="#CD5C5C")

ttk.Label(app, text="Select Finished Good:").grid(column=0, row=0, padx=10, pady=10)
finished_good_combobox = ttk.Combobox(app, values=[fg.name for fg in finished_goods], state="readonly", width=40)
finished_good_combobox.grid(column=1, row=0, padx=10, pady=10)

style = ttk.Style(app)
style.theme_use("clam")  # Use 'clam' theme
style.configure("Treeview", background="#008080", foreground="white", rowheight=18, font=("Helvetica", 10))
style.configure("Treeview.Heading", font=("Helvetica", 8, "bold"))

ttk.Button(app, text="Calculate Gross Margin", command=show_gross_margin).grid(column=0, row=5, columnspan=2, padx=10, pady=10)
ttk.Button(app, text="Export to PDF", command=export_to_pdf).grid(column=0, row=6, columnspan=2, pady=10)

heading_label = ttk.Label(app, text="", font=("Helvetica", 16, "bold"),background="#CD5C5C", anchor="center")
heading_label.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

subhead_label = ttk.Label(app, text="Cost Sheet", font=("Helvetica", 16, "bold"))
subhead_label.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

# Treeview for displaying the details in tabular form
columns = ('Name', 'Consumption', 'Rate', 'Amount')
tree = ttk.Treeview(app, columns=columns, show='headings', height=35)
for col in columns:
    tree.heading(col, text=col)
    tree.column('Name', anchor='w', width=350)
    tree.column('Consumption', anchor='e', width=100)
    tree.column('Rate', anchor='e', width=80)
    tree.column('Amount', anchor='e', width=80)
tree.grid(column=0, row=4, columnspan=2, padx=10, pady=10)



app.mainloop()