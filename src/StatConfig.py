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


# ADDITIONAL LICENSE NOTES
#
# GitHub's Octicons:
# The paths defining the icons used in the action
# are derived from GitHub's Octicons (https://github.com/primer/octicons),
# and are copyright (c) GitHub, Inc, and licensed by GitHub under
# the MIT license.

# Mapping from category key to list of stats keys in the
# order they should appear.
statsByCategory = {
    "general" : [
        "joined",
        "featured",
        "mostStarred",
        "mostForked",
        "followers",
        "sponsors",
        "following",
        "sponsoring"
    ],
    "repositories" : [
        "public",
        "starredBy",
        "forkedBy",
        "watchedBy",
        "templates",
        "archived"
    ],
    "contributions" : [
        "commits",
        "issues",
        "prs",
        "reviews",
        "contribTo",
        "private"
    ],
    "languages" : []
}

# The default order for the categories of stats on the SVG
categoryOrder = ["general", "repositories", "contributions", "languages"]


# Steps to Contributing a New Locale:
# (0) Check if there are any open issues or pull requests
#     related to the locale that you want to add. Begin by opening
#     an issue indicating the locale that you want to add. Perhaps
#     mention in the issue that you are planning to work on it, so
#     we know the difference between a simple request with nobody to
#     work on it vs a volunteer. Once you've submitted the issue,
#     fork the repo, and create a branch for your feature.
# (1) Add a string for the 2-character code to the set
#     supportedLocales.
# (2) In the Python dictionary, categoryLabels, create a
#     mapping corresponding to that new 2-character string.
#     You might start by copying and pasting the entirety of
#     the entry for "en". Make sure you keep the dictionary keys
#     as they are, and only translate the values.
# (3) In the Python dictionary, titleTemplates, add a template for
#     the default title by adding a mapping from the 2-character
#     string for the new locale to a format string (see the comments
#     where titleTemplates is declared.
# (4) In the Python dictionary, statLabels, each key "label" maps to
#     a Python dictionary with the locale code as key. Add a corresponding
#     key value pair for the new locale.
# (5) The existing test cases will verify that all of the above
#     has been done for each 2 character locale code in the
#     supportedLocales set. So no new test cases should be necessary when
#     adding a locale, but existing tests must pass.
# (6) If you contribute translations for a new locale,
#     or if you correct any errors in one, then please
#     credit yourself here by either adding a list below for
#     the relevant locale if it is new, or adding your
#     GitHub user id to the list below if you contributed a bug
#     fix to an existing one.
#
# Locale Contributors:
# en: cicirello
# it: ziriuz84
# de: pje3110
# pt: andrefpoliveira
# hi: Anik-Bardhan
# fr: thomasbnt
# ru: JayBee007
# es: alanverdugo
# pl: Jibendu007

# The locale keys are ISO 639-1 two-character language codes
# (see: https://www.loc.gov/standards/iso639-2/php/English_list.php).
supportedLocales = { "en", "it", "de", "pt", "id", "hi", "fr", "ru", "es", "pl" }


