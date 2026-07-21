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
