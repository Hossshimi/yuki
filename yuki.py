

from mastodon import Mastodon

def login():
    mastodon = Mastodon(
        client_id="yuki_key.txt",
        access_token="yuki_secret_token.txt",
        api_base_url = "https://kawaiuniv.work"
    )
    return mastodon

