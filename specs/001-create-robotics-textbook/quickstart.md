# Quickstart: Robotics Textbook Development

This guide explains how to set up the local development environment for the textbook.

## Prerequisites

- Node.js (v18 or later)
- npm or yarn

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    # or
    yarn install
    ```

3.  **Start the development server**:
    ```bash
    npm run start
    # or
    yarn start
    ```
    This will open a browser window with the Docusaurus site running at `http://localhost:3000`. The site will automatically reload when you make changes to the source files.

## Content Development

-   **Add a new chapter**: Create a new `.mdx` file inside the appropriate module folder in `/docs`.
-   **Add images**: Place images in the `/static/img` directory and reference them using a relative path.
-   **Add custom components**: Create new React components in `/src/components` and import them into your MDX files.
