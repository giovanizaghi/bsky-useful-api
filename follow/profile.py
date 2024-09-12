from atproto import Client

# Configura e autentica o cliente
client = Client(base_url='https://bsky.social')
client.login('SEU_EMAIL', 'SUA_SENHA')
i = 0
while i < 20:

    user1_followers_response = client.get_followers(actor='did:plc:2rjdcvh2znplhwwoijelhxxs', limit=100)
    user2_followers_response = client.get_follows(actor='did:plc:bujpi4u6bwu5b3ltiktxsijw', limit=100)

    # Extraí os DIDs dos seguidores de user1 e user2
    user1_followers_dids = set(follower.did for follower in user1_followers_response.followers)
    user2_followers_dids = set(follow.did for follow in user2_followers_response.follows)

    # Determine quais seguidores de user1 não estão em user2
    user1_not_in_user2 = user1_followers_dids - user2_followers_dids

    # Converta o resultado para uma lista e imprima
    user1_not_in_user2_list = list(user1_not_in_user2)

    for did in user1_not_in_user2_list:
        try:
            follow_response = client.follow(did)
            print(f"Seguindo {did}: {follow_response.uri}")
        except Exception as e:
            print(f"Erro ao seguir {did}: {e}")

    i += 1
