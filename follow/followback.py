from atproto import Client

# Este código segue TODOS que te seguem

# Configura e autentica o cliente
client = Client(base_url='https://bsky.social')
# Recupera o perfil através do login
profile = client.login('SEU_EMAIL', 'SUA_SENHA')

cursor = None
currentLimit = 100
loop = profile.followers_count / currentLimit
i = 0

while i < loop:
    myFollowers = client.get_followers(actor=profile.did, cursor=cursor, limit=currentLimit)
    cursor = myFollowers.cursor

    for follower in myFollowers.followers:
        if follower.viewer.following is None:
            try:
                follow_response = client.follow(follower.did)
                print(f"Seguindo {follower.handle}: {follow_response.uri}")
            except Exception as e:
                print(f"Erro ao seguir {follower.handle}: {e}")
    i = i + 1
