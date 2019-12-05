from notion.client import NotionClient
from add_link import add_links
from replace_link import replace_links
from remove_link import remove_links

import converter
import os
import argparse
import snapshot

def run(notion_url):
    client = NotionClient(token_v2=os.getenv('NOTION_MIKAN_TOKEN'))

    remote_snapshot = snapshot.fetch_remote_snapshot(client)
    local_snapshot = snapshot.fetch_local_snapshot()
    to_add, to_replace, to_remove = converter.from_snapshot(local_snapshot, remote_snapshot)

    def _add_blocks(head_block, terms):
        for child in head_block.children:
            if hasattr(child, 'title'):
                child.title = add_links(child.title, terms)
            _add_blocks(child, terms)

    def _replace_blocks(head_block, terms):
        for child in head_block.children:
            if hasattr(child, 'title'):
                child.title = replace_links(child.title, terms)
            _replace_blocks(child, terms)

    def _remove_blocks(head_block, terms):
        for child in head_block.children:
            if hasattr(child, 'title'):
                child.title = remove_links(child.title, terms)
            _remove_blocks(child, terms)

    base_block = client.get_block(notion_url)
    # to prevent unnecessary traversing
    if len(to_replace) > 0:
        _replace_blocks(base_block, to_replace)
    if len(to_remove) > 0:
        _remove_blocks(base_block, to_remove)
    if len(to_add) > 0:
        _add_blocks(base_block, to_add)

    snapshot.save_remote_snapshot(remote_snapshot)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url")

    args = parser.parse_args()
    if not args.url:
        print("--url NotionのURL と語尾につけてください！ python main.py --url www.notion.py/... みたいに")
    else:
        run(args.url)