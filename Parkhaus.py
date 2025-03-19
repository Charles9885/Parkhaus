import requests
import json
import csv

def read_sse(url, csv_file):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Prueft, ob der Statuscode 200 ist
        with open(csv_file, 'a', newline='') as csvfile:
            fieldnames = None
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for line in response.iter_lines():
                if line:
                    data = line.decode('utf-8').strip()
                    if data.startswith('data:'):
                        json_data = data[5:].strip()
                        try:
                            parsed_json = json.loads(json_data)
                            # Schreibe die Daten in die CSV-Datei
                            if fieldnames is None:
                                fieldnames = parsed_json.keys()
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writeheader()
                            writer.writerow(parsed_json)
                        except json.JSONDecodeError:
                            print(f"Konnte JSON nicht decodieren: {json_data}")
            # Um den Endlosschleifen zu entgehen, brechen wir nach der ersten Datenuebertragung ab
            # Dieser Teil ist optional und haengt von deinen Anforderungen ab
            # if data and data.startswith('data:'):
            #     break
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")

def main():
    url = 'https://parken.telekom.net/isac3-web/public/sse/ci'
    csv_file = 'Parkhaus.csv'
    read_sse(url, csv_file)

if __name__ == "__main__":
    main()
