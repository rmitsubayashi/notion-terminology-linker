from notion.client import NotionClient
from add_link import add_links
from replace_link import replace_links
from remove_link import remove_links

import converter
import os
import snapshot

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

base_block = client.get_block('https://www.notion.so/Test-Page2-90941d48ed694d15bafc50746b73a016')
_replace_blocks(base_block, to_replace)
_remove_blocks(base_block, to_remove)
_add_blocks(base_block, to_add)

snapshot.save_remote_snapshot(remote_snapshot)