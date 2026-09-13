# Shell Block

<!-- block-metadata:start -->
[![Block version: unversioned](https://img.shields.io/badge/block-unversioned-lightgrey)](model.json)
[![BloxSmith compatibility: 1.0.9](https://img.shields.io/badge/BloxSmith-1.0.9-brightgreen)](compatibility.json)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

Verified BloxSmith versions: **1.0.9** (bundled-block tests; see [test evidence](compatibility.json)).
<!-- block-metadata:end -->


## Role

`shell` is a compatibility passthrough block. Despite its name, it does not execute operating-system commands.

## Files

- `block.py`: passthrough runtime behavior and inspector rendering.
- `model.json`: one input and one output.
- `inspector_panel.html`: shell inspector UI.
- `node_card.html`: block-owned canvas card body.

## Ports

- Inputs:
  - `in` (`id: 1`): optional `message/*`.
- Outputs:
  - `out` (`id: 1`): emits `message/*`.

## Configuration

No config is required.

## Runtime Behavior

`execute_runtime()` forwards `context.input_message` to every output as `text/plain` and logs the forwarded payload size.

## UI Behavior

The inspector is informational.

## Editor Display

The canvas card is rendered by this block through `node_card.html`. It exposes the passthrough behavior while the shared editor shell keeps ports, dragging, status, and graph links generic.

## Modal

`block_modal.html` is owned by this block and rendered by the generic modal contract. It shows block state and lets users edit supported title/config fields through generic bindings. It intentionally does not declare autonomous refresh or block-owned modal JavaScript because it has no custom modal interaction beyond generic Apply.

## Maintenance Notes

Do not add command execution here. Use the `cli` block for subprocess execution.

## Compatibility policy

[compatibility.json](compatibility.json) records HackInvent's verified BloxSmith versions and test evidence. Only the versions listed above have been verified, using the block-owned suites in a **bundled-block test installation**. This is not a certification of managed-package installation, every browser/OS, or live provider availability. Other framework versions are unverified, not necessarily incompatible.

The block-version badge follows `model.json`, not a published Git tag. `unversioned` means that no block release version is declared; no number is inferred from the framework version. The framework still uses `model.json` for its runtime/install contract; the tester-owned JSON does not replace it. Official integration tests run in the private `bloxmith-blocs` workspace. Test helpers and the proprietary framework are not bundled in this public block repository.
