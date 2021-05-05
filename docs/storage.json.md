# storage.json
mainly for storaging user information such as the private key.

## Format
The base format looks following<br>
<br>
```json
{
    "DISCORD_USER_ID": {
        "key": "STARFILES_PRIVATE_KEY",
        "page": 0
    }
}
```

### page
Why? It's mainly used in [listing.py](https://github.com/CrafterPika/starfiles-bot/blob/master/events/listing.py)<br>
It's responsible for possibility of having infinte pages.<br>

#### Infinite pages
What do i mean by "Infinite pages"?<br>
Well i mean in [listing.py](https://github.com/CrafterPika/starfiles-bot/blob/master/events/listing.py) the arrow actions (mainly "⬅️" and "➡️")
if you press "➡️" the page 0 value get's [calculated](https://github.com/CrafterPika/starfiles-bot/blob/master/events/listing.py#L100) up by 1. (+1 calculation)
so format will look like:<br>
```json
{
    "DISCORD_USER_ID": {
        "key": "STARFILES_PRIVATE_KEY",
        "page": 1
    }
}
```
This number is then used as init to parse the json for the index result [listing.py](https://github.com/CrafterPika/starfiles-bot/blob/master/events/listing.py#L108-L111) example
<br>
<br>
Yes i know it's not the greatest method but it works :)<br>
So lets imagine someone did "➡️" Twice. The Page value is <code>"page": 2</code>
<br>
If he now presses "⬅️" it get calculated down by one so the page value will change back to <code>"page": 1</code> (-1 calculation)

#### Reset on command start
Maybe you noticed i allway reset in [listing.py](https://github.com/CrafterPika/starfiles-bot/blob/master/events/listing.py#L22-L28) the page value to 0 on executing one of those command.<br>
The reason i do it is to prevent fuck ups with value results as starfiles api uses <code>name[0]</code> to parse json and the number out of the index is not a great thing and would result in one command to fuck up if that occurs
