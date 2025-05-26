import streamlit as st
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Kontrola importu matplotlib a seaborn
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ModuleNotFoundError as e:
    st.error(f"Chyba: Modul {e.name} není nainstalován. Nainstalujte jej příkazem: `pip install {e.name}`")
    st.stop()

# Simulace Grok API
class Grok:
    def generate_response(self, otázka):
        return f"AI odpověď: {otázka} - Například, protilátky jsou proteiny produkované B-lymfocyty, které neutralizují patogeny."

grok = Grok()

# Databáze markerů a scénářů
MARKER_DB = {
    "Leukémie": {
        "markery": ["CD45", "CD34", "CD117", "CD13", "CD33"],
        "popis": "Akutní myeloidní leukémie (AML) a lymfoblastická leukémie (ALL). CD45 je obecný leukocytový marker, CD34 a CD117 označují kmenové buňky, CD13/CD33 myeloidní linie."
    },
    "Imunodeficience": {
        "markery": ["CD45", "CD3", "CD4", "CD8", "CD19", "CD56"],
        "popis": "Poruchy imunitního systému, např. HIV/AIDS nebo SCID. CD4/CD8 poměr je klíčový pro hodnocení T-buněčných subpopulací, CD19 označuje B-buňky, CD56 NK-buňky."
    },
    "Lymfomy": {
        "markery": ["CD45", "CD20", "CD5", "CD10", "BCL2", "Ki67"],
        "popis": "Non-Hodgkinovy a Hodgkinovy lymfomy. CD20 je marker B-buněk, CD5/CD10 pomáhají rozlišit typy lymfomů, BCL2 označuje antiapoptotickou aktivitu, Ki67 proliferaci."
    },
    "Autoimunitní onemocnění": {
        "markery": ["CD45", "CD3", "CD4", "CD25", "FOXP3", "CD19"],
        "popis": "Např. revmatoidní artritida nebo lupus. CD25 a FOXP3 označují regulační T-buňky (Treg), které regulují imunitní toleranci."
    },
    "Alergie": {
        "markery": ["CD45", "CD3", "CD4", "CD23", "IgE", "CD203c"],
        "popis": "Alergické reakce, např. atopická dermatitida. CD23 a IgE jsou klíčové pro B-buněčnou aktivaci, CD203c označuje aktivované bazofily."
    },
    "T-buněčná aktivace (výuka)": {
        "markery": ["CD3", "CD4", "CD8", "CD25", "CD69", "CD44"],
        "popis": "Modeluje proces aktivace T-buněk během imunitní odpovědi. CD25 a CD69 jsou markery časné aktivace, CD44 označuje paměťové T-buňky."
    },
    "B-buněčná diferenciace (výuka)": {
        "markery": ["CD19", "CD20", "CD27", "CD38", "IgM", "IgD"],
        "popis": "Sleduje vývoj B-buněk od naivních po plazmatické buňky. CD27 označuje paměťové B-buňky, CD38 plazmatické buňky."
    }
}

# Popisy markerů
MARKER_POPIS = {
    "CD45": "Obecný leukocytový marker, exprimován na všech hematopoetických buňkách kromě erytrocytů.",
    "CD34": "Marker kmenových buněk, exprimován na hematopoetických prekurzorech.",
    "CD117": "C-kit, marker kmenových buněk a mastocytů.",
    "CD13": "Myeloidní marker, exprimován na granulocytech a monocytech.",
    "CD33": "Myeloidní marker, typický pro AML a monocyty.",
    "CD3": "Součást T-buněčného receptoru, exprimován na T-buňkách.",
    "CD4": "Ko-receptor na T-helper buňkách, klíčový pro MHC-II interakce.",
    "CD8": "Ko-receptor na cytotoxických T-buňkách, váže MHC-I.",
    "CD19": "Marker B-buněk, klíčový pro signalizaci B-buněčného receptoru.",
    "CD56": "Marker NK-buněk, exprimován také na některých T-buňkách.",
    "CD20": "Marker zralých B-buněk, cíl pro monoklonální protilátky (např. rituximab).",
    "CD5": "Exprimován na T-buňkách a podskupině B-buněk (B1), typický pro CLL.",
    "CD10": "Marker nezralých B-buněk, exprimován v ALL a folikulárních lymfomech.",
    "BCL2": "Antiapoptotický protein, zvýšená exprese u lymfomů.",
    "Ki67": "Marker proliferace, exprimován v dělících se buňkách.",
    "CD25": "IL-2 receptor alfa, marker aktivovaných T-buněk a Treg.",
    "FOXP3": "Transkripční faktor, specifický pro regulační T-buňky (Treg).",
    "CD23": "Nízký afinitní receptor IgE, exprimován na B-buňkách a bazofilech.",
    "IgE": "Imunoglobulin spojený s alergickými reakcemi, váže se na CD23.",
    "CD203c": "Marker aktivace bazofilů, používaný při alergických testech.",
    "CD69": "Časný aktivační marker T- a NK-buněk.",
    "CD44": "Marker paměťových T-buněk, podílí se na adhezi a migraci.",
    "CD27": "Marker paměťových B-buněk, podílí se na kostimulaci.",
    "CD38": "Marker plazmatických buněk a aktivovaných lymfocytů.",
    "IgM": "První imunoglobulin exprimovaný naivními B-buňkami.",
    "IgD": "Marker naivních B-buněk, exprimován společně s IgM."
}

