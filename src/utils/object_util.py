"""Object Utils"""


class RosterAccess(dict):
    def __init__(self, data: dict):
        """
        Create facade object of mRoster endpoint returns
        Args:
            data: dict response object

        Returns:
            super dict object with accesses
        """
        super(RosterAccess, self).__init__(data)

    @property
    def team_id(self):
        return self['id']

    @property
    def roster(self):
        return self['roster']

    @property
    def entries(self):
        roster = self.roster
        return roster['entries'] if roster else None


class RosterEntryAccess(dict):
    def __init__(self, data: dict):
        """
        Create facade object of mRoster endpoint 'entries' key
        Args:
            data: 'entries' key of mRoster response object

        Returns:
            super dict object with accesses
        """
        super(RosterEntryAccess, self).__init__(data)

    @property
    def player_id(self):
        return self.get('playerId', None) if self else None

    @property
    def player_pool_entry(self):
        return self.get('playerPoolEntry', None) if self else None

    @property
    def player(self):
        player_pool_entry = self.player_pool_entry
        return player_pool_entry.get('player', None) if player_pool_entry else None

    @property
    def full_name(self):
        player = self.player
        return player.get('fullName') if player else None

    @property
    def stats(self):
        player = self.player
        return player.get('stats', None) if player else None


class TeamMetaAccess(dict):
    def __init__(self, data: dict):
        """
        Create facade object of mTeam endpoint "team_id" key
        Args:
            data: specific team_id key of mTeam response object

        Returns:
            super dict object with accesses
        """
        super(TeamMetaAccess, self).__init__(data)

    @property
    def abbrev(self):
        return self.get('abbrev', None) if self else None

    @property
    def primary_owner(self):
        return self.get('primaryOwner', None) if self else None

    @property
    def nick_name(self):
        return self.get('nickname', None) if self else None

    @property
    def values_by_stat(self):
        return self.get('valuesByStat', None) if self else None

    @property
    def record(self):
        return self['record'] if self else None

    @property
    def overall(self):
        record = self.record
        return record.get('overall', None) if record else None

    @property
    def wins(self):
        overall = self.overall
        return overall.get('wins', None) if overall else None

    @property
    def losses(self):
        overall = self.overall
        return overall.get('losses', None) if overall else None

    @property
    def ties(self):
        overall = self.overall
        return overall.get('ties', None) if overall else None
