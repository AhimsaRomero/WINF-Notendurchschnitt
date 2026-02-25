import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(
    page_title="WINF Notendurchschnitt Rechner",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
)

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def ensure_user_fields(username):
    users = load_users()
    changed = False
    if "noten" not in users[username]:
        users[username]["noten"] = {}
        changed = True
    if "wahlpflicht" not in users[username]:
        users[username]["wahlpflicht"] = {}
        changed = True
    if "setup_done" not in users[username]:
        users[username]["setup_done"] = False
        changed = True
    if "auslandssemester" not in users[username]:
        users[username]["auslandssemester"] = False
        changed = True
    if "auslands_faecher" not in users[username]:
        users[username]["auslands_faecher"] = []
        changed = True
    if changed:
        save_users(users)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

KERNMODULE = [
    {"Fachname": "ITMA - IT-Management",                           "ECTS": 6,  "Semester": 1},
    {"Fachname": "DTRA - Digitale Transformation: Prinzipien",     "ECTS": 6,  "Semester": 1},
    {"Fachname": "KETE - Key Technologies",                        "ECTS": 3,  "Semester": 1},
    {"Fachname": "SGPM - Strategisches Geschäftsprozessmanagement","ECTS": 3,  "Semester": 1},
    {"Fachname": "WIAS - Wissenschaftliches Arbeiten & Schreiben", "ECTS": 3,  "Semester": 1},
    {"Fachname": "BINA - Business Intelligence & Analytics",       "ECTS": 6,  "Semester": 2},
    {"Fachname": "PPMA - Programm- und Portfolio-Management",      "ECTS": 3,  "Semester": 2},
    {"Fachname": "BPPM - Business Process Performance Management", "ECTS": 3,  "Semester": 2},
    {"Fachname": "AFEU - aF&E Übungen",                           "ECTS": 6,  "Semester": 2},
    {"Fachname": "ISMA - Information Security Management",         "ECTS": 3,  "Semester": 3},
    {"Fachname": "DSCI - Data Science",                            "ECTS": 6,  "Semester": 3},
    {"Fachname": "VMAT - Vorstudie Master Thesis",                 "ECTS": 3,  "Semester": 3},
    {"Fachname": "AFEP - aF&E Projekte",                           "ECTS": 6,  "Semester": 3},
    {"Fachname": "GORC - Governance, Risk & Compliance",           "ECTS": 3,  "Semester": 4},
    {"Fachname": "DECO - Digital Ecosystems",                      "ECTS": 3,  "Semester": 4},
    {"Fachname": "MATH - Master Thesis",                           "ECTS": 12, "Semester": 4},
]

AUSLAND_PFLICHT = ["VMAT - Vorstudie Master Thesis", "AFEP - aF&E Projekte"]

WAHLPFLICHT = {
    "Wahlpflichtmodule Digital Health": [
        {"Fachname": "DIHG - Digital Health – Grundlagen",              "ECTS": 3, "Semester": 2},
        {"Fachname": "DIHA - Digital Health – Anwendung & Technologie", "ECTS": 3, "Semester": 3},
        {"Fachname": "ARTI - Artifacts in IT (Digital Health)",         "ECTS": 3, "Semester": 4},
    ],
    "Wahlpflichtmodule Digital Finance": [
        {"Fachname": "DIFG - Digital Finance – Grundlagen",             "ECTS": 3, "Semester": 2},
        {"Fachname": "DIFA - Digital Finance – Anwendungen",            "ECTS": 3, "Semester": 3},
        {"Fachname": "ARTI - Artifacts in IT (Digital Finance)",        "ECTS": 3, "Semester": 4},
    ],
    "Wahlpflichtmodule Digital Manufacturing": [
        {"Fachname": "DIMG - Digital Manufacturing – Grundlagen",       "ECTS": 3, "Semester": 2},
        {"Fachname": "DIMA - Digital Manufacturing – Anwendungen",      "ECTS": 3, "Semester": 3},
        {"Fachname": "ARTI - Artifacts in IT (Digital Manufacturing)",  "ECTS": 3, "Semester": 4},
    ],
    "Wahlpflichtmodule General Business IT": [
        {"Fachname": "RQEM - Requirements Engineering & -Management",   "ECTS": 6, "Semester": 2},
        {"Fachname": "SWEN - Softwareentwicklung",                      "ECTS": 6, "Semester": 3},
        {"Fachname": "DABA - Datenbanken & Datenbankabfragen",          "ECTS": 3, "Semester": 4},
    ],
    "Wahlpflichtmodule allgemein": [
        {"Fachname": "HUCI - Human Computer Interaction",               "ECTS": 3, "Semester": 2},
        {"Fachname": "LCCD - Low Code & Citizen Development",           "ECTS": 3, "Semester": 3},
        {"Fachname": "CONS - Consulting",                               "ECTS": 3, "Semester": 3},
        {"Fachname": "NWAO - New Work & Agile Organisation",            "ECTS": 3, "Semester": 4},
    ],
}

