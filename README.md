# Hugo Theme: Live CV

*Live CV* is a Hugo theme designed for building academic-style online curriculum vitae.

## Demo

View a live demo of the theme (built using the exampleSite as the source and featuring a fictional character Evander Grimveil) hosted on [GitHub Pages](https://ziruifan.github.io/hugo-theme-live-cv).

![preview](images/preview.png)

## Features

- **Academic Styling**: Clean, professional design optimized for academic CVs.
- **Custom Project Profiles**:
  - Flexible date fields for start and end dates.
  - Option to link projects with related publications.
- **Easy Publication Management**:
  - Automatic author name highlighting.
  - Support for defining representative publications.
- **Responsive Design**: 
  - Adaptive layout for various screen sizes.
  - Automatic light/dark mode based on system preferences.

## Installation

To install *Live CV*, run the following commands in the root directory of your Hugo site:

```bash
cd themes
git clone https://github.com/ziruifan/hugo-theme-live-cv.git
```

## Configuration

Site configurations are defined in the main Hugo configuration file (e.g., `hugo.toml`). Available sections include Contacts, Research Interests, Education, Employment, Projects, Publications, Awards, Posts, and People. For an example, refer to [exampleSite/hugo.toml](https://github.com/ziruifan/hugo-theme-live-cv/blob/main/exampleSite/hugo.toml).

## Usage

The file tree below shows the structure of the site’s content directory:

```
.
└── content/
    ├── posts/
    │   ├── post-1/
    │   │   ├── index.md
    │   │   └── image.png
    │   └── post-2/
    │       └── index.md
    └── projects/
        └── project-1/
            └── index.md
```

To create a new page, run one of the following commands in the root directory of your Hugo site:

For a new post:
```bash
hugo new content/posts/post-1/index.md
```

For a new project:
```bash
hugo new content/projects/project-1/index.md
```