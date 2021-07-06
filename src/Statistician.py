#
# user-statistician: Github action for generating a user stats card
# 
# Copyright (c) 2021 Vincent A Cicirello
# https://www.cicirello.org/
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import json
import subprocess

class Statistician :
    """The Statistician class executes GitHub GraphQl queries,
    and parses the query results.
    """

    __slots__ = [
        '_contributionYears',
        '_user',
        '_contrib',
        '_repo',
        '_login',
        '_name'
        ]

    def __init__(self, fail=True) :
        """The initializer executes the queries and parses the results.
        Upon completion of the intitializer, the user statistics will
        be available.

        Keyword arguments:
        fail - If True, the workflow will fail if there are errors.
        """
        self.ghDisableInteractivePrompts()
        basicStatsQuery = self.loadQuery("/queries/basicstats.graphql",
                                         fail)
        additionalRepoStatsQuery = self.loadQuery("/queries/repostats.graphql",
                                                  fail)
        oneYearContribTemplate = self.loadQuery("/queries/singleYearQueryFragment.graphql",
                                                fail)
        watchingAdjustmentQuery = self.loadQuery("/queries/watchingAdjustment.graphql",
                                                 fail)
        self.parseStats(
            self.executeQuery(basicStatsQuery,
                              failOnError=fail),
            self.executeQuery(additionalRepoStatsQuery,
                              needsPagination=True),
            self.executeQuery(watchingAdjustmentQuery,
                              needsPagination=True)
            )
        self.parsePriorYearStats(self.executeQuery(self.createPriorYearStatsQuery(self._contributionYears, oneYearContribTemplate)))

    def loadQuery(self, queryFilepath, failOnError=True) :
        """Loads a graphql query.

        Keyword arguments:
        queryFilepath - The file with path of the query.
        failOnError - If True, the workflow will fail if there is an error loading the
            query; and if False, this action will quietly exit with no error code. In
            either case, an error message will be logged to the console.
        """
        try :
            with open(queryFilepath, 'r') as file:
                return file.read()
        except IOError:
            print("Error: Failed to open query file:", queryFilePath)
            print("::set-output name=exit-code::1")
            exit(1 if failOnError else 0)

    def parseStats(self, basicStats, repoStats, watchingStats) :
        """Parses the user statistics.

        Keyword arguments:
        basicStats - The results of the basic stats query.
        repoStats - The results of the repo stats query.
        watchingStats - The results of the query of repositories the user is watching.
        """
        # Extract username (i.e., login) and fullname.
        # Name needed for title of statistics card, and username
        # needed if we support committing stats card.
        self._login = basicStats["data"]["user"]["login"]
        self._name = basicStats["data"]["user"]["name"]
        
        # Extract most recent year data from query results
        pastYearData = basicStats["data"]["user"]["contributionsCollection"]
        
        # Extract repositories contributes to (pwned by others) in past year
        pastYearData["repositoriesContributedTo"] = basicStats["data"]["user"]["repositoriesContributedTo"]["totalCount"]

        # Extract list of contribution years
        self._contributionYears = pastYearData["contributionYears"]
        # Just reoganizing data for clarity
        del pastYearData["contributionYears"]

        # Extract followed and following counts
        self._user = {}
        self._user["followers"] = [ basicStats["data"]["user"]["followers"]["totalCount"] ]
        self._user["following"] = [ basicStats["data"]["user"]["following"]["totalCount"] ]

        # Extract all time counts of issues and pull requests
        issues = basicStats["data"]["user"]["issues"]["totalCount"]
        pullRequests = basicStats["data"]["user"]["pullRequests"]["totalCount"]

        # Reorganize for simplicity
        repoStats = list(map(lambda x : x["data"]["user"]["repositories"], repoStats))
        watchingStats = list(map(lambda x : x["data"]["user"]["watching"], watchingStats))
        
        # Initialize this with count of all repos contributed to, and later subtract owned repos
        repositoriesContributedTo = basicStats["data"]["user"]["topRepositories"]["totalCount"]
        # This is the count of owned repos, including all public, but may or may not include all private.
        # These, however, are all included in topRepositories.
        ownedRepositories = repoStats[0]["totalCount"]
        # Compute num contributed to (other people's repos) by reducing all repos contributed to by count of owned
        repositoriesContributedTo -= ownedRepositories

        self._contrib = {
            "commits" : [pastYearData["totalCommitContributions"], 0],
            "issues" : [pastYearData["totalIssueContributions"], issues],
            "prs" : [pastYearData["totalPullRequestContributions"], pullRequests],
            "reviews" : [pastYearData["totalPullRequestReviewContributions"], 0],
            "contribTo" : [pastYearData["repositoriesContributedTo"], repositoriesContributedTo],
            "private" : [pastYearData["restrictedContributionsCount"], 0]
            }

        # Count stargazers, forks of my repos, and watchers excluding me
        stargazers = sum(repo["stargazerCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
        forksOfMyRepos = sum(repo["forkCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
        stargazersAll = sum(repo["stargazerCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"])
        forksOfMyReposAll = sum(repo["forkCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"])

        # Compute number of watchers excluding cases where user is watching their own repos.
        watchingMyOwnNonForks = sum(1 for page in watchingStats for repo in page["nodes"] if not repo["isFork"])
        watchers = sum(repo["watchers"]["totalCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"])
        watchers -= watchingStats[0]["totalCount"]
        watchersNonForks = sum(repo["watchers"]["totalCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
        watchersNonForks -= watchingMyOwnNonForks
        
        # Count of private repos (which is not accurate since depends on token used to authenticate query,
        # however, all those here are included in count of owned repos.
        privateCount = sum(1 for page in repoStats for repo in page["nodes"] if repo["isPrivate"])

        publicAll = ownedRepositories - privateCount

        # Counts of archived repos
        publicNonForksArchivedCount = sum(1 for page in repoStats for repo in page["nodes"] if repo["isArchived"] and not repo["isPrivate"] and not repo["isFork"])
        publicArchivedCount = sum(1 for page in repoStats for repo in page["nodes"] if repo["isArchived"] and not repo["isPrivate"])
        
        # Count of public non forks owned by user
        publicNonForksCount = ownedRepositories - sum(1 for page in repoStats for repo in page["nodes"] if repo["isPrivate"] or repo["isFork"])

        self._repo = {
            "public" : [publicNonForksCount, publicAll],
            "starredBy" : [stargazers, stargazersAll],
            "forkedBy" : [forksOfMyRepos, forksOfMyReposAll],
            "watchedBy" : [watchersNonForks, watchers],
            "archived" : [publicNonForksArchivedCount, publicArchivedCount]
            }

    def createPriorYearStatsQuery(self, yearList, oneYearContribTemplate) :
        """Generates the query for prior year stats.

        Keyword arguments:
        yearList - a list of the years when the user had contributions, obtained by one of the other queries.
        oneYearContribTemplate - a string template of the part of a query for one year
        """
        query = "query($owner: String!) {\n  user(login: $owner) {\n"
        for y in yearList :
            query += oneYearContribTemplate.format(y)
        query += "  }\n}\n"
        return query
    
    def parsePriorYearStats(self, queryResults) :
        """Parses one year of commits, PR reviews, and restricted contributions.

        Keyword arguments:
        queryResults - The results of the query.
        """
        queryResults = queryResults["data"]["user"]
        self._contrib["commits"][1] = sum(stats["totalCommitContributions"] for k, stats in queryResults.items())
        self._contrib["reviews"][1] = sum(stats["totalPullRequestReviewContributions"] for k, stats in queryResults.items())
        self._contrib["private"][1] = sum(stats["restrictedContributionsCount"] for k, stats in queryResults.items())
        
    def executeQuery(self, query, needsPagination=False, failOnError=True) :
        """Executes a GitHub GraphQl query using the GitHub CLI (gh).

        Keyword arguments:
        query - The query as a string.
        needsPagination - Pass True to enable pagination of query results.
        failOnError - If True, the workflow will fail if there is an error executing the
            query; and if False, this action will quietly exit with no error code. In
            either case, an error message will be logged to the console.
        """
        arguments = [
            'gh', 'api', 'graphql',
            '-F', 'owner={owner}',
            '--cache', '1h',
            '-f', 'query=' + query
            ]
        if needsPagination :
            arguments.insert(5, '--paginate')
        result = subprocess.run(
            arguments,
            stdout=subprocess.PIPE,
            universal_newlines=True
            ).stdout.strip()
        numPages = result.count('{"data"')
        if numPages == 0 :
            # Check if any error details
            result = json.loads(result) if len(result) > 0 else ""
            if "errors" in result :
                print("GitHub api Query failed with error:")
                print(result["errors"])
                print("::set-output name=exit-code::2")
                code = 2
            else :
                print("Something unexpected occurred during GitHub API query.")
                print("::set-output name=exit-code::3")
                code = 3
            exit(code if failOnError else 0)
        elif needsPagination :
            if (numPages > 1) :
                result = result.replace('}{"data"', '},{"data"')
            result = "[" + result + "]"
        result = json.loads(result)
        return result

    def ghDisableInteractivePrompts(self) :
        """Disable gh's interactive prompts. This is probably unnecessary,
        as all of our testing so far, the queries run fine and don't produce any
        prompts. Disabling as a precaution in case some unexpected condition occurs
        that generates a prompt, so we don't accidentally leave a workflow waiting for
        user itneraction.
        """
        result = subprocess.run(
            ["gh", "config", "set", "prompt", "disabled"],
            stdout=subprocess.PIPE,
            universal_newlines=True
            ).stdout.strip()
    
