+++
title = "{{ replace .File.ContentBaseName "-" " " | title }}"
date = {{ .Date }}
draft = true
categories = []   # the kind of work, shown above the title, e.g. "Research" or "Fieldwork"
tags = []         # shown under the photo on the project page

# One or two sentences: the question the project asks and the short answer.
summary = ""

[params]
  # Main projects are full-width stories with a large photo; others are cards a third wide.
  main = false
  start = {{ dateFormat "2006" .Date }}
  end = "Present"
  # Key outcomes, shown as bullets on the projects list and under "Contributions".
  contributions = []
  # People who worked on the project, and what they did:
  #   { name = "Name", contribution = "What they did" }, or just "Name".
  contributors = []
  # IDs from data/publications.yaml
  publications = []

  # Put an image named cover.* (or featured.*) next to this file,
  # or point to another image in the bundle.
  [params.cover]
    image = ""
    alt = ""
    caption = ""
+++

