# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2024-09-27

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Dependencies
* Bump cicirello/pyaction from 4.29.0 to 4.32.0

### CI/CD

### Other


## [1.23.0] - 2024-05-13

### Added
* An action input, `commit-message`, to enable customizing the commit message

### Dependencies
* Bump cicirello/pyaction from 4.27.0 to 4.29.0


## [1.22.1] - 2023-12-08

### Fixed
* Eliminated adjustment for watching own repositories from the "Watched By" stat for consistency with other stats that don't make such an adjustment such as the star count.

### Dependencies
* Bump cicirello/pyaction from 4.25.0 to 4.27.0


## [1.22.0] - 2023-10-18

### Added
* Translation to Armenian (`locale: hy`) in #240 (@JairTorres1003).

### Dependencies
* Bump cicirello/pyaction from 4.24.0 to 4.25.0 (which includes bumping Python to 3.12).

### CI/CD
* Bump Python to 3.12 in CI/CD workflows when running unit tests (@cicirello).


## [1.21.0] - 2023-10-04

### Added
* Translation to Tagalog (`locale: tl`) in #227 (@digracesion).
* Translation to Swedish (`locale: sv`) in #230 (@Viveksati5143).
* Translation to Persian (`locale: fa`) in #232 (@AshkanArabim).
* Translation to Malayalam (`locale: ml`) in #235 (@Sarthak027).
* Translation to Finnish (`locale: fi`) in #236 (@Sadeedpv).

### Dependencies
* Bump cicirello/pyaction from 4.22.0 to 4.24.0

### Other
* Updated the quickstart / sample workflows to the latest version of actions/checkout.


## [1.20.5] - 2023-09-07

### Fixed
* Resolved issue with failing to commit and push, a bug introduced in v1.20.3.


## [1.20.4] - 2023-09-07

### Fixed
* Refactored everything locale related to extract definitions of locales from Python dictionaries into JSON files to make it easier to contribute additional language translations.


## [1.20.3] - 2023-09-06

### Fixed
* Get repository owner (user for stats image) from GitHub Actions environment variables #210 (fixes issue related to update to GitHub CLI #209 determining owner of repository).

### Dependencies
* Bump cicirello/pyaction from 4.14.0 to 4.22.0


## [1.20.2] - 2022-12-30

### Fixed
* Better match background for GitHub-inspired themes, using GitHub's canvas.default instead of canvas.inset.


## [1.20.1] - 2022-12-30

### Fixed
* Improved Russian Translation in #203, contributed by @mrtnvgr.

### Dependencies
* Bump cicirello/pyaction from 4.12.0 to 4.14.0


## [1.20.0] - 2022-10-25

### Added
* Translation to Odia (`locale: or`) in #186, contributed by @Prasanta-Hembram.

### Fixed
* Some users may be using the action on a self-hosted runner not yet updated to a version supporting the
  new GitHub Actions `GITHUB_OUTPUT` env file. This patch adds backwards compatibility for that case by 
  falling back to the deprecated `set-output` if `GITHUB_OUTPUT` doesn't exist. #190 (@cicirello).

### Dependencies
* Bump cicirello/pyaction from 4.11.0 to 4.12.0, including upgrading Python within the Docker container to 3.11.

### CI/CD
* Bump Python to 3.11 in CI/CD workflows.


## [1.19.0] - 2022-10-20

### Added
* Translation to Santali (`locale: sat`) in #178, contributed by @Prasanta-Hembram.
* Translation to Serbian (`locale: sr`) in #182, contributed by @keen003.

### Fixed
* Replaced use of GitHub Action's deprecated `set-output` with the new `$GITHUB_OUTPUT` env file,
  in #184 (@cicirello).
  
### Dependencies
* Bump cicirello/pyaction from 4.10.0 to 4.11.0


## [1.18.0] - 2022-10-12

### Added
* Translation to Hungarian (`locale: hu`) in #172, contributed by @jpacsai.

### Dependencies
* Bump cicirello/pyaction from 4.9.0 to 4.10.0


## [1.17.0] - 2022-10-05

### Added
* Increased internationalization with the addition of new locales:
  * Dutch (`locale: nl`) in #166, contributed by @lovelacecoding.
  * Norwegian (`locale: no`) in #167, contributed by @rubjo.
  * Romanian (`locale: ro`) in #164, contributed by @donheshanthaka.
  * Thai (`locale: th`) in #165, contributed by @Slowlife01 and updated by @thititongumpun.

### Dependencies
* Bump cicirello/pyaction from 4.8.1 to 4.9.0.


## [1.16.1] - 2022-09-09

### Fixed
* Corrected minor error in language chart radius calculation that was causing too small margin around chart for users with long names.


## [1.16.0] - 2022-09-08

### Added
* New themes, including
  * halloween - A dark theme for use around Halloween
  * halloween-light - A light theme for use around Halloween
  * batty - A light theme for use around Halloween
