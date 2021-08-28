# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2021-08-28

### Added
* Italian locale
  
### Changed

### Deprecated

### Removed

### Fixed
* Missing UTF-8 encoding


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