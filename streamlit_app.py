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
    "Alexa Fluor 647": [(630, 0.1), (650, 0.5), (668, 1.0), (690, 0.5), (710, 0.2)],
    "PE-CF594": [(580, 0.1), (600, 0.5), (617, 1.0), (640, 0.5), (660, 0.2)],
    "AmCyan": [(460, 0.1), (480, 0.5), (491, 1.0), (510, 0.5), (530, 0.2)],
    "VioGreen": [(480, 0.1), (500, 0.5), (520, 1.0), (540, 0.5), (560, 0.2)]
}

LASER_BARVY = {
    "405 nm": "#D6BBF7",
    "488 nm": "#A9CCE3",
    "633 nm": "#F5B7B1"
}

# Databáze pro simulaci cizokrevního prostředí
IMMUNE_RESPONSE_DB = {
    "Virus": {
        "cytokiny": {"IFN-γ": 0.8, "IL-4": 0.1, "IL-17": 0.2, "TGF-β": 0.3},
        "T_subpopulace": {"Th1": 0.6, "Th2": 0.1, "Th17": 0.1, "Treg": 0.2},
        "imunoglobuliny": {"IgM": 0.3, "IgG": 0.6, "IgA": 0.05, "IgE": 0.05},
        "popis": "Virová infekce podporuje Th1 odpověď a produkci IgG pro neutralizaci virů."
    },
    "Bakterie (intracelulární)": {
        "cytokiny": {"IFN-γ": 0.7, "IL-4": 0.1, "IL-17": 0.3, "TGF-β": 0.2},
        "T_subpopulace": {"Th1": 0.5, "Th2": 0.1, "Th17": 0.3, "Treg": 0.1},
        "imunoglobuliny": {"IgM": 0.4, "IgG": 0.5, "IgA": 0.1, "IgE": 0.0},
        "popis": "Intracelulární bakterie stimulují Th1 a Th17, produkují IgG a IgM."
    },
    "Bakterie (extracelulární)": {
        "cytokiny": {"IFN-γ": 0.2, "IL-4": 0.2, "IL-17": 0.7, "TGF-β": 0.1},
        "T_subpopulace": {"Th1": 0.2, "Th2": 0.2, "Th17": 0.5, "Treg": 0.1},
        "imunoglobuliny": {"IgM": 0.5, "IgG": 0.3, "IgA": 0.15, "IgE": 0.05},
        "popis": "Extracelulární bakterie podporují Th17 a produkci IgM a IgA."
    },
    "Parazit": {
        "cytokiny": {"IFN-γ": 0.1, "IL-4": 0.8, "IL-17": 0.1, "TGF-β": 0.2},
        "T_subpopulace": {"Th1": 0.1, "Th2": 0.6, "Th17": 0.1, "Treg": 0.2},
        "imunoglobuliny": {"IgM": 0.2, "IgG": 0.2, "IgA": 0.1, "IgE": 0.5},
        "popis": "Parazitární infekce podporují Th2 a produkci IgE pro alergické odpovědi."
    },
    "Autoimunitní reakce": {
        "cytokiny": {"IFN-γ": 0.3, "IL-4": 0.2, "IL-17": 0.6, "TGF-β": 0.4},
        "T_subpopulace": {"Th1": 0.3, "Th2": 0.1, "Th17": 0.4, "Treg": 0.2},
        "imunoglobuliny": {"IgM": 0.3, "IgG": 0.4, "IgA": 0.2, "IgE": 0.1},
        "popis": "Autoimunitní reakce podporují Th17 a Treg, produkují IgG a IgA."
    }
}

def kontroluj_spektralni_konflikt(vybrane):
    konflikt = []
    hodnoty = [(f, FLUOROCHROM_DB[f][0]) for f in vybrane]
    for i in range(len(hodnoty)):
        for j in range(i+1, len(hodnoty)):
            rozdil = abs(hodnoty[i][1] - hodnoty[j][1])
            if rozdil < 40:
                konflikt.append((hodnoty[i][0], hodnoty[j][0]))
    return konflikt

def generuj_kompenzaci(fluora):
    kanaly = list(dict.fromkeys(fluora))
    data = []
    for r in kanaly:
        row = []
        for c in kanaly:
            if r == c:
                row.append(100.0)
            else:
                overlap = max(0.0, 100.0 - abs(FLUOROCHROM_DB[r][0] - FLUOROCHROM_DB[c][0])) / 2.5
                row.append(round(overlap, 1))
        data.append(row)
    return pd.DataFrame(data, index=kanaly, columns=kanaly)

