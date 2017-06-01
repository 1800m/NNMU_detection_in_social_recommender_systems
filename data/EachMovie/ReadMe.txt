The data set is available as eachmoviedata.tar.gz (zipped tab-separated-value text files, 17632000 bytes compressed). There are three tables, one per file:

Person (person.txt) provides optional, unaudited demographic data supplied by each person:
ID: Number -- primary key
Age: Number
Gender: Text -- one of "M", "F"
Zip_Code: Text
Movie (movie.txt) provides descriptive information about each movie:
ID: Number -- primary key
Name: Text
PR_URL: Text -- URL of studio PR site
IMDb_URL: Text -- URL of Internet Movie Database entry
Theater_Status: Text -- either "old" or "current"
Theater_Release: Date/Time
Video_Status: Text -- either "old" or "current"
Video_Release: Date/Time
Action, Animation, Art_Foreign, Classic, Comedy, Drama, Family, Horror, Romance, Thriller: Yes/No
IMDb URLs are provided by courtesy of Internet Movie Database.

The theater and video status and release dates were (approximately) correct in the San Francisco bay area as of September 15, 1997, when EachMovie was terminated.

Vote (vote.txt) is the actual rating data:
Person_ID: Number
Movie_ID: Number
Score: Number -- 0 <= Score <= 1
Weight: Number -- 0 < Weight <= 1
Modified: Date/Time
