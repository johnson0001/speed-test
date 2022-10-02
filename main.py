import os
import csv
import json
import requests
import subprocess

def get_speedtest_result():

    process = subprocess.run(['speedtest', '--secure', '--json'], capture_output=True)
    return json.loads(process.stdout)

def bit_to_mbit(bit):
    
    return round(bit / 1024 / 1024, 2)

def write_csv(filepath, result):

    if os.path.exists(filepath):
        with open(filepath, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([result["timestamp"], bit_to_mbit(result["download"]), bit_to_mbit(result["upload"])])
    else:
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "download", "upload"])
            writer.writerow([result["timestamp"], bit_to_mbit(result["download"]), bit_to_mbit(result["upload"])])

def send_message(result):

    message = f"Timestamp: {result['timestamp']}\nDownload: {bit_to_mbit(result['download'])}\nUpload: {bit_to_mbit(result['upload'])}"

    url = "https://notify-api.line.me/api/notify"
    data = {"message": message}
    headers = {"Authorization": "Bearer " + line_token}
    try:
        requests.post(url, data=data, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == "__main__":
    csv_file = "result.csv"
    line_token = "QeuWrSlI3duuTnqXpFOzchf0vKgHt9OWmeqU2LV6Su9"
    result = get_speedtest_result()
    write_csv(csv_file, result)
    send_message(result)