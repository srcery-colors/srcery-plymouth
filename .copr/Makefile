NAME := plymouth-theme-srcery
# The spec's Version: is the single source of truth; the tarball name must match it.
VERSION := $(shell awk '/^Version:/{print $$2}' $(NAME).spec)

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
