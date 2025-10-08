import streamlit as st
import os

st.title("Prefiksbehandler for geotekniske sonderinger")

# Brukerinput
path = st.text_input("Skriv inn filbane til mappen med filene (AUTOGRAF-mappa):", "")
action = st.selectbox("Velg handling:", ["Legg til prefiks", "Endre prefiks", "Fjern prefiks"])
prefix = st.text_input("Skriv inn prefikset du ønsker å bruke (for Legg til/Endre):", "")

# Kjør knapp
if st.button("Kjør"):
    if not os.path.exists(path):
        st.error("Filen eller mappen finnes ikke. Sjekk banen og prøv igjen.")
    else:
        os.chdir(path)
        files = os.listdir(path)
        count = 0

        # Legge til prefiks
        if action == "Legg til prefiks":
            for file in files:
                f, e = os.path.splitext(file)
                if not f.startswith(prefix):
                    os.rename(file, f"{prefix}{f}{e}")
                    count += 1
            st.success(f"Prefiks '{prefix}' lagt til {count} filer.")

        # Endre prefiks
        elif action == "Endre prefiks":
            old_prefix = st.text_input("Skriv inn gammelt prefiks:", "")
            if old_prefix:
                for file in files:
                    f, e = os.path.splitext(file)
                    if f.startswith(old_prefix):
                        new_name = f.replace(old_prefix, prefix, 1)
                        os.rename(file, f"{new_name}{e}")
                        count += 1
                st.success(f"Prefiks '{old_prefix}' endret til '{prefix}' for {count} filer.")
            else:
                st.warning("Du må skrive inn gammelt prefiks for å endre.")

        # Fjerne prefiks
        elif action == "Fjern prefiks":
            for file in files:
                f, e = os.path.splitext(file)
                if f.startswith(old_prefix):
                    new_name = f.replace(old_prefix, "", 1)
                    os.rename(file, f"{new_name}{e}")
                    count += 1
                st.success(f"Prefiks '{old_prefix}' fjernet for {count} filer.")
            else:
                st.warning("Du må skrive inn gammelt prefiks for å endre.")
