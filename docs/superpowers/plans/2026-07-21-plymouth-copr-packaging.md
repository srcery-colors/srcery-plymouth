# Plymouth Srcery COPR Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `srcery-plymouth` (currently just theme data files + README + LICENSE) into a COPR-buildable, Fedora-guideline-conformant `plymouth-theme-srcery` RPM, without restructuring the existing `srcery/` asset layout.

**Architecture:** Add a root-level spec file that packages the existing `srcery/` directory verbatim into `/usr/share/plymouth/themes/srcery/`, a `.copr/Makefile` that builds a source tarball straight from the git checkout (no tito/rpkg), an `ATTRIBUTION.md` for the CC-BY-4.0 glyph frames, an expanded `README.md`, and a GitHub Actions workflow that lints and scratch-builds the spec on every PR. No code in `srcery.script` needs to change — it was already audited and contains no `%`-style formatting.

**Tech Stack:** RPM spec (rpmbuild), COPR SCM builds, GitHub Actions (this repo is hosted on GitHub, not GitLab — see Global Constraints), Fedora container (via `docker`) for local `rpmbuild`/`rpmlint` validation since neither tool is installed on this Mac.

## Global Constraints

- Package name: `plymouth-theme-srcery` (matches the `%package theme-*` naming convention Fedora's own `plymouth` srpm uses for bundled themes — verified at `src.fedoraproject.org/rpms/plymouth`).
- Repo URL: `https://github.com/srcery-colors/srcery-plymouth` (remote `origin`, default branch `main`; local branch is `master` and is byte-identical to `origin/main` as of this session).
- `License:` MUST be an SPDX expression: `MIT AND CC-BY-4.0` — `MIT` covers `srcery.plymouth`/`srcery.script` (repo's existing `LICENSE`), `CC-BY-4.0` covers the `eye-0*.png` glyph frames derived from the srcery-assets logo. Both identifiers confirmed present on Fedora's allowed-licenses table (`docs.fedoraproject.org/en-US/legal/allowed-licenses/`) as of this session.
- `BuildArch: noarch` — package ships only data files, no compiled code.
- Do **not** add a `%post` that force-activates the theme. Verified against the real, current Fedora `plymouth.spec` (`src.fedoraproject.org/rpms/plymouth/raw/rawhide/f/plymouth.spec`): none of its bundled theme subpackages (`theme-charge`, `theme-fade-in`, `theme-solar`, `theme-spinfinity`) auto-activate on install. They only clean up in `%postun`, guarded by `$1 -eq 0` (erase, not upgrade — confirmed against the exact `$1` semantics table on `docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/`), and only if this package's theme is the one currently active. This repo will follow the same pattern.
- `plymouth-set-default-theme` semantics verified directly from its source (`gitlab.freedesktop.org/plymouth/plymouth` → `scripts/plymouth-set-default-theme.in`): no-arg prints the current theme name; `--reset`/`-r` deletes the `Theme=` line from `plymouthd.conf` (falls back to the compiled default) and does **not** touch `/boot` unless `-R`/`--rebuild-initrd` is also passed. Our `%postun` will use `--reset` only — no `-R` — matching the upstream spec's own choice not to force an initrd rebuild on erase.
- Every scriptlet command whose failure shouldn't abort the transaction MUST end in `|| :` (per the Scriptlets guideline's "all scriptlets MUST exit with zero status" rule).
- `Requires(post): plymouth-scripts` and `Requires(postun): plymouth-scripts` are both declared (the upstream spec only declares `Requires(post)` even for postun-only scriptlets on some subpackages — a minor gap we intentionally close, since our `%postun` genuinely calls the `plymouth-scripts`-owned binary).
- CI: the task spec suggested "GitLab CI or COPR webhook", but this repo lives on GitHub, so we use **GitHub Actions** instead — flagged explicitly in the PR description as a deliberate deviation driven by the actual hosting platform, not a guess.
- ATTRIBUTION per CC BY 4.0's TASL convention (Title, Author, Source, License — verified at `wiki.creativecommons.org/wiki/Best_practices_for_attribution`): Author is "Daniel Berg and srcery-colors contributors" (confirmed verbatim from the `srcery-assets` repo's own README license line), Source is `https://github.com/srcery-colors/srcery-assets/blob/master/logo/glyph.svg`, License is CC BY 4.0, and the entry must note the glyph was adapted into 5 raster blink-keyframe PNGs for this package.
- Version scheme: repo has no prior tags/releases. Start at `1.0.0-1%{?dist}`, tag `v1.0.0` once merged. `.copr/Makefile` derives the tarball version from `git describe --tags --always`, falling back to `1.0.0` if no tag exists yet (it won't, on the first build).
- All new commits go on a new branch (`chore/copr-packaging`), not directly on `master`. Do not push or open the PR without asking first — pushing/opening a PR is an explicit-permission action.

---

### Task 1: ATTRIBUTION.md

**Files:**
- Create: `ATTRIBUTION.md`

**Interfaces:**
- Produces: a root-level `ATTRIBUTION.md` that Task 2's spec `%files` list references via `%doc`.

- [ ] **Step 1: Write the file**

```markdown
# Attribution

## Srcery eye glyph (boot animation frames)

- **Title:** Srcery glyph (`logo/glyph.svg`)
- **Author:** Daniel Berg and srcery-colors contributors
- **Source:** https://github.com/srcery-colors/srcery-assets/blob/master/logo/glyph.svg
- **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Modifications:** The vector glyph was rasterized and split into five PNG
  keyframes (`srcery/eye-00.png` through `srcery/eye-04.png`) representing an
  open → half → closed blink cycle, sized and cropped for use as Plymouth
  boot-splash sprites. No other assets in `srcery/` are derived from
  third-party sources.

All other files in this repository are original work licensed under the MIT
License — see `LICENSE`.
```

- [ ] **Step 2: Verify formatting renders correctly**

Run: `cat ATTRIBUTION.md`
Expected: file exists, renders as valid Markdown, no TODO/placeholder text.

- [ ] **Step 3: Commit**

```bash
git add ATTRIBUTION.md
git commit -m "docs: add CC-BY-4.0 attribution for eye glyph assets

Per CC BY 4.0's TASL attribution convention (creativecommons.org/wiki/Best_practices_for_attribution)."
```

---

### Task 2: `plymouth-theme-srcery.spec`

**Files:**
- Create: `plymouth-theme-srcery.spec`

**Interfaces:**
- Consumes: `LICENSE`, `README.md`, `ATTRIBUTION.md` (Task 1), `srcery/*` (existing, unmodified).
- Produces: an RPM installing to `/usr/share/plymouth/themes/srcery/`, package name `plymouth-theme-srcery`.

- [ ] **Step 1: Write the spec file**

```spec
Name:           plymouth-theme-srcery
Version:        1.0.0
Release:        1%{?dist}
Summary:        Srcery colorscheme boot splash theme for Plymouth

License:        MIT AND CC-BY-4.0
URL:            https://github.com/srcery-colors/srcery-plymouth
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       plymouth
Requires:       plymouth-plugin-script
Requires(post):   plymouth-scripts
Requires(postun): plymouth-scripts

%description
Srcery is a dark, contrast-forward colorscheme. This package installs a
Plymouth boot splash theme that renders the Srcery eye glyph, a progress
bar, and password/question dialogs in the Srcery palette.

Installing this package does not switch your active Plymouth theme. Run
`plymouth-set-default-theme -R srcery` afterwards (see README.md).

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to compile: this package ships static Plymouth theme data only.

%install
install -d %{buildroot}%{_datadir}/plymouth/themes/srcery
install -p -m 0644 srcery/srcery.plymouth %{buildroot}%{_datadir}/plymouth/themes/srcery/
install -p -m 0644 srcery/srcery.script %{buildroot}%{_datadir}/plymouth/themes/srcery/
install -p -m 0644 srcery/*.png %{buildroot}%{_datadir}/plymouth/themes/srcery/

%postun
export PLYMOUTH_PLUGIN_PATH=%{_libdir}/plymouth/
if [ "$1" -eq 0 ]; then
    if [ "$(%{_sbindir}/plymouth-set-default-theme 2>/dev/null)" == "srcery" ]; then
        %{_sbindir}/plymouth-set-default-theme --reset || :
    fi
fi

%files
%license LICENSE
%doc README.md ATTRIBUTION.md
%dir %{_datadir}/plymouth/themes/srcery
%{_datadir}/plymouth/themes/srcery/srcery.plymouth
%{_datadir}/plymouth/themes/srcery/srcery.script
%{_datadir}/plymouth/themes/srcery/*.png

%changelog
* Tue Jul 21 2026 Birger Johan Nordølum <me@mindtooth.no> - 1.0.0-1
- Initial COPR packaging: noarch spec, no forced theme activation on
  install, %%postun-only cleanup guarded by erase ($1 == 0) and
  currently-active-theme checks (docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/).
```

- [ ] **Step 2: Sanity-check the spec parses**

Run (from repo root, using a Fedora container since `rpmbuild` isn't installed on this Mac):
```bash
docker run --rm -v "$PWD":/repo:Z -w /repo fedora:latest \
  bash -c "dnf install -y rpmdevtools >/dev/null && rpmspec -q plymouth-theme-srcery.spec"
```
Expected: prints `plymouth-theme-srcery-1.0.0-1.<dist>.noarch` with no parse errors.

- [ ] **Step 3: Commit**

```bash
git add plymouth-theme-srcery.spec
git commit -m "packaging: add plymouth-theme-srcery.spec

noarch, SPDX license expression, %postun-only theme cleanup per verified
Fedora Scriptlets and plymouth-set-default-theme semantics."
```

---

### Task 3: `.copr/Makefile`

**Files:**
- Create: `.copr/Makefile`

**Interfaces:**
- Consumes: `plymouth-theme-srcery.spec` (Task 2).
- Produces: an SRPM in `$(outdir)` when COPR (or a local test) runs `make -f .copr/Makefile srpm outdir=<dir> spec=plymouth-theme-srcery.spec`, per the exact target signature documented at `docs.pagure.org/copr.copr/user_documentation.html`.

- [ ] **Step 1: Write the Makefile**

```makefile
NAME := plymouth-theme-srcery
VERSION := $(shell git describe --tags --always 2>/dev/null | sed 's/^v//' || echo 1.0.0)

srpm:
	rm -rf /tmp/$(NAME)-build
	mkdir -p /tmp/$(NAME)-build
	git archive --prefix=$(NAME)-$(VERSION)/ HEAD | tar -x -C /tmp/$(NAME)-build
	tar czf $(outdir)/$(NAME)-$(VERSION).tar.gz -C /tmp/$(NAME)-build $(NAME)-$(VERSION)
	rpmbuild -bs $(NAME).spec \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)" \
		--define "version $(VERSION)"
	rm -rf /tmp/$(NAME)-build
```

- [ ] **Step 2: Test the srpm target locally in a Fedora container**

```bash
mkdir -p /tmp/copr-outdir
docker run --rm -v "$PWD":/repo:Z -v /tmp/copr-outdir:/out:Z -w /repo fedora:latest \
  bash -c "dnf install -y rpmdevtools git >/dev/null && \
           git config --global --add safe.directory /repo && \
           make -f .copr/Makefile srpm outdir=/out spec=plymouth-theme-srcery.spec"
ls /tmp/copr-outdir
```
Expected: exits 0, `/tmp/copr-outdir` contains `plymouth-theme-srcery-1.0.0-1.<dist>.src.rpm` (or `-<gitdescribe>-` if a tag exists).

- [ ] **Step 3: Commit**

```bash
git add .copr/Makefile
git commit -m "packaging: add .copr/Makefile SCM srpm target

Implements the documented srpm target contract (docs.pagure.org/copr.copr/user_documentation.html):
builds Source0 from a git archive since COPR clones a fresh checkout with no
pre-built tarball."
```

---

### Task 4: README.md rewrite

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: package name/scriptlet behavior from Task 2, COPR project name (confirmed by user: `mindtooth/srcery`).

- [ ] **Step 1: Replace the empty "Installation" and "Screenshots" sections and requirements list**

Replace lines 27-35 of the current `README.md`:
```markdown
## Requirements

- Plymouth
- [plymouth-plugin-script](https://packages.fedoraproject.org/pkgs/plymouth/plymouth-plugin-script/)

## Installation

## Screenshots
```
with:
```markdown
## Requirements

- Plymouth
- [plymouth-plugin-script](https://packages.fedoraproject.org/pkgs/plymouth/plymouth-plugin-script/)

## Installation

Via COPR (Fedora/RHEL/CentOS and derivatives):

```bash
sudo dnf copr enable mindtooth/srcery
sudo dnf install plymouth-theme-srcery
```

Installing the package does **not** switch your boot splash automatically —
see [What the scriptlets do](#what-the-scriptlets-do) for why. To activate it:

```bash
sudo plymouth-set-default-theme -R srcery
```

`-R` rebuilds the initramfs, which is required for the new theme to actually
appear on the next boot.

## What the scriptlets do

This package intentionally has **no `%post` scriptlet** — installing it never
changes your active theme, matching how Fedora's own bundled Plymouth themes
behave (`plymouth-theme-solar`, `plymouth-theme-spinfinity`, etc. don't
self-activate either).

Its `%postun` scriptlet runs only on a genuine uninstall (RPM's `$1 == 0`
case, never on upgrade), and only touches your configuration if `srcery` is
still the *currently active* theme — in that case it clears the `Theme=`
line from `plymouthd.conf` (`plymouth-set-default-theme --reset`) so you
aren't left pointing at a theme whose files no longer exist. It never
rebuilds your initramfs on removal.

## Standalone vs. paired with the GRUB theme

This Plymouth theme works on its own. It's also designed to pair with the
sibling [srcery GRUB2 theme](https://github.com/srcery-colors) so the
boot sequence reads as one continuous animation: GRUB draws the same eye
glyph near the left edge of the boot menu, and this Plymouth theme spawns
the glyph at that same relative position before easing it to center. If you
only install this package, you still get the full boot splash — you just
won't get the GRUB-to-Plymouth handoff animation (Plymouth already detects
this: it skips the slide-in for the `shutdown`/`reboot` modes, since there's
no preceding GRUB screen then either).

## Tunables

- `EYE_START_X_FRAC` / `EYE_START_Y_FRAC` (top of `srcery/srcery.script`):
  the fractional screen position the glyph starts its intro animation from.
  These must match the image block's position in the GRUB theme's
  `theme.txt` for the slide-in to look continuous — if you move one, move
  the other.

## Screenshots

_TODO: add screenshots once available._
```

- [ ] **Step 2: Proofread rendered markdown**

Run: `cat README.md`
Expected: no broken links, no leftover empty headings, COPR command has an obvious `<owner>/<project>` placeholder for the user to fill in (flag this to the user rather than guessing a COPR namespace).

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: document COPR install, scriptlet behavior, and GRUB pairing

Explains the %postun-only cleanup behavior verbatim so users understand
why installing the package doesn't change their active theme."
```

---

### Task 5: GitHub Actions CI

**Files:**
- Create: `.github/workflows/rpm-ci.yml`

**Interfaces:**
- Consumes: `plymouth-theme-srcery.spec` (Task 2), `.copr/Makefile` (Task 3).

- [ ] **Step 1: Write the workflow**

```yaml
name: RPM packaging checks

on:
  pull_request:
  push:
    branches: [main]

jobs:
  rpmlint-and-scratch-build:
    runs-on: ubuntu-latest
    container: fedora:latest
    steps:
      - name: Install tooling
        run: dnf install -y rpmlint rpmdevtools git
      - name: Check out repository
        uses: actions/checkout@v4
      - name: Mark repo safe for git (container root vs checkout owner)
        run: git config --global --add safe.directory "$GITHUB_WORKSPACE"
      - name: rpmlint the spec
        run: rpmlint plymouth-theme-srcery.spec
      - name: Scratch build an SRPM via the COPR Makefile contract
        run: |
          mkdir -p /tmp/outdir
          make -f .copr/Makefile srpm outdir=/tmp/outdir spec=plymouth-theme-srcery.spec
          ls /tmp/outdir/*.src.rpm
```

- [ ] **Step 2: Validate the workflow YAML parses**

Run: `docker run --rm -v "$PWD":/repo:Z -w /repo fedora:latest bash -c "dnf install -y python3-pyyaml >/dev/null && python3 -c \"import yaml; yaml.safe_load(open('.github/workflows/rpm-ci.yml'))\""`
Expected: exits 0, no exception.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/rpm-ci.yml
git commit -m "ci: run rpmlint and a scratch SRPM build on every PR

No existing CI in this repo to integrate with, so this adds a minimal
GitHub Actions workflow (repo is hosted on GitHub, not GitLab, so this
substitutes for the GitLab-CI suggestion in the packaging spec)."
```

---

### Task 6: Full local validation pass

**Files:** none (verification only).

**Interfaces:**
- Consumes: everything from Tasks 1-5.

- [ ] **Step 1: Build the real tarball and both SRPM and RPM in one container run**

```bash
mkdir -p /tmp/rpm-outdir
docker run --rm -v "$PWD":/repo:Z -v /tmp/rpm-outdir:/out:Z -w /repo fedora:latest bash -c '
  set -e
  dnf install -y rpmlint rpmdevtools git
  git config --global --add safe.directory /repo
  rpmlint plymouth-theme-srcery.spec

  # Build the tarball the same way .copr/Makefile does, but keep the
  # intermediate around so we can run -bs and -bb explicitly.
  VERSION=$(git describe --tags --always 2>/dev/null | sed "s/^v//" || echo 1.0.0)
  rm -rf /tmp/build && mkdir -p /tmp/build
  git archive --prefix=plymouth-theme-srcery-$VERSION/ HEAD | tar -x -C /tmp/build
  tar czf /out/plymouth-theme-srcery-$VERSION.tar.gz -C /tmp/build plymouth-theme-srcery-$VERSION

  rpmbuild -bs plymouth-theme-srcery.spec \
    --define "_sourcedir /out" --define "_srcrpmdir /out" --define "version $VERSION"
  rpmbuild -bb plymouth-theme-srcery.spec \
    --define "_sourcedir /out" --define "_rpmdir /out" --define "version $VERSION"

  echo "--- files ---"
  rpm -qlp /out/noarch/plymouth-theme-srcery-*.noarch.rpm
  echo "--- scripts ---"
  rpm -qp --scripts /out/noarch/plymouth-theme-srcery-*.noarch.rpm
  echo "--- requires ---"
  rpm -qp --requires /out/noarch/plymouth-theme-srcery-*.noarch.rpm
'
```
Expected:
- `rpmlint` reports 0 errors (warnings about e.g. missing `%changelog` version bump format are acceptable to note but not required to fix).
- `rpmbuild -bs` exits 0 and produces a `.src.rpm` in `/out`.
- `rpmbuild -bb` exits 0 (run separately from `-bs`, per the exact validation checklist in the packaging task) and produces `/out/noarch/plymouth-theme-srcery-*.noarch.rpm`.
- `rpm -qlp` lists exactly: the theme dir, `srcery.plymouth`, `srcery.script`, the 9 PNGs, plus doc/license paths — nothing else (no leaked buildroot paths, no missing files).
- `rpm -qp --scripts` shows the `%postun` block expanded with macros resolved (no literal `%{_sbindir}` left unexpanded).
- `rpm -qp --requires` includes `plymouth`, `plymouth-plugin-script`, and the `plymouth-scripts` postun-scriptlet dependency — confirming `Requires:` wasn't accidentally placed after `%description` (the known failure mode from this codebase's history where `Requires:` gets silently dropped).

- [ ] **Step 2: Fix anything the validation surfaces**

If `rpmlint` or the file/scriptlet/requires checks turn up a real problem (not a style nit), fix it in the relevant task's file and re-run Step 1 before moving on. Do not proceed to Task 7 with unresolved errors.

- [ ] **Step 3: No commit for this task** — it's pure verification. If Step 2 required a fix, that fix's commit belongs to whichever Task's file it touched (amend that task's story by adding a small follow-up commit, e.g. `fix: correct rpmlint warning in plymouth-theme-srcery.spec`).

---

### Task 7: Gap list + branch wrap-up

**Files:** none (process only).

- [ ] **Step 1: Confirm branch state**

```bash
git log --oneline master..HEAD 2>/dev/null || git log --oneline -7
git status
```
Expected: a clean working tree, one commit per task above (plus any Task 6 fixups), all on `chore/copr-packaging`.

- [ ] **Step 2: Write the gap list into the PR description (not a repo file)**

Summarize, for the human reviewer: what was missing before (no spec, no `.copr/Makefile`, no `ATTRIBUTION.md`, no CI, thin README) vs. what each commit added, and explicitly flag the two judgment calls that weren't literal spec matches:
1. GitHub Actions instead of GitLab CI (repo is hosted on GitHub).
2. `%postun`-only theme cleanup instead of any `%post` activation (matches verified real-world Fedora `plymouth.spec` precedent rather than force-switching the user's theme).
The COPR namespace (`mindtooth/srcery`) was confirmed by the user up front, so the README ships with the real command, not a placeholder.

Also record, as a checked-and-passed item (not a change made): `srcery/srcery.script` was audited against the "known failure modes" list before any packaging work started — it uses only `+` string concatenation (e.g. `"eye-0" + i + ".png"`), never `%`-style formatting, so the "Plymouth `%`-format strings parsing as garbage filenames and rendering nothing" failure mode does not apply here and required no fix.

- [ ] **Step 3: Stop and ask the user**

Do not push the branch or open a PR/MR without asking first (pushing and opening PRs are explicit-permission actions). Ask: push `chore/copr-packaging` and open a PR now, or leave it local for the user to review first?
