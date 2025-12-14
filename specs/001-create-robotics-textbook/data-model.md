# Data Model: Create Robotics Textbook

This document defines the key content entities for the textbook.

- **Book**
  - **Description**: The top-level container for all content.
  - **Attributes**:
    - `title`: The main title of the book.
    - `introduction`: The introductory content.
  - **Relationships**: Has many Modules.

- **Module**
  - **Description**: A collection of chapters representing a major topic area (e.g., "ROS 2 Fundamentals").
  - **Attributes**:
    - `title`: The title of the module.
    - `learningObjectives`: A list of what the reader will learn.
  - **Relationships**: Belongs to a Book, Has many Chapters.

- **Chapter**
  - **Description**: A single page of content within a module.
  - **Attributes**:
    - `title`: The title of the chapter.
    - `content`: The main body of the chapter in MDX format.
  - **Relationships**: Belongs to a Module.

- **Content Block** (within Chapter)
  - **Description**: Represents various types of content within a chapter's MDX file.
  - **Types**:
    - **Code Snippet**: A formatted block of code. Can have tabs for different languages (Python, C++).
    - **Diagram**: An image or a Mermaid diagram.
    - **Exercise**: A practical task for the user.
    - **Admonition**: A note, tip, or warning.
