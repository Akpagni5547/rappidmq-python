import pika, os, logging, json
msg = {
    "_id": "61f40b773b10f06383c6593d",
    "campagne_name": "oeil",
    "partner_name": "gendarme",
    "agence_name": "gagnoa",
    "candidat_genre": "femme",
    "created_by": "helios",
    "history":  "admin",
    "created_at": "2021-03-01T15:55:01.436Z",
    "updated_at": "2022-12-14T15:55:01.436Z",
    "data_examens": [{
                  "name": "Type de Permis de conduire",
                  "exams": [{
                      "label": "Type PC",
                      "value": "PETRG"
                  }]
    }, {
        "name": "Groupe sanguin",
        "exams": [{
            "label": "Groupe",
            "value": "O+"
        },
            {
            "label": "Rhésus",
            "value": "+ (POSITIF)"
        }]
    }, {
        "name": "Décision",
        "exams": [{
            "label": "",
            "value": "Inapte"
        },
            {
            "label": "Condition",
            "value": "Normale"
        }, {
            "label": "Catégorie du permis souhaitée",
            "value": ["A", "B", "C"]
        }, {
            "label": "Catégorie du permis obtenue",
            "value": ["A", "B", "C"]
        }, {
            "label": "Observation",
            "value": "Aucune"
        }]
    }, ],

}

message_dump = json.dumps(msg)
logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqps://iboylxcs:fIAbJWpKY4o88ybFOfr3gMRgs6_XJ0Ro@chimpanzee.rmq.cloudamqp.com/iboylxcs')
params = pika.URLParameters(url)
params.socket_timeout = 5
params.heartbeat = 60
params.blocked_connection_timeout = 3600
"""
    paramètre supplémentaire
    params.client_properties = 0
    params.channel_max = 0
    params.connection_attempts = 5
    params.frame_max = 360
    params.locale = En
    params.ssl_options = None
    params.retry_delay = 25
    params.stack_timeout = 30
    params.socket_timeout = 5
    params.blocked_connection_timeout = 3600
    params.tcp_options = none
    params.heartbeat = 60
    lien pour tous les paramètres et explications :  https://pika.readthedocs.io/en/latest/modules/parameters.html
"""

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.exchange_declare(exchange='amq.direct', exchange_type='direct', durable=True)
channel.queue_declare(queue='elastic', durable=True) # Declare a queue
# send a message

channel.basic_publish(exchange='amq.direct', routing_key='elastic-search', body=message_dump)
print ("[x] Message sent to consumer" + message_dump)
connection.close()