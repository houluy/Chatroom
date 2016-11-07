# Developing details of Chatroom

### [Gaming]

- self.game: a dict to save the instances of every game this client is playing. 
```
    self.game = {
        'name': {
            'game_name': [game_instance, player_seq],
            'game_name2': [game_instance2, player_seq],
            ...
        }
    }
```


