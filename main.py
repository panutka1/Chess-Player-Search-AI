import requests
import streamlit as st

def opis_szachisty(szachista):
    username = szachista['username']
    wynik_opis = (f"{szachista.get('title', '')} {szachista.get('name', username)}"
            f" has {szachista['followers']} followers and"
            f" is from {szachista.get('location', 'unknown')}")
    return wynik_opis
    


st.title("Chess Player Search")
wyszukany_zawodnik = st.text_input("Zawodnik")
button = st.button("Search")

def szukany_szachista(wyszukany_zawodnik):
    if wyszukany_zawodnik == '':
            st.write("Enter username!")
    else:
        try:
            url = f"https://api.chess.com/pub/player/{wyszukany_zawodnik}"
            payload = {}
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.request("GET", url, headers=headers, data=payload)

            status_code = (response.status_code)
            if status_code == 200:
                szachista = opis_szachisty(response.json())
                ready_data = szachista.strip()
                result = ready_data
                return result
                
            elif status_code == 404:
                response_404 = response.json()
                result = (response_404['message'])
                return result
            else:
                result = (f" message error code: {status_code}")
                return result

        except ValueError as e:
            result = (f"error: {e}")
            return result
        except KeyError as a:
            result = (f"error: {a}")
            return result


def streamlit_management():
    if button:
        result_to_stream = szukany_szachista(wyszukany_zawodnik)
        st.write(result_to_stream)

streamlit_management()
