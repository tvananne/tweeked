from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import json
import time

""" Oauth Constants - get these from apps.twitter.com (will need to create app if haven't already)"""
CONSUMER_KEY = "ApSJcidYxIegrZo7FiSC8XrB4"								#Consumer Key here
CONSUMER_SECRET = "I8TYKGCA34M2ac8Hyg1CYs47U0Ectg2yPAKzJZJSKwGw3ClDiT"  #Consumer Secret Here
OAUTH_TOKEN = "4583054541-wIOztctSzu7eUXMAvbyK35yFHtOYugArl0ym4cK"		#Access Token Here
OAUTH_TOKEN_SECRET = "Xq6OVoy6rJYEU64oLuHuiy77EpB4h1L8yvNvE8iC7lyVw"	#Access Token Secret Here

#this is used in some functions such as 'get my followers' and 'get my friends'
MY_SCREEN_NAME = "alleycatpython"	#put your screen name (twitter handle without the @)



"""
1) get_oauth - used for oauth token
2) get_limits - gives you information regarding how many 
	API requests you've used vs how many you can use in a certain amount of time
3) get_tweets - returns a certain number of tweets from a twitter account
4) get_retweeters - returns a list of people who have retweeted certain tweets
5) follow_user - follows a user (API limits are not clear, but you will be limited)
6) get_followers - returns YOUR followers (based on MY_SCREEN_NAME constant above) 5k limit currently
7) get_friends - returns accounts YOU follow (based on MY_SCREEN_NAME constant above) 5k limit currently
8) unfollow - unfollows the user 
"""

""" ******************************* FUNCTION DEFINITIONS ******************************"""


""" oauth """
def get_oauth():
	print "****************************  get_oauth ********************************"
	oauth = OAuth1(CONSUMER_KEY,
				client_secret=CONSUMER_SECRET,
				resource_owner_key=OAUTH_TOKEN,
				resource_owner_secret=OAUTH_TOKEN_SECRET)
	print "---------------------------------------------- END get_oauth ----"
	return oauth


def get_limits():
	print "****************************  get_oauth ********************************"
	gl_baseURL = "https://api.twitter.com/1.1/application/rate_limit_status.json?resources=help,users,search,statuses"
	if __name__ == "__main__":
		if not OAUTH_TOKEN:
			print "something went wrong with Authentication"
		else:
			oauth = get_oauth()
			gl_r = requests.get(url=gl_baseURL, auth=oauth)
			gl_temp_json = json.dumps(gl_r.json(), indent=4, sort_keys=True)	#pretty JSON
			gl_decoded = json.loads(gl_temp_json)								#JSON that can be subsetted
			
			print "gl_temp_json - this is how you print pretty JSON - human readable"
			print gl_temp_json
			
			print "gl_decoded - this is the JSON that you can subset on"
			print gl_decoded
			
			print "these are various examples of how you can subset the response"
			print gl_decoded["resources"]["statuses"]["/statuses/retweeters/ids"]
			print gl_decoded["resources"]["statuses"]["/statuses/retweeters/ids"]["remaining"]
			print gl_decoded["resources"]["statuses"]["/statuses/retweeters/ids"]["reset"]
			print ""
			print gl_decoded["resources"]["users"]["/users/search"]
			print gl_decoded["resources"]["users"]["/users/search"]["limit"]
			print gl_decoded["resources"]["users"]["/users/search"]["remaining"]
			print "The large numbers are time stamps"
			
			#choose what you want to return. I like to return all of this so I can subset what I want later
			return gl_decoded
			

""" I get 180 per 15 min here (12 per minute)"""
def get_tweets(name, count):
	print "****************************  get_tweets ********************************"
	baseURL = "https://api.twitter.com/1.1/statuses/user_timeline.json"
	#these will eventually need try catches or some validation that they are the right type
	URL_screen_name = "screen_name=" + name
	URL_tweet_count = "count=" + count		#count actually needs to be a string. ex "3"
	fullURL = baseURL + '?' + URL_screen_name + '&' + URL_tweet_count
	print fullURL #debug and dev
	
	if __name__ == "__main__":
		if not OAUTH_TOKEN:
			print "something went wrong with Authentication"
		else:
			oauth = get_oauth()
			r = requests.get(url=fullURL, auth=oauth)
			temp_json = json.dumps(r.json(), indent=4, sort_keys=True)
			decoded = json.loads(temp_json)
			numOfTweets = len(decoded)
			myseq = range(0, numOfTweets)
			temp_tweetids = []
			for i in myseq:
				temp_tweet_text = decoded[i]["text"]	
				print (temp_tweet_text.encode("utf-8"))		#debug and dev
				temp_tweetids.append(decoded[i]["id_str"])
			print "---------------------------------------------- END get_tweets ----"
			return temp_tweetids

"""  This can run once per minute, set it to once every 70 sec to be safe  """
def get_retweeters(tweetid):
	print "****************************  get_retweeters ********************************"
	gr_baseURL = "https://api.twitter.com/1.1/statuses/retweeters/ids.json"
	gr_tweetid = "id=" + tweetid
	gr_stringify = "stringify_ids=true"
	gr_FullURL = gr_baseURL + '?' + gr_tweetid + '&' + gr_stringify
	print gr_FullURL
	
	if __name__ == "__main__":
		if not OAUTH_TOKEN:
			print "something went wrong with Authentication"
		else:
			oauth = get_oauth()
			gr_r = requests.get(url=gr_FullURL, auth=oauth)
			gr_temp_json = json.dumps(gr_r.json(), indent=4, sort_keys=True)
			gr_decoded = json.loads(gr_temp_json) 
			tempTest = gr_decoded["ids"]
			if tempTest:
				print "Yes, there are retweets"
				print "---------------------------------------------- END get_retweeters ----"
				return tempTest
			else:
				print "No, there aren't retweets"
				print "---------------------------------------------- END get_retweeters ----"
				return
				

""" Follow the user - Yes rate limited, not sure what the rate is"""
def follow_user(userid):
	print "****************************  follow_user ********************************"
	#http://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
	fu_id = userid	#need to check if this userid has ever been followed before (Database)
	fu_NotifyUser = "follow=true"
	fu_userid = "user_id=" + userid
	fu_baseURL = "https://api.twitter.com/1.1/friendships/create.json"
	fu_fullURL = fu_baseURL + '?' + fu_userid + '&' + fu_NotifyUser		#follow user
	print fu_fullURL
	
	if __name__ == "__main__":
		if not OAUTH_TOKEN:
			print "something went wrong with Authentication"
		else:
			oauth = get_oauth()
			fu_r = requests.post(url=fu_fullURL, auth=oauth)

def get_followers():
	print "****************************  get_followers ********************************"
	#get followers
	gfol_baseURL = "https://api.twitter.com/1.1/followers/ids.json"
	gfol_cursor = '-1'
	#gfol_fullURL = gfol_baseURL + '?' + 'cursor=' + gfol_cursor + '&' + 'screen_name=' + MY_SCREEN_NAME + '&' + 'count=6' + '&' + 'stringify_ids=true'
	gfol_fullURL = gfol_baseURL + '?' + 'screen_name=' + MY_SCREEN_NAME + '&' + 'stringify_ids=true'
	print gfol_fullURL
	if __name__ == "__main__":
		if not OAUTH_TOKEN:
			print "something went wrong with Authentication"
		else:
			oauth = get_oauth()
			gfol_r = requests.get(url=gfol_fullURL, auth=oauth)
			gfol_temp_json = json.dumps(gfol_r.json(), indent=4, sort_keys=True)
			gfol_decoded = json.loads(gfol_temp_json)
			#print gfol_temp_json
			print "---------------------------------------------- END get_followers ----"
			return gfol_decoded["ids"]
	
	print "---------------------------------------------- END get_followers ----"
	
	
def get_friends():
	print "****************************  get_friends ********************************"
	#get friends
	gfri_baseURL = "https://api.twitter.com/1.1/friends/ids.json"
	gfri_cursor = '-1'
	#gfri_fullURL = gfri_baseURL + '?' + 'cursor=' + gfri_cursor + '&' + 'screen_name=' + MY_SCREEN_NAME + '&' + 'count=108' + '&' + 'stringify_ids=true'
	gfri_fullURL = gfri_baseURL + '?' + 'screen_name=' + MY_SCREEN_NAME + '&' + 'stringify_ids=true'
	print gfri_fullURL
	if __name__ == "__main__":
		if not OAUTH_TOKEN:
			print "something went wrong with Authentication"
		else:
			oauth = get_oauth()
			gfri_r = requests.get(url=gfri_fullURL, auth=oauth)
			gfri_temp_json = json.dumps(gfri_r.json(), indent=4, sort_keys=True)
			gfri_decoded = json.loads(gfri_temp_json)
			print gfri_temp_json
			print "---------------------------------------------- END get_friends ----"
			return gfri_decoded["ids"]

			
def unfollow(userid):
	print "****************************  unfollow ********************************"
	unf_baseURL = "https://api.twitter.com/1.1/friendships/destroy.json"
	unf_userid = userid
	unf_fullURL = unf_baseURL + '?' + 'user_id=' + unf_userid
	print unf_fullURL
	if __name__ == "__main__":
		if not OAUTH_TOKEN:
			print "something went wrong with Authentication"
		else:
			oauth = get_oauth()
			unf_r = requests.post(url=unf_fullURL, auth=oauth)
			unf_temp_json = json.dumps(unf_r.json(), indent=4, sort_keys=True)
			unf_decoded = json.loads(unf_temp_json)
			#print unf_temp_json
			#print unf_temp_json
			
			unf_unfollowed_id = unf_decoded["id_str"]
			unf_unfollowsn = unf_decoded["screen_name"]
			print "unfollowing: " + unf_unfollowsn + " - id: " + unf_unfollowed_id
			
			print "---------------------------------------------- END unfollow ----"
			return
			
			

print get_limits()			

print get_tweets("ESPN_Big12", "5")
