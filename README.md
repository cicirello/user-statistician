# user-statistician

## About

[![build](https://github.com/cicirello/user-statistician/actions/workflows/build.yml/badge.svg)](https://github.com/cicirello/user-statistician/actions/workflows/build.yml)

The [cicirello/user-statistician](https://github.com/cicirello/user-statistician) GitHub 
Action generates a visual summary of your activity on GitHub. The intended use-case is
to generate an image that you can display on your [GitHub Profile README](https://docs.github.com/en/github/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme) 
summarizing your activity on GitHub. This includes statistics for the repositories that
you own as well as your contribution statistics (e.g., commits, issues, PRs, etc). If you
don't already have a GitHub Profile README, start by creating a public repository
with a name identical to your user name, and everything you include in the `README.md` of
that repository will show up on your GitHub Profile.

The `user-statistician` action runs entirely here on GitHub. It uses the 
[GitHub GraphQL API](https://docs.github.com/en/graphql) to collect all of the
data. For details of how GitHub counts contributions, see 
[GitHub's documentation](https://docs.github.com/en/github/setting-up-and-managing-your-github-profile/managing-contribution-graphs-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile).
The repository and contribution data included is all public. This is true even
of the "Private Contributions" entry on the stats image, as the data needed
for that should only be returned from the query executed by the action if you have
already opted in to inclusion of private contributions via GitHub's profile settings. 
You can also disable the "Private Contributions" entry as well (see the 
[inputs section](#section)). It will also auto-hide if the count is 0, as will
any other statistics with a count of 0.

To use the `user-statistician` action, you just need to set up a workflow in your
profile repository (or technically any repository that you own) on a schedule (daily
should be sufficient), and then add a link to the image. The action handles committing
and pushing the generated image to the repository (provided you use it on a branch without
required reviews and without required checks---running on a protected branch 
is otherwise fine).

## Design

### Samples

### The Stats



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

### `hide-keys`

The action automatically hides any statistics with a value of 0. For example,
if you have no pull requests, the action automatically will hide the pull requests
entry from the image rather than listing it as 0. Otherwise, all supported statistics
are shown by default. If you wish to hide any regardless of whether it has a value of 0, 
then just pass a list of the "keys"
corresponding to those you want to hide. The list can be either space or comma separated.
If you want to hide an entire group, including the relevant column headings, then 
list all of the keys for the elements
of that group. For example, `hide-keys: followers following private` will hide
both The "Followers" and "Following" counts from the "General User Stats" section,
and thus will also eliminate the column headings for that entire section, and this will
also hide the "Private Contributions" item from the "Contributions" section.

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

### `locale`

This input is an ISO 639-1, two character language code for the
language used in names of statistics, section and column headings,
and default title on the user stats card. The default is `locale: en`,
which is English. At the present time, this is the only supported 
locale, but we anticipate introducing support for additional languages.
If an unsupported locale is passed, then the action will use the
default of "en".

If you are interested in contributing a new locale, only the 
[src/StatLabels.py](src/StatLabels.py) file must be updated.

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

The action has only the following action output variable.

### `exit-code`

If the input `fail-on-error` is set to `false`, then in addition to
quietly failing (i.e., not failing the workflow run), the output `exit-code`
will be set to a non-zero exit code that may be useful in debugging the
issue. If the input `fail-on-error` is set to `true` (the default), your
workflow run won't have the opportunity to check the `exit-code` output.
However, the `exit-code` and a descriptive error message will still be
logged in the workflow output. In either case, if you believe that the
failure is a bug, please include this in any bug reports.

