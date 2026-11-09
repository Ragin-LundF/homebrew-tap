# Ragin-LundF Homebrew tap

Install an app with its full name. That is all you need, also with Homebrew 6 and later:

```sh
brew install --cask ragin-lundf/tap/3d-hoard-deck   # 3D Hoard Deck: library for 3D printable files
brew install --cask ragin-lundf/tap/ragin-dms       # Ragin DMS: document management
brew install --cask ragin-lundf/tap/ruleengine-ui   # Rule Engine visual editor
brew install --cask ragin-lundf/tap/ssh-connect     # ssh-connect: terminal UI for SSH servers
```

Update with `brew upgrade`. 3D Hoard Deck updates itself from version 1.1.0 on, so `brew upgrade` skips it;
use `brew upgrade --greedy` to update it through Homebrew anyway.

## Trusting this tap (Homebrew 6 and later)

Since [Homebrew 6.0.0](https://brew.sh/2026/06/11/homebrew-6.0.0/), Homebrew only runs code from third-party taps
you have trusted ([Tap Trust](https://docs.brew.sh/Tap-Trust)).

- Installing with the full name, as above, trusts just that app. Nothing else to do.
- To install with the short name (`brew install --cask 3d-hoard-deck`), trust the app first:

  ```sh
  brew tap ragin-lundf/tap
  brew trust --cask ragin-lundf/tap/3d-hoard-deck
  brew install --cask 3d-hoard-deck
  ```

- Or trust every cask of this tap, now and in the future: `brew trust ragin-lundf/tap`.
- `brew trust` lists what you trust; `brew untrust ragin-lundf/tap` takes the trust back.

If Homebrew refuses to load a cask from this tap, it is not trusted yet: run one of the commands above.

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
