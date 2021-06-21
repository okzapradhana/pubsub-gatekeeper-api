from google.cloud import pubsub_v1


class PubSubClient():
    def __init__(self, project_id, topic_id):
        self.publisher_client = pubsub_v1.PublisherClient()
        self.subscriber_client = pubsub_v1.SubscriberClient()
        self.project_id = project_id
        self.topic_id = topic_id

    def _publish(self, message):
        topic_path = self.publisher_client.topic_path(
            self.project_id, self.topic_id)
        future = self.publisher_client.publish(topic_path, message)
        return future

    def _subscribe(self, callback):
        subscription_path = self.subscriber_client.subscription_path(
            self.project_id, self.topic_id)
        pull = self.subscriber_client.subscribe(
            subscription_path, callback=callback)
        return pull
