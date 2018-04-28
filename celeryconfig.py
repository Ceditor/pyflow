from kombu.serialization import registry

broker_url = 'redis://127.0.0.1:6379'
task_serializer = 'msgpack'
imports = ["utils"]
accept_content = ['msgpack', 'application/x-msgpack']
registry.enable('msgpack')
registry.enable('application/x-msgpack')