def generuj_spektra(fluora):
    fig, ax = plt.subplots(figsize=(6, 4))
    vlnove_delky = np.linspace(400, 800, 400)
    for fluor in set(fluora):
        laser = FLUOROCHROM_DB[fluor][1]
        barva = LASER_BARVY.get(laser, "gray")
        spektrum = SPECTRA_DB[fluor]
        vlnove_delky_spektra, intenzity = zip(*spektrum)
        intenzity_interpol = np.interp(vlnove_delky, vlnove_delky_spektra, intenzity)
        ax.plot(vlnove_delky, intenzity_interpol, label=fluor, color=barva, linewidth=2)
    ax.set_xlabel("Vlnová délka (nm)")
    ax.set_ylabel("Relativní intenzita")
    ax.set_title("Emisní spektra vybraných fluorochromů")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

def simuluj_imunitni_odpoved(patogen, cytokiny):
    base_response = IMMUNE_RESPONSE_DB.get(patogen, IMMUNE_RESPONSE_DB["Virus"])
    T_subpopulace = base_response["T_subpopulace"].copy()
    imunoglobuliny = base_response["imunoglobuliny"].copy()
    
    # Modifikace podle uživatelských cytokinů
    for cytokin, hodnota in cytokiny.items():
        if hodnota > 0.5:
            if cytokin == "IFN-γ":
                T_subpopulace["Th1"] += 0.2
                imunoglobuliny["IgG"] += 0.2
            elif cytokin == "IL-4":
                T_subpopulace["Th2"] += 0.2
                imunoglobuliny["IgE"] += 0.2
            elif cytokin == "IL-17":
                T_subpopulace["Th17"] += 0.2
                imunoglobuliny["IgA"] += 0.2
            elif cytokin == "TGF-β":
                T_subpopulace["Treg"] += 0.2
                imunoglobuliny["IgA"] += 0.1
    
    # Normalizace T-subpopulací a imunoglobulinů
    total_T = sum(T_subpopulace.values())
    total_ig = sum(imunoglobuliny.values())
    T_subpopulace = {k: v/total_T for k, v in T_subpopulace.items()}
    imunoglobuliny = {k: v/total_ig for k, v in imunoglobuliny.items()}
    
    return T_subpopulace, imunoglobuliny, base_response["popis"]

# Záhlaví
st.title("Interaktivní výuka imunologie a flow cytometrie")

# Menu v levém sloupci
st.sidebar.header("Navigace")
section = st.sidebar.selectbox("Vyberte sekci", ["Úvod do imunologie", "Kvízy", "Interaktivní diagramy", "AI Vysvětlení", "Flow Cytometrie", "Simulace imunitní odpovědi"])

# Hlavní obsah a AI chat v pravém sloupci
main_col, ai_chat_col = st.columns([2, 1])

