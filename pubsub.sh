gcloud pubsub topics create db-transaction-topic
gcloud pubsub subscriptions create db-sub --topic db-transaction-topic