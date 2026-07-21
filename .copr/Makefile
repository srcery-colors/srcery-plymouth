NAME := plymouth-theme-srcery
# Contract: $(VERSION) below must always match plymouth-theme-srcery.spec's
# literal `Version:` tag exactly. RPM does not allow a command-line
# `--define "version ..."` to override a spec's hardcoded Version tag, so
# there is no way to wire this Makefile's computed version into the spec at
# build time. Bumping the release therefore requires updating BOTH the
# spec's Version: tag AND creating/moving the matching git tag before
# building an SRPM — they are not automatically kept in sync.
GIT_VERSION := $(shell git describe --tags 2>/dev/null | sed 's/^v//')
VERSION := $(if $(GIT_VERSION),$(GIT_VERSION),1.0.0)

.ONESHELL:
srpm:
	set -e
	trap 'rm -rf /tmp/$(NAME)-build' EXIT
	rm -rf /tmp/$(NAME)-build
	mkdir -p /tmp/$(NAME)-build
	git archive --prefix=$(NAME)-$(VERSION)/ HEAD | tar -x -C /tmp/$(NAME)-build
	tar czf $(outdir)/$(NAME)-$(VERSION).tar.gz -C /tmp/$(NAME)-build $(NAME)-$(VERSION)
	rpmbuild -bs $(NAME).spec \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)"
