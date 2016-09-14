from redis.sentinel import Sentinel
from sockjs.tornado import SockJSConnection
from chat_app.models import Messages, Credential


class SocketHandler(SockJSConnection):
    client_sock = {}
    sent = Sentinel([('127.0.0.1', 17777)], socket_timeout=0.1)
    data_base = sent.master_for('mymaster', socket_timeout=0.1)

    def on_open(self, request):
        print('socket open')

    def on_close(self):
        print('socket close')

    def on_message(self, message):
        message_array = message.split(':')
        if message_array[0] == 'name':
            SocketHandler.client_sock[message_array[1]] = self
            messages = Messages.objects.filter(id_receiver__login=message_array[1])
            for mes in messages:
                user = Credential.objects.filter(id=mes.id_sender_id).first()
                output = user.login + ':' + mes.message
                self.send(output)
            broadcast_messages = SocketHandler.data_base.lrange('broadcast', 0, -1)
            for br_mes in broadcast_messages:
                output = 'broadcast:' + str(br_mes)
                self.send(output)
        elif message_array[0] == 'list_active':
            print('list_active')
            output = 'list_active:'
            for key in SocketHandler.client_sock.keys():
                output += key + '\n'
            self.send(output)
        elif message_array[0] == 'list_all':
            print('list_all')
            output = 'list_all:'
            users = Credential.objects.all()
            for user in users:
                output += user.login + '\n'
            self.send(output)
        elif message_array[0] == 'broadcast':
            SocketHandler.data_base.lpush('broadcast', message_array[1])
            output_message = message_array[0] + ':' + message_array[1]
            for client in SocketHandler.client_sock.values():
                client.send(output_message)
        else:
            receiver_name = message_array[0]
            sender_name = None
            for name,sock in SocketHandler.client_sock.items():
                if sock == self:
                    sender_name = name
                    break
            output_message = sender_name + ':' + message_array[1]
            if receiver_name in SocketHandler.client_sock.keys():
                SocketHandler.client_sock[receiver_name].send(output_message)
            else:
                credential_sender = Credential.objects.filter(login=sender_name).first()
                credential_receiver = Credential.objects.filter(login=receiver_name).first()
                mes = Messages(id_sender=credential_sender, id_receiver=credential_receiver, message=message_array[1])
                mes.save()
