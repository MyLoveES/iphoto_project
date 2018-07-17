import json

from pykafka import KafkaClient
from pykafka.common import OffsetType


class KafkaTest(object):
    def __init__(self, host="106.15.191.61:9092"):
        self.host = host
        self.client = KafkaClient(hosts=self.host)

    def simple_consumer(self, offset=0):
        """
        消费者指定消费
        :param offset:
        :return:
        """

        topic = self.client.topics["iphoto_log".encode()]
        partitions = topic.partitions
        last_offset = topic.latest_available_offsets()
        print("最近可用offset {}".format(last_offset))  # 查看所有分区
        consumer = topic.get_simple_consumer(b"simple_consumer_group", partitions=[partitions[0]])  # 选择一个分区进行消费
        offset_list = consumer.held_offsets
        print("当前消费者分区offset情况{}".format(offset_list))  # 消费者拥有的分区offset的情况
        consumer.reset_offsets([(partitions[0], offset)])  # 设置offset
        msg = consumer.consume()
        print("消费 :{}".format(msg.value.decode()))
        msg = consumer.consume()
        print("消费 :{}".format(msg.value.decode()))
        msg = consumer.consume()
        print("消费 :{}".format(msg.value.decode()))
        offset = consumer.held_offsets
        print("当前消费者分区offset情况{}".format(offset)) # 3

    def balance_consumer(self, offset=0):
        """
        使用balance consumer去消费kafka
        :return:
        """
        topic = self.client.topics["entity".encode()]
        consumer = topic.get_balanced_consumer(
            consumer_group= b'entity',
            auto_offset_reset=OffsetType.LATEST,  # 在consumer_group存在的情况下，设置此变量，表示从最新的开始取
            # auto_offset_reset=OffsetType.EARLIEST,
            # reset_offset_on_start=True,
            auto_commit_enable=True,
            managed=True
        )
        # self.consumer = topic.get_simple_consumer(reset_offset_on_start=False)

        # managed=True 设置后，使用新式reblance分区方法，不需要使用zk，而False是通过zk来实现reblance的需要使用zk
        # consumer = topic.get_balanced_consumer(b"entity_detection", auto_commit_enable = True, managed=True)
        while True:
            msg = consumer.consume()
            consumer.commit_offsets()
            offset = consumer.held_offsets
            print("当前消费者分区offset情况{}".format(offset))
            if msg is None:
                print("GG")
            else:
                print("OK")
            offset = consumer.held_offsets
            print("{}, 当前消费者分区offset情况{}".format(msg.value.decode('unicode_escape'), offset))


if __name__ == '__main__':
    kafka_ins = KafkaTest()
    # kafka_ins.simple_consumer()
    kafka_ins.balance_consumer()
    # client = KafkaClient(hosts="106.15.191.61:9092")
    # topic = client.topics['entity_detection'.encode()]
    # consumer = topic.get_balanced_consumer(b"entity_detection", managed=True)
    # print("Topic:", consumer.topic)
    # while True:
    #     try:
    #         msg = consumer.consume()
    #         value = msg.value.decode('unicode_escape')
    #         value = json.loads(value)
    #         offset = consumer.held_offsets
    #         print("{}, 当前消费者分区offset情况{}".format(value, offset))
    #         token = value['token']
    #         user = value['user']
    #         photo = value['photo']
    #         photo_path = value['photo_filepath']
    #
    #         if token != 'detection':
    #             print("Wrong request")
    #             continue

            # img = request.urlopen(photo_path)
            # image = Image.open(img)
            # entities = yolo.detect_image(image)
            # print("entities:", entities)
            # data = {}
            # person_list = []
            # transport_list = []
            # animal_list = []
            # office_list = []
            # sport_list = []
            # gourmet_list = []
            # furniture_list = []
            # for entity in entities:
            #     print("entity is:", entity)
            #     if entity in person:
            #         print("person add")
            #         person_list.append(entity)
            #     elif entity in transport:
            #         print("transport add")
            #         transport_list.append(entity)
            #     elif entity in animal:
            #         print("animal add")
            #         animal_list.append(entity)
            #     elif entity in office:
            #         print("office add")
            #         office_list.append(entity)
            #     elif office_list in sport:
            #         print("sport add")
            #         sport_list.append(entity)
            #     elif entity in gourmet:
            #         print("gourmet add")
            #         gourmet_list.append(entity)
            #     elif entity in furniture:
            #         print("furniture add")
            #         furniture_list.append(entity)
            # data = {
            #     "token": "detection",
            #     "photo": photo,
            #     "category_data": {
            #         "person": person_list,
            #         "transport": transport_list,
            #         "animal": animal_list,
            #         "office": office_list,
            #         "sport": sport_list,
            #         "gourmet": gourmet_list,
            #         "furniture": furniture_list
            #     }
            # }
            # print('data:', data)
            # data = json.dumps(data)
            # data = bytes(data, 'utf8')
            # headers = {
            #     'Content-Type': 'application/json',
            #     'Authorization': "JWT " + TOKEN
            # }
            # req = request.Request(url=SERVER_URL + "/photoentity/",
            #                       data=data,
            #                       headers=headers,
            #                       method='POST')
            # page = request.urlopen(req)
            # print("OK")
            # # r_image.show()
        # except Exception as e:
        #     print('Error! Try again:', e.args)
        #     continue