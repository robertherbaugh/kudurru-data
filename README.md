# Kudurru catalog

Blocked-service domains and safe-search targets authored for Kudurru, published
as reusable Apache-2.0 data. The initial catalog contains 150 services in 15
categories and seven safe-search engines. It is schema version 2, catalog
version `2026.10.12`.

`catalogue.json` contains the data. `PROVENANCE.md` records its SHA-256 and the
source of every entry. Logos retain their original Apache-2.0 license and exact
upstream provenance under `icons/`. Product and service names and logos remain
the property of their respective owners. Inclusion does not imply endorsement.

This repository contains data, attribution and verification tooling. Kudurru's
application implementation is maintained separately at
<https://github.com/robertherbaugh/kudurru> under its own license.

## Use in Kudurru

The embedded catalog remains available offline. To select a published revision,
set `blocking.catalogue.url` to the HTTPS raw `catalogue.json` URL at a reviewed
full commit SHA in this repository. A commit URL pins the bytes; selecting a
moving branch instead intentionally opts into future updates.

Kudurru validates a downloaded document before replacing the catalog in service.
Malformed, oversized, incompatible or unavailable updates retain the last good
catalog. Policies choose services and safe-search engines explicitly. Fetching
this document alone does not enable blocking or safe search.

## Verify and update

Run `python3 verify.py` to verify the initial file manifest, JSON structure,
references and per-entry provenance. This needs only Python's standard library.
The consumer repository additionally compiles every service rule and tests DNS
behavior, safe-search targets, shared infrastructure and resolver exclusions.

For a proposed update:

1. Use vendor documentation or independently verified first-party domains.
   Record the original source for every changed service or engine. Do not copy
   GPL/EUPL service lists or other incompatible data.
2. Preserve existing IDs. Keep a service's domains specific to that service;
   avoid shared login, CDN and DNS resolver domains.
3. Update the catalog version and the matching provenance entries, SHA-256 and
   counts. Preserve source attribution and the icon license/provenance.
4. Regenerate `SHA256SUMS` for the reviewed files, run `python3 verify.py`, and run
   the consumer's catalog compilation and DNS tests before accepting the update.
5. Review and commit the change. Consumers pinned to a full commit SHA update
   only when their operator explicitly selects the new commit.

The data is licensed under Apache-2.0; see `LICENSE`. Contributions must be
original or compatible with that license and include their provenance.
