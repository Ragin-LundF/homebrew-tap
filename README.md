# Ragin-LundF Homebrew tap

```sh
brew tap ragin-lundf/tap
brew install --cask 3d-hoard-deck     # 3D Hoard Deck: library for 3D printable files
brew install --cask ragin-dms         # Ragin DMS: document management
brew install --cask ruleengine-ui     # Rule Engine visual editor
brew install --cask ssh-connect       # ssh-connect: terminal UI for SSH servers
```

Or in one step, e.g. `brew install --cask ragin-lundf/tap/3d-hoard-deck`. Update with `brew upgrade`.

## First start on macOS

The apps are not signed with an Apple developer certificate yet. The first time you open one, macOS refuses it:
go to **System Settings › Privacy & Security** and choose **Open Anyway**. This is needed only once per app.

## How the casks are updated

- `ssh-connect` is written by GoReleaser on each ssh-connect release.
- The other casks are written by the **Update casks** workflow from the templates in `.github/cask-templates`.
  It runs every hour, picks the latest *published* release of each app (never drafts or prereleases), downloads
  its DMG, and commits the new version and checksum. To publish a cask right away, run the workflow by hand.
- To change a cask (name, description, `zap`, `auto_updates`), edit its template, then run the workflow with
  **force** on.
