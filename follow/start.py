from atproto import Client

# Este código segue TODOS que comentaram em alguma postagem
# Configura e autentica o cliente
client = Client(base_url='https://bsky.social')
profile = client.login('SEU_EMAIL', 'SUA_SENHA')


# Obtém o thread de um post específico colocar o did logo após o att:// e colocar o id do post no final (vc consegue esse id no link do post)
res = client.get_post_thread(uri='at://did:plc:2rjdcvh2znplhwwoijelhxxs/app.bsky.feed.post/3l3tzg2jj572k')

thread = res.thread

# Cria uma lista para armazenar os dids
dids = []


def extract_dids(item):
    # Verifica se o item é um objeto com os atributos esperados
    if hasattr(item, 'post') and hasattr(item.post, 'author') and hasattr(item.post.author, 'did'):
        did = item.post.author.did
        dids.append(did)

    # Verifica se o item tem replies e itera sobre eles
    if hasattr(item, 'replies') and item.replies:
        for reply in item.replies:
            extract_dids(reply)


# Trata o caso onde `thread` é um objeto e não uma lista
extract_dids(thread)

# Imprime a lista de dids
print("DIDs encontrados:", dids)

myUser_follows_response = client.get_follows(actor=profile.did, limit=100)
myUser_follows_dids = set(follow.did for follow in myUser_follows_response.follows)

dids_not_in_myFollows = [did for did in dids if did not in myUser_follows_dids]

# Imprime a lista de DIDs que não estão sendo seguidos
print("DIDs não encontrados nos meus follows:", dids_not_in_myFollows)

# Segue cada DID que ainda não está sendo seguido
for did in dids_not_in_myFollows:
    try:
        follow_response = client.follow(did)
        print(f"Seguindo {did}: {follow_response.uri}")
    except Exception as e:
        print(f"Erro ao seguir {did}: {e}")