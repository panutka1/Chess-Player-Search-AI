import json
import requests
import streamlit as st

def opis_szachisty(szachista):
    username = szachista['username']
    return (f"{szachista.get('title', '')} {szachista.get('name', username)}"
            f" has {szachista['followers']} followers and"
            f" is from {szachista.get('location', 'unknown')}")
    


st.title("Chess Player Search")
wyszukany_zawodnik = st.text_input("Zawodnik")
button = st.button("Search")

if button:
    if wyszukany_zawodnik == '':
        st.write("Nie podano nazwy uzytkownika!")
    else:
        try:
            url = f"https://api.chess.com/pub/player/{wyszukany_zawodnik}"
            payload = {}
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.request("GET", url, headers=headers, data=payload)
            status_code = (response.status_code)
            #st.write(response.json())
            #st.write(status_code)
            #st.write(response.json())
            if status_code == 200:
                #st.write(f"{status_code} + OK")
                szachista = opis_szachisty(response.json())
                ready_data = szachista.strip()
                st.write(ready_data)
                #print(szachista.strip())
            elif status_code == 404:
                response_404 = response.json()
                st.write(response_404['message'])
            else:
                st.write(f" message error code: {status_code}")

        except ValueError as e:
            st.write(f"error: {e}")
        except KeyError as a:
            st.write(f"error: {a}")


