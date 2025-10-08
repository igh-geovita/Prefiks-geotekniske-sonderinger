import streamlit as st
import os
import io
import zipfile

st.title("🔤 Prefiksbehandler for geotekniske sonderinger")

# Opplasting av filer
uploaded_files = st.file_uploader(
    "Last opp filene du ønsker å behandle (for eksempel alle fra AUTOGRAF-mappa):",
    accept_multiple_files=True
)

# Valg av handling
action = st.selectbox(
    "Velg handling:",
    ["Legg til prefiks", "Endre prefiks", "Fjern prefiks"]
)

# Prefiks-input
prefix = st.text_input("Skriv inn nytt prefiks (for Legg til / Endre):", "")

# For endre/fjerne
old_prefix = ""
if action in ["Endre prefiks", "Fjern prefiks"]:
    old_prefix = st.text_input("Skriv inn gammelt prefiks (for Fjerne/Endre):", "")

# Kjør knapp
if st.button("Kjør behandling"):
    if not uploaded_files:
        st.warning("Du må laste opp minst én fil.")
    else:
        processed_files = []
        count = 0

        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            f, e = os.path.splitext(file_name)
            new_name = file_name  # fallback

            # Legge til prefiks
            if action == "Legg til prefiks":
                if not f.startswith(prefix):
                    new_name = f"{prefix}{f}{e}"
                    count += 1

            # Endre prefiks
            elif action == "Endre prefiks" and old_prefix:
                if f.startswith(old_prefix):
                    new_name = f.replace(old_prefix, prefix, 1) + e
                    count += 1

            # Fjerne prefiks
            elif action == "Fjern prefiks" and old_prefix:
                if f.startswith(old_prefix):
                    new_name = f.replace(old_prefix, "", 1) + e
                    count += 1

            # Lagre innholdet med nytt navn
            processed_files.append((new_name, uploaded_file.read()))

        # Opprett en zip-fil med resultatet
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for fname, data in processed_files:
                zipf.writestr(fname, data)

        zip_buffer.seek(0)

        # Nedlastbar ZIP
        st.success(f"✅ Ferdig! {count} filer ble behandlet.")
        st.download_button(
            label="⬇️ Last ned oppdaterte filer (ZIP)",
            data=zip_buffer,
            file_name="prefiksbehandlede_filer.zip",
            mime="application/zip"
        )
