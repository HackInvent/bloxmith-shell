#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Role: Verifies shell passthrough block behavior for the shell block.
# File Name: F5.13_shell_passthrough_block.py
# Author: Alexandre EL
# Email: alex@hackinvent.com
# Created Date: 2024-09-07
# -----------------------------------------------------------------------------

"""F5.13 - Shell passthrough block.

The test runs `text -> shell -> display` in an isolated server. The Shell
block is a runtime passthrough placeholder, not an operating-system command
runner, so the test verifies that it forwards input text to its output.
"""

# Test cases:
# - FB1 - Run text -> shell -> display and verify the Shell output equals the input.
# - FB2/FB3 - Verify Shell logs identify passthrough behavior and never command execution.

from ui_smoke_common import (
    create_run_api,
    data_edge,
    display_node,
    expect,
    graph_payload,
    isolated_server,
    text_node,
    wait_for_run_terminal,
)

from bloxsmith_app.block_ui import render_block_modal


def shell_node() -> dict:
    return {
        "id": "shell-1",
        "kind": "shell",
        "title": "Shell passthrough",
        "position": {"x": 360, "y": 120},
        "inputs": [
            {"id": 1, "name": "in", "title": "In", "accepts": ["message/*"], "multiplicity": "many"}
        ],
        "outputs": [
            {"id": 1, "name": "out", "title": "Out", "emits": ["message/*"], "multiplicity": "many"}
        ],
        "config": {},
    }


def test_shell_modal_uses_generic_surface_contract() -> None:
    """TC3 - Shell modal stays a simple generic surface without block JS."""

    rendered = render_block_modal("shell", {"node": shell_node(), "runtime": {}})
    html = str(rendered.get("html") or "")
    assets = rendered.get("assets") or []

    expect("block-config-modal" in html, "Shell modal must use the generic config layout.")
    expect("data-block-apply" in html, "Shell modal must keep generic Apply persistence.")
    expect("data-block-runtime-refresh" not in html, "Shell modal must not claim autonomous refresh without block JS.")
    expect(assets == [], "Shell modal must not declare block JS while it has no custom interaction.")


def test_shell_runtime_mode(runtime_mode: str) -> None:
    """Run the Shell passthrough mini-graph through one selected execution engine."""

    with isolated_server() as server:
        document = graph_payload(
            f"F5 Shell passthrough {runtime_mode}",
            [
                text_node("text-1", "Text source", "hello shell", 80, 120),
                shell_node(),
                display_node("display-1", "Display", 640, 120),
            ],
            [
                data_edge("edge-text-shell", "text-1", 1, "shell-1", 1),
                data_edge("edge-shell-display", "shell-1", 1, "display-1", 1),
            ],
        )
        created = create_run_api(server, document, runtime_mode=runtime_mode)
        run = wait_for_run_terminal(server, str(created.get("run_id") or ""), timeout_sec=20)

        expect(run.get("status") == "success", f"Shell passthrough {runtime_mode} run must succeed.")
        expect(run.get("runtime_mode") == runtime_mode, f"Shell run must remain in {runtime_mode}.")
        expect(
            run.get("output_values", {}).get("shell-1:1", {}).get("value") == "hello shell",
            "Shell output must match input text.",
        )
        logs = "\n".join(run.get("logs") or [])
        expect("[shell] shell-1: passthrough actif" in logs, "Shell passthrough log is missing.")
        if runtime_mode == "zeromq_active":
            expect(
                run.get("results", {}).get("shell-1", {}).get("transport") == "zeromq_active",
                "Shell active must not use centralized execution.",
            )


def main() -> None:
    test_shell_modal_uses_generic_surface_contract()
    for runtime_mode in ("centralized", "zeromq_active"):
        test_shell_runtime_mode(runtime_mode)
    print("[ok] F5.13_shell_passthrough_block")


if __name__ == "__main__":
    main()