with main_col:
    # Sekce 1: Úvod do imunologie
    if section == "Úvod do imunologie":
        st.header("Úvod do imunologie")
        st.write("Imunologie je věda, která studuje imunitní systém, jehož hlavní funkcí je chránit tělo před infekcemi a cizími látkami.")
        st.subheader("Základní pojmy")
        st.write("- **Innata imunita**: Vrozená imunita, první linie obrany.")
        st.write("- **Adaptivní imunita**: Specifická imunita, která se učí a přizpůsobuje.")
        st.write("- **Imunitní buňky**: Např. T-lymfocyty, B-lymfocyty, makrofágy.")

    # Sekce 2: Kvízy
    elif section == "Kvízy":
        st.header("Test svých znalostí")
        quiz_questions = [
            {"otázka": "Co je hlavní funkcí T-lymfocytů?", 
             "možnosti": ["Produkce protilátek", "Zabíjení infikovaných buněk", "Fagocytóza"], 
             "správná": "Zabíjení infikovaných buněk"},
            {"otázka": "Která buňka produkuje protilátky?", 
             "možnosti": ["Makrofág", "B-lymfocyt", "Dendritická buňka"], 
             "správná": "B-lymfocyt"},
        ]
        
        st.subheader("Kviz: Základy imunologie")
        otázka = random.choice(quiz_questions)
        st.write(otázka["otázka"])
        odpověď = st.radio("Vyberte správnou odpověď:", otázka["možnosti"])
        
        if st.button("Odeslat odpověď"):
            if odpověď == otázka["správná"]:
                st.success("Správně! 🎉")
            else:
                st.error(f"Špatně. Správná odpověď je: {otázka['správná']}.")

    # Sekce 3: Interaktivní diagramy
    elif section == "Interaktivní diagramy":
        st.header("Interaktivní diagramy imunitního systému")
        st.write("Vyberte typ imunitní buňky pro zobrazení její distribuce.")
        buňky = ["T-lymfocyty", "B-lymfocyty", "Makrofágy", "Neutrofily"]
        vybraná_buňka = st.selectbox("Vyberte buňku", buňky)
        
        data = {
            "Buňka": ["T-lymfocyty", "B-lymfocyty", "Makrofágy", "Neutrofily"],
            "Procento": [30, 20, 25, 25]
        }
        df = pd.DataFrame(data)
        
        plt.figure(figsize=(6, 4))
        sns.barplot(x="Buňka", y="Procento", data=df)
        plt.title(f"Distribuce imunitních buněk")
        plt.xticks(rotation=45)
        st.pyplot(plt)
        
        st.write(f"**{vybraná_buňka}**: Zde by bylo podrobné vysvětlení role této buňky v imunitním systému.")

    # Sekce 5: Flow Cytometrie
    elif section == "Flow Cytometrie":
        st.header("Návrh panelu a spektrální kompenzace")
        
        rezim = st.radio("Vyberte režim:", ["Přednastavený klinický scénář", "Ruční výběr markerů"])
        
        if rezim == "Přednastavený klinický scénář":
            scenar = st.selectbox("Vyberte klinický nebo výukový scénář:", list(MARKER_DB.keys()))
            navrzeno = MARKER_DB[scenar]["markery"]
            st.write(f"**Popis scénáře:** {MARKER_DB[scenar]['popis']}")
            st.write(f"**Navržené markery:** {', '.join(navrzeno)}")
        else:
            st.write("**Vyberte markery ručně (max. 8):**")
            vsechny_markery = sorted(list(MARKER_POPIS.keys()))
            navrzeno = st.multiselect(
                "Vyberte CD markery:",
                vsechny_markery,
                default=["CD45", "CD3", "CD4"],
                max_selections=8,
                help="Vyberte až 8 markerů pro analýzu. Popisy markerů naleznete níže."
            )
            if not navrzeno:
                st.warning("Vyberte alespoň jeden marker.")
                st.stop()
        
        st.write("**Popisy vybraných markerů:**")
        for marker in navrzeno:
            st.markdown(f"- **{marker}**: {MARKER_POPIS.get(marker, 'Popis není k dispozici.')}")
        
        st.write("**Zvolte fluorochromy pro každý marker:**")
        fluoro_volby = {}
        for marker in navrzeno:
            st.markdown(f"**{marker}:**")
            selected_fluoro = st.selectbox(
                "",
                list(FLUOROCHROM_DB.keys()),
                key=marker,
                label_visibility="collapsed"
            )
            fluoro_volby[marker] = selected_fluoro
            laser = FLUOROCHROM_DB[selected_fluoro][1]
            color = LASER_BARVY.get(laser, "white")
            st.markdown(
                f"<span style='display: inline-flex; align-items: center; font-size: 0.9em; color: #666;'>"
                f"Vybraný laser: <span style='width: 12px; height: 12px; border-radius: 50%; background-color: {color}; margin-left: 8px; margin-right: 8px;'></span>{laser}</span>",
                unsafe_allow_html=True
            )
        
        zvolene_fluora = list(fluoro_volby.values())
        konflikty = kontroluj_spektralni_konflikt(zvolene_fluora)
        
        if konflikty:
            st.warning("Nalezeny spektrální konflikty mezi:")
            for k in konflikty:
                st.write(f"- {k[0]} a {k[1]}")
        else:
            st.success("Bez spektrálních konfliktů. Panel je v pořádku.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("**Předpokládaná kompenzační matice (%):**")
            kompenzace_df = generuj_kompenzaci(zvolene_fluora)
            def zbarvi_bunky(val):
                laser = FLUOROCHROM_DB[val.name][1] if val.name in FLUOROCHROM_DB else None
                color = LASER_BARVY.get(laser, "white")
                return [f"background-color: {color}" for _ in val]
            st.dataframe(kompenzace_df.style.apply(zbarvi_bunky, axis=1))
        
        with col2:
            st.write("**Emisní spektra vybraných fluorochromů:**")
            fig = generuj_spektra(zvolene_fluora)
            st.pyplot(fig)

    # Sekce 6: Simulace imunitní odpovědi
    elif section == "Simulace imunitní odpovědi":
        st.header("Simulace cizokrevního prostředí")
        st.write("Vyberte patogen a upravte hladiny cytokinů pro simulaci imunitní odpovědi.")
        
        patogen = st.selectbox("Vyberte typ patogenu:", list(IMMUNE_RESPONSE_DB.keys()))
        
        st.subheader("Nastavení cytokinů")
        cytokiny = {
            "IFN-γ": st.slider("IFN-γ (Th1 podpora)", 0.0, 1.0, IMMUNE_RESPONSE_DB[patogen]["cytokiny"]["IFN-γ"]),
            "IL-4": st.slider("IL-4 (Th2 podpora)", 0.0, 1.0, IMMUNE_RESPONSE_DB[patogen]["cytokiny"]["IL-4"]),
            "IL-17": st.slider("IL-17 (Th17 podpora)", 0.0, 1.0, IMMUNE_RESPONSE_DB[patogen]["cytokiny"]["IL-17"]),
            "TGF-β": st.slider("TGF-β (Treg podpora)", 0.0, 1.0, IMMUNE_RESPONSE_DB[patogen]["cytokiny"]["TGF-β"])
        }
        
        if st.button("Spustit simulaci"):
            T_subpopulace, imunoglobuliny, popis = simuluj_imunitni_odpoved(patogen, cytokiny)
            
            st.write(f"**Popis simulace:** {popis}")
            
            # Vizualizace T-subpopulací
            st.subheader("Rozložení T-buněčných subpopulací")
            T_df = pd.DataFrame.from_dict(T_subpopulace, orient="index", columns=["Procento"])
            T_df["Procento"] *= 100
            plt.figure(figsize=(6, 4))
            sns.barplot(x=T_df.index, y="Procento", data=T_df)
            plt.title("Distribuce T-buněčných subpopulací")
            plt.xticks(rotation=45)
            plt.ylabel("Procento (%)")
            st.pyplot(plt)
            
            # Vizualizace imunoglobulinů
            st.subheader("Produkce imunoglobulinů")
            ig_df = pd.DataFrame.from_dict(imunoglobuliny, orient="index", columns=["Procento"])
            ig_df["Procento"] *= 100
            plt.figure(figsize=(6, 4))
            sns.barplot(x=ig_df.index, y="Procento", data=ig_df)
            plt.title("Distribuce imunoglobulinů")
            plt.xticks(rotation=45)
            plt.ylabel("Procento (%)")
            st.pyplot(plt)
            
            # Tabulka s výsledky
            st.subheader("Podrobné výsledky")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**T-buněčné subpopulace (%):**")
                st.dataframe(T_df.style.format("{:.1f}"))
            with col2:
                st.write("**Imunoglobuliny (%):**")
                st.dataframe(ig_df.style.format("{:.1f}"))

with ai_chat_col:
    st.header("AI Chat")
    if section == "AI Vysvětlení":
        otázka = st.text_input("Zadejte otázku (např. Co jsou protilátky?)")
        if st.button("Získat odpověď"):
            if otázka:
                odpověď = grok.generate_response(otázka)
                st.write(f"**Odpověď AI**: {odpověď}")
            else:
                st.warning("Prosím, zadejte otázku.")
    else:
        st.write("Vyberte sekci 'AI Vysvětlení' v menu pro interakci s AI.")

# Instrukce pro spuštění
st.sidebar.write("**Jak spustit aplikaci**:")
st.sidebar.write("1. Nainstalujte knihovny: `pip install streamlit pandas numpy matplotlib seaborn`")
st.sidebar.write("2. Spusťte příkaz: `streamlit run streamlit_app.py`")
st.sidebar.write("3. Pokud nasazujete na Streamlit Cloud, ujistěte se, že máte správný soubor `requirements.txt`.")
