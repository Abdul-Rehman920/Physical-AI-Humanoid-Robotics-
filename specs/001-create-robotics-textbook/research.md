# Research: Create Robotics Textbook

## Decisions

- **Static Site Generator**: Docusaurus v3
  - **Rationale**: It is specifically designed for content-rich sites like documentation and books. It uses React, supports MDX for rich content, and has excellent features like search, versioning, and i18n out of the box. It aligns perfectly with all user requirements.
  - **Alternatives Considered**: Next.js with custom solution, GitBook. Docusaurus was chosen for its focus on documentation and ease of use.

- **Search**: Algolia DocSearch
  - **Rationale**: It is the recommended search solution for Docusaurus and provides a high-quality search experience with minimal configuration.
  - **Alternatives Considered**: Custom search solution. Algolia is more powerful and requires less development effort.

- **Deployment**: GitHub Pages
  - **Rationale**: It is free, integrates seamlessly with GitHub repositories, and has a straightforward CI/CD setup using GitHub Actions.
  - **Alternatives Considered**: Vercel, Netlify. GitHub Pages is sufficient for this project and keeps everything within the GitHub ecosystem.
