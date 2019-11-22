from snapshot import Snapshot
from add_link import TermToAdd
from replace_link import TermToReplace
from remove_link import TermToRemove

from typing import List

def from_snapshot(local_snapshot: List[Snapshot], remote_snapshot: List[Snapshot]) -> (List[TermToAdd], List[TermToReplace], List[TermToRemove]):
    terms_to_add = []
    for rs in remote_snapshot:
        term_to_add = TermToAdd(rs.url, rs.term)
        terms_to_add.append(term_to_add)
    
    local_snapshot_map = {}
    for ls in local_snapshot:
        local_snapshot_map[ls.id] = ls
    terms_to_replace = []
    for rs in remote_snapshot:
        if rs.id in local_snapshot_map:
            ls = local_snapshot_map[rs.id]
            if ls.term != rs.term:
                term_to_replace = TermToReplace(ls.url, rs.url, rs.term)
                terms_to_replace.append(term_to_replace)

    remote_snapshot_set = set()
    for rs in remote_snapshot:
        remote_snapshot_set.add(rs.id)
    terms_to_remove = []
    for ls in local_snapshot:
        if ls.id not in remote_snapshot_set:
            term_to_remove = TermToRemove(ls.url, ls.term)
            terms_to_remove.append(term_to_remove)


    return terms_to_add, terms_to_replace, terms_to_remove