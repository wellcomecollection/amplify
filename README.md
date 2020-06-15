# AMPLIFY

Amplify: Assisted Metadata Processing for Libraries – a Feasibility Study

## Overview

Amplify uses machine learning to help librarians construct minimal viable catalogue records for works based only on rough images of their title page.

We allow the machine to take over a few stages of the initial cataloguing process:

- the reading and parsing of text on title pages
- translating text in non-english language / non-latin scripts
- querying third party catalogue APIs to look for matching existing catalogue records for the item
- querying our own catalogue for existing/duplicate versions of the item

Librarians are kept in control of the workflow, able to correct and and re-run queries at every stage of the process.  
Rather than letting the machine make strong assertions about which work/record is being viewed, the interface presents librarians with options which can always be corrected or augmented with locally relevant information.

**N.B.** This is still an experimental study of the feasibility of this kind of workflow - none of this work is being used in a production setting (yet).

## Docs

See [setup docs](docs/setup.md) for instructions on how to set up and run the project.

See [architecture docs](docs/architecture.md) for a rough description of the project's internal architecture and functionality.