* Additional icon options for the icon in top corners, including:
  * pumpkin
  * bat

### Dependencies
* Bump cicirello/pyaction from 4.7.1 to 4.8.1, including upgrading Python within the Docker container to 3.10.7 


## [1.15.1] - 2022-08-24

### Fixed
* Decreased the size of icon in top corners for better visual appearance.


## [1.15.0] - 2022-08-19

### Added
* Icons in upper corners surrounding the title, with the following features:
  * Theme-defined icons, initially the GitHub Octocat from Octicons for current built-in themes.
  * Input `top-icon` to enable overriding, such as disabling the icons, or setting a different one.
  * For now, `top-icon` is limited to the GitHub Octocat or nothing (additional options planned).

### Dependencies
* Bump cicirello/pyaction from 4.4.0 to 4.7.1


## [1.14.0] - 2022-06-08

### Changed
* Centered title.
* Bumped base docker image cicirello/pyaction from 4.3.1 to 4.4.0.

### Fixed
* Minor label edit.


## [1.13.0] - 2022-05-02

### Added
* New themes added to correspond to all of GitHub's themes, including:
  * dark-high-contrast
  * light-high-contrast
  * dark-colorblind
  * light-colorblind
  * dark-tritanopia
  * light-tritanopia

### Changed
* Bumped base Docker image cicirello/pyaction from 4.2.0 to 4.3.1.

### Fixed
* Fixed margin calculation when most starred, most forked, or featured repo has long name.
* Adjusted existing themes (dark, light, dark-dimmed) based on newer versions of corresponding GitHub themes.


## [1.12.3] - 2022-02-22

### Changed
* Switched to specific release of base Docker image to avoid accidental breaking changes
  in base Docker image.

### Fixed
* Total count of repositories (other than own) contributed to will now show as
  a blank spot on the SVG. Previously reported values were highly inaccurate, and
  cannot be computed accurately at the present time due to unavailability of
  necessary data from the GitHub GraphQL API.
  

## [1.12.2] - 2022-02-18

### Fixed
* Suppressed Python's pycache on imports (fixes Issue #107).


## [1.12.1] - 2022-02-17

### Changed
* Refactored text length calculation.


## [1.12.0] - 2021-11-04

