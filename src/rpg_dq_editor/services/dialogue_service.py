"""Business logic for dialogue trees: CRUD, linking, orphan detection."""

from __future__ import annotations

from rpg_dq_editor.models.dialogue import DialogueNode, DialogueOption, DialogueTree


class DialogueService:
    def __init__(self, tree: DialogueTree) -> None:
        self._tree = tree

    def add_node(self, node: DialogueNode) -> None:
        if node.node_id in self._tree.nodes:
            raise ValueError(f"duplicate node_id: {node.node_id}")
        self._tree.nodes[node.node_id] = node

    def link_option(self, node_id: str, option_id: str, target_node_id: str) -> None:
        if target_node_id not in self._tree.nodes:
            raise KeyError(f"target node missing: {target_node_id}")
        node = self._tree.nodes[node_id]
        for opt in node.options:
            if opt.option_id == option_id:
                opt.target_node_id = target_node_id
                return
        raise KeyError(f"option missing: {option_id}")

    def orphan_nodes(self) -> list[str]:
        reachable = self._tree.reachable_ids()
        return sorted(set(self._tree.nodes) - reachable)

    def dead_ends(self) -> list[str]:
        return sorted(
            nid for nid, n in self._tree.nodes.items() if not n.options
        )

    def add_option(self, node_id: str, option: DialogueOption) -> None:
        self._tree.nodes[node_id].options.append(option)