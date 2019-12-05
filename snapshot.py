from notion.client import NotionClient

from typing import List
import csv
import os
from google.cloud import storage

class Snapshot:
    def __init__(self, id: str, term: str, url: str):
        self.id = id
        self.term = term
        self.url = url

def fetch_local_snapshot() -> List[Snapshot]:
    if _is_on_gae():
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(os.getenv('STORAGE_BUCKET'))
        blob = bucket.blob("mikan-terminology-linker/local_snapshot.txt")
        snapshot_string = blob.download_as_string().decode('utf-8')
        snapshot_strings = snapshot_string.split('\n')
        snapshots = []
        for s in snapshot_strings:
            if not s:
                continue
            snapshot_arr = s.split(',')
            if len(snapshot_arr) != 3:
                continue
            snapshot = Snapshot(snapshot_arr[0], snapshot_arr[1], snapshot_arr[2])
            snapshots.append(snapshot)
        return snapshots
    else:
        snapshots = []
        if not os.path.exists('local_snapshot.txt'):
            return snapshots
        with open('local_snapshot.txt', 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                snapshot = Snapshot(row[0], row[1], row[2])
                snapshots.append(snapshot)
        return snapshots

def fetch_remote_snapshot(client: NotionClient) -> List[Snapshot]:
    table = client.get_block("https://www.notion.so/mikantechnology/3e6a181e18a5421fb42d7bf137a6b500?v=29ab01d76c6d4058a1349ee29f8ed90a")
    # bug where collection.get_rows() returns nothing
    # https://github.com/jamalex/notion-py/issues/52
    ids = table.views[0].get()['page_sort']
    rows = []
    for id in ids: 
        block = client.get_block(id)
        if block is not None:
            rows.append(block)
    
    snapshots = []
    for row in rows:
        if not row.title:
            continue
        snapshot = Snapshot(row.id, row.title, row.get_browseable_url())
        snapshots.append(snapshot)
    return snapshots

def save_remote_snapshot(snapshots: List[Snapshot]):
    if _is_on_gae():
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(os.getenv('STORAGE_BUCKET'))
        blob = bucket.blob("mikan-terminology-linker/local_snapshot.txt")
        snapshots_str = ''
        for snapshot in snapshots:
            snapshots_str += snapshot.id + ',' + snapshot.term + ',' + snapshot.url + '\n'
        
        blob.upload_from_string(snapshots_str)
    else:
        with open('local_snapshot.txt', 'w', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            for snapshot in snapshots:
                csv_writer.writerow([snapshot.id, snapshot.term, snapshot.url])

def _is_on_gae():
    return False