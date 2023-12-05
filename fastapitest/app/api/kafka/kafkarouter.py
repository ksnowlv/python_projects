
from fastapi import APIRouter
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException

router = APIRouter(
    prefix="/kafka",
    tags=["kafka测试接口"],
    responses={404: {"description": "Not found"}},
)

# CONSUMER_GROUP_ID = "my_consumer_group"  # 自定义消费者组 ID
#
# # Kafka 服务器配置
# kafka_conf = {
#     'bootstrap.servers': 'localhost:9092',
#     'group.id': CONSUMER_GROUP_ID  # 添加消费者组 ID
# }
#
# producer = None
# consumer = None
#
# def init_kafka():
#     return
#     global producer
#     global consumer
#     # 创建 Kafka 生产者
#     producer = Producer(kafka_conf)
#
#     # 创建 Kafka 消费者
#     consumer = Consumer(kafka_conf)
#
#
# @router.post("/send_message/{topic}")
# def send_message(topic: str, message: str):
#     producer.produce(topic, value=message)
#     producer.flush()
#     return {"message": f"Message sent to Kafka topic：{topic}"}
#
# @router.get("/consume_messages/{topic}")
# def consume_messages(topic: str):
#     consumer.subscribe([topic])
#
#     while True:
#         msg = consumer.poll(1.0)
#         print(f"msg = {msg}")
#         if msg is None:
#             continue
#         if msg.error():
#             if msg.error().code() == KafkaError._PARTITION_EOF:
#                 print(f"KafkaError._PARTITION_EOF")
#                 continue
#             else:
#                 raise KafkaException(msg.error())
#         value = msg.value().decode("utf-8")
#         consumer.commit()
#         return {f"consume topic: {topic} message": value}
