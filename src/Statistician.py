#
# user-statistician: Github action for generating a user stats card
# 
# Copyright (c) 2021-2023 Vincent A Cicirello
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
import os

def set_outputs(names_values) :
    """Sets the GitHub Action outputs.

    Keyword arguments:
    names_values - Dictionary of output names with values
    """
    if "GITHUB_OUTPUT" in os.environ :
        with open(os.environ["GITHUB_OUTPUT"], "a") as f :
            for name, value in names_values.items() :
                print("{0}={1}".format(name, value), file=f)
    else : # Fall-back to deprecated set-output for self-hosted runners
        for name, value in names_values.items() :
            print("::set-output name={0}::{1}".format(name, value))

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
        '_name',
        '_languages',
        '_autoLanguages',
        '_maxLanguages',
        '_languageRepoExclusions',
        '_featuredRepo'
        ]

    def __init__(self, fail, autoLanguages, maxLanguages, languageRepoExclusions, featuredRepo) :
        """The initializer executes the queries and parses the results.
        Upon completion of the intitializer, the user statistics will
        be available.

        Keyword arguments:
        fail - If True, the workflow will fail if there are errors.
        autoLanguages - If True, the number of displayed languages is chosen based on data,
            regardless of value of maxLanguages.
        maxLanguages - The maximum number of languages to display. Must be at least 1. If less than
            1, it treats it as if it was 1.
        languageRepoExclusions - A set of repositories to exclude from language stats
        """
        self._autoLanguages = autoLanguages
        self._maxLanguages = maxLanguages if maxLanguages >= 1 else 1
        self._languageRepoExclusions = languageRepoExclusions
        self._featuredRepo = featuredRepo
        self.ghDisableInteractivePrompts()
        basicStatsQuery = self.loadQuery("/queries/basicstats.graphql",
                                         fail)
        additionalRepoStatsQuery = self.loadQuery("/queries/repostats.graphql",
                                                  fail)
        oneYearContribTemplate = self.loadQuery("/queries/singleYearQueryFragment.graphql",
                                                fail)
        watchingAdjustmentQuery = self.loadQuery("/queries/watchingAdjustment.graphql",
                                                 fail)

        reposContributedTo = self.loadQuery("/queries/reposContributedTo.graphql",
                                                 fail)
        
        self.parseStats(
            self.executeQuery(basicStatsQuery,
                              failOnError=fail),
            self.executeQuery(additionalRepoStatsQuery,
                              needsPagination=True,
                              failOnError=fail),
            self.executeQuery(watchingAdjustmentQuery,
                              needsPagination=True,
                              failOnError=fail),
            self.executeQuery(reposContributedTo,
                              needsPagination=True,
                              failOnError=fail)
            )
        self.parsePriorYearStats(
            self.executeQuery(
                self.createPriorYearStatsQuery(self._contributionYears, oneYearContribTemplate),
                failOnError=fail
                )
            )

    def getStatsByKey(self, key) :
        """Gets a category of stats by key.

        Keyword arguments:
        key - A category key.
        """
        if key == "general" :
            return self._user
        elif key == "repositories" :
            return self._repo
        elif key == "contributions" :
            return self._contrib
        elif key == "languages" :
            return self._languages
        else :
            return None # passed an invalid key 
        
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
            print("Error (1): Failed to open query file:", queryFilePath)
            set_outputs({"exit-code" : 1})
            exit(1 if failOnError else 0)

    def parseStats(self, basicStats, repoStats, watchingStats, reposContributedToStats) :
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

        # The name field is nullable, so use the login id if
        # user's public name is null.
        if self._name == None :
            self._name = self._login
        
        # Extract most recent year data from query results
        pastYearData = basicStats["data"]["user"]["contributionsCollection"]
        
        # Extract repositories contributes to (owned by others) in past year
        pastYearData["repositoriesContributedTo"] = basicStats["data"]["user"]["repositoriesContributedTo"]["totalCount"]

        # Extract list of contribution years
        self._contributionYears = pastYearData["contributionYears"]
        # Just reorganizing data for clarity
        del pastYearData["contributionYears"]

        # Extract followed and following counts
        self._user = {}
        self._user["followers"] = [ basicStats["data"]["user"]["followers"]["totalCount"] ]
        self._user["following"] = [ basicStats["data"]["user"]["following"]["totalCount"] ]
        self._user["joined"] = [ min(self._contributionYears) ]

        # Extract sponsors and sponsoring counts
        self._user["sponsors"] = [ basicStats["data"]["user"]["sponsorshipsAsMaintainer"]["totalCount"] ]
        self._user["sponsoring"] = [ basicStats["data"]["user"]["sponsorshipsAsSponsor"]["totalCount"] ]

        #
        if self._featuredRepo != None :
            self._user["featured"] = [ self._featuredRepo ]

        # Extract all time counts of issues and pull requests
        issues = basicStats["data"]["user"]["issues"]["totalCount"]
        pullRequests = basicStats["data"]["user"]["pullRequests"]["totalCount"]

        # Reorganize for simplicity
        repoStats = list(map(lambda x : x["data"]["user"]["repositories"], repoStats))
        watchingStats = list(map(lambda x : x["data"]["user"]["watching"], watchingStats))
        reposContributedToStats = list(map(lambda x : x["data"]["user"]["topRepositories"], reposContributedToStats))

        # This is the count of owned repos, including all public,
        # but may or may not include all private depending upon token used to authenticate.
        ownedRepositories = repoStats[0]["totalCount"]
        
        # Count num repos owned by someone else that the user has contributed to
        # NOTE: It doesn't appear that it is currently possible through any query
        # or combination of queries to actually compute this other than for the most recent
        # year's data. Keeping the query in, but changing to leave that stat blank in
        # the SVG.
        repositoriesContributedTo = sum(1 for page in reposContributedToStats if page["nodes"] != None for repo in page["nodes"] if repo["owner"]["login"] != self._login)
        
        self._contrib = {
            "commits" : [pastYearData["totalCommitContributions"], 0],
            "issues" : [pastYearData["totalIssueContributions"], issues],
            "prs" : [pastYearData["totalPullRequestContributions"], pullRequests],
            "reviews" : [pastYearData["totalPullRequestReviewContributions"], 0],
            # See comment above for reason for this change.
            #"contribTo" : [pastYearData["repositoriesContributedTo"], repositoriesContributedTo],
            "contribTo" : [pastYearData["repositoriesContributedTo"]],
            "private" : [pastYearData["restrictedContributionsCount"], 0]
            }

        # The "nodes" field is nullable so make sure the user owns at least 1 repo. 
        if repoStats[0]["totalCount"] > 0 :
            # Note that the explicit checks of, if page["nodes"] != None, are precautionary
            # since the above check of totalCount should be sufficient to protect against a null list of repos.
            
            # Count stargazers, forks of my repos, and watchers excluding me
            stargazers = sum(repo["stargazerCount"] for page in repoStats if page["nodes"] != None for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
            forksOfMyRepos = sum(repo["forkCount"] for page in repoStats if page["nodes"] != None for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
            stargazersAll = sum(repo["stargazerCount"] for page in repoStats if page["nodes"] != None for repo in page["nodes"] if not repo["isPrivate"])
            forksOfMyReposAll = sum(repo["forkCount"] for page in repoStats if page["nodes"] != None for repo in page["nodes"] if not repo["isPrivate"])

            # Find repos with most stars and most forks
            try :
                mostStars = max( (repo for page in repoStats if page["nodes"] != None for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"]), key=lambda x : x["stargazerCount"])["name"]
                self._user["mostStarred"] = [ mostStars ]
            except ValueError:
                pass

            try :
                mostForks = max( (repo for page in repoStats if page["nodes"] != None for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"]), key=lambda x : x["forkCount"])["name"]
                self._user["mostForked"] = [ mostForks ]
            except ValueError:
                pass
            
            # Compute number of watchers excluding cases where user is watching their own repos.
            watchers = sum(repo["watchers"]["totalCount"] for page in repoStats if page["nodes"] != None for repo in page["nodes"] if not repo["isPrivate"])
            watchers -= watchingStats[0]["totalCount"]

            if watchingStats[0]["totalCount"] > 0 :
                watchingMyOwnNonForks = sum(1 for page in watchingStats if page["nodes"] != None for repo in page["nodes"] if not repo["isFork"])
            else :
                watchingMyOwnNonForks = 0
            watchersNonForks = sum(repo["watchers"]["totalCount"] for page in repoStats if page["nodes"] != None for repo in page["nodes"] if not repo["isPrivate"] and not repo["isFork"])
            watchersNonForks -= watchingMyOwnNonForks
        
            # Count of private repos (which is not accurate since depends on token used to authenticate query,
            # however, all those here are included in count of owned repos.
            privateCount = sum(1 for page in repoStats if page["nodes"] != None for repo in page["nodes"] if repo["isPrivate"])

            publicAll = ownedRepositories - privateCount

            # Counts of archived repos
            publicNonForksArchivedCount = sum(1 for page in repoStats if page["nodes"] != None for repo in page["nodes"] if repo["isArchived"] and not repo["isPrivate"] and not repo["isFork"])
            publicArchivedCount = sum(1 for page in repoStats if page["nodes"] != None for repo in page["nodes"] if repo["isArchived"] and not repo["isPrivate"])

            # Counts of template repos
            publicNonForksTemplatesCount = sum(1 for page in repoStats if page["nodes"] != None for repo in page["nodes"] if repo["isTemplate"] and not repo["isPrivate"] and not repo["isFork"])
            publicTemplatesCount = sum(1 for page in repoStats if page["nodes"] != None for repo in page["nodes"] if repo["isTemplate"] and not repo["isPrivate"])
            
            # Count of public non forks owned by user
            publicNonForksCount = ownedRepositories - sum(1 for page in repoStats if page["nodes"] != None for repo in page["nodes"] if repo["isPrivate"] or repo["isFork"])

            # Compute language distribution
            totalSize, languageData = self.summarizeLanguageStats(repoStats)
        else :
            # if no owned repos then set all repo related stats to 0
            stargazers = 0
            forksOfMyRepos = 0
            stargazersAll = 0
            forksOfMyReposAll = 0
            watchers = 0
            watchingMyOwnNonForks = 0
            watchersNonForks = 0
            privateCount = 0
            publicAll = 0
            publicNonForksArchivedCount = 0
            publicArchivedCount = 0
            publicNonForksCount = 0
            publicNonForksTemplatesCount = 0
            publicTemplatesCount = 0
            totalSize, languageData = 0, {}

        self._repo = {
            "public" : [publicNonForksCount, publicAll],
            "starredBy" : [stargazers, stargazersAll],
            "forkedBy" : [forksOfMyRepos, forksOfMyReposAll],
            "watchedBy" : [watchersNonForks, watchers],
            "archived" : [publicNonForksArchivedCount, publicArchivedCount],
            "templates" : [publicNonForksTemplatesCount, publicTemplatesCount]
            }

        self._languages = self.organizeLanguageStats(totalSize, languageData)

    def organizeLanguageStats(self, totalSize, languageData) :
        """Computes a list of languages and percentages in decreasing order
        by percentage.

        Keyword arguments:
        totalSize - total size of all code with language detection data
        languageData - the summarized language totals, colors, etc
        """
        if totalSize == 0 :
            return { "totalSize" : 0, "languages" : [] }
        else :
            languages = [ (name, data) for name, data in languageData.items() ]
            languages.sort(key = lambda L : L[1]["size"], reverse=True)
            if self._autoLanguages :
                for i, L in enumerate(languages) :
                    if L[1]["percentage"] < 0.01 :
                        self._maxLanguages = i
                        break
            if len(languages) > self._maxLanguages :
                self.combineLanguages(languages, self._maxLanguages, totalSize)
            self.checkColors(languages)
            return { "totalSize" : totalSize, "languages" : languages }

    def combineLanguages(self, languages, maxLanguages, totalSize) :
        """Combines lowest percentage languages into an Other.

        Keyword arguments:
        languages - Sorted list of languages (sorted by size).
        maxLanguages - The maximum number of languages to keep as is.
        """
        if len(languages) > self._maxLanguages :
            combinedSize = sum(L[1]["size"] for L in languages[maxLanguages:])
            languages[maxLanguages] = (
                "Other",
                { "color" : None,
                  "size" : combinedSize,
                  "percentage" : combinedSize / totalSize
                  }
                )
            del languages[maxLanguages+1:]
        
    def checkColors(self, languages) :
        """Make sure all languages have colors, and assign shades of gray to
        those that don't.

        Keyword arguments:
        languages - Sorted list of languages (sorted by size).
        """
        # Not all languages have colors assigned by GitHub's Linguist.
        # In such cases, we alternate between these two shades of gray.
        colorsForLanguagesWithoutColors = [ "#959da5", "#d1d5da" ]
        index = 0
        for L in languages :
            if L[1]["color"] == None :
                L[1]["color"] = colorsForLanguagesWithoutColors[index]
                index = (index + 1) % 2

    def summarizeLanguageStats(self, repoStats) :
        """Summarizes the language distibution of the user's owned repositories.

        Keyword arguments:
        repoStats - The results of the repo stats query.
        """
        totalSize = 0
        languageData = {}
        for page in repoStats :
            if page["nodes"] != None :
                for repo in page["nodes"] :
                    if not repo["isPrivate"] and not repo["isFork"] and (repo["name"].lower() not in self._languageRepoExclusions) :
                        totalSize += repo["languages"]["totalSize"]
                        if repo["languages"]["edges"] != None :
                            for L in repo["languages"]["edges"] :
                                name = L["node"]["name"]
                                if name in languageData :
                                    languageData[name]["size"] += L["size"]
                                else :
                                    languageData[name] = {
                                        "color" : L["node"]["color"],
                                        "size" : L["size"]
                                        }
        for L in languageData :
            languageData[L]["percentage"] = languageData[L]["size"] / totalSize
        return totalSize, languageData

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
        if "GITHUB_REPOSITORY_OWNER" in os.environ :
            owner = os.environ["GITHUB_REPOSITORY_OWNER"]
        else :
            print("Error (7): Could not determine the repository owner.")
            set_outputs({"exit-code" : 7})
            exit(7 if failOnError else 0)
        arguments = [
            'gh', 'api', 'graphql',
            '-F', 'owner=' + owner,
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
        numPages = result.count('"data"')
        if numPages == 0 :
            # Check if any error details
            result = json.loads(result) if len(result) > 0 else ""
            if "errors" in result :
                print("Error (2): GitHub api Query failed with error:")
                print(result["errors"])
                code = 2
            else :
                print("Error (3): Something unexpected occurred during GitHub API query.")
                code = 3
            set_outputs({"exit-code" : code})
            exit(code if failOnError else 0)
        elif needsPagination :
            if (numPages > 1) :
                result = result.replace('}{"data"', '},{"data"')
            result = "[" + result + "]"
        result = json.loads(result)
        failed = False
        errorMessage = None
        if (not needsPagination) and (("data" not in result) or result["data"] == None) :
            failed = True
            if "errors" in result :
                errorMessage = result["errors"]
        elif needsPagination and ("data" not in result[0] or result[0]["data"] == None):
            failed = True
            if "errors" in result[0] :
                errorMessage = result[0]["errors"]
        if failed :
            print("Error (6): No data returned.")
            if errorMessage != None :
                print(errorMessage)
            set_outputs({"exit-code" : 6})
            exit(6 if failOnError else 0)
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
    
