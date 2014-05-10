from models import RSAClient

client1 = RSAClient(2**12)
print(client1.get_n())
client2 = RSAClient(2**15)
print(client2.get_n())

message = client2.generate_message(client1.get_public_key(), client1.get_n())
message = client1.receive_message(message)
print(message)