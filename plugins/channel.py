from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file

media_filter = filters.document | filters.video | filters.audio


@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Media Handler"""
    media = None # Initialize media
    file_type = None # Initialize file_type
    
    # 1. Loop through all types
    for ft in ("document", "video", "audio"):
        # Use a temporary variable for the loop, or reset media
        media_temp = getattr(message, ft, None) 
        if media_temp is not None:
            media = media_temp # Assign final media object
            file_type = ft       # Assign final file type
            break # Exit the loop once media is found
            
    # 2. Check AFTER the loop if media was found
    if media is None:
        # If the loop finished and no media was found, exit
        return
        
    # 3. If media was found, proceed with saving
    media.file_type = file_type # This line is now safe
    media.caption = message.caption
    await save_file(media)
