from atproto import Client
# Este código deixa de seguir TODOS que não te seguem de volta

# Configura e autentica o cliente
client = Client(base_url='https://bsky.social')

# Faz login e traz os dados do perfil
profile = client.login('SEU_EMAIL', 'SUA_SENHA')

cursor = None
currentLimit = 100
loop = profile.follows_count / currentLimit
i = 0

while i < loop:
    myFollows = client.get_follows(actor=profile.did, cursor=cursor, limit=currentLimit)
    cursor = myFollows.cursor

    for follow in myFollows.follows:
        if follow.viewer.followed_by is None:
            try:
                # Verificando se a string existe e, em seguida, separando e revertendo a lista
                if isinstance(follow.viewer.following, str) and follow.viewer.following:
                    # Dividindo a string pelo separador '/'
                    parts = follow.viewer.following.split('/')
                    if len(parts) > 0:
                        # Pega o último valor como rkey e o penúltimo como repo
                        rkey = parts[-1]  # Último elemento
                        repo = parts[-3]  # Penúltimo elemento que é o repo (depois do 'app.bsky.graph.follow')
                else:
                    rkey, repo = None, None

                if rkey and repo:
                    client.com.atproto.repo.delete_record(data={
                        'collection': 'app.bsky.graph.follow',
                        'repo': repo,
                        'rkey': rkey
                    })
                    print(f"Deixando de seguir {follow.handle} {follow.display_name}")
            except Exception as e:
                print(f"Erro ao deixar de seguir {follow.display_name}: {e}")
    i = i + 1