# Dictionary of header rows for categories of statistics
categoryLabels = {
  
    "en" : {
        "general" : {
            "heading" : "General Stats and Info",
            "column-one" : None,
            "column-two" : None
        },
        "repositories" : {
            "heading" : "Repositories",
            "column-one" : "Non-Forks",
            "column-two" : "All"
        },
        "contributions" : {
            "heading" : "Contributions",
            "column-one" : "Past Year",
            "column-two" : "Total"
        },
        "languages" : {
            "heading" : "Language Distribution in Public Repositories",
            "column-one" : None,
            "column-two" : None
        }
    },
  
    "it" : {
        "general" : {
            "heading" : "Statistiche Generali e Informazioni",
            "column-one" : None,
            "column-two" : None
        },
        "repositories" : {
            "heading" : "Repository",
            "column-one" : "Non-Fork",
            "column-two" : "Tutti"
        },
        "contributions" : {
            "heading" : "Contributi",
            "column-one" : "Anno Scorso",
            "column-two" : "Totale"
        },
        "languages" : {
            "heading" : "Distribuzione del Linguaggio nei Repository Pubblici",
            "column-one" : None,
            "column-two" : None
        }
    },
  
    "de" : {
        "general" : {
            "heading" : "Allgemeine Statistiken und Informationen",
            "column-one" : None,
            "column-two" : None
        },
        "repositories" : {
            "heading" : "Repositories",
            "column-one" : "Non-Forks",
            "column-two" : "Alle"
        },
        "contributions" : {
            "heading" : "Beiträge",
            "column-one" : "Letztes Jahr",
            "column-two" : "Gesamt"
        },
        "languages" : {
            "heading" : "Verteilung der Sprachen in Öffentlichen Repositories",
            "column-one" : None,
            "column-two" : None
        }
    },

    "pt" : {
        "general" : {
            "heading" : "Estatísticas Gerais e Informações",
            "column-one" : None,
            "column-two" : None
        },
        "repositories" : {
            "heading" : "Repositórios",
            "column-one" : "Sem Forks",
            "column-two" : "Todos"
        },
        "contributions" : {
            "heading" : "Contribuições",
            "column-one" : "Último ano",
            "column-two" : "Total"
        },
        "languages" : {
            "heading" : "Distribuição de Linguagens em Repositórios Públicos",
            "column-one" : None,
            "column-two" : None
        }
    },

    "id" : {
        "general" : {
            "heading" : "Info dan Status Umum",
            "column-one" : None,
            "column-two" : None
        },
        "repositories" : {
            "heading" : "Repositori",
            "column-one" : "Non Fork",
            "column-two" : "Semua"
        },
        "contributions" : {
            "heading" : "Kontribusi",
            "column-one" : "Tahun Lalu",
            "column-two" : "Total"
        },
        "languages" : {
            "heading" : "Distribusi Bahasa dalam Repositori Publik",
            "column-one" : None,
            "column-two" : None
        }
    },
  
    "hi" : {
        "general" : {
            "heading" : "साधारण सांख्यिकी और सूचना",
            "column-one" : None,
            "column-two" : None
            },
        "repositories" : {
            "heading" : "भंडार",
            "column-one" : "गैर-फोर्क",
            "column-two" : "सभी"
            },
        "contributions" : {
            "heading" : "योगदान",
            "column-one" : "पिछला वर्ष",
            "column-two" : "कुल"
            },
        "languages" : {
            "heading" : "सार्वजनिक भंडारों में भाषा वितरण",
            "column-one" : None,
            "column-two" : None
            }
    },
  
    "fr" : {
        "general" : {
          "heading" : "Statistiques Générales et Info",
          "column-one" : None,
          "column-two" : None
        },
        "repositories" : {
          "heading" : "Dépôts",
          "column-one" : "Non clonés",
          "column-two" : "Tout"
        },
        "contributions" : {
          "heading" : "Contributions",
          "column-one" : "Dernière année",
          "column-two" : "Total"
        },
        "languages" : {
          "heading" : "Répartition des langages dans les dépôts publiques",
          "column-one" : None,
          "column-two" : None
        }
    },
  
    "ru" : {
        "general" : {
            "heading" : "Общая статистика и информация",
            "column-one" : None,
            "column-two" : None
        },
        "repositories" : {
            "heading" : "Репозиториев",
            "column-one" : "Без форков",
            "column-two" : "Все"
        },
        "contributions" : {
            "heading" : "Участие",
            "column-one" : "За последный год",
            "column-two" : "Всего"
        },
        "languages" : {
            "heading" : "Использование языков в общедоступных репозиториях",
            "column-one" : None,
            "column-two" : None
        }
    },
  
    "es" : {
        "general" : {
            "heading" : "Estadísticas generales e información",
            "column-one" : None,
            "column-two" : None
        },
        "repositories" : {
            "heading" : "Repositorios",
            "column-one" : "No bifurcados",
            "column-two" : "Todos"
        },
        "contributions" : {
            "heading" : "Contribuciones",
            "column-one" : "Año pasado",
            "column-two" : "Total"
        },
        "languages" : {
            "heading" : "Distribución de lenguajes en repositorios públicos",
            "column-one" : None,
            "column-two" : None
        }
    },

    "pl" : {
        "general" : {
            "heading" : "Ogólne statystyki i informacje",
            "column-one" : None,
            "column-two" : None
            },
        "repositories" : {
            "heading" : "Repozytoria",
            "column-one" : "Non-Forks",
            "column-two" : "Wszystkie"
            },
        "contributions" : {
            "heading" : "Kontrybucje",
            "column-one" : "Ostatni rok",
            "column-two" : "Wszystkie"
            },
        "languages" : {
            "heading" : "Rozkład języków w Repozytoriach Publicznych",
            "column-one" : None,
            "column-two" : None
        }
    }
}

# Dictionary of default title templates.
# {0} corresponds to repository owner's name.
titleTemplates = {
    "en" : "{0}'s GitHub Activity",
    "it" : "Attività GitHub di {0}",
    "de" : "{0}s GitHub Aktivität",
    "pt" : "Atividade de {0} no GitHub",
    "id" : "Aktivitas Github {0}",
    "hi" : "{0} की गिटहब गतिविधि",
    "fr" : "Activité GitHub de {0}",
    # Russian declension depends on many factors
    # just adding 's wont help
    # so it literally says "Activity on Github"
    "ru" : "Активность на гитхабе",
    "es" : "Actividad en GitHub de {0}",
    "pl" : "Aktywność {0} na GitHubie"
}

# Dictionary of icon paths and labels for the supported statistics.
statLabels = {

    "joined" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M13.25 0a.75.75 0 01.75.75V2h1.25a.75.75 0 010 1.5H14v1.25a.75.75 0 01-1.5 0V3.5h-1.25a.75.75 0 010-1.5h1.25V.75a.75.75 0 01.75-.75zM5.5 4a2 2 0 100 4 2 2 0 000-4zm2.4 4.548a3.5 3.5 0 10-4.799 0 5.527 5.527 0 00-3.1 4.66.75.75 0 101.498.085A4.01 4.01 0 015.5 9.5a4.01 4.01 0 014.001 3.793.75.75 0 101.498-.086 5.527 5.527 0 00-3.1-4.659z"/>',
        "label" : {
            "en" : "Year Joined",
            "it" : "Anno di Iscrizione",
            "de" : "Beitrittsdatum",
            "pt" : "Ano de Inscrição",
            "id" : "Tahun Bergabung",
            "hi" : "युक्त होने का वर्ष",
            "fr" : "Année d'adhésion",
            "ru" : "Год начала работы на гитхабе",
            "es" : "Año de ingreso",
            "pl" : "Rok Dołączenia"
        }
    },

    "featured" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M3.637 2.291A.75.75 0 014.23 2h7.54a.75.75 0 01.593.291l3.48 4.5a.75.75 0 01-.072.999l-7.25 7a.75.75 0 01-1.042 0l-7.25-7a.75.75 0 01-.072-.999l3.48-4.5zM4.598 3.5L1.754 7.177 8 13.207l6.246-6.03L11.402 3.5H4.598z"/>',
        "label" : {
            "en" : "Featured Repo",
            "it" : "Repo in Primo Piano",
            "de" : "Vorgestelltes Repo",
            "pt" : "Repositório em Primeiro Plano",
            "id" : "Repositori Unggulan",
            "hi" : "विशेष रुप से प्रदर्शित भंडार",
            "fr" : "Dépôt en vedette",
            "ru" : "Избранное репо",
            "es" : "Repositorio destacado",
            "pl" : "Polecane repozytorium"
        }
    },

    "mostStarred" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"/>',
        "label" : {
            "en" : "Most Starred Repo",
            "it" : "Repo con più Stelle",
            "de" : "Meistmarkiertes Repo",
            "pt" : "Repositório com mais estrelas",
            "id" : "Repositori dengan Bintang Terbanyak",
            "hi" : "सर्वाधिक तारांकित भंडार",
            "fr" : "Dépôt le plus étoilé",
            "ru" : "Самое замеченное репо",
            "es" : "Repositorio con más estrellas",
            "pl" : "Repozytoria z największą ilością gwiazdek"
        }
    },

    "mostForked" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"/>',
        "label" : {
            "en" : "Most Forked Repo",
            "it" : "Repo con più Fork",
            "de" : "Meistgeforktes Repo",
            "pt" : "Repositório mais bifurcado",
            "id" : "Repositori dengan Fork Terbanyak",
            "hi" : "सर्वाधिक फोर्क भंडार",
            "fr" : "Dépôt le plus cloné",
            "ru" : "Самое клонированное репо",
            "es" : "Repositorio más bifurcado",
            "pl" : "Najczęściej Forkowane Repozytoria"
        }
    },

    "followers" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M5.5 3.5a2 2 0 100 4 2 2 0 000-4zM2 5.5a3.5 3.5 0 115.898 2.549 5.507 5.507 0 013.034 4.084.75.75 0 11-1.482.235 4.001 4.001 0 00-7.9 0 .75.75 0 01-1.482-.236A5.507 5.507 0 013.102 8.05 3.49 3.49 0 012 5.5zM11 4a.75.75 0 100 1.5 1.5 1.5 0 01.666 2.844.75.75 0 00-.416.672v.352a.75.75 0 00.574.73c1.2.289 2.162 1.2 2.522 2.372a.75.75 0 101.434-.44 5.01 5.01 0 00-2.56-3.012A3 3 0 0011 4z"/>',
        "label" : {
            "en" : "Followers",
            "it" : "Seguaci",
            "de" : "Follower",
            "pt" : "Seguidores",
            "id" : "Pengikut",
            "hi" : "समर्थक",
            "fr" : "Abonnés",
            "ru" : "Подписчики",
            "es" : "Seguidores",
            "pl" : "Obserwujący"
        }
    },

    "following" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M5.5 3.5a2 2 0 100 4 2 2 0 000-4zM2 5.5a3.5 3.5 0 115.898 2.549 5.507 5.507 0 013.034 4.084.75.75 0 11-1.482.235 4.001 4.001 0 00-7.9 0 .75.75 0 01-1.482-.236A5.507 5.507 0 013.102 8.05 3.49 3.49 0 012 5.5zM11 4a.75.75 0 100 1.5 1.5 1.5 0 01.666 2.844.75.75 0 00-.416.672v.352a.75.75 0 00.574.73c1.2.289 2.162 1.2 2.522 2.372a.75.75 0 101.434-.44 5.01 5.01 0 00-2.56-3.012A3 3 0 0011 4z"/>',
        "label" : {
            "en" : "Following",
            "it" : "Seguendo",
            "de" : "Folgt",
            "pt" : "A seguir",
            "id" : "Mengikuti",
            "hi" : "अनुगामी",
            "fr" : "Abonnements",
            "ru" : "Подписан",
            "es" : "Siguiendo",
            "pl" : "Obserwowani"
        }
    },

    "sponsors" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M4.25 2.5c-1.336 0-2.75 1.164-2.75 3 0 2.15 1.58 4.144 3.365 5.682A20.565 20.565 0 008 13.393a20.561 20.561 0 003.135-2.211C12.92 9.644 14.5 7.65 14.5 5.5c0-1.836-1.414-3-2.75-3-1.373 0-2.609.986-3.029 2.456a.75.75 0 01-1.442 0C6.859 3.486 5.623 2.5 4.25 2.5zM8 14.25l-.345.666-.002-.001-.006-.003-.018-.01a7.643 7.643 0 01-.31-.17 22.075 22.075 0 01-3.434-2.414C2.045 10.731 0 8.35 0 5.5 0 2.836 2.086 1 4.25 1 5.797 1 7.153 1.802 8 3.02 8.847 1.802 10.203 1 11.75 1 13.914 1 16 2.836 16 5.5c0 2.85-2.045 5.231-3.885 6.818a22.08 22.08 0 01-3.744 2.584l-.018.01-.006.003h-.002L8 14.25zm0 0l.345.666a.752.752 0 01-.69 0L8 14.25z"/>',
        "label" : {
            "en" : "Sponsors",
            "it" : "Sponsors",
            "de" : "Sponsoren",
            "pt" : "Patrocinado",
            "id" : "Sponsor",
            "hi" : "प्रायोजक",
            "fr" : "Sponsors",
            "ru" : "Спонсоры",
            "es" : "Patrocinadores",
            "pl" : "Sponsorzy"
        }
    },

    "sponsoring" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M4.25 2.5c-1.336 0-2.75 1.164-2.75 3 0 2.15 1.58 4.144 3.365 5.682A20.565 20.565 0 008 13.393a20.561 20.561 0 003.135-2.211C12.92 9.644 14.5 7.65 14.5 5.5c0-1.836-1.414-3-2.75-3-1.373 0-2.609.986-3.029 2.456a.75.75 0 01-1.442 0C6.859 3.486 5.623 2.5 4.25 2.5zM8 14.25l-.345.666-.002-.001-.006-.003-.018-.01a7.643 7.643 0 01-.31-.17 22.075 22.075 0 01-3.434-2.414C2.045 10.731 0 8.35 0 5.5 0 2.836 2.086 1 4.25 1 5.797 1 7.153 1.802 8 3.02 8.847 1.802 10.203 1 11.75 1 13.914 1 16 2.836 16 5.5c0 2.85-2.045 5.231-3.885 6.818a22.08 22.08 0 01-3.744 2.584l-.018.01-.006.003h-.002L8 14.25zm0 0l.345.666a.752.752 0 01-.69 0L8 14.25z"/>',
        "label" : {
            "en" : "Sponsoring",
            "it" : "Sponsorizza",
            "de" : "Sponsoring",
            "pt" : "A patrocinar",
            "id" : "Mensponsori",
            "hi" : "प्रायोजन",
            "fr" : "Sponsorise",
            "ru" : "Спонсирует",
            "es" : "Patrocinando",
            "pl" : "Sponsoring"
        }
    },

    "public" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>',
        "label" : {
            "en" : "Repositories Owned",
            "it" : "Repository di Proprietà",
            "de" : "Eigene Repositories",
            "pt" : "Repositórios Possuídos",
            "id" : "Repositori yang Dimiliki",
            "hi" : "अपना भंडार",
            "fr" : "Dépôts possédés",
            "ru" : "Собственные репозитории",
            "es" : "Repositorios propios",
            "pl" : "Posiadane Repozytoria"
        }
    },

    "starredBy" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"/>',
        "label" : {
            "en" : "Starred By",
            "it" : "Stellato Da",
            "de" : "Markiert Von",
            "pt" : "Com Estrela De",
            "id" : "Diberikan bintang oleh",
            "hi" : "किसके द्वारा तारांकित",
            "fr" : "Étoilé par",
            "ru" : "Отметили",
            "es" : "Con estrella por",
            "pl" : "Polubione przez"
        }
    },

    "forkedBy" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"/>',
        "label" : {
            "en" : "Forked By",
            "it" : "Forkato Da",
            "de" : "Geforkt Von",
            "pt" : "Bifurcado Por",
            "id" : "Di-fork oleh",
            "hi" : "किसके द्वारा फोर्क किया गया",
            "fr" : "Cloné par",
            "ru" : "Клонирован",
            "es" : "Bifurcado por",
            "pl" : "Sforkowane przez"
        }
    },

    "watchedBy" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M1.679 7.932c.412-.621 1.242-1.75 2.366-2.717C5.175 4.242 6.527 3.5 8 3.5c1.473 0 2.824.742 3.955 1.715 1.124.967 1.954 2.096 2.366 2.717a.119.119 0 010 .136c-.412.621-1.242 1.75-2.366 2.717C10.825 11.758 9.473 12.5 8 12.5c-1.473 0-2.824-.742-3.955-1.715C2.92 9.818 2.09 8.69 1.679 8.068a.119.119 0 010-.136zM8 2c-1.981 0-3.67.992-4.933 2.078C1.797 5.169.88 6.423.43 7.1a1.619 1.619 0 000 1.798c.45.678 1.367 1.932 2.637 3.024C4.329 13.008 6.019 14 8 14c1.981 0 3.67-.992 4.933-2.078 1.27-1.091 2.187-2.345 2.637-3.023a1.619 1.619 0 000-1.798c-.45-.678-1.367-1.932-2.637-3.023C11.671 2.992 9.981 2 8 2zm0 8a2 2 0 100-4 2 2 0 000 4z"/>',
        "label" : {
            "en" : "Watched By",
            "it" : "Seguito Da",
            "de" : "Verfolgt Von",
            "pt" : "Visto Por",
            "id" : "Dilihat oleh",
            "hi" : "किसके द्वारा देखा गया",
            "fr" : "Regardé par",
            "ru" : "Наблюдатели",
            "es" : "Visto por",
            "pl" : "Obserwowane przez"
        }
    },

    "templates" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M6 .75A.75.75 0 016.75 0h2.5a.75.75 0 010 1.5h-2.5A.75.75 0 016 .75zm5 0a.75.75 0 01.75-.75h1.5a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0V1.5h-.75A.75.75 0 0111 .75zM4.992.662a.75.75 0 01-.636.848c-.436.063-.783.41-.846.846a.75.75 0 01-1.485-.212A2.501 2.501 0 014.144.025a.75.75 0 01.848.637zM2.75 4a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 012.75 4zm10.5 0a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5a.75.75 0 01.75-.75zM2.75 8a.75.75 0 01.75.75v.268A1.72 1.72 0 013.75 9h.5a.75.75 0 010 1.5h-.5a.25.25 0 00-.25.25v.75c0 .28.114.532.3.714a.75.75 0 01-1.05 1.072A2.495 2.495 0 012 11.5V8.75A.75.75 0 012.75 8zm10.5 0a.75.75 0 01.75.75v4.5a.75.75 0 01-.75.75h-2.5a.75.75 0 010-1.5h1.75v-2h-.75a.75.75 0 010-1.5h.75v-.25a.75.75 0 01.75-.75zM6 9.75A.75.75 0 016.75 9h2.5a.75.75 0 010 1.5h-2.5A.75.75 0 016 9.75zm-1 2.5v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>',
        "label" : {
            "en" : "Templates",
            "it" : "Modelli",
            "de" : "Vorlagen",
            "pt" : "Modelos",
            "id" : "Template",
            "hi" : "आकार पट्ट",
            "fr" : "Modèles",
            "ru" : "Шаблоны",
            "es" : "Plantillas",
            "pl" : "Szablony"
        }
    },

    "archived" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M1.75 2.5a.25.25 0 00-.25.25v1.5c0 .138.112.25.25.25h12.5a.25.25 0 00.25-.25v-1.5a.25.25 0 00-.25-.25H1.75zM0 2.75C0 1.784.784 1 1.75 1h12.5c.966 0 1.75.784 1.75 1.75v1.5A1.75 1.75 0 0114.25 6H1.75A1.75 1.75 0 010 4.25v-1.5zM1.75 7a.75.75 0 01.75.75v5.5c0 .138.112.25.25.25h10.5a.25.25 0 00.25-.25v-5.5a.75.75 0 111.5 0v5.5A1.75 1.75 0 0113.25 15H2.75A1.75 1.75 0 011 13.25v-5.5A.75.75 0 011.75 7zm4.5 1a.75.75 0 000 1.5h3.5a.75.75 0 100-1.5h-3.5z"/>',
        "label" : {
            "en" : "Archived",
            "it" : "Archiviato",
            "de" : "Archiviert",
            "pt" : "Arquivados",
            "id" : "Diarsipkan",
            "hi" : "संग्रहीत",
            "fr" : "Archivé",
            "ru" : "Заархивированный",
            "es" : "Archivado",
            "pl" : "Zarchiwizowane"
        }
    },

    "commits" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M10.5 7.75a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zm1.43.75a4.002 4.002 0 01-7.86 0H.75a.75.75 0 110-1.5h3.32a4.001 4.001 0 017.86 0h3.32a.75.75 0 110 1.5h-3.32z"/>',
        "label" : {
            "en" : "Commits",
            "it" : "Commits",
            "de" : "Commits",
            "pt" : "Commits",
            "id" : "Commits",
            "hi" : "प्रतिबद्ध",
            "fr" : "Commits",
            "ru" : "Коммиты",
            "es" : "Commits",
            "pl" : "Commity"
        }
    },

    "issues" : {
        "icon" : '<path fill="{0}" d="M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"/><path fill="{0}" fill-rule="evenodd" d="M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z"/>',
        "label" : {
            "en" : "Issues",
            "it" : "Problemi",
            "de" : "Issues",
            "pt" : "Problemas",
            "id" : "Isu",
            "hi" : "मुद्दे",
            "fr" : "Issues",
            "ru" : "Проблемы",
            "es" : "Problemas",
            "pl" : "Problemy"
        }
    },

    "prs" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z"/>',
        "label" : {
            "en" : "Pull Requests",
            "it" : "Richieste di Pull",
            "de" : "Pull Requests",
            "pt" : "Pull Requests",
            "id" : "Pull Requests",
            "hi" : "अनुरोध",
            "fr" : "Pull Requests",
            "ru" : "Пулл реквесты",
            "es" : "Pull Requests",
            "pl" : "Pull Requesty"
        }
    },

    "reviews" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M1.5 2.75a.25.25 0 01.25-.25h8.5a.25.25 0 01.25.25v5.5a.25.25 0 01-.25.25h-3.5a.75.75 0 00-.53.22L3.5 11.44V9.25a.75.75 0 00-.75-.75h-1a.25.25 0 01-.25-.25v-5.5zM1.75 1A1.75 1.75 0 000 2.75v5.5C0 9.216.784 10 1.75 10H2v1.543a1.457 1.457 0 002.487 1.03L7.061 10h3.189A1.75 1.75 0 0012 8.25v-5.5A1.75 1.75 0 0010.25 1h-8.5zM14.5 4.75a.25.25 0 00-.25-.25h-.5a.75.75 0 110-1.5h.5c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0114.25 12H14v1.543a1.457 1.457 0 01-2.487 1.03L9.22 12.28a.75.75 0 111.06-1.06l2.22 2.22v-2.19a.75.75 0 01.75-.75h1a.25.25 0 00.25-.25v-5.5z"/>',
        "label" : {
            "en" : "Pull Request Reviews",
            "it" : "Revisioni di Richieste di Pull",
            "de" : "Überprüfungen von Pull Requests",
            "pt" : "Avaliação de Pull Requests",
            "id" : "Ulasan Pull Request",
            "hi" : "अनुरोध समीक्षा",
            "fr" : "Révision de Pull Request",
            "ru": "Ревьювы пулл реквестов",
            "es" : "Revisiones de Pull Requests",
            "pl" : "Recenzje Pull Requestów"
        }
    },

    "contribTo" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M1 2.5A2.5 2.5 0 013.5 0h8.75a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0V1.5h-8a1 1 0 00-1 1v6.708A2.492 2.492 0 013.5 9h3.25a.75.75 0 010 1.5H3.5a1 1 0 100 2h5.75a.75.75 0 010 1.5H3.5A2.5 2.5 0 011 11.5v-9zm13.23 7.79a.75.75 0 001.06-1.06l-2.505-2.505a.75.75 0 00-1.06 0L9.22 9.229a.75.75 0 001.06 1.061l1.225-1.224v6.184a.75.75 0 001.5 0V9.066l1.224 1.224z"/>',
        "label" : {
            "en" : "Contributed To",
            "it" : "Contribuito A",
            "de" : "Beigetragen Zu",
            "pt" : "Contribuiu Para",
            "id" : "Berkontribusi Ke",
            "hi" : "योगदान",
            "fr" : "Contribué à",
            "ru" : "Участие в",
            "es" : "Contribuido a",
            "pl" : "Kontrybuował Do"
        }
    },

    "private" : {
        "icon" : '<path fill="{0}" fill-rule="evenodd" d="M4 4v2h-.25A1.75 1.75 0 002 7.75v5.5c0 .966.784 1.75 1.75 1.75h8.5A1.75 1.75 0 0014 13.25v-5.5A1.75 1.75 0 0012.25 6H12V4a4 4 0 10-8 0zm6.5 2V4a2.5 2.5 0 00-5 0v2h5zM12 7.5h.25a.25.25 0 01.25.25v5.5a.25.25 0 01-.25.25h-8.5a.25.25 0 01-.25-.25v-5.5a.25.25 0 01.25-.25H12z"/>',
        "label" : {
            "en" : "Private Contributions",
            "it" : "Contributi Privati",
            "de" : "Private Beiträge",
            "pt" : "Contribuições Privadas",
            "id" : "Kontribusi Pribadi",
            "hi" : "गुप्त योगदान",
            "fr" : "Contributions privées",
            "ru" : "Частное участие",
            "es" : "Contribuciones privadas",
            "pl" : "Prywatne Kontrybucje"
        }
    }
}
