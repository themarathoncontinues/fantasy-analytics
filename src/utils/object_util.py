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
        """get id"""
        return self.get("id")

    @property
    def roster(self):
        """get roster"""
        return self.get("roster")

    @property
    def entries(self):
        """get roster.entries"""
        roster = self.roster
        return roster["entries"] if roster else None


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
        """get playerId"""
        return self.get("playerId", None) if self else None

    @property
    def player_pool_entry(self):
        """get playerPoolEntry"""
        return self.get("playerPoolEntry", None) if self else None

    @property
    def player(self):
        """get playerPoolEntry.player"""
        ppe = self.player_pool_entry
        return ppe.get("player", None) if ppe else None

    @property
    def full_name(self):
        """get playerPoolEntry.player.fullName"""
        player = self.player
        return player.get("fullName") if player else None

    @property
    def stats(self):
        """get playerPoolEntry.player.stats"""
        player = self.player
        return player.get("stats", None) if player else None


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
        """get abbrev"""
        return self.get("abbrev", None) if self else None

    @property
    def primary_owner(self):
        """get primaryOwner"""
        return self.get("primaryOwner", None) if self else None

    @property
    def nick_name(self):
        """get nickname"""
        return self.get("nickname", None) if self else None

    @property
    def values_by_stat(self):
        """get valuesByStat"""
        return self.get("valuesByStat", None) if self else None

    @property
    def record(self):
        """get record"""
        return self.get("record") if self else None

    @property
    def overall(self):
        """get record.overall"""
        record = self.record
        return record.get("overall", None) if record else None

    @property
    def wins(self):
        """get record.overall.wins"""
        overall = self.overall
        return overall.get("wins", None) if overall else None

    @property
    def losses(self):
        """get record.overall.losses"""
        overall = self.overall
        return overall.get("losses", None) if overall else None

    @property
    def ties(self):
        """get record.overall.ties"""
        overall = self.overall
        return overall.get("ties", None) if overall else None
