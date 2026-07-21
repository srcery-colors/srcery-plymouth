NAME := plymouth-theme-srcery
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
		--define "_srcrpmdir $(outdir)" \
		--define "version $(VERSION)"
