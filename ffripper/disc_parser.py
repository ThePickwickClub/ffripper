#   ffripper-1.0 - Audio-CD ripper.
#   Copyright 2020-2021 Stefan Garlonta
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; version 3 of the License.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#   USA
#
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; version 3 of the License.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#   USA
#

from ffripper.cd_info_parser import CdInfoParser
from ffripper.track_info import TrackInfo
from ffripper.errors import Reason, RipperError
from ffripper.cdrom_info_object import CDInfo


class CdDiscParser(CdInfoParser):

    def __init__(self, dictionary):
        self.dict = dictionary
        self.disc_id = self.dict['disc']['id']

    def get_disc_info(self):
        try:
            album = self.parse_for_album()
            artist = self.parse_for_artist()
            tracks = self.parse_for_tracks()
        except:
            raise RipperError(Reason.UNKNOWNERROR, "An unknown Error occurred while Parsing")
        return CDInfo(album, artist, tracks)

    def parse_for_album(self):
        album = self.dict["disc"]["release-list"][0]["title"]
        return album

    def parse_for_artist(self):
        artist = self.dict["disc"]["release-list"][0]["artist-credit"][0]["artist"]["name"]
        return artist

    def parse_for_tracks(self):
        tracks = []
        try:
            for i in range(len(self.dict['disc']['release-list'][0]['medium-list'])):
                if 0 < len(self.dict['disc']['release-list'][0]['medium-list'][i]['disc-list']):
                    for f in range(len(self.dict['disc']['release-list'][0]['medium-list'][i]['disc-list'])):
                        if self.dict['disc']['release-list'][0]['medium-list'][i]['disc-list'][f]['id'] == self.disc_id:
                            for j in range(len(self.dict['disc']['release-list'][0]['medium-list'][i]['track-list'])):
                                tracks.append(
                                    TrackInfo(self.dict['disc']['release-list'][0]['medium-list'][i]['track-list'][j]
                                              ['recording']["title"],
                                              self.dict['disc']['release-list'][0]['medium-list'][i]['track-list'][j][
                                                  'length'],
                                              None, self.dict['disc']['release-list'][0]['medium-list'][i]['track-list']
                                              [j]['recording']['artist-credit'][0]['artist']['name']))
        except IndexError:
            for i in range(0, len(self.dict['disc']['release-list'][0]['medium-list'][0]['track-list'])):
                tracks.append(
                    TrackInfo(self.dict['disc']['release-list'][0]['medium-list'][0]['track-list'][i]['recording'][
                                  "title"],
                              self.dict['disc']['release-list'][0]['medium-list'][0]['track-list'][i]['length'],
                              None, None))
        return tracks