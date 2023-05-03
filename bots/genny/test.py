import tweepy

C_KEY_PROD = "TBD"
C_SECRET_PROD = "TBD"
A_TOKEN_PROD = "TBD"
A_TOKEN_SECRET_PROD = "TBD"
auth = tweepy.OAuthHandler(C_KEY_PROD, C_SECRET_PROD)
auth.set_access_token(A_TOKEN_PROD, A_TOKEN_SECRET_PROD)
api = tweepy.API(auth)
message = "just checking if mr elon is still gonna let me post to this account :^)\n\nnice"
api.update_status(message)
