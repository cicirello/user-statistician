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
year{0}: contributionsCollection(from: "{0}-01-01T00:00:00.001Z") {
  totalCommitContributions 
  totalPullRequestReviewContributions
  restrictedContributionsCount 
}
"""

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
        self._stargazers = 0
        self._forksOfMyRepos = 0
        self._watchers = 0
        self._privateCount = 0
        self._archivedCount = 0
        self._forkCount = 0
        self.parseBasicUserStats(self.executeQuery(basicStatsQuery))
        self.parseAdditionalRepoStats(self.executeQuery(additionalRepoStatsQuery, True))
        self.parsePriorYearStats(self.createPriorYearStatsQuery(self._contributionYears))

    def parseBasicUserStats(self, queryResults) :
        result = json.loads(queryResults)
        if "data" in result :
            self._pastYearData = result["data"]["user"]["contributionsCollection"]
            self._contributionYears = self._pastYearData["contributionYears"]
            del self._pastYearData["contributionYears"]
            self._followers = result["data"]["user"]["followers"]["totalCount"]
            self._issues = result["data"]["user"]["issues"]["totalCount"]
            self._pullRequests = result["data"]["user"]["pullRequests"]["totalCount"]
            self._pastYearData["repositoriesContributedTo"] = result["data"]["user"]["repositoriesContributedTo"]["totalCount"]
            # Initialize this with count of all repos contributed to, and later subtract owned repos
            self._repositoriesContributedTo = result["data"]["user"]["topRepositories"]["totalCount"]
            # Number of owned repos that user is watching to remove later from watchers count
            self._watchingMyOwn = result["data"]["user"]["watching"]["totalCount"]
        else :
            pass # FOR NOW
            # ERROR: do something here for an error

    def parseAdditionalRepoStats(self, queryResults) :
        result = queryResults
        numPages = result.count('{"data"')
        if numPages >= 1 :
            if (numPages > 1) :
                result = result.replace('}{"data"', '},{"data"')
            result = "[" + result + "]"
            result = json.loads(result)
            result = list(map(lambda x : x["data"]["user"]["repositories"], result))
            self._ownedRepositories = result[0]["totalCount"]
            # Compute num contributed to (other people's repos) by reducing all repos contributed to by count of owned
            self._repositoriesContributedTo -= self._ownedRepositories
            # initialize before iterating over repos
            self._publicNonForksCount = self._ownedRepositories
            for page in result :
                for repo in page["nodes"] :
                    self.processRepoStats(repo)
            self._watchers -= self._watchingMyOwn
        else :
            pass # FOR NOW
            # ERROR: do something here for an error

    def processRepoStats(self, repo) :
        if not repo["isPrivate"] :
            self._stargazers += repo["stargazerCount"]
            self._watchers += repo["watchers"]["totalCount"]
            if not repo["isFork"] :
                self._forksOfMyRepos += repo["forkCount"]
        else :
            self._privateCount += 1
        if repo["isFork"] :
            self._forkCount += 1
        if repo["isArchived"] :
            self._archivedCount += 1
        if repo["isFork"] or repo["isPrivate"]:
            self._publicNonForksCount -= 1

    def createPriorYearStatsQuery(self, yearList) :
        query = "query($owner: String!) {\n  user(login: $owner) {\n"
        for y in yearList :
            query += oneYearContribTemplate.format(y)
        query += "  }\n}\n"
        return query
    
    def parsePriorYearStats(self, queryResults) :
        print(queryResults)

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
        return result
    

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
