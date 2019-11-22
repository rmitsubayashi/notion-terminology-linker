from notion.client import NotionClient

from typing import List
import csv
import os

class Snapshot:
    def __init__(self, id: str, term: str, url: str):
        self.id = id
        self.term = term
        self.url = url

def fetch_local_snapshot() -> List[Snapshot]:
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
    table = client.get_block("https://www.notion.so/bc0baa0329a84632a029a92135dc32dc?v=05869ec07e8d47ff9f831094f622bed4")
    # bug where collection.get_rows() returns nothing
    # https://github.com/jamalex/notion-py/issues/52
    ids = table.views[0].get()['page_sort']
    rows = []
    for id in ids: 
        rows.append(client.get_block(id))
    
    snapshots = []
    for row in rows:
        if not row.title:
            continue
        snapshot = Snapshot(row.id, row.title, row.get_browseable_url())
        snapshots.append(snapshot)
        
    return snapshots

def save_remote_snapshot(snapshots: List[Snapshot]):
    with open('local_snapshot.txt', 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        for snapshot in snapshots:
            csv_writer.writerow([snapshot.id, snapshot.term, snapshot.url])