# Tasks: Create Robotics Textbook

**Input**: Design documents from `/specs/001-create-robotics-textbook/`

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Initialize Docusaurus project using `npx create-docusaurus@latest textbook-docusaurus classic`
- [ ] T002 [P] Install additional dependencies: `mermaid`
- [ ] T003 [P] Create the project structure in the repository as per `plan.md` (`/docs`, `/src/components`, `/src/css`, `/static/img`)

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T004 Configure `docusaurus.config.js`: set project title, tagline, URL, and theme configuration
- [ ] T005 [P] Configure Algolia DocSearch in `docusaurus.config.js` with placeholder credentials
- [ ] T006 [P] Configure Prism theme for code highlighting in `docusaurus.config.js`
- [ ] T007 [P] Enable Mermaid diagrams by adding `markdown: { mermaid: true }, themes: ['@docusaurus/theme-mermaid']` to `docusaurus.config.js`
- [ ] T008 [P] Create `src/css/custom.css` for custom styling
- [ ] T009 Create the directory structure for all 6 modules inside the `/docs` folder

## Phase 3: User Story 1 - Structured Learning Path (🎯 MVP)

**Goal**: Establish the complete book structure and navigation flow.
**Independent Test**: A user can click through the entire sidebar, from the introduction to the last chapter of the last module, and see empty placeholder pages for all content.

- [ ] T010 [P] [US1] Create `_category_.json` files for each of the 6 module directories to set their labels and positions in the sidebar.
- [ ] T011 [P] [US1] Create a placeholder `Introduction.mdx` file in `/docs`.
- [ ] T012 [P] [US1] Create placeholder `.mdx` files for every chapter within their respective module folders (e.g., `/docs/module-1/chapter-1.mdx`).
- [ ] T013 [US1] Configure the sidebar in `docusaurus.config.js` (or `sidebars.js`) to reflect the full module and chapter structure.

## Phase 4: User Story 2 - Practical Application (Content Creation)

**Goal**: Populate the placeholder pages with actual content.
**Independent Test**: A user can read a chapter, view the diagrams, and run the code examples.

- [ ] T014 [P] [US2] Write content for Module 1, Chapter 1: Foundation of Physical AI & Embodied Intelligence in `/docs/module-1/chapter-1.mdx`.
- [ ] T015 [P] [US2] Write content for Module 1, Chapter 2: Humanoid Robotics Landscape & Sensor System in `/docs/module-1/chapter-2.mdx`.
- [ ] T016 [P] [US2] Write content for Module 2, Chapter 1: ROS 2 Architecture & Core Concept in `/docs/module-2/chapter-1.mdx`.
- [ ] T017 [P] [US2] Write content for Module 2, Chapter 2: ROS 2 Python Package Building and Launch files in `/docs/module-2/chapter-2.mdx`.
- [ ] T018 [P] [US2] Write content for Module 2, Chapter 3: Advance ROS 2 Concept and Tools in `/docs/module-2/chapter-3.mdx`.
- [ ] T019 [P] [US2] Write content for Module 3, Chapter 1: Gazebo Setup and URDF/SDF Models in `/docs/module-3/chapter-1.mdx`.
- [ ] T020 [P] [US2] Write content for Module 3, Chapter 2: Physics, Sensor Simulation & Unity Introduction in `/docs/module-3/chapter-2.mdx`.
- [ ] T021 [P] [US2] Write content for Module 4, Chapter 1: Introduction to Isaac SDK & Isaac Sim in `/docs/module-4/chapter-1.mdx`.
- [ ] T022 [P] [US2] Write content for Module 4, Chapter 2: Perception and Manipulation in Isaac Sim in `/docs/module-4/chapter-2.mdx`.
- [ ] T023 [P] [US2] Write content for Module 4, Chapter 3: Reinforcement Learning and Sim-to-Real Transfer in `/docs/module-4/chapter-3.mdx`.
- [ ] T024 [P] [US2] Write content for Module 5, Chapter 1: Kinematics, Dynamics and Motion Planning in `/docs/module-5/chapter-1.mdx`.
- [ ] T025 [P] [US2] Write content for Module 5, Chapter 2: Bipedal Locomotion, Grasping and Human-Robot Interaction in `/docs/module-5/chapter-2.mdx`.
- [ ] T026 [P] [US2] Write content for Module 6, Chapter 1: Conversational Robotics in `/docs/module-6/chapter-1.mdx`.
- [ ] T027 [P] [US2] Write content for Module 6, Chapter 2: Capstone Project in `/docs/module-6/chapter-2.mdx`.

## Phase 5: User Story 3 - Easy Navigation and Search

**Goal**: Ensure a high-quality navigation and search experience.
**Independent Test**: A user can find a specific term using search and the results are accurate.

- [ ] T028 [US3] Apply for and configure live Algolia DocSearch credentials.
- [ ] T029 [US3] Test search functionality with key terms from each module and verify relevance of results.
- [ ] T030 [US3] Review and test sidebar navigation, ensuring all links are correct and the structure is intuitive.

## Phase N: Polish & Cross-Cutting Concerns

- [ ] T031 [P] Create and populate the "Hardware Requirements" page in `/docs/hardware.mdx`.
- [ ] T032 [P] Create and populate the "Prerequisites and Setup Instructions" page in `/docs/setup.mdx`.
- [ ] T033 [P] Create and populate the "Glossary" page in `/docs/glossary.mdx`.
- [ ] T034 [P] Create and populate the "Additional Resources" page in `/docs/resources.mdx`.
- [ ] T035 [P] Perform a full review of all content for clarity, consistency, and correctness.
- [ ] T036 [P] Conduct an accessibility review (WCAG 2.1 AA) of the site.
- [ ] T037 Create a GitHub Actions workflow in `.github/workflows/deploy.yml` to build and deploy the site to GitHub Pages.

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed first.
- **Phase 2 (Foundational)** depends on Phase 1.
- **Phase 3 (US1 - MVP)** depends on Phase 2. This phase delivers the core testable structure.
- **Phase 4 (US2 - Content)** can begin after Phase 3. Tasks within this phase are highly parallelizable.
- **Phase 5 (US3 - Navigation)** can be done in parallel with Phase 4.
- **Phase N (Polish)** should be done last, before final release.
