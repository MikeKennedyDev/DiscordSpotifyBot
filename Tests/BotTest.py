import main


class TestMessage:
    guild = "MikeKenndy's test server"
    channel = 'general'
    content = ''


# playlist_url = message.content.split()[1]

PlaylistId = 'test_id'


# <
# Message id=1040713672030441482
# channel=<TextChannel id=835148037126619179 name='general' position=0 nsfw=False news=False category_id=835148037126619177>
# type=<MessageType.default: 0>
# author=<Member id=304434847764578308 name='MikeKenndy' discriminator='7857' bot=False nick=None
# guild=<Guild id=835148037126619176 name="MikeKenndy's test server" shard_id=0 chunked=True member_count=2>>
# flags=<MessageFlags value=0>>


def GetHelpMessageTest():
    print('Getting help message.')
    message = main.GetHelpMessage(TestMessage)
    assert message is not None


def MapPlaylistTest():
    print('Testing map playlist')
    TestMessage.content = '/AddPlaylist https://open.spotify.com/playlist/2UmDYQxgIDaKikeG53Ffd5?si=2c5b253d321b4db4'
    result = main.MapNewPlaylist(TestMessage)
    assert result == 'Playlist linked to current channel.' or result == 'Playlist already mapped to current channel.'


def RemoveMappedPlaylistTest():
    print('Testing remove playlist')
    TestMessage.content = '/AddPlaylist https://open.spotify.com/playlist/2UmDYQxgIDaKikeG53Ffd5?si=2c5b253d321b4db4'
    result = main.RemoveMappedPlaylist(TestMessage)
    assert result == 'Playlist unlinked from current channel.'


if __name__ == '__main__':
    print('Testing PlaylistMaintainer functions')

    GetHelpMessageTest()
    MapPlaylistTest()
    RemoveMappedPlaylistTest()
