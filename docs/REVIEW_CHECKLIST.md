# Owner review — RC1

## Interface

- [ ] Research desk: typography, spacing, contrast and language feel right.
- [ ] Document library: title search, visibility labels and empty state are clear.
- [ ] Upload dialog: text/Markdown import and pasted content are comfortable to use.
- [ ] Ask a question; inspect the research note and click its numbered source.
- [ ] Ask an unrelated question; check evidence-insufficiency behavior.
- [ ] Open the mobile navigation; switch views on your actual phone.
- [ ] Review on iOS Safari, Android Chrome and a computer. Size buttons only simulate widths.

## Full backend locally

- [ ] Run the app and load the fictional sample library.
- [ ] Check admin/reader behavior with the actual backend passwords.
- [ ] Delete a test document and confirm its excerpts disappear.
- [ ] Restart the process and confirm documents/session persist.
- [ ] Run the supplied tests and read ARCHITECTURE.md.

## Before independent deployment

- [ ] Approve the code version for GitHub upload.
- [ ] Provision separate managed PostgreSQL databases for testing and hosting.
- [ ] Run the real PostgreSQL integration test and initialize production tables.
- [ ] Configure Azure model deployments and verify real calls.
- [ ] Deploy the reviewed commit to Vercel and complete the live checklist.

No user GitHub upload or Vercel deployment has occurred. Cloud credentials are not embedded in this package.
