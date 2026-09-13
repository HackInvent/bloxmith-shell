# -----------------------------------------------------------------------------
# Role: Implements the shell block runtime and UI contract.
# File Name: block.py
# Author: Alexandre EL
# Email: alex@hackinvent.com
# Created Date: 2024-08-01
# -----------------------------------------------------------------------------

from __future__ import annotations

from typing import Any

from bloxsmith_app.block_api import (
    BlockDefinition,
    BlockRuntimeContext,
    BlockRuntimeOutput,
    BlockRuntimeResult,
    render_inspector_template,
    render_node_card_template,
    TEXT_PLAIN,
)


# Functional behavior:
# FB1 - Forward the current input message to every output as text/plain.
# FB2 - Log passthrough behavior and forwarded payload size.
# FB3 - Never execute operating-system shell commands; command execution belongs to the CLI block.
class ShellBlock(BlockDefinition):
    """Autonomous block implementation for `ShellBlock`."""
    kind = "shell"

    def ui_assets(self, surface: str = "modal") -> list[dict[str, str]]:
        """Return block-owned frontend assets for the requested UI surface.

        Args:
            surface: UI surface requesting assets.
        """
        return []

    def render_node_card(self, *, node: dict[str, Any], payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Render the Shell passthrough canvas card body from the block template."""

        return render_node_card_template(
            block=self,
            node=node,
            node_classes=["cli-node"],
            replacements={
                "title": node.get("title") or self.default_title(),
                "preview": "input -> output",
                "mode": "passthrough",
            },
        )

    def render_inspector_panel(self, *, node: dict[str, Any], payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Render the block-owned inspector panel HTML for the selected node.

        Args:
            node: Serialized graph node handled by the block.
            payload: Optional UI or runtime payload provided by the framework.
        """
        template = (self.directory / "inspector_panel.html").read_text(encoding="utf-8")
        html = render_inspector_template(
            template=template,
            node={**node, "type": self.kind, "kind": self.kind},
            payload=payload,
        )
        return {"html": html, "context": {"node_id": str(node.get("id") or ""), "full_panel": True}}

    def execute_runtime(self, context: BlockRuntimeContext) -> BlockRuntimeResult:
        """Execute the block through the generic runtime context and return runtime outputs.

        Args:
            context: Generic runtime context injected by the execution engine.
        """
        value = str(context.input_message or "")
        outputs = [
            BlockRuntimeOutput(
                port_id=int(getattr(port, "id", 0) or 0),
                port_name=str(getattr(port, "name", "") or ""),
                value=value,
                content_type=TEXT_PLAIN,
            )
            for port in context.output_ports
        ]
        return BlockRuntimeResult(
            status="success",
            outputs=outputs,
            logs=[f"[shell] {context.node_id}: passthrough actif ({len(value)} caractere(s))."],
            last_message=value,
            content_type=TEXT_PLAIN,
            worker_received=value,
        )
