q = open("q.txt","r").readlines()
keywords = [i.strip() for i in q] # Strip any leading/trailing whitespace from list items
# Generate queries formatted for the Search and Streaming API respectively.
searchquery = " OR ".join(keywords)
streamingquery = keywords # same format