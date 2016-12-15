from sklearn.base import BaseEstimator, TransformerMixin
import datetime
class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


class ColumnSelector(TransformerMixin):

    def __init__(self, column):
        self.column = column

    def fit(self, x, y=None):
        return self

    def transform(self, data_frame):
       return data_frame[[self.column]]

class LengthSelector(BaseEstimator, TransformerMixin):

    def fit(self, x, y=None):
        return self

    def transform(self, links):
        return [{'length': len(text)} for text in links['text']]

class DateSelector(BaseEstimator, TransformerMixin):

    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, tweets):
        dates = []
        for date in tweets[self.key]:
            strip = datetime.datetime.strptime(date, '%a %b %d %H:%M:%S PDT %Y')
            dates.append({'day': strip.weekday(), 'hour': strip.hour, 'month': strip.month})
        return dates

class KeywordSelector(BaseEstimator, TransformerMixin):

    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, tweets):
        keywords = \
            [('hasAddict',     (' addict',)), \
             ('hasAwesome',    ('awesome',)), \
             ('hasBroken',     ('broke',)), \
             ('hasBad',        (' bad',)), \
             ('hasBug',        (' bug',)), \
             ('hasCant',       ('cant','can\'t')), \
             ('hasCrash',      ('crash',)), \
             ('hasCool',       ('cool',)), \
             ('hasDifficult',  ('difficult',)), \
             ('hasDisaster',   ('disaster',)), \
             ('hasDown',       (' down',)), \
             ('hasDont',       ('dont','don\'t','do not','does not','doesn\'t')), \
             ('hasEasy',       (' easy',)), \
             ('hasExclaim',    ('!',)), \
             ('hasExcite',     (' excite',)), \
             ('hasExpense',    ('expense','expensive')), \
             ('hasFail',       (' fail',)), \
             ('hasFast',       (' fast',)), \
             ('hasFix',        (' fix',)), \
             ('hasFree',       (' free',)), \
             ('hasFrowny',     (':(', '):')), \
             ('hasFuck',       ('fuck',)), \
             ('hasGood',       ('good','great')), \
             ('hasHappy',      (' happy',' happi')), \
             ('hasHate',       ('hate',)), \
             ('hasHeart',      ('heart', '<3')), \
             ('hasIssue',      (' issue',)), \
             ('hasIncredible', ('incredible',)), \
             ('hasInterest',   ('interest',)), \
             ('hasLike',       (' like',)), \
             ('hasLol',        (' lol',)), \
             ('hasLove',       ('love','loving')), \
             ('hasLose',       (' lose',)), \
             ('hasNeat',       ('neat',)), \
             ('hasNever',      (' never',)), \
             ('hasNice',       (' nice',)), \
             ('hasPoor',       ('poor',)), \
             ('hasPerfect',    ('perfect',)), \
             ('hasPlease',     ('please',)), \
             ('hasSerious',    ('serious',)), \
             ('hasShit',       ('shit',)), \
             ('hasSlow',       (' slow',)), \
             ('hasSmiley',     (':)', ':D', '(:')), \
             ('hasSuck',       ('suck',)), \
             ('hasTerrible',   ('terrible',)), \
             ('hasThanks',     ('thank',)), \
             ('hasTrouble',    ('trouble',)), \
             ('hasUnhappy',    ('unhapp',)), \
             ('hasWin',        (' win ','winner','winning')), \
             ('hasWinky',      (';)',)), \
             ('hasWow',        ('wow','omg')) ]
        keywordFeatures = []
        for tweet in tweets[self.key]:
            keywordDict = {}
            for keyword in keywords:
                key = keyword[0]
                keywordDict[key] = False
                for word in keyword[1]:
                    keywordDict[key] = keywordDict[key] or (tweet.lower().find(word) != -1)
            keywordFeatures.append(keywordDict)
        return keywordFeatures