MASTER_ECTS = 90

# ─── LOGIN / REGISTRIERUNG ───────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.title("WINF Notendurchschnitt Rechner")
    tab1, tab2 = st.tabs(["Login", "Registrieren"])

    with tab1:
        st.subheader("Login")
        login_user = st.text_input("Benutzername", key="login_user")
        if st.button("Einloggen"):
            users = load_users()
            login_user_lower = login_user.strip().lower()
            users_lower = {k.lower(): k for k in users.keys()}
            if login_user_lower in users_lower:
                original_key = users_lower[login_user_lower]
                st.session_state.logged_in = True
                st.session_state.username = original_key
                ensure_user_fields(original_key)
                st.rerun()
            else:
                st.error("Benutzername nicht gefunden. Bitte zuerst registrieren.")

    with tab2:
        st.subheader("Registrieren")
        reg_user = st.text_input("Gewünschter Benutzername", key="reg_user")
        if st.button("Registrieren"):
            users = load_users()
            if reg_user == "":
                st.error("Bitte einen Benutzernamen eingeben.")
            elif reg_user.strip().lower() in {k.lower() for k in users.keys()}:
                st.error("Benutzername bereits vergeben.")
            else:
                users[reg_user.strip()] = {
                    "noten": {},
                    "wahlpflicht": {},
                    "setup_done": False,
                    "auslandssemester": False,
                    "auslands_faecher": []
                }
                save_users(users)
                st.success(f"Benutzer '{reg_user}' erfolgreich erstellt! Bitte jetzt einloggen.")