### Added
* Increased internationalization support with the addition of new locales:
  * Ukrainian (`locale: uk`) via [PR#102](https://github.com/cicirello/user-statistician/pull/102).

### Fixed
* Added missing `lang` and `xml:lang` attributes to the opening svg tag to report the
  language of the content of the SVG to provide better support for visually impaired
  users who use a screen reader.


## [1.11.0] - 2021-10-13

### Added
* Increased internationalization support with the addition of new locales:
  * Lithuanian (`locale: lt`) via [PR#98](https://github.com/cicirello/user-statistician/pull/98).
  * Japanese (`locale: ja`) via [PR#89](https://github.com/cicirello/user-statistician/pull/89).
  * Turkish (`locale: tr`) via [PR#90](https://github.com/cicirello/user-statistician/pull/90).
  

## [1.10.0] - 2021-10-06

### Added
* Increased internationalization support with the addition of new locales:
  * Korean (`locale: ko`) via [PR#93](https://github.com/cicirello/user-statistician/pull/93).

### Fixed
* The total column for the number of repositories (owned by someone else) that the user has
  contributed to, at the present time, cannot be computed exactly due to limitations in the
  GitHub API. The relevant queries seem to exclude older contribTo data. To account for this,
  that value is now listed as a lower bound (e.g., instead of a number like 7, it is listed
  as &geq;7). This is the only stat affected by this.
  

## [1.9.0] - 2021-10-04

### Added
* Increased internationalization support with the addition of new locales:
  * Portuguese (`locale: pt`) via [PR#69](https://github.com/cicirello/user-statistician/pull/69).
  * Bahasa Indonesia (`locale: id`) via [PR#71](https://github.com/cicirello/user-statistician/pull/71).
  * French (`locale: fr`) via [PR#77](https://github.com/cicirello/user-statistician/pull/77).
  * Spanish (`locale: es`) via [PR#79](https://github.com/cicirello/user-statistician/pull/79).
  * Russian (`locale: ru`) via [PR#80](https://github.com/cicirello/user-statistician/pull/80).
  * Hindi (`locale: hi`) via [PR#81](https://github.com/cicirello/user-statistician/pull/81).
  * Polish (`locale: pl`) via [PR#78](https://github.com/cicirello/user-statistician/pull/78).
  * Bengali (`locale: bn`) via [PR#92](https://github.com/cicirello/user-statistician/pull/92).

### Changed
* Minor refactoring to improve code maintainability


## [1.8.1] - 2021-09-02

### Fixed
* Improved visual consistency of fonts across browsers


## [1.8.0] - 2021-08-31

### Added
* German locale: German translations of title template, headings, labels, 
  etc for locale code `de`.
  
### Changed
* Improved precision of fonts if the SVG is scaled.
* Minor adjustment to margins.


## [1.7.1] - 2021-08-30

### Fixed
* The width of the SVG is now set based on the content, including
  factoring in the effects of different locales where headings, and
  labels may be longer. Note that the `image-width` input can still
  be used to set a larger width. The action will now use the larger
  of the user-defined value of `image-width`, or the width necessary
  to accommodate the content.


## [1.7.0] - 2021-08-28

### Added
* Italian locale: Italian translations of title template, headings, labels, 
  etc for locale code `it`.
  
### Fixed
* Added missing UTF-8 encoding when writing the SVG to fix issue with
  characters needed for some language translations.
* Fixed exception in case when user stores the SVG at root of repo.
  

## [1.6.0] - 2021-08-09

### Added
* User adjustable width, via a new action input `image-width`.
  
### Changed
* Revised SVG generation to eliminate unnecessary SVG tags surrounding 
  icon paths and language chart. This is a non-functional change. The SVG 
  tags referred to here are not incorrect, but they are not needed. By changing
  SVG generation to not insert them, DOM size is decreased (possibly decreasing 
  rendering time), and file size is decreased, possibly speeding up download time.


## [1.5.0] - 2021-08-06

### Added
* A new action input, `featured-repository`, that enables the user of the action
  to (optionally) specify a repository to feature in the General Stats and Info
  section of the SVG. For example, perhaps they have a repository that they feel
  is a better representative of their work than their most starred and most forked
  repositories.
* An option to animate the language distribution chart, a continuous rotation of the
  pie chart. This feature is disabled by default. It is controlled by a pair of new inputs:
  `animated-language-chart` and `language-animation-speed`.

### Fixed
* Corrected bug in edge case when user only owns forks, which had been causing the
  action to fail with an exception.


## [1.4.0] - 2021-08-04

### Added
* Most starred repo added to General Stats and Info section of SVG.
* Most forked repo added to General Stats and Info section of SVG.

### Changed
* "General User Stats" section renamed to "General Stats and Info" to better reflect
  the addition of Most Starred and Most Forked.


## [1.3.0] - 2021-07-29

### Added
* The ability to exclude specific repositories from the language
  distribution chart, controlled by a new action input `language-repository-exclusions`,
  which is a list of repositories to exclude from the language stats.
  
### Changed
* Revised the Quickstart workflows to include pushing the workflow file to
  the events that runs the workflow to make it even easier for a user to get started.


## [1.2.0] - 2021-07-23

### Added
* The year user joined GitHub is now in General User Stats section of card.
* New action input, `category-order`, which allows user to customize the order
  of the categories of stats.
  
### Changed
* Minified SVG during generation (removed unnecessary characters like new lines,
  and a couple empty text tags). This doesn't change the contents or appearance
  of the SVG.
  

## [1.1.1] - 2021-07-22

### Fixed
* Fixed minor bug in handling of failOnError input.


## [1.1.0] - 2021-07-20

### Added
* Language Distribution section added to the card:
  * Languages section of the stats card that summarizes the distribution
    of languages for the public repositories owned by the user. This is intended
    to be the equivalent of the languages graph that GitHub generates for each
    individual repository, except for the combination of all of the user's 
    repositories. The distribution is visualized, however, with a pie chart, rather
    than the simple line chart.
  * The language distribution calculation features a user customizable number
    of languages to display. Any extra languages beyond what the user specifies
    are summarized into a single "Other" item (much like the "Other" that appears
    in GitHub's language graphs in a repository for low percentage languages).
  * By default, the language distribution auto-calibrates the number of languages
    based on the percentages. Specifically, all languages that individually account for
    less than one percent are combined into an "Other" item.
  
### Changed
* Text and title colors in built-in themes (light, dark, and dark-dimmed)
  changed slightly for accessibility (changed to ensure text and background
  have contrast ratio of at least 4.5, and title and background have contrast
  ratio of at least 4.5). Test cases will enforce this criteria on any themes
  that may be contributed in the future (but not on a user's own custom colors).
* Increased width of image slightly for better visual appearance of data portion
  with label portion (e.g., right half with data is same width as left half with
  labels).
* Changed default title template to better reflect content of the stats card.


## [1.0.2] - 2021-07-15

### Fixed
* Corrected all-time count of repositories contributed to that are owned by others.


## [1.0.1] - 2021-07-14

### Fixed
* Changed the author of commits to the github-actions bot
  to avoid artificially inflating the user of the action's
  commit count.


## [1.0.0] - 2021-07-13

### Added
* This is the initial release. The user-statistician is a GitHub 
  Action that generates a detailed visual summary of your activity 
  on GitHub in the form of an SVG, suitable to display on your GitHub 
  Profile README. It runs entirely on GitHub, and is designed to run on 
  a schedule, pushing an updated user stats SVG to your profile repo.
