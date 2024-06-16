import subprocess
import json

def wyslij_zadanie(url):
    try:
        odpowiedz = subprocess.check_output(['curl', '-s', url])
        return odpowiedz
    except subprocess.CalledProcessError as e:
        print(f"Błąd przy wysyłaniu żądania do {url}: {e}")
        return None

def sprawdz_odpowiedz(odpowiedz, oczekiwany_status=200):
    if odpowiedz is None:
        return False, "Brak odpowiedzi"
    
    try:
        odpowiedz_json = json.loads(odpowiedz)
    except json.JSONDecodeError:
        return False, "Niepoprawny JSON"

    return True, odpowiedz_json

def testuj_endpoint(url, oczekiwane_klucze):
    odpowiedz = wyslij_zadanie(url)
    status_ok, odpowiedz_json = sprawdz_odpowiedz(odpowiedz)
    
    if not status_ok:
        print(f"Test dla {url}: NIE POWIÓDŁ SIĘ ({odpowiedz_json})")
        return
    
    for klucz in oczekiwane_klucze:
        if klucz not in odpowiedz_json:
            print(f"Test dla {url}: NIE POWIÓDŁ SIĘ (brak klucza '{klucz}')")
            return

    print(f"Test dla {url}: UDANY")

def main():
    baza_url = 'https://jsonplaceholder.typicode.com'
    endpointy = [
        {'url': f'{baza_url}/posts/1', 'klucze': ['userId', 'id', 'title', 'body']},
        {'url': f'{baza_url}/comments/1', 'klucze': ['postId', 'id', 'name', 'email', 'body']},
        {'url': f'{baza_url}/users/1', 'klucze': ['id', 'name', 'username', 'email']}
    ]
    
    for endpoint in endpointy:
        testuj_endpoint(endpoint['url'], endpoint['klucze'])

if __name__ == "__main__":
    main()
