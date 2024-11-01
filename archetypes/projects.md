+++
type = "project"
title = "{{ replace .File.ContentBaseName '-' ' ' | title }}"
categories = []
tags = []
[params]
    start = {{ dateFormat "2006" .Date }}
    end = {{ dateFormat "2006" .Date }}
    abstract = ""
    publications = []
+++