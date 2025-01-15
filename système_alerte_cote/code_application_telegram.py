from telethon import TelegramClient, events
import re

# Remplacez par vos identifiants donné aprés création de l'application telegram
api_id = ''
api_hash = ''
supergroupe_nom = "" #remplacez par le nom du groupe ou se trouve le bot @grosse_cbot

# Thread principal
async def main():
    # Crée une instance du client Telegram
    client = TelegramClient('session_automatisation', api_id, api_hash)

    # se connecte au client
    await client.start()
    print(f"Connecté à Telegram. En attente de messages dans le supergroupe {supergroupe_nom}...")

    # Gère les nouveaux messages
    @client.on(events.NewMessage)
    async def handle_new_message(event):
        chat = await event.get_chat()
        if chat.title == supergroupe_nom:
            message = event.message.message
            match = re.search(r'💡(.*?)\n', message) #extrait la cote en string du message recu
            
            if match:
                extracted_text = match.group(1).strip()  # Supprime les espaces autour du texte extrait
                print(f"Texte extrait : {extracted_text}")
                
                # Appele la fonction de prise de pari, avec l'intitulé de la cote
                print(f"prise de la cote {extracted_text}")
                #placer_pari(extracted_text) indenté car ce code présente uniquement la partie alerte de sortie d'une cote boostée
                
            else:
                print("Pas de texte à extraire dans ce message.")
            

    # Lance l'écoute en continu
    await client.run_until_disconnected()

# Main
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
