<!-- markdownlint-disable MD024 -->
# Contribution Guidelines

Thanks for your interest in contributing to our project. This page will give you a quick overview of how things are organized and, most importantly, how to get involved. Everyone is welcome to contribute, and we value everybody's contribution.

## Table of contents

- [Contribution Guidelines](#contribution-guidelines)
  - [Table of contents](#table-of-contents)
  - [Add a project](#add-a-project)
  - [Update a project](#update-a-project)
  - [Report a mistake](#report-a-mistake)
  - [Report or remove a project](#report-or-remove-a-project)
  - [Project properties](#project-properties)
  - [Improve metadata collection](#improve-metadata-collection)
  - [Improve markdown generation](#improve-markdown-generation)
  - [Create your own best-of list](#create-your-own-best-of-list)
  - [Code of Conduct](#code-of-conduct)

## Add a project

If you like to suggest or add a project or resource, choose one of the following ways:

- Suggest a project by opening an issue: Please use the "📦 Add Project" template from the [issue page](https://github.com/awesome-obsidian/awesome-obsidian/issues/new/choose) and fill in the requested information.
- Add a project by modifying the [projects.yaml](https://github.com/awesome-obsidian/awesome-obsidian/blob/main/projects.yaml) and submitting a pull request with your addition. This can also be done directly via the [Github UI](https://github.com/awesome-obsidian/awesome-obsidian/edit/main/projects.yaml).

Before opening an issue or pull request, please ensure that you adhere to the following guidelines:

- Please make sure that the project was not already added or suggested to this best-of list. You can ensure this by searching the projects.yaml, the Readme, and the issue list.
- ⚠️ **Plugins and Themes are not yet accepted.** These categories are currently a work in progress — please use the official [Obsidian Community](https://community.obsidian.md/) in the meantime.
- Add the project to the `projects.yaml` and never to the `README.md` file directly. Use the yaml format and the properties documented in the [project properties](#project-properties) section below to add a new project.

  For a GitHub project:
    ```yaml
    - name: Quartz
      github_id: jackyzha0/quartz
      category: ssg
      docs_url: https://quartz.jzhao.xyz/
    ```

  For a resource without a GitHub repository (e.g. an article, guide, or methodology):
    ```yaml
    - name: Zettelkasten
      homepage: https://zettelkasten.de/overview/
      description: "A method for developing interconnected notes and ideas through atomic notes, links, and a networked system of knowledge."
      category: workflows
      resource: true
    ```
- Please create an individual issue or pull request for each project.
- Please use the following title format for the issue or pull request: `Add project: project-name`.
- If a project doesn't fit into any of the pre-existing categories, it should go under the `Others` category by not assigning any category. You can also suggest a new category via the "🏷️ Add or Update a Category" template on the [issue page](https://github.com/awesome-obsidian/awesome-obsidian/issues/new/choose).

## Update a project

If you like to suggest or contribute a project update, choose one of the following ways:

- Suggest a project update by opening an issue: Please use the "✏️ Update Project" template from the [issue page](https://github.com/awesome-obsidian/awesome-obsidian/issues/new/choose) and fill in the requested information.
- Update a project by modifying the [projects.yaml](https://github.com/awesome-obsidian/awesome-obsidian/blob/main/projects.yaml) and submitting a pull request with your changes. This can also be done directly via the [Github UI](https://github.com/awesome-obsidian/awesome-obsidian/edit/main/projects.yaml).

Before opening an issue or pull request, please ensure that you adhere to the following guidelines:

- Only update the project in the `projects.yaml` and never in the `README.md` file directly. Use the yaml format and the properties documented in the [project properties](#project-properties) section below to update a project.
- Please create an individual issue or pull request for each project.
- Please use the following title format for the issue or pull request: `Update project: project-name`.

## Report a mistake

Found a typo, a wrong license, a broken link, or any other error in the list?

- Please use the "🚩 Report a Mistake" template from the [issue page](https://github.com/awesome-obsidian/awesome-obsidian/issues/new/choose), or fix it directly via a pull request.

## Report or remove a project

If a listed project is inactive, archived, broken, or otherwise shouldn't be part of the list anymore, or if you are a maintainer of a listed project and want it removed:

- Please use the "🔍 Report a Project" template from the [issue page](https://github.com/awesome-obsidian/awesome-obsidian/issues/new/choose) and describe the reason for removal.

## Project properties

<table>
    <tr>
        <th>Property</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>name</code></td>
        <td>Name of the project. This name is required to be unique on the best-of list.</td>
    </tr>
    <tr>
        <td><code>github_id</code></td>
        <td>Github ID of the project based on user or organization and the repository name, e.g. <code>jackyzha0/quartz</code>. Required unless the entry is a <code>resource</code> without a GitHub repository.</td>
    </tr>
    <tr>
        <td colspan="2"><b>Optional Properties:</b></td>
    </tr>
    <tr>
        <td><code>category</code></td>
        <td>Category that this project is most related to. You can find all available category IDs in the <code>projects.yaml</code> file. Note that <code>plugins</code> and <code>themes</code> are not yet accepted. The project will be sorted into the <code>Others</code> category if no category is provided.</td>
    </tr>
    <tr>
        <td><code>homepage</code></td>
        <td>Homepage or website of the project, if different from the GitHub repository. Required for resources that don't have a <code>github_id</code>.</td>
    </tr>
    <tr>
        <td><code>docs_url</code></td>
        <td>Link to the project's documentation, if it lives at a different URL than the homepage.</td>
    </tr>
    <tr>
        <td><code>image</code></td>
        <td>URL to a logo, banner, or screenshot to display in the list.</td>
    </tr>
    <tr>
        <td><code>description</code></td>
        <td>A short, neutral 1–2 sentence description. Mainly needed for resources without a <code>github_id</code>, since GitHub project descriptions are usually pulled automatically.</td>
    </tr>
    <tr>
        <td><code>license</code></td>
        <td>License of the project, e.g. <code>MIT</code> or <code>GPL-3.0</code>. Mainly needed for resources without a github_id, since a GitHub projects license is usually pulled automatically.</td>
    </tr>
    <tr>
        <td><code>labels</code></td>
        <td>List of labels that this project is related to, e.g. <code>[official]</code>. You can find all available label IDs in the <code>projects.yaml</code> file.</td>
    </tr>
    <tr>
        <td><code>resource</code></td>
        <td>Set to <code>true</code> for entries that are not a GitHub project — e.g. an article, guide, or methodology — and are identified by <code>homepage</code> instead of <code>github_id</code>.</td>
    </tr>
</table>

Please refer to the [best-of-generator documentation](https://github.com/best-of-lists/best-of-generator#project-properties) for a complete and up-to-date list of supported project properties.

## Improve metadata collection

If you like to contribute to or share suggestions regarding the project metadata collection, please refer to the [best-of-generator](https://github.com/best-of-lists/best-of-generator) repository.

## Improve markdown generation

If you like to contribute to or share suggestions regarding the markdown generation, please refer to the [best-of-generator](https://github.com/best-of-lists/best-of-generator) repository.

## Create your own best-of list

If you want to create your own best-of list, we strongly recommend to follow [this guide](https://github.com/best-of-lists/best-of/blob/main/create-best-of-list.md). With this guide, it will only take about 3 minutes to get you started. It is already set-up to automatically run the best-of generator via our Github Action and includes other useful template files.

## Code of Conduct

All members of the project community must abide by the [Contributor Covenant, version 3.0](./.github/CODE_OF_CONDUCT.md). Only by respecting each other we can develop a productive, collaborative community. Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting a project maintainer.