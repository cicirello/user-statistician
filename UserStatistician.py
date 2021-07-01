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
    watching(ownerAffiliations: OWNER) {
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

class Statistician :

    __slots__ = []

    def __init__(self) :
        self.queryBasicUserStats()
        self.queryAdditionalRepoStats()

    def queryBasicUserStats(self) :
        result = json.loads(self.executeQuery(basicStatsQuery))
        print(result)

    def queryAdditionalRepoStats(self) :
        result = self.executeQuery(additionalRepoStatsQuery, True)
        numPages = result.count('{"data"')
        if (numPages > 1) :
            result = result.replace('}{"data"', '},{"data"')
        result = "[" + result + "]"
        result = json.loads(result)
        print(result)

    def queryPriorYearStats(self) :
        pass

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


    # Fake example outputs
    output1 = "Hello"
    output2 = "World"

    # This is how you produce outputs.
    # Make sure corresponds to output variable names in action.yml
    print("::set-output name=output-one::" + output1)
    print("::set-output name=output-two::" + output2)
