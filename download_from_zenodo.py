import requests
import os
import argparse
def main():
    parser = argparse.ArgumentParser(description='Parses Json and passes arguments to download-artifacts-sh')
    parser.add_argument("-a", "--access_token")
    parser.add_argument("-r", "--record_id")

    args = parser.parse_args()

    r = requests.get(f"https://zenodo.org/api/records/{args.record_id}", params={'access_token': args.access_token})
    download_urls = [f['links']['self'] for f in r.json()['files']]
    filenames = [f['key'] for f in r.json()['files']]

    for filename, url in zip(filenames, download_urls):
        # if os.path.splitext(filename)[1] == ".gz" and "tiled" in filename:
        print("Downloading:", filename)
        print("url:", url)
        r = requests.get(url, params={'access_token': args.access_token})
        with open(f'artifacts/{filename}', 'wb') as f:
            f.write(r.content)

if __name__ == "__main__":
    main()