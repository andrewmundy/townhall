from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
 
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-db35c7ce-f0de-11e6-8939-02ee2ddab7fe"
pnconfig.publish_key = "pub-c-86d84ec4-ecff-4478-b0d6-e2122e6b28f5"
pnconfig.ssl = True
 
pubnub = PubNub(pnconfig)



# "insert"
def publish_callback(result, status):
	if status.isError:
		pass
pubnub.publish().channel(rep_name).message(message)\
        .should_store(True).use_post(True).async(publish_callback)

# "select"
envelope = pubnub.history().channel(rep_name).reverse(True).sync()
# envelope = {messages: [{timetoken: ---, entry: ---}], start_timetoken: ---, end_timetoken: ---}

# "select" the first message
envelope = pubnub.history().channel(rep_name).reverse(True).count(1).sync()
