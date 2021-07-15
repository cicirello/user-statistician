# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2021-07-15

### Added
  
### Changed

### Deprecated

### Removed

### Fixed


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