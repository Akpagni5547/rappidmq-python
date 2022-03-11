import json
import pika
import sys

url = 'amqps://iboylxcs:fIAbJWpKY4o88ybFOfr3gMRgs6_XJ0Ro@chimpanzee.rmq.cloudamqp.com/iboylxcs'
params = pika.URLParameters(url)

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='amq.direct', exchange_type='direct', durable=True)

keyQueue = "elastic-search"

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
channel.basic_publish(
    exchange='amq.direct', routing_key=keyQueue, body=message_dump)
print(f" [x] Sent {message_dump}")
connection.close()
