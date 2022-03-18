# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2022-03-18

### Added

### Changed
* Bumped base Docker image cicirello/pyaction from 4.2.0 to 4.3.0.

### Deprecated

### Removed

### Fixed


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
