# python-github-action-template
A template repository for GitHub Actions implemented in Python.

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
