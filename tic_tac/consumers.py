from channels.generic.websocket import AsyncJsonWebsocketConsumer
import contextlib
import random
from .helpers import check_win, is_draw

class TicTacConsumer(AsyncJsonWebsocketConsumer):

    board = {i: '' for i in range(320)}

    async def connect(self):
        print(self.scope['url_route']['kwargs']['id'])
        self.room_id = self.scope['url_route']['kwargs']['id']
        self.group_name = f"group_{self.room_id}"

        with contextlib.suppress(KeyError):
            if len(self.channel_layer.groups[self.group_name]) >= 2:
                await self.accept()
                await self.send_json({
                    "event": "show_error",
                    "error": "Room is full"
                })
                return await self.close(1)

        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        if len(self.channel_layer.groups[self.group_name]) == 2:
            tmp_group = list(self.channel_layer.groups[self.group_name])
            first_player = random.choice(tmp_group)
            tmp_group.remove(first_player)
            final_group = [first_player, tmp_group[0]]
            for i, channel_name in enumerate(final_group):
                await self.channel_layer.send(channel_name, {
                    "type": "game_data.send",
                    "data": {
                        "event": "game_start",
                        "board": self.board,
                        "myTurn": True if i == 0 else False
                    }
                })



    async def receive_json(self, content, **kwargs):
        print(content)
        if content['event'] == "board_data_send":
            self.clicked_key = content.get('clickedKey')
            self.letter = content.get('letter')
            self.score, board = check_win(content['board'], self.clicked_key, self.letter)
            if self.score > 0:
                return await self.channel_layer.group_send(self.group_name, {
                    "type": "game_data_send",
                    "data": {
                        "event": "won",
                        "board": board,
                        "winner": self.letter,
                        "myTurn": False,
                    }
                })
            elif is_draw(content['board']):
                return await self.channel_layer.group_send(self.group_name, {
                    "type": "game_data_send",
                    "data": {
                        "event": "draw",
                        "board": content['board'],
                        "myTurn": False,
                    }
                })
            else:

                for channel_name in self.channel_layer.groups[self.group_name]:
                    await self.channel_layer.send(channel_name, {
                        "type": "game_data_send",
                        "data": {
                            "event": "board_data_send",
                            "board": board,
                            "myTurn": False if self.channel_name == channel_name else True
                        }
                    })

        elif content['event'] == "restart":
            if len(self.channel_layer.groups[self.group_name]) == 2:
                tmp_group = list(self.channel_layer.groups[self.group_name])
                first_player = random.choice(tmp_group)
                tmp_group.remove(first_player)
                final_group = [first_player, tmp_group[0]]
                for i, channel_name in enumerate(final_group):
                    await self.channel_layer.send(channel_name, {
                        "type": "game_data_send",
                        "data": {
                            "event": "game_start",
                            "board": self.board,
                            "myTurn": True if i == 0 else False
                        }
                    })
    async def disconnect(self, code):
        if code == 1:
            return
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_send(self.group_name, {
            "type": "game_data_send",
            "data": {
                "event": "opponent_left",
                "board": self.board,
                "myTurn": False,
            }
        })

    async def game_data_send(self, context):
        await self.send_json(context['data'])