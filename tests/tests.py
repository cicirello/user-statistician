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

import unittest

import sys
sys.path.insert(0,'src')
from Statistician import *
from Colors import *
from StatConfig import *

executedQueryResults = [
    {'data': {'user': {'contributionsCollection': {'totalCommitContributions': 3602, 'totalIssueContributions': 79, 'totalPullRequestContributions': 289, 'totalPullRequestReviewContributions': 315, 'totalRepositoryContributions': 18, 'restrictedContributionsCount': 105, 'contributionYears': [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011]}, 'followers': {'totalCount': 9}, 'following': {'totalCount': 7}, 'issues': {'totalCount': 81}, 'login': 'cicirello', 'name': 'Vincent A. Cicirello', 'pullRequests': {'totalCount': 289}, 'repositoriesContributedTo': {'totalCount': 3}, 'topRepositories': {'totalCount': 33}}}},

    [{'data': {'user': {'repositories': {'totalCount': 29, 'nodes': [{'stargazerCount': 0, 'forkCount': 0, 'isArchived': True, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': True, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 3, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': True, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 3, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 2}}, {'stargazerCount': 3, 'forkCount': 2, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 2, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 7, 'forkCount': 4, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 3, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 3, 'forkCount': 2, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 1, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 1, 'forkCount': 2, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 2, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 2, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 1, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 9, 'forkCount': 14, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 2}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': True, 'isTemplate': False, 'watchers': {'totalCount': 1}}], 'pageInfo': {'hasNextPage': False, 'endCursor': 'Y3Vyc29yOnYyOpHOFsahLQ=='}}}}}],

    [{'data': {'user': {'watching': {'totalCount': 28, 'nodes': [{'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}], 'pageInfo': {'hasNextPage': False, 'endCursor': 'Mjg'}}}}}],

    {'data': {'user': {'year2021': {'totalCommitContributions': 1850, 'totalPullRequestReviewContributions': 223, 'restrictedContributionsCount': 105}, 'year2020': {'totalCommitContributions': 1845, 'totalPullRequestReviewContributions': 92, 'restrictedContributionsCount': 0}, 'year2019': {'totalCommitContributions': 194, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2018': {'totalCommitContributions': 198, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2017': {'totalCommitContributions': 177, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2016': {'totalCommitContributions': 138, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2015': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2014': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2013': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2012': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2011': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}}}}
    ]

executedQueryResultsMultiPage = [
    {'data': {'user': {'contributionsCollection': {'totalCommitContributions': 3602, 'totalIssueContributions': 79, 'totalPullRequestContributions': 289, 'totalPullRequestReviewContributions': 315, 'totalRepositoryContributions': 18, 'restrictedContributionsCount': 105, 'contributionYears': [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011]}, 'followers': {'totalCount': 9}, 'following': {'totalCount': 7}, 'issues': {'totalCount': 81}, 'login': 'cicirello', 'name': 'Vincent A. Cicirello', 'pullRequests': {'totalCount': 289}, 'repositoriesContributedTo': {'totalCount': 3}, 'topRepositories': {'totalCount': 33}}}},

    [{'data': {'user': {'repositories': {'totalCount': 29, 'nodes': [{'stargazerCount': 0, 'forkCount': 0, 'isArchived': True, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': True, 'watchers': {'totalCount': 1}}, {'stargazerCount': 3, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': True, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 3, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 2}}, {'stargazerCount': 3, 'forkCount': 2, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 2, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 7, 'forkCount': 4, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}], 'pageInfo': {'hasNextPage': True, 'endCursor': 'Y3Vyc29yOnYyOpHOEEbJCQ=='}}}}}, {'data': {'user': {'repositories': {'totalCount': 29, 'nodes': [{'stargazerCount': 3, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 3, 'forkCount': 2, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 1, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 1, 'forkCount': 2, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 2, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 2, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}], 'pageInfo': {'hasNextPage': True, 'endCursor': 'Y3Vyc29yOnYyOpHOEcjkCw=='}}}}}, {'data': {'user': {'repositories': {'totalCount': 29, 'nodes': [{'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 1, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 9, 'forkCount': 14, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 2}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': False, 'isTemplate': False, 'watchers': {'totalCount': 1}}, {'stargazerCount': 0, 'forkCount': 0, 'isArchived': False, 'isFork': False, 'isPrivate': True, 'isTemplate': False, 'watchers': {'totalCount': 1}}], 'pageInfo': {'hasNextPage': False, 'endCursor': 'Y3Vyc29yOnYyOpHOFsahLQ=='}}}}}],

    [{'data': {'user': {'watching': {'totalCount': 28, 'nodes': [{'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}], 'pageInfo': {'hasNextPage': True, 'endCursor': 'MTA'}}}}}, {'data': {'user': {'watching': {'totalCount': 28, 'nodes': [{'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}], 'pageInfo': {'hasNextPage': True, 'endCursor': 'MjA'}}}}}, {'data': {'user': {'watching': {'totalCount': 28, 'nodes': [{'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}, {'isFork': False}], 'pageInfo': {'hasNextPage': False, 'endCursor': 'Mjg'}}}}}],
    
    {'data': {'user': {'year2021': {'totalCommitContributions': 1850, 'totalPullRequestReviewContributions': 223, 'restrictedContributionsCount': 105}, 'year2020': {'totalCommitContributions': 1845, 'totalPullRequestReviewContributions': 92, 'restrictedContributionsCount': 0}, 'year2019': {'totalCommitContributions': 194, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2018': {'totalCommitContributions': 198, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2017': {'totalCommitContributions': 177, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2016': {'totalCommitContributions': 138, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2015': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2014': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2013': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2012': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}, 'year2011': {'totalCommitContributions': 0, 'totalPullRequestReviewContributions': 0, 'restrictedContributionsCount': 0}}}}
    ]

class TestSomething(unittest.TestCase) :

    def test_parseQueryResults(self) :
        class NoQueries(Statistician) :
            def __init__(self, fail=True) :
                self.parseStats(
                    executedQueryResults[0],
                    executedQueryResults[1],
                    executedQueryResults[2]
                    )
                self.parsePriorYearStats(executedQueryResults[3])
        stats = NoQueries()
        self._validate(stats)
    
    def test_parseQueryResultsMultipageQueryResults(self) :
        class NoQueriesMultipage(Statistician) :
            def __init__(self, fail=True) :
                self.parseStats(
                    executedQueryResultsMultiPage[0],
                    executedQueryResultsMultiPage[1],
                    executedQueryResultsMultiPage[2]
                    )
                self.parsePriorYearStats(executedQueryResultsMultiPage[3])
        stats = NoQueriesMultipage()
        self._validate(stats)

    def test_color_themes(self) :
        originalThemes = {"light", "dark", "dark-dimmed"}
        for theme in originalThemes :
            self._colorValidation(colorMapping[theme])
        for theme in colorMapping :
            if theme not in originalThemes :
                self._colorValidation(colorMapping[theme])

    def test_title_templates(self) :
        unlikelyInTemplate = "qwertyuiop"
        try :
            for locale in supportedLocales :
                title = titleTemplates[locale].format(unlikelyInTemplate)
                self.assertTrue(title.find(unlikelyInTemplate)>=0)
        except IndexError :
            self.fail()

    def test_categories(self) :
        categories = {"general", "repositories", "contributions"}
        self.assertEqual(set(categoryOrder), categories)
        statistics = {
            "followers", "following", "public", "starredBy",
            "forkedBy", "watchedBy", "templates", "archived", "commits",
            "issues", "prs", "reviews", "contribTo", "private"
            }
        
        # Make sure all are accounted for in a category
        statKeys = { stat for cat in categoryOrder for stat in statsByCategory[cat]}
        self.assertEqual(statistics, statKeys)

        # Make sure none are in more than one categories
        numStats = sum(len(statsByCategory[cat]) for cat in categoryOrder)
        self.assertEqual(numStats, len(statistics))

    def test_category_labels(self) :
        categories = categoryOrder
        types = {"heading", "column-one", "column-two"}
        for locale in supportedLocales :
            self.assertTrue(locale in categoryLabels)
            labelMap = categoryLabels[locale]
            for cat in categories :
                self.assertTrue(cat in labelMap)
                for t in types :
                    self.assertTrue(t in labelMap[cat])
                    
    def test_stat_labels(self) :
        keys = {
            "followers", "following", "public", "starredBy",
            "forkedBy", "watchedBy", "templates", "archived", "commits",
            "issues", "prs", "reviews", "contribTo", "private"
            }
        self.assertTrue(all(k in statLabels for k in keys))
        for k in keys :
            self.assertTrue("icon" in statLabels[k])
            self.assertTrue(statLabels[k]["icon"].startswith("<path "))
            self.assertTrue(statLabels[k]["icon"].endswith("/>"))
            labelsByLocale = statLabels[k]["label"]
            for locale in supportedLocales :
                self.assertTrue(locale in labelsByLocale)

    def _colorValidation(self, theme) :
        props = {"bg", "border", "icons", "text", "title"}
        validHexDigits = set("0123456789abcdefABCDEF")
        for p in props :
            color = theme[p]
            self.assertEqual("#", color[0])
            self.assertTrue(len(color)==4 or len(color)==7)
            self.assertTrue(all(c in validHexDigits for c in color[1:]))

    def _validate(self, stats) :
        self.assertEqual(9, stats._user["followers"][0])
        self.assertEqual(7, stats._user["following"][0])
        self.assertEqual(28, stats._repo["public"][0])
        self.assertEqual(28, stats._repo["public"][1])
        self.assertEqual(36, stats._repo["starredBy"][0])
        self.assertEqual(36, stats._repo["starredBy"][1])
        self.assertEqual(28, stats._repo["forkedBy"][0])
        self.assertEqual(28, stats._repo["forkedBy"][1])
        self.assertEqual(2, stats._repo["watchedBy"][0])
        self.assertEqual(2, stats._repo["watchedBy"][1])
        self.assertEqual(2, stats._repo["archived"][0])
        self.assertEqual(2, stats._repo["archived"][1])
        self.assertEqual(1, stats._repo["templates"][0])
        self.assertEqual(1, stats._repo["templates"][1])
        self.assertEqual(3602, stats._contrib["commits"][0])
        self.assertEqual(4402, stats._contrib["commits"][1])
        self.assertEqual(79, stats._contrib["issues"][0])
        self.assertEqual(81, stats._contrib["issues"][1])
        self.assertEqual(289, stats._contrib["prs"][0])
        self.assertEqual(289, stats._contrib["prs"][1])
        self.assertEqual(315, stats._contrib["reviews"][0])
        self.assertEqual(315, stats._contrib["reviews"][1])
        self.assertEqual(3, stats._contrib["contribTo"][0])
        self.assertEqual(4, stats._contrib["contribTo"][1])
        self.assertEqual(105, stats._contrib["private"][0])
        self.assertEqual(105, stats._contrib["private"][1])
        
        