# Fluorochromy a spektrální data
FLUOROCHROM_DB = {
    "FITC": (519, "488 nm"),
    "PE": (578, "488 nm"),
    "PerCP": (677, "488 nm"),
    "APC": (660, "633 nm"),
    "Pacific Blue": (455, "405 nm"),
    "Alexa Fluor 700": (723, "633 nm"),
    "BV421": (421, "405 nm"),
    "BV510": (510, "405 nm"),
    "BV605": (605, "405 nm"),
    "BV711": (711, "405 nm"),
    "PE-Cy5.5": (695, "488 nm"),
    "PE-Cy7": (780, "488 nm"),
    "APC-Cy7": (785, "633 nm"),
    "ECD": (610, "488 nm"),
    "Pacific Orange": (551, "405 nm"),
    "BV650": (650, "405 nm"),
    "Alexa Fluor 647": (668, "633 nm"),
    "PE-CF594": (617, "488 nm"),
    "AmCyan": (491, "405 nm"),
    "VioGreen": (520, "405 nm")
}

SPECTRA_DB = {
    "FITC": [(480, 0.1), (500, 0.5), (519, 1.0), (540, 0.5), (560, 0.2), (580, 0.05)],
    "PE": [(540, 0.1), (560, 0.4), (578, 1.0), (600, 0.6), (620, 0.3), (650, 0.1)],
    "PerCP": [(640, 0.1), (660, 0.5), (677, 1.0), (700, 0.4), (720, 0.1)],
    "APC": [(620, 0.1), (640, 0.5), (660, 1.0), (680, 0.5), (700, 0.2)],
    "Pacific Blue": [(420, 0.1), (440, 0.6), (455, 1.0), (470, 0.5), (490, 0.1)],
    "Alexa Fluor 700": [(680, 0.1), (700, 0.5), (723, 1.0), (740, 0.4), (760, 0.1)],
    "BV421": [(400, 0.1), (410, 0.5), (421, 1.0), (440, 0.5), (460, 0.2)],
    "BV510": [(470, 0.1), (490, 0.5), (510, 1.0), (530, 0.5), (550, 0.2)],
    "BV605": [(570, 0.1), (590, 0.5), (605, 1.0), (620, 0.5), (640, 0.2)],
    "BV711": [(670, 0.1), (690, 0.5), (711, 1.0), (730, 0.5), (750, 0.2)],
    "PE-Cy5.5": [(660, 0.1), (680, 0.5), (695, 1.0), (710, 0.5), (730, 0.2)],
    "PE-Cy7": [(740, 0.1), (760, 0.5), (780, 1.0), (800, 0.4), (820, 0.1)],
    "APC-Cy7": [(740, 0.1), (760, 0.5), (785, 1.0), (800, 0.4), (820, 0.1)],
    "ECD": [(580, 0.1), (600, 0.5), (610, 1.0), (630, 0.5), (650, 0.2)],
    "Pacific Orange": [(520, 0.1), (540, 0.5), (551, 1.0), (570, 0.5), (590, 0.2)],
    "BV650": [(620, 0.1), (640, 0.5), (650, 1.0), (670, 0.5), (690, 0.2)],
    "Alexa Fluor 647": [(630, 0.1), (650, 0.5), (668, 1.0), (690, 0
