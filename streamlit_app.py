import streamlit as st
import random
import pandas as pd

# Kontrola importu matplotlib a seaborn
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ModuleNotFoundError as e:
    st.error(f"Chyba: Modul {e.name} není nainstalován. Nainstalujte jej příkazem: `pip install {e.name}`")
    st.stop()

# Simulace Grok API přímo v kódu
class Grok:
    def generate_response(self, otázka):
        # Simulovaná odpověď pro demonstrační účely
        return f"AI odpověď: {otázka} - Například, protilátky jsou proteiny produkované B-lymfocyty, které neutralizují patogeny."

grok = Grok()

# Hlavní nadpis aplikace
st.title("Interaktivní výuka imunologie")

# Sidebar pro navigaci
st.sidebar.header("Navigace")
section = st.sidebar.selectbox("Vyberte sekci", ["Úvod do imunologie", "Kvízy", "Interaktivní diagramy", "AI Vysvětlení"])

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
    
    # Simulace dat o distribuci buněk
    data = {
        "Buňka": ["T-lymfocyty", "B-lymfocyty", "Makrofágy", "Neutrofily"],
        "Procento": [30, 20, 25, 25]
    }
    df = pd.DataFrame(data)
    
    # Vytvoření grafu
    plt.figure(figsize=(6, 4))
    sns.barplot(x="Buňka", y="Procento", data=df)
    plt.title(f"Distribuce imunitních buněk")
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
    st.write(f"**{vybraná_buňka}**: Zde by bylo podrobné vysvětlení role této buňky v imunitním systému.")

# Sekce 4: AI Vysvětlení
elif section == "AI Vysvětlení":
    st.header("Zeptejte se AI na imunologii")
    otázka = st.text_input("Zadejte otázku (např. Co jsou protilátky?)")
    if st.button("Získat odpověď"):
        if otázka:
            odpověď = grok.generate_response(otázka)
            st.write(f"**Odpověď AI**: {odpověď}")
        else:
            st.warning("Prosím, zadejte otázku.")

# Instrukce pro spuštění
st.sidebar.write("**Jak spustit aplikaci**:")
st.sidebar.write("1. Nainstalujte knihovny: `pip install streamlit pandas matplotlib seaborn`")
st.sidebar.write("2. Spusťte příkaz: `streamlit run streamlit_app.py`")
st.sidebar.write("3. Pokud nasazujete na Streamlit Cloud, ujistěte se, že máte správný soubor `requirements.txt`.")
