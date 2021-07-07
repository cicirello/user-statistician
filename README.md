# user-statistician

## About

[![build](https://github.com/cicirello/user-statistician/actions/workflows/build.yml/badge.svg)](https://github.com/cicirello/user-statistician/actions/workflows/build.yml)



## Inputs

All inputs include default values, and are thus optional provided the 
defaults are relevant to your use-case.

### `image-file`

The `image-file` input is the name of the file (including path relative to the 
root of the repository) for the user statistics image that is generated
by the action. It defaults to `image-file: images/userstats.svg`. The action
will create any directories that don't already exist, as necessary. The image is
an svg.

### `include-title`

The `include-title` controls whether or not the user statistics card 
includes a title. It defaults to `true`. If you'd rather not have a 
title in the image, then just pass `include-title: false` (actually, anything
other than `true`, case insensitive, will be treated as `false`).

### `custom-title`

If you include a title in the user statistics image, the default 
title is of the form "Your Name's Statistics", where "Your Name" is the name 
of the owner of the repository that is using the action.

You can customize the title using the `custom-title` input. For example,
`custom-title: Hello GitHub` will set the title accordingly. Be aware that
the image width is fixed, and is not resized based on title length. Note that
if you pass a custom title with the `custom-title` input and also pass
`include-title: false`, then the conflicting input values will be resolved in
favor of the `include-title: false`.

### `colors`

The `colors` input enables you to either select from a set of
built-in color themes, or to define your own set of custom colors.
At the present time, there are three built-in themes: `light`, `dark`, and
`dark-dimmed` that are based on GitHub's color palette and themes of the
same names. If you want to know the specific colors used in each of these,
see the source in [src/Colors.py](src/Colors.py). Also see the [samples](#samples)
section of this readme.

The default is `colors: light`. You can change to a different color theme
by just passing its name (e.g., `colors: dark`).

If you have a specific set of colors that you'd like to instead use, you
can pass a list of colors (space or comma separated). The list should include
at least 4 colors in the following order: background color, border color, 
icon color, title color, and (optionally) text color. If only 4 colors are specified,
then all text will use the title color. If you pass more than 5 colors, the extras
are ignored. If you pass less than 4 colors, then the default `light` theme will
be used.  Here is an example: `colors: '#f6f8fa #c8e1ff #0366d6 #24292e #586069'`.
This example happens to be the `light` theme. Because `#` has special meaning to 
YAML (it is used for comments), you must either put quotes around the input value 
as shown in this example, or you can escape each `#` individually. The colors in this 
list can be specified either with hex (as in the example above), or with any 
named colors that are recognized by SVG, or some combination of the two. Here is an 
example with named colors: `colors: black yellow green white white`. Notice that you 
don't need quotes around the input if none of the colors are specified by hex.

__The action does not do any validation of the colors that you pass.__ If you pass
invalid color names or invalid hex color values, then the image generated will be
incorrect. The color values that you specify are inserted verbatim into the appropriate
places within the SVG.

### `exclude`

The action automatically excludes any statistics with a value of 0. For example,
if you have no pull requests, the action automatically will exclude the pull requests
entry from the image rather than listing it as 0. Otherwise, all supported statistics
are included by default. If you wish to exclude any, then just pass a list of the "keys"
corresponding to those you want to exclude. The list can be either space or comma separated.
If you want to exclude an entire group, including the relevant column headings, then 
list all of the keys for the elements
of that group. For example, `exclude: followers following private` will exclude
both The "Followers" and "Following" counts from the "General User Stats" section,
and thus will also eliminate the column headings for that section, and this will
also exclude the "Private Contributions" item from the "Contributions" section.

The keys are case sensitive, and include the following:

| Key | Statistic |
| --- | --- |
| `followers` | Followers |
| `following` | Following |
| `public` | Repositories Owned |
| `starredBy` | Starred By |
| `forkedBy` | Forked By  |
| `watchedBy` | Watched By |
| `archived` | Archived |
| `commits` | Commits |
| `issues` | Issues |
| `prs` | Pull Requests |
| `reviews` | Pull Request Reviews |
| `contribTo` | Contributed To |
| `private` | Private Contributions |

### `fail-on-error`

This input enables you to control what happens if the
action fails for some reason (e.g., error communicating
with the GitHub GraphQL API, etc). Note that in all of
our testing so far, this has not happened yet. But as software
developers, we all know that anything that can go wrong, will
go wrong eventually.

The default is `fail-on-error: true`, which means that if
an error occurs it will cause the workflow to fail. The rationale
for this default is that the failed workflow will lead to a
GitHub notification so that you know something went wrong.
If you'd rather just let it quietly fail, to most likely correct
itself during the next run, then pass `fail-on-error: false`
(actually anything other than `true` will be treated as `false`).

### `commit-and-push`

## Outputs



## Files in This Template

### README.md

Obviously, update this to reflect your GitHub Action.

### LICENSE

Choose your license.  This template is licensed under the MIT license,
so that is what the LICENSE file indicates. If you use this template,
either keep the MIT license or update to something compatible.

### CHANGELOG.md

It is a good idea to keep a changelog, so we've provided a template
of a changelog within this template repository.

### dockerignore

The `.dockerignore` is set up as a whitelist, initially 
allowing only the `Dockerfile` and the `entrypoint.py`.
If you rename `entrypoint.py`, be sure to edit 
the `.dockerignore` (or likewise, if your GitHub Action
needs any additional files while running).

### gitignore

The `.gitignore` includes Python related things you likely
won't want to store in git (update as appropriate).

### Dockerfile

The `Dockerfile` in this template pulls an image that
includes Python, and then sets the entrypoint to `entrypoint.py`.
If you rename `entrypoint.py` (or need additional files) then
don't forget to edit the `Dockerfile`.

Additionally, you will need to decide which docker image to start
with. There are two that I commonly use that I also maintain,
both of which can be pulled from either Docker Hub or the Github Container
Registry. Uncomment/comment as appropriate in the Dockerfile
as desired. Or if you'd rather not pull one of my images, you can 
see the source repository for the details.  Here are the options
found in the Dockerfile comments:
* An image with Alpine Linux and Python only to keep image small for fast loading: `FROM cicirello/pyaction-lite:latest`
* An image with Alpine Linux, Python, and git, which is also relatively small: `FROM cicirello/pyaction:latest`
* To pull from the Github Container Registry instead of Docker Hub: `FROM ghcr.io/cicirello/pyaction-lite:latest` (and likewise for the other image).

The source repositories for these images:
* https://github.com/cicirello/pyaction-lite
* https://github.com/cicirello/pyaction

### action.yml

Edit the `action.yml` file to define your action's inputs and outputs
(see examples in the file).

### entrypoint.py

You can rename this Python file to whatever you want, provided you change
its name in all other files above that reference it.  The template version
includes examples of accessing Action inputs and producing outputs.  Make
sure it is executable (the one in the template is already executable). If
you simply rename the file, it should keep the executable bit set. However,
if you delete it and replace it with a new file, you'll need to set it
executable.

### tests/tests.py

Python unit test cases could go here.

### tests/integration.py

Ideally, after unit testing the Python functions, methods, 
etc (see above), you should also test the action itself.
This involves running the action locally in a workflow
within the action's own repository. If the action generates
any files, or alters any files, then you can add a step
to run the tests in `tests/integration.py` to validate the
action's output. Although you don't necessarily need to do
this with Python, it may be convenient since Python would
already be configured in your workflow. 

### .github/dependabot.yml

The template repository enables GitHub's dependabot for keeping dependencies up to date
(it generates pull requests when new versions are found).  The template file
enables dependabot for Docker (since we're using Docker for the GitHub Action),
and GitHub Actions to keep any workflow dependencies up to date.

### .github/workflows/build.yml

This workflow runs on pushes and pull requests against the main branch. It
executes all Python unit tests (see tests/tests.py section above). It verifies that
the docker image for the GitHub Action builds. It then executes the GitHub Action
locally against the action's own repository, as an integration test. Finally, it 
executes the tests in `tests/integration.py` (see earlier section) to validate
any files created or edited by the integration test. You might also add a step
to the workflow to test that outputs are correct as well. 

### .github/workflows/major-release-num.yml

This workflow maintains a major release tag (e.g., v1 if current release 
is v1.x.y). It runs on each release and either creates the tag (if this is the
first release of a new major release number) or moves it if this is a minor
or patch level release. __IMPORTANT: You must edit this with your name, etc in
the commit and push step.__
