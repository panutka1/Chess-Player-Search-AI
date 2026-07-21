import requests
import streamlit as st

def player_data(player):
    username = player['username']
    wynik_opis = (f"{player.get('title', '')} {player.get('name', username)}"
            f" has {player['followers']} followers and"
            f" is from {player.get('location', 'unknown')}")
    return wynik_opis

def chess_player_search(player):
    if player == '':
            return "Enter username!"
    else:
        try:
            url = f"https://api.chess.com/pub/player/{player}"
            payload = {}
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.request("GET", url, headers=headers, data=payload, timeout=10)

            status_code = (response.status_code)
            if status_code == 200:
                data = player_data(response.json())
                ready_data = data.strip()
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
        except KeyError as e:
            result = (f"error: {e}")
            return result
        except requests.exceptions.RequestException as e:
            result = (f"Server error, try later: {e}")
            return result


def streamlit_management():
    st.title("Chess Player Search")
    player = st.text_input("Player")
    button = st.button("Search")
    if button:
        result_to_stream = chess_player_search(player)
        st.write(result_to_stream)

if __name__ == "__main__":
    streamlit_management()