# ─── HAUPTSEITE ──────────────────────────────────────────────────────────────
else:
    ensure_user_fields(st.session_state.username)
    users = load_users()
    setup_done = users[st.session_state.username].get("setup_done", False)

    st.title("WINF Notendurchschnitt Rechner")
    st.markdown("Notendurchschnitt Rechner für WINF-Studierende mit Berücksichtigung der ECTS-Gewichtung")
    st.markdown(f"👤 Eingeloggt als: **{st.session_state.username}**")

    col_logout, col_reset = st.columns([1, 5])
    with col_logout:
        if st.button("Ausloggen"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    with col_reset:
        if setup_done:
            if st.button("🔄 Wahlpflichtmodule neu wählen"):
                users = load_users()
                users[st.session_state.username]["setup_done"] = False
                users[st.session_state.username]["wahlpflicht"] = {}
                save_users(users)
                st.rerun()

    st.divider()

    # ═══════════════════════════════════════════════════════════════════════
    # SCHRITT 1: WAHLPFLICHTMODULE WÄHLEN
    # ═══════════════════════════════════════════════════════════════════════
    if not setup_done:
        st.subheader("Schritt 1: Wahlpflichtmodule auswählen")
        st.markdown("Wähle deine Wahlpflichtmodule aus. Danach klicke auf **Weiter** um die Noten einzutragen.")
        kern_ects_total = sum(f["ECTS"] for f in KERNMODULE)
        st.info(f"ℹ️ Für den Master werden **{MASTER_ECTS} ECTS** benötigt. Kern-ECTS: **{kern_ects_total}** — du musst noch **{MASTER_ECTS - kern_ects_total} Wahl-ECTS** auswählen.")

        auswahl = {}
        laufende_wahl_ects = 0

        for kategorie, module in WAHLPFLICHT.items():
            st.markdown(f"**{kategorie}**")
            col1, col2, col3, col4 = st.columns(4)
            spalten_wahl = {1: col1, 2: col2, 3: col3, 4: col4}

            for modul in module:
                sem = modul["Semester"]
                col = spalten_wahl.get(sem, col4)
                key = f"{kategorie}__{modul['Fachname']}"
                with col:
                    gewaehlt = st.checkbox(
                        f"{modul['Fachname']} ({modul['ECTS']} ECTS) → Sem. {sem}",
                        value=False,
                        key=f"setup_{key}"
                    )
                    auswahl[key] = {
                        "gewaehlt": gewaehlt,
                        "note": 6.0,
                        "ects": modul["ECTS"],
                        "semester": sem
                    }
                    if gewaehlt:
                        laufende_wahl_ects += modul["ECTS"]
            st.divider()

        total_mit_wahl = kern_ects_total + laufende_wahl_ects
        fehlende_ects = MASTER_ECTS - total_mit_wahl

        if fehlende_ects > 0:
            st.warning(f"⚠️ Du hast aktuell **{total_mit_wahl} von {MASTER_ECTS} ECTS** ausgewählt. Dir fehlen noch **{fehlende_ects} Wahl-ECTS**.")
        else:
            st.success(f"✅ Du hast genügend ECTS ausgewählt: **{total_mit_wahl} ECTS** (Minimum: {MASTER_ECTS})")

        weiter_disabled = fehlende_ects > 0
        if st.button("Weiter zur Notenerfassung", disabled=weiter_disabled):
            users = load_users()
            users[st.session_state.username]["wahlpflicht"] = auswahl
            users[st.session_state.username]["setup_done"] = True
            save_users(users)
            st.rerun()

        if weiter_disabled:
            st.caption("Der Weiter-Button wird aktiv sobald du genügend ECTS ausgewählt hast.")

    # ═══════════════════════════════════════════════════════════════════════
    # SCHRITT 2: NOTEN ERFASSEN
    # ═══════════════════════════════════════════════════════════════════════
    else:
        users = load_users()
        noten = users[st.session_state.username].get("noten", {})
        wahlpflicht_gespeichert = users[st.session_state.username].get("wahlpflicht", {})
        auslandssemester = users[st.session_state.username].get("auslandssemester", False)
        auslands_faecher = users[st.session_state.username].get("auslands_faecher", [])

        neue_noten = {}
        neue_wahlpflicht = {}

        alle_wahlmodule = []
        for kategorie, module in WAHLPFLICHT.items():
            for modul in module:
                alle_wahlmodule.append({**modul, "kategorie": kategorie})

        gewaehlt_keys = {
            k for k, v in wahlpflicht_gespeichert.items() if v.get("gewaehlt", False)
        }

        total_kern_ects = sum(f["ECTS"] for f in KERNMODULE if not (
            auslandssemester and f["Semester"] == 3 and f["Fachname"] not in AUSLAND_PFLICHT
        ))
        total_wahl_ects = sum(
            v["ects"] for v in wahlpflicht_gespeichert.values()
            if v.get("gewaehlt", False) and not (auslandssemester and v.get("semester") == 3)
        )
        total_auslands_ects = sum(f.get("ects", 0) for f in auslands_faecher) if auslandssemester else 0
        total_ects_gesamt = total_kern_ects + total_wahl_ects + total_auslands_ects

        # ─── ECTS Übersicht klein & grau ─────────────────────────────────
        auslands_str = f" | Ausland: {total_auslands_ects} ECTS" if auslandssemester else ""
        st.caption(f"Kern: {total_kern_ects} ECTS | Wahl: {total_wahl_ects} ECTS{auslands_str} | Total: {total_ects_gesamt} / {MASTER_ECTS} ECTS")

        if total_ects_gesamt < MASTER_ECTS:
            st.warning(f"⚠️ Dir fehlen noch **{MASTER_ECTS - total_ects_gesamt} ECTS**.")

        ausland_toggle = st.toggle(
            "🌍 3. Semester: Auslandssemester",
            value=auslandssemester,
            help="Bei Aktivierung werden die fixen Module des 3. Semesters (ausser VMAT und AFEP) durch freie Eingabe ersetzt."
        )

        if ausland_toggle != auslandssemester:
            users = load_users()
            users[st.session_state.username]["auslandssemester"] = ausland_toggle
            if not ausland_toggle:
                users[st.session_state.username]["auslands_faecher"] = []
            save_users(users)
            st.rerun()

        st.divider()

        st.subheader("📚 WINF Curriculum — Noten eintragen")
        st.caption("Schweizer Notensystem: 6.0 = beste Note, 4.0 = Mindestanforderung zum Bestehen")
        col1, col2, col3, col4 = st.columns(4)
        spalten = {1: col1, 2: col2, 3: col3, 4: col4}

        for sem in [1, 2, 3, 4]:
            kern_sem = [f for f in KERNMODULE if f["Semester"] == sem]
            kern_ects_sem = sum(f["ECTS"] for f in kern_sem)
            wahl_sem = [
                m for m in alle_wahlmodule
                if m["Semester"] == sem and
                f"{m['kategorie']}__{m['Fachname']}" in gewaehlt_keys
            ]
            wahl_ects_sem = sum(m["ECTS"] for m in wahl_sem)

            with spalten[sem]:
                st.markdown(f"**{sem}. Semester**")

                if sem == 3 and auslandssemester:
                    st.caption("🌍 Auslandssemester")

                    for fach in kern_sem:
                        if fach["Fachname"] in AUSLAND_PFLICHT:
                            key = fach["Fachname"]
                            gespeicherte_note = noten.get(key, {})
                            prev_note = float(gespeicherte_note.get("note", 6.0)) if isinstance(gespeicherte_note, dict) else 6.0
                            note = st.number_input(
                                f"{fach['Fachname']} ({fach['ECTS']} ECTS)",
                                min_value=1.0, max_value=6.0, step=0.1,
                                value=prev_note,
                                key=f"kern_{key}",
                                format="%.1f"
                            )
                            neue_noten[key] = {"note": note, "ects": fach["ECTS"], "semester": sem}

                    st.markdown("---")

                    neue_auslands_faecher = []
                    for i, fach in enumerate(auslands_faecher):
                        t_col, x_col = st.columns([4, 1])
                        t_col.caption(f"Auslandsfach {i + 1}")
                        if x_col.button("x", key=f"ausland_remove_{i}"):
                            users = load_users()
                            users[st.session_state.username]["auslands_faecher"].pop(i)
                            save_users(users)
                            st.rerun()

                        n_col, e_col = st.columns([3, 1])
                        fname = n_col.text_input(
                            "Fachname",
                            value=fach.get("fachname", ""),
                            key=f"ausland_name_{i}",
                            label_visibility="collapsed",
                            placeholder="Fachname"
                        )
                        fects = e_col.number_input(
                            "ECTS",
                            min_value=1, max_value=30, step=1,
                            value=int(fach.get("ects", 3)),
                            key=f"ausland_ects_{i}",
                            label_visibility="collapsed"
                        )
                        fnote = st.number_input(
                            "Note",
                            min_value=1.0, max_value=6.0, step=0.1,
                            value=float(fach.get("note", 6.0)),
                            key=f"ausland_note_{i}",
                            format="%.1f"
                        )
                        neue_auslands_faecher.append({
                            "fachname": fname,
                            "note": fnote,
                            "ects": fects,
                            "semester": 3
                        })

                    if st.button("+ Fach hinzufügen", key="ausland_add"):
                        users = load_users()
                        users[st.session_state.username]["auslands_faecher"].append({
                            "fachname": "",
                            "note": 6.0,
                            "ects": 3,
                            "semester": 3
                        })
                        save_users(users)
                        st.rerun()

                    pflicht_ects = sum(f["ECTS"] for f in kern_sem if f["Fachname"] in AUSLAND_PFLICHT)
                    auslands_ects_sem = sum(f.get("ects", 0) for f in auslands_faecher)
                    st.markdown("---")
                    st.markdown(
                        f"<small>Pflicht: {pflicht_ects} ECTS &nbsp;|&nbsp; Ausland: {auslands_ects_sem} ECTS &nbsp;|&nbsp; Total: {pflicht_ects + auslands_ects_sem} ECTS</small>",
                        unsafe_allow_html=True
                    )

                else:
                    for fach in kern_sem:
                        key = fach["Fachname"]
                        gespeicherte_note = noten.get(key, {})
                        prev_note = float(gespeicherte_note.get("note", 6.0)) if isinstance(gespeicherte_note, dict) else 6.0
                        note = st.number_input(
                            f"{fach['Fachname']} ({fach['ECTS']} ECTS)",
                            min_value=1.0, max_value=6.0, step=0.1,
                            value=prev_note,
                            key=f"kern_{key}",
                            format="%.1f"
                        )
                        neue_noten[key] = {"note": note, "ects": fach["ECTS"], "semester": sem}

                    for modul in wahl_sem:
                        wkey = f"{modul['kategorie']}__{modul['Fachname']}"
                        gespeichert = wahlpflicht_gespeichert.get(wkey, {})
                        prev_note = float(gespeichert.get("note", 6.0))
                        note = st.number_input(
                            f"{modul['Fachname']} ({modul['ECTS']} ECTS) [Wahl]",
                            min_value=1.0, max_value=6.0, step=0.1,
                            value=prev_note,
                            key=f"wahl_{wkey}",
                            format="%.1f"
                        )
                        neue_wahlpflicht[wkey] = {
                            "gewaehlt": True,
                            "note": note,
                            "ects": modul["ECTS"],
                            "semester": sem
                        }

                    st.markdown("---")
                    st.markdown(
                        f"<small>Kern: {kern_ects_sem} ECTS &nbsp;|&nbsp; Wahl: {wahl_ects_sem} ECTS &nbsp;|&nbsp; Total: {kern_ects_sem + wahl_ects_sem} ECTS</small>",
                        unsafe_allow_html=True
                    )

        st.divider()

        if st.button("💾 Speichern & Berechnen"):
            if auslandssemester:
                users = load_users()
                users[st.session_state.username]["auslands_faecher"] = neue_auslands_faecher
                save_users(users)

            for k, v in wahlpflicht_gespeichert.items():
                if v.get("gewaehlt", False) and k not in neue_wahlpflicht:
                    if not (auslandssemester and v.get("semester") == 3):
                        neue_wahlpflicht[k] = v

            users = load_users()
            users[st.session_state.username]["noten"] = neue_noten
            users[st.session_state.username]["wahlpflicht"] = neue_wahlpflicht
            save_users(users)

            alle = []
            for key, val in neue_noten.items():
                alle.append({"note": val["note"], "ects": val["ects"], "semester": val["semester"]})
            for key, val in neue_wahlpflicht.items():
                if val["gewaehlt"]:
                    alle.append({"note": val["note"], "ects": val["ects"], "semester": val["semester"]})
            if auslandssemester:
                for fach in neue_auslands_faecher:
                    if fach["fachname"] and fach["ects"] > 0:
                        alle.append({"note": fach["note"], "ects": fach["ects"], "semester": 3})

            df = pd.DataFrame(alle)
            total_ects = df["ects"].sum()
            durchschnitt = (df["note"] * df["ects"]).sum() / total_ects

            st.session_state["ergebnis"] = {
                "durchschnitt": durchschnitt,
                "anzahl": len(df),
                "total_ects": total_ects,
                "semester": {
                    int(sem): {
                        "avg": (df[df["semester"] == sem]["note"] * df[df["semester"] == sem]["ects"]).sum() / df[df["semester"] == sem]["ects"].sum(),
                        "ects": df[df["semester"] == sem]["ects"].sum()
                    }
                    for sem in sorted(df["semester"].unique())
                }
            }
            st.rerun()

        if "ergebnis" in st.session_state:
            e = st.session_state["ergebnis"]
            st.success("✅ Gespeichert!")
            st.subheader("Gesamtergebnis Masterstudiengang")
            st.metric("Gewichteter Notendurchschnitt (gesamt)", f"{e['durchschnitt']:.2f}")
            st.info(f"Berechnet aus **{e['anzahl']}** Fächern mit total **{e['total_ects']} ECTS**")

            st.subheader("Notendurchschnitt pro Semester")
            for sem, val in e["semester"].items():
                label = f"Semester {sem}"
                if sem == 3 and auslandssemester:
                    label += " (Auslandssemester)"
                st.write(f"**{label}:** Ø {val['avg']:.2f} ({val['ects']} ECTS)")