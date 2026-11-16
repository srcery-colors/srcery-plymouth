NAME := plymouth-theme-srcery
# The spec's Version: is the single source of truth; the tarball name must match it.
VERSION := $(shell awk '/^Version:/{print $$2}' $(NAME).spec)

srpm:
	# tar, not git archive: COPR's make_srpm chroot has no git. Packs the working tree, so build from a clean clone.
	tar czf $(outdir)/$(NAME)-$(VERSION).tar.gz --exclude-vcs --transform 's,^\.,$(NAME)-$(VERSION),' .
	rpmbuild -bs $(NAME).spec \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)"
