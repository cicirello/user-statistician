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
    repositories(first: 10, after: $endCursor, ownerAffiliations: OWNER) {
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
        '_pastYearData',
        '_contributionYears',
        '_followers',
        '_issues',
        '_pullRequests',
        '_repositoriesContributedTo',
        '_watchingMyOwn',
        '_ownedRepositories',
        '_stargazers',
        '_forksOfMyRepos',
        '_watchers',
        '_publicNonForksCount',
        '_privateCount',
        '_archivedCount',
        '_forkCount'
        ]

    def __init__(self) :
        self.parseStats(
            self.executeQuery(basicStatsQuery),
            self.executeQuery(additionalRepoStatsQuery, True)
            )
        #self.parsePriorYearStats(self.executeQuery(self.createPriorYearStatsQuery(self._contributionYears)))

    def parseStats(self, basicStats, repoStats) :
        # Extract most recent year data from query results
        self._pastYearData = basicStats["data"]["user"]["contributionsCollection"]

        # Extract repositories contributes to (pwned by others) in past year
        self._pastYearData["repositoriesContributedTo"] = basicStats["data"]["user"]["repositoriesContributedTo"]["totalCount"]

        # Extract list of contribution years
        self._contributionYears = self._pastYearData["contributionYears"]
        # Just reoganizing data for clarity
        del self._pastYearData["contributionYears"]

        # Extract followed count
        self._followers = basicStats["data"]["user"]["followers"]["totalCount"]

        # Extract all time counts of issues and pull requests
        self._issues = basicStats["data"]["user"]["issues"]["totalCount"]
        self._pullRequests = basicStats["data"]["user"]["pullRequests"]["totalCount"]
        
        # Reorganize for simplicity
        repoStats = list(map(lambda x : x["data"]["user"]["repositories"], repoStats))

        # Initialize this with count of all repos contributed to, and later subtract owned repos
        self._repositoriesContributedTo = basicStats["data"]["user"]["topRepositories"]["totalCount"]
        # This is the count of owned repos, including all public, but may or may not include all private.
        # These, however, are all included in topRepositories.
        self._ownedRepositories = repoStats[0]["totalCount"]
        # Compute num contributed to (other people's repos) by reducing all repos contributed to by count of owned
        self._repositoriesContributedTo -= self._ownedRepositories

        # Count stargazers, forks of my repos, and watchers excluding me
        self._stargazers = sum(repo["stargazerCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
        self._forksOfMyRepos = sum(repo["forkCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])

        # Number of owned repos that user is watching to remove later from watchers count
        self._watchingMyOwn = basicStats["data"]["user"]["watching"]["totalCount"]
        self._watchers = sum(repo["watchers"]["totalCount"] for page in repoStats for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
        self._watchers -= self._watchingMyOwn

        # Count of private repos (which is not accurate since depends on token used to authenticate query
        self._privateCount = sum(1 for page in repoStats for repo in page["nodes"] if repo["isPrivate"])

        # Counts of archived repos and num repos that are forks of others
        self._archivedCount = sum(1 for page in repoStats for repo in page["nodes"] if repo["isArchived"])
        self._forkCount = sum(1 for page in repoStats for repo in page["nodes"] if repo["isFork"])

        # Count of public non forks owned by user
        self._publicNonForksCount = self._ownedRepositories - sum(1 for page in repoStats for repo in page["nodes"] if repo["isPrivate"] or repo["isFork"])
 

    def isResultsValid(self, queryResult) :
        pass

    
    
    

    def createPriorYearStatsQuery(self, yearList) :
        query = "query($owner: String!) {\n  user(login: $owner) {"
        for y in yearList :
            query += oneYearContribTemplate.format(y)
        query += "\n  }\n}\n"
        return query
    
    def parsePriorYearStats(self, queryResults) :
        result = json.loads(queryResults)
        if "data" in result :
            result = result["data"]["user"]
            print(result)
        else :
            pass # FOR NOW
            # ERROR: do something here for an error

    def executeQuery(self, query, needsPagination=False) :
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
        # PUT IN SOME ERROR CHECKING HERE
        if needsPagination :
            numPages = result.count('{"data"')
            if (numPages > 1) :
                result = result.replace('}{"data"', '},{"data"')
            result = "[" + result + "]"
        return json.loads(result)
    

if __name__ == "__main__" :
    # Rename these variables to something meaningful
    input1 = sys.argv[1]
    input2 = sys.argv[2]

    stats = Statistician()
    print("Prior Year", stats._pastYearData)
    print("Contrib Years", stats._contributionYears)
    print("Followers", stats._followers)
    print("Issues", stats._issues)
    print("PRs", stats._pullRequests)
    print("Contributed To", stats._repositoriesContributedTo)
    print("Watching My Own", stats._watchingMyOwn)
    print("Owns", stats._ownedRepositories)
    print("Starred by", stats._stargazers)
    print("Forked by", stats._forksOfMyRepos)
    print("Watched by", stats._watchers)
    print("Public non-forks", stats._publicNonForksCount)
    print("Private repos", stats._privateCount)
    print("Archived repos", stats._archivedCount)
    print("Forks of others repos", stats._forkCount)

    # Fake example outputs
    output1 = "Hello"
    output2 = "World"

    # This is how you produce outputs.
    # Make sure corresponds to output variable names in action.yml
    print("::set-output name=output-one::" + output1)
    print("::set-output name=output-two::" + output2)
