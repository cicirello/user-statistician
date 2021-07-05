#!/usr/bin/env python3
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
import sys
import subprocess

basicStatsQuery = """
query($owner: String!) {
  user(login: $owner) {
    contributionsCollection {
      totalCommitContributions 
      totalIssueContributions 
      totalPullRequestContributions
      totalPullRequestReviewContributions
      totalRepositoryContributions
      restrictedContributionsCount
      contributionYears
    }
    followers {
      totalCount
    }
    issues {
      totalCount
    }
    pullRequests {
      totalCount
    }
    topRepositories(orderBy: {direction: DESC, field: UPDATED_AT}) {
      totalCount
    }
    repositoriesContributedTo {
      totalCount
    }
    watching(ownerAffiliations: OWNER, privacy: PUBLIC) {
      totalCount
    }              
  }
}
"""

additionalRepoStatsQuery = """
query($owner: String!, $endCursor: String) {
  user(login: $owner) {
    repositories(first: 100, after: $endCursor, ownerAffiliations: OWNER) {
      totalCount
      nodes {
        stargazerCount 
        forkCount
        isArchived
        isFork
        isPrivate
        watchers {
          totalCount
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }              
  }
}
"""

oneYearContribTemplate = """
  year{0}: contributionsCollection(from: "{0}-01-01T00:00:00.001Z") {{
    totalCommitContributions 
    totalPullRequestReviewContributions
    restrictedContributionsCount 
  }}"""

class Statistician :

    __slots__ = [
        '_contributionYears',
        '_followers',
        '_contrib',
        '_repo'
        ]

    def __init__(self) :
        basicStatsQuery = loadQuery("/queries/basicstats.graphql")
        self.parseStats(
            self.executeQuery(basicStatsQuery),
            self.executeQuery(additionalRepoStatsQuery, True)
            )
        self.parsePriorYearStats(self.executeQuery(self.createPriorYearStatsQuery(self._contributionYears)))

    def loadQuery(self, queryFilepath, failOnError=True) :
        try :
            with open(queryFilepath, 'r') as file:
                return file.read()
        except IOError:
            print("Failed to open query file:", queryFilePath)
            exit(1 if failOnError else 0)

    def parseStats(self, basicStats, repoStats) :
        # Extract most recent year data from query results
        pastYearData = basicStats["data"]["user"]["contributionsCollection"]
        
        # Extract repositories contributes to (pwned by others) in past year
        pastYearData["repositoriesContributedTo"] = basicStats["data"]["user"]["repositoriesContributedTo"]["totalCount"]

        # Extract list of contribution years
        self._contributionYears = pastYearData["contributionYears"]
        # Just reoganizing data for clarity
        del pastYearData["contributionYears"]

        # Extract followed count
        self._followers = basicStats["data"]["user"]["followers"]["totalCount"]

        # Extract all time counts of issues and pull requests
        issues = basicStats["data"]["user"]["issues"]["totalCount"]
        pullRequests = basicStats["data"]["user"]["pullRequests"]["totalCount"]

        # Reorganize for simplicity
        repoStats = list(map(lambda x : x["data"]["user"]["repositories"], repoStats))
        
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
            "pr-reviews" : [pastYearData["totalPullRequestReviewContributions"], 0],
            "contribTo" : [pastYearData["repositoriesContributedTo"], repositoriesContributedTo],
            "private" : [pastYearData["restrictedContributionsCount"], 0]
            }

        # Count stargazers, forks of my repos, and watchers excluding me
        stargazers = sum(repo["stargazerCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
        forksOfMyRepos = sum(repo["forkCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
        stargazersAll = sum(repo["stargazerCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"])
        forksOfMyReposAll = sum(repo["forkCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"])

        # Number of owned repos that user is watching to remove later from watchers count
        watchingMyOwn = basicStats["data"]["user"]["watching"]["totalCount"]
        watchers = sum(repo["watchers"]["totalCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"])
        watchersNonForks = sum(repo["watchers"]["totalCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
        # Don't filter our watching of my own for now. See comment that follows for explanation.
        #    watchers -= watchingMyOwn
        # Note: watchers includes forks of repos because of adjustment for owners repos.
        # Need an additional query of some sort to filter our watching of owner's forks of other's repos.

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

    def createPriorYearStatsQuery(self, yearList) :
        query = "query($owner: String!) {\n  user(login: $owner) {"
        for y in yearList :
            query += oneYearContribTemplate.format(y)
        query += "\n  }\n}\n"
        return query
    
    def parsePriorYearStats(self, queryResults) :
        queryResults = queryResults["data"]["user"]
        self._contrib["commits"][1] = sum(stats["totalCommitContributions"] for k, stats in queryResults.items())
        self._contrib["pr-reviews"][1] = sum(stats["totalPullRequestReviewContributions"] for k, stats in queryResults.items())
        self._contrib["private"][1] = sum(stats["restrictedContributionsCount"] for k, stats in queryResults.items())
        
    def executeQuery(self, query, needsPagination=False, failOnError=True) :
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
            result = json.loads(result)
            if "errors" in result :
                print("GitHub api Query failed with error:")
                print(result["errors"])
            else :
                print("Something unexpected occurred during GitHub API query.")
            exit(1 if failOnError else 0)
        elif needsPagination :
            if (numPages > 1) :
                result = result.replace('}{"data"', '},{"data"')
            result = "[" + result + "]"
        return json.loads(result)
    

if __name__ == "__main__" :
    # Rename these variables to something meaningful
    input1 = sys.argv[1]
    input2 = sys.argv[2]

    stats = Statistician()
    print("Contributions", stats._contrib)
    print("Contrib Years", stats._contributionYears)
    print("Followers", stats._followers)
    print("Repos", stats._repo)
    
    # Fake example outputs
    output1 = "Hello"
    output2 = "World"

    # This is how you produce outputs.
    # Make sure corresponds to output variable names in action.yml
    print("::set-output name=output-one::" + output1)
    print("::set-output name=output-two::" + output2)
