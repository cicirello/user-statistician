# user-statistician

## About

[![build](https://github.com/cicirello/user-statistician/actions/workflows/build.yml/badge.svg)](https://github.com/cicirello/user-statistician/actions/workflows/build.yml)

The [cicirello/user-statistician](https://github.com/cicirello/user-statistician) GitHub 
Action generates a visual summary of your activity on GitHub, suitable to display on
your [GitHub Profile README](https://docs.github.com/en/github/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme). 
Although the intended use-case is to generate an image for your GitHub Profile README,
you can also potentially link to the image from a personal website, or from anywhere else
where you'd like to share a summary of your activity on GitHub. The image that the action 
generates includes statistics for the repositories that
you own as well as your contribution statistics (e.g., commits, issues, PRs, etc). 
The user stats image can be customized, including the colors such as with one
of the built-in themes or your own set of custom colors.

The `user-statistician` action runs entirely here on GitHub. It uses the 
[GitHub GraphQL API](https://docs.github.com/en/graphql) to collect all of the
necessary data. The contribution counts are as reported by the GitHub GraphQL API.
For details of how GitHub counts contributions, see 
[GitHub's documentation](https://docs.github.com/en/github/setting-up-and-managing-your-github-profile/managing-contribution-graphs-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile).
The repository and contribution data included is all public. This is true even
of the "Private Contributions" entry on the stats image, as 
the "restrictedContributionsCount" returned from the query executed by the action 
will only be non-zero if you have opted in to sharing private contributions via 
[GitHub's profile settings](https://docs.github.com/en/github/setting-up-and-managing-your-github-profile/managing-contribution-graphs-on-your-profile/publicizing-or-hiding-your-private-contributions-on-your-profile). 
You can also disable the "Private Contributions" entry as well (see the 
[Inputs section](#inputs)) regardless of your GitHub settings. It will also auto-hide if 
the count is 0, as will any other statistics with a count of 0.

To use the `user-statistician` action, you just need to set up a workflow in your
profile repository (or technically any repository that you own) on a schedule (daily
should be sufficient), and then add a link to the image. The action handles committing
and pushing the generated image to the repository. If you
don't already have a GitHub Profile README, start by creating a public repository
with a name identical to your user name, and everything you include in the `README.md` of
that repository will show up on your GitHub Profile at the 
address: `https://github.com/USERNAME`.

The remainder of the documentation is organized into the following sections:
* [Example Workflows and Image Samples](#example-workflows-and-image-samples):
  This section includes workflows to get you started using the action, as well as
  sample images.
* [The Stats](#the-stats): a listing of all of the statistics included in the
  images that the action generates.
* [Inputs](#inputs): Documentation of all of the inputs to the action, their
  default values, and the effects they have on the behavior of the action.
* [Outputs](#outputs): Documentation of outputs of the action.
* [All Possible Action Inputs](#all-possible-action-inputs): This section provides
  a workflow that summarizes all of the action's inputs along with their default values.

## Example Workflows and Image Samples

This section provides example workflows using the action, as
well as samples of the corresponding images that they generate.

### Example 1: All default inputs

This first example uses all of the default inputs (see [Inputs](#inputs) section
for details of available inputs). Specifically, it uses the default color
theme (a light theme), and includes all available statistics in the image and
the default title. The action commits and pushes the image by default as well.

```yml
name: user-statistician

on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:

jobs:
  stats:
    runs-on: ubuntu-latest
      
    steps:
    - uses: actions/checkout@v2

    - name: Generate the user stats image
      uses: cicirello/user-statistician@v1
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

This example workflow runs on a schedule (every day at 3am) and also includes
the `workflow_dispatch` event so that you can run it manually if desired.
The `actions/checkout@v2` step is required because the action generates the stats image
for the owner of the checked out repository, and it is also for the commit and push
functionality. Additionally, the `GITHUB_TOKEN` must be passed via an environment
variable to `cicirello/user-statistician` (see 
the `GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}`) in order to be able to query 
GitHub's GraphQl API. The default permissions of the `GITHUB_TOKEN` are sufficient
for the API queries as well as (in most cases) for pushing the image to your 
repository. If you are running this in a repository with branch 
protection rules that require either reviews or checks, then see the section
below on [Protected branches with required checks](#protected-branches-with-required-checks).

Assuming that you use the default image filename and path, then you can
insert the image into your README with the following markdown:

```markdown
![My user statistics](images/userstats.svg)
```

Although not required, it is appreciated if you instead link the image to this repository
so that others know how you generated it, with the following markdown:

```markdown
[![My user statistics](images/userstats.svg)](https://github.com/cicirello/user-statistician)
```

Here is a sample of what this will produce:

[![Default input values uses light theme](https://github.com/cicirello/user-statistician/blob/samples/images/light.svg)](https://github.com/cicirello/user-statistician)

### Example 2: Dark theme without title

This example shows how to change colors to the
dark theme, as well as disabling the title.

```yml
name: user-statistician

on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:

jobs:
  stats:
    runs-on: ubuntu-latest
      
    steps:
    - uses: actions/checkout@v2

    - name: Generate the user stats image
      uses: cicirello/user-statistician@v1
      with:
        colors: dark
        include-title: false
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

Here is a sample of what this will produce:

[![Dark theme without title](https://github.com/cicirello/user-statistician/blob/samples/images/dark.svg)](https://github.com/cicirello/user-statistician)

### Example 3: Dark-dimmed theme with custom title and some hidden stats

This example shows the dark-dimmed theme, uses a custom title, and hides a
few statistics (followers, following, and private). Note by hiding both followers
and following that the action will automatically hide the header row for the
"General User Stats" section since we've hidden all of the stats from that section.

```yml
name: user-statistician

on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:

jobs:
  stats:
    runs-on: ubuntu-latest
      
    steps:
    - uses: actions/checkout@v2

    - name: Generate the user stats image
      uses: cicirello/user-statistician@v1
      with:
        colors: dark-dimmed
        custom-title: My GitHub Statistics
        hide-keys: followers, following, private
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

Here is a sample of what this will produce:

[![Dark-dimmed theme with custom title, and with private, followers, and following all hidden](https://github.com/cicirello/user-statistician/blob/samples/images/dark-dimmed.svg)](https://github.com/cicirello/user-statistician)

### Specific version vs major release

All of the above examples used the major release tag
for the `user-statistician` step 
(i.e., `uses: cicirello/user-statistician@v1`):

```yml
    - name: Generate the user stats image
      uses: cicirello/user-statistician@v1
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

The advantage to this is that you will automatically
get all non-breaking changes and bug fixes without the
need to alter your workflow. If you prefer to 
use a specific release, just use the SemVer of the
release that you wish to use, such as with the following:

```yml
    - name: Generate the user stats image
      uses: cicirello/user-statistician@v1.0.0
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

If you do use a specific release, then we recommend
configuring [GitHub's Dependabot](https://github.blog/2020-06-01-keep-all-your-packages-up-to-date-with-dependabot/)
in your repository.  Dependabot can be used to monitor dependencies,
including GitHub Actions, and generates automated pull requests to update
versions. The PRs it generates includes the text of release notes and ChangeLogs
giving you the opportunity to decide whether to upgrade the version.

### Protected branches with required checks

The default permissions of the `GITHUB_TOKEN` are sufficient for pushing
to a protected branch, provided that the branch protection hasn't been
configured with required reviews nor with required checks. If your
GitHub profile repository does have a branch protection rule with
required reviews or required checks, there are a couple solutions.

__Not Recommended:__ First, you could create a personal access token (PAT) with necessary
permissions, save it as a repository secret, and pass that to the action
instead of the `GITHUB_TOKEN`. However, we do not recommend doing so.
If anyone else has write access to the repository, then they can potentially
create additional workflows using that PAT. This is probably reasonably safe
since it is probably rare to have collaborators on ones profile repository.
However, we still do not recommend this approach, as you must have had a reason
to put the required checks in place.

__Recommended:__ The second (and recommended) approach to dealing with a 
protected branch with
required checks is to set up a dedicated branch for generating the stats image.
This is actually what we are doing in this repository to generate the samples.
Our `main` branch is protected with required checks, after all this is a development
project repository and not a profile repository. We have a separate branch, `samples`,
that is protected, but does not have any required checks. The `GITHUB_TOKEN`
is sufficient to push to this branch.

Here is how you can do something similar if your profile repository has 
required checks on its main branch. First, create a branch, perhaps called `stats`.
The special `stats` branch does not need to be kept up to date with `main`. In fact,
once you create the `stats` branch, you can delete everything from that branch (e.g.,
you'll notice that the `samples` branch of this repository only has an "images"
directory. Next, create or modify a workflow in your `main` (or default) branch 
that checks out the dedicated `stats` branch (see the modified `actions/checkout@v2` 
step) as follows:

```yml
name: user-statistician

on:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:

jobs:
  stats:
    runs-on: ubuntu-latest
      
    steps:
    - uses: actions/checkout@v2
      with:
        ref: stats   # Or whatever you named your dedicated branch

    - name: Generate the user stats image
      uses: cicirello/user-statistician@v1
      env:
        GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

Since the image is now in a different branch than your README,
you then need to modify the markdown used to insert the
image into your profile README to refer explicitly to that branch
as follows:

```markdown
![My user statistics](https://github.com/USERNAME/USERNAME/blob/BRANCHNAME/images/userstats.svg)
```

The repetition of "USERNAME" in the above example is that we are assuming this
is in your profile repository, which must be named identically to your username.

A version that links the image to this repository
so that others know how you generated it is as follows:

```markdown
[![My user statistics](https://github.com/USERNAME/USERNAME/blob/BRANCHNAME/images/userstats.svg)](https://github.com/cicirello/user-statistician)
```


## The Stats

The statistics displayed in the image is organized into categories,
and includes the following. Note that the "Key" is what you need if
you are using the `hide-keys` input (see the [Inputs](#inputs) section).

### General User Stats

| Key | Statistic | Details |
| --- | --- | ------ |
| `followers` | Followers | simple count |
| `following` | Following | simple count |

### Repositories

The Repositories category in the image includes
two columns with data summarizing information
about the non-forks that you own, as well as all repositories
that you own, including forks.  The statistics include the 
following.

| Key | Statistic | Details |
| --- | --- | ------ |
| `public` | Repositories Owned | simple count |
| `starredBy` | Starred By | simple count |
| `forkedBy` | Forked By  | simple count |
| `watchedBy` | Watched By | number watching your repositories (excluding you) |
| `archived` | Archived | number of your repositories that you have archived |

### Contributions

The Contributions category in the image includes
two columns with data summarizing information
about your contributions during the past year, as well as
totals over all years. Please note that this can be no more
accurate than what is available via GitHub's API. For example,
we have noticed that older contributions of our own seem to
be missing. Also keep in mind what GitHub specifically counts as contributions. 
For details of how GitHub counts contributions, see 
[GitHub's documentation](https://docs.github.com/en/github/setting-up-and-managing-your-github-profile/managing-contribution-graphs-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile).

The contributions statistics in the image include the following.

| Key | Statistic | Details |
| --- | --- | ------ |
| `commits` | Commits | simple count |
| `issues` | Issues | simple count |
| `prs` | Pull Requests | simple count |
| `reviews` | Pull Request Reviews | simple count |
| `contribTo` | Contributed To | number of repositories owned by others that you have contributed to |
| `private` | Private Contributions | number of private contributions if you have shared them via your GitHub settings |

Please note that GitHub's "restrictedContributionsCount" (which is your private contributions
count) doesn't distinguish the type of contributions, so we cannot simply add
these to the specific counts by type. 


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
see the source in [src/Colors.py](src/Colors.py). Also see 
the [Example Workflows and Image Samples](#example-workflows-and-image-samples)
section of this readme for a few samples.

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

See earlier in the section [The Stats](#the-stats) for the keys needed for this input.
The keys are case sensitive.

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


## All Possible Action Inputs

The workflow here shows all possible inputs, with their default
values, and also shows how to access the action's `exit-code`
output if desired.

```yml

```

## License

This GitHub action is released under the [MIT License](LICENSE.md).

