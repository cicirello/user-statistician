# Quickstart

This directory contains several ready-to-use workflows for a few
of the more common anticipated settings. The idea is to make it
as easy as possible for you to try out the action. You can start
with one of these and then customize to your liking.

## How to Use

To use one of these workflows, do the following:
1. In your GitHub profile repository (repository with 
  same name as your username), create a directory `.github/workflows`
  if you don't already have this.
2. Pick one of the provided workflows (see the [list](#workflow-list) below).
3. Download your chosen workflow and commit it to your `.github/workflows`
  directory within your profile repository.
4. The workflow will run on a schedule, but you might want to run it once
  manually, so that you can verify it is set up correctly. To do this,
  navigate to the `Actions` tab for your profile repository. Select the
  workflow from the list of workflows on the left. You'll notice that
  it indicates: "This workflow has a workflow_dispatch event trigger."
  To the right of that click the "Run workflow" button to run the workflow
  manually.
5. Now that you've run the workflow, you'll find the SVG in the images
  directory (which the action creates if it doesn't already exist).
6. Add a link to it in the `README.md` in your profile repository. If you 
  used one of these workflows as is, without using the inputs to change
  the file name of the image, then you can add the image to your profile 
  with the following Markdown:

```markdown
![My user statistics](images/userstats.svg)
```

Although not required, it is appreciated if you instead link the image to this repository
so that others know how you generated it, with the following markdown:

```markdown
[![My user statistics](images/userstats.svg)](https://github.com/cicirello/user-statistician)
```

## Workflow List